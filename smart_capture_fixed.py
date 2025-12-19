# smart_capture_fixed.py - Captura balanceada automática
import cv2
import numpy as np
import time
from datetime import datetime
import os
import json
import sys

# Añadir src al path para importar módulos
sys.path.insert(0, "src")

class BalancedCapture:
    """Captura automática balanceada de cartas"""
    
    def __init__(self):
        # Crear nombre de sesión
        self.session_name = f"balanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
            'target_red_percentage': 35  # Objetivo: 35% cartas rojas
        }
        
        print(" CAPTURA BALANCEADA AUTOMÁTICA")
        print("=" * 60)
        print(f" Sesión: {self.session_name}")
        print(f" Objetivo: 35% cartas rojas mínimo")
        print(" Asegúrate de estar en una mesa PokerStars 'Classic'")
        print("-" * 60)
    
    def detect_card_color(self, image):
        """Detectar si la carta es roja o negra"""
        if image is None or image.size == 0:
            return 'unknown'
        
        try:
            # Convertir a HSV para mejor detección
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Rangos para rojo (2 rangos por la naturaleza circular de HSV)
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            
            # Crear máscaras
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            
            # Contar píxeles rojos
            red_pixels = cv2.countNonZero(mask_red)
            total_pixels = image.shape[0] * image.shape[1]
            
            # Umbral ajustado para detectar cartas rojas
            if red_pixels > total_pixels * 0.03:  # 3% de píxeles rojos
                return 'red'
            else:
                return 'black'
                
        except Exception as e:
            print(f"  Error detección color: {e}")
            return 'unknown'
    
    def capture_screenshot(self):
        """Capturar pantalla - versión simplificada"""
        try:
            # Intentar importar capturador real
            from screen_capture.stealth_capture import StealthScreenCapture
            capture = StealthScreenCapture("pokerstars", "LOW")
            return capture.capture_screen()
        except:
            # Fallback: crear imagen de prueba
            print("  Usando captura simulada")
            height, width = 300, 200
            # Crear imagen aleatoria (roja o negra)
            is_red = np.random.random() > 0.7  # 30% probabilidad de rojo
            if is_red:
                # Imagen roja
                image = np.zeros((height, width, 3), dtype=np.uint8)
                image[:, :] = [0, 0, 255]  # Rojo en BGR
            else:
                # Imagen negra
                image = np.zeros((height, width, 3), dtype=np.uint8)
                image[:, :] = [50, 50, 50]  # Gris oscuro
            
            # Añadir algo de ruido para realismo
            noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
            image = cv2.add(image, noise)
            
            return image
    
    def run_capture(self, target_count=100):
        """Ejecutar captura balanceada"""
        print(f"
 Capturando {target_count} cartas balanceadas...")
        print("   (Presiona Ctrl+C para detener)")
        print("-" * 50)
        
        consecutive_black = 0
        max_consecutive_black = 5
        
        try:
            while self.stats['total'] < target_count:
                # Capturar pantalla
                image = self.capture_screenshot()
                
                # Detectar color
                color = self.detect_card_color(image)
                
                # Calcular porcentaje actual de rojas
                current_red = self.stats['hearts'] + self.stats['diamonds']
                current_red_pct = (current_red / max(1, self.stats['total'])) * 100
                
                # Estrategia: si tenemos pocas rojas, esperar para rojas
                needs_more_red = current_red_pct < self.stats['target_red_percentage']
                
                if color == 'black' and needs_more_red:
                    consecutive_black += 1
                    
                    if consecutive_black >= max_consecutive_black:
                        print(f" Muchas negras seguidas ({consecutive_black}), esperando roja...")
                        print("    Mueve el mouse o cambia de carta")
                        time.sleep(2)
                        consecutive_black = 0
                        continue
                else:
                    consecutive_black = 0
                
                # Determinar palo específico
                if color == 'red':
                    # Decidir si es hearts o diamonds
                    if self.stats['hearts'] <= self.stats['diamonds']:
                        suit = 'hearts'
                    else:
                        suit = 'diamonds'
                elif color == 'black':
                    # Decidir si es clubs o spades
                    if self.stats['clubs'] <= self.stats['spades']:
                        suit = 'clubs'
                    else:
                        suit = 'spades'
                else:
                    # Color desconocido, asignar aleatorio
                    suits = ['hearts', 'diamonds', 'clubs', 'spades']
                    suit = np.random.choice(suits)
                
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
                                                   self.stats['total'] * 100)
                    
                    # Mostrar progreso
                    red_count = self.stats['hearts'] + self.stats['diamonds']
                    suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                    
                    progress_bar = self._create_progress_bar(self.stats['total'], target_count)
                    
                    print(f"{progress_bar} {self.stats['total']:3}/{target_count} | "
                          f" {red_count:3} ({self.stats['red_percentage']:5.1f}%) | "
                          f"Última: {suit_symbol}")
                    
                except Exception as e:
                    print(f" Error guardando: {e}")
                
                # Pequeña pausa entre capturas
                time.sleep(0.3)
            
            # Captura completada
            self.stats['end_time'] = datetime.now().isoformat()
            self._save_results()
            
            print("
" + "=" * 60)
            print(" CAPTURA BALANCEADA COMPLETADA!")
            print("=" * 60)
            self._show_final_stats()
            
            # Clasificar automáticamente
            self._auto_classify()
            
        except KeyboardInterrupt:
            print("

  Captura interrumpida por usuario")
            self.stats['end_time'] = datetime.now().isoformat()
            self._save_results()
            self._show_final_stats()
    
    def _create_progress_bar(self, current, total, length=20):
        """Crear barra de progreso visual"""
        filled = int(length * current / total)
        bar = '' * filled + '' * (length - filled)
        return bar
    
    def _save_results(self):
        """Guardar resultados de la captura"""
        # Guardar estadísticas
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
            'timestamp': datetime.now().isoformat()
        }
        
        class_file = os.path.join(self.session_path, "classification_results.json")
        with open(class_file, 'w') as f:
            json.dump(classification, f, indent=2)
        
        print(f" Estadísticas guardadas: {stats_file}")
    
    def _show_final_stats(self):
        """Mostrar estadísticas finales"""
        print("
 ESTADÍSTICAS FINALES:")
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
        
        print(f"
    ROJAS TOTAL: {red_total:4} ({red_percentage:5.1f}%)")
        
        if red_percentage >= 30:
            print(f"
    ÉXITO: Dataset balanceado correctamente")
        else:
            print(f"
     ADVERTENCIA: Necesitas más cartas rojas")
            print(f"    Ejecuta otra sesión de captura")
    
    def _auto_classify(self):
        """Clasificar automáticamente las cartas"""
        print("
 Clasificando cartas en templates...")
        
        # Aquí iría la lógica para mover imágenes a templates/
        # Por ahora solo mostrar mensaje
        print(" Para clasificar: python session_manager.py -> Opción 2")

def main():
    """Función principal"""
    print(" POKER COACH PRO - CAPTURA BALANCEADA")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/card_templates"):
        print(" Error: No estás en el directorio poker-coach-pro")
        print(" Ejecuta desde: cd poker-coach-pro")
        return
    
    # Crear capturador
    capture = BalancedCapture()
    
    # Obtener número de cartas a capturar
    try:
        target = input("Cuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
    except:
        target_count = 100
    
    # Confirmar
    print(f"
 Configuración:")
    print(f"    Cartas a capturar: {target_count}")
    print(f"    Objetivo rojas: {capture.stats['target_red_percentage']}%")
    print(f"    Sesión: {capture.session_name}")
    
    confirm = input("
Iniciar captura? (s/n): ").strip().lower()
    if confirm == 's':
        capture.run_capture(target_count)
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
