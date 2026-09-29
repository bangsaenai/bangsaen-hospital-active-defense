import os
import sys
import json
from datetime import datetime

# เพิ่ม Path ไปยังโฟลเดอร์ releases เพื่อโหลด C-Native active_defense_v27.pyd
releases_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../releases'))
sys.path.append(releases_dir)

def run_sovereign_audit():
    print("==================================================================")
    print("   BANGSAEN AI LABS - SOVEREIGN AUDIT & EXTRACTION PROTOCOL")
    print("==================================================================")
    print("[1] Verifying Auditor Credentials & Master Token...")

    # ตรวจสอบ Master Bearer Token ของฝ่าย Auditor
    audit_token = os.getenv("BANGSAEN_GCP_AUTH_BEARER")
    
    if audit_token != "BSH_GCP_LIVE_TOKEN_2026":
        print("[AUDIT REJECTED] Unauthorized Access: Missing or Invalid Master Token.")
        print("[SECURITY NOTICE] Audit protocol terminated to prevent data breach.")
        print("==================================================================")
        return

    print("[2] Credentials Verified. Requesting Ephemeral Key from Cloud KMS...")
    
    try:
        import active_defense_v27 as container
        print("[3] Invoking C-Core Extract Engine into RAM Space...")
        
        # เรียกฟังก์ชัน C-Native เพื่อถอดรหัสข้อมูลประวัติคนไข้ VIP
        raw_json_str = container.extract_vip_context()
        
        if not raw_json_str:
            print("[AUDIT FAILED] Null-Space Shredder executed or memory zeroed.")
            return

        print("\n[AUDIT SUCCESS] Decrypted VIP Patient Data Successfully Extracted!")
        
        # แสดงผลบน Terminal
        parsed_json = json.loads(raw_json_str)
        print(json.dumps(parsed_json, indent=2, ensure_ascii=False))

        # บันทึกลงไฟล์ Audit Report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"audit_record_dump_{timestamp}.json"
        
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(raw_json_str)
            
        print(f"\n[AUDIT TRAIL] Forensic log exported to: {report_filename}")
        print("==================================================================")

    except Exception as e:
        print(f"\n[AUDIT ERROR] Extraction process failed: {e}")
        print("==================================================================")

if __name__ == "__main__":
    run_sovereign_audit()