#!/usr/bin/env python3
"""
Organiza archivos Python funcionales en la estructura src/
Ejecutar: python organize_to_src.py
"""

import os
import shutil
from pathlib import Path

# Mapeo de archivos actuales -> nueva ubicación en src/
FILE_MAPPING = {
    # Archivos principales que sabemos que existen
    "poker_coach_core.py": "src/core/coach_core.py",
    "CARD_OCR_SYSTEM.py": "src/core/card_recognizer.py",
    "POKERSTARS_CALIBRATOR.py": "src/integration/pokerstars_calibrator.py",
    "pokerstars_assistant.py": "src/integration/pokerstars_assistant.py",
    
    # Archivos de utilidad
    "auto_fix.py": "src/utils/auto_fix.py",
    "check_system.py": "src/utils/system_check.py",
    
    # Archivos de lógica de juego
    "complete_poker_learning_system.py": "src/core/learning_system.py",
    
    # Archivos de inicio/ejecución (NO mover estos - quedan en raíz)
    # "start_coach.py": "RAÍZ",  # No mover - punto de entrada
    # "run_poker.py": "RAÍZ",    # No mover - punto de entrada
}

def safe_move_file(source, destination):
    """Mueve un archivo de manera segura con backup."""
    src_path = Path(source)
    dst_path = Path(destination)
    
    if not src_path.exists():
        print(f"  ⚠️  No existe: {source}")
        return False
    
    # Crear directorio destino si no existe
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Si el destino ya existe, crear backup
    if dst_path.exists():
        backup_path = dst_path.with_suffix(dst_path.suffix + '.backup')
        shutil.copy2(dst_path, backup_path)
        print(f"  💾 Backup creado: {backup_path.name}")
    
    try:
        # Mover el archivo
        shutil.move(str(src_path), str(dst_path))
        print(f"  ✅ Movido: {source} -> {destination}")
        return True
    except Exception as e:
        print(f"  ❌ Error moviendo {source}: {e}")
        return False

def analyze_current_files():
    """Analiza qué archivos existen actualmente."""
    print("🔍 Analizando archivos disponibles...")
    existing_files = {}
    
    for source, dest in FILE_MAPPING.items():
        if Path(source).exists():
            existing_files[source] = dest
            
            # Mostrar información del archivo
            with open(source, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
                
            print(f"  📄 {source}")
            print(f"     → Destino: {dest}")
            print(f"     → Líneas: {len(lines)} total, {len(code_lines)} código")
            
            # Mostrar primera línea significativa
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    preview = line.strip()[:60] + ('...' if len(line.strip()) > 60 else '')
                    print(f"     → Ejemplo: {preview}")
                    break
            print()
    
    return existing_files

def create_init_files():
    """Crea archivos __init__.py necesarios."""
    init_paths = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/integration/__init__.py",
        "src/utils/__init__.py",
    ]
    
    for path in init_paths:
        p = Path(path)
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# Package initialization\n")
            print(f"  📄 Creado: {path}")

def main():
    print("=" * 60)
    print("ORGANIZADOR DE CÓDIGO - Poker Coach Pro")
    print("=" * 60)
    
    # 1. Verificar estructura
    print("\n1. 🏗️  Verificando estructura de directorios...")
    create_init_files()
    
    # 2. Analizar archivos existentes
    print("\n2. 📊 Archivos disponibles para organizar:")
    existing_files = analyze_current_files()
    
    if not existing_files:
        print("  ⚠️  No se encontraron archivos para organizar.")
        print("  ℹ️  Asegúrate de que los archivos principales existan en la raíz.")
        return
    
    # 3. Confirmar con el usuario
    print("\n3. ❓ Confirmación de cambios:")
    print(f"  Se moverán {len(existing_files)} archivos a la estructura src/")
    print("  Los archivos originales se ELIMINARÁN de su ubicación actual.")
    
    response = input("\n  ¿Continuar? (sí/no): ").lower().strip()
    if response not in ['s', 'si', 'sí', 'y', 'yes']:
        print("  Operación cancelada.")
        return
    
    # 4. Mover archivos
    print("\n4. 🚀 Moviendo archivos...")
    moved_count = 0
    
    for source, dest in existing_files.items():
        print(f"\n  📦 Procesando: {source}")
        if safe_move_file(source, dest):
            moved_count += 1
    
    # 5. Crear archivo de integración principal
    print("\n5. 🧩 Creando integrador principal...")
    create_main_integrator()
    
    # 6. Resumen
    print("\n" + "=" * 60)
    print("✅ ORGANIZACIÓN COMPLETADA")
    print("=" * 60)
    print(f"  Archivos movidos: {moved_count}/{len(existing_files)}")
    print(f"  Estructura creada en: src/")
    print("\n  📁 Estructura actual de src/:")
    for root, dirs, files in os.walk("src"):
        level = root.replace("src", "").count(os.sep)
        indent = "  " * level
        print(f"{indent}├── {os.path.basename(root) or 'src'}/")
        subindent = "  " * (level + 1)
        for file in files[:10]:  # Mostrar primeros 10 archivos por carpeta
            print(f"{subindent}├── {file}")
        if len(files) > 10:
            print(f"{subindent}└── ... y {len(files) - 10} más")
    
    print("\n🎯 SIGUIENTE PASO:")
    print("  Ejecuta 'python main.py' para verificar que todo funciona.")
    print("  Si hay errores de import, necesitaremos ajustar los imports en los archivos.")

def create_main_integrator():
    """Crea un archivo integrador principal en src/."""
    integrator_path = Path("src/main_integrator.py")
    
    integrator_content = '''"""
Integrador principal - Conecta todos los módulos de Poker Coach Pro
Este archivo importa todos los componentes del sistema.
"""

import sys
import os

# Añadir el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Re-exportar los módulos principales
try:
    from core.coach_core import PokerCoachCore
    from core.card_recognizer import CardOCRSystem
    from core.learning_system import PokerLearningSystem
    from integration.pokerstars_calibrator import PokerStarsCalibrator
    from integration.pokerstars_assistant import PokerStarsAssistant
    from utils.system_check import SystemChecker
    
    __all__ = [
        'PokerCoachCore',
        'CardOCRSystem', 
        'PokerLearningSystem',
        'PokerStarsCalibrator',
        'PokerStarsAssistant',
        'SystemChecker'
    ]
    
    print("✅ Todos los módulos importados correctamente")
    
except ImportError as e:
    print(f"⚠️  Error de importación: {e}")
    print("   Algunos módulos pueden no estar disponibles aún.")
'''

    integrator_path.parent.mkdir(exist_ok=True)
    integrator_path.write_text(integrator_content, encoding='utf-8')
    print(f"  📄 Creado: {integrator_path}")

if __name__ == "__main__":
    main()