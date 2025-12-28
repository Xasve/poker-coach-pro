# fix_imports.py - Reparador de importaciones
import sys
import subprocess
import os

def check_and_fix():
    """Verificar y reparar importaciones"""
    print("🔧 REPARADOR DE IMPORTACIONES")
    print("=" * 50)
    
    problems = []
    
    # Verificar numpy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        problems.append(("numpy", "1.24.4"))
    
    # Verificar OpenCV
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        problems.append(("opencv-python", "4.9.0.80"))
    
    # Verificar PIL
    try:
        from PIL import Image
        import PIL
        print(f"✅ Pillow {PIL.__version__}")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        problems.append(("pillow", "10.3.0"))
    
    # Reparar problemas
    if problems:
        print(f"\n🔧 Reparando {len(problems)} problemas...")
        
        for package, version in problems:
            print(f"   📦 Instalando {package}=={version}...")
            
            # Desinstalar primero si existe
            subprocess.run([sys.executable, "-m", "pip", "uninstall", package, "-y"], 
                         capture_output=True)
            
            # Instalar versión específica
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", f"{package}=={version}", "--no-cache-dir"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"   ✅ {package} instalado")
            else:
                print(f"   ❌ Error instalando {package}: {result.stderr[:100]}")
        
        print("\n🔄 Verificando nuevamente...")
        check_and_fix()
    else:
        print("\n🎉 Todas las importaciones funcionan correctamente")
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python color_optimizer.py")
        print("   python poker_coach_pro.py")

if __name__ == "__main__":
    check_and_fix()
