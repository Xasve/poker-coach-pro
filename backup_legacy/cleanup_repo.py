# cleanup_repo.py
import os
import shutil
import glob

def cleanup_repository():
    """Limpiar el repositorio de archivos temporales"""
    
    print("🧹 LIMPIANDO REPOSITORIO POKER COACH PRO")
    print("=" * 60)
    
    # Archivos a eliminar (patrones)
    patterns_to_remove = [
        "test_*.py",
        "fix_*.py", 
        "setup_*.py",
        "check_*.py",
        "verify_*.py",
        "temp_*.py",
        "*_temp.py",
        "nuclear_*.py",
        "*.placeholder"
    ]
    
    # Directorios a limpiar (no eliminar)
    dirs_to_clean = ["debug", "logs", "__pycache__"]
    
    # Eliminar archivos por patrón
    files_removed = 0
    for pattern in patterns_to_remove:
        for filepath in glob.glob(pattern):
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(f"🗑️  Eliminado: {filepath}")
                files_removed += 1
    
    # Limpiar directorios
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            # Eliminar contenido pero mantener directorio
            for item in os.listdir(dir_name):
                item_path = os.path.join(dir_name, item)
                try:
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {item_path}: {e}")
            print(f"🧽 Limpiado: {dir_name}/")
    
    # Crear estructura organizada
    print("\n📁 ORGANIZANDO ESTRUCTURA...")
    
    # Crear directorios necesarios
    required_dirs = [
        'tests',
        'docs',
        'data/models',
        'data/card_templates/pokerstars',
        'config'
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Mover archivos de test a carpeta tests
    test_files = []
    for pattern in ["*test*.py", "*Test*.py"]:
        test_files.extend(glob.glob(pattern))
    
    for test_file in test_files:
        if os.path.isfile(test_file) and test_file != "cleanup_repo.py":
            dest = os.path.join("tests", os.path.basename(test_file))
            shutil.move(test_file, dest)
            print(f"📦 Movido a tests/: {test_file}")
    
    # Verificar estructura final
    print("\n📊 ESTRUCTURA FINAL:")
    
    structure = {
        "src/": "Código fuente principal",
        "data/": "Datos y templates",
        "config/": "Configuración",
        "tests/": "Tests unitarios",
        "docs/": "Documentación",
        "logs/": "Archivos de log",
        "debug/": "Depuración",
        "main.py": "Punto de entrada",
        "requirements.txt": "Dependencias",
        "README.md": "Documentación"
    }
    
    for item, description in structure.items():
        if os.path.exists(item.rstrip('/')) or item.endswith('.py'):
            print(f"✅ {item:20} - {description}")
        else:
            print(f"⚠️  {item:20} - {description} (faltante)")
    
    print("\n" + "=" * 60)
    print(f"✅ Limpieza completada: {files_removed} archivos eliminados")
    print("\n💡 Recomendación: Revisar manualmente los archivos restantes")

if __name__ == "__main__":
    cleanup_repository()