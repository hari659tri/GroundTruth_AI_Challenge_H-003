# utils.py
import os
import zipfile
import json

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def make_zip(output_zip: str, files: list):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f, arcname in files:
            zf.write(f, arcname)

def save_metadata(metadata: dict, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
