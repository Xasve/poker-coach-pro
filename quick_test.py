#!/usr/bin/env python3
"""
PRUEBA RÁPIDA - Poker Coach Pro
Verifica que todo funcione correctamente.
"""

import sys
import os
from pathlib import Path

print("⚡ PRUEBA RÁPIDA DEL SISTEMA")
print("=" * 50)

# 1. Verificar Python
print("\n1. 🐍 Verificando Python...")
print(f"   Versión: {sys.version.split()[0]}")
if "3.11" in sys.version:
    print("   ✅ Python 3.11 detectado")
else:
    print("   ⚠️  Versión diferente a 3.11")

# 2. Verificar estructura
print("\n2. 📁 Verificando estructura...")
folders = ["src", "config", "data", "logs"]
all_ok = True

for folder in folders:
    path = Path(folder)
    if path.exists():
        print(f"   ✅ {folder}/")
    else:
        print(f"   ❌ {folder}/ (FALTANTE)")
        all_ok = False

# 3. Verificar módulos principales
print("\n3. 🔍 Verificando módulos en src/...")
src_path = Path("src")
if src_path.exists():
    modules_found = []
    for item in src_path.rglob("*.py"):
        if not item.name.startswith("__") and "pycache" not in str(item):
            rel_path = item.relative_to(src_path)
            modules_found.append(str(rel_path))
    
    print(f"   📦 Módulos encontrados: {len(modules_found)}")
    for module in modules_found[:8]:  # Mostrar primeros 8
        print(f"     • {module}")
    if len(modules_found) > 8:
        print(f"     ... y {len(modules_found) - 8} más")
else:
    print("   ❌ Carpeta src/ no encontrada")
    all_ok = False

# 4. Verificar imports básicos
print("\n4. 📦 Verificando imports básicos...")
basic_imports = ["json", "os", "sys", "pathlib", "time"]
for imp in basic_imports:
    try:
        __import__(imp)
        print(f"   ✅ {imp}")
    except:
        print(f"   ❌ {imp}")

# 5. Verificar imports avanzados (opcional)
print("\n5. 🔧 Verificando imports avanzados...")
advanced_imports = [
    ("cv2", "OpenCV (procesamiento de imágenes)"),
    ("numpy", "NumPy (cálculos numéricos)"),
    ("pyautogui", "PyAutoGUI (automatización)"),
    ("PIL", "Pillow (imágenes)")
]

for imp, desc in advanced_imports:
    try:
        if imp == "PIL":
            from PIL import Image
        else:
            __import__(imp)
        print(f"   ✅ {imp} - {desc}")
    except ImportError:
        print(f"   ⚠️  {imp} - {desc} (NO INSTALADO)")

# Resultado final
print("\n" + "=" * 50)
if all_ok:
    print("✅ SISTEMA LISTO PARA USAR")
    print("\n🎯 Ejecuta: python poker_coach_working.py")
else:
    print("⚠️  ALGUNOS PROBLEMAS DETECTADOS")
    print("\n💡 Soluciones:")
    print("1. Ejecuta: pip install -r requirements.txt")
    print("2. Crea las carpetas faltantes manualmente")
    print("3. Verifica que los archivos estén en src/")

print("\n📋 Comandos disponibles:")
print("   • python poker_coach_working.py  (sistema principal)")
print("   • python quick_test.py           (verificar sistema)")
print("=" * 50)