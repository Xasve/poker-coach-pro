# verify_installations.py

import sys
import subprocess

def check_package(package_name, import_name=None):
    """Verificar si un paquete está instalado correctamente"""
    if import_name is None:
        import_name = package_name
    
    try:
        exec(f"import {import_name}")
        version = eval(f"{import_name}.__version__")
        return True, version
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 VERIFICANDO INSTALACIONES")
    print("=" * 50)
    
    packages = [
        ("numpy", "numpy"),
        ("opencv-python", "cv2"),
        ("PIL", "PIL.Image"),  # Para pillow
        ("mss", "mss"),
        ("pytesseract", "pytesseract"),
    ]
    
    all_ok = True
    
    for pip_name, import_name in packages:
        success, info = check_package(pip_name, import_name)
        if success:
            print(f"✅ {pip_name}: versión {info}")
        else:
            print(f"❌ {pip_name}: ERROR - {info}")
            all_ok = False
    
    print("=" * 50)
    
    # Verificar Python version
    print(f"🐍 Python: {sys.version}")
    
    if all_ok:
        print("🎉 ¡Todas las instalaciones son correctas!")
    else:
        print("⚠️  Hay problemas con algunas instalaciones")
    
    return all_ok

if __name__ == "__main__":
    main()