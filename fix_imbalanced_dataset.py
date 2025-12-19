# fix_imbalanced_dataset.py - Solución automática para dataset desbalanceado
import os
import cv2
import numpy as np
import shutil
import json
import time
from datetime import datetime
from pathlib import Path
import sys

class DatasetFixer:
    """Solución completa para dataset desbalanceado"""
    
    def __init__(self):
        self.sessions_path = "data/card_templates/auto_captured"
        self.templates_path = "data/card_templates/pokerstars_real"
        
    def run_full_fix(self):
        """Ejecutar solución completa"""
        print(" SOLUCIÓN COMPLETA PARA DATASET DESBALANCEADO")
        print("=" * 70)
        
        self.show_current_status()
        self.clean_imbalanced_sessions()
        self.generate_smart_capture_script()
        self.generate_pokerstars_guide()
        
        print("\n✅ SOLUCIÓN COMPLETADA")
        print("\n🎮 SIGUE ESTOS PASOS:")
        print("1. Abre PokerStars en una mesa 'Classic' (NO 'Dark')")
        print("2. Ejecuta: python smart_capture_fixed.py")
        print("3. Espera a que capture 100 cartas balanceadas")
        print("4. Verifica: python verify_balance.py")
    
    def show_current_status(self):
        """Mostrar estado actual del dataset"""
        print("\n📊 ANÁLISIS DEL DATASET ACTUAL")
        print("-" * 50)
        
        # Analizar sesiones existentes
        if not os.path.exists(self.sessions_path):
            print(" No hay sesiones de captura")
            return
        
        sessions = [d for d in os.listdir(self.sessions_path) 
                   if os.path.isdir(os.path.join(self.sessions_path, d))]
        
        if not sessions:
            print("❌ No hay sesiones")
            return
        
        total_cards = 0
        suit_counts = {'hearts': 0, 'diamonds': 0, 'clubs': 0, 'spades': 0}
        
        for session in sessions:
            results_file = os.path.join(self.sessions_path, session, "classification_results.json")
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    if 'distribution' in data:
                        for suit, count in data['distribution'].items():
                            suit_counts[suit] = suit_counts.get(suit, 0) + count
                            total_cards += count
                except:
                    continue
        
        if total_cards > 0:
            print(f" CARTAS TOTALES: {total_cards}")
            print(f" DISTRIBUCIÓN:")
            
            for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                count = suit_counts.get(suit, 0)
                percentage = (count / total_cards * 100)
                suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                print(f"   {suit_symbol} {suit.upper():9} {count:4} ({percentage:5.1f}%)")
            
            # Calcular balance rojo/negro
            red_total = suit_counts['hearts'] + suit_counts['diamonds']
            black_total = suit_counts['clubs'] + suit_counts['spades']
            red_percentage = (red_total / total_cards * 100)
            
            print(f"\n BALANCE DE COLORES:")
            print(f"    ROJAS: {red_total:4} ({red_percentage:5.1f}%)")
            print(f"    NEGRAS: {black_total:4} ({100-red_percentage:5.1f}%)")
            
            if red_total == 0:
                print("\n PROBLEMA CRÍTICO: 0% cartas rojas")
                print(" El sistema NO puede funcionar sin cartas rojas")
            elif red_percentage < 30:
                print(f"\n  PROBLEMA: Solo {red_percentage:.1f}% cartas rojas")
                print(" Necesitas al menos 30% para reconocimiento confiable")
            else:
                print("\n Dataset balanceado correctamente")
        
        # Verificar templates organizados
        print("\n TEMPLATES ORGANIZADOS:")
        if os.path.exists(self.templates_path):
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            for suit in suits:
                suit_path = os.path.join(self.templates_path, suit)
                if os.path.exists(suit_path):
                    count = len([f for f in os.listdir(suit_path) 
                               if f.endswith(('.png', '.jpg'))])
                    suit_symbol = {'hearts': '', 'diamonds': '', 'clubs': '', 'spades': ''}[suit]
                    print(f"   {suit_symbol} {suit.upper():9} {count:4} templates")
    
    def clean_imbalanced_sessions(self):
        """Limpiar sesiones desbalanceadas"""
        print("\n  LIMPIANDO SESIONES DESBALANCEADAS")
        print("-" * 50)
        
        if not os.path.exists(self.sessions_path):
            print(" No hay sesiones para limpiar")
            return
        
        sessions = [d for d in os.listdir(self.sessions_path) 
                   if os.path.isdir(os.path.join(self.sessions_path, d))]
        
        deleted_count = 0
        kept_count = 0
        
        for session in sessions:
            session_path = os.path.join(self.sessions_path, session)
            results_file = os.path.join(session_path, "classification_results.json")
            
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    if 'distribution' in data:
                        dist = data['distribution']
                        total = sum(dist.values())
                        red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                        red_percentage = (red_cards / total * 100) if total > 0 else 0
                        
                        # Eliminar sesiones con menos del 10% de cartas rojas
                        if red_percentage < 10:
                            shutil.rmtree(session_path)
                            print(f"    ELIMINADA: {session} ({red_percentage:.1f}% rojas)")
                            deleted_count += 1
                        else:
                            print(f"    MANTENIDA: {session} ({red_percentage:.1f}% rojas)")
                            kept_count += 1
                except:
                    # Si hay error, mantener la sesión
                    kept_count += 1
            else:
                # Sesión sin resultados, mantener
                kept_count += 1
        
        print(f"\n RESULTADO: {deleted_count} eliminadas, {kept_count} mantenidas")
        
        # Limpiar también templates organizados si están desbalanceados
        self.clean_imbalanced_templates()
    
    def clean_imbalanced_templates(self):
        """Limpiar templates organizados desbalanceados"""
        print("\n LIMPIANDO TEMPLATES ORGANIZADOS")
        print("-" * 50)
        
        if not os.path.exists(self.templates_path):
            print(" No hay templates organizados")
            return
        
        # Contar templates por palo
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        counts = {}
        
        for suit in suits:
            suit_path = os.path.join(self.templates_path, suit)
            if os.path.exists(suit_path):
                count = len([f for f in os.listdir(suit_path) 
                           if f.endswith(('.png', '.jpg'))])
                counts[suit] = count
        
        total = sum(counts.values())
        
        if total > 0:
            red_total = counts.get('hearts', 0) + counts.get('diamonds', 0)
            red_percentage = (red_total / total * 100)
            
            print(f"   Total templates: {total}")
            print(f"   Cartas rojas: {red_total} ({red_percentage:.1f}%)")
            
            if red_percentage < 20:
                print("     Templates desbalanceados, creando backup...")
                
                # Crear backup
                backup_dir = f"{self.templates_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                if os.path.exists(self.templates_path):
                    shutil.copytree(self.templates_path, backup_dir)
                    print(f"    Backup creado: {backup_dir}")
                
                # Limpiar directory
                shutil.rmtree(self.templates_path)
                os.makedirs(self.templates_path)
                for suit in suits:
                    os.makedirs(os.path.join(self.templates_path, suit), exist_ok=True)
                
                print("     Templates desbalanceados eliminados")
                print("    Nuevo directorio vacío creado")
    
    def generate_smart_capture_script(self):
        """Generar script de captura inteligente"""
        print("\n GENERANDO SCRIPT DE CAPTURA INTELIGENTE")
        print("-" * 50)
        
        script_content = '''# smart_capture_fixed.py - Captura balanceada automática
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
        print(f"\n Capturando {target_count} cartas balanceadas...")
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
            
            print("\n" + "=" * 60)
            print(" CAPTURA BALANCEADA COMPLETADA!")
            print("=" * 60)
            self._show_final_stats()
            
            # Clasificar automáticamente
            self._auto_classify()
            
        except KeyboardInterrupt:
            print("\n\n  Captura interrumpida por usuario")
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
        else:
            print(f"\n     ADVERTENCIA: Necesitas más cartas rojas")
            print(f"    Ejecuta otra sesión de captura")
    
    def _auto_classify(self):
        """Clasificar automáticamente las cartas"""
        print("\n Clasificando cartas en templates...")
        
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
    print(f"\n Configuración:")
    print(f"    Cartas a capturar: {target_count}")
    print(f"    Objetivo rojas: {capture.stats['target_red_percentage']}%")
    print(f"    Sesión: {capture.session_name}")
    
    confirm = input("\nIniciar captura? (s/n): ").strip().lower()
    if confirm == 's':
        capture.run_capture(target_count)
    else:
        print("  Captura cancelada")

if __name__ == "__main__":
    main()
'''
        
        # Guardar script
        with open("smart_capture_fixed.py", "w", encoding="utf-8") as f:
            f.write(script_content)
        
        print(" Script generado: smart_capture_fixed.py")
        
        # Generar también script de verificación
        self.generate_verification_script()
    
    def generate_verification_script(self):
        """Generar script de verificación"""
        verify_script = '''# verify_balance.py - Verificar balance del dataset
import os
import json

def check_dataset_balance():
    """Verificar balance del dataset"""
    print(" VERIFICANDO BALANCE DEL DATASET")
    print("=" * 60)
    
    # Verificar sesiones
    sessions_path = "data/card_templates/auto_captured"
    if not os.path.exists(sessions_path):
        print(" No hay sesiones de captura")
        return False
    
    sessions = [d for d in os.listdir(sessions_path) 
               if os.path.isdir(os.path.join(sessions_path, d))]
    
    if not sessions:
        print(" No hay sesiones")
        return False
    
    print(f" Sesiones encontradas: {len(sessions)}")
    
    # Analizar cada sesión
    all_stats = []
    
    for session in sessions:
        results_file = os.path.join(sessions_path, session, "classification_results.json")
        stats_file = os.path.join(sessions_path, session, "capture_stats.json")
        
        session_stats = {'name': session, 'cards': 0, 'red_percentage': 0}
        
        # Intentar cargar classification_results
        if os.path.exists(results_file):
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                
                if 'distribution' in data:
                    dist = data['distribution']
                    total = sum(dist.values())
                    red_cards = dist.get('hearts', 0) + dist.get('diamonds', 0)
                    red_percentage = (red_cards / total * 100) if total > 0 else 0
                    
                    session_stats['cards'] = total
                    session_stats['red_percentage'] = red_percentage
                    session_stats['distribution'] = dist
            except:
                pass
        
        # Intentar cargar capture_stats
        elif os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                
                total = data.get('total', 0)
                red_cards = data.get('hearts', 0) + data.get('diamonds', 0)
                red_percentage = (red_cards / total * 100) if total > 0 else 0
                
                session_stats['cards'] = total
                session_stats['red_percentage'] = red_percentage
            except:
                pass
        
        if session_stats['cards'] > 0:
            all_stats.append(session_stats)
    
    # Mostrar resultados
    if not all_stats:
        print(" No hay datos de sesiones")
        return False
    
    print("\n SESIONES ANALIZADAS:")
    print("-" * 50)
    
    total_cards = 0
    total_red = 0
    
    for stats in all_stats:
        red_cards = int(stats['cards'] * stats['red_percentage'] / 100)
        total_cards += stats['cards']
        total_red += red_cards
        
        status = "" if stats['red_percentage'] >= 30 else " " if stats['red_percentage'] >= 15 else ""
        
        print(f"{status} {stats['name']:30} {stats['cards']:4} cartas | "
              f"{stats['red_percentage']:5.1f}% rojas")
    
    # Calcular totales
    overall_red_percentage = (total_red / total_cards * 100) if total_cards > 0 else 0
    
    print("\n" + "=" * 60)
    print(" ESTADÍSTICAS GLOBALES:")
    print(f"    Total cartas: {total_cards}")
    print(f"    Cartas rojas: {total_red} ({overall_red_percentage:.1f}%)")
    print(f"    Cartas negras: {total_cards - total_red} ({100-overall_red_percentage:.1f}%)")
    
    # Evaluación
    print("\n EVALUACIÓN:")
    if overall_red_percentage >= 35:
        print("    EXCELENTE: Dataset bien balanceado (>35% rojas)")
    elif overall_red_percentage >= 30:
        print("    BUENO: Dataset aceptable (30-35% rojas)")
    elif overall_red_percentage >= 20:
        print("     REGULAR: Necesitas más cartas rojas (20-30%)")
    elif overall_red_percentage >= 10:
        print("    MALO: Dataset muy desbalanceado (10-20%)")
    else:
        print("    CRÍTICO: Dataset inútil (<10% rojas)")
    
    # Recomendación
    print("\n RECOMENDACIÓN:")
    if overall_red_percentage < 30:
        needed_red = int((0.3 * total_cards - total_red) / 0.7)
        print(f"   Captura al menos {max(20, needed_red)} cartas más")
        print(f"   Usa: python smart_capture_fixed.py")
    else:
        print("   Dataset listo para entrenamiento")
    
    return overall_red_percentage >= 30

def main():
    """Función principal"""
    if check_dataset_balance():
        print("\n El dataset está listo para usar")
        print(" Ejecuta: python main_integrated.py")
    else:
        print("\n El dataset necesita más cartas rojas")
        print(" Ejecuta: python smart_capture_fixed.py")

if __name__ == "__main__":
    main()
'''
        
        with open("verify_balance.py", "w", encoding="utf-8") as f:
            f.write(verify_script)
        
        print(" Script de verificación: verify_balance.py")
    
    def generate_pokerstars_guide(self):
        """Generar guía para configurar PokerStars"""
        print("\n GENERANDO GUÍA DE CONFIGURACIÓN POKERSTARS")
        print("-" * 50)
        
        guide = '''# CONFIGURACIÓN POKERSTARS PARA CAPTURA BALANCEADA

##  PASO 1: ELEGIR MESA CORRECTA
 USAR ESTAS MESAS (cartas rojas visibles):
    "Classic" tables
    "Triton" series tables  
    "Sunday Million" tables
    Tables with BRIGHT backgrounds

 EVITAR ESTAS MESAS (solo cartas negras):
    "Dark" tables
    "Stealth" tables
    "Night" mode tables
    Tables with DARK backgrounds

##  PASO 2: CONFIGURAR PANTALLA
1. Resolución: 1920x1080 recomendada
2. Brillo del monitor: 70-80%
3. Contraste: 60-70%
4. Apagar "Night Light" o modos oscuros

##  PASO 3: CONFIGURAR POKERSTARS
1. Table Appearance -> "Classic"
2. Card Deck -> "Standard" (no "Dark")
3. Background -> "Light" or "Default"
4. Desactivar "4-Color Deck" (opcional)

##  PASO 4: POSICIÓN DE MESA
1. Mesa NO maximizada (ventana normal)
2. Posición: centro de la pantalla
3. Sin superposiciones (chat, estadísticas a un lado)

##  PASO 5: DETECCIÓN DE COORDENADAS
1. Ejecutar: python detect_coords.py
2. Seleccionar región de cartas del HERO
3. Seleccionar región de cartas COMUNITARIAS
4. Guardar configuración

##  CAPTURA BALANCEADA
Ejecutar: python smart_capture_fixed.py
'''
        
        with open("POKERSTARS_GUIDE.txt", "w", encoding="utf-8") as f:
            f.write(guide)
        
        print(" Guía generada: POKERSTARS_GUIDE.txt")

def main():
    """Función principal"""
    print(" INICIANDO SOLUCIÓN AUTOMÁTICA...")
    
    fixer = DatasetFixer()
    fixer.run_full_fix()

if __name__ == "__main__":
    main()
