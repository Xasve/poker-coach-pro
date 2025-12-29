"""
SUGERIDOR DE ACCIONES BASADO EN GTO
Analiza situación y sugiere mejor acción
"""

import random
from datetime import datetime

class ActionSuggester:
    """Sugiere acciones basadas en GTO y situación actual"""
    
    def __init__(self):
        self.position_weights = {
            "BTN": 1.2,  # Button tiene ventaja
            "CO": 1.1,   # Cutoff
            "MP": 1.0,   # Middle Position
            "EP": 0.9,   # Early Position
            "BB": 0.8,   # Big Blind
            "SB": 0.7    # Small Blind
        }
        
        # Rangos GTO simplificados
        self.preflop_ranges = self.load_preflop_ranges()
        
    def load_preflop_ranges(self):
        """Cargar rangos GTO preflop simplificados"""
        # Rangos basados en posición (simplificados)
        return {
            "EP": ["AA", "KK", "QQ", "AKs", "AKo", "JJ", "TT", "AQs"],
            "MP": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AKo", "AQs", "AQo", "AJs"],
            "CO": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs", "KQs"],
            "BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs", "A9s", 
                   "KQs", "KQo", "KJs", "QJs", "JTs", "T9s", "98s"],
            "SB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AKs", "AKo", "AQs", "AQo"],
            "BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs"]
        }
    
    def analyze_situation(self, hero_cards, board_cards, game_state):
        """Analizar situación completa"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "hero_cards": hero_cards,
            "board_cards": board_cards,
            "game_state": game_state,
            "hand_strength": self.evaluate_hand_strength(hero_cards, board_cards),
            "position_factor": self.get_position_factor(game_state),
            "action_required": game_state.get("is_our_turn", False),
            "available_actions": game_state.get("available_actions", [])
        }
        
        return analysis
    
    def evaluate_hand_strength(self, hero_cards, board_cards):
        """Evaluar fuerza de mano (simplificado)"""
        if hero_cards == ["??", "??"]:
            return 0.5  # Valor medio por defecto
        
        # Clasificación básica de manos
        card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        
        # Convertir cartas a valores
        values = []
        for card in hero_cards:
            if card == "??":
                continue
            rank = card[:-1] if len(card) > 1 else card
            value = card_values.get(rank, int(rank) if rank.isdigit() else 0)
            values.append(value)
        
        if len(values) < 2:
            return 0.5
        
        # Evaluar fuerza básica
        card1, card2 = values[0], values[1]
        
        # Pares altos
        if card1 == card2:
            if card1 >= 10:  # JJ+
                return 0.9
            elif card1 >= 7:  # 77-TT
                return 0.7
            else:  # 22-66
                return 0.5
        
        # Cartas altas conectadas
        if max(card1, card2) >= 12:  # Q+
            diff = abs(card1 - card2)
            if diff <= 1:  # Conectadas
                return 0.8
            elif diff <= 3:  # Semi-conectadas
                return 0.6
            else:
                return 0.4
        
        return 0.3  # Manos marginales
    
    def get_position_factor(self, game_state):
        """Factor basado en posición (simplificado)"""
        # Por ahora, posición fija
        # EN PRÓXIMAS ITERACIONES: detectar posición real
        return self.position_weights.get("MP", 1.0)
    
    def suggest_action(self, analysis):
        """Sugerir acción basada en análisis"""
        if not analysis.get("action_required", False):
            return {
                "action": "WAIT",
                "confidence": 1.0,
                "reasoning": "No es nuestro turno"
            }
        
        hand_strength = analysis.get("hand_strength", 0.5)
        position_factor = analysis.get("position_factor", 1.0)
        available_actions = analysis.get("available_actions", [])
        
        # Ajustar por posición
        adjusted_strength = hand_strength * position_factor
        
        # Decisiones basadas en fuerza ajustada
        if "FOLD" in available_actions and adjusted_strength < 0.3:
            action = "FOLD"
            confidence = 0.9
            reasoning = "Mano muy débil para continuar"
        
        elif adjusted_strength < 0.5:
            if "CHECK" in available_actions:
                action = "CHECK"
                confidence = 0.7
                reasoning = "Mano marginal, ver el siguiente street gratis"
            elif "CALL" in available_actions:
                action = "CALL"
                confidence = 0.6
                reasoning = "Mano jugable con odds adecuadas"
            else:
                action = "FOLD"
                confidence = 0.8
                reasoning = "Mano débil sin opción de check"
        
        elif adjusted_strength < 0.7:
            if "BET" in available_actions or "RAISE" in available_actions:
                action = "BET" if "BET" in available_actions else "RAISE"
                confidence = 0.75
                reasoning = "Mano buena para construir el bote"
            elif "CHECK" in available_actions:
                action = "CHECK"
                confidence = 0.65
                reasoning = "Mano decente, puede atraer apuestas"
            else:
                action = "CALL"
                confidence = 0.7
                reasoning = "Mano jugable, ver siguiente carta"
        
        else:  # adjusted_strength >= 0.7
            if "RAISE" in available_actions:
                action = "RAISE"
                confidence = 0.85
                reasoning = "Mano muy fuerte, maximizar valor"
                bet_size = self.calculate_bet_size(hand_strength)
            elif "BET" in available_actions:
                action = "BET"
                confidence = 0.8
                reasoning = "Mano fuerte, sacar valor"
                bet_size = self.calculate_bet_size(hand_strength)
            else:
                action = "CALL" if "CALL" in available_actions else "CHECK"
                confidence = 0.75
                reasoning = "Mano fuerte pero limitada por acciones disponibles"
        
        suggestion = {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "hand_strength": hand_strength,
            "adjusted_strength": adjusted_strength
        }
        
        if 'bet_size' in locals():
            suggestion["bet_size"] = bet_size
        
        return suggestion
    
    def calculate_bet_size(self, hand_strength):
        """Calcular tamaño de apuesta basado en fuerza de mano"""
        if hand_strength > 0.9:
            return "75-100% del bote"  # Valor máximo
        elif hand_strength > 0.7:
            return "50-75% del bote"   # Valor estándar
        elif hand_strength > 0.5:
            return "33-50% del bote"   # Valor/extracción
        else:
            return "25-33% del bote"   # Apuesta pequeña/bluff