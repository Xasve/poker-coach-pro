# coach_integrator_minimal.py - Coach mínimo funcional
class CoachIntegrator:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        print(f"🤖 Coach mínimo para {platform}")
    
    def analyze_hand(self, situation):
        # Análisis básico
        hole_cards = situation.get("hole_cards", [])
        
        if hole_cards and len(hole_cards) >= 2:
            # Evaluación simple
            card1 = hole_cards[0][0] if isinstance(hole_cards[0], tuple) else "?"
            card2 = hole_cards[1][0] if isinstance(hole_cards[1], tuple) else "?"
            
            # AA, KK, QQ, AK -> RAISE
            if card1 == "A" and card2 == "A":
                return {"primary_action": "RAISE", "confidence": 0.95, "reasoning": "Pocket Aces"}
            elif card1 == "K" and card2 == "K":
                return {"primary_action": "RAISE", "confidence": 0.90, "reasoning": "Pocket Kings"}
            elif card1 == "A" and card2 == "K":
                return {"primary_action": "RAISE", "confidence": 0.85, "reasoning": "Big Slick"}
            else:
                return {"primary_action": "FOLD", "confidence": 0.70, "reasoning": "Mano marginal"}
        
        return {"primary_action": "CHECK", "confidence": 0.5, "reasoning": "Sin información"}
    
    def set_strategy(self, name):
        return True
    
    def get_available_strategies(self):
        return ["minimal"]
    
    def get_session_stats(self):
        return {"hands_analyzed": 0}
    
    def save_session(self, filename=None):
        return True
