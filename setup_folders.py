#!/usr/bin/env python3
"""
Script para crear la estructura de directorios del Poker Coach Pro
CORREGIDO - VERSIÓN FUNCIONAL
"""

import os
import sys

def create_structure(base_path="."):
    """Crea toda la estructura de directorios y archivos base"""
    
    structure = {
        "config": ["ggpoker_config.json", "pokerstars_config.json", "general_settings.json", "stealth_config.json"],
        "src/core": ["__init__.py", "poker_engine.py", "game_state.py", "equity_calculator.py"],
        "src/platforms": ["__init__.py", "ggpoker_adapter.py", "pokerstars_adapter.py", "base_adapter.py"],
        "src/screen_capture": ["__init__.py", "screen_reader.py", "card_recognizer.py", "table_detector.py", "text_ocr.py", "stealth_capture.py"],
        "src/overlay": ["__init__.py", "overlay_gui.py", "overlay_server.py", "styles.css"],
        "src/strategies": ["__init__.py", "preflop_strategy.py", "postflop_strategy.py", "tournament_strategy.py", "cash_strategy.py"],
        "src/database": ["__init__.py", "hand_history_db.py", "player_stats_db.py", "session_db.py"],
        "src/utils": ["__init__.py", "logger.py", "helpers.py", "constants.py"],
        "src/security": ["__init__.py", "anti_detection.py", "process_protector.py"],
        "data/card_templates/ggpoker": [],
        "data/card_templates/pokerstars": [],
        "data/table_templates": [],
        "data/fonts": [],
        "data/logs": [],
        "data/hand_history": [],
        "scripts": ["install_deps.bat", "install_deps.sh"],
        "docs": ["setup_guide.md", "ggpoker_guide.md", "pokerstars_guide.md", "strategy_guide.md", "stealth_guide.md"],
        "tests": ["test_screen_capture.py", "test_poker_engine.py", "test_overlay.py"]
    }
    
    print("Creando estructura de directorios...")
    
    # Crear directorios y archivos
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"  ✅ {folder_path}")
        
        for file in files:
            filepath = os.path.join(folder_path, file)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    if file.endswith('.py'):
                        f.write(f'"""\nArchivo: {file}\nRuta: {folder}/{file}\n"""\n\n')
                    elif file.endswith('.json'):
                        f.write('{\n    "version": "1.0"\n}\n')
                    elif file.endswith('.md'):
                        f.write(f'# {file}\n\nDocumentación\n')
                    elif file.endswith('.css'):
                        f.write('/* Estilos CSS */\n')
                    elif file.endswith('.bat') or file.endswith('.sh'):
                        pass  # Scripts vacíos por ahora
                    else:
                        f.write(f'# {file}\n')
                print(f"    📄 {file}")
    
    # Crear archivos raíz importantes
    create_root_files(base_path)
    
    print(f"\n✅ Estructura creada exitosamente en: {os.path.abspath(base_path)}")
    print("\n🎴 Para instalar dependencias:")
    print("   1. pip install -r requirements.txt")
    print("   2. python start_coach.py")

def create_root_files(base_path):
    """Crear archivos principales en la raíz"""
    
    # requirements.txt
    req_content = """# Dependencias principales
opencv-python>=4.8.0
numpy>=1.24.0
pillow>=10.0.0
pytesseract>=0.3.10
pandas>=2.0.0
python-socketio>=5.9.0
websockets>=12.0
pyautogui>=0.9.54
mss>=9.0.1
psutil>=5.9.0
tinydb>=4.8.0

# Para Windows
pywin32>=306
pypiwin32>=223

# Para desarrollo
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
"""
    
    with open(os.path.join(base_path, "requirements.txt"), 'w', encoding='utf-8') as f:
        f.write(req_content)
    
    # start_coach.py (versión simple)
    start_content = '''#!/usr/bin/env python3
"""
Poker Coach Pro - Script de inicio simplificado
Versión simple para comenzar
"""

print("🎴 POKER COACH PRO - INSTALACIÓN NECESARIA")
print("="*50)
print()
print("Primero necesitas instalar las dependencias:")
print("1. Abre una terminal como Administrador")
print("2. Navega a esta carpeta")
print("3. Ejecuta: pip install -r requirements.txt")
print()
print("Si hay errores, ejecuta estos comandos uno por uno:")
print("pip install opencv-python numpy pillow")
print("pip install pyautogui mss psutil")
print("pip install pytesseract pandas")
print()
input("Presiona Enter para salir...")
'''
    
    with open(os.path.join(base_path, "start_coach.py"), 'w', encoding='utf-8') as f:
        f.write(start_content)
    
    # main.py (versión mínima)
    main_content = '''#!/usr/bin/env python3
"""
Poker Coach Pro - Versión mínima para comenzar
"""

print("🎴 POKER COACH PRO - VERSIÓN MÍNIMA")
print("="*50)
print()
print("Para comenzar, ejecuta primero:")
print("python setup_folders.py")
print("pip install -r requirements.txt")
print()
print("Luego puedes ejecutar:")
print("python start_coach.py")
print()
input("Presiona Enter para salir...")
'''
    
    with open(os.path.join(base_path, "main.py"), 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    # README.md
    readme_content = '''# Poker Coach Pro

Sistema de asistencia para poker en tiempo real.

## Instalación Rápida:

1. Ejecutar: `python setup_folders.py`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `python start_coach.py`

## Problemas Comunes:

Si hay errores de instalación:
- Ejecuta como Administrador
- Usa: `python -m pip install --upgrade pip`
- Instala Visual C++ Build Tools
'''
    
    with open(os.path.join(base_path, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    print("="*60)
    print("POKER COACH PRO - SETUP DE ESTRUCTURA")
    print("="*60)
    create_structure()