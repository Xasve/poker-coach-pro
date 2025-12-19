# analyze_structure.py
import os
import json
from pathlib import Path

def analyze_repository():
    """Analizar la estructura del repositorio"""
    print("🔍 ANALIZANDO ESTRUCTURA DEL REPOSITORIO")
    print("=" * 60)
    
    repo_path = Path.cwd()
    
    # Contar archivos por tipo
    file_types = {}
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Ignorar venv y otros directorios
        if 'venv' in root or '__pycache__' in root:
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1]
            file_types[ext] = file_types.get(ext, 0) + 1
            
            filepath = os.path.join(root, file)
            total_size += os.path.getsize(filepath)
            total_files += 1
    
    print(f"📁 Directorio actual: {repo_path}")
    print(f"📊 Total archivos: {total_files}")
    print(f"💾 Tamaño total: {total_size / 1024 / 1024:.2f} MB")
    print("\n📈 Tipos de archivos:")
    for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
        if ext:  # Ignorar archivos sin extensión
            print(f"   {ext}: {count}")
    
    # Verificar estructura clave
    print("\n🔑 VERIFICANDO ESTRUCTURA CLAVE:")
    required_dirs = [
        ("src/", True),
        ("data/card_templates/", True),
        ("config/", True),
        ("logs/", False),
        ("debug/", False)
    ]
    
    for dir_path, required in required_dirs:
        exists = os.path.exists(dir_path)
        status = "✅" if exists else ("⚠️ " if not required else "❌")
        print(f"   {status} {dir_path}")
    
    # Buscar archivos principales
    print("\n📄 ARCHIVOS PRINCIPALES:")
    main_files = [
        "main.py",
        "detect_coords.py", 
        "capture_templates.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in main_files:
        exists = os.path.exists(file)
        print(f"   {'✅' if exists else '❌'} {file}")
    
    return repo_path

if __name__ == "__main__":
    analyze_repository()