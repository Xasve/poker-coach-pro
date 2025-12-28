# Script de instalación optimizada para el bot extremo
import subprocess
import sys
import time

def install_optimized():
    \"\"\"Instalar dependencias optimizadas\"\"\"
    
    print(" INSTALANDO DEPENDENCIAS OPTIMIZADAS...")
    print("=" * 50)
    
    # Dependencias esenciales optimizadas
    packages = [
        "opencv-contrib-python==4.8.1.78",  # Versión estable
        "numpy==1.24.3",                    # Versión ligera
        "pyautogui==0.9.54",                # Control de interfaz
        "psutil==5.9.6",                    # Monitoreo de recursos
        "numba==0.58.1"                     # Aceleración JIT
    ]
    
    success_count = 0
    failed_count = 0
    
    for pkg in packages:
        print(f"Instalando {pkg}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"  ✅ {pkg}")
                success_count += 1
            else:
                print(f"  ⚠️  {pkg}: Error")
                failed_count += 1
                
        except subprocess.TimeoutExpired:
            print(f"    {pkg}: Timeout")
            failed_count += 1
        except Exception as e:
            print(f"   {pkg}: {str(e)[:50]}")
            failed_count += 1
    
    print("\n" + "=" * 50)
    print(f" RESUMEN: {success_count} exitosas, {failed_count} fallidas")
    
    if failed_count == 0:
        print(" Instalación completada exitosamente")
    else:
        print("  Algunas instalaciones fallaron")
    
    print("\n Para verificar instalación:")
    print("   python -c \"import cv2, numpy; print(f'OpenCV {cv2.__version__}, NumPy {numpy.__version__}')\"")
    
    return success_count

if __name__ == "__main__":
    install_optimized()
