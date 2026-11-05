"""Summarize a playback-v4 run without exporting private paths, PID/TID or session IDs.
Usage: python analyze_playback_v4.py LOG RECEIPT SESSION_BEFORE SESSION_AFTER OUTPUT
"""
from pathlib import Path
import hashlib,json,re,sys

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def analyze(log,receipt,before,after):
    raw=Path(log).read_bytes()
    events=[]
    for line in raw.decode("utf-8-sig").splitlines():
        m=re.fullmatch(r"tick=(\d+) tid=(\d+) event=([A-Z_0-9]+) value=(-?\d+)",line)
        if not m:raise ValueError("Unexpected log line")
        tick,tid,event,value=m.groups()
        events.append((int(tick),int(tid),event,int(value)))
    def values(key):return [x[3] for x in events if x[2]==key]
    def require(condition,why):
        if not condition:raise ValueError(why)
    require(len({x[1] for x in events})==1,"One worker")
    require(values("PLAYBACK_BEGIN")==[4],"Version")
    require(events[-1][2:]==("END",0),"End")
    for key in ("PLAY_FIRST_RESULT","PLAY_SECOND_RESULT","VOLUME_RESULT","STOP_FIRST_RESULT","STOP_SECOND_RESULT","PLAYBACK_RESULT"):
        require(values(key)==[0],key)
    for key in ("OPEN_RETURN","CLEAR_RETURN","DS_BUFFER_RESULT","DS_LOCK_RESULT","DS_UNLOCK_RESULT","DS_PLAY_RESULT","DS_STOP_RESULT"):
        require(values(key)==[0,0],key)
    require(values("DS_VOLUME_RESULT")==[0,0,0],"Volume calls")
    require(values("DECODE_EOF")==[1,1],"EOF")
    require(values("PCM_BYTES")==[1007616,1007616],"PCM bytes")
    require(values("CHANNELS")==[2,2] and values("RATE")==[44100,44100],"Format")
    require(values("LIVE_VOICES")==[1,2,2,1],"Voices")
    starts=[i for i,x in enumerate(events) if x[2]=="OPEN_BEGIN"]
    require(len(starts)==2,"Two lifecycles")
    counts=[]
    for start in starts:
        end=next(i for i in range(start,len(events)) if events[i][2]=="PCM_BYTES")
        reads=[x[3] for x in events[start:end+1] if x[2]=="READ_RETURN"]
        require(reads[-1]==0 and all(0<x<=16384 and x%4==0 for x in reads[:-1]),"Read bounds")
        require(sum(reads)==1007616,"Read sum")
        counts.append(len(reads)-1)
    samples=[]
    for i,x in enumerate(events):
        if x[2]=="POSITION_HANDLE":
            block=events[i:i+7]
            require([y[2] for y in block]==["POSITION_HANDLE","POSITION_RESULT","POSITION_BYTES","STATUS_RESULT","BUFFER_STATUS","GET_VOLUME_RESULT","BUFFER_VOLUME_DB100"],"Position block")
            require(block[1][3]==block[3][3]==block[5][3]==0,"Getter success")
            require(block[4][3]==5 and 0<=block[2][3]<1007616,"Playing/looping/cursor")
            samples.append({"handle":x[3],"cursor_bytes":block[2][3],"status":block[4][3],"volume_db100":block[6][3]})
    require([s["handle"] for s in samples]==[1,1,2,1,2,2],"Handle sample order")
    require([s["volume_db100"] for s in samples if s["handle"]==1]==[-1046,-1046,-2602],"Voice 1 volume")
    require([s["volume_db100"] for s in samples if s["handle"]==2]==[-1398,-1398,-1398],"Voice 2 unchanged")
    def session(path):
        text=Path(path).read_text(encoding="utf-8-sig")
        require("AUDIT_ERRORS=0" in text and "MATCHES=1" in text,"Audit complete")
        require(not re.search(r"hr=(?!00000000)[0-9a-fA-F]{8}",text),"Audit getter errors")
        ids=re.findall(r"^SESSION_ID_HASH=([0-9a-f]{16})$",text,re.M)
        masters=re.findall(r"^MASTER value=([0-9.eE+-]+) hr=00000000$",text,re.M)
        mutes=re.findall(r"^MUTE value=([01]) hr=00000000$",text,re.M)
        channels=re.findall(r"^CHANNEL index=(\d+) value=([0-9.eE+-]+) hr=00000000$",text,re.M)
        require(len(ids)==len(masters)==len(mutes)==1 and len(channels)==2,"Audit fields")
        require([int(c[0]) for c in channels]==[0,1],"Channel indices")
        return ids[0],{"master":float(masters[0]),"mute":int(mutes[0]),"channels":[float(c[1]) for c in channels]}
    aid,a=session(before);bid,b=session(after)
    require(aid==bid and a==b,"Same session unchanged")
    r=json.loads(Path(receipt).read_text(encoding="utf-8-sig"))
    return {
        "research_id":"REA-T015-OGG-REUSE-20261105",
        "status":"HOST_DECODE_DS_SECONDARY_PLAYBACK_AND_VOLUME_ISOLATION_OBSERVED_LIMITED_RUN",
        "raw_log_sha256":digest(log),"raw_log_bytes":len(raw),"events":len(events),
        "session_before_log_sha256":digest(before),"session_after_log_sha256":digest(after),
        "identities":{k:v for k,v in r.items() if k.endswith("_sha256")},
        "decode_cycles":2,"pcm_bytes_per_cycle":1007616,"frames_per_cycle":251904,
        "channels":2,"rate":44100,"bits":16,"positive_reads_per_cycle":counts,
        "eof_and_clear_success":True,"samples":samples,"live_voices":[1,2,2,1],
        "same_session":True,"session_before":a,"session_after":b,
        "user_report":{"bgm_volume_unchanged_during_v4":True,"game_quiet_since_startup":True,
                       "v4_additional_audio_and_operability_separately_reconfirmed":False,
                       "volume_restoration_confirmed":False},
        "interpretation":"Persistent session attenuation from v3 is consistent with pre-v4 master about 0.05; pre-v3 baseline unknown.",
        "limitations":["One normal OGG and one short v4 run","Snapshots do not exclude transient session changes",
                       "Cursor wrap/status are API observations, not proof of gapless audible loops",
                       "No malformed-input, leak, all-WAV coexistence, device-loss or DAT integration test"]
    }
if __name__=="__main__":
    result=analyze(*sys.argv[1:5])
    Path(sys.argv[5]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
