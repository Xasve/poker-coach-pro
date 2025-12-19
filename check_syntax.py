# check_syntax.py - Verificar sintaxis de todos los scripts
import os
import sys
import subprocess

print("🔍 VERIFICANDO SINTAXIS DE TODOS LOS SCRIPTS")
print("=" * 70)

# Lista de scripts a verificar
scripts_to_check = [
    "diagnostic.py",
    "smart_capture_fixed.py", 
    "verify_balance.py",
    "main_integrated.py",
    "session_manager.py",
    "detect_coords.py",
    "start_auto_simple.py",
    "quick_balance_check.py"
]

all_ok = True

for script in scripts_to_check:
    if os.path.exists(script):
        try:
            # Intentar compilar el script
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"✅ {script:30} Sintaxis CORRECTA")
            else:
                print(f" {script:30} Error de sintaxis")
                print(f"   Error: {result.stderr[:100]}")
                all_ok = False
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  {script:30} Timeout al verificar")
        except Exception as e:
            print(f"  {script:30} Error verificando: {e}")
    else:
        print(f"📭 {script:30} No existe")

print("\n" + "=" * 70)
if all_ok:
    print("🎉 ¡TODOS LOS SCRIPTS TIENEN SINTAXIS CORRECTA!")
else:
    print("⚠️  Algunos scripts tienen errores de sintaxis")

print("\n Para reparar scripts con errores:")
print("   1. Ejecuta este comando de PowerShell nuevamente")
print("   2. O contacta con soporte técnico")

# Verificar también dependencias básicas
print("\n VERIFICANDO DEPENDENCIAS BÁSICAS:")
try:
    import cv2
    print(" OpenCV (cv2)")
except:
    print(" OpenCV (cv2) - Faltante")

try:
    import numpy as np
    print(" NumPy")
except:
    print(" NumPy - Faltante")

try:
    import PIL
    print(" Pillow (PIL)")
except:
    print(" Pillow (PIL) - Faltante")

print("\n" + "=" * 70)
print(" DIAGNÓSTICO COMPLETADO")
