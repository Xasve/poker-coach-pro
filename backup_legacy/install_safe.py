# install_safe.py - Instalación segura de dependencias
import subprocess
import sys
import os

print("🔧 INSTALACIÓN SEGURA DE DEPENDENCIAS")
print("=" * 60)

def run_command(cmd):
    """Ejecutar comando de forma segura"""
    print(f"\n▶️  Ejecutando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Éxito")
            if result.stdout:
                print(f"   📄 Salida: {result.stdout[:100]}...")
            return True
        else:
            print(f"   ❌ Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ Excepción: {e}")
        return False

def main():
    print("\n1. VERIFICANDO PYTHON...")
    print(f"   Versión: {sys.version}")
    
    print("\n2. ACTUALIZANDO PIP...")
    if not run_command(f'"{sys.executable}" -m pip install --upgrade pip --no-cache-dir'):
        print("⚠️  Usando ensurepip como respaldo...")
        run_command(f'"{sys.executable}" -m ensurepip --upgrade')
    
    print("\n3. INSTALANDO DEPENDENCIAS UNA POR UNA...")
    
    # Instalar en orden específico (más estables primero)
    dependencies = [
        ("setuptools", "setuptools"),
        ("wheel", "wheel"),
        ("numpy", "numpy==1.24.3"),  # Versión específica estable
        ("opencv", "opencv-python==4.8.1.78"),  # Versión específica
        ("mss", "mss==9.0.1"),  # Versión específica
        ("pillow", "pillow==10.1.0"),  # Para procesamiento de imágenes
    ]
    
    for name, package in dependencies:
        print(f"\n📦 Instalando {name}...")
        if not run_command(f'"{sys.executable}" -m pip install {package} --no-cache-dir'):
            print(f"⚠️  Falló {name}, intentando sin versión específica...")
            run_command(f'"{sys.executable}" -m pip install {package.split("==")[0]} --no-cache-dir')
    
    print("\n4. VERIFICANDO INSTALACIONES...")
    
    checks = [
        ("NumPy", "import numpy; print(f'   ✅ NumPy: {numpy.__version__}')"),
        ("OpenCV", "import cv2; print(f'   ✅ OpenCV: {cv2.__version__}')"),
        ("MSS", "import mss; print('   ✅ MSS instalado')"),
        ("Pillow", "from PIL import Image; print('   ✅ Pillow instalado')"),
    ]
    
    for name, code in checks:
        print(f"\n🔍 Verificando {name}...")
        try:
            exec(code)
        except Exception as e:
            print(f"   ❌ {name}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ INSTALACIÓN COMPLETADA")
    print("\n📋 RESUMEN:")
    print("• Dependencias instaladas en orden seguro")
    print("• Versiones específicas para estabilidad")
    print("• Sin cache para evitar corrupción")
    
    print("\n🚀 EJECUTA AHORA:")
    print("   python check_system.py")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()