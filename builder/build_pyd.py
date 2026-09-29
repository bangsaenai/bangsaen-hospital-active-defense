import os
import sys
import shutil
import subprocess

def apply_chaos_encrypt(data_bytes):
    # เข้ารหัสทุก Byte ด้วย Chaos Seed Matrix ป้องกันคำสั่ง 'strings' สแกนเจอ
    encrypted = bytearray()
    for i, b in enumerate(data_bytes):
        chaos_key = (i * 17 + 0x5A) % 256
        encrypted.append(b ^ chaos_key)
    return encrypted

def run_pipeline():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    json_path = os.path.join(base_dir, 'data_source', 'vip_patients_raw.json')
    header_out_path = os.path.join(base_dir, 'core', 'include', 'generated_vip_data.h')
    releases_dir = os.path.join(base_dir, 'releases')

    print("[1/3] Reading raw VIP dataset...")
    if not os.path.exists(json_path):
        print(f"[ERROR] Cannot find {json_path}")
        return

    with open(json_path, 'rb') as f:
        raw_bytes = f.read()

    # 1. เข้ารหัส Data Bytes ด้วย Chaos Algorithm
    encrypted_bytes = apply_chaos_encrypt(raw_bytes)

    # 2. แปลง Encrypted Bytes เป็น C-Byte Array
    byte_array = [f"0x{b:02x}" for b in encrypted_bytes]
    byte_array_str = ", ".join(byte_array)

    header_content = f"""#ifndef GENERATED_VIP_DATA_H
#define GENERATED_VIP_DATA_H

// Hardened & Encrypted Byte Array (No Plaintext Strings in Binary)
static const unsigned char VIP_RAW_DATA[] = {{ {byte_array_str} }};
static const size_t VIP_RAW_DATA_LEN = {len(raw_bytes)};

#endif
"""
    with open(header_out_path, 'w', encoding='utf-8') as f:
        f.write(header_content)
    print(f"[2/3] Hardened & Encrypted C-Header generated ({len(raw_bytes)} bytes obfuscated).")

    # 3. สั่ง Build C-Extension
    print("[3/3] Compiling C-Native Module (.pyd)...")
    setup_script = os.path.join(base_dir, 'builder', 'setup.py')
    
    cmd = [sys.executable, setup_script, 'build_ext', '--inplace']
    result = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True)

    if result.returncode != 0:
        print("[ERROR] Compilation failed!")
        print(result.stderr)
        return

    pyd_found = False
    for file in os.listdir(base_dir):
        if file.endswith('.pyd') or file.endswith('.so'):
            target_path = os.path.join(releases_dir, 'active_defense_v27.pyd')
            src_path = os.path.join(base_dir, file)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.move(src_path, target_path)
            print(f"[SUCCESS] Binary generated: {target_path}")
            pyd_found = True
            break

if __name__ == '__main__':
    run_pipeline()