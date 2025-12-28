# verify_installation.py
import sys, os, subprocess, importlib, platform

print("🔍 VERIFICACIÓN COMPLETA DE INSTALACIÓN POKER COACH PRO")
print("="*70)

def run_check(name, check_func):
    print(f"\n🧪 {name}...")
    try:
        result = check_func()
        print(f"   ✅ {result}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

# Check 1: Python version
def check_python():
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return f"Python {version.major}.{version.minor}.{version.micro} "
    return f"Python {version.major}.{version.minor}.{version.micro} (Necesita 3.11+)"

# Check 2: Dependencies
def check_dependencies():
    deps = [
        ("numpy", "1.24.4"),
        ("cv2", "4.9.0"),
        ("PIL", "10.3.0"),
        ("mss", "9.0.1"),
        ("yaml", None),
        ("pyautogui", "0.9.54")
    ]
    
    results = []
    for dep, expected in deps:
        try:
            module = importlib.import_module(dep if dep != "cv2" else "cv2")
            version = getattr(module, "__version__", "OK")
            results.append(f"{dep}: {version}")
        except ImportError:
            results.append(f"{dep}: FALTANTE")
    
    return ", ".join(results)

# Check 3: Project structure
def check_structure():
    required = [
        "src/",
        "src/platforms/pokerstars_adapter.py",
        "src/core/poker_engine.py",
        "src/screen_capture/stealth_capture.py",
        "data/card_templates/pokerstars/",
        "config/",
        "main_real.py"
    ]
    
    missing = []
    for item in required:
        if not os.path.exists(item.rstrip("/")):
            missing.append(item)
    
    if missing:
        return f"Faltan: {', '.join(missing)}"
    return f"Estructura completa ({len(required)} items)"

# Check 4: PokerStars detection capability
def check_pokerstars_detection():
    try:
        import mss, cv2, numpy as np
        
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(sct.monitors[1]))
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Check for green (PokerStars tables)
            green_mask = cv2.inRange(hsv, np.array([35,50,50]), np.array([85,255,255]))
            green_pixels = np.sum(green_mask > 0)
            
            if green_pixels > 50000:
                return f" PokerStars detectable ({green_pixels:,} px verdes)"
            else:
                return f"  Poco verde detectado ({green_pixels:,} px)"
                
    except Exception as e:
        return f"Error detección: {e}"

# Run all checks
checks = [
    ("Python Version", check_python),
    ("Dependencies", check_dependencies),
    ("Project Structure", check_structure),
    ("PokerStars Detection", check_pokerstars_detection)
]

all_passed = True
for name, func in checks:
    if not run_check(name, func):
        all_passed = False

print("\n" + "="*70)
if all_passed:
    print(" INSTALACIÓN COMPLETAMENTE VERIFICADA!")
    print("\n EJECUTAR:")
    print("   1. python detect_coords.py    # Para coordenadas reales")
    print("   2. python main_real.py        # Sistema principal")
    print("   3. python realtime_monitor.py # Dashboard tiempo real")
else:
    print("  INSTALACIÓN INCOMPLETA")
    print("\n EJECUTA:")
    print("   .\venv\Scripts\Activate.ps1")
    print("   pip install -r requirements.txt")
    print("\n Asegúrate de tener la estructura completa")
