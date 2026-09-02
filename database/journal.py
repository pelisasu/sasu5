import json, os, time

PATH="journal.jsonl"

def log_event(row):
    row=dict(row)
    row.setdefault("timestamp", int(time.time()))
    with open(PATH,"a",encoding="utf-8") as f:
        f.write(json.dumps(row,ensure_ascii=False)+"\n")
