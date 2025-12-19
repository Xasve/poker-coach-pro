# clean_project.py - Limpiador del proyecto
import os
import shutil
import glob
from pathlib import Path

print("🧹 LIMPIADOR DEL PROYECTO POKER COACH PRO")
print("=" * 60)

def get_directory_size(path):
    """Calcular tamaño de directorio"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

def clean_project():
    """Limpiar archivos innecesarios"""
    print("\n📊 ANÁLISIS DEL PROYECTO:")
    
    # Estructura actual
    project_size = get_directory_size(".")
    print(f"   Tamaño total del proyecto: {project_size / 1024 / 1024:.2f} MB")
    
    # Archivos a conservar (ESENCIALES)
    essential_files = {
        "src/": "Código fuente",
        "config/": "Configuraciones",
        "data/card_templates/": "Templates de cartas",
        "run_pokerstars_optimized.py": "Script principal",
        "check_system.py": "Verificador",
        "calibrate_detector.py": "Calibrador",
        "calibrate_positions.py": "Calibrador posiciones",
        "requirements.txt": "Dependencias",
        "README.md": "Documentación"
    }
    
    # Directorios a limpiar
    clean_dirs = [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".coverage",
        "htmlcov",
        "*.egg-info",
        "build",
        "dist",
        ".eggs",
        "pip-wheel-metadata"
    ]
    
    # Extensiones de archivos temporales
    temp_extensions = [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.c",
        "*.html",
        "*.css",
        "*.js.map",
        "*.log",
        "*.tmp",
        "*.temp",
        "*.bak",
        "*.backup",
        "*.orig",
        "*.rej",
        "*.swp",
        "*.swo",
        "*.swn",
        "Thumbs.db",
        ".DS_Store"
    ]
    
    print("\n🔍 BUSCANDO ARCHIVOS TEMPORALES...")
    
    total_deleted = 0
    total_freed = 0
    
    # 1. Limpiar directorios de cache
    for cache_dir in clean_dirs:
        for found in glob.glob(f"**/{cache_dir}", recursive=True):
            if os.path.exists(found):
                size = get_directory_size(found)
                try:
                    shutil.rmtree(found)
                    print(f"   🗑️  Eliminado: {found}/ ({size / 1024:.1f} KB)")
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {found}: {e}")
    
    # 2. Limpiar archivos temporales por extensión
    for ext in temp_extensions:
        for found in glob.glob(f"**/{ext}", recursive=True):
            if os.path.exists(found):
                try:
                    size = os.path.getsize(found)
                    os.remove(found)
                    print(f"   🗑️  Eliminado: {found} ({size / 1024:.1f} KB)")
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {found}: {e}")
    
    # 3. Limpiar debug/ (conservar algunos archivos importantes)
    debug_dir = "debug"
    if os.path.exists(debug_dir):
        print(f"\n🔧 LIMPIANDO DIRECTORIO {debug_dir}/")
        
        # Conservar estos subdirectorios
        keep_subdirs = ["calibration", "captures"]
        
        for item in os.listdir(debug_dir):
            item_path = os.path.join(debug_dir, item)
            
            if os.path.isdir(item_path):
                if item not in keep_subdirs:
                    try:
                        size = get_directory_size(item_path)
                        shutil.rmtree(item_path)
                        print(f"   🗑️  Eliminado: {item_path}/ ({size / 1024:.1f} KB)")
                        total_deleted += 1
                        total_freed += size
                    except Exception as e:
                        print(f"   ⚠️  No se pudo eliminar {item_path}: {e}")
            else:
                # Eliminar archivos viejos en debug/
                try:
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                    print(f"   🗑️  Eliminado: {item_path} ({size / 1024:.1f} KB)")
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {item_path}: {e}")
    
    # 4. Limpiar logs/ (conservar últimos 5 archivos por sesión)
    logs_dir = "logs"
    if os.path.exists(logs_dir):
        print(f"\n📝 LIMPIANDO DIRECTORIO {logs_dir}/")
        
        # Por cada subdirectorio en logs/
        for subdir in os.listdir(logs_dir):
            subdir_path = os.path.join(logs_dir, subdir)
            
            if os.path.isdir(subdir_path):
                # Obtener todos los archivos ordenados por fecha
                files = []
                for f in os.listdir(subdir_path):
                    f_path = os.path.join(subdir_path, f)
                    if os.path.isfile(f_path):
                        files.append((f_path, os.path.getmtime(f_path)))
                
                # Ordenar por fecha (más antiguos primero)
                files.sort(key=lambda x: x[1])
                
                # Conservar solo los 5 más recientes
                if len(files) > 5:
                    for i in range(len(files) - 5):
                        f_path, mtime = files[i]
                        try:
                            size = os.path.getsize(f_path)
                            os.remove(f_path)
                            print(f"   🗑️  Eliminado (viejo): {f_path} ({size / 1024:.1f} KB)")
                            total_deleted += 1
                            total_freed += size
                        except Exception as e:
                            print(f"   ⚠️  No se pudo eliminar {f_path}: {e}")
    
    # 5. Limpiar hand_history/ (conservar últimos 10 archivos)
    hand_history_dir = "hand_history"
    if os.path.exists(hand_history_dir):
        print(f"\n🃏 LIMPIANDO DIRECTORIO {hand_history_dir}/")
        
        files = []
        for f in os.listdir(hand_history_dir):
            f_path = os.path.join(hand_history_dir, f)
            if os.path.isfile(f_path):
                files.append((f_path, os.path.getmtime(f_path)))
        
        files.sort(key=lambda x: x[1])
        
        if len(files) > 10:
            for i in range(len(files) - 10):
                f_path, mtime = files[i]
                try:
                    size = os.path.getsize(f_path)
                    os.remove(f_path)
                    print(f"   🗑️  Eliminado (historial viejo): {f_path} ({size / 1024:.1f} KB)")
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {f_path}: {e}")
    
    # 6. Archivos de test temporales
    test_files_to_clean = [
        "quick_test.py",
        "quick_test_fixed.py",
        "test_*.py",
        "*_test.py",
        "*_backup.py",
        "*_old.py",
        "temp_*.py",
        "debug_*.py"
    ]
    
    for pattern in test_files_to_clean:
        for found in glob.glob(pattern):
            if os.path.exists(found) and found not in ["test_coach_fixed.py", "check_system.py"]:
                try:
                    size = os.path.getsize(found)
                    os.remove(found)
                    print(f"   🗑️  Eliminado (archivo test): {found} ({size / 1024:.1f} KB)")
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {found}: {e}")
    
    # 7. Vaciar papelera de Python
    print("\n🗑️  VACIANDO PAPELERA DE PYTHON...")
    
    # Archivos específicos de Python a limpiar
    python_trash = [
        "*.log",           # Log files
        "*.pid",           # Process IDs
        "*.lock",          # Lock files
        "coverage.xml",    # Coverage reports
        ".coverage",       # Coverage data
        "nosetests.xml",   # Test reports
        "htmlcov/",        # HTML coverage
        ".tox/",           # Tox environments
        ".venv/",          # Entornos virtuales (excepto el actual)
        "venv*/",          # Otros venv
        "env*/",           # Otros env
        ".env",            # Environment files
        ".env.*"           # Environment files
    ]
    
    for pattern in python_trash:
        for found in glob.glob(f"**/{pattern}", recursive=True):
            # No eliminar el venv actual
            if "venv" in found and os.path.exists("venv") and found.startswith("venv"):
                continue
                
            if os.path.exists(found):
                try:
                    if os.path.isdir(found):
                        size = get_directory_size(found)
                        shutil.rmtree(found)
                        print(f"   🗑️  Eliminado (Python): {found}/ ({size / 1024:.1f} KB)")
                    else:
                        size = os.path.getsize(found)
                        os.remove(found)
                        print(f"   🗑️  Eliminado (Python): {found} ({size / 1024:.1f} KB)")
                    
                    total_deleted += 1
                    total_freed += size
                except Exception as e:
                    print(f"   ⚠️  No se pudo eliminar {found}: {e}")
    
    # 8. Verificar estructura final
    print("\n📁 ESTRUCTURA FINAL DEL PROYECTO:")
    
    essential_structure = {
        "src/": "✓ Código fuente",
        "src/platforms/": "✓ Adaptadores de casino",
        "src/screen_capture/": "✓ Sistema de captura",
        "src/integration/": "✓ Coach GTO",
        "src/core/": "✓ Motor principal",
        "config/": "✓ Configuraciones",
        "data/": "✓ Datos y templates",
        "debug/": "✓ Debug (limitado)",
        "logs/": "✓ Logs (limitado)",
        "hand_history/": "✓ Historial (limitado)"
    }
    
    for path, description in essential_structure.items():
        if os.path.exists(path.rstrip('/')):
            if os.path.isdir(path.rstrip('/')):
                size = get_directory_size(path.rstrip('/')) / 1024
                print(f"   {description}: {size:.1f} KB")
            else:
                size = os.path.getsize(path) / 1024
                print(f"   {description}: {size:.1f} KB")
        else:
            print(f"   {description}: ❌ FALTANTE")
    
    # Resumen final
    new_size = get_directory_size(".")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA LIMPIEZA:")
    print(f"   Archivos eliminados: {total_deleted}")
    print(f"   Espacio liberado: {total_freed / 1024 / 1024:.2f} MB")
    print(f"   Tamaño anterior: {project_size / 1024 / 1024:.2f} MB")
    print(f"   Tamaño actual: {new_size / 1024 / 1024:.2f} MB")
    print(f"   Reducción: {(project_size - new_size) / 1024 / 1024:.2f} MB ({(1 - new_size/project_size)*100:.1f}%)")
    
    print("\n✅ PROYECTO LIMPIADO EXITOSAMENTE")
    print("=" * 60)

def create_clean_structure():
    """Crear estructura limpia si no existe"""
    print("\n🏗️  CREANDO ESTRUCTURA LIMPIA...")
    
    directories = [
        "src/platforms",
        "src/screen_capture",
        "src/integration",
        "src/core",
        "src/utils",
        "config",
        "data/card_templates/pokerstars",
        "data/card_templates/ggpoker",
        "debug/calibration",
        "debug/captures",
        "logs/sessions",
        "hand_history"
    ]
    
    created = 0
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"   📁 Creado: {directory}/")
            created += 1
    
    if created > 0:
        print(f"\n   ✅ {created} directorios creados")
    
    # Crear archivos esenciales si no existen
    essential_files = {
        "config/settings.json": '''{
    "stealth_level": 1,
    "capture_delay": 0.5,
    "overlay_opacity": 0.8,
    "confidence_threshold": 0.7,
    "min_table_detections": 3
}''',
        "config/strategies.json": '''{
    "default_strategy": "gto_basic",
    "aggression_factor": 0.7,
    "risk_tolerance": 0.5,
    "bluff_frequency": 0.25
}''',
        "README.md": '''# Poker Coach Pro
Sistema de análisis GTO para poker en tiempo real

## Instalación
```bash
pip install -r requirements.txt