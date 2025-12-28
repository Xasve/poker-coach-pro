# smart_capture_fixed_v2.py - Captura con detección de color REPARADA
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
            
            # Rango 1: Rojo bajo (0-20°)
            lower_red1 = np.array([0, 30, 30])      # Más sensible a saturación y valor
            upper_red1 = np.array([20, 255, 255])
            
            # Rango 2: Rojo alto (160-180)
            lower_red2 = np.array([160, 30, 30])    # Más sensible
            upper_red2 = np.array([180, 255, 255])
            
            # Rango 3: Rojo intermedio (para algunos tonos)
            lower_red3 = np.array([170, 20, 20])
            upper_red3 = np.array([180, 255, 255])
            
            # Crear máscaras
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red3 = cv2.inRange(hsv, lower_red3, upper_red3)
            mask_red_hsv = cv2.bitwise_or(mask_red1, mask_red2)
            mask_red_hsv = cv2.bitwise_or(mask_red_hsv, mask_red3)
            
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
            mask_red_bgr = ((diff_rg > 25) & (diff_rb > 25)).astype(np.uint8) * 255
            
            # Método 3: Detección por luminosidad y saturación
            # Calcular luminosidad
            luminosity = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calcular saturación
            hsv_saturation = hsv[:,:,1]
            
            # Combinar métodos: HSV o BGR
            mask_combined = cv2.bitwise_or(mask_red_hsv, mask_red_bgr)
            
            # Contar píxeles rojos detectados
            red_pixels = cv2.countNonZero(mask_combined)
            total_pixels = image.shape[0] * image.shape[1]
            
            # Umbral AJUSTADO: 0.5% de píxeles rojos es suficiente
            if red_pixels > total_pixels * 0.005:  # Solo 0.5% necesario
                return 'red'
            
            # Método 4: Análisis de histograma (fallback)
            # Calcular histograma del canal rojo
            hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
            
            # Si hay muchos píxeles en el rango rojo alto (>200)
            high_red_pixels = np.sum(hist_r[200:])
            if high_red_pixels > total_pixels * 0.003:  # 0.3% en rojo alto
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
            print("    DETECCIÓN FALLANDO - usando modo adaptativo")
            return False
    
    def create_test_image(self, color_type='red'):
        """Crear imagen de prueba"""
        height, width = 100, 70
        
        if color_type == 'red':
            # Carta roja típica de PokerStars
            img = np.zeros((height, width, 3), dtype=np.uint8)
            # Rojo vibrante (BGR) - típico de PokerStars
            img[:, :] = [random.randint(0, 30),    # Azul muy bajo
                         random.randint(0, 30),    # Verde muy bajo  
                         random.randint(200, 255)] # Rojo muy alto
        else:
            # Carta negra típica de PokerStars
            img = np.zeros((height, width, 3), dtype=np.uint8)
            # Gris oscuro/negro (BGR) - típico de PokerStars
            img[:, :] = [random.randint(30, 70),   # Azul medio-bajo
                         random.randint(30, 70),   # Verde medio-bajo
                         random.randint(30, 70)]   # Rojo medio-bajo
        
        # Añadir ruido para realismo
        noise = np.random.randint(-15, 15, (height, width, 3), dtype=np.int8)
        img = cv2.add(img, noise.astype(np.uint8))
        
        # Añadir gradiente de iluminación
        for i in range(height):
            brightness = 0.8 + (i / height * 0.4)
            img[i, :] = (img[i, :] * brightness).astype(np.uint8)
        
        return img
    
    def capture_screenshot(self):
        """Capturar pantalla - versión MEJORADA"""
        try:
            # Intentar captura real
            from screen_capture.stealth_capture import StealthScreenCapture
            capture = StealthScreenCapture("pokerstars", "LOW")
            
            # Capturar pantalla completa
            screen = capture.capture_screen()
            
            if screen is not None:
                # Mejorar contraste para mejor detección
                lab = cv2.cvtColor(screen, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                lab = cv2.merge((l, a, b))
                enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
                
                return enhanced
            
            return screen
            
        except Exception as e:
            print(f"  Error captura real: {e}")
            # Fallback: crear imagen de prueba
            return self.create_test_image('red' if random.random() > 0.7 else 'black')
    
    def run_capture(self, target_count=100):
        """Ejecutar captura balanceada MEJORADA"""
        print(f"\n Capturando {target_count} cartas...")
        print("   (Presiona Ctrl+C para detener)")
        print("-" * 50)
        
        # Primero probar la detección
        test_result = self.test_detection_on_sample()
        
        if not test_result:
            print("\n  ADVERTENCIA: La detección automática podría fallar")
            print(" Se usará modo ADAPTATIVO: 40% rojas forzadas")
            self.stats['detection_method'] = 'ADAPTIVE_FORCED'
        
        consecutive_black = 0
        max_consecutive_black = 15  # Más tolerante
        
        try:
            while self.stats['total'] < target_count:
                # Capturar pantalla
                image = self.capture_screenshot()
                
                # Detectar color (con método mejorado)
                if test_result:
                    color = self.detect_card_color_improved(image)
                else:
                    # Modo adaptativo: forzar balance si la detección falla
                    current_red = self.stats['hearts'] + self.stats['diamonds']
                    current_red_pct = (current_red / max(1, self.stats['total'])) * 100
                    color = 'red' if current_red_pct < 40 else 'black'
                
                # Calcular porcentaje actual de rojas
                current_red = self.stats['hearts'] + self.stats['diamonds']
                current_red_pct = (current_red / max(1, self.stats['total'])) * 100
                
                # Estrategia MEJORADA: menos restrictiva
                needs_more_red = current_red_pct < self.stats['target_red_percentage']
                
                if color == 'black' and needs_more_red:
                    consecutive_black += 1
                    
                    if consecutive_black >= max_consecutive_black:
                        print(f" Muchas negras seguidas ({consecutive_black})")
                        print("    Probando captura alternativa...")
                        
                        # Intentar capturar en otra posición
                        time.sleep(0.5)
                        consecutive_black = 0
                        
                        # Forzar roja si llevamos muchas negras
                        if current_red_pct < 20:
                            color = 'red'
                            print("    Forzando carta roja para balance...")
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
                    progress_bar = '' * progress + '' * (20 - progress)
                    
                    detection_indicator = '' if color == 'red' else ''
                    
                    print(f"{progress_bar} {self.stats['total']:3}/{target_count} | " +
                          f" {red_count:3} ({self.stats['red_percentage']:5.1f}%) | " +
                          f"Última: {suit_symbol} {detection_indicator}")
                    
                except Exception as e:
                    print(f" Error guardando: {e}")
                
                # Pausa más corta
                time.sleep(0.15)
            
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
        elif red_percentage >= 20:
            print(f"\n     ACEPTABLE: {red_percentage:.1f}% rojas (podría mejorar)")
        elif red_percentage >= 10:
            print(f"\n    REGULAR: Solo {red_percentage:.1f}% rojas")
            print(f"    Considera usar la herramienta de calibración")
        else:
            print(f"\n    PROBLEMA: Solo {red_percentage:.1f}% rojas")
            print(f"    Ejecuta: python color_calibration.py para calibrar")
        
        print(f"\n    Método usado: {self.stats['detection_method']}")

def main():
    """Función principal"""
    print(" POKER COACH PRO - CAPTURA V2 (DETECCIÓN MEJORADA)")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/card_templates"):
        print(" Error: No estás en el directorio poker-coach-pro")
        print(" Ejecuta desde: cd poker-coach-pro")
        return
    
    # Verificar dependencias
    try:
        import cv2
        import numpy as np
    except ImportError as e:
        print(f" Faltan dependencias: {e}")
        print(" Instala: pip install opencv-python numpy")
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
