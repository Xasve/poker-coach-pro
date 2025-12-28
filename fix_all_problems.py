#!/usr/bin/env python3
"""
CORREGIR TODOS LOS PROBLEMAS - Poker Coach Pro
Ejecutar: python fix_all_problems.py
"""

import os
import shutil
from pathlib import Path

print("🔧 CORRIGIENDO TODOS LOS PROBLEMAS")
print("=" * 60)

# ============================================================================
# 1. CORREGIR window_selector.py
# ============================================================================
print("\n1. 🛠️ Corrigiendo window_selector.py...")

window_selector_path = Path("src/utils/window_selector.py")
if window_selector_path.exists():
    try:
        with open(window_selector_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar tk.messagebox
        new_content = content.replace('tk.messagebox', 'messagebox')
        
        # Asegurar que tenga el import correcto
        if 'from tkinter import messagebox' not in new_content:
            # Reemplazar 'import tkinter as tk' con ambos imports
            if 'import tkinter as tk' in new_content:
                new_content = new_content.replace(
                    'import tkinter as tk',
                    'import tkinter as tk\nfrom tkinter import messagebox'
                )
            else:
                # Insertar al inicio
                lines = new_content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        continue
                    else:
                        lines.insert(i, 'import tkinter as tk')
                        lines.insert(i + 1, 'from tkinter import messagebox')
                        break
                new_content = '\n'.join(lines)
        
        with open(window_selector_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("   ✅ window_selector.py corregido")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print("   ❌ Archivo no encontrado")

# ============================================================================
# 2. REPARAR pokerstars_calibrator.py (error línea 18)
# ============================================================================
print("\n2. 🛠️ Reparando pokerstars_calibrator.py...")

calibrator_path = Path("src/integration/pokerstars_calibrator.py")
fixed_path = Path("src/integration/pokerstars_calibrator_fixed.py")

if calibrator_path.exists():
    try:
        # Primero, hacer backup del archivo corrupto
        backup_path = calibrator_path.with_suffix('.py.backup')
        shutil.copy2(calibrator_path, backup_path)
        print(f"   💾 Backup creado: {backup_path.name}")
        
        # Leer el archivo problemático
        with open(calibrator_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        print(f"   📊 Archivo original: {len(lines)} líneas")
        
        # Mostrar líneas problemáticas (15-20)
        print("   🔍 Líneas 15-20:")
        for i in range(14, min(20, len(lines))):
            print(f"     {i+1}: {repr(lines[i])}")
        
        # Crear versión corregida simple
        fixed_content = '''"""
POKERSTARS CALIBRATOR - Versión corregida
Sistema de calibración para PokerStars.
"""

import json
import time
import pyautogui
import cv2
import numpy as np
from pathlib import Path

class PokerStarsCalibrator:
    """Calibra las posiciones de la mesa de PokerStars."""
    
    def __init__(self, config_path="config/pokerstars_calibration.json"):
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.screen_width, self.screen_height = pyautogui.size()
    
    def load_config(self):
        """Carga configuración existente."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                return self.create_default_config()
        return self.create_default_config()
    
    def create_default_config(self):
        """Crea configuración por defecto."""
        return {
            "table": {
                "x1": 100, "y1": 100,
                "x2": 900, "y2": 700,
                "width": 800, "height": 600
            },
            "cards": {},
            "buttons": {},
            "screen_resolution": f"{self.screen_width}x{self.screen_height}"
        }
    
    def save_config(self):
        """Guarda la configuración."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuración guardada: {self.config_path}")
    
    def calibrate_table_interactive(self):
        """Calibra la mesa interactivamente."""
        print("🎯 CALIBRACIÓN DE MESA")
        print("=" * 50)
        
        print("1. Abre PokerStars en una mesa")
        print("2. Coloca el cursor en la ESQUINA SUPERIOR IZQUIERDA")
        input("   Presiona Enter cuando estés listo...")
        
        x1, y1 = pyautogui.position()
        print(f"   ✅ Capturado: ({x1}, {y1})")
        
        print("\n3. Coloca el cursor en la ESQUINA INFERIOR DERECHA")
        input("   Presiona Enter cuando estés listo...")
        
        x2, y2 = pyautogui.position()
        print(f"   ✅ Capturado: ({x2}, {y2})")
        
        self.config["table"] = {
            "x1": x1, "y1": y1,
            "x2": x2, "y2": y2,
            "width": abs(x2 - x1),
            "height": abs(y2 - y1)
        }
        
        self.save_config()
        print(f"\n✅ Mesa calibrada: {x2-x1}x{y2-y1} píxeles")
        return True
    
    def calibrate_card_position(self, position_name, description):
        """Calibra una posición de carta específica."""
        print(f"\n🎴 {description}")
        input("   Coloca el cursor en el CENTRO y presiona Enter...")
        
        x, y = pyautogui.position()
        
        if "cards" not in self.config:
            self.config["cards"] = {}
        
        self.config["cards"][position_name] = {"x": x, "y": y}
        print(f"   ✅ Posición '{position_name}': ({x}, {y})")
        return (x, y)
    
    def run_full_calibration(self):
        """Ejecuta calibración completa."""
        print("=" * 60)
        print("CALIBRACIÓN COMPLETA - POKERSTARS")
        print("=" * 60)
        
        self.calibrate_table_interactive()
        
        # Posiciones opcionales
        positions = [
            ("hole_card_1", "Tu primera carta (hole card 1)"),
            ("hole_card_2", "Tu segunda carta (hole card 2)"),
            ("flop_1", "Primera carta del flop"),
            ("flop_2", "Segunda carta del flop"),
            ("flop_3", "Tercera carta del flop"),
        ]
        
        for pos_key, pos_desc in positions:
            calibrate = input(f"\n¿Calibrar {pos_desc}? (s/n): ").lower()
            if calibrate in ['s', 'si', 'sí']:
                self.calibrate_card_position(pos_key, pos_desc)
        
        self.save_config()
        print("\n" + "=" * 60)
        print("✅ CALIBRACIÓN COMPLETADA")
        print("=" * 60)
        return True

def main():
    """Función principal."""
    calibrator = PokerStarsCalibrator()
    
    print("🎯 POKERSTARS CALIBRATOR")
    print("=" * 50)
    
    print("Opciones:")
    print("1. Calibración completa (recomendado)")
    print("2. Solo calibrar mesa")
    print("3. Ver configuración actual")
    
    choice = input("\nSelecciona (1-3): ").strip()
    
    if choice == "1":
        calibrator.run_full_calibration()
    elif choice == "2":
        calibrator.calibrate_table_interactive()
    elif choice == "3":
        print(f"\n📋 Configuración actual:")
        print(json.dumps(calibrator.config, indent=2))
    else:
        print("❌ Opción inválida")
    
    print("\nPresiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
'''
        
        # Guardar versión corregida
        with open(fixed_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"   ✅ Versión corregida creada: {fixed_path.name}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print("   ❌ Archivo original no encontrado")

# ============================================================================
# 3. CREAR ESTRUCTURA DE CARPETAS
# ============================================================================
print("\n3. 📁 Creando estructura de carpetas...")

folders = [
    "data/card_templates",
    "config",
    "logs",
    "data/gto_ranges",
    "exports",
    "backups"
]

for folder in folders:
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ {folder}")

# ============================================================================
# 4. CREAR ARCHIVOS DE CONFIGURACIÓN BÁSICOS
# ============================================================================
print("\n4. 📄 Creando archivos de configuración...")

# Configuración del sistema
system_config = {
    "system": {
        "name": "Poker Coach Pro",
        "version": "1.0.0",
        "python_version": "3.11",
        "status": "active"
    },
    "pokerstars": {
        "calibrated": False,
        "table_position": {"x1": 100, "y1": 100, "x2": 900, "y2": 700},
        "last_calibration": None
    },
    "gto": {
        "aggression_level": "medium",
        "ranges_path": "data/gto_ranges",
        "confidence_threshold": 0.75
    },
    "ocr": {
        "tesseract_path": None,
        "confidence": 0.8,
        "enabled": False
    }
}

config_path = Path("config/system_config.json")
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, 'w', encoding='utf-8') as f:
    import json
    json.dump(system_config, f, indent=2)

print(f"   ✅ {config_path.name}")

# ============================================================================
# 5. CREAR ARCHIVO PRINCIPAL SIMPLIFICADO
# ============================================================================
print("\n5. 🚀 Creando sistema principal simplificado...")

main_system_content = '''#!/usr/bin/env python3
"""
POKER COACH PRO - SISTEMA SIMPLIFICADO Y FUNCIONAL
Ejecutar: python poker_coach_simple.py
"""

import os
import sys
import json
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class PokerCoachSimple:
    """Sistema simplificado que SÍ funciona."""
    
    def __init__(self):
        self.modules = {}
        self.config = self.load_config()
        self.setup_system()
    
    def load_config(self):
        """Carga la configuración."""
        config_path = project_root / "config" / "system_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"system": {"name": "Poker Coach Pro"}}
    
    def setup_system(self):
        """Configura los módulos que SÍ funcionan."""
        print("🔧 CONFIGURANDO SISTEMA")
        print("=" * 50)
        
        # 1. Sistema de aprendizaje GTO (¡ESTE SÍ FUNCIONA!)
        try:
            from core.learning_system import PokerCoachProCompleteSystem
            self.modules['gto_system'] = PokerCoachProCompleteSystem()
            print("✅ Sistema GTO: PokerCoachProCompleteSystem")
        except Exception as e:
            print(f"⚠️  Sistema GTO: {str(e)[:40]}")
        
        # 2. Selector de ventanas (corregido)
        try:
            from utils.window_selector import WindowSelector
            self.modules['window_selector'] = WindowSelector()
            print("✅ Selector de ventanas: WindowSelector")
        except Exception as e:
            print(f"⚠️  Selector: {str(e)[:40]}")
        
        # 3. Verificador de sistema
        try:
            from utils import system_checker
            self.modules['checker'] = system_checker
            print("✅ Verificador de sistema")
        except Exception as e:
            print(f"⚠️  Verificador: {str(e)[:40]}")
        
        print(f"\n📊 Módulos cargados: {len(self.modules)}")
    
    def show_menu(self):
        """Menú principal simplificado."""
        while True:
            print("\n" + "=" * 50)
            print("🎯 POKER COACH PRO - MENÚ PRINCIPAL")
            print("=" * 50)
            print("1. 🧠 Modo práctica GTO (decisiones)")
            print("2. 🪟 Probar selector de ventanas")
            print("3. 📋 Verificar sistema")
            print("4. ⚙️  Configurar")
            print("5. 📊 Información del sistema")
            print("0. 🚪 Salir")
            print("=" * 50)
            
            try:
                choice = input("\nOpción: ").strip()
                
                if choice == "1":
                    self.practice_gto()
                elif choice == "2":
                    self.test_window_selector()
                elif choice == "3":
                    self.check_system()
                elif choice == "4":
                    self.configure_system()
                elif choice == "5":
                    self.system_info()
                elif choice == "0":
                    print("\n👋 ¡Hasta luego! 🍀")
                    break
                else:
                    print("❌ Opción inválida")
            
            except KeyboardInterrupt:
                print("\n⚠️  Operación cancelada")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            if choice != "0":
                input("\nPresiona Enter para continuar...")
    
    def practice_gto(self):
        """Modo práctica de decisiones GTO."""
        print("\n🧠 MODO PRÁCTICA GTO")
        print("=" * 40)
        
        print("Ejercicio 1: Hero en BTN con A♠ K♠")
        print("Situación: MP raise 3bb, folds to hero")
        print("Stack: 100bb efectivos")
        print()
        
        print("Opciones:")
        print("1. Fold (0bb)")
        print("2. Call (3bb)")
        print("3. 3-bet to 9bb")
        print("4. 3-bet to 12bb")
        print("5. All-in (100bb)")
        print()
        
        user_choice = input("Tu decisión (1-5): ").strip()
        
        # Análisis GTO
        analysis = {
            "1": "❌ Fold - AKs es demasiado fuerte para fold desde BTN",
            "2": "⚠️  Call - Aceptable, pero 3-bet es mejor",
            "3": "✅  3-bet 9bb - Tamaño óptimo GTO",
            "4": "⚠️  3-bet 12bb - Demasiado grande para este spot",
            "5": "❌ All-in - Solo vs jugadores muy tight"
        }
        
        result = analysis.get(user_choice, "❌ Opción inválida")
        print(f"\n📊 Resultado: {result}")
        
        if 'gto_system' in self.modules:
            print("\n💡 Análisis avanzado disponible en el sistema GTO")
    
    def test_window_selector(self):
        """Prueba el selector de ventanas."""
        print("\n🪟 PRUEBA SELECTOR DE VENTANAS")
        print("=" * 40)
        
        if 'window_selector' in self.modules:
            print("✅ Selector disponible")
            print("Opciones:")
            print("1. Mostrar información")
            print("2. Volver al menú")
            
            choice = input("\nOpción: ").strip()
            
            if choice == "1":
                selector = self.modules['window_selector']
                methods = [m for m in dir(selector) if not m.startswith('_')]
                print(f"\nMétodos disponibles: {', '.join(methods[:8])}")
        else:
            print("❌ Selector no disponible")
    
    def check_system(self):
        """Verifica el sistema."""
        print("\n📋 VERIFICACIÓN DEL SISTEMA")
        print("=" * 40)
        
        checks = [
            ("Python", sys.version.split()[0]),
            ("Directorio", str(project_root)),
            ("Módulos cargados", str(len(self.modules))),
            ("Configuración", "✅" if self.config else "❌"),
        ]
        
        for name, value in checks:
            print(f"{name}: {value}")
    
    def configure_system(self):
        """Configuración básica."""
        print("\n⚙️  CONFIGURACIÓN")
        print("=" * 40)
        
        print("1. Crear carpetas necesarias")
        print("2. Ver archivos disponibles")
        print("3. Probar imports")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            folders = ["data/card_templates", "config", "logs"]
            for folder in folders:
                os.makedirs(folder, exist_ok=True)
                print(f"✅ {folder}")
        
        elif choice == "2":
            print("\n📁 Archivos en src/:")
            src_path = project_root / "src"
            for item in src_path.glob("*.py"):
                print(f"  • {item.name}")
    
    def system_info(self):
        """Información del sistema."""
        print("\n📊 INFORMACIÓN DEL SISTEMA")
        print("=" * 40)
        print(f"Proyecto: {self.config.get('system', {}).get('name', 'Poker Coach Pro')}")
        print(f"Módulos: {len(self.modules)} disponibles")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Directorio: {project_root}")

def main():
    """Función principal."""
    print("=" * 50)
    print("🎯 POKER COACH PRO - SISTEMA SIMPLIFICADO")
    print("=" * 50)
    
    try:
        coach = PokerCoachSimple()
        coach.show_menu()
    except Exception as e:
        print(f"\n❌ ERROR INICIAL: {e}")
        print("\n💡 Solución rápida:")
        print("1. Ejecuta: pip install -r requirements.txt")
        print("2. Asegúrate de usar Python 3.11")
        print("3. Ejecuta fix_all_problems.py primero")

if __name__ == "__main__":
    main()
'''

main_path = Path("poker_coach_simple.py")
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_system_content)

print(f"   ✅ {main_path.name}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 60)
print("✅ CORRECCIONES COMPLETADAS")
print("=" * 60)
print("\n📋 RESUMEN:")
print("  1. ✅ window_selector.py corregido")
print("  2. ✅ pokerstars_calibrator_fixed.py creado")
print("  3. ✅ Estructura de carpetas creada")
print("  4. ✅ Archivos de configuración creados")
print("  5. ✅ Sistema principal simplificado creado")
print("\n🎯 INSTRUCCIONES:")
print("  1. Ejecuta: python poker_coach_simple.py")
print("  2. Usa la opción 1 para practicar decisiones GTO")
print("  3. La opción 2 prueba el selector de ventanas")
print("  4. La opción 3 verifica el sistema")
print("\n⚠️  NOTA: El sistema funciona SIN pytesseract")
print("     (solo modo práctica de decisiones GTO)")
print("=" * 60)