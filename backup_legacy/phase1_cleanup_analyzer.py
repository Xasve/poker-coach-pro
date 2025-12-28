#!/usr/bin/env python3
"""
PHASE 1 - Analizador y Limpiador de Proyecto Poker Coach Pro
Ejecutar: python phase1_cleanup_analyzer.py
"""

import os
import hashlib
import shutil
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN - EDITA ESTAS RUTAS SI ES NECESARIO
# ============================================================================
PROJECT_ROOT = Path(".").resolve()
BACKUP_DIR = PROJECT_ROOT / "backup_legacy"
EXCLUDE_DIRS = {".git", ".idea", "__pycache__", "venv", "venv311", "backup_legacy"}
EXCLUDE_EXTENSIONS = {".pyc", ".log", ".tmp", ".bak"}
MIN_SIMILARITY_PERCENT = 85  # Porcentaje para considerar archivos "duplicados"

# Lista de patrones de archivos que DEBEMOS PRESERVAR (núcleo funcional)
CORE_PATTERNS = [
    "requirements.txt",
    "README.md",
    "LICENSE",
    "src/",           # Cualquier cosa dentro de src/
    "data/",          # Cualquier cosa dentro de data/ (plantillas, config)
    "config/",        # Configuraciones
    "docs/",          # Documentación
]

# ============================================================================
# FUNCIONES DE ANÁLISIS
# ============================================================================
def get_file_hash(filepath):
    """Calcula hash MD5 de un archivo (para duplicados exactos)."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"  [ERROR] No se pudo leer {filepath}: {e}")
        return None

def get_simple_content_signature(filepath):
    """Obtiene una firma simple basada en primeras líneas para similitud."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [line.strip() for line in f.readlines()[:50] if line.strip()]
        return ' '.join(lines[:10])  # Primera parte no vacía
    except:
        return ""

def find_duplicate_files_by_hash(directory):
    """Encuentra archivos duplicados exactos (mismo hash MD5)."""
    hashes = {}
    duplicates = []
    
    for root, _, files in os.walk(directory):
        root_path = Path(root)
        if any(excl in str(root_path) for excl in EXCLUDE_DIRS):
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
                continue
                
            filepath = root_path / file
            file_hash = get_file_hash(filepath)
            if file_hash:
                if file_hash in hashes:
                    duplicates.append((str(filepath), hashes[file_hash]))
                else:
                    hashes[file_hash] = str(filepath)
    
    return duplicates

def find_similar_files_by_name(directory):
    """Encuentra archivos con nombres muy similares (probables versiones)."""
    all_files = []
    for root, _, files in os.walk(directory):
        root_path = Path(root)
        if any(excl in str(root_path) for excl in EXCLUDE_DIRS):
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
                continue
            all_files.append((root_path / file).relative_to(directory))
    
    similar_groups = {}
    for file_path in all_files:
        name_lower = file_path.name.lower()
        base_match = False
        for existing in similar_groups:
            if existing in name_lower or name_lower in existing:
                similar_groups.setdefault(existing, []).append(str(file_path))
                base_match = True
                break
        if not base_match:
            similar_groups[name_lower] = [str(file_path)]
    
    # Filtrar grupos con más de 1 archivo
    return {k: v for k, v in similar_groups.items() if len(v) > 1}

def should_preserve(filepath, core_patterns):
    """Determina si un archivo debe preservarse según patrones de núcleo."""
    file_str = str(filepath)
    for pattern in core_patterns:
        if pattern.endswith('/'):
            if pattern in file_str + '/':
                return True
        elif filepath.name == pattern or file_str.endswith(pattern):
            return True
    return False

def create_backup_and_remove(files_to_backup, backup_dir):
    """Mueve archivos identificados a backup y los elimina de su ubicación original."""
    backup_dir.mkdir(exist_ok=True, parents=True)
    actions = []
    
    for original in files_to_backup:
        orig_path = Path(original)
        if not orig_path.exists():
            continue
            
        # Crear ruta en backup manteniendo estructura relativa
        rel_path = orig_path.relative_to(PROJECT_ROOT)
        backup_path = backup_dir / rel_path
        
        # Asegurar que el directorio destino exista
        backup_path.parent.mkdir(exist_ok=True, parents=True)
        
        try:
            # Si ya existe en backup, agregar sufijo
            counter = 1
            while backup_path.exists():
                backup_path = backup_path.with_name(f"{backup_path.stem}_v{counter}{backup_path.suffix}")
                counter += 1
            
            shutil.move(str(orig_path), str(backup_path))
            actions.append((str(orig_path), str(backup_path)))
            print(f"  [MOVED] {rel_path} -> backup_legacy/{rel_path}")
        except Exception as e:
            print(f"  [ERROR] Moviendo {orig_path}: {e}")
    
    return actions

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================
def main():
    print("=" * 70)
    print("POKER COACH PRO - FASE 1: ANALIZADOR Y LIMPIADOR")
    print("=" * 70)
    print(f"Directorio raíz: {PROJECT_ROOT}")
    print(f"Directorio backup: {BACKUP_DIR}")
    print()
    
    # 1. Encontrar duplicados exactos (por hash)
    print("1. BUSCANDO DUPLICADOS EXACTOS (mismo contenido)...")
    exact_dups = find_duplicate_files_by_hash(PROJECT_ROOT)
    if exact_dups:
        print(f"   Se encontraron {len(exact_dups)} archivos duplicados exactos:")
        for dup, original in exact_dups[:10]:  # Mostrar primeros 10
            print(f"     - {dup} (duplicado de {original})")
        if len(exact_dups) > 10:
            print(f"     ... y otros {len(exact_dups) - 10} más.")
    else:
        print("   ✓ No se encontraron duplicados exactos.")
    
    # 2. Encontrar archivos con nombres similares
    print("\n2. BUSCANDO ARCHIVOS CON NOMBRES SIMILARES (posibles versiones)...")
    similar_files = find_similar_files_by_name(PROJECT_ROOT)
    if similar_files:
        print(f"   Se encontraron {len(similar_files)} grupos de archivos con nombres similares:")
        for base_name, files in list(similar_files.items())[:5]:
            print(f"     Grupo '{base_name}':")
            for f in files:
                print(f"       - {f}")
        if len(similar_files) > 5:
            print(f"     ... y otros {len(similar_files) - 5} grupos más.")
    else:
        print("   ✓ No se encontraron archivos con nombres similares.")
    
    # 3. Identificar archivos "candidatos" a limpieza (no esenciales)
    print("\n3. IDENTIFICANDO ARCHIVOS NO ESENCIALES...")
    candidate_files = []
    preserved_files = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        root_path = Path(root)
        
        # Saltar directorios excluidos
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        if any(excl in str(root_path) for excl in EXCLUDE_DIRS):
            continue
        
        for file in files:
            if any(file.endswith(ext) for ext in EXCLUDE_EXTENSIONS):
                continue
                
            filepath = root_path / file
            rel_path = filepath.relative_to(PROJECT_ROOT)
            
            if should_preserve(rel_path, CORE_PATTERNS):
                preserved_files.append(str(rel_path))
            else:
                candidate_files.append(str(filepath))
    
    print(f"   Se preservarán automáticamente: {len(preserved_files)} archivos")
    print(f"   Candidatos a revisión/backup: {len(candidate_files)} archivos")
    
    # 4. Mostrar algunos candidatos
    print("\n   Ejemplos de archivos candidatos (primeros 15):")
    for cand in candidate_files[:15]:
        print(f"     - {Path(cand).relative_to(PROJECT_ROOT)}")
    if len(candidate_files) > 15:
        print(f"     ... y otros {len(candidate_files) - 15} más.")
    
    # 5. Preguntar al usuario qué hacer
    print("\n" + "=" * 70)
    print("OPCIONES DE ACCIÓN:")
    print("  1) Crear backup de candidatos y eliminarlos (RECOMENDADO para empezar)")
    print("  2) Solo generar reporte, no hacer cambios")
    print("  3) Salir sin hacer nada")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        print("\nCREANDO BACKUP DE ARCHIVOS NO ESENCIALES...")
        # Primero mover duplicados exactos (excepto el primero de cada grupo)
        files_to_backup = []
        for dup, original in exact_dups:
            files_to_backup.append(dup)
        
        # Agregar archivos candidatos no esenciales
        files_to_backup.extend(candidate_files)
        
        # Eliminar duplicados de la lista
        files_to_backup = list(set(files_to_backup))
        
        print(f"Se moverán {len(files_to_backup)} archivos a 'backup_legacy/'")
        confirm = input("¿Continuar? (sí/no): ").lower()
        
        if confirm in ('s', 'si', 'sí', 'y', 'yes'):
            actions = create_backup_and_remove(files_to_backup, BACKUP_DIR)
            print(f"\n✓ COMPLETADO: {len(actions)} archivos movidos a backup_legacy/")
            print("\nRECOMENDACIONES:")
            print("  1. Revisa la carpeta 'backup_legacy' para asegurarte de no haber")
            print("     movido nada crítico.")
            print("  2. Ejecuta 'python phase1_cleanup_analyzer.py' nuevamente para")
            print("     ver el estado más limpio del proyecto.")
            print("  3. Cuando estés seguro, puedes eliminar 'backup_legacy' con:")
            print("     `rmdir /s /q backup_legacy` (Windows) o `rm -rf backup_legacy` (Linux/Mac)")
        else:
            print("Operación cancelada.")
    
    elif choice == "2":
        print("\nReporte generado. No se realizaron cambios.")
        print(f"Archivos a preservar: {len(preserved_files)}")
        print(f"Archivos candidatos: {len(candidate_files)}")
        print(f"Duplicados exactos: {len(exact_dups)}")
        print(f"Grupos similares: {len(similar_files)}")
        
        # Guardar reporte en archivo
        report_path = PROJECT_ROOT / "cleanup_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE LIMPIEZA - POKER COACH PRO\n")
            f.write("=" * 50 + "\n")
            f.write(f"Archivos preservados: {len(preserved_files)}\n")
            f.write(f"Archivos candidatos: {len(candidate_files)}\n")
            f.write(f"Duplicados exactos: {len(exact_dups)}\n")
            f.write(f"Grupos similares: {len(similar_files)}\n\n")
            
            f.write("ARCHIVOS CANDIDATOS (no esenciales):\n")
            for cand in candidate_files:
                f.write(f"  - {Path(cand).relative_to(PROJECT_ROOT)}\n")
            
            f.write("\nDUPLICADOS EXACTOS:\n")
            for dup, original in exact_dups:
                f.write(f"  - {dup} (copia de {original})\n")
        
        print(f"Reporte detallado guardado en: {report_path}")
    
    else:
        print("Operación cancelada.")
    
    print("\n" + "=" * 70)
    print("FASE 1 COMPLETADA. Siguiente paso: Fase 2 - Reestructuración.")
    print("=" * 70)

if __name__ == "__main__":
    main()