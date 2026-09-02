import hashlib, json, os, time

STATE="state.json"

def fingerprint(signal):
    raw=json.dumps({
        "symbol":signal["symbol"],
        "direction":signal["direction"],
        "entry_bucket":round(signal["entry"],2),
        "tp1":round(signal["tp1"],2)
    },sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:20]

def load():
    if not os.path.exists(STATE): return {}
    try:
        with open(STATE,"r") as f: return json.load(f)
    except: return {}

def allow(signal, cooldown_seconds):
    st=load()
    fp=fingerprint(signal)
    now=time.time()
    if fp in st and now-st[fp] < cooldown_seconds:
        return False, fp
    st[fp]=now
    with open(STATE,"w") as f: json.dump(st,f)
    return True, fp
