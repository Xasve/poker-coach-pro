# check_system.py - Diagnóstico rápido del sistema
import sys
import os
import subprocess

print("🔍 DIAGNÓSTICO RÁPIDO DEL SISTEMA")
print("=" * 60)

# 1. Verificar estructura de archivos
print("\n📁 ESTRUCTURA DE ARCHIVOS:")
required_files = [
    ("run_pokerstars_optimized.py", True),
    ("calibrate_detector.py", True),
    ("src/platforms/pokerstars_adapter.py", True),
    ("src/screen_capture/table_detector.py", True),
    ("src/integration/coach_integrator.py", True),
    ("config/settings.json", True),
    ("debug/calibration/", False),  # Directorio, no archivo
]

for file_path, is_file in required_files:
    exists = os.path.exists(file_path)
    if is_file:
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
    else:
        if not exists:
            os.makedirs(file_path, exist_ok=True)
            print(f"📁 Creado: {file_path}/")
        else:
            print(f"✅ {file_path}/")

# 2. Verificar dependencias
print("\n📦 DEPENDENCIAS INSTALADAS:")
dependencies = [
    ("opencv-python", "cv2"),
    ("numpy", "numpy"),
    ("mss", "mss"),
]

for pkg_name, import_name in dependencies:
    try:
        __import__(import_name)
        print(f"✅ {pkg_name}")
    except ImportError:
        print(f"❌ {pkg_name} (FALTANTE)")

# 3. Probar imports básicos
print("\n🔄 PROBANDO IMPORTS CRÍTICOS:")
sys.path.insert(0, 'src')

imports_to_test = [
    ("platforms.pokerstars_adapter", "PokerStarsAdapter"),
    ("screen_capture.table_detector", "TableDetector"),
    ("integration.coach_integrator", "CoachIntegrator"),
]

all_imports_ok = True
for module_path, class_name in imports_to_test:
    try:
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        
        # Probar creación básica
        if class_name == "TableDetector":
            obj = cls()  # Sin argumentos
        elif class_name == "CoachIntegrator":
            obj = cls("pokerstars")
        else:
            obj = cls(stealth_level=1)
            
        print(f"✅ {class_name}")
    except Exception as e:
        print(f"❌ {class_name}: {str(e)[:50]}")
        all_imports_ok = False

# 4. Verificar configuraciones
print("\n⚙️  CONFIGURACIONES:")
configs = ["config/settings.json", "config/strategies.json", "config/platforms.json"]

for config in configs:
    if os.path.exists(config):
        try:
            with open(config, 'r') as f:
                content = f.read()
                if len(content.strip()) > 0:
                    print(f"✅ {config}")
                else:
                    print(f"⚠️  {config} (vacío)")
        except:
            print(f"❌ {config} (error lectura)")
    else:
        print(f"❌ {config} (faltante)")

# Resumen
print("\n" + "=" * 60)
if all_imports_ok:
    print("🎉 ¡SISTEMA LISTO PARA USAR!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Ejecuta: python calibrate_detector.py")
    print("2. Ajusta el detector si es necesario")
    print("3. Ejecuta: python run_pokerstars_optimized.py")
else:
    print("⚠️  HAY PROBLEMAS QUE RESOLVER")
    print("\n🔧 SOLUCIONES:")
    print("1. Instala dependencias faltantes")
    print("2. Verifica que los archivos existan")
    print("3. Revisa errores específicos arriba")

print("\n" + "=" * 60)