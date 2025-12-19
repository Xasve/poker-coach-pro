# diagnostic.py
import sys
import os

print(" DIAGNÓSTICO DEL SISTEMA POKER COACH")
print("=" * 60)

# 1. Verificar Python
print(f"Python: {sys.version}")

# 2. Verificar estructura
print("\n Estructura de archivos:")
for item in ['src/', 'data/card_templates/pokerstars/', 'config/']:
    if os.path.exists(item):
        print(f" {item}")
    else:
        print(f" {item}")

# 3. Verificar PokerStars abierto (Windows)
print("\n Buscando PokerStars...")
try:
    import psutil
    poker_processes = [p for p in psutil.process_iter(['name']) if 'poker' in p.info['name'].lower()]
    if poker_processes:
        for p in poker_processes:
            print(f" Proceso encontrado: {p.info['name']}")
    else:
        print(" No se encontró PokerStars ejecutándose")
except:
    print("ℹ  Instala psutil: pip install psutil")

# 4. Verificar captura de pantalla
print("\n Probando captura de pantalla...")
try:
    import mss
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        print(f" Captura exitosa: {screenshot.width}x{screenshot.height}")
except Exception as e:
    print(f" Error captura: {e}")

print("\n" + "=" * 60)
print(" SUGERENCIAS:")
print("1. Abre PokerStars y colócalo en primer plano")
print("2. Asegúrate de tener templates en data/card_templates/pokerstars/")
print("3. Ejecuta: python test_detection.py")
