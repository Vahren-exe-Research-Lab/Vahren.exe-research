"""Read-only parser for the fixed playback-v3 diagnostic sequence.
Usage: python analyze_playback.py <playback.log> <run.json> <summary.json>
Raw paths, PID/TID and absolute ticks are deliberately excluded from output.
"""
import collections, hashlib, json, re, sys
from pathlib import Path

def analyze(log, receipt):
    raw = Path(log).read_bytes()
    events = []
    for line in raw.decode("utf-8").splitlines():
        m = re.fullmatch(r"tick=(\d+) tid=(\d+) event=([A-Z_0-9]+) value=(-?\d+)", line)
        if not m:
            raise ValueError("Unrecognized log record")
        tick, tid, event, value = m.groups()
        events.append((int(tick), int(tid), event, int(value)))
    def vals(key):
        return [e[3] for e in events if e[2] == key]
    def need(ok, why):
        if not ok:
            raise ValueError(why)
    need(len({e[1] for e in events}) == 1, "Expected one owner thread")
    need(events[-1][2:] == ("END", 0), "Missing final END")
    need(vals("PLAYBACK_BEGIN") == [3], "Wrong diagnostic")
    for key in ("PLAY_FIRST_RESULT", "PLAY_SECOND_RESULT", "VOLUME_RESULT",
                "STOP_FIRST_RESULT", "STOP_SECOND_RESULT", "PLAYBACK_RESULT"):
        need(vals(key) == [0], key)
    for key in ("OPEN_RETURN", "CLEAR_RETURN", "WAVE_OPEN_RESULT",
                "PREPARE_RESULT", "INITIAL_VOLUME_RESULT", "WRITE_RESULT"):
        need(vals(key) == [0, 0], key)
    need(vals("DECODE_EOF") == [1, 1], "Two EOFs required")
    need(vals("LOOP_REQUEST") == [1, 1], "Loop configuration")
    need(vals("WAIT_MS") == [3000, 3000, 3000, 2000], "Scenario timing")
    need(vals("LIVE_VOICES") == [1, 2, 2, 1], "Scenario resources")
    need(vals("FIRST_HANDLE") == [1] and vals("SECOND_HANDLE") == [2], "Handles")
    starts = [i for i, e in enumerate(events) if e[2] == "OPEN_BEGIN"]
    need(len(starts) == 2, "Two open lifecycles")
    cycles = []
    for start in starts:
        end = next(i for i in range(start, len(events)) if events[i][2] == "PCM_BYTES")
        block = events[start:end+1]
        reads = [e[3] for e in block if e[2] == "READ_RETURN"]
        total = block[-1][3]
        need(reads and reads[-1] == 0 and all(0 < x <= 16384 and x % 4 == 0 for x in reads[:-1]), "Signed read/EOF/frame invariant")
        need(sum(reads) == total, "PCM byte sum")
        need([e[3] for e in block if e[2] == "CHANNELS"] == [2], "Channels")
        need([e[3] for e in block if e[2] == "RATE"] == [44100], "Rate")
        cycles.append({"pcm_bytes": total, "pcm_frames": total//4,
                       "duration_seconds": total/(4*44100), "channels": 2, "rate": 44100, "bits": 16,
                       "positive_read_count": len(reads)-1,
                       "read_return_histogram": dict(sorted(collections.Counter(reads).items())),
                       "eof_observed": True, "clear_return": 0})
    positions = []
    for i, e in enumerate(events):
        if e[2] == "POSITION_HANDLE":
            block = events[i:i+5]
            need([x[2] for x in block] == ["POSITION_HANDLE", "POSITION_RESULT", "POSITION_TYPE", "POSITION_SAMPLES", "BUFFER_FLAGS"], "Position layout")
            need(block[1][3] == 0 and block[2][3] == 2, "Position API/format")
            positions.append({"handle": e[3], "samples": block[3][3], "buffer_flags": block[4][3]})
    need([p["handle"] for p in positions] == [1,1,2,1,2,2], "Position sequence")
    for handle in (1, 2):
        samples = [p["samples"] for p in positions if p["handle"] == handle]
        need(all(b > a for a,b in zip(samples,samples[1:])), "Position progression")
    r = json.loads(Path(receipt).read_text(encoding="utf-8-sig"))
    return {
        "research_id": "REA-T015-OGG-REUSE-20261105",
        "status": "HOST_DECODE_AND_DLL_AUDIO_OBSERVED_BGM_VOLUME_ISOLATION_UNRESOLVED",
        "raw_log_sha256": hashlib.sha256(raw).hexdigest(),
        "raw_log_bytes": len(raw), "events": len(events),
        **{k:r[k] for k in ("game_sha256","dll_sha256","runner_sha256","source_sha256")},
        "cycles": cycles, "positions": positions, "live_voices": vals("LIVE_VOICES"),
        "volume_api_return": 0, "stop_api_returns": [0,0], "end_recorded": True,
        "user_report": {
            "additional_audio_heard": True, "bgm_uninterrupted": True,
            "additional_audio_stopped": True, "post_test_game_operable": True,
            "bgm_volume": "User suspects BGM became quieter; magnitude/timing unmeasured"
        },
        "limitations": [
            "Two sequential full decodes of one normal OGG, not concurrent DLL decoder contexts",
            "No PCM content hash or reference-decoder equivalence in v3",
            "Position progression supports queued playback; not independent loop-boundary audibility proof",
            "Successful volume API call does not prove per-voice isolation",
            "BGM session volume before diagnostic was not logged",
            "No malformed inputs, leak measurement, DAT integration or long-duration coverage"
        ]
    }

if __name__ == "__main__":
    result = analyze(sys.argv[1],sys.argv[2])
    Path(sys.argv[3]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
