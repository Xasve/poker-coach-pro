"""
PokerStars Adapter Modificado - No requiere screen_capture
"""
import time
import logging
import random
from typing import Optional, Dict, Any
from dataclasses import dataclass

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

class PokerStarsAdapterNoCapture:
    """Adaptador que NO depende de screen_capture"""
    
    def __init__(self, stealth_level: str = "MEDIUM"):
        self.logger = logging.getLogger(__name__)
        self.stealth_level = stealth_level
        self.hand_history = []
        self.current_hand_id = None
        
        self.logger.info(f" PokerStarsAdapterNoCapture inicializado")
    
    def is_pokerstars_active(self) -> bool:
        """Siempre devuelve True para pruebas"""
        # En una versión real, aquí iría la detección de la ventana de PokerStars
        return True  # Cambiar a False para forzar modo demo
    
    def capture_and_analyze(self) -> Optional[PokerStarsGameState]:
        """Simula captura para desarrollo"""
        try:
            self.logger.debug("Simulando captura de mesa...")
            
            # Simular un retardo de captura real
            time.sleep(0.1)
            
            # Generar datos simulados REALISTAS
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
            suits = ['h', 'd', 'c', 's']
            
            # Cartas del héroe (simuladas)
            hero_cards = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(2)]
            
            # Determinar calle
            streets = ['preflop', 'flop', 'turn', 'river']
            street = random.choice(streets)
            
            # Cartas comunitarias según calle
            num_community = {'preflop': 0, 'flop': 3, 'turn': 4, 'river': 5}[street]
            community_cards = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(num_community)]
            
            # Generar estado del juego SIMULADO pero realista
            game_state = PokerStarsGameState(
                hero_cards=hero_cards,
                community_cards=community_cards,
                street=street,
                position=random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
                pot=random.randint(100, 1000),
                stack=random.randint(1000, 5000),
                to_call=random.randint(0, 200),
                min_raise=random.randint(50, 400),
                max_raise=random.randint(500, 2000),
                actions_available=random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
            )
            
            # Guardar en historial
            hand_data = {
                "timestamp": time.time(),
                "hand_id": f"hand_{int(time.time())}",
                "state": game_state.to_dict()
            }
            self.hand_history.append(hand_data)
            
            # Mantener solo las últimas 100 manos
            if len(self.hand_history) > 100:
                self.hand_history = self.hand_history[-100:]
            
            self.logger.info(f"Estado simulado: {street} - Cartas: {hero_cards}")
            return game_state
            
        except Exception as e:
            self.logger.error(f"Error en simulación: {e}")
            return None
    
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
            "platform": "PokerStars (Simulado)"
        }
