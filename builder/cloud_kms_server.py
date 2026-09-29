from fastapi import FastAPI, Header, HTTPException
import time
import hashlib

app = FastAPI(title="Bangsaen AI Labs - Sovereign Cloud KMS Gateway")

# Master Seed เก็บไว้เฉพาะบน GCP Cloud (ไม่หลุดไปใน .pyd)
GCP_MASTER_SEED = "BANGSAEN_HOSPITAL_SOVEREIGN_MASTER_SEED_2026"

@app.get("/v1/auth-key")
def get_dynamic_60s_key(authorization: str = Header(None)):
    # 1. Verify Authorization Token
    if not authorization or authorization != "Bearer BSH_GCP_LIVE_TOKEN_2026":
        raise HTTPException(status_code=403, detail="[GCP KMS] 403 Forbidden: Invalid Cryptographic Proof")
    
    # 2. คำนวณ 60s Dynamic Time Window
    current_time_window = int(time.time()) // 60
    
    # 3. เจน 256-bit Dynamic Key จาก Master Seed + Time Window
    raw_key_material = f"{GCP_MASTER_SEED}:{current_time_window}"
    dynamic_key_hex = hashlib.sha256(raw_key_material.encode('utf-8')).hexdigest()
    
    return {
        "status": "GRANTED",
        "time_window": current_time_window,
        "ephemeral_key": dynamic_key_hex,
        "ttl_seconds": 60 - (int(time.time()) % 60)
    }