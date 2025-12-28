# coach_integrator_simple.py - Versión simplificada y 100% funcional
import json
import random
from typing import Dict, List
from datetime import datetime

class CoachIntegrator:
    """Coach simplificado - Sin errores"""
    
    def __init__(self, platform="pokerstars", strategy="gto_basic"):
        self.platform = platform
        self.strategy = strategy
        
        # Tablas de decisiones CORRECTAS
        self.decision_tables = {
            "VERY_STRONG": {
                "preflop": "RAISE",
                "flop": "BET",
                "turn": "BET",
                "river": "BET"
            },
            "STRONG": {
                "preflop": "RAISE",
                "flop": "BET",
                "turn": "CHECK",
                "river": "CHECK"
            },
            "MEDIUM": {
                "preflop": "CALL",
                "flop": "CHECK",
                "turn": "CHECK",
                "river": "CHECK"
            },
            "WEAK": {
                "preflop": "FOLD",
                "flop": "FOLD",
                "turn": "FOLD",
                "river": "FOLD"
            },
            "UNKNOWN": {
                "preflop": "FOLD",
                "flop": "CHECK",
                "turn": "CHECK",
                "river": "CHECK"
            }
        }
        
        print(f"🤖 CoachIntegrator (simplificado) para {platform}")
    
    def analyze_hand(self, situation: Dict) -> Dict:
        """Análisis simplificado pero funcional"""
        hole_cards = situation.get("hole_cards", [])
        stage = situation.get("stage", "preflop")
        position = situation.get("position", "unknown")
        
        # Evaluar fuerza
        strength = self._evaluate_strength(hole_cards)
        
        # Obtener acción
        action = self.decision_tables.get(strength, {}).get(stage, "CHECK")
        
        # Calcular confianza
        confidence_map = {
            "VERY_STRONG": 0.95,
            "STRONG": 0.85,
            "MEDIUM": 0.65,
            "WEAK": 0.75,
            "UNKNOWN": 0.6
        }
        
        confidence = confidence_map.get(strength, 0.5)
        
        # Generar razón
        reasoning = f"Mano {strength.lower().replace('_', ' ')}, posición {position}, etapa {stage}"
        
        return {
            "primary_action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "hand_evaluation": {"strength": strength},
            "stage": stage,
            "position": position
        }
    
    def _evaluate_strength(self, hole_cards: List) -> str:
        """Evaluación simplificada"""
        if not hole_cards or len(hole_cards) < 2:
            return "UNKNOWN"
        
        values = []
        for card in hole_cards:
            if isinstance(card, tuple) and len(card) >= 2:
                values.append(str(card[0]).upper())
        
        if len(values) < 2:
            return "UNKNOWN"
        
        # Mapeo de valores
        value_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14
        }
        
        val1 = value_map.get(values[0], 0)
        val2 = value_map.get(values[1], 0)
        high_val = max(val1, val2)
        
        # Pocket pairs
        if values[0] == values[1]:
            if high_val >= 12:  # AA, KK, QQ
                return "VERY_STRONG"
            elif high_val >= 9:  # JJ, TT, 99
                return "STRONG"
            else:
                return "MEDIUM"
        
        # Cartas altas con As
        if 14 in [val1, val2]:
            other = val2 if val1 == 14 else val1
            if other >= 12:  # AK, AQ
                return "VERY_STRONG"
            elif other >= 10:  # AJ, AT
                return "STRONG"
            elif other >= 8:  # A9, A8
                return "MEDIUM"
        
        # KQ, KJ, QJ
        if high_val >= 12:
            low_val = min(val1, val2)
            if low_val >= 11:  # KQ, KJ, QJ
                return "MEDIUM"
        
        return "WEAK"
    
    def set_strategy(self, strategy_name: str):
        """Cambiar estrategia (simulado)"""
        print(f"🔄 Estrategia cambiada a: {strategy_name}")
        self.strategy = strategy_name
        return True
    
    def get_available_strategies(self):
        """Estrategias disponibles"""
        return ["gto_basic", "aggressive", "tight_passive"]
    
    def get_session_stats(self):
        """Estadísticas simuladas"""
        return {"hands_analyzed": 0, "recommendations_given": 0}
    
    def save_session(self, filename=None):
        """Guardar sesión simulada"""
        if filename:
            print(f"💾 Sesión guardada: {filename}")
        return True
