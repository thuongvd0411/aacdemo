import os
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_name(name):
    name_without_ext, ext = os.path.splitext(name)
    name_without_ext = remove_accents(name_without_ext)
    name_without_ext = name_without_ext.replace(' ', '_').replace('-', '_')
    name_without_ext = name_without_ext.lower()
    return name_without_ext + ext.lower()

base_dir = r"c:\Users\8470p\Desktop\aac"
dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d[0].isdigit()]

mapping = {}

for d in dirs:
    new_d = normalize_name(d)
    mapping[new_d] = d
    
    old_path = os.path.join(base_dir, d)
    new_path = os.path.join(base_dir, new_d)
    
    if old_path != new_path:
        print(f"Renaming directory: {d} -> {new_d}")
        # Rename files inside first
        for f in os.listdir(old_path):
            old_f_path = os.path.join(old_path, f)
            if os.path.isfile(old_f_path):
                new_f = normalize_name(f)
                new_f_path = os.path.join(old_path, new_f)
                if old_f_path != new_f_path:
                    print(f"  Renaming file: {f} -> {new_f}")
                    os.rename(old_f_path, new_f_path)
        
        os.rename(old_path, new_path)

print("Done renaming. Folder mapping:")
print("FOLDER_MAPPING = {")
for k, v in mapping.items():
    print(f'    "{k}": "{v}",')
print("}")
