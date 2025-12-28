#!/usr/bin/env python3
"""
Limpia requirements.txt y analiza imports reales del proyecto.
"""

import re
from pathlib import Path

# 1. LIMPIAR requirements.txt
print("🧹 Limpiando requirements.txt...")
req_file = Path("requirements.txt")
clean_lines = []

if req_file.exists():
    with open(req_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig maneja BOM
        for line in f:
            line = line.strip()
            # Eliminar líneas vacías, comentarios y caracteres raros
            if line and not line.startswith('#') and not line.startswith('ï»¿'):
                # Obtener solo el nombre del paquete (sin versiones)
                pkg_name = re.split(r'[<>=!\[\]]', line)[0].strip()
                if pkg_name:
                    clean_lines.append(pkg_name)

# Paquetes base ESSENCIALES para tu proyecto (basado en lo que mencionaste)
ESSENTIAL_PACKAGES = [
    'opencv-python',    # Procesamiento de imágenes
    'pytesseract',      # OCR para texto en cartas
    'pillow',           # Manipulación de imágenes
    'numpy',            # Cálculos numéricos
    'pyautogui',        # Captura de pantalla
    'mss',              # Captura de pantalla más rápida
    'colorama',         # Colores en consola
    'pyyaml',           # Configuraciones YAML
]

# Combinar paquetes limpiados con esenciales
all_packages = sorted(set(clean_lines + ESSENTIAL_PACKAGES))

# Escribir nuevo requirements.txt
with open(req_file, 'w', encoding='utf-8') as f:
    f.write("# Dependencias Poker Coach Pro\n")
    f.write("# ============================\n\n")
    for pkg in all_packages:
        f.write(f"{pkg}\n")

print(f"✅ requirements.txt limpiado. {len(all_packages)} paquetes:")
for pkg in all_packages:
    print(f"   • {pkg}")

# 2. ANALIZAR IMPORTS DE TU CÓDIGO REAL
print("\n🔍 Analizando imports en src/ y config/...")

# Lista de módulos estándar de Python (no necesitan pip)
STD_MODULES = {
    'os', 'sys', 'json', 'time', 're', 'datetime', 'math', 'random',
    'collections', 'pathlib', 'logging', 'typing', 'itertools', 'functools',
    'hashlib', 'statistics', 'csv', 'string', 'decimal', 'fractions',
    'ast', 'inspect', 'textwrap', 'enum', 'argparse'
}

found_imports = set()

# Buscar en src/, config/, y archivos .py en raíz
search_paths = ['src', 'config'] + [f for f in Path('.').iterdir() if f.suffix == '.py']

for path in search_paths:
    if Path(path).exists():
        for py_file in Path(path).rglob('*.py'):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                # Buscar imports simples (no perfecto pero funciona)
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('import ') or line.startswith('from '):
                        # Extraer nombre del módulo
                        if 'import' in line:
                            parts = line.split()
                            for part in parts[1:]:
                                module = part.split('.')[0].strip(',')
                                if module and not module.startswith('#'):
                                    found_imports.add(module)
            except:
                continue

# Filtrar módulos estándar
external_imports = sorted([imp for imp in found_imports if imp not in STD_MODULES])

print(f"\n📦 Imports externos encontrados: {len(external_imports)}")
if external_imports:
    for imp in external_imports[:20]:  # Mostrar primeros 20
        print(f"   • {imp}")
    if len(external_imports) > 20:
        print(f"   ... y {len(external_imports) - 20} más")

# 3. VERIFICAR QUE TENEMOS LOS PAQUETES NECESARIOS
missing = [imp for imp in external_imports if imp not in all_packages]
if missing:
    print(f"\n⚠️  Paquetes faltantes en requirements.txt:")
    for pkg in missing[:10]:
        print(f"   • {pkg}")
    print("\n   Añadiendo automáticamente...")
    all_packages.extend(missing)
    all_packages = sorted(set(all_packages))

# Actualizar requirements.txt final
with open(req_file, 'w', encoding='utf-8') as f:
    f.write("# Dependencias Poker Coach Pro\n")
    f.write("# ============================\n\n")
    for pkg in all_packages:
        f.write(f"{pkg}\n")

print(f"\n✅ requirements.txt finalizado con {len(all_packages)} paquetes.")
print(f"\n📋 Contenido final:")
print("-" * 40)
print(req_file.read_text())
print("-" * 40)

print("\n🎯 Siguiente paso: Ejecutar 'pip install -r requirements.txt'")