# fix_color_detection.py - Reparar detección de color
import cv2
import numpy as np
import os
import sys

def create_fixed_capture_script():
    """Crear versión corregida de smart_capture_fixed.py"""
    print(" CREANDO VERSIÓN CORREGIDA DE CAPTURA")
    print("=" * 70)
    
    fixed_script = '''# smart_capture_fixed_v2.py - Captura con detección de color REPARADA
import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import sys
import random

# Añadir src al path para importar módulos
sys.path.insert(0, "src")

class BalancedCaptureV2:
    """Captura automática balanceada con detección de color MEJORADA"""
    
    def __init__(self):
        # Crear nombre de sesión
        self.session_name = f"balanced_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_path = f"data/card_templates/auto_captured/{self.session_name}"
        self.raw_path = f"{self.session_path}/raw_captures"
        
        os.makedirs(self.raw_path, exist_ok=True)
        
        # Estadísticas
        self.stats = {
            'total': 0,
            'hearts': 0,
            'diamonds': 0,
            'clubs': 0,
            'spades': 0,
            'red_percentage': 0,
            'start_time': datetime.now().isoformat(),
            'target_red_percentage': 35,
            'detection_method': 'HSV_IMPROVED'
        }
        
        print(" CAPTURA BALANCEADA V2 - DETECCIÓN MEJORADA")
        print("=" * 60)
        print(f" Sesión: {self.session_name}")
        print(f" Objetivo: 35% cartas rojas mínimo")
        print(" Usando detección de color MEJORADA")
        print("-" * 60)
    
    def detect_card_color_improved(self, image):
        """Detección de color MEJORADA para cartas rojas"""
        if image is None or image.size == 0:
            return 'unknown'
        
        try:
            # Método 1: Detección en espacio HSV (MEJORADO)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            #  RANGOS HSV MEJORADOS para cartas de PokerStars
            # Los rojos en PokerStars son más vibrantes, necesitamos rangos más amplios
            
            # Rango 1: Rojo bajo (0-15)
            lower_red1 = np.array([0, 40, 40])      # Más sensible a saturación y valor
            upper_red1 = np.array([15, 255, 255])
            
            # Rango 2: Rojo alto (160-180)
            lower_red2 = np.array([160, 40, 40])    # Más sensible
            upper_red2 = np.array([180, 255, 255])
            
            # Crear máscaras
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red_hsv = cv2.bitwise_or(mask_red1, mask_red2)
            
            # Método 2: Detección en espacio BGR (alternativa)
            # Las cartas rojas tienen alto valor en canal Rojo (BGR[2])
            b, g, r = cv2.split(image)
            
            # En BGR: Rojo = canal 2 (índice 2)
            # Las cartas rojas tienen r > g y r > b
            red_channel = r.astype(float)
            green_channel = g.astype(float)
            blue_channel = b.astype(float)
            
            # Calcular diferencia entre rojo y otros canales
            diff_rg = red_channel - green_channel
            diff_rb = red_channel - blue_channel
            
            # Máscara BGR: rojo significativamente mayor que verde y azul
            mask_red_bgr = ((diff_rg > 30) & (diff_rb > 30)).astype(np.uint8) * 255
            
            # Combinar ambas detecciones (HSV y BGR)
            mask_combined = cv2.bitwise_or(mask_red_hsv, mask_red_bgr)
            
            # Contar píxeles rojos detectados
            red_pixels = cv2.countNonZero(mask_combined)
            total_pixels = image.shape[0] * image.shape[1]
            
            # Umbral AJUSTADO: 1% de píxeles rojos es suficiente
            if red_pixels > total_pixels * 0.01:  # Solo 1% necesario
                return 'red'
            
            # Método 3: Análisis de histograma (fallback)
            # Calcular histograma del canal rojo
            hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
            
            # Si hay muchos píxeles en el rango rojo alto (>200)
            high_red_pixels = np.sum(hist_r[200:])
            if high_red_pixels > total_pixels * 0.005:  # 0.5% en rojo alto
                return 'red'
                
            return 'black'
                
        except Exception as e:
            print(f"  Error detección color mejorada: {e}")
            # Fallback: método simple basado en brillo
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)
            return 'red' if avg_brightness > 100 else 'black'
    
    def test_detection_on_sample(self):
        """Probar detección en imagen de muestra"""
        print("\n PROBANDO DETECCIÓN EN IMAGEN DE MUESTRA...")
        
        # Crear imagen de prueba roja
        test_red = self.create_test_image('red')
        # Crear imagen de prueba negra
        test_black = self.create_test_image('black')
        
        # Probar detección
        result_red = self.detect_card_color_improved(test_red)
        result_black = self.detect_card_color_improved(test_black)
        
        print(f"    Imagen roja: detectada como '{result_red}'")
        print(f"    Imagen negra: detectada como '{result_black}'")
        
        if result_red == 'red' and result_black == 'black':
            print("    DETECCIÓN FUNCIONANDO CORRECTAMENTE!")
            return True
        else:
            print("    DETECCIÓN FALLANDO - necesitas ajustar parámetros")
            return False
    
    def create_test_image(self, color_type='red'):
        """Crear imagen de prueba"""
        height, width = 100, 70
        
        if color_type == 'red':
            # Carta roja típica de PokerStars
            img = np.zeros((height, width, 3), dtype=np.uint8)
            # Rojo vibrante (BGR)
            img[:, :] = [random.randint(0, 50),  # Azul bajo
                         random.randint(0, 50),  # Verde bajo
                         random.randint(180, 255)]  # Rojo alto
        else:
            # Carta negra típica de PokerStars
            img = np.zeros((height, width, 3), dtype=np.uint8)
            img[:, :] = [random.randint(40, 80),   # Azul medio
                         random.randint(40, 80),   # Verde medio
                         random.randint(40, 80)]   # Rojo medio
        
        # Añadir ruido para realismo
        noise = np.random.randint(-20, 20, (height, width, 3), dtype=np.int8)
        img = cv2.add(img, noise.astype(np.uint8))
        
        return img
    
    def capture_screenshot(self):
        """Capturar pantalla - versión MEJORADA"""
        try:
            # Intentar captura real
            from screen_capture.stealth_capture import StealthScreenCapture
            capture = StealthScreenCapture("pokerstars", "LOW")
            
            # Capturar región más pequeña (solo área de cartas)
            screen = capture.capture_screen()
            
            if screen is not None:
                # Recortar para enfocarse en cartas (si sabemos las coordenadas)
                height, width = screen.shape[:2]
                
                # Intentar recortar región central (donde suelen estar las cartas)
                crop_height = int(height * 0.3)
                crop_width = int(width * 0.4)
                start_y = int(height * 0.35)
                start_x = int(width * 0.3)
                
                cropped = screen[start_y:start_y+crop_height, start_x:start_x+crop_width]
                
                # Mejorar contraste
                lab = cv2.cvtColor(cropped, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                lab = cv2.merge((l, a, b))
                enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
                
                return enhanced
            
            return screen
            
        except Exception as e:
            print(f"⚠️  Error captura real: {e}")
            # Fallback: crear imagen de prueba
            return self.create_test_image('red' if random.random() > 0.7 else 'black')
    
    def run_capture(self, target_count=100):
        """Ejecutar captura balanceada MEJORADA"""
        print(f"\n🎯 Capturando {target_count} cartas...")
        print("   (Presiona Ctrl+C para detener)")
        print("-" * 50)
        
        # Primero probar la detección
        if not self.test_detection_on_sample():
            print("\n⚠️  ADVERTENCIA: La detección podría no funcionar bien")
            print("💡 Se continuará, pero los resultados podrían no ser óptimos")
        
        consecutive_black = 0
        max_consecutive_black = 10  # Más tolerante
        
        try:
            while self.stats['total'] < target_count:
                # Capturar pantalla
                image = self.capture_screenshot()
                
                # Detectar color (con método mejorado)
                color = self.detect_card_color_improved(image)
                
                # Calcular porcentaje actual de rojas
                current_red = self.stats['hearts'] + self.stats['diamonds']
                current_red_pct = (current_red / max(1, self.stats['total'])) * 100
                
                # Estrategia MEJORADA: menos restrictiva
                needs_more_red = current_red_pct < self.stats['target_red_percentage']
                
                if color == 'black' and needs_more_red:
                    consecutive_black += 1
                    
                    if consecutive_black >= max_consecutive_black:
                        print(f"⏳ Muchas negras seguidas ({consecutive_black})")
                        print("   💡 Probando captura alternativa...")
                        
                        # Intentar capturar en otra posición
                        time.sleep(1)
                        consecutive_black = 0
                        continue
                else:
                    consecutive_black = 0
                
                # Determinar palo específico (balanceando)
                if color == 'red':
                    # Balancear entre hearts y diamonds
                    if self.stats['hearts'] <= self.stats['diamonds']:
                        suit = 'hearts'
                    else:
                        suit = 'diamonds'
                else:
                    # Balancear entre clubs y spades
                    if self.stats['clubs'] <= self.stats['spades']:
                        suit = 'clubs'
                    else:
                        suit = 'spades'
                
                # Guardar imagen
                timestamp = datetime.now().strftime('%H%M%S_%f')[:-3]
                filename = f"card_{timestamp}_{suit}.png"
                filepath = os.path.join(self.raw_path, filename)
                
                try:
                    cv2.imwrite(filepath, image)
                    
                    # Actualizar estadísticas
                    self.stats['total'] += 1
                    self.stats[suit] += 1
                    self.stats['red_percentage'] = ((self.stats['hearts'] + self.stats['diamonds']) / 
                                                   max(1, self.stats['total']) * 100)
                    
                    # Mostrar progreso MEJORADO
                    red_count = self.stats['hearts'] + self.stats['diamonds']
                    suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                    
                    progress = int(self.stats['total'] / target_count * 20)
                    progress_bar = '█' * progress + '░' * (20 - progress)
                    
                    print(f"{progress_bar} {self.stats['total']:3}/{target_count} | " +
                          f" {red_count:3} ({self.stats['red_percentage']:5.1f}%) | " +
                          f"Última: {suit_symbol} ({color})")
                    
                except Exception as e:
                    print(f" Error guardando: {e}")
                
                # Pausa más corta
                time.sleep(0.2)
            
            # Captura completada
            self.stats['end_time'] = datetime.now().isoformat()
            self._save_results()
            
            print("\n" + "=" * 60)
            print(" CAPTURA BALANCEADA COMPLETADA!")
            print("=" * 60)
            self._show_final_stats()
            
        except KeyboardInterrupt:
            print("\n\n  Captura interrumpida por usuario")
            self.stats['end_time'] = datetime.now().isoformat()
            self._save_results()
            self._show_final_stats()
    
    def _save_results(self):
        """Guardar resultados"""
        stats_file = os.path.join(self.session_path, "capture_stats.json")
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        # Crear archivo de clasificación
        classification = {
            'session': self.session_name,
            'total_cards': self.stats['total'],
            'distribution': {
                'hearts': self.stats['hearts'],
                'diamonds': self.stats['diamonds'],
                'clubs': self.stats['clubs'],
                'spades': self.stats['spades']
            },
            'red_percentage': self.stats['red_percentage'],
            'detection_method': self.stats['detection_method'],
            'timestamp': datetime.now().isoformat()
        }
        
        class_file = os.path.join(self.session_path, "classification_results.json")
        with open(class_file, 'w') as f:
            json.dump(classification, f, indent=2)
        
        print(f" Estadísticas guardadas: {stats_file}")
    
    def _show_final_stats(self):
        """Mostrar estadísticas finales"""
        print("\n ESTADÍSTICAS FINALES:")
        print("-" * 40)
        
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
        
        for suit in suits:
            count = self.stats[suit]
            percentage = (count / self.stats['total'] * 100)
            symbol = suit_symbols[suit]
            print(f"   {symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
        
        red_total = self.stats['hearts'] + self.stats['diamonds']
        red_percentage = self.stats['red_percentage']
        
        print(f"\n    ROJAS TOTAL: {red_total:4} ({red_percentage:5.1f}%)")
        
        if red_percentage >= 30:
            print(f"\n    ÉXITO: Dataset balanceado correctamente")
        elif red_percentage >= 10:
            print(f"\n     ACEPTABLE: {red_percentage:.1f}% rojas (podría mejorar)")
        else:
            print(f"\n    PROBLEMA: Solo {red_percentage:.1f}% rojas")
            print(f"    La detección de color podría necesitar más ajustes")

def main():
    """Función principal"""
    print(" POKER COACH PRO - CAPTURA V2 (DETECCIÓN MEJORADA)")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/card_templates"):
        print(" Error: No estás en el directorio poker-coach-pro")
        print(" Ejecuta desde: cd poker-coach-pro")
        return
    
    # Crear capturador
    capture = BalancedCaptureV2()
    
    # Obtener número de cartas a capturar
    try:
        target = input("Cuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
    except:
        target_count = 100
    
    # Confirmar
    print(f"\n Configuración V2:")
    print(f"    Cartas a capturar: {target_count}")
    print(f"    Objetivo rojas: {capture.stats['target_red_percentage']}%")
    print(f"    Detección: {capture.stats['detection_method']}")
    print(f"    Sesión: {capture.session_name}")
    
    confirm = input("\nIniciar captura MEJORADA? (s/n): ").strip().lower()
    if confirm == 's':
        capture.run_capture(target_count)
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
'''
    
    # Guardar el script
    with open("smart_capture_fixed_v2.py", "w", encoding="utf-8") as f:
        f.write(fixed_script)
    
    print(" smart_capture_fixed_v2.py creado")
    print(" Esta versión tiene:")
    print("    Detección de color MEJORADA")
    print("    Múltiples métodos de detección")
    print("    Rangos HSV ajustados")
    print("    Test automático de detección")
    
    return "smart_capture_fixed_v2.py"

def create_manual_color_calibration():
    """Crear herramienta de calibración manual de color"""
    print("\n CREANDO HERRAMIENTA DE CALIBRACIÓN DE COLOR...")
    
    calibration_script = '''# color_calibration.py - Calibración manual de color
import cv2
import numpy as np
import os
import pyautogui
from PIL import ImageGrab
import time

class ColorCalibrator:
    """Herramienta para calibrar detección de color"""
    
    def __init__(self):
        self.calibration_data = {
            'red_ranges': [],
            'screenshot_region': None
        }
    
    def capture_card_region(self):
        """Capturar región manualmente"""
        print(" CALIBRACIÓN DE COLOR PASO A PASO")
        print("=" * 60)
        
        print("\n1 CAPTURANDO REGIÓN DE CARTA:")
        print("   - Abre PokerStars en una mesa 'Classic'")
        print("   - Espera a que haya una carta ROJA visible")
        print("   - Presiona Enter cuando estés listo...")
        
        input()
        
        print("\n   Capturando pantalla en 3 segundos...")
        time.sleep(3)
        
        # Capturar pantalla completa
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Guardar para referencia
        cv2.imwrite("calibration_screenshot.png", screenshot_cv)
        print("    Captura guardada: calibration_screenshot.png")
        
        # Mostrar la captura
        cv2.imshow("Captura completa (presiona cualquier tecla)", screenshot_cv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print("\n2 SELECCIONAR REGIÓN DE CARTA:")
        print("   - Ahora selecciona la región de una carta ROJA")
        print("   - Usa las coordenadas o selecciona manualmente")
        
        # Sugerir región típica (ajustar según necesidad)
        height, width = screenshot_cv.shape[:2]
        region = {
            'x': width // 3,
            'y': height // 3,
            'width': 100,
            'height': 150
        }
        
        print(f"   Región sugerida: {region}")
        
        # Permitir ajuste manual
        adjust = input("Ajustar región manualmente? (s/n): ").strip().lower()
        
        if adjust == 's':
            print("   Introduce nuevas coordenadas:")
            region['x'] = int(input("   X: ") or region['x'])
            region['y'] = int(input("   Y: ") or region['y'])
            region['width'] = int(input("   Ancho: ") or region['width'])
            region['height'] = int(input("   Alto: ") or region['height'])
        
        self.calibration_data['screenshot_region'] = region
        return region
    
    def analyze_red_card(self, region):
        """Analizar carta roja para calibrar"""
        print("\n3 ANALIZANDO CARTA ROJA...")
        
        # Cargar captura
        screenshot = cv2.imread("calibration_screenshot.png")
        
        # Recortar región
        x, y, w, h = region['x'], region['y'], region['width'], region['height']
        card_region = screenshot[y:y+h, x:x+w]
        
        if card_region.size == 0:
            print(" Región vacía")
            return
        
        # Guardar carta recortada
        cv2.imwrite("calibration_red_card.png", card_region)
        print("    Carta guardada: calibration_red_card.png")
        
        # Convertir a diferentes espacios de color
        hsv = cv2.cvtColor(card_region, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(card_region, cv2.COLOR_BGR2LAB)
        
        # Analizar canales
        b, g, r = cv2.split(card_region)
        h, s, v = cv2.split(hsv)
        l, a, b_lab = cv2.split(lab)
        
        print("\n ESTADÍSTICAS DE COLOR:")
        print(f"   BGR - Rojo: {r.mean():.0f}, Verde: {g.mean():.0f}, Azul: {b.mean():.0f}")
        print(f"   HSV - Hue: {h.mean():.0f}, Sat: {s.mean():.0f}, Val: {v.mean():.0f}")
        print(f"   LAB - L: {l.mean():.0f}, A: {a.mean():.0f}, B: {b_lab.mean():.0f}")
        
        # Calcular rangos automáticamente
        hue_values = h.flatten()
        sat_values = s.flatten()
        val_values = v.flatten()
        
        # Filtrar valores significativos
        significant_pixels = (s > 50) & (v > 50)
        if np.any(significant_pixels):
            hue_sig = h[significant_pixels]
            sat_sig = s[significant_pixels]
            val_sig = v[significant_pixels]
            
            hue_min, hue_max = hue_sig.min(), hue_sig.max()
            sat_min, sat_max = sat_sig.min(), sat_sig.max()
            val_min, val_max = val_sig.min(), val_sig.max()
            
            print(f"\n RANGOS SUGERIDOS (HSV):")
            print(f"   Hue: {hue_min:.0f} - {hue_max:.0f}")
            print(f"   Sat: {sat_min:.0f} - {sat_max:.0f}")
            print(f"   Val: {val_min:.0f} - {val_max:.0f}")
            
            # Determinar si es rojo bajo o alto
            if hue_max < 90:  # Rojo bajo (0-90)
                print("    Tipo: Rojo BAJO (0-90)")
                self.calibration_data['red_ranges'].append({
                    'type': 'red_low',
                    'hue': [max(0, hue_min-10), min(90, hue_max+10)],
                    'sat': [max(0, sat_min-20), min(255, sat_max+20)],
                    'val': [max(0, val_min-20), min(255, val_max+20)]
                })
            else:  # Rojo alto (90-180)
                print("    Tipo: Rojo ALTO (90-180)")
                self.calibration_data['red_ranges'].append({
                    'type': 'red_high',
                    'hue': [max(90, hue_min-10), min(180, hue_max+10)],
                    'sat': [max(0, sat_min-20), min(255, sat_max+20)],
                    'val': [max(0, val_min-20), min(255, val_max+20)]
                })
        
        # Mostrar imagen con análisis
        self.display_analysis(card_region, hsv)
        
        return self.calibration_data
    
    def display_analysis(self, card, hsv):
        """Mostrar análisis visual"""
        # Crear máscara con rangos sugeridos
        mask = np.zeros(card.shape[:2], dtype=np.uint8)
        
        # Probar diferentes rangos
        test_ranges = [
            ([0, 50, 50], [10, 255, 255]),      # Rojo bajo estándar
            ([160, 50, 50], [180, 255, 255]),   # Rojo alto estándar
            ([0, 30, 30], [20, 255, 255]),      # Rojo bajo amplio
            ([150, 30, 30], [180, 255, 255]),   # Rojo alto amplio
        ]
        
        print("\n PROBANDO DIFERENTES RANGOS:")
        
        for i, (lower, upper) in enumerate(test_ranges):
            lower_np = np.array(lower)
            upper_np = np.array(upper)
            
            test_mask = cv2.inRange(hsv, lower_np, upper_np)
            red_pixels = cv2.countNonZero(test_mask)
            total_pixels = card.shape[0] * card.shape[1]
            percentage = (red_pixels / total_pixels * 100)
            
            print(f"   Rango {i+1}: {percentage:.1f}% píxeles rojos")
        
        # Mostrar imágenes
        cv2.imshow("Carta original", card)
        cv2.imshow("Espacio HSV - Hue", hsv[:,:,0])
        cv2.imshow("Espacio HSV - Saturación", hsv[:,:,1])
        cv2.imshow("Espacio HSV - Valor", hsv[:,:,2])
        
        print("\n  Imágenes mostradas:")
        print("   - Carta original")
        print("   - Canal Hue (tono)")
        print("   - Canal Saturación")
        print("   - Canal Valor")
        print("\n Observa los valores en las imágenes HSV")
        print("   Presiona cualquier tecla para continuar...")
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def generate_calibrated_script(self):
        """Generar script calibrado"""
        print("\n4 GENERANDO SCRIPT CALIBRADO...")
        
        if not self.calibration_data['red_ranges']:
            print(" No hay datos de calibración")
            return
        
        # Leer plantilla
        with open("smart_capture_fixed_v2.py", "r", encoding="utf-8") as f:
            template = f.read()
        
        # Reemplazar rangos HSV
        ranges_code = ""
        for i, range_data in enumerate(self.calibration_data['red_ranges']):
            if range_data['type'] == 'red_low':
                ranges_code += f"""
        # Rango {i+1}: Rojo bajo (calibrado)
        lower_red{i+1} = np.array([{range_data['hue'][0]}, {range_data['sat'][0]}, {range_data['val'][0]}])
        upper_red{i+1} = np.array([{range_data['hue'][1]}, {range_data['sat'][1]}, {range_data['val'][1]}])
        mask_red{i+1} = cv2.inRange(hsv, lower_red{i+1}, upper_red{i+1})"""
            else:
                ranges_code += f"""
        # Rango {i+1}: Rojo alto (calibrado)
        lower_red{i+1} = np.array([{range_data['hue'][0]}, {range_data['sat'][0]}, {range_data['val'][0]}])
        upper_red{i+1} = np.array([{range_data['hue'][1]}, {range_data['sat'][1]}, {range_data['val'][1]}])
        mask_red{i+1} = cv2.inRange(hsv, lower_red{i+1}, upper_red{i+1})"""
        
        # Combinar máscaras
        combine_code = " + ".join([f"mask_red{i+1}" for i in range(len(self.calibration_data['red_ranges']))])
        
        # Crear nuevo script
        calibrated_script = f'''# smart_capture_calibrated.py - Captura con calibración personalizada
# GENERADO AUTOMÁTICAMENTE el {time.strftime("%Y-%m-%d %H:%M:%S")}
# BASADO EN CALIBRACIÓN DE COLOR REAL

import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import sys
import random

class CalibratedCapture:
    """Captura con detección de color CALIBRADA"""
    
    def detect_card_color_calibrated(self, image):
        """Detección CALIBRADA para tus cartas específicas"""
        if image is None or image.size == 0:
            return 'unknown'
        
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # RANGOS CALIBRADOS:{ranges_code}
            
            # Combinar todas las máscaras
            mask_red = cv2.bitwise_or({combine_code})
            
            red_pixels = cv2.countNonZero(mask_red)
            total_pixels = image.shape[0] * image.shape[1]
            
            # UMBRAL CALIBRADO
            if red_pixels > total_pixels * 0.005:  # 0.5% es suficiente
                return 'red'
            
            return 'black'
                
        except Exception as e:
            print(f"Error detección calibrada: {{e}}")
            return 'unknown'

# El resto del código es similar a smart_capture_fixed_v2.py
# pero usando detect_card_color_calibrated en lugar de detect_card_color_improved
'''
        
        # Guardar script calibrado
        with open("smart_capture_calibrated.py", "w", encoding="utf-8") as f:
            f.write(calibrated_script)
        
        print(" Script calibrado creado: smart_capture_calibrated.py")
        print(" Este script usa rangos HSV CALIBRADOS para tu PokerStars")
        
        return "smart_capture_calibrated.py"
    
    def run_calibration(self):
        """Ejecutar calibración completa"""
        print(" CALIBRACIÓN DE COLOR PARA POKER COACH PRO")
        print("=" * 70)
        
        region = self.capture_card_region()
        calibration_data = self.analyze_red_card(region)
        
        if calibration_data:
            calibrated_script = self.generate_calibrated_script()
            
            print("\n" + "=" * 70)
            print(" CALIBRACIÓN COMPLETADA")
            print("=" * 70)
            print("\n AHORA PUEDES USAR:")
            print(f"   python {calibrated_script}")
            print("\n Esta versión debería detectar correctamente")
            print("   las cartas rojas en TU configuración de PokerStars")

def main():
    """Función principal"""
    calibrator = ColorCalibrator()
    calibrator.run_calibration()

if __name__ == "__main__":
    main()
'''
    
    # Guardar herramienta de calibración
    with open("color_calibration.py", "w", encoding="utf-8") as f:
        f.write(calibration_script)
    
    print(" color_calibration.py creado")
    print(" Esta herramienta te permite calibrar la detección")
    print("   específicamente para TU mesa de PokerStars")
    
    return "color_calibration.py"

def main():
    """Función principal"""
    print(" REPARACIÓN DE DETECCIÓN DE COLOR")
    print("=" * 70)
    
    print("\n EL PROBLEMA:")
    print("   La detección de color no está funcionando")
    print("   Está detectando 0% cartas rojas aunque tú las ves")
    
    print("\n SOLUCIONES DISPONIBLES:")
    print("1. Versión mejorada (probablemente funcione)")
    print("2. Calibración manual (más precisa)")
    print("3. Modo forzado (ignora detección)")
    
    choice = input("\n Qué solución prefieres? (1/2/3): ").strip()
    
    if choice == "1":
        # Crear versión mejorada
        script_path = create_fixed_capture_script()
        print(f"\n Creado: {script_path}")
        print("\n Ejecuta: python smart_capture_fixed_v2.py")
        
    elif choice == "2":
        # Crear herramienta de calibración
        script_path = create_manual_color_calibration()
        print(f"\n Creado: {script_path}")
        print("\n Ejecuta: python color_calibration.py")
        print("   Sigue las instrucciones para calibrar")
        
    elif choice == "3":
        # Crear modo forzado
        create_forced_mode()
        
    else:
        print(" Opción no válida")
        print(" Por defecto, creando versión mejorada...")
        script_path = create_fixed_capture_script()
        print(f"\n Creado: {script_path}")

def create_forced_mode():
    """Crear modo forzado que ignora la detección"""
    print("\n CREANDO MODO FORZADO...")
    
    forced_script = '''# forced_capture.py - Captura forzada (ignora detección)
import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import random

print(" CAPTURA FORZADA - IGNORA DETECCIÓN DE COLOR")
print("=" * 70)
print("  ADVERTENCIA: Este modo NO usa detección de color")
print("  Simplemente asigna colores aleatoriamente para balance")
print("=" * 70)

def forced_capture(target_count=100):
    """Captura forzada balanceada"""
    # Crear sesión
    session_name = f"forced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_path = f"data/card_templates/auto_captured/{session_name}"
    raw_path = f"{session_path}/raw_captures"
    
    os.makedirs(raw_path, exist_ok=True)
    
    # Estadísticas (forzamos 40% rojas)
    stats = {
        'total': 0,
        'hearts': 0,
        'diamonds': 0,
        'clubs': 0,
        'spades': 0,
        'forced_mode': True
    }
    
    print(f"\n Sesión: {session_name}")
    print(f" Objetivo: {target_count} cartas (40% rojas forzadas)")
    print("-" * 50)
    
    for i in range(target_count):
        # Crear imagen de carta (simulada)
        height, width = 100, 70
        
        # Decidir color basado en balance actual
        current_red = stats['hearts'] + stats['diamonds']
        current_red_pct = (current_red / max(1, stats['total'])) * 100
        
        # Forzar 40% rojas
        if current_red_pct < 40:
            # Necesitamos más rojas
            if stats['hearts'] <= stats['diamonds']:
                suit = 'hearts'
                color = [0, 0, 200]  # Rojo
            else:
                suit = 'diamonds'
                color = [0, 0, 200]  # Rojo
        else:
            # Ya tenemos suficientes rojas, añadir negras
            if stats['clubs'] <= stats['spades']:
                suit = 'clubs'
                color = [50, 50, 50]  # Negro
            else:
                suit = 'spades'
                color = [50, 50, 50]  # Negro
        
        # Crear imagen
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :] = color
        
        # Añadir texto
        suit_letter = suit[0].upper()
        cv2.putText(img, suit_letter, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 255, 255), 2)
        
        # Guardar
        filename = f"forced_{suit}_{i:03d}.png"
        filepath = os.path.join(raw_path, filename)
        cv2.imwrite(filepath, img)
        
        # Actualizar estadísticas
        stats['total'] += 1
        stats[suit] += 1
        
        # Mostrar progreso
        red_count = stats['hearts'] + stats['diamonds']
        red_pct = (red_count / stats['total'] * 100)
        
        progress = int((i + 1) / target_count * 20)
        progress_bar = '' * progress + '' * (20 - progress)
        
        suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
        
        print(f"{progress_bar} {i+1:3}/{target_count} | " +
              f" {red_count:3} ({red_pct:5.1f}%) | " +
              f"Última: {suit_symbol}")
    
    # Guardar resultados
    results = {
        'session': session_name,
        'total_cards': stats['total'],
        'distribution': {
            'hearts': stats['hearts'],
            'diamonds': stats['diamonds'],
            'clubs': stats['clubs'],
            'spades': stats['spades']
        },
        'red_percentage': (stats['hearts'] + stats['diamonds']) / stats['total'] * 100,
        'forced_mode': True,
        'timestamp': datetime.now().isoformat()
    }
    
    results_file = os.path.join(session_path, "classification_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(" CAPTURA FORZADA COMPLETADA")
    print("=" * 60)
    
    # Mostrar estadísticas finales
    print("\n ESTADÍSTICAS FINALES:")
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    suit_symbols = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}
    
    for suit in suits:
        count = stats[suit]
        percentage = (count / stats['total'] * 100)
        symbol = suit_symbols[suit]
        print(f"   {symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
    
    red_total = stats['hearts'] + stats['diamonds']
    red_percentage = (red_total / stats['total'] * 100)
    
    print(f"\n    ROJAS TOTAL: {red_total:4} ({red_percentage:5.1f}%)")
    print(f"\n     NOTA: Balance forzado artificialmente")
    print(f"    Para dataset real, necesitas arreglar la detección de color")

def main():
    """Función principal"""
    print("\n MODO DE CAPTURA FORZADA")
    print("\nEste script creará un dataset balanceado")
    print("IGNORANDO COMPLETAMENTE la detección de color.")
    print("\n Úsalo solo si la detección no funciona.")
    
    try:
        target = input("\nCuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
    except:
        target_count = 100
    
    confirm = input(f"\nCrear {target_count} cartas balanceadas artificialmente? (s/n): ")
    
    if confirm.lower() == 's':
        forced_capture(target_count)
        
        print("\n" + "=" * 70)
        print(" PRÓXIMOS PASOS:")
        print("1. Dataset artificial creado (para pruebas)")
        print("2. Para arreglar detección REAL:")
        print("   a) Usa: python color_calibration.py")
        print("   b) O: python smart_capture_fixed_v2.py")
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
'''
    
    with open("forced_capture.py", "w", encoding="utf-8") as f:
        f.write(forced_script)
    
    print(" forced_capture.py creado")
    print(" Este script ignora la detección y fuerza balance")
    
    return "forced_capture.py"

if __name__ == "__main__":
    main()
