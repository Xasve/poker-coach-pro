#!/usr/bin/env python3
"""
 POKERSTARS_CALIBRATOR.py - Calibración Automática para PokerStars
Detecta y se adapta a diferentes temas y configuraciones de mesa
"""

import cv2
import numpy as np
import pyautogui
import time
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import mss

@dataclass
TableConfig:
    """Configuración de mesa detectada"""
    theme: str
    table_size: Tuple[int, int]
    card_positions: Dict[str, List[Tuple[int, int]]]
    chip_colors: Dict[str, Tuple[int, int, int]]
    button_positions: Dict[str, Tuple[int, int]]
    confidence: float
    
    def save(self, filename: str):
        """Guardar configuración a archivo"""
        config_dict = {
            "theme": self.theme,
            "table_size": self.table_size,
            "card_positions": self.card_positions,
            "chip_colors": {k: list(v) for k, v in self.chip_colors.items()},
            "button_positions": self.button_positions,
            "confidence": self.confidence,
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load(cls, filename: str):
        """Cargar configuración desde archivo"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return cls(
            theme=data["theme"],
            table_size=tuple(data["table_size"]),
            card_positions={k: [tuple(pos) for pos in v] for k, v in data["card_positions"].items()},
            chip_colors={k: tuple(v) for k, v in data["chip_colors"].items()},
            button_positions={k: tuple(v) for k, v in data["button_positions"].items()},
            confidence=data["confidence"]
        )

class PokerStarsCalibrator:
    """Calibrador automático para PokerStars"""
    
    def __init__(self):
        self.sct = mss.mss()
        self.themes = self._load_theme_profiles()
        self.current_config = None
        
    def _load_theme_profiles(self):
        """Cargar perfiles de temas conocidos"""
        return {
            "classic": {
                "table_color_range": ((30, 80, 30), (50, 100, 50)),
                "card_color": (240, 240, 220),
                "button_colors": {
                    "fold": (200, 50, 50),
                    "call": (50, 150, 50),
                    "raise": (50, 100, 200)
                }
            },
            "dark": {
                "table_color_range": ((10, 30, 10), (30, 60, 30)),
                "card_color": (50, 50, 70),
                "button_colors": {
                    "fold": (180, 60, 60),
                    "call": (60, 180, 60),
                    "raise": (60, 120, 220)
                }
            },
            "stealth": {
                "table_color_range": ((5, 15, 5), (25, 45, 25)),
                "card_color": (30, 30, 50),
                "button_colors": {
                    "fold": (160, 70, 70),
                    "call": (70, 160, 70),
                    "raise": (70, 140, 210)
                }
            }
        }
    
    def auto_calibrate(self):
        """Calibración automática completa"""
        print(" INICIANDO CALIBRACIÓN AUTOMÁTICA")
        print("="*50)
        
        # 1. Capturar pantalla
        print("\n Capturando pantalla...")
        screenshot = self.capture_screen()
        
        if screenshot is None:
            print(" No se pudo capturar pantalla")
            return None
        
        # 2. Detectar tema
        print(" Detectando tema de PokerStars...")
        theme = self.detect_theme(screenshot)
        print(f" Tema detectado: {theme}")
        
        # 3. Detectar mesa
        print(" Localizando mesa...")
        table_region = self.detect_table_region(screenshot, theme)
        
        if table_region is None:
            print(" No se detectó mesa de poker")
            return None
        
        print(f" Mesa localizada: {table_region}")
        
        # 4. Detectar posiciones de cartas
        print(" Detectando posiciones de cartas...")
        card_positions = self.detect_card_positions(screenshot, table_region, theme)
        print(f" Posiciones detectadas: {len(card_positions)} áreas")
        
        # 5. Detectar botones de acción
        print(" Detectando botones de acción...")
        button_positions = self.detect_action_buttons(screenshot, table_region, theme)
        print(f" Botones detectados: {list(button_positions.keys())}")
        
        # 6. Detectar colores de fichas
        print(" Detectando colores de fichas...")
        chip_colors = self.detect_chip_colors(screenshot, table_region)
        print(f" Colores detectados: {list(chip_colors.keys())}")
        
        # Crear configuración
        self.current_config = TableConfig(
            theme=theme,
            table_size=(table_region[2], table_region[3]),
            card_positions=card_positions,
            chip_colors=chip_colors,
            button_positions=button_positions,
            confidence=0.85
        )
        
        # Guardar configuración
        config_file = "config/pokerstars_calibration.json"
        Path("config").mkdir(exist_ok=True)
        self.current_config.save(config_file)
        
        print(f"\n CALIBRACIÓN COMPLETADA")
        print(f" Configuración guardada en: {config_file}")
        
        return self.current_config
    
    def capture_screen(self):
        """Capturar pantalla completa"""
        try:
            monitor = self.sct.monitors[1]
            screenshot = np.array(self.sct.grab(monitor))
            return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            print(f" Error capturando pantalla: {e}")
            return None
    
    def detect_theme(self, screenshot):
        """Detectar tema de PokerStars basado en colores"""
        # Analizar colores predominantes
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # Buscar verdes de mesa
        green_mask = cv2.inRange(hsv, (35, 40, 40), (85, 255, 255))
        green_pixels = cv2.countNonZero(green_mask)
        total_pixels = screenshot.shape[0] * screenshot.shape[1]
        green_ratio = green_pixels / total_pixels
        
        # Si hay mucho verde, es tema clásico
        if green_ratio > 0.1:
            return "classic"
        
        # Buscar colores oscuros
        dark_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 80))
        dark_pixels = cv2.countNonZero(dark_mask)
        dark_ratio = dark_pixels / total_pixels
        
        if dark_ratio > 0.3:
            # Distinguir entre dark y stealth
            # Analizar contraste
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            contrast = gray.std()
            
            if contrast < 50:
                return "stealth"
            else:
                return "dark"
        
        return "classic"  # Por defecto
    
    def detect_table_region(self, screenshot, theme):
        """Detectar región de la mesa"""
        height, width = screenshot.shape[:2]
        
        # Para cada tema, buscar características específicas
        if theme == "classic":
            # Buscar verde de mesa
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
        else:  # dark o stealth
            # Buscar áreas oscuras
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
        
        # Encontrar el contorno más grande (la mesa)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Tomar el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Verificar que sea tamaño razonable para una mesa
        if w < 400 or h < 300:
            return None
        
        return (x, y, w, h)
    
    def detect_card_positions(self, screenshot, table_region, theme):
        """Detectar posiciones donde aparecen las cartas"""
        x, y, w, h = table_region
        table_img = screenshot[y:y+h, x:x+w]
        
        card_positions = {
            "hero": [],      # Cartas del jugador
            "community": [], # Cartas comunitarias
            "opponents": []  # Cartas de oponentes (si visibles)
        }
        
        # Buscar áreas rectangulares claras (cartas)
        gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
        
        if theme == "classic":
            # Cartas claras sobre fondo oscuro
            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        else:
            # Cartas oscuras sobre fondo menos oscuro
            _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # Encontrar contornos rectangulares
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por tamaño de carta
            if 800 < area < 3000:
                xc, yc, wc, hc = cv2.boundingRect(contour)
                
                # Verificar relación de aspecto (~1.4:1 para cartas)
                aspect_ratio = wc / hc
                if 1.2 < aspect_ratio < 1.6:
                    # Posición absoluta
                    abs_x = x + xc
                    abs_y = y + yc
                    
                    # Clasificar por posición en la mesa
                    if abs_y > y + h * 0.7:  # Parte inferior (hero)
                        card_positions["hero"].append((abs_x, abs_y))
                    elif y + h * 0.3 < abs_y < y + h * 0.7:  # Centro (comunitarias)
                        card_positions["community"].append((abs_x, abs_y))
                    else:  # Parte superior (oponentes)
                        card_positions["opponents"].append((abs_x, abs_y))
        
        return card_positions
    
    def detect_action_buttons(self, screenshot, table_region, theme):
        """Detectar botones de acción (Fold, Call, Raise)"""
        x, y, w, h = table_region
        table_img = screenshot[y:y+h, x:x+w]
        
        button_positions = {}
        theme_profile = self.themes[theme]
        
        # Buscar colores específicos de botones
        hsv = cv2.cvtColor(table_img, cv2.COLOR_BGR2HSV)
        
        # Buscar botón FOLD (rojo)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red = cv2.bitwise_or(
            cv2.inRange(hsv, lower_red1, upper_red1),
            cv2.inRange(hsv, lower_red2, upper_red2)
        )
        
        fold_pos = self._find_button_position(mask_red, table_region)
        if fold_pos:
            button_positions["fold"] = fold_pos
        
        # Buscar botón CALL/CALL ANY (verde)
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        
        call_pos = self._find_button_position(mask_green, table_region)
        if call_pos:
            button_positions["call"] = call_pos
        
        # Buscar botón RAISE/BET (azul)
        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        raise_pos = self._find_button_position(mask_blue, table_region)
        if raise_pos:
            button_positions["raise"] = raise_pos
        
        return button_positions
    
    def _find_button_position(self, mask, table_region):
        """Encontrar posición central de un botón"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Tomar el contorno más grande
            largest = max(contours, key=cv2.contourArea)
            xc, yc, wc, hc = cv2.boundingRect(largest)
            
            # Verificar tamaño razonable para botón
            if 40 < wc < 150 and 20 < hc < 60:
                tx, ty, _, _ = table_region
                center_x = tx + xc + wc // 2
                center_y = ty + yc + hc // 2
                return (center_x, center_y)
        
        return None
    
    def detect_chip_colors(self, screenshot, table_region):
        """Detectar colores de fichas en la mesa"""
        x, y, w, h = table_region
        table_img = screenshot[y:y+h, x:x+w]
        
        chip_colors = {}
        
        # Definir rangos de color para fichas comunes
        color_ranges = {
            "white": ((0, 0, 200), (180, 30, 255)),
            "red": ((0, 100, 100), (10, 255, 255)),
            "blue": ((100, 100, 100), (140, 255, 255)),
            "green": ((35, 100, 100), (85, 255, 255)),
            "black": ((0, 0, 0), (180, 255, 50))
        }
        
        hsv = cv2.cvtColor(table_img, cv2.COLOR_BGR2HSV)
        
        for color_name, (lower, upper) in color_ranges.items():
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            
            mask = cv2.inRange(hsv, lower_np, upper_np)
            
            # Contar píxeles de este color
            pixel_count = cv2.countNonZero(mask)
            
            if pixel_count > 100:  # Umbral mínimo
                # Obtener color promedio
                mean_color = cv2.mean(table_img, mask=mask)[:3]
                chip_colors[color_name] = tuple(map(int, mean_color))
        
        return chip_colors
    
    def test_calibration(self):
        """Probar calibración actual"""
        if not self.current_config:
            print(" No hay calibración activa")
            return False
        
        print("\n PROBANDO CALIBRACIÓN...")
        print("="*50)
        
        screenshot = self.capture_screen()
        if screenshot is None:
            return False
        
        tests_passed = 0
        total_tests = 3
        
        # Test 1: Verificar tema
        print("\n Test 1: Verificando tema...")
        detected_theme = self.detect_theme(screenshot)
        if detected_theme == self.current_config.theme:
            print(f" Tema correcto: {detected_theme}")
            tests_passed += 1
        else:
            print(f" Tema incorrecto: Esperado {self.current_config.theme}, Detectado {detected_theme}")
        
        # Test 2: Verificar mesa
        print("\n Test 2: Verificando mesa...")
        table_region = self.detect_table_region(screenshot, detected_theme)
        if table_region:
            print(f" Mesa detectada: {table_region}")
            tests_passed += 1
        else:
            print(" No se detectó mesa")
        
        # Test 3: Verificar botones
        print("\n Test 3: Verificando botones...")
        buttons = self.detect_action_buttons(screenshot, table_region, detected_theme)
        if buttons:
            print(f" Botones detectados: {len(buttons)}")
            tests_passed += 1
        else:
            print(" No se detectaron botones")
        
        print(f"\n RESULTADO: {tests_passed}/{total_tests} tests pasados")
        
        return tests_passed == total_tests

def main():
    """Función principal"""
    print(" POKERSTARS CALIBRATOR - Calibración Automática")
    print("="*60)
    
    calibrator = PokerStarsCalibrator()
    
    print("\n OPCIONES:")
    print("1.  Calibración automática completa")
    print("2.  Probar calibración existente")
    print("3.  Cargar calibración guardada")
    print("4.  Calibrar solo tema")
    print("5.  Salir")
    
    choice = input("\nSeleccione opción (1-5): ").strip()
    
    if choice == "1":
        config = calibrator.auto_calibrate()
        if config:
            print("\n Calibración exitosa")
            
            # Preguntar si probar
            test = input("\nProbar calibración? (s/n): ").strip().lower()
            if test == 's':
                calibrator.test_calibration()
    
    elif choice == "2":
        # Cargar y probar
        config_file = "config/pokerstars_calibration.json"
        if Path(config_file).exists():
            config = TableConfig.load(config_file)
            calibrator.current_config = config
            calibrator.test_calibration()
        else:
            print(" No hay calibración guardada")
    
    elif choice == "3":
        config_file = "config/pokerstars_calibration.json"
        if Path(config_file).exists():
            config = TableConfig.load(config_file)
            calibrator.current_config = config
            print(f" Configuración cargada: Tema {config.theme}")
        else:
            print(" Archivo no encontrado")
    
    elif choice == "4":
        screenshot = calibrator.capture_screen()
        if screenshot is not None:
            theme = calibrator.detect_theme(screenshot)
            print(f" Tema detectado: {theme}")
    
    elif choice == "5":
        print(" Saliendo...")
        return
    
    else:
        print(" Opción no válida")
    
    input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
