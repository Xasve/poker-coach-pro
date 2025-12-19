# src/integration/coach_integrator.py
import sys
import os
import json
import random
from typing import Dict, List, Tuple, Optional

class CoachIntegrator:
    """
    Sistema de integración del coach - Proporciona recomendaciones GTO
    """
    
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        self.strategy = "gto_basic"
        
        # Cargar configuraciones
        self.config = self._load_config()
        
        # Estrategias predefinidas
        self.strategies = self._initialize_strategies()
        
        print(f"🤖 CoachIntegrator inicializado para {platform}")
        print(f"📊 Estrategia: {self.strategy}")
    
    def _load_config(self) -> Dict:
        """Cargar configuración desde archivo"""
        config_path = "config/strategies.json"
        default_config = {
            "default_strategy": "gto_basic",
            "aggression_factor": 0.7,
            "risk_tolerance": 0.5,
            "bluff_frequency": 0.25,
            "min_confidence": 0.6
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
            except Exception as e:
                print(f"⚠️  No se pudo cargar configuración: {e}")
        
        return default_config
    
    def _initialize_strategies(self) -> Dict:
        """Inicializar estrategias de juego"""
        strategies = {
            "gto_basic": {
                "description": "Estrategia GTO básica equilibrada",
                "preflop_ranges": self._load_preflop_ranges(),
                "postflop_aggression": 0.6,
                "bluff_ratio": 0.3
            },
            "aggressive": {
                "description": "Estilo agresivo",
                "preflop_ranges": self._load_aggressive_ranges(),
                "postflop_aggression": 0.8,
                "bluff_ratio": 0.4
            },
            "tight": {
                "description": "Estilo conservador",
                "preflop_ranges": self._load_tight_ranges(),
                "postflop_aggression": 0.4,
                "bluff_ratio": 0.2
            }
        }
        
        return strategies
    
    def _load_preflop_ranges(self) -> Dict:
        """Rangos preflop básicos (simplificado)"""
        return {
            "UTG": ["AA", "KK", "QQ", "AKs", "AKo", "JJ"],
            "MP": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AKo", "AQs"],
            "CO": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AKo", "AQs", "AQo", "AJs"],
            "BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs", "KQs"],
            "SB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs"],
            "BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "AKs", "AKo", "AQs", "AQo", "AJs", "ATs", "KQs", "QJs"]
        }
    
    def _load_aggressive_ranges(self) -> Dict:
        """Rangos para estilo agresivo"""
        ranges = self._load_preflop_ranges()
        # Expandir rangos para ser más agresivo
        for position in ranges:
            ranges[position].extend(["77", "66", "55", "A9s", "KJs", "QTs"])
        return ranges
    
    def _load_tight_ranges(self) -> Dict:
        """Rangos para estilo conservador"""
        ranges = self._load_preflop_ranges()
        # Reducir rangos para ser más conservador
        for position in ranges:
            ranges[position] = [hand for hand in ranges[position] 
                               if hand in ["AA", "KK", "QQ", "AKs", "AKo"]]
        return ranges
    
    def analyze_hand(self, situation: Dict) -> Dict:
        """
        Analizar una situación de mano y dar recomendación
        
        Args:
            situation: Diccionario con información de la mano
        
        Returns:
            Dict: Recomendación con acción, confianza, etc.
        """
        print(f"🔍 Analizando situación...")
        
        # Extraer información de la situación
        hole_cards = situation.get("hole_cards", [])
        community_cards = situation.get("community_cards", [])
        pot_size = situation.get("pot_size", 0)
        position = situation.get("position", "unknown")
        stage = situation.get("stage", "preflop")
        
        # Convertir cartas a formato string para análisis
        hole_str = self._cards_to_string(hole_cards)
        community_str = self._cards_to_string(community_cards)
        
        print(f"   Cartas: {hole_str}")
        print(f"   Mesa: {community_str}")
        print(f"   Posición: {position}, Etapa: {stage}")
        
        # Determinar la acción recomendada
        recommendation = self._determine_action(
            hole_cards=hole_cards,
            community_cards=community_cards,
            position=position,
            stage=stage,
            pot_size=pot_size
        )
        
        return recommendation
    
    def _cards_to_string(self, cards: List) -> str:
        """Convertir lista de cartas a string legible"""
        if not cards:
            return "Ninguna"
        
        result = []
        for card in cards:
            if isinstance(card, tuple) and len(card) >= 2:
                value, suit = card[0], card[1]
                # Usar símbolos Unicode para palos
                suit_symbols = {
                    "hearts": "♥",
                    "diamonds": "♦",
                    "clubs": "♣",
                    "spades": "♠"
                }
                suit_symbol = suit_symbols.get(suit, suit[0].upper())
                result.append(f"{value}{suit_symbol}")
            elif isinstance(card, str):
                result.append(card)
        
        return ", ".join(result)
    
    def _determine_action(self, **kwargs) -> Dict:
        """Determinar la acción a tomar basada en la situación"""
        hole_cards = kwargs.get("hole_cards", [])
        stage = kwargs.get("stage", "preflop")
        position = kwargs.get("position", "unknown")
        
        # Evaluar fuerza de la mano
        hand_strength = self._evaluate_hand_strength(hole_cards, stage)
        
        # Determinar acción basada en fuerza y posición
        if stage == "preflop":
            action = self._preflop_decision(hand_strength, position)
        else:
            action = self._postflop_decision(hand_strength, stage)
        
        # Calcular confianza
        confidence = self._calculate_confidence(hand_strength, action)
        
        # Generar explicación
        reasoning = self._generate_reasoning(action, hand_strength, stage)
        
        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "hand_strength": hand_strength,
            "stage": stage,
            "position": position
        }
    
    def _evaluate_hand_strength(self, hole_cards: List, stage: str) -> str:
        """Evaluar la fuerza de la mano"""
        if not hole_cards or len(hole_cards) < 2:
            return "UNKNOWN"
        
        # Extraer valores y palos
        values = []
        suits = []
        
        for card in hole_cards:
            if isinstance(card, tuple) and len(card) >= 2:
                values.append(card[0])
                suits.append(card[1])
        
        if len(values) < 2:
            return "WEAK"
        
        # Evaluar pares
        if values[0] == values[1]:
            if values[0] in ["A", "K", "Q"]:
                return "VERY_STRONG"
            elif values[0] in ["J", "10", "9"]:
                return "STRONG"
            else:
                return "MEDIUM"
        
        # Evaluar conectores y suited
        value_ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, 
                      "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        
        val1 = value_ranks.get(values[0], 0)
        val2 = value_ranks.get(values[1], 0)
        
        # Cartas altas
        if val1 >= 10 and val2 >= 10:
            if suits[0] == suits[1]:
                return "STRONG"
            return "MEDIUM"
        
        # Suited connectors
        if suits[0] == suits[1] and abs(val1 - val2) <= 2:
            return "MEDIUM"
        
        return "WEAK"
    
    def _preflop_decision(self, hand_strength: str, position: str) -> str:
        """Tomar decisión preflop"""
        strength_map = {
            "VERY_STRONG": ["RAISE", "RAISE", "ALL_IN", "RAISE"],
            "STRONG": ["RAISE", "RAISE", "CALL", "RAISE"],
            "MEDIUM": ["CALL", "FOLD", "FOLD", "CALL"],
            "WEAK": ["FOLD", "FOLD", "FOLD", "FOLD"],
            "UNKNOWN": ["FOLD", "FOLD", "FOLD", "FOLD"]
        }
        
        # Mapear posición a índice
        position_index = {"UTG": 0, "MP": 1, "CO": 2, "BTN": 3, "SB": 2, "BB": 3}
        idx = position_index.get(position, 1)
        
        actions = strength_map.get(hand_strength, ["FOLD", "FOLD", "FOLD", "FOLD"])
        
        return actions[min(idx, len(actions)-1)]
    
    def _postflop_decision(self, hand_strength: str, stage: str) -> str:
        """Tomar decisión postflop"""
        if hand_strength in ["VERY_STRONG", "STRONG"]:
            return "RAISE"
        elif hand_strength == "MEDIUM":
            return "CALL" if stage == "flop" else "CHECK"
        else:
            return "FOLD" if random.random() > 0.3 else "CHECK"
    
    def _calculate_confidence(self, hand_strength: str, action: str) -> float:
        """Calcular nivel de confianza para la recomendación"""
        confidence_map = {
            ("VERY_STRONG", "RAISE"): 0.95,
            ("VERY_STRONG", "ALL_IN"): 0.90,
            ("STRONG", "RAISE"): 0.85,
            ("STRONG", "CALL"): 0.80,
            ("MEDIUM", "CALL"): 0.70,
            ("MEDIUM", "CHECK"): 0.65,
            ("WEAK", "FOLD"): 0.75,
            ("UNKNOWN", "FOLD"): 0.60
        }
        
        return confidence_map.get((hand_strength, action), 0.5)
    
    def _generate_reasoning(self, action: str, hand_strength: str, stage: str) -> str:
        """Generar explicación para la recomendación"""
        reasoning_map = {
            "RAISE": f"Mano {hand_strength.lower().replace('_', ' ')}, construir bote",
            "CALL": f"Mano {hand_strength.lower().replace('_', ' ')}, ver siguiente carta",
            "CHECK": f"Mano {hand_strength.lower().replace('_', ' ')}, controlar bote",
            "FOLD": f"Mano {hand_strength.lower().replace('_', ' ')}, evitar pérdidas",
            "ALL_IN": f"Mano {hand_strength.lower().replace('_', ' ')}, máxima presión"
        }
        
        return reasoning_map.get(action, "Análisis básico de situación")
    
    def set_strategy(self, strategy_name: str):
        """Cambiar estrategia de juego"""
        if strategy_name in self.strategies:
            self.strategy = strategy_name
            print(f"🔄 Estrategia cambiada a: {strategy_name}")
            print(f"   {self.strategies[strategy_name]['description']}")
        else:
            print(f"⚠️  Estrategia '{strategy_name}' no encontrada")
    
    def get_available_strategies(self) -> List[str]:
        """Obtener lista de estrategias disponibles"""
        return list(self.strategies.keys())

# Para uso independiente
if __name__ == "__main__":
    coach = CoachIntegrator("pokerstars")
    
    # Probar con situación de ejemplo
    test_situation = {
        "hole_cards": [("A", "hearts"), ("K", "spades")],
        "community_cards": [("10", "diamonds"), ("J", "clubs"), ("Q", "hearts")],
        "pot_size": 150,
        "position": "BTN",
        "stage": "flop"
    }
    
    print("\n🧪 PROBANDO COACH CON SITUACIÓN DE EJEMPLO:")
    recommendation = coach.analyze_hand(test_situation)
    
    print(f"\n🎯 RECOMENDACIÓN:")
    for key, value in recommendation.items():
        print(f"   {key}: {value}")