#!/usr/bin/env python3
"""
RESTAURA archivos importantes desde backup_legacy/ a src/
Ejecutar: python restore_from_backup.py
"""

import os
import shutil
from pathlib import Path

# Mapeo: Nombre archivo -> Nueva ubicación en src/
RESTORE_MAPPING = {
    # ARCHIVOS PRINCIPALES (alta prioridad)
    "poker_coach_core.py": "src/core/coach_core.py",
    "CARD_OCR_SYSTEM.py": "src/core/card_recognizer.py", 
    "POKERSTARS_CALIBRATOR.py": "src/integration/pokerstars_calibrator.py",
    "pokerstars_assistant.py": "src/integration/pokerstars_assistant.py",
    
    # ARCHIVOS DE SOPORTE (media prioridad)
    "complete_poker_learning_system.py": "src/core/learning_system.py",
    "auto_fix.py": "src/utils/auto_fixer.py",
    "check_system.py": "src/utils/system_checker.py",
    "window_selector.py": "src/utils/window_selector.py",
    
    # ARCHIVOS DE CONFIGURACIÓN (baja prioridad)
    "create_config.py": "src/utils/config_creator.py",
    "calibrate_positions.py": "src/integration/position_calibrator.py",
}

def find_in_backup(filename):
    """Busca un archivo en backup_legacy/ (recursivo)."""
    backup_path = Path("backup_legacy")
    if not backup_path.exists():
        return None
    
    for file_path in backup_path.rglob(filename):
        if file_path.is_file():
            return file_path
    return None

def restore_file(source_path, dest_path):
    """Restaura un archivo con verificación."""
    src = Path(source_path)
    dst = Path(dest_path)
    
    if not src.exists():
        return False, f"❌ No existe: {src}"
    
    # Crear directorio destino
    dst.parent.mkdir(parents=True, exist_ok=True)
    
    # Verificar si ya existe en destino
    if dst.exists():
        # Comparar tamaños
        src_size = src.stat().st_size
        dst_size = dst.stat().st_size
        
        if src_size == dst_size:
            return True, f"⚠️  Ya existe (mismo tamaño): {dst.name}"
        
        # Hacer backup del existente
        backup = dst.with_suffix(dst.suffix + '.old')
        shutil.copy2(dst, backup)
    
    try:
        # Copiar archivo
        shutil.copy2(src, dst)
        
        # Leer para verificar
        with open(dst, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        return True, f"✅ Restaurado: {src.name} -> {dst} ({len(lines)} líneas)"
    
    except Exception as e:
        return False, f"❌ Error: {e}"

def main():
    print("=" * 70)
    print("RESTAURADOR DE CÓDIGO - Poker Coach Pro")
    print("=" * 70)
    
    # Verificar backup_legacy
    backup_path = Path("backup_legacy")
    if not backup_path.exists():
        print("❌ ERROR: No se encuentra backup_legacy/")
        print("   La carpeta fue eliminada o renombrada.")
        return
    
    print(f"📁 Backup encontrado: {backup_path}")
    print(f"📦 Archivos a restaurar: {len(RESTORE_MAPPING)}")
    print()
    
    # 1. BUSCAR ARCHIVOS EN BACKUP
    print("1. 🔍 Buscando archivos en backup...")
    found_files = {}
    not_found = []
    
    for filename, dest in RESTORE_MAPPING.items():
        source_path = find_in_backup(filename)
        if source_path:
            found_files[filename] = (source_path, dest)
            print(f"   ✅ {filename} -> {dest}")
        else:
            not_found.append(filename)
            print(f"   ❌ {filename} (NO ENCONTRADO)")
    
    if not found_files:
        print("\n⚠️  No se encontró NINGÚN archivo para restaurar.")
        print("   Revisando estructura de backup...")
        
        # Mostrar qué hay en backup
        print("\n📂 Contenido de backup_legacy/ (primeros 20):")
        items = list(backup_path.rglob("*"))
        for item in items[:20]:
            if item.is_file():
                print(f"   • {item.relative_to(backup_path)}")
        return
    
    # 2. RESUMEN DE BÚSQUEDA
    print(f"\n📊 Resultados:")
    print(f"   ✅ Encontrados: {len(found_files)}")
    print(f"   ❌ No encontrados: {len(not_found)}")
    
    if not_found:
        print("\n   Archivos no encontrados:")
        for filename in not_found:
            print(f"     • {filename}")
    
    # 3. CONFIRMAR RESTAURACIÓN
    print("\n" + "=" * 70)
    print("❓ CONFIRMACIÓN DE RESTAURACIÓN")
    print("=" * 70)
    print("Se restaurarán los archivos a la nueva estructura src/")
    print("Los archivos originales permanecerán en backup_legacy/")
    
    response = input("\n¿Continuar con la restauración? (sí/no): ").lower().strip()
    if response not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Operación cancelada.")
        return
    
    # 4. RESTAURAR ARCHIVOS
    print("\n2. 🚀 Restaurando archivos...")
    success_count = 0
    failed_files = []
    
    for filename, (source_path, dest_path) in found_files.items():
        print(f"\n   📦 {filename}:")
        success, message = restore_file(source_path, dest_path)
        print(f"      {message}")
        
        if success:
            success_count += 1
        else:
            failed_files.append(filename)
    
    # 5. CREAR ARCHIVO DE INTEGRACIÓN
    print("\n3. 🧩 Creando integrador principal...")
    create_integrator(list(found_files.keys()))
    
    # 6. RESUMEN FINAL
    print("\n" + "=" * 70)
    print("✅ RESTAURACIÓN COMPLETADA")
    print("=" * 70)
    print(f"   Archivos restaurados: {success_count}/{len(found_files)}")
    
    if failed_files:
        print(f"   Fallos: {len(failed_files)}")
        for filename in failed_files:
            print(f"     • {filename}")
    
    # Mostrar estructura resultante
    print("\n📁 ESTRUCTURA DE src/ RESULTANTE:")
    print_structure()
    
    print("\n🎯 SIGUIENTE PASO:")
    print("   1. Revisa que los archivos estén en src/")
    print("   2. Ejecuta: python -c \"from src.main_integrator import *\"")
    print("   3. Luego prueba: python main.py")

def create_integrator(restored_files):
    """Crea archivo integrador con los módulos restaurados."""
    integrator_path = Path("src/main_integrator.py")
    
    # Crear imports basados en archivos restaurados
    imports = []
    classes = []
    
    mapping = {
        "poker_coach_core.py": ["PokerCoachCore", "from core.coach_core import PokerCoachCore"],
        "CARD_OCR_SYSTEM.py": ["CardOCRSystem", "from core.card_recognizer import CardOCRSystem"],
        "POKERSTARS_CALIBRATOR.py": ["PokerStarsCalibrator", "from integration.pokerstars_calibrator import PokerStarsCalibrator"],
        "pokerstars_assistant.py": ["PokerStarsAssistant", "from integration.pokerstars_assistant import PokerStarsAssistant"],
        "complete_poker_learning_system.py": ["PokerLearningSystem", "from core.learning_system import PokerLearningSystem"],
        "auto_fix.py": ["AutoFixer", "from utils.auto_fixer import AutoFixer"],
        "check_system.py": ["SystemChecker", "from utils.system_checker import SystemChecker"],
    }
    
    for filename in restored_files:
        if filename in mapping:
            class_name, import_stmt = mapping[filename]
            imports.append(import_stmt)
            classes.append(class_name)
    
    # Crear contenido del integrador
    content = '''"""
MAIN INTEGRATOR - Poker Coach Pro
Conecta todos los módulos restaurados del sistema.
Este archivo se genera automáticamente.
"""

import sys
import os

# Añadir ruta para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# === IMPORTS DE MÓDULOS RESTAURADOS ===
'''
    
    # Añadir imports
    for import_stmt in imports:
        content += f"{import_stmt}\n"
    
    # Añadir lista __all__
    content += f'''
__all__ = {classes}

# === VERIFICACIÓN DE MÓDULOS ===
def verify_modules():
    """Verifica que todos los módulos se importen correctamente."""
    print("🔍 VERIFICANDO MÓDULOS RESTAURADOS...")
    print("-" * 50)
    
    modules_status = []
'''
    
    # Añadir verificación para cada módulo
    for filename, (class_name, _) in mapping.items():
        if filename in restored_files:
            content += f'''
    # Verificar {class_name}
    try:
        from {mapping[filename][1].split(' import ')[0].replace('from ', '')} import {class_name}
        modules_status.append(("✅", "{class_name}", "{filename}"))
    except ImportError as e:
        modules_status.append(("❌", "{class_name}", f"Error: {{e}}"))
'''
    
    content += '''
    # Mostrar resultados
    for status, module, info in modules_status:
        print(f"{status} {module:20} | {info}")
    
    print("-" * 50)
    success = all(status == "✅" for status, _, _ in modules_status)
    
    if success:
        print("🎉 TODOS los módulos se importan correctamente!")
        return True
    else:
        print("⚠️  Algunos módulos tienen problemas de importación.")
        print("   Revisa los imports en los archivos individuales.")
        return False

if __name__ == "__main__":
    verify_modules()
'''
    
    # Escribir archivo
    integrator_path.parent.mkdir(exist_ok=True)
    integrator_path.write_text(content, encoding='utf-8')
    print(f"   ✅ Creado: {integrator_path}")

def print_structure():
    """Muestra la estructura de src/."""
    src_path = Path("src")
    if not src_path.exists():
        print("   (src/ no existe)")
        return
    
    for item in src_path.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(src_path)
            size_kb = item.stat().st_size / 1024
            print(f"   • {rel_path} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()