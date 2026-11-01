"""Saved Ghidra 0x470830 string-writer byte-level microcontract.

The target validates the entire std::string before writing any content.
If *any* byte is <0x20 or >0x7F it writes only a terminating NUL.
Otherwise it writes all string bytes followed by NUL. DEL 0x7F is allowed.
The reader and caller-side recovery of malformed values are NOT modeled.
"""
from __future__ import annotations

def write_native_cstring(raw:bytes)->bytes:
    """Single native writer 0x470830 operation (pre-encryption payload)."""
    if not isinstance(raw,bytes):
        raise TypeError("native string writer fixture requires bytes")
    if any(value<0x20 or value>0x7F for value in raw):
        return b"\x00"
    return raw+b"\x00"
