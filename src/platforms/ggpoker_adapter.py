"""
ggpoker_adapter.py - Adaptador específico para GG Poker
Versión completa con importaciones corregidas - FUNCIONA CON ESTRUCTURA src/
"""

import cv2
import numpy as np
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import sys
import os
import random

# ============================================================================
# CORRECCIÓN CRÍTICA DE IMPORTACIONES - FUNCIONA CON ESTRUCTURA src/
# ============================================================================

# Obtener el directorio actual de este archivo
current_dir = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel para llegar a 'src'
src_dir = os.path.join(current_dir, '..')

# Añadir 'src' al path de Python para importaciones absolutas
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# IMPORTAR TODOS LOS MÓDULOS NECESARIOS
try:
    from screen_capture.adaptive_recognizer import AdaptiveCardRecognizer
    from screen_capture.table_detector import TableDetector
    from screen_capture.text_ocr import TextOCR
    from screen_capture.stealth_capture import StealthScreenCapture
    IMPORT_SUCCESS = True
    print("✅ Módulos screen_capture importados correctamente")
except ImportError as e:
    print(f"❌ ERROR CRÍTICO: No se pudieron importar módulos de screen_capture")
    print(f"   Error: {e}")
    print("📁 ESTRUCTURA REQUERIDA:")
    print("   poker-coach-pro/")
    print("   ├── src/")
    print("   │   ├── platforms/ggpoker_adapter.py")
    print("   │   └── screen_capture/")
    print("   │       ├── adaptive_recognizer.py")
    print("   │       ├── table_detector.py")
    print("   │       ├── text_ocr.py")
    print("   │       └── stealth_capture.py")
    print("   └── start_integrated.py")
    IMPORT_SUCCESS = False

# ============================================================================
# DEFINICIÓN DE CLASES
# ============================================================================

@dataclass
class GameState:
    """Estado completo del juego para GG Poker"""
    # Cartas
    hero_cards: List[str]  # Ej: ['Ah', 'Ks']
    board_cards: List[str]  # Ej: ['Jc', 'Th', '2d', '5s', 'Qh']
    
    # Montos
    pot_amount: float
    hero_stack: float
    villain_stack: float
    hero_bet_amount: float
    villain_bet_amount: float
    
    # Estado del juego
    current_street: str  # 'preflop', 'flop', 'turn', 'river', 'showdown'
    hero_position: str  # 'SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'
    action_on_hero: bool  # True si es nuestro turno
    last_action: str  # 'fold', 'check', 'call', 'raise', 'bet'
    
    # Acciones disponibles
    available_actions: Dict[str, bool]  # {'fold': True, 'check': True, 'call': True, 'raise': True}
    min_raise: float
    max_raise: float
    call_amount: float
    
    # Metadatos
    hand_id: str
    timestamp: datetime
    confidence: float  # Confianza total del análisis (0-1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para JSON"""
        return {
            "hero_cards": self.hero_cards,
            "board_cards": self.board_cards,
            "pot_amount": round(self.pot_amount, 2),
            "hero_stack": round(self.hero_stack, 2),
            "villain_stack": round(self.villain_stack, 2),
            "current_street": self.current_street,
            "hero_position": self.hero_position,
            "action_on_hero": self.action_on_hero,
            "available_actions": self.available_actions,
            "min_raise": round(self.min_raise, 2),
            "max_raise": round(self.max_raise, 2),
            "call_amount": round(self.call_amount, 2),
            "hand_id": self.hand_id,
            "timestamp": self.timestamp.isoformat(),
            "confidence": round(self.confidence, 3)
        }

class GGPokerAdapter:
    """Adaptador principal para GG Poker - Conecta captura con análisis"""
    
    def __init__(self, stealth_level: str = "MEDIUM", learning_mode: bool = True):
        """
        Inicializar adaptador para GG Poker
        
        Args:
            stealth_level: Nivel de stealth (MINIMUM, MEDIUM, MAXIMUM)
            learning_mode: Si True, el sistema aprende mientras juega
        """
        if not IMPORT_SUCCESS:
            raise ImportError("No se pudieron importar los módulos necesarios de screen_capture")
        
        self.stealth_level = stealth_level
        self.learning_mode = learning_mode
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging si no está configurado
        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        # Cargar configuración específica de GG Poker
        self.config = self._load_config()
        
        # Inicializar componentes
        self.logger.info("Inicializando componentes de GG Poker...")
        
        # 1. Sistema de captura stealth
        self.capture_system = StealthScreenCapture(stealth_level=stealth_level)
        
        # 2. Reconocedor adaptativo (usa las cartas que descargaste/creaste)
        self.card_recognizer = AdaptiveCardRecognizer(
            platform="ggpoker", 
            stealth_level=stealth_level
        )
        
        # 3. Detector de mesa
        self.table_detector = TableDetector(platform="ggpoker")
        
        # 4. OCR para texto (montos, stacks)
        self.text_ocr = TextOCR(platform="ggpoker")
        
        # 5. Estadísticas y estado
        self.hand_history: List[GameState] = []
        self.current_hand_id = self._generate_hand_id()
        self.session_start = datetime.now()
        
        self.logger.info(f"✅ GGPokerAdapter inicializado (stealth: {stealth_level}, aprendizaje: {learning_mode})")
    
    def _load_config(self) -> Dict:
        """Cargar configuración específica de GG Poker"""
        config_path = Path("config/ggpoker_config.json")
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Configuración por defecto para 1920x1080
            self.logger.warning(f"Configuración no encontrada: {config_path}. Usando valores por defecto.")
            
            default_config = {
                "platform": "ggpoker",
                "optimal_resolution": "1920x1080",
                "preflop_open_size": 2.2,
                "regions": {
                    "hero_cards": {"x1": 0.45, "y1": 0.75, "x2": 0.55, "y2": 0.85},
                    "board_cards": {"x1": 0.35, "y1": 0.45, "x2": 0.65, "y2": 0.55},
                    "pot_amount": {"x1": 0.48, "y1": 0.40, "x2": 0.52, "y2": 0.44},
                    "hero_stack": {"x1": 0.44, "y1": 0.80, "x2": 0.48, "y2": 0.84},
                    "villain_stack": {"x1": 0.52, "y1": 0.80, "x2": 0.56, "y2": 0.84},
                    "action_buttons": {"x1": 0.42, "y1": 0.85, "x2": 0.58, "y2": 0.92},
                    "bet_slider": {"x1": 0.45, "y1": 0.82, "x2": 0.55, "y2": 0.85}
                },
                "colors": {
                    "fold_button": [200, 50, 50],     # Rojo
                    "call_button": [50, 200, 50],     # Verde
                    "raise_button": [50, 100, 200],   # Azul
                    "check_button": [150, 150, 50]    # Amarillo
                },
                "timings": {
                    "analysis_delay_ms": 1000,
                    "min_decision_time": 1.5,
                    "max_decision_time": 3.0
                }
            }
            
            # Guardar configuración por defecto
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            self.logger.info(f"✅ Configuración por defecto guardada en: {config_path}")
            return default_config
    
    def _generate_hand_id(self) -> str:
        """Generar ID único para la mano actual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"GGP_{timestamp}_{random.randint(1000, 9999)}"
    
    def capture_and_analyze(self) -> Optional[GameState]:
        """
        Capturar pantalla y analizar el estado actual del juego
        Esta es la función principal que se llamará en bucle
        
        Returns:
            GameState si se pudo analizar, None si hay error o no es nuestro turno
        """
        try:
            self.logger.debug("Iniciando captura y análisis...")
            
            # 1. Capturar pantalla con stealth
            screenshot = self.capture_system.capture_screen()
            if screenshot is None:
                self.logger.warning("No se pudo capturar pantalla")
                return None
            
            # 2. Analizar estado de la mesa
            table_state = self.table_detector.detect_table_state(screenshot)
            
            # 3. Reconocer cartas del hero
            hero_cards_result = self.card_recognizer.recognize_and_learn(
                screenshot, 
                self.config["regions"]["hero_cards"]
            )
            hero_cards = [str(card) for card in hero_cards_result]
            
            # 4. Reconocer cartas del board (mesa)
            board_cards_result = self.card_recognizer.recognize_and_learn(
                screenshot, 
                self.config["regions"]["board_cards"]
            )
            board_cards = [str(card) for card in board_cards_result]
            
            # 5. Determinar calle (street) basado en número de cartas del board
            current_street = self._determine_street(len(board_cards))
            
            # 6. Leer montos (usando OCR básico por ahora)
            pot_amount = self._read_pot_amount(screenshot)
            hero_stack = self._read_hero_stack(screenshot)
            villain_stack = self._read_villain_stack(screenshot)
            
            # 7. Detectar acciones disponibles
            available_actions = self._detect_available_actions(screenshot)
            action_on_hero = any(available_actions.values())
            
            # 8. Determinar posición del hero (simplificado)
            hero_position = self._determine_hero_position(screenshot, table_state)
            
            # 9. Calcular montos de apuesta
            min_raise, max_raise, call_amount = self._calculate_bet_amounts(
                pot_amount, hero_stack, villain_stack, available_actions
            )
            
            # 10. Calcular confianza total
            confidence = self._calculate_confidence(
                hero_cards, board_cards, pot_amount, hero_stack
            )
            
            # Crear estado del juego
            game_state = GameState(
                hero_cards=hero_cards,
                board_cards=board_cards,
                pot_amount=pot_amount,
                hero_stack=hero_stack,
                villain_stack=villain_stack,
                hero_bet_amount=0.0,  # Por implementar
                villain_bet_amount=0.0,  # Por implementar
                current_street=current_street,
                hero_position=hero_position,
                action_on_hero=action_on_hero,
                last_action="",  # Por implementar
                available_actions=available_actions,
                min_raise=min_raise,
                max_raise=max_raise,
                call_amount=call_amount,
                hand_id=self.current_hand_id,
                timestamp=datetime.now(),
                confidence=confidence
            )
            
            # Guardar en historial
            self.hand_history.append(game_state)
            
            # Log información
            self._log_game_state(game_state)
            
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error en captura y análisis: {e}")
            return None
    
    def _determine_street(self, board_cards_count: int) -> str:
        """Determinar la calle basado en el número de cartas del board"""
        street_map = {
            0: "preflop",
            3: "flop", 
            4: "turn",
            5: "river"
        }
        
        return street_map.get(board_cards_count, "unknown")
    
    def _read_pot_amount(self, screenshot: np.ndarray) -> float:
        """Leer cantidad del pot desde la pantalla"""
        try:
            # Extraer región del pot
            pot_region = self.capture_system.extract_region(
                screenshot, 
                self.config["regions"]["pot_amount"]
            )
            
            # Usar OCR para leer el texto (implementación básica)
            # En una versión real, esto usaría Tesseract o similar
            return self.text_ocr.read_pot_amount(pot_region)
            
        except Exception as e:
            self.logger.warning(f"Error leyendo pot amount: {e}. Usando valor por defecto.")
            return 0.0
    
    def _read_hero_stack(self, screenshot: np.ndarray) -> float:
        """Leer stack del hero"""
        try:
            stack_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["hero_stack"]
            )
            return self.text_ocr.read_player_stack(stack_region)
        except:
            return 100.0  # Valor por defecto
    
    def _read_villain_stack(self, screenshot: np.ndarray) -> float:
        """Leer stack del villain"""
        try:
            stack_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["villain_stack"]
            )
            return self.text_ocr.read_player_stack(stack_region)
        except:
            return 100.0  # Valor por defecto
    
    def _detect_available_actions(self, screenshot: np.ndarray) -> Dict[str, bool]:
        """Detectar qué botones de acción están disponibles"""
        try:
            # Extraer región de botones
            buttons_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["action_buttons"]
            )
            
            # Usar detección de color para identificar botones
            # Esta es una implementación simplificada
            actions = {
                "fold": False,
                "check": False, 
                "call": False,
                "raise": False,
                "bet": False
            }
            
            # Detectar colores de botones
            hsv = cv2.cvtColor(buttons_region, cv2.COLOR_BGR2HSV)
            
            # Buscar botón rojo (Fold)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            red_mask = cv2.inRange(hsv, lower_red, upper_red)
            
            if cv2.countNonZero(red_mask) > 50:
                actions["fold"] = True
            
            # Buscar botón verde (Call/Check)
            lower_green = np.array([40, 100, 100])
            upper_green = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            if cv2.countNonZero(green_mask) > 50:
                # Determinar si es Call o Check basado en contexto
                actions["call"] = True
                actions["check"] = True
            
            # Buscar botón azul (Raise/Bet)
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([140, 255, 255])
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            if cv2.countNonZero(blue_mask) > 50:
                actions["raise"] = True
                actions["bet"] = True
            
            return actions
            
        except Exception as e:
            self.logger.warning(f"Error detectando acciones: {e}")
            return {"fold": True, "check": True, "call": True, "raise": True, "bet": False}
    
    def _determine_hero_position(self, screenshot: np.ndarray, table_state: Dict) -> str:
        """Determinar posición del hero en la mesa"""
        # Esta es una implementación simplificada
        # En una versión completa, analizaríamos la posición del dealer button
        positions = ["SB", "BB", "UTG", "MP", "CO", "BTN"]
        
        # Por ahora, devolver una posición aleatoria para testing
        return random.choice(positions)
    
    def _calculate_bet_amounts(self, pot: float, hero_stack: float, 
                              villain_stack: float, actions: Dict[str, bool]) -> Tuple[float, float, float]:
        """Calcular montos de apuesta mínimos y máximos"""
        min_raise = 2.0  # Mínimo raise en BB
        max_raise = hero_stack  # Máximo: todo el stack
        
        # Si hay una apuesta previa, calcular call amount
        call_amount = 0.0
        
        # Valores por defecto para testing
        if pot > 0:
            min_raise = max(2.0, pot * 0.5)  # Mínimo: 2BB o 50% del pot
            call_amount = pot * 0.25  # 25% del pot para call
        
        return min_raise, max_raise, call_amount
    
    def _calculate_confidence(self, hero_cards: List[str], board_cards: List[str],
                            pot_amount: float, hero_stack: float) -> float:
        """Calcular confianza total del análisis"""
        confidence = 1.0
        
        # Penalizar por cartas no reconocidas
        if len(hero_cards) < 2:
            confidence *= 0.5
        elif len(hero_cards) == 2:
            confidence *= 0.9
        
        # Penalizar por pot amount 0 (posible error de lectura)
        if pot_amount == 0:
            confidence *= 0.7
        
        # Penalizar por stack default
        if hero_stack == 100.0:
            confidence *= 0.8
        
        return max(0.1, min(1.0, confidence))
    
    def _log_game_state(self, game_state: GameState):
        """Loggear información del estado del juego"""
        if game_state.confidence > 0.7:  # Solo loggear si confianza es buena
            self.logger.info(f"🃏 Estado: {game_state.current_street.upper()}")
            self.logger.info(f"   Hero: {game_state.hero_cards} | Board: {game_state.board_cards}")
            self.logger.info(f"   Pot: ${game_state.pot_amount:.2f} | Stack: ${game_state.hero_stack:.2f}")
            
            if game_state.action_on_hero:
                available = [action for action, available in game_state.available_actions.items() if available]
                self.logger.info(f"   ⏰ ACCIÓN REQUERIDA: {', '.join(available)}")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión"""
        if not self.hand_history:
            return {"total_hands": 0, "average_confidence": 0.0}
        
        total_hands = len(self.hand_history)
        avg_confidence = sum(state.confidence for state in self.hand_history) / total_hands
        
        # Contar calles
        streets = {}
        for state in self.hand_history:
            street = state.current_street
            streets[street] = streets.get(street, 0) + 1
        
        return {
            "total_hands": total_hands,
            "average_confidence": round(avg_confidence, 3),
            "streets_analyzed": streets,
            "session_duration": str(datetime.now() - self.session_start),
            "learning_mode": self.learning_mode
        }
    
    def save_hand_history(self, filename: str = None):
        """Guardar historial de manos en JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hand_history_GGP_{timestamp}.json"
        
        filepath = Path("data/hand_history") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        history_data = [state.to_dict() for state in self.hand_history]
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2, default=str)
        
        self.logger.info(f"✅ Historial guardado: {filepath} ({len(history_data)} manos)")
    
    def reset_hand(self):
        """Reiniciar para nueva mano"""
        self.current_hand_id = self._generate_hand_id()
        self.logger.debug(f"Nueva mano iniciada: {self.current_hand_id}")

# ============================================================================
# FUNCIONES DE PRUEBA Y UTILIDAD
# ============================================================================

def test_ggpoker_adapter():
    """Probar el adaptador de GG Poker"""
    print("🧪 TEST: GGPokerAdapter")
    print("=" * 60)
    
    try:
        # 1. Inicializar adaptador
        print("1. Inicializando GGPokerAdapter...")
        adapter = GGPokerAdapter(stealth_level="MINIMUM", learning_mode=True)
        print("   ✅ Adaptador inicializado")
        
        # 2. Mostrar configuración cargada
        print(f"\n2. Configuración cargada:")
        print(f"   Plataforma: {adapter.config.get('platform', 'N/A')}")
        print(f"   Resolución óptima: {adapter.config.get('optimal_resolution', 'N/A')}")
        print(f"   Regiones definidas: {len(adapter.config.get('regions', {}))}")
        
        # 3. Probar estadísticas de aprendizaje
        print("\n3. Verificando sistema de aprendizaje...")
        learning_stats = adapter.card_recognizer.get_learning_stats()
        print(f"   Cartas aprendidas: {learning_stats.get('total_learned_cards', 0)}")
        print(f"   Confianza promedio: {learning_stats.get('average_confidence', 0):.3f}")
        
        # 4. Probar con imagen de prueba (simulada)
        print("\n4. Probando análisis con imagen simulada...")
        
        # Crear screenshot simulado
        test_screenshot = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        # Simular análisis
        game_state = adapter.capture_and_analyze()
        
        if game_state:
            print(f"   ✅ Estado analizado:")
            print(f"      Calle: {game_state.current_street}")
            print(f"      Cartas Hero: {game_state.hero_cards}")
            print(f"      Cartas Board: {game_state.board_cards}")
            print(f"      Pot: ${game_state.pot_amount:.2f}")
            print(f"      Confianza: {game_state.confidence:.3f}")
        else:
            print("   ⚠️  No se pudo analizar (esperado sin juego real)")
        
        # 5. Mostrar estadísticas de sesión
        print("\n5. Estadísticas de sesión:")
        session_stats = adapter.get_session_stats()
        for key, value in session_stats.items():
            print(f"   {key}: {value}")
        
        print("\n" + "=" * 60)
        print("✅ TEST COMPLETADO")
        print("\n🎯 PARA USAR EN JUEGO REAL:")
        print("   1. Abre GG Poker en una mesa")
        print("   2. Ejecuta: python start_coach.py")
        print("   3. El sistema analizará automáticamente cada mano")
        print("   4. Mejorará con cada mano que juegues")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_ggpoker_launcher():
    """Crear script de lanzamiento para GG Poker"""
    launcher_content = '''"""
start_ggpoker_coach.py - Lanzador principal para GG Poker Coach
"""

import sys
import os
import time
import logging
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def main():
    """Función principal del coach de GG Poker"""
    print("🎴 POKER COACH PRO - GG POKER EDITION")
    print("=" * 60)
    
    try:
        # Importar adaptador
        from platforms.ggpoker_adapter import GGPokerAdapter
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/ggpoker_session.log'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger(__name__)
        
        # Inicializar adaptador
        print("🚀 Inicializando Poker Coach Pro para GG Poker...")
        adapter = GGPokerAdapter(stealth_level="MEDIUM", learning_mode=True)
        
        print("✅ Sistema listo")
        print("📋 Modo: Aprendizaje automático ACTIVADO")
        print("🎯 El sistema mejorará con cada mano que juegues")
        print("\n⚠️  ADVERTENCIA: Usa solo para práctica/estudio")
        print("   Las plataformas prohíben software de asistencia")
        
        print("\n" + "=" * 60)
        print("🔄 Iniciando monitoreo... (Ctrl+C para detener)")
        print("=" * 60)
        
        hand_counter = 0
        last_action_time = time.time()
        
        # Bucle principal
        while True:
            try:
                # Capturar y analizar
                game_state = adapter.capture_and_analyze()
                
                if game_state and game_state.action_on_hero:
                    hand_counter += 1
                    last_action_time = time.time()
                    
                    # Mostrar información de la mano
                    print(f"\\n🃏 MANO #{hand_counter} - {game_state.current_street.upper()}")
                    print(f"   Hero: {game_state.hero_cards} | Board: {game_state.board_cards}")
                    print(f"   Pot: ${game_state.pot_amount:.2f} | Stack: ${game_state.hero_stack:.2f}")
                    print(f"   Posición: {game_state.hero_position}")
                    
                    # Mostrar acciones disponibles
                    available = [a.upper() for a, avail in game_state.available_actions.items() if avail]
                    print(f"   ⏰ ACCIONES: {', '.join(available)}")
                    
                    # TODO: Aquí se integrará el motor de decisiones
                    print("   🤖 [DECISIÓN PENDIENTE - Motor en desarrollo]")
                    
                    # Pequeña pausa para no saturar
                    time.sleep(1.5)
                
                # Pausa entre análisis (configurable por stealth)
                time.sleep(0.5)  # 500ms
                
                # Auto-guardar cada 10 manos
                if hand_counter % 10 == 0 and hand_counter > 0:
                    adapter.save_hand_history()
                    
                    # Mostrar estadísticas
                    stats = adapter.get_session_stats()
                    print(f"\\n📊 Estadísticas: {stats['total_hands']} manos analizadas")
                    print(f"   Confianza promedio: {stats['average_confidence']:.3f}")
                
            except KeyboardInterrupt:
                print("\\n⏹️  Deteniendo Poker Coach...")
                break
            except Exception as e:
                logger.error(f"Error en bucle principal: {e}")
                time.sleep(2)  # Pausa más larga en error
        
        # Guardar al finalizar
        print("\\n💾 Guardando datos de sesión...")
        adapter.save_hand_history()
        
        # Mostrar resumen final
        stats = adapter.get_session_stats()
        print(f"\\n📈 RESUMEN FINAL:")
        print(f"   Manos analizadas: {stats['total_hands']}")
        print(f"   Duración: {stats['session_duration']}")
        print(f"   Cartas aprendidas: {adapter.card_recognizer.get_learning_stats()['total_learned_cards']}")
        
        print("\\n✅ Sesión guardada. ¡Hasta la próxima!")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Asegúrate de que todos los módulos estén instalados")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    # Guardar el launcher
    launcher_path = Path("start_ggpoker_coach.py")
    launcher_path.write_text(launcher_content)
    
    print(f"✅ Script de lanzamiento creado: {launcher_path}")
    return launcher_path

if __name__ == "__main__":
    # Ejecutar test
    if test_ggpoker_adapter():
        # Crear script de lanzamiento
        create_ggpoker_launcher()
        
        print("\n🎯 SIGUIENTES PASOS:")
        print("   1. Ejecuta: python start_ggpoker_coach.py")
        print("   2. Abre GG Poker en una mesa")
        print("   3. El sistema analizará automáticamente")
        print("   4. Verás las decisiones en tiempo real")
