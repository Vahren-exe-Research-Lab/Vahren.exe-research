# E-owned T020 static source gate; does not start/modify the game or index.
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "rea_lab" / "headless_analysis" / "search_index"
FIXTURE = Path(__file__).with_name("T020_V9_STATIC_PROVENANCE_NEGATIVES_20261024_09H.json")
EXPECTED_DB = "2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE"
EXPECTED_CLI = "6B3333571CD3E2E97BB6E6DBFD85D751EA869903998C93E49E70FB3461547896"
EXPECTED_EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def digest(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()

def classify(c):
    if c["index"] != "V9":
        return "HISTORICAL_REPLAY_ONLY"
    if c["db_hash"] != "match":
        return "REJECT_INDEX_HASH"
    if c["exe_hash"] != "match":
