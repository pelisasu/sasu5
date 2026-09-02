import json, os

def load_journal(path="journal.jsonl"):
    if not os.path.exists(path):
        return []
    out=[]
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            try: out.append(json.loads(line))
            except: pass
    return out

def performance_gate(settings, path="journal.jsonl"):
    rows=load_journal(path)
    resolved=[x for x in rows if x.get("result") in ("WIN","LOSS")]
    if len(resolved) < settings.min_resolved_for_gate:
        return True, f"WARMUP:{len(resolved)}/{settings.min_resolved_for_gate}"
    wins=sum(x["result"]=="WIN" for x in resolved[-settings.min_resolved_for_gate:])
    wr=wins/settings.min_resolved_for_gate
    if wr < settings.min_target_win_rate:
        return False, f"PAUSED_ROLLING_WIN_RATE:{wr:.2%}"
    return True, f"ROLLING_WIN_RATE:{wr:.2%}"
