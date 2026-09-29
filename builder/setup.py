from setuptools import setup, Extension
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
include_dirs = [os.path.join(base_dir, 'core', 'include')]

# ดึงไฟล์ C ทั้งหมดใน core/src/ เข้ามาร่วม Compile
sources_list = [
    os.path.join(base_dir, 'core', 'src', 'container_core.c')
]

vip_embedder_path = os.path.join(base_dir, 'core', 'src', 'vip_data_embedder.c')
if os.path.exists(vip_embedder_path) and os.path.getsize(vip_embedder_path) > 0:
    sources_list.append(vip_embedder_path)

active_defense_module = Extension(
    'active_defense_v27',
    sources=sources_list,
    include_dirs=include_dirs,
    libraries=['winhttp', 'Advapi32', 'User32', 'Kernel32'] if sys.platform == 'win32' else [],
    extra_compile_args=['/O2', '/DWIN32_LEAN_AND_MEAN'] if sys.platform == 'win32' else ['-O3']
)

setup(
    name='active_defense_v27',
    version='1.0',
    description='Bangsaen AI Labs Sovereign Active Defense C-Container',
    ext_modules=[active_defense_module]
)