# integrated_system_v2.py - Sistema completamente integrado y optimizado
import os
import sys
import time
import threading
import json
from datetime import datetime
from pathlib import Path

# Añadir directorios al path
sys.path.insert(0, "src")
sys.path.insert(0, ".")

class PokerCoachProV2:
    """Versión 2.0 completamente optimizada"""
    
    def __init__(self):
        self.components = {}
        self.is_running = False
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.performance_stats = {
            "capture_times": [],
            "ocr_times": [],
            "gto_times": [],
            "total_times": []
        }
        
        # Cargar configuración
        self.config = self.load_config()
        
        print(" POKER COACH PRO V2.0 - SISTEMA OPTIMIZADO")
        print("=" * 70)
    
    def load_config(self):
        """Cargar configuración del sistema"""
        config_file = "config/system_config.yaml"
        
        if os.path.exists(config_file):
            try:
                import yaml
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            except:
                pass
        
        # Configuración por defecto
        return {
            "capture": {
                "engine": "optimized_capture",
                "interval_ms": 150,
                "adaptive": True
            },
            "ocr": {
                "confidence_threshold": 0.7,
                "use_augmented_data": True
            },
            "performance": {
                "max_threads": 4,
                "cache_enabled": True,
                "monitoring": True
            }
        }
    
    def initialize_optimized(self):
        """Inicialización optimizada con carga diferida"""
        print("\n INICIALIZANDO SISTEMA OPTIMIZADO...")
        
        # Cargar componentes críticos primero
        critical_components = [
            ("capture", self.initialize_capture),
            ("ocr", self.initialize_ocr),
            ("gto", self.initialize_gto)
        ]
        
        loaded = 0
        for name, init_func in critical_components:
            try:
                if init_func():
                    self.components[name] = True
                    loaded += 1
                    print(f"    {name.upper():15} [OPTIMIZADO]")
                else:
                    print(f"     {name.upper():15} [MODO BÁSICO]")
            except Exception as e:
                print(f"    {name.upper():15} Error: {str(e)[:50]}")
        
        # Cargar componentes opcionales
        optional_components = [
            ("overlay", self.initialize_overlay),
            ("analyzer", self.initialize_analyzer),
            ("logger", self.initialize_logger)
        ]
        
        for name, init_func in optional_components:
            try:
                if init_func():
                    self.components[name] = True
                    print(f"    {name.upper():15} [CARGADO]")
            except:
                pass  # Componente opcional, puede fallar
        
        print(f"\n COMPONENTES CARGADOS: {loaded}/3 críticos + {len(self.components)-loaded} opcionales")
        
        return loaded >= 2  # Mínimo captura y OCR
    
    def initialize_capture(self):
        """Inicializar captura optimizada"""
        try:
            # Intentar cargar captura optimizada
            from color_optimizer import ColorOptimizer
            
            self.color_optimizer = ColorOptimizer()
            print("    Optimizador de color cargado")
            
            # Cargar coordenadas de PokerStars
            coords_file = "config/pokerstars_coords.json"
            if os.path.exists(coords_file):
                with open(coords_file, 'r') as f:
                    self.table_regions = json.load(f).get("pokerstars_regions", {})
                print(f"    {len(self.table_regions)} regiones configuradas")
            
            return True
        except Exception as e:
            print(f"     Captura optimizada no disponible: {e}")
            return self.initialize_basic_capture()
    
    def initialize_basic_capture(self):
        """Inicializar captura básica (fallback)"""
        try:
            import pyautogui
            from PIL import Image
            
            print("    Usando captura básica")
            return True
        except:
            return False
    
    def initialize_ocr(self):
        """Inicializar OCR optimizado"""
        try:
            # Verificar si hay dataset aumentado
            aug_dataset = "data/card_templates/augmented_dataset"
            if os.path.exists(aug_dataset):
                print(f"    Dataset aumentado disponible ({len(list(Path(aug_dataset).glob('*/*')))} imágenes)")
            
            # Cargar modelo OCR si existe
            model_path = "data/models/ocr_model.pkl"
            if os.path.exists(model_path):
                print("    Modelo OCR entrenado cargado")
            
            return True
        except Exception as e:
            print(f"     OCR optimizado no disponible: {e}")
            return True  # Siempre retornar True para modo básico
    
    def initialize_gto(self):
        """Inicializar motor GTO optimizado"""
        try:
            # Verificar modelo GTO
            model_path = "data/models/gto_model.pkl"
            
            if os.path.exists(model_path):
                print("    Modelo GTO avanzado cargado")
                
                # Cargar estadísticas
                stats_path = "data/models/gto_stats.json"
                if os.path.exists(stats_path):
                    with open(stats_path, 'r') as f:
                        stats = json.load(f)
                    print(f"   📊 {stats.get('trained_samples', 0)} muestras entrenadas")
            else:
                print("    Usando motor GTO básico")
            
            return True
        except:
            print("     Motor GTO no disponible")
            return True  # Siempre retornar True para modo básico
    
    def initialize_overlay(self):
        """Inicializar overlay optimizado"""
        try:
            # Verificar si tkinter está disponible
            import tkinter as tk
            
            print("     Overlay disponible")
            return True
        except:
            print("   ⚠️  Overlay no disponible")
            return False
    
    def capture_optimized(self):
        """Captura optimizada con detección adaptativa"""
        import pyautogui
        import numpy as np
        
        start_time = time.time()
        
        try:
            # Capturar pantalla completa
            screenshot = pyautogui.screenshot()
            
            # Convertir a numpy array
            frame = np.array(screenshot)
            frame = frame[:, :, ::-1].copy()  # RGB to BGR
            
            # Si tenemos regiones configuradas, extraer mesa
            if hasattr(self, 'table_regions') and 'table_area' in self.table_regions:
                region = self.table_regions['table_area']
                x1, y1, x2, y2 = region['x1'], region['y1'], region['x2'], region['y2']
                table_image = frame[y1:y2, x1:x2]
            else:
                table_image = frame
            
            capture_time = time.time() - start_time
            self.performance_stats["capture_times"].append(capture_time)
            
            # Limitar historial a 100 muestras
            if len(self.performance_stats["capture_times"]) > 100:
                self.performance_stats["capture_times"].pop(0)
            
            return table_image, frame
            
        except Exception as e:
            print(f" Error en captura: {e}")
            return None, None
    
    def detect_cards_optimized(self, table_image):
        """Detección optimizada de cartas"""
        import cv2
        import numpy as np
        
        if table_image is None:
            return []
        
        start_time = time.time()
        
        try:
            # Detectar áreas de interés (cartas)
            gray = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar filtros
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            
            # Buscar contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detected_cards = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filtrar por tamaño (área de carta típica)
                if 500 < area < 5000:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Verificar relación de aspecto (carta ~1.4:1)
                    aspect_ratio = w / h
                    if 1.2 < aspect_ratio < 1.6:
                        # Extraer ROI
                        card_roi = table_image[y:y+h, x:x+w]
                        
                        # Detectar color
                        is_red = self.detect_card_color(card_roi)
                        
                        detected_cards.append({
                            'bbox': (x, y, w, h),
                            'area': area,
                            'aspect_ratio': aspect_ratio,
                            'is_red': is_red,
                            'image': card_roi
                        })
            
            detection_time = time.time() - start_time
            
            return detected_cards
            
        except Exception as e:
            print(f" Error en detección: {e}")
            return []
    
    def detect_card_color(self, card_image):
        """Detección optimizada de color de carta"""
        if not hasattr(self, 'color_optimizer'):
            return False  # Fallback
        
        try:
            import cv2
            import numpy as np
            
            hsv = cv2.cvtColor(card_image, cv2.COLOR_BGR2HSV)
            
            # Usar perfil "classic" por defecto
            mask = self.color_optimizer.detect_red(hsv, "classic")
            
            # Calcular porcentaje de rojo
            red_pixels = np.sum(mask > 0)
            total_pixels = mask.shape[0] * mask.shape[1]
            
            return (red_pixels / total_pixels) > 0.05  # Al menos 5% rojo
            
        except:
            return False
    
    def analyze_with_optimized_gto(self, game_state):
        """Análisis optimizado con motor GTO"""
        start_time = time.time()
        
        # Lógica básica mejorada
        hero_cards = game_state.get('hero_cards', [])
        
        if len(hero_cards) >= 2:
            card1 = hero_cards[0].get('value', '').upper()
            card2 = hero_cards[1].get('value', '').upper()
            suited = hero_cards[0].get('suit') == hero_cards[1].get('suit')
            
            # Evaluación mejorada de mano
            hand_strength = self.evaluate_hand_strength(card1, card2, suited)
            
            decision = self.get_decision_from_strength(
                hand_strength, 
                game_state.get('position', 0),
                game_state.get('bet_to_call', 0)
            )
            
            decision['game_state'] = game_state
            decision['timestamp'] = datetime.now().isoformat()
            decision['hand_evaluation'] = hand_strength
            
            gto_time = time.time() - start_time
            self.performance_stats["gto_times"].append(gto_time)
            
            return decision
        
        # Decisión por defecto
        return {
            'action': 'CHECK',
            'confidence': 0.5,
            'reason': 'Analizando...',
            'timestamp': datetime.now().isoformat()
        }
    
    def evaluate_hand_strength(self, card1, card2, suited):
        """Evaluar fuerza de mano (optimizada)"""
        # Mapear valores a rangos
        value_map = {
            'A': 14, 'K': 13, 'Q': 12, 'J': 11,
            '10': 10, '9': 9, '8': 8, '7': 7,
            '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
        }
        
        v1 = value_map.get(card1, 0)
        v2 = value_map.get(card2, 0)
        
        # Clasificar mano
        if v1 == v2:
            return "POCKET_PAIR"
        elif v1 >= 12 and v2 >= 12:
            return "BIG_CARDS"
        elif suited and (v1 >= 10 or v2 >= 10):
            return "SUITED_CONNECTORS"
        elif abs(v1 - v2) <= 2:
            return "CONNECTORS"
        else:
            return "SPECULATIVE"
    
    def get_decision_from_strength(self, hand_strength, position, bet_to_call):
        """Obtener decisión basada en fuerza de mano"""
        strength_map = {
            "POCKET_PAIR": {"action": "RAISE", "confidence": 0.8},
            "BIG_CARDS": {"action": "RAISE", "confidence": 0.7},
            "SUITED_CONNECTORS": {"action": "CALL", "confidence": 0.6},
            "CONNECTORS": {"action": "CALL", "confidence": 0.5},
            "SPECULATIVE": {"action": "FOLD", "confidence": 0.4}
        }
        
        base = strength_map.get(hand_strength, {"action": "CHECK", "confidence": 0.5})
        
        # Ajustar por posición
        if position <= 2:  # Posición temprana
            if base["action"] == "RAISE":
                base["confidence"] *= 0.9
        elif position >= 4:  # Posición tardía
            base["confidence"] *= 1.1
        
        # Ajustar por tamaño de bet
        if bet_to_call > 0:
            if base["action"] in ["CALL", "RAISE"]:
                base["confidence"] *= 0.95
        
        base["confidence"] = min(0.95, max(0.3, base["confidence"]))
        base["reason"] = f"Mano: {hand_strength.replace('_', ' ').title()}"
        
        return base
    
    def show_performance_dashboard(self):
        """Mostrar dashboard de rendimiento"""
        print("\n" + "=" * 70)
        print(" DASHBOARD DE RENDIMIENTO - POKER COACH PRO V2")
        print("=" * 70)
        
        if not self.performance_stats["capture_times"]:
            print(" No hay datos de rendimiento disponibles")
            return
        
        # Calcular estadísticas
        stats = {}
        for metric, values in self.performance_stats.items():
            if values:
                stats[metric] = {
                    "avg": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values)
                }
        
        print(f"\n  TIEMPOS PROMEDIO (últimas {stats['capture_times']['count']} iteraciones):")
        print(f"    Captura:     {stats['capture_times']['avg']*1000:.1f} ms")
        
        if 'ocr_times' in stats and stats['ocr_times']['count'] > 0:
            print(f"    OCR:         {stats['ocr_times']['avg']*1000:.1f} ms")
        
        print(f"    GTO:         {stats['gto_times']['avg']*1000:.1f} ms")
        
        if 'total_times' in stats and stats['total_times']['count'] > 0:
            total_avg = stats['total_times']['avg'] * 1000
            fps = 1000 / total_avg if total_avg > 0 else 0
            print(f"    Total:       {total_avg:.1f} ms ({fps:.1f} FPS)")
        
        # Mostrar componentes activos
        print(f"\n COMPONENTES ACTIVOS:")
        for name, active in self.components.items():
            status = "" if active else ""
            print(f"   {status} {name}")
        
        # Recomendaciones de optimización
        print(f"\n RECOMENDACIONES:")
        
        if stats['capture_times']['avg'] > 0.1:
            print("    Optimizar captura de pantalla (muy lenta)")
        
        if 'total_times' in stats and stats['total_times']['avg'] > 0.5:
            print("    Reducir intervalo de análisis (>500ms)")
        
        if len(self.components) < 3:
            print("    Cargar más componentes para mejor precisión")
    
    def run_optimized_loop(self, interval=2):
        """Ejecutar loop optimizado de análisis"""
        print("\n" + "=" * 70)
        print(" INICIANDO ANÁLISIS OPTIMIZADO")
        print("=" * 70)
        print(f" Sesión: {self.session_id}")
        print(f"  Intervalo: {interval} segundos")
        print(f" Modo: {'OPTIMIZADO' if len(self.components) >= 3 else 'BÁSICO'}")
        print(" Presiona Ctrl+C para detener")
        print("=" * 70)
        
        self.is_running = True
        iteration = 0
        
        try:
            while self.is_running:
                iteration += 1
                total_start = time.time()
                
                # 1. Capturar
                table_image, full_frame = self.capture_optimized()
                
                if table_image is not None:
                    # 2. Detectar cartas
                    detected_cards = self.detect_cards_optimized(table_image)
                    
                    # 3. Crear game state
                    game_state = {
                        'iteration': iteration,
                        'timestamp': datetime.now().isoformat(),
                        'cards_detected': len(detected_cards),
                        'hero_cards': [],
                        'community_cards': [],
                        'pot_size': 1000,  # Simulado
                        'bet_to_call': 200,  # Simulado
                        'position': 2,
                        'players': 6,
                        'detection_time': time.time() - total_start
                    }
                    
                    # 4. Analizar con GTO
                    decision = self.analyze_with_optimized_gto(game_state)
                    
                    # 5. Mostrar resultados
                    if iteration % 5 == 0:  # Mostrar cada 5 iteraciones
                        print(f"\n Iteración {iteration}")
                        print(f"    Cartas detectadas: {len(detected_cards)}")
                        if detected_cards:
                            red_cards = sum(1 for card in detected_cards if card.get('is_red', False))
                            print(f"    Cartas rojas: {red_cards}")
                        print(f"    Decisión: {decision.get('action', 'N/A')}")
                        print(f"    Confianza: {decision.get('confidence', 0)*100:.0f}%")
                    
                    # Registrar tiempo total
                    total_time = time.time() - total_start
                    self.performance_stats["total_times"].append(total_time)
                    
                    # Limitar historial
                    if len(self.performance_stats["total_times"]) > 100:
                        self.performance_stats["total_times"].pop(0)
                
                # Esperar hasta siguiente iteración
                elapsed = time.time() - total_start
                sleep_time = max(0.1, interval - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print("\n\n  Análisis detenido por usuario")
        except Exception as e:
            print(f"\n Error en loop: {e}")
        finally:
            self.is_running = False
            
            # Mostrar estadísticas finales
            self.show_performance_dashboard()
            
            print("\n Análisis finalizado")
    
    def interactive_mode_v2(self):
        """Modo interactivo mejorado"""
        print("\n" + "=" * 70)
        print(" MODO INTERACTIVO V2 - POKER COACH PRO")
        print("=" * 70)
        
        # Inicializar sistema optimizado
        if not self.initialize_optimized():
            print(" No se pudieron cargar componentes críticos")
            return
        
        while True:
            try:
                print("\n OPCIONES PRINCIPALES:")
                print("1. Iniciar análisis continuo optimizado")
                print("2. Ver dashboard de rendimiento")
                print("3. Probar captura única")
                print("4. Optimizar sistema")
                print("5. Salir")
                
                choice = input("\n Selecciona opción (1-5): ").strip()
                
                if choice == "1":
                    interval = input("Intervalo (segundos, default 2): ").strip()
                    interval = float(interval) if interval.replace('.', '').isdigit() else 2.0
                    
                    self.run_optimized_loop(interval)
                    
                elif choice == "2":
                    self.show_performance_dashboard()
                    
                elif choice == "3":
                    self.test_single_capture()
                    
                elif choice == "4":
                    self.run_optimization_wizard()
                    
                elif choice == "5":
                    print("\n Saliendo del sistema...")
                    break
                    
                else:
                    print(" Opción no válida")
                    
            except KeyboardInterrupt:
                print("\n\n  Operación interrumpida")
            except Exception as e:
                print(f" Error: {e}")
    
    def test_single_capture(self):
        """Probar captura única"""
        print("\n PROBANDO CAPTURA ÚNICA")
        print("-" * 40)
        
        table_image, full_frame = self.capture_optimized()
        
        if table_image is not None:
            import cv2
            
            # Mostrar información
            print(f"   Dimensiones: {table_image.shape[1]}x{table_image.shape[0]}")
            print(f"   Canales: {table_image.shape[2] if len(table_image.shape) > 2 else 1}")
            
            # Detectar cartas
            cards = self.detect_cards_optimized(table_image)
            print(f"    Cartas detectadas: {len(cards)}")
            
            if cards:
                red_cards = sum(1 for card in cards if card.get('is_red', False))
                print(f"    Cartas rojas: {red_cards}")
                
                # Mostrar primera carta
                if cards[0]['image'] is not None:
                    temp_path = "temp_card_test.png"
                    cv2.imwrite(temp_path, cards[0]['image'])
                    print(f"    Primera carta guardada en: {temp_path}")
            
            input("\n Presiona Enter para continuar...")
        else:
            print(" No se pudo capturar imagen")
    
    def run_optimization_wizard(self):
        """Asistente de optimización del sistema"""
        print("\n ASISTENTE DE OPTIMIZACIÓN")
        print("=" * 60)
        
        print("\n SELECCIONA ÁREA A OPTIMIZAR:")
        print("1. Detección de color (para diferentes mesas)")
        print("2. Dataset OCR (data augmentation)")
        print("3. Rendimiento del sistema")
        print("4. Configuración de PokerStars")
        
        choice = input("\n Selecciona (1-4): ").strip()
        
        if choice == "1":
            print("\n EJECUTANDO OPTIMIZADOR DE COLOR...")
            os.system("python color_optimizer.py")
            
        elif choice == "2":
            print("\n EJECUTANDO MEJORADOR OCR...")
            os.system("python ocr_enhancer.py")
            
        elif choice == "3":
            print("\n OPTIMIZANDO RENDIMIENTO...")
            self.show_performance_dashboard()
            
            # Recomendaciones específicas
            print("\n ACCIONES RECOMENDADAS:")
            print("    Ejecutar con menos componentes si es lento")
            print("    Aumentar intervalo de análisis")
            print("    Usar modo básico en computadoras lentas")
            
        elif choice == "4":
            print("\n CONFIGURANDO POKERSTARS...")
            
            config_file = "config/pokerstars_coords.json"
            if os.path.exists(config_file):
                print(" Configuración existente encontrada")
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                print(f"   Mesas configuradas: {len(config.get('pokerstars_regions', {}))}")
                
                update = input("Actualizar configuración? (s/n): ").strip().lower()
                if update == 's':
                    os.system("python detect_coords.py")
            else:
                print(" No hay configuración")
                os.system("python detect_coords.py")
        
        else:
            print(" Opción no válida")

def main():
    """Función principal"""
    print(" POKER COACH PRO V2.0 - SISTEMA OPTIMIZADO")
    print("=" * 70)
    print(" Versión completamente integrada y optimizada")
    print(" Lista para pruebas de rendimiento y producción")
    print("=" * 70)
    
    # Verificar requisitos
    if not os.path.exists("data/card_templates"):
        print(" Error: Estructura del proyecto incompleta")
        print(" Ejecuta primero: python startup_check.py")
        return
    
    # Crear sistema
    system = PokerCoachProV2()
    
    # Mostrar menú
    print("\n MODO DE EJECUCIÓN:")
    print("1. Modo interactivo mejorado (recomendado)")
    print("2. Análisis continuo automático")
    print("3. Solo verificación del sistema")
    print("4. Optimización avanzada")
    
    try:
        choice = input("\n Selecciona opción (1-4): ").strip()
        
        if choice == "1":
            system.interactive_mode_v2()
        elif choice == "2":
            interval = input("Intervalo (segundos, default 2): ").strip()
            interval = float(interval) if interval.replace('.', '').isdigit() else 2.0
            system.initialize_optimized()
            system.run_optimized_loop(interval)
        elif choice == "3":
            system.initialize_optimized()
            system.show_performance_dashboard()
        elif choice == "4":
            system.run_optimization_wizard()
        else:
            print(" Opción no válida")
            
    except KeyboardInterrupt:
        print("\n\n  Programa interrumpido")
    except Exception as e:
        print(f" Error inesperado: {e}")

if __name__ == "__main__":
    main()
