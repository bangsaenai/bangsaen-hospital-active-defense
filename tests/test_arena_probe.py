import sys
import os

# เพิ่มเส้นทางไปยังโฟลเดอร์ releases เพื่อนำเข้า C-Native Active Defense Module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../releases')))

def run_arena_test():
    print("==================================================================")
    print("   BANGSAEN AI LABS - SOVEREIGN LETHAL ACTIVE DEFENSE ARENA (EP.27)")
    print("==================================================================")
    print("[1] Attempting to load C-Native Living Container (.pyd)...")

    try:
        import active_defense_v27 as container
        print("[2] Module loaded successfully into RAM.")
        print("[3] Initiating Telemetry Verification & GCP Cloud KMS Handshake...")
        
        # พยายามสกัดข้อมูลประวัติคนไข้ VIP
        vip_data = container.extract_vip_context()
        
        print("\n[SUCCESS - DEFENSE BREACHED!]")
        print("Raw VIP Patient Record Extracted:")
        print(vip_data)
        print("==================================================================")

    except Exception as e:
        print(f"\n[FAIL - ACTIVE DEFENSE TRIGGERED!]: {e}")
        print("Context Annihilated or Process Terminated by Thanos Shredder.")
        print("==================================================================")

if __name__ == "__main__":
    run_arena_test()