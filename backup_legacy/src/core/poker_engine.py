import random

class PokerEngine:
    def __init__(self, aggression=1.0, tightness=1.0):
        self.aggression = aggression
        self.tightness = tightness
        print(f"PokerEngine inicializado")
    
    def analyze_hand(self, hole_cards=None, community_cards=None, pot_size=0, position="middle"):
        print(f"Analizando: {hole_cards} vs {community_cards}, pot: {pot_size}, pos: {position}")
        
        # Lógica simple
        if hole_cards and len(hole_cards) >= 2:
            rank1 = hole_cards[0][0] if hole_cards[0] else '2'
            rank2 = hole_cards[1][0] if hole_cards[1] else '2'
            
            if rank1 == rank2:
                action = "RAISE"
                confidence = 0.8
                reason = "Pareja"
            elif rank1 in 'AKQJ' and rank2 in 'AKQJ':
                action = "CALL"
                confidence = 0.7
                reason = "Cartas altas"
            else:
                action = random.choice(["CHECK", "FOLD"])
                confidence = 0.5
                reason = "Mano promedio"
        else:
            action = "CHECK"
            confidence = 0.5
            reason = "Sin datos"
        
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand_strength": 0.5
        }
