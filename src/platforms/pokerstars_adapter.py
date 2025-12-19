"""
Adaptador para PokerStars - Captura y análisis de mesa
"""
import os
import sys
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Añadir path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from screen_capture.stealth_capture import StealthScreenCapture
from screen_capture.card_recognizer import CardRecognizer
from screen_capture.table_detector import TableDetector
from screen_capture.text_ocr import TextOCR

logger = logging.getLogger(__name__)

@dataclass
class PokerStarsGameState:
    """Estado del juego en PokerStars"""
    hero_cards: list = None
    community_cards: list = None
    street: str = ""
    position: str = ""
    pot: int = 0
    stack: int = 0
    to_call: int = 0
    min_raise: int = 0
    max_raise: int = 0
    actions_available: list = None
    
    def __post_init__(self):
        if self.hero_cards is None:
            self.hero_cards = []
        if self.community_cards is None:
            self.community_cards = []
        if self.actions_available is None:
            self.actions_available = []
    
    def is_valid(self) -> bool:
        """Verificar si el estado es válido"""
        return bool(self.hero_cards) and self.street
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "hero_cards": self.hero_cards,
            "community_cards": self.community_cards,
            "street": self.street,
            "position": self.position,
            "pot": self.pot,
            "stack": self.stack,
            "to_call": self.to_call,
            "min_raise": self.min_raise,
            "max_raise": self.max_raise,
            "actions_available": self.actions_available
        }

class PokerStarsAdapter:
    """Adaptador para capturar y analizar mesas de PokerStars"""
    
    def __init__(self, stealth_level: str = "MEDIUM"):
        """
        Inicializar adaptador para PokerStars
        
        Args:
            stealth_level: Nivel de stealth (LOW, MEDIUM, HIGH)
        """
        self.logger = logging.getLogger(__name__)
        self.stealth_level = stealth_level
        self.learning_mode = True
        
        # Inicializar componentes
        self._initialize_components()
        
        # Historial
        self.hand_history = []
        self.current_hand_id = None
        
        self.logger.info(f" PokerStarsAdapter inicializado (stealth: {stealth_level})")
    
    def _initialize_components(self):
        """Inicializar todos los componentes de captura"""
        try:
            # Sistema de captura stealth
            self.capture_system = StealthScreenCapture("pokerstars", self.stealth_level)
            
            # Reconocedor de cartas específico para PokerStars
            self.card_recognizer = CardRecognizer("pokerstars", self.stealth_level)
            
            # Detector de mesa PokerStars
            self.table_detector = TableDetector("pokerstars")
            
            # OCR para textos
            self.text_ocr = TextOCR("pokerstars")
            
            self.logger.info(" Componentes de captura inicializados")
            
        except Exception as e:
            self.logger.error(f" Error inicializando componentes: {e}")
            raise
    
    def is_pokerstars_active(self) -> bool:
        """
        Verificar si PokerStars está activo y visible
        
        Returns:
            bool: True si PokerStars está detectado
        """
        try:
            # Capturar pantalla
            screenshot = self.capture_system.capture()
            if screenshot is None:
                return False
            
            # Buscar elementos característicos de PokerStars
            # 1. Logo de PokerStars
            # 2. Colores específicos (verde oscuro #0a5c1f)
            # 3. Diseño de mesa característico
            
            # Por ahora, simular detección
            # TODO: Implementar detección real con CV
            return self._detect_pokerstars_elements(screenshot)
            
        except Exception as e:
            self.logger.error(f"Error verificando PokerStars: {e}")
            return False
    
    def _detect_pokerstars_elements(self, screenshot) -> bool:
        """Detectar elementos específicos de PokerStars"""
        # Método temporal - siempre devuelve True para testing
        # En producción, implementar detección real con OpenCV
        return True
    
    def capture_and_analyze(self) -> Optional[PokerStarsGameState]:
        """
        Capturar pantalla y analizar estado del juego
        
        Returns:
            PokerStarsGameState o None si no se detecta juego
        """
        try:
            self.logger.debug("Capturando y analizando mesa...")
            
            # 1. Capturar pantalla
            screenshot = self.capture_system.capture()
            if screenshot is None:
                self.logger.warning("No se pudo capturar pantalla")
                return None
            
            # 2. Detectar mesa
            table_info = self.table_detector.detect_table(screenshot)
            if not table_info:
                self.logger.debug("Mesa no detectada")
                return None
            
            # 3. Extraer cartas del héroe
            hero_cards = self.card_recognizer.recognize_hero_cards(screenshot)
            
            # 4. Extraer cartas comunitarias
            community_cards = self.card_recognizer.recognize_community_cards(screenshot)
            
            # 5. Extraer montos (pot, stack, to_call)
            amounts = self.text_ocr.extract_amounts(screenshot)
            
            # 6. Detectar calle actual
            street = self._detect_street(screenshot, community_cards)
            
            # 7. Detectar posición
            position = self._detect_position(screenshot, table_info)
            
            # 8. Detectar acciones disponibles
            actions = self._detect_available_actions(screenshot)
            
            # Crear estado del juego
            game_state = PokerStarsGameState(
                hero_cards=hero_cards,
                community_cards=community_cards,
                street=street,
                position=position,
                pot=amounts.get("pot", 0),
                stack=amounts.get("stack", 0),
                to_call=amounts.get("to_call", 0),
                min_raise=amounts.get("min_raise", 0),
                max_raise=amounts.get("max_raise", 0),
                actions_available=actions
            )
            
            # Guardar en historial si es una mano nueva
            if hero_cards:
                self._save_to_history(game_state)
            
            self.logger.info(f"Estado analizado: {street} - Cartas: {hero_cards}")
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error en captura y análisis: {e}")
            return None
    
    def _detect_street(self, screenshot, community_cards) -> str:
        """Detectar la calle actual del juego"""
        if not community_cards:
            return "preflop"
        elif len(community_cards) == 3:
            return "flop"
        elif len(community_cards) == 4:
            return "turn"
        elif len(community_cards) == 5:
            return "river"
        else:
            return "unknown"
    
    def _detect_position(self, screenshot, table_info) -> str:
        """Detectar posición del jugador"""
        # Por ahora, posición aleatoria para testing
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        import random
        return random.choice(positions)
    
    def _detect_available_actions(self, screenshot) -> list:
        """Detectar acciones disponibles"""
        # Por ahora, acciones básicas
        return ["FOLD", "CHECK", "CALL", "RAISE"]
    
    def _save_to_history(self, game_state: PokerStarsGameState):
        """Guardar estado en historial"""
        hand_data = {
            "timestamp": time.time(),
            "hand_id": self.current_hand_id or f"hand_{int(time.time())}",
            "state": game_state.to_dict()
        }
        self.hand_history.append(hand_data)
        
        # Mantener solo las últimas 100 manos
        if len(self.hand_history) > 100:
            self.hand_history = self.hand_history[-100:]
    
    def save_hand_history(self, game_state: PokerStarsGameState, decision: Dict[str, Any]):
        """Guardar decisión en historial"""
        if self.hand_history:
            last_hand = self.hand_history[-1]
            last_hand["decision"] = decision
            last_hand["decision_time"] = time.time()
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la sesión"""
        return {
            "total_hands": len(self.hand_history),
            "hands_with_decisions": len([h for h in self.hand_history if "decision" in h]),
            "session_start": self.hand_history[0]["timestamp"] if self.hand_history else None,
            "platform": "PokerStars"
        }
    
    def reset_hand_history(self):
        """Resetear historial de manos"""
        self.hand_history = []
        self.current_hand_id = None
