"""
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
        
        print("
3. Coloca el cursor en la ESQUINA INFERIOR DERECHA")
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
        print(f"
✅ Mesa calibrada: {x2-x1}x{y2-y1} píxeles")
        return True
    
    def calibrate_card_position(self, position_name, description):
        """Calibra una posición de carta específica."""
        print(f"
🎴 {description}")
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
            calibrate = input(f"
¿Calibrar {pos_desc}? (s/n): ").lower()
            if calibrate in ['s', 'si', 'sí']:
                self.calibrate_card_position(pos_key, pos_desc)
        
        self.save_config()
        print("
" + "=" * 60)
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
    
    choice = input("
Selecciona (1-3): ").strip()
    
    if choice == "1":
        calibrator.run_full_calibration()
    elif choice == "2":
        calibrator.calibrate_table_interactive()
    elif choice == "3":
        print(f"
📋 Configuración actual:")
        print(json.dumps(calibrator.config, indent=2))
    else:
        print("❌ Opción inválida")
    
    print("
Presiona Enter para salir...")
    input()

if __name__ == "__main__":
    main()
