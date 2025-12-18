"""
Adaptador simplificado para PokerStars - Versión mínima funcional
"""
import time
import logging
import random
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SimplePokerStarsAdapter:
    """Adaptador simplificado para pruebas"""
    
    def __init__(self, stealth_level: str = "MEDIUM"):
        self.stealth_level = stealth_level
        self.hand_history = []
        logger.info(f" SimplePokerStarsAdapter inicializado")
    
    def is_pokerstars_active(self) -> bool:
        """Verificar si PokerStars está activo (simulado)"""
        # Por ahora, siempre True para pruebas
        return True
    
    def capture_and_analyze(self) -> Optional[Dict[str, Any]]:
        """Simular captura y análisis"""
        try:
            # Simular estado de juego
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
            suits = ['h', 'd', 'c', 's']
            
            # Generar cartas aleatorias
            hero_cards = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(2)]
            
            # Determinar calle
            streets = ['preflop', 'flop', 'turn', 'river']
            street = random.choice(streets)
            
            # Cartas comunitarias según calle
            num_community = {'preflop': 0, 'flop': 3, 'turn': 4, 'river': 5}[street]
            community_cards = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(num_community)]
            
            # Generar estado
            state = {
                "hero_cards": hero_cards,
                "community_cards": community_cards,
                "street": street,
                "position": random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
                "pot": random.randint(100, 1000),
                "stack": random.randint(1000, 5000),
                "to_call": random.randint(0, 200),
                "min_raise": random.randint(50, 400),
                "max_raise": random.randint(500, 2000),
                "actions_available": random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
            }
            
            # Guardar en historial
            self.hand_history.append({
                "timestamp": time.time(),
                "state": state
            })
            
            logger.info(f"Estado simulado: {street} - Cartas: {hero_cards}")
            return state
            
        except Exception as e:
            logger.error(f"Error en captura simulada: {e}")
            return None
    
    def save_hand_history(self, game_state: Dict[str, Any], decision: Dict[str, Any]):
        """Guardar decisión en historial"""
        if self.hand_history:
            self.hand_history[-1]["decision"] = decision
            self.hand_history[-1]["decision_time"] = time.time()
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas"""
        return {
            "total_hands": len(self.hand_history),
            "platform": "PokerStars (Simulado)"
        }
