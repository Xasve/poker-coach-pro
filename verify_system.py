# VERIFICADOR RÁPIDO DEL SISTEMA
import sys
import os

def check_system():
    """Verificar que todo el sistema está correcto"""
    
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("="*60)
    
    checks = [
        ("Python versión", lambda: f"{sys.version.split()[0]}"),
        ("Directorio actual", lambda: os.getcwd()),
        ("Scripts disponibles", lambda: ", ".join([f for f in os.listdir() if f.endswith(('.py', '.bat', '.ps1'))][:5]))
    ]
    
    for name, check_func in checks:
        try:
            result = check_func()
            print(f" {name}: {result}")
        except Exception as e:
            print(f" {name}: Error - {e}")
    
    # Verificar dependencias
    print("\n DEPENDENCIAS:")
    dependencies = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("pyautogui", "PyAutoGUI"),
        ("scipy", "SciPy")
    ]
    
    missing = []
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"    {name}: Instalado")
        except ImportError:
            print(f"    {name}: FALTANTE")
            missing.append(name)
    
    # Verificar archivos del sistema
    print("\n ARCHIVOS DEL SISTEMA:")
    required_files = [
        "professional_system/professional_poker_system.py",
        "professional_system/integrate_professional.py",
        "extreme_optimization/extreme_bot_simple.py",
        "quick_start.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"    {file}")
        else:
            print(f"     {file}: No encontrado")
    
    # Recomendaciones
    print("\n RECOMENDACIONES:")
    if missing:
        print(f"   1. Instalar dependencias faltantes: {', '.join(missing)}")
        print("      Ejecuta: python -m pip install " + " ".join(m.lower().replace(" ", "") for m in missing))
    
    if not os.path.exists("professional_system"):
        print("   2. El sistema profesional no está instalado")
        print("      Ejecuta: .\\QUICK_START_PRO.bat")
    
    print("\n COMANDOS DISPONIBLES:")
    print("    .\\QUICK_START_PRO.bat     - Inicio completo")
    print("    python INSTALLER_FIXED.py  - Instalar/reparar")
    print("    python quick_start.py      - Sistema original")
    
    return len(missing) == 0

def quick_fix():
    """Reparación rápida de problemas comunes"""
    
    print("\n REPARACIÓN RÁPIDA")
    print("="*60)
    
    # Verificar OpenCV (el problema más común)
    try:
        import cv2
        print(" OpenCV ya está instalado")
    except ImportError:
        print("  Instalando OpenCV...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "opencv-contrib-python", "--quiet"])
        print(" OpenCV instalado")
    
    # Verificar archivos BAT
    bat_files = ["QUICK_START_PRO.bat", "PROFESSIONAL_BOT_FIXED.bat"]
    for bat_file in bat_files:
        if not os.path.exists(bat_file):
            print(f"  {bat_file} no encontrado")
            # Podríamos crearlo aquí si quisiéramos
    
    print("\n Reparación completada")
    print(" Ahora ejecuta: .\\QUICK_START_PRO.bat")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        quick_fix()
    else:
        check_system()
        print("\n Para reparación automática: python verify_system.py fix")

