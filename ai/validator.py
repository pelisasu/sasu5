import json

SYSTEM = """
You are a strict quantitative signal validator.
You must NOT invent prices, candles, indicators, news, broker quotes, or facts.
Only use the numeric/structured data supplied in the user payload.
If data conflicts or is incomplete, reject.
Return JSON only:
{"decision":"APPROVE"|"REJECT","confidence":0-100,"reasons":["..."]}
Approval requires strong M30/M15 alignment and no obvious contradiction.
"""

def validate_with_ai(client, model, payload):
    if client is None:
        return {"decision":"APPROVE","confidence":100,"reasons":["AI_DISABLED_ENGINE_ONLY"]}

    response = client.responses.create(
        model=model,
        input=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":json.dumps(payload, separators=(",",":"))}
        ],
        text={"format":{
            "type":"json_schema",
            "name":"signal_validation",
            "schema":{
                "type":"object",
                "properties":{
                    "decision":{"type":"string","enum":["APPROVE","REJECT"]},
                    "confidence":{"type":"number","minimum":0,"maximum":100},
                    "reasons":{"type":"array","items":{"type":"string"}}
                },
                "required":["decision","confidence","reasons"],
                "additionalProperties":False
            },
            "strict":True
        }}
    )
    text = response.output_text
    return json.loads(text)
