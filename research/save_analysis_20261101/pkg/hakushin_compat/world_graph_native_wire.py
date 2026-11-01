"""World map Spot/Path/EscapePath saved STREAM shape, Vahren 0.67.

Saved Ghidra + native vtables / RTTI:
 * 0x435C10 writer: classify graph object SpotElm-derived / SpotPath /
   SpotEscapePath into three ordered buckets, virtual method +0x60.
 * 0x5A93F0: Spot::vf24 writes string plus (byte+0x88) zero-extended u32;
   caller in 0x435C10 wrote object key just before method.
 * 0x5B0600: SpotPath/EscapePath::vf24 emits string+0x6C,
   (byte+0x88) as u32, string+0x1E8, string+0x204,
   string+0x220, raw u32+0x23C.
 * Actual saves have runtime bucket markers "00000000", "11111111",
   "22222222", "33333333". Static initial global fields at
   0x65C828 / 0x65C844 / 0x65C860 / 0x65C87C were empty in .data;
   do not assume the string contents for all scenarios/builds.

This is BYTE serializer/reader, not native in-memory polymorphic objects,
graph reference resolution, route movement, diplomacy or gameplay parity.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from struct import pack,unpack_from

from .real_save_frontmatter import _read_native_ascii_z
from .save_envelope import SaveFormatError

RUNTIME_MARKERS=(b"00000000",b"11111111",b"22222222",b"33333333")
MAX_BUCKET_ITEMS=5000


def _check_text(b:bytes,label:str,*,nonempty=True)->bytes:
    if type(b) is not bytes or len(b)>65536 or (nonempty and not b):
        raise SaveFormatError(label+": native nonempty ASCII bytes required")
    if any(c<0x20 or c>0x7f for c in b):
        raise SaveFormatError(label+": native writer would collapse invalid text")
    if b in RUNTIME_MARKERS:
        raise SaveFormatError(label+": conflicts with runtime bucket sentinel")
    return b


def _u32(n:int,name:str)->int:
    if type(n) is not int or not 0<=n<=0xffffffff:
        raise SaveFormatError(name+": unsigned raw DWORD required")
    return n


def _read_u32(blob:bytes,pos:int)->tuple[int,int]:
    if pos+4>len(blob):
        raise SaveFormatError("world graph truncated raw u32")
    return unpack_from("<I",blob,pos)[0],pos+4


def _read_marker_or_key(blob:bytes,pos:int)->tuple[bytes,int]:
    if type(blob) is not bytes or type(pos) is not int or not 0<=pos<len(blob):
        raise SaveFormatError("world graph cursor out of bounds")
    return _read_native_ascii_z(blob,pos)


@dataclass(frozen=True,slots=True)
class NativeWorldSpot:
    key:bytes
    serialized_spot_name:bytes
    memory_byte_88:int

    def pack(self)->bytes:
        if _u32(self.memory_byte_88,"Spot+0x88")>255:
            raise SaveFormatError("Spot byte stored as u32 outside 0..255")
        return (_check_text(self.key,"Spot graph key")+b"\x00"+
                _check_text(self.serialized_spot_name,"Spot saved name")+b"\x00"+
                pack("<I",self.memory_byte_88))


@dataclass(frozen=True,slots=True)
class NativeWorldPath:
    key:bytes
    serialized_name_6c:bytes
    memory_byte_88:int
    endpoint_name_1e8:bytes
    endpoint_name_204:bytes
    route_name_220:bytes
    raw_u32_23c:int

    def pack(self)->bytes:
        if _u32(self.memory_byte_88,"Path+0x88")>255:
            raise SaveFormatError("Path byte stored as u32 outside 0..255")
        result=bytearray()
        for label,data in (("Path key",self.key),
                           ("Path+0x6C",self.serialized_name_6c)):
            result+=_check_text(data,label)+b"\x00"
        result+=pack("<I",self.memory_byte_88)
        for label,data in (("Path+0x1E8",self.endpoint_name_1e8),
                           ("Path+0x204",self.endpoint_name_204),
                           ("Path+0x220",self.route_name_220)):
            result+=_check_text(data,label,nonempty=False)+b"\x00"
        result+=pack("<I",_u32(self.raw_u32_23c,"Path+0x23C"))
        return bytes(result)

@dataclass(frozen=True,slots=True)
class NativeWorldGraph:
    spot_elm_bucket:tuple[NativeWorldSpot,...]
    path_bucket:tuple[NativeWorldPath,...]
    escape_path_bucket:tuple[NativeWorldPath,...]

    def pack(self)->bytes:
        out=bytearray()
        for marker,items in zip(RUNTIME_MARKERS,
              (self.spot_elm_bucket,self.path_bucket,self.escape_path_bucket)):
            if len(items)>MAX_BUCKET_ITEMS:
                raise SaveFormatError("world graph bucket exceeds bound")
            out+=marker+b"\x00"
            for item in items:
                out+=item.pack()
        out+=RUNTIME_MARKERS[3]+b"\x00"
        return bytes(out)

    def counts(self)->dict[str,int]:
        return {"Spot_elm_bucket":len(self.spot_elm_bucket),
                "SpotPath_bucket":len(self.path_bucket),
                "SpotEscapePath_bucket":len(self.escape_path_bucket)}


def _read_spot_entry(blob:bytes,pos:int)->tuple[NativeWorldSpot,int]:
    key,pos=_read_marker_or_key(blob,pos)
    name,pos=_read_marker_or_key(blob,pos)
    val,pos=_read_u32(blob,pos)
    if val>255:
        raise SaveFormatError("Spot+88 raw u32 exceeds byte-in-memory")
    return NativeWorldSpot(key,name,val),pos


def _read_path_entry(blob:bytes,pos:int)->tuple[NativeWorldPath,int]:
    key,pos=_read_marker_or_key(blob,pos)
    name,pos=_read_marker_or_key(blob,pos)
    flag,pos=_read_u32(blob,pos)
    if flag>255:
        raise SaveFormatError("Path+88 raw u32 exceeds byte-in-memory")
    src,pos=_read_marker_or_key(blob,pos)
    dst,pos=_read_marker_or_key(blob,pos)
    route,pos=_read_marker_or_key(blob,pos)
    scalar,pos=_read_u32(blob,pos)
    return NativeWorldPath(key,name,flag,src,dst,route,scalar),pos


@dataclass(frozen=True,slots=True)
class WorldGraphByteProof:
    graph:NativeWorldGraph
    start_offset:int
    end_offset:int
    original_sha256:str
    bytes_identical:bool


def read_world_graph(
    blob:bytes,*,offset:int=0
)->WorldGraphByteProof:
    """Read all buckets and require exactly the expected 4 runtime sentinels."""
    if type(blob) is not bytes or type(offset) is not int or not 0<=offset<len(blob):
        raise SaveFormatError("world graph byte offset invalid")
    begin=offset
    marker,pos=_read_marker_or_key(blob,begin)
    if marker!=RUNTIME_MARKERS[0]:
        raise SaveFormatError("unexpected first world graph runtime marker")
    buckets=[]
    for idx,stop in enumerate(RUNTIME_MARKERS[1:]):
        bucket=[]
        for _ in range(MAX_BUCKET_ITEMS):
            key,_=_read_marker_or_key(blob,pos)
            if key==stop:
                pos+=len(stop)+1
                break
            if key in RUNTIME_MARKERS:
                raise SaveFormatError("unexpected world graph bucket marker/order")
            if idx==0:record,pos=_read_spot_entry(blob,pos)
            else:record,pos=_read_path_entry(blob,pos)
            bucket.append(record)
        else:
            raise SaveFormatError("world graph bucket unbounded")
        buckets.append(tuple(bucket))
    graph=NativeWorldGraph(*buckets)
    if graph.pack()!=blob[begin:pos]:
        raise SaveFormatError("world graph writer readback bytes differ")
    return WorldGraphByteProof(graph,begin,pos,
                              sha256(blob[begin:pos]).hexdigest(),True)

