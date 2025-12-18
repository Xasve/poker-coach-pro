# Archivo: src/platforms/ggpoker_adapter.py
"""
ggpoker_adapter.py - Adaptador específico para GG Poker
Analiza screenshots completos y extrae el estado del juego
"""

import cv2
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..screen_capture.card_recognizer import CardRecognizer
from ..screen_capture.table_detector import TableDetector
from ..screen_capture.text_ocr import TextOCR

@dataclass
class GameState:
    """Estado completo del juego"""
    hero_cards: List[str]  # Ej: ['Ah', 'Ks']
    board_cards: List[str]  # Ej: ['Jc', 'Th', '2d']
    pot_amount: float
    hero_stack: float
    villain_stack: float
    current_street: str  # 'preflop', 'flop', 'turn', 'river'
    hero_position: str  # 'SB', 'BB', 'UTG', 'MP', 'CO', 'BTN'
    action_on_hero: bool
    min_raise: float
    max_raise: float
    timestamp: datetime

class GGPokerAdapter:
    """Adaptador específico para GG Poker"""
    
    def __init__(self, stealth_level: str = "MEDIUM"):
        self.stealth_level = stealth_level
        self.logger = logging.getLogger(__name__)
        
        # Inicializar componentes
        self.card_recognizer = CardRecognizer(
            platform="ggpoker", 
            stealth_level=stealth_level
        )
        self.table_detector = TableDetector(platform="ggpoker")
        self.text_ocr = TextOCR(platform="ggpoker")
        
        # Configuración de regiones para GG Poker (1920x1080)
        self.regions = {
            "hero_cards": {"x1": 0.45, "y1": 0.75, "x2": 0.55, "y2": 0.85},
            "board_cards": {"x1": 0.35, "y1": 0.45, "x2": 0.65, "y2": 0.55},
            "pot_amount": {"x1": 0.48, "y1": 0.40, "x2": 0.52, "y2": 0.44},
            "hero_stack": {"x1": 0.44, "y1": 0.80, "x2": 0.48, "y2": 0.84},
            "action_buttons": {"x1": 0.42, "y1": 0.85, "x2": 0.58, "y2": 0.92}
        }
        
        self.logger.info(f"GGPokerAdapter inicializado (stealth: {stealth_level})")
    
    def analyze_screenshot(self, screenshot: np.ndarray) -> Optional[GameState]:
        """
        Analizar screenshot completo y extraer estado del juego
        
        Args:
            screenshot: Captura de pantalla completa
            
        Returns:
            Estado del juego o None si no se pudo analizar
        """
        try:
            self.logger.debug("Analizando screenshot de GG Poker")
            
            # 1. Reconocer cartas del hero
            hero_cards_result = self.card_recognizer.recognize_cards_in_region(
                screenshot, self.regions["hero_cards"]
            )
            hero_cards = [str(card) for card in hero_cards_result]
            
            # 2. Reconocer cartas del board
            board_cards_result = self.card_recognizer.recognize_cards_in_region(
                screenshot, self.regions["board_cards"]
            )
            board_cards = [str(card) for card in board_cards_result]
            
            # 3. Determinar calle (street) basado en número de cartas del board
            current_street = self._determine_street(len(board_cards))
            
            # 4. Leer montos (implementación básica - en realidad usar OCR)
            pot_amount = 0.0  # self.text_ocr.read_pot_amount(...)
            hero_stack = 100.0  # self.text_ocr.read_player_stack(...)
            
            # 5. Detectar acción disponible
            action_available = self._detect_action_buttons(screenshot)
            
            # 6. Determinar posición (simplificado por ahora)
            hero_position = self._determine_hero_position(screenshot)
            
            # Crear estado del juego
            game_state = GameState(
                hero_cards=hero_cards,
                board_cards=board_cards,
                pot_amount=pot_amount,
                hero_stack=hero_stack,
                villain_stack=50.0,  # Valor por defecto
                current_street=current_street,
                hero_position=hero_position,
                action_on_hero=action_available,
                min_raise=2.0,  # Valor por defecto
                max_raise=hero_stack,
                timestamp=datetime.now()
            )
            
            self.logger.info(f"Estado analizado: {current_street}, Hero: {hero_cards}, Board: {board_cards}")
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error analizando screenshot: {e}")
            return None
    
    def _determine_street(self, board_cards_count: int) -> str:
        """Determinar la calle basado en el número de cartas del board"""
        if board_cards_count == 0:
            return "preflop"
        elif board_cards_count == 3:
            return "flop"
        elif board_cards_count == 4:
            return "turn"
        elif board_cards_count == 5:
            return "river"
        else:
            return "unknown"
    
    def _detect_action_buttons(self, screenshot: np.ndarray) -> bool:
        """Detectar si hay botones de acción disponibles para el hero"""
        # Implementación básica - en realidad analizaría la región de botones
        return True  # Por defecto, asumir que es nuestro turno
    
    def _determine_hero_position(self, screenshot: np.ndarray) -> str:
        """Determinar la posición del hero en la mesa"""
        # Implementación simplificada - en realidad analizaría posiciones
        positions = ["SB", "BB", "UTG", "MP", "CO", "BTN"]
        return positions[2]  # Por defecto, asumir UTG
    
    def get_recommendation(self, game_state: GameState) -> Dict:
        """
        Generar recomendación basada en el estado del juego
        
        Args:
            game_state: Estado actual del juego
            
        Returns:
            Dict con recomendación y detalles
        """
        # Lógica básica de recomendación (se expandirá)
        recommendation = {
            "action": "CHECK/FOLD",
            "confidence": 0.7,
            "reason": "Implementación básica",
            "alternative_actions": ["FOLD", "CALL", "RAISE"],
            "optimal_bet_size": 0.0
        }
        
        # Lógica preflop básica
        if game_state.current_street == "preflop":
            if len(game_state.hero_cards) == 2:
                # Evaluar fuerza de mano preflop
                card1 = game_state.hero_cards[0]
                card2 = game_state.hero_cards[1]
                
                # Parejas altas
                if card1[0] == card2[0] and card1[0] in ['A', 'K', 'Q', 'J']:
                    recommendation["action"] = "RAISE"
                    recommendation["confidence"] = 0.85
                    recommendation["reason"] = "Pareja alta"
                    recommendation["optimal_bet_size"] = 2.2  # 2.2 BB
                
                # Cartas altas suited
                elif card1[1] == card2[1] and card1[0] in ['A', 'K']:
                    recommendation["action"] = "RAISE"
                    recommendation["confidence"] = 0.80
                    recommendation["reason"] = "Cartas altas suited"
                    recommendation["optimal_bet_size"] = 2.2
        
        self.logger.debug(f"Recomendación generada: {recommendation['action']}")
        return recommendation

# Función de utilidad para prueba rápida
def test_ggpoker_adapter():
    """Probar el adaptador de GG Poker"""
    print("🧪 Probando GGPokerAdapter...")
    
    try:
        adapter = GGPokerAdapter(stealth_level="MINIMUM")
        print("✅ Adaptador inicializado")
        
        # Crear screenshot de prueba
        test_screenshot = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        # Analizar
        game_state = adapter.analyze_screenshot(test_screenshot)
        
        if game_state:
            print(f"✅ Estado del juego analizado:")
            print(f"   Hero cards: {game_state.hero_cards}")
            print(f"   Board cards: {game_state.board_cards}")
            print(f"   Street: {game_state.current_street}")
            
            # Generar recomendación
            recommendation = adapter.get_recommendation(game_state)
            print(f"✅ Recomendación: {recommendation['action']}")
        else:
            print("⚠️  No se pudo analizar el estado del juego")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_ggpoker_adapter()