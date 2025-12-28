#!/usr/bin/env python3
"""
Analizador de dependencias para Poker Coach Pro.
Ejecutar: python analyze_deps.py
"""

import ast
import os
from pathlib import Path

# Mapeo de imports comunes a nombres de pip
COMMON_IMPORTS = {
    'cv2': 'opencv-python',
    'PIL': 'Pillow',
    'numpy': 'numpy',
    'pytesseract': 'pytesseract',
    'pyautogui': 'pyautogui',
    'mss': 'mss',
    'pynput': 'pynput',
    'requests': 'requests',
    'json': None,  # Built-in
    'os': None,
    'sys': None,
    'time': None,
    'logging': None,
    'pathlib': None,
    'collections': None,
    'math': None,
    're': None,
    'datetime': None,
    'random': None,
}

def extract_imports(filepath):
    """Extrae todos los imports de un archivo Python."""
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"  ⚠️  Error analizando {filepath}: {e}")
    return imports

def scan_project_for_imports(root_path):
    """Escanea todos los archivos .py en busca de imports."""
    all_imports = set()
    py_files = []
    
    for ext in ['*.py', '*.pyw']:
        py_files.extend(Path(root_path).rglob(ext))
    
    print(f"🔍 Analizando {len(py_files)} archivos Python...")
    
    for py_file in py_files:
        # Saltar archivos en backup_legacy y entornos virtuales
        if 'backup_legacy' in str(py_file) or 'venv' in str(py_file):
            continue
            
        file_imports = extract_imports(py_file)
        if file_imports:
            all_imports.update(file_imports)
            print(f"  📄 {py_file.relative_to(root_path)} -> {', '.join(sorted(file_imports))}")
    
    return sorted(all_imports)

def map_to_pip_packages(imports):
    """Mapea nombres de import a paquetes pip."""
    packages = set()
    unknown_imports = set()
    
    for imp in imports:
        if imp in COMMON_IMPORTS:
            pip_name = COMMON_IMPORTS[imp]
            if pip_name:
                packages.add(pip_name)
        else:
            # Si no está en el mapeo común, lo añadimos como posible paquete
            unknown_imports.add(imp)
    
    return sorted(packages), sorted(unknown_imports)

def main():
    print("=" * 60)
    print("ANALIZADOR DE DEPENDENCIAS - POKER COACH PRO")
    print("=" * 60)
    
    project_root = Path(".").resolve()
    
    # 1. Escanear imports
    found_imports = scan_project_for_imports(project_root)
    
    if not found_imports:
        print("❌ No se encontraron imports en los archivos Python.")
        return
    
    print(f"\n📦 Imports encontrados: {', '.join(found_imports)}")
    
    # 2. Mapear a paquetes pip
    packages, unknown = map_to_pip_packages(found_imports)
    
    print(f"\n✅ Paquetes pip identificados:")
    for pkg in packages:
        print(f"   • {pkg}")
    
    if unknown:
        print(f"\n❓ Imports no identificados (revisar manualmente):")
        for imp in unknown:
            print(f"   • {imp}")
        print("\n   ℹ️  Algunos pueden ser módulos personalizados o built-in.")
    
    # 3. Generar requirements.txt
    requirements_path = project_root / "requirements.txt"
    
    # Leer requirements existente si hay
    existing_packages = set()
    if requirements_path.exists():
        with open(requirements_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    pkg_name = line.split('==')[0].split('>=')[0].split('[')[0]
                    existing_packages.add(pkg_name)
    
    # Combinar paquetes identificados y existentes
    all_packages = sorted(set(packages) | existing_packages)
    
    if all_packages:
        with open(requirements_path, 'w') as f:
            f.write("# Dependencias principales de Poker Coach Pro\n")
            f.write("# Generado automáticamente por analyze_deps.py\n\n")
            for pkg in all_packages:
                f.write(f"{pkg}\n")
        
        print(f"\n💾 requirements.txt actualizado en: {requirements_path}")
        print(f"   Total de paquetes: {len(all_packages)}")
        
        # Mostrar contenido
        print("\n📄 Contenido de requirements.txt:")
        print("-" * 40)
        with open(requirements_path, 'r') as f:
            print(f.read())
        print("-" * 40)
    else:
        print("\n⚠️  No se pudieron identificar paquetes pip.")
    
    # 4. Recomendaciones
    print("\n" + "=" * 60)
    print("RECOMENDACIONES PARA LA FASE 2:")
    print("=" * 60)
    print("1. ✅ Ejecuta este comando para instalar dependencias:")
    print("   pip install -r requirements.txt")
    print("\n2. 🔍 Revisa los 'imports no identificados' arriba.")
    print("   Si son módulos tuyos (ej: 'card_utils'), ignóralos.")
    print("   Si son paquetes externos, añádelos manualmente a requirements.txt")
    print("\n3. 🚀 Continúa con la Fase 2: Reestructuración del código.")
    print("=" * 60)

if __name__ == "__main__":
    main()