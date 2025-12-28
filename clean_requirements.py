#!/usr/bin/env python3
"""
LIMPIEZA COMPLETA de requirements.txt
Ejecutar: python clean_requirements.py
"""

import os
from pathlib import Path

print("🧹 LIMPIANDO requirements.txt CORROMPIDO...")

# 1. VERIFICAR Y BACKUP DEL ARCHIVO ACTUAL
req_file = Path("requirements.txt")
backup_file = Path("requirements_BACKUP.txt")

if req_file.exists():
    # Hacer backup primero
    try:
        with open(req_file, 'rb') as f:
            raw_content = f.read()
        backup_file.write_bytes(raw_content)
        print(f"✅ Backup creado: {backup_file}")
        
        # Mostrar contenido RAW (para diagnóstico)
        print(f"\n📄 Contenido RAW (primeros 500 bytes):")
        print("-" * 50)
        print(raw_content[:500])
        print("-" * 50)
        
        # Intentar decodificar con diferentes codificaciones
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii', 'utf-8-sig']
        decoded_content = None
        
        for enc in encodings:
            try:
                decoded_content = raw_content.decode(enc)
                print(f"✅ Decodificado con {enc}")
                break
            except UnicodeDecodeError:
                continue
        
        if decoded_content:
            # Filtrar solo líneas válidas
            valid_lines = []
            for line in decoded_content.split('\n'):
                line = line.strip()
                # Eliminar caracteres no ASCII y líneas corruptas
                if line and not line.startswith('#') and not any(c in line for c in ['ï»¿', '¬°', '¬']):
                    # Mantener solo caracteres válidos para nombres de paquetes
                    clean_line = ''.join(c for c in line if c.isprintable() and ord(c) < 128)
                    if clean_line and not clean_line.startswith('ÿ'):
                        valid_lines.append(clean_line)
            
            print(f"\n📋 Líneas válidas encontradas: {len(valid_lines)}")
            for line in valid_lines[:10]:
                print(f"  • {line}")
            if len(valid_lines) > 10:
                print(f"  ... y {len(valid_lines) - 10} más")
        else:
            print("❌ No se pudo decodificar el archivo")
            valid_lines = []
            
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        valid_lines = []
else:
    print("ℹ️  requirements.txt no existe")
    valid_lines = []

# 2. CREAR NUEVO requirements.txt CON PAQUETES ESENCIALES
print("\n📦 CREANDO NUEVO requirements.txt CON PAQUETES ESENCIALES...")

# Paquetes BASE para tu proyecto de Poker
ESSENTIAL_PACKAGES = [
    # Procesamiento de imágenes y captura
    'opencv-python>=4.8.0',
    'pillow>=10.0.0',
    'numpy>=1.24.0',
    'mss>=9.0.1',
    'pyautogui>=0.9.54',
    
    # OCR y reconocimiento
    'pytesseract>=0.3.10',
    
    # Interfaz y utilidades
    'colorama>=0.4.6',
    'pyyaml>=6.0',
    'tqdm>=4.66.0',
    
    # Análisis de datos (para lógica GTO)
    'pandas>=2.0.0',
    
    # Machine learning (potencialmente para mejorar decisiones)
    'scikit-learn>=1.3.0',
    
    # Visualización (opcional, para debugging)
    'matplotlib>=3.7.0',
]

# Combinar con paquetes válidos encontrados
all_packages = list(set(ESSENTIAL_PACKAGES + valid_lines))
all_packages.sort()

# Escribir nuevo archivo
with open(req_file, 'w', encoding='utf-8') as f:
    f.write("# DEPENDENCIAS POKER COACH PRO\n")
    f.write("# ============================\n")
    f.write("# Archivo regenerado automáticamente - " + 
            "NO EDITAR MANUALMENTE A MENOS QUE SEAS EXPERTO\n\n")
    
    f.write("# PROCESAMIENTO DE IMAGEN Y CAPTURA\n")
    for pkg in ['opencv-python', 'pillow', 'numpy', 'mss', 'pyautogui']:
        for package in all_packages:
            if package.startswith(pkg):
                f.write(f"{package}\n")
    
    f.write("\n# OCR Y RECONOCIMIENTO\n")
    for pkg in ['pytesseract']:
        for package in all_packages:
            if package.startswith(pkg):
                f.write(f"{package}\n")
    
    f.write("\n# UTILIDADES Y FRAMEWORKS\n")
    utility_pkgs = ['colorama', 'pyyaml', 'tqdm', 'pandas', 'scikit-learn', 'matplotlib']
    for pkg in utility_pkgs:
        for package in all_packages:
            if package.startswith(pkg):
                f.write(f"{package}\n")
    
    # Agregar cualquier paquete que no esté en las categorías anteriores
    other_packages = [p for p in all_packages if not any(p.startswith(cat) for cat in 
                     ['opencv', 'pillow', 'numpy', 'mss', 'pyautogui', 'pytesseract'] + utility_pkgs)]
    
    if other_packages:
        f.write("\n# OTRAS DEPENDENCIAS\n")
        for package in other_packages:
            f.write(f"{package}\n")

print(f"\n✅ NUEVO requirements.txt CREADO con {len(all_packages)} paquetes")
print("\n📋 CONTENIDO FINAL:")
print("=" * 60)
print(req_file.read_text(encoding='utf-8'))
print("=" * 60)

print("\n🎯 SIGUIENTE PASO: Ejecutar 'pip install -r requirements.txt'")
print("   o usar el script setup_fixed.ps1 que crearemos a continuación.")