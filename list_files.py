#!/usr/bin/env python3
"""
Listar archivos en el repositorio actual
"""
import os

print("📁 CONTENIDO DEL REPOSITORIO")
print("=" * 60)

# Listar todo recursivamente
for root, dirs, files in os.walk("."):
    # Ignorar algunas carpetas
    dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', '.idea']]
    
    level = root.count(os.sep) - 1
    indent = "  " * level
    
    print(f"{indent}{os.path.basename(root)}/")
    
    for file in sorted(files):
        if file.endswith(('.py', '.txt', '.md', '.json')):
            print(f"{indent}  📄 {file}")

print("\n" + "=" * 60)
print("🎯 ARCHIVOS CRÍTICOS QUE DEBEN EXISTIR:")
print("=" * 60)

critical_files = [
    "poker_coach_pro.py",
    "requirements.txt",
    "src/screen_capture/__init__.py",
    "src/screen_capture/stealth_capture.py",
    "src/screen_capture/table_detector.py"
]

missing = []
for file in critical_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - FALTANTE")
        missing.append(file)

if missing:
    print(f"\n⚠️  Faltan {len(missing)} archivos críticos")
else:
    print("\n🎉 Todos los archivos críticos existen")