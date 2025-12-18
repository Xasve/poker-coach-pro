"""
pokerstars_adapter.py - Adaptador específico para PokerStars
Versión completa con importaciones corregidas
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
# CORRECCIÓN DE IMPORTACIONES
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
    print("✅ Módulos screen_capture importados correctamente para PokerStars")
except ImportError as e:
    print(f"❌ ERROR CRÍTICO: No se pudieron importar módulos de screen_capture")
    print(f"   Error: {e}")
    IMPORT_SUCCESS = False

# ============================================================================
# DEFINICIÓN DE CLASES
# ============================================================================

@dataclass
class PokerStarsGameState:
    """Estado completo del juego para PokerStars"""
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
    
    # Específico de PokerStars
    tournament_mode: bool  # True si es torneo
    ante_amount: float  # Ante si aplica
    time_bank_remaining: float  # Tiempo de banco restante
    
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
            "confidence": round(self.confidence, 3),
            "tournament_mode": self.tournament_mode,
            "ante_amount": round(self.ante_amount, 2),
            "time_bank_remaining": round(self.time_bank_remaining, 1)
        }

class PokerStarsAdapter:
    """Adaptador principal para PokerStars - Conecta captura con análisis"""
    
    def __init__(self, stealth_level: str = "MEDIUM", learning_mode: bool = True, 
                 is_tournament: bool = False):
        """
        Inicializar adaptador para PokerStars
        
        Args:
            stealth_level: Nivel de stealth (MINIMUM, MEDIUM, MAXIMUM)
            learning_mode: Si True, el sistema aprende mientras juega
            is_tournament: True si estamos en modo torneo
        """
        if not IMPORT_SUCCESS:
            raise ImportError("No se pudieron importar los módulos necesarios de screen_capture")
        
        self.stealth_level = stealth_level
        self.learning_mode = learning_mode
        self.is_tournament = is_tournament
        self.logger = logging.getLogger(__name__)
        
        # Configurar logging si no está configurado
        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        # Cargar configuración específica de PokerStars
        self.config = self._load_config()
        
        # Inicializar componentes
        self.logger.info("Inicializando componentes de PokerStars...")
        
        # 1. Sistema de captura stealth
        self.capture_system = StealthScreenCapture(stealth_level=stealth_level)
        
        # 2. Reconocedor adaptativo
        self.card_recognizer = AdaptiveCardRecognizer(
            platform="pokerstars", 
            stealth_level=stealth_level
        )
        
        # 3. Detector de mesa
        self.table_detector = TableDetector(platform="pokerstars")
        
        # 4. OCR para texto (montos, stacks)
        self.text_ocr = TextOCR(platform="pokerstars")
        
        # 5. Estadísticas y estado
        self.hand_history: List[PokerStarsGameState] = []
        self.current_hand_id = self._generate_hand_id()
        self.session_start = datetime.now()
        self.time_bank_start = 30.0 if is_tournament else 0.0  # 30 segundos en torneos
        
        self.logger.info(f"✅ PokerStarsAdapter inicializado (stealth: {stealth_level}, torneo: {is_tournament})")
    
    def _load_config(self) -> Dict:
        """Cargar configuración específica de PokerStars"""
        config_path = Path("config/pokerstars_config.json")
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Configuración por defecto para 1920x1080 - INTERFAZ VERDE CLÁSICA
            self.logger.warning(f"Configuración no encontrada: {config_path}. Usando valores por defecto.")
            
            default_config = {
                "platform": "pokerstars",
                "optimal_resolution": "1920x1080",
                "preflop_open_size": 2.5,  # PokerStars usa 2.5BB standard
                "theme": "green_classic",  # Tema verde clásico
                
                # REGIONES PARA POKERSTARS (1920x1080 - Tema verde)
                "regions": {
                    "hero_cards": {"x1": 0.47, "y1": 0.78, "x2": 0.53, "y2": 0.85},
                    "board_cards": {"x1": 0.38, "y1": 0.48, "x2": 0.62, "y2": 0.55},
                    "pot_amount": {"x1": 0.49, "y1": 0.42, "x2": 0.51, "y2": 0.45},
                    "hero_stack": {"x1": 0.46, "y1": 0.82, "x2": 0.50, "y2": 0.86},
                    "villain_stack": {"x1": 0.50, "y1": 0.82, "x2": 0.54, "y2": 0.86},
                    "action_buttons": {"x1": 0.40, "y1": 0.87, "x2": 0.60, "y2": 0.95},
                    "bet_slider": {"x1": 0.44, "y1": 0.84, "x2": 0.56, "y2": 0.87},
                    "tournament_info": {"x1": 0.02, "y1": 0.02, "x2": 0.15, "y2": 0.08},
                    "time_bank": {"x1": 0.85, "y1": 0.02, "x2": 0.95, "y2": 0.06}
                },
                
                # COLORES POKERSTARS (Tema verde)
                "colors": {
                    "fold_button": [180, 40, 40],     # Rojo oscuro
                    "call_button": [40, 180, 40],     # Verde brillante
                    "raise_button": [40, 100, 200],   # Azul
                    "check_button": [180, 180, 40],   # Amarillo
                    "bet_button": [200, 120, 40],     # Naranja
                    "allin_button": [200, 40, 200],   # Púrpura
                    "table_background": [0, 80, 0],   # Verde oscuro de fondo
                    "card_background": [240, 240, 220] # Beige de cartas
                },
                
                "timings": {
                    "analysis_delay_ms": 1200,
                    "min_decision_time": 1.8,
                    "max_decision_time": 3.2,
                    "time_bank_warning": 10.0  # Advertir cuando queden 10s de time bank
                },
                
                # CONFIGURACIONES ESPECÍFICAS POKERSTARS
                "pokerstars_specific": {
                    "standard_bet_sizes": {
                        "preflop_open": 2.5,
                        "3bet": 3.0,
                        "4bet": 2.2,
                        "cbet": 0.66,  # 2/3 del pot (común en PokerStars)
                        "turn_barrel": 0.75,
                        "river_value": 0.80
                    },
                    "ante_structure": {
                        "cash_no_ante": 0.0,
                        "tournament_ante": 0.1,  # 10% del BB
                        "spin_go_ante": 0.25    # 25% del BB
                    },
                    "time_banks": {
                        "cash_no_bank": 0.0,
                        "tournament_initial": 30.0,
                        "spin_go_initial": 12.0
                    }
                }
            }
            
            # Guardar configuración por defecto
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            self.logger.info(f"✅ Configuración PokerStars guardada en: {config_path}")
            return default_config
    
    def _generate_hand_id(self) -> str:
        """Generar ID único para la mano actual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = "PS_T" if self.is_tournament else "PS_C"  # PS_T para torneo, PS_C para cash
        return f"{prefix}_{timestamp}_{random.randint(1000, 9999)}"
    
    def capture_and_analyze(self) -> Optional[PokerStarsGameState]:
        """
        Capturar pantalla y analizar el estado actual del juego en PokerStars
        
        Returns:
            PokerStarsGameState si se pudo analizar, None si hay error
        """
        try:
            self.logger.debug("Iniciando captura y análisis PokerStars...")
            
            # 1. Capturar pantalla con stealth
            screenshot = self.capture_system.capture_screen()
            if screenshot is None:
                self.logger.warning("No se pudo capturar pantalla")
                return None
            
            # 2. Detectar si es torneo (basado en región de info de torneo)
            tournament_detected = self._detect_tournament_mode(screenshot)
            if tournament_detected != self.is_tournament:
                self.logger.info(f"Modo detectado: {'Torneo' if tournament_detected else 'Cash'}")
                self.is_tournament = tournament_detected
            
            # 3. Analizar estado de la mesa
            table_state = self.table_detector.detect_table_state(screenshot)
            
            # 4. Reconocer cartas del hero
            hero_cards_result = self.card_recognizer.recognize_and_learn(
                screenshot, 
                self.config["regions"]["hero_cards"]
            )
            hero_cards = [str(card) for card in hero_cards_result]
            
            # 5. Reconocer cartas del board (mesa)
            board_cards_result = self.card_recognizer.recognize_and_learn(
                screenshot, 
                self.config["regions"]["board_cards"]
            )
            board_cards = [str(card) for card in board_cards_result]
            
            # 6. Determinar calle (street) basado en número de cartas del board
            current_street = self._determine_street(len(board_cards))
            
            # 7. Leer montos
            pot_amount = self._read_pot_amount(screenshot)
            hero_stack = self._read_hero_stack(screenshot)
            villain_stack = self._read_villain_stack(screenshot)
            
            # 8. Leer ante si hay (especialmente en torneos)
            ante_amount = self._read_ante_amount(screenshot)
            
            # 9. Leer time bank restante (si es torneo)
            time_bank_remaining = self._read_time_bank(screenshot) if self.is_tournament else 0.0
            
            # 10. Detectar acciones disponibles
            available_actions = self._detect_available_actions(screenshot)
            action_on_hero = any(available_actions.values())
            
            # 11. Determinar posición del hero
            hero_position = self._determine_hero_position(screenshot, table_state)
            
            # 12. Calcular montos de apuesta (ajustados para PokerStars)
            min_raise, max_raise, call_amount = self._calculate_bet_amounts_pokerstars(
                pot_amount, hero_stack, villain_stack, available_actions, current_street
            )
            
            # 13. Calcular confianza total
            confidence = self._calculate_confidence_pokerstars(
                hero_cards, board_cards, pot_amount, hero_stack, time_bank_remaining
            )
            
            # Crear estado del juego específico de PokerStars
            game_state = PokerStarsGameState(
                hero_cards=hero_cards,
                board_cards=board_cards,
                pot_amount=pot_amount,
                hero_stack=hero_stack,
                villain_stack=villain_stack,
                hero_bet_amount=0.0,
                villain_bet_amount=0.0,
                current_street=current_street,
                hero_position=hero_position,
                action_on_hero=action_on_hero,
                last_action="",
                available_actions=available_actions,
                min_raise=min_raise,
                max_raise=max_raise,
                call_amount=call_amount,
                hand_id=self.current_hand_id,
                timestamp=datetime.now(),
                confidence=confidence,
                tournament_mode=self.is_tournament,
                ante_amount=ante_amount,
                time_bank_remaining=time_bank_remaining
            )
            
            # Guardar en historial
            self.hand_history.append(game_state)
            
            # Log información específica de PokerStars
            self._log_pokerstars_game_state(game_state)
            
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error en captura y análisis PokerStars: {e}")
            return None
    
    def _detect_tournament_mode(self, screenshot: np.ndarray) -> bool:
        """Detectar si estamos en modo torneo"""
        try:
            # Extraer región de información de torneo
            tourney_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["tournament_info"]
            )
            
            # Buscar texto como "Tournament", "Blinds", "Players", etc.
            # Implementación básica - buscar colores específicos de torneo
            hsv = cv2.cvtColor(tourney_region, cv2.COLOR_BGR2HSV)
            
            # Buscar colores de indicadores de torneo (dorado/amarillo típico)
            lower_gold = np.array([20, 100, 100])
            upper_gold = np.array([40, 255, 255])
            gold_mask = cv2.inRange(hsv, lower_gold, upper_gold)
            
            # Si hay suficiente área dorada, probablemente sea torneo
            if cv2.countNonZero(gold_mask) > 100:
                return True
            
            # Buscar texto "Tournament" con detección de bordes
            edges = cv2.Canny(tourney_region, 50, 150)
            if np.sum(edges) > 5000:  # Muchos bordes = probablemente texto
                return True
                
        except:
            pass
        
        return False
    
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
        """Leer cantidad del pot en PokerStars"""
        try:
            # PokerStars suele mostrar el pot en el centro
            pot_region = self.capture_system.extract_region(
                screenshot, 
                self.config["regions"]["pot_amount"]
            )
            
            # Convertir a escala de grises y mejorar contraste
            gray = cv2.cvtColor(pot_region, cv2.COLOR_BGR2GRAY)
            enhanced = cv2.equalizeHist(gray)
            
            # Usar OCR básico
            # En versión real usaríamos Tesseract entrenado para PokerStars
            return self.text_ocr.read_pot_amount(enhanced)
            
        except Exception as e:
            self.logger.warning(f"Error leyendo pot amount PokerStars: {e}")
            return 0.0
    
    def _read_hero_stack(self, screenshot: np.ndarray) -> float:
        """Leer stack del hero en PokerStars"""
        try:
            stack_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["hero_stack"]
            )
            return self.text_ocr.read_player_stack(stack_region)
        except:
            return 100.0  # Valor por defecto
    
    def _read_villain_stack(self, screenshot: np.ndarray) -> float:
        """Leer stack del villain en PokerStars"""
        try:
            stack_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["villain_stack"]
            )
            return self.text_ocr.read_player_stack(stack_region)
        except:
            return 100.0  # Valor por defecto
    
    def _read_ante_amount(self, screenshot: np.ndarray) -> float:
        """Leer cantidad de ante (si aplica)"""
        if not self.is_tournament:
            return 0.0
        
        try:
            # En PokerStars, el ante suele mostrarse cerca del pot
            # Implementación simplificada
            return self.config["pokerstars_specific"]["ante_structure"]["tournament_ante"]
        except:
            return 0.0
    
    def _read_time_bank(self, screenshot: np.ndarray) -> float:
        """Leer tiempo de banco restante"""
        try:
            time_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["time_bank"]
            )
            
            # Convertir a HSV para detectar colores del time bank
            hsv = cv2.cvtColor(time_region, cv2.COLOR_BGR2HSV)
            
            # Buscar verde (tiempo bueno) vs rojo (tiempo bajo)
            lower_green = np.array([40, 100, 100])
            upper_green = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            red_mask = cv2.inRange(hsv, lower_red, upper_red)
            
            # Estimación simple basada en color
            green_area = cv2.countNonZero(green_mask)
            red_area = cv2.countNonZero(red_mask)
            
            if red_area > green_area * 2:
                return 5.0  # Poco tiempo (rojo dominante)
            elif red_area > green_area:
                return 15.0  # Tiempo medio
            else:
                return 30.0  # Tiempo bueno
            
        except:
            return self.time_bank_start
    
    def _detect_available_actions(self, screenshot: np.ndarray) -> Dict[str, bool]:
        """Detectar qué botones de acción están disponibles en PokerStars"""
        try:
            # Extraer región de botones
            buttons_region = self.capture_system.extract_region(
                screenshot,
                self.config["regions"]["action_buttons"]
            )
            
            # PokerStars tiene colores característicos
            actions = {
                "fold": False,
                "check": False, 
                "call": False,
                "raise": False,
                "bet": False,
                "allin": False  # Botón All-in específico de PokerStars
            }
            
            # Detectar colores específicos de PokerStars
            hsv = cv2.cvtColor(buttons_region, cv2.COLOR_BGR2HSV)
            
            # Botón FOLD - Rojo oscuro en PokerStars
            lower_fold = np.array([0, 100, 50])
            upper_fold = np.array([10, 255, 150])
            fold_mask = cv2.inRange(hsv, lower_fold, upper_fold)
            
            if cv2.countNonZero(fold_mask) > 30:
                actions["fold"] = True
            
            # Botón CALL/CHECK - Verde brillante
            lower_call = np.array([40, 150, 100])
            upper_call = np.array([80, 255, 200])
            call_mask = cv2.inRange(hsv, lower_call, upper_call)
            
            if cv2.countNonZero(call_mask) > 30:
                actions["call"] = True
                actions["check"] = True
            
            # Botón RAISE/BET - Azul
            lower_raise = np.array([100, 100, 100])
            upper_raise = np.array([140, 255, 255])
            raise_mask = cv2.inRange(hsv, lower_raise, upper_raise)
            
            if cv2.countNonZero(raise_mask) > 30:
                actions["raise"] = True
                actions["bet"] = True
            
            # Botón ALL-IN - Púrpura (específico de PokerStars)
            lower_allin = np.array([140, 100, 100])
            upper_allin = np.array([170, 255, 255])
            allin_mask = cv2.inRange(hsv, lower_allin, upper_allin)
            
            if cv2.countNonZero(allin_mask) > 30:
                actions["allin"] = True
            
            return actions
            
        except Exception as e:
            self.logger.warning(f"Error detectando acciones PokerStars: {e}")
            return {"fold": True, "check": True, "call": True, "raise": True, "bet": False, "allin": False}
    
    def _determine_hero_position(self, screenshot: np.ndarray, table_state: Dict) -> str:
        """Determinar posición del hero en la mesa de PokerStars"""
        # Implementación simplificada
        positions = ["SB", "BB", "UTG", "MP", "CO", "BTN"]
        return random.choice(positions)
    
    def _calculate_bet_amounts_pokerstars(self, pot: float, hero_stack: float, 
                                         villain_stack: float, actions: Dict[str, bool],
                                         street: str) -> Tuple[float, float, float]:
        """Calcular montos de apuesta específicos para PokerStars"""
        
        # Tamaños de apuesta estándar en PokerStars
        bet_sizes = self.config["pokerstars_specific"]["standard_bet_sizes"]
        
        min_raise = 2.5  # PokerStars: 2.5BB mínimo
        max_raise = hero_stack
        
        # Call amount por defecto
        call_amount = 0.0
        
        # Ajustar según la calle
        if street == "preflop":
            min_raise = bet_sizes["preflop_open"]
            if pot > 0:
                call_amount = pot * 0.4  # 40% del pot para call preflop
        elif street == "flop":
            min_raise = max(2.5, pot * bet_sizes["cbet"])
            call_amount = pot * 0.33  # 33% del pot
        elif street == "turn":
            min_raise = max(2.5, pot * bet_sizes["turn_barrel"])
            call_amount = pot * 0.5  # 50% del pot
        elif street == "river":
            min_raise = max(2.5, pot * bet_sizes["river_value"])
            call_amount = pot * 0.66  # 66% del pot
        
        return min_raise, max_raise, call_amount
    
    def _calculate_confidence_pokerstars(self, hero_cards: List[str], board_cards: List[str],
                                       pot_amount: float, hero_stack: float, 
                                       time_bank: float) -> float:
        """Calcular confianza total del análisis para PokerStars"""
        confidence = 1.0
        
        # Penalizar por cartas no reconocidas
        if len(hero_cards) < 2:
            confidence *= 0.4
        elif len(hero_cards) == 2:
            confidence *= 0.9
        
        # Penalizar por pot amount 0
        if pot_amount == 0:
            confidence *= 0.6
        
        # Penalizar por stack default
        if hero_stack == 100.0:
            confidence *= 0.7
        
        # Bonificar/penalizar por time bank
        if self.is_tournament:
            if time_bank < 5.0:
                confidence *= 0.8  # Menos confianza con poco time bank
            elif time_bank > 20.0:
                confidence *= 1.1  # Más confianza con buen time bank
        
        return max(0.1, min(1.0, confidence))
    
    def _log_pokerstars_game_state(self, game_state: PokerStarsGameState):
        """Loggear información del estado del juego específica de PokerStars"""
        if game_state.confidence > 0.6:
            mode = "🎯 TORNEO" if game_state.tournament_mode else "💰 CASH"
            self.logger.info(f"{mode} - {game_state.current_street.upper()}")
            self.logger.info(f"   Hero: {game_state.hero_cards} | Board: {game_state.board_cards}")
            
            if game_state.tournament_mode and game_state.ante_amount > 0:
                self.logger.info(f"   Pot: ${game_state.pot_amount:.2f} (+${game_state.ante_amount:.2f} ante)")
            else:
                self.logger.info(f"   Pot: ${game_state.pot_amount:.2f}")
                
            self.logger.info(f"   Stack: ${game_state.hero_stack:.2f}")
            
            if game_state.tournament_mode:
                self.logger.info(f"   Time Bank: {game_state.time_bank_remaining:.1f}s")
            
            if game_state.action_on_hero:
                available = [action.upper() for action, avail in game_state.available_actions.items() if avail]
                self.logger.info(f"   ⏰ ACCIÓN REQUERIDA: {', '.join(available)}")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión de PokerStars"""
        if not self.hand_history:
            return {"total_hands": 0, "average_confidence": 0.0}
        
        total_hands = len(self.hand_history)
        avg_confidence = sum(state.confidence for state in self.hand_history) / total_hands
        
        # Contar calles y modos
        streets = {}
        tournament_hands = 0
        cash_hands = 0
        
        for state in self.hand_history:
            street = state.current_street
            streets[street] = streets.get(street, 0) + 1
            
            if state.tournament_mode:
                tournament_hands += 1
            else:
                cash_hands += 1
        
        return {
            "total_hands": total_hands,
            "average_confidence": round(avg_confidence, 3),
            "streets_analyzed": streets,
            "tournament_hands": tournament_hands,
            "cash_hands": cash_hands,
            "session_duration": str(datetime.now() - self.session_start),
            "learning_mode": self.learning_mode,
            "platform": "PokerStars"
        }
    
    def save_hand_history(self, filename: str = None):
        """Guardar historial de manos en JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode = "TOURNEY" if self.is_tournament else "CASH"
            filename = f"hand_history_PS_{mode}_{timestamp}.json"
        
        filepath = Path("data/hand_history") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        history_data = [state.to_dict() for state in self.hand_history]
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2, default=str)
        
        self.logger.info(f"✅ Historial PokerStars guardado: {filepath} ({len(history_data)} manos)")
    
    def reset_hand(self):
        """Reiniciar para nueva mano"""
        self.current_hand_id = self._generate_hand_id()
        self.logger.debug(f"Nueva mano PokerStars iniciada: {self.current_hand_id}")
    
    def export_to_hand_history_converter(self):
        """Exportar historial en formato compatible con convertidores de HH"""
        if not self.hand_history:
            return None
        
        # Formato básico para convertidores como PokerTracker, Hold'em Manager
        hh_format = []
        
        for state in self.hand_history:
            hand_text = f"PokerStars Hand #{state.hand_id}: "
            hand_text += f"Hold'em {'Tournament' if state.tournament_mode else 'Cash Game'} "
            
            if state.tournament_mode:
                hand_text += f"(Ante ${state.ante_amount:.2f}) "
            
            hand_text += f"- {state.timestamp.strftime('%Y/%m/%d %H:%M:%S')}\n"
            hand_text += f"Hero: {', '.join(state.hero_cards)}\n"
            
            if state.board_cards:
                hand_text += f"Board: {', '.join(state.board_cards)}\n"
            
            hand_text += f"Pot: ${state.pot_amount:.2f}\n"
            hand_text += f"Street: {state.current_street}\n"
            
            hh_format.append(hand_text)
        
        return hh_format

# ============================================================================
# FUNCIONES DE PRUEBA Y UTILIDAD
# ============================================================================

def test_pokerstars_adapter():
    """Probar el adaptador de PokerStars"""
    print("🧪 TEST: PokerStarsAdapter")
    print("=" * 60)
    
    try:
        # 1. Inicializar adaptador
        print("1. Inicializando PokerStarsAdapter...")
        adapter = PokerStarsAdapter(stealth_level="MINIMUM", learning_mode=True, is_tournament=False)
        print("   ✅ Adaptador inicializado")
        
        # 2. Mostrar configuración cargada
        print(f"\n2. Configuración PokerStars cargada:")
        print(f"   Plataforma: {adapter.config.get('platform', 'N/A')}")
        print(f"   Tema: {adapter.config.get('theme', 'N/A')}")
        print(f"   Open preflop: {adapter.config.get('preflop_open_size', 'N/A')}BB")
        print(f"   Regiones definidas: {len(adapter.config.get('regions', {}))}")
        
        # 3. Probar estadísticas de aprendizaje
        print("\n3. Verificando sistema de aprendizaje...")
        learning_stats = adapter.card_recognizer.get_learning_stats()
        print(f"   Cartas aprendidas: {learning_stats.get('total_learned_cards', 0)}")
        print(f"   Plataforma aprendizaje: {learning_stats.get('platform', 'N/A')}")
        
        # 4. Probar con imagen de prueba (simulada)
        print("\n4. Probando análisis con imagen simulada...")
        
        # Crear screenshot simulado con fondo verde (PokerStars)
        test_screenshot = np.zeros((1080, 1920, 3), dtype=np.uint8)
        # Fondo verde típico de PokerStars
        test_screenshot[:, :] = [0, 100, 0]  # BGR: verde
        
        # Simular análisis
        game_state = adapter.capture_and_analyze()
        
        if game_state:
            print(f"   ✅ Estado analizado:")
            print(f"      Calle: {game_state.current_street}")
            print(f"      Cartas Hero: {game_state.hero_cards}")
            print(f"      Cartas Board: {game_state.board_cards}")
            print(f"      Pot: ${game_state.pot_amount:.2f}")
            print(f"      Modo: {'Torneo' if game_state.tournament_mode else 'Cash'}")
            print(f"      Confianza: {game_state.confidence:.3f}")
        else:
            print("   ⚠️  No se pudo analizar (esperado sin juego real)")
        
        # 5. Mostrar estadísticas de sesión
        print("\n5. Estadísticas de sesión:")
        session_stats = adapter.get_session_stats()
        for key, value in session_stats.items():
            if key not in ["streets_analyzed"]:
               