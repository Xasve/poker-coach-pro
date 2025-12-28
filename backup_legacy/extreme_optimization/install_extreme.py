# Script de instalación optimizada para el bot extremo
import subprocess
import sys

def install_optimized():
    """Instalar dependencias optimizadas"""
    
    print(" INSTALANDO DEPENDENCIAS OPTIMIZADAS...")
    
    # Dependencias esenciales optimizadas
    packages = [
        "opencv-contrib-python==4.8.1.78",  # Versión estable
        "numpy==1.24.3",                    # Versión ligera
        "pyautogui==0.9.54",                # Control de interfaz
        "psutil==5.9.6",                    # Monitoreo de recursos
        "numba==0.58.1"                     # Aceleración JIT
    ]
    
    for pkg in packages:
        print(f"Instalando {pkg}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"   {pkg}")
        else:
            print(f"    {pkg}: {result.stderr[:100]}")
    
    print("\n✅ Instalación completada")
    print("🚀 Ejecuta: python extreme_poker_bot.py")

if __name__ == "__main__":
    install_optimized()
