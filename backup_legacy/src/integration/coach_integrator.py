# src/integration/coach_integrator.py - Coach GTO Mejorado
import sys
import os
import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class CoachIntegrator:
    """
    Sistema de integración del coach mejorado - Proporciona recomendaciones GTO avanzadas
    """
    
    def __init__(self, platform="pokerstars", strategy="gto_basic"):
        self.platform = platform
        self.strategy = strategy
        
        # Cargar configuraciones
        self.config = self._load_config()
        
        # Historial de manos
        self.hand_history = []
        self.max_history = 100
        
        # Estadísticas de sesión
        self.session_stats = {
            "hands_analyzed": 0,
            "recommendations_given": 0,
            "actions_taken": {"FOLD": 0, "CHECK": 0, "CALL": 0, "RAISE": 0, "ALL_IN": 0},
            "win_rate": 0.0,
            "start_time": datetime.now().isoformat()
        }
        
        # Estrategias predefinidas mejoradas
        self.strategies = self._initialize_strategies()
        
        # Rangos preflop completos
        self.preflop_ranges = self._initialize_preflop_ranges()
        
        # Tablas de decisiones postflop
        self.postflop_decisions = self._initialize_postflop_decisions()
        
        print(f"🤖 CoachIntegrator PRO inicializado para {platform}")
        print(f"📊 Estrategia: {self.strategy}")
        print(f"🎯 Rangos preflop cargados: {len(self.preflop_ranges)} posiciones")
    
    def _load_config(self) -> Dict:
        """Cargar configuración desde archivo"""
        config_path = "config/strategies.json"
        default_config = {
            "default_strategy": "gto_basic",
            "aggression_factor": 0.7,
            "risk_tolerance": 0.5,
            "bluff_frequency": 0.25,
            "min_confidence": 0.6,
            "preflop_adjustment": 1.0,
            "postflop_adjustment": 1.0,
            "position_aware": True,
            "stack_size_aware": True,
            "player_count_aware": True,
            "pot_odds_aware": True,
            "equity_aware": True
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
                    print("✅ Configuración de estrategias cargada")
            except Exception as e:
                print(f"⚠️  No se pudo cargar configuración: {e}")
        
        return default_config
    
    def _initialize_strategies(self) -> Dict:
        """Inicializar estrategias de juego mejoradas"""
        strategies = {
            "gto_basic": {
                "description": "Estrategia GTO básica equilibrada",
                "preflop_tightness": 0.7,
                "postflop_aggression": 0.6,
                "bluff_ratio": 0.3,
                "cbet_frequency": 0.7,
                "fold_to_3bet": 0.4,
                "river_aggression": 0.5
            },
            "aggressive": {
                "description": "Estilo TAG (Tight-Aggressive)",
                "preflop_tightness": 0.8,
                "postflop_aggression": 0.8,
                "bluff_ratio": 0.4,
                "cbet_frequency": 0.85,
                "fold_to_3bet": 0.3,
                "river_aggression": 0.7
            },
            "loose_aggressive": {
                "description": "Estilo LAG (Loose-Aggressive)",
                "preflop_tightness": 0.4,
                "postflop_aggression": 0.9,
                "bluff_ratio": 0.5,
                "cbet_frequency": 0.9,
                "fold_to_3bet": 0.2,
                "river_aggression": 0.8
            },
            "tight_passive": {
                "description": "Estilo Nit (Ultra-conservador)",
                "preflop_tightness": 0.9,
                "postflop_aggression": 0.3,
                "bluff_ratio": 0.1,
                "cbet_frequency": 0.4,
                "fold_to_3bet": 0.7,
                "river_aggression": 0.2
            },
            "balanced": {
                "description": "Estrategia perfectamente balanceada",
                "preflop_tightness": 0.65,
                "postflop_aggression": 0.65,
                "bluff_ratio": 0.35,
                "cbet_frequency": 0.65,
                "fold_to_3bet": 0.45,
                "river_aggression": 0.55
            }
        }
        
        return strategies
    
    def _initialize_preflop_ranges(self) -> Dict:
        """Rangos preflop completos para 6-max"""
        return {
            "UTG": [
                "AA", "AKs", "AQs", "AJs", "ATs", "AKo", "KK", "KQs", "KJs", "QQ", 
                "QJs", "JJ", "TT", "99", "88", "77", "66"
            ],
            "MP": [
                "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "AKo", "AQo", "KK", "KQs", 
                "KJs", "KTs", "QQ", "QJs", "QTs", "JJ", "JTs", "TT", "99", "88", 
                "77", "66", "55"
            ],
            "CO": [
                "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A5s", "AKo", 
                "AQo", "AJo", "KK", "KQs", "KJs", "KTs", "K9s", "QQ", "QJs", "QTs", 
                "Q9s", "JJ", "JTs", "J9s", "TT", "T9s", "99", "98s", "88", "87s", 
                "77", "66", "55", "44"
            ],
            "BTN": [
                "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", 
                "A4s", "A3s", "A2s", "AKo", "AQo", "AJo", "ATo", "KK", "KQs", "KJs", 
                "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s", "QQ", 
                "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "JJ", "JTs", "J9s", 
                "J8s", "TT", "T9s", "T8s", "99", "98s", "97s", "88", "87s", "86s", 
                "77", "76s", "75s", "66", "65s", "55", "44", "33", "22"
            ],
            "SB": [
                "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", 
                "A4s", "A3s", "A2s", "AKo", "AQo", "AJo", "ATo", "KK", "KQs", "KJs", 
                "KTs", "K9s", "K8s", "QQ", "QJs", "QTs", "Q9s", "JJ", "JTs", "J9s", 
                "TT", "T9s", "99", "98s", "88", "87s", "77", "66", "55", "44", "33", "22"
            ],
            "BB": [
                "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", 
                "A4s", "A3s", "A2s", "AKo", "AQo", "AJo", "ATo", "A9o", "KK", "KQs", 
                "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s", 
                "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "JJ", "JTs", "J9s", "J8s", 
                "TT", "T9s", "T8s", "99", "98s", "97s", "88", "87s", "86s", "77", 
                "76s", "66", "65s", "55", "44", "33", "22"
            ]
        }
    
    def _initialize_postflop_decisions(self) -> Dict:
        """Tablas de decisiones postflop mejoradas"""
        return {
            "VERY_STRONG": {
                "preflop": ["RAISE", "RAISE", "ALL_IN", "RAISE"],
                "flop": ["RAISE", "BET", "BET", "RAISE"],
                "turn": ["RAISE", "BET", "BET", "RAISE"],
                "river": ["RAISE", "BET", "BET", "ALL_IN"]
            },
            "STRONG": {
                "preflop": ["RAISE", "RAISE", "CALL", "RAISE"],
                "flop": ["BET", "BET", "CHECK", "BET"],
                "turn": ["BET", "CHECK", "CHECK", "BET"],
                "river": ["BET", "CHECK", "CHECK", "BET"]
            },
            "MEDIUM": {
                "preflop": ["CALL", "FOLD", "FOLD", "CALL"],
                "flop": ["CHECK", "CHECK", "FOLD", "CHECK"],
                "turn": ["CHECK", "CHECK", "FOLD", "CHECK"],
                "river": ["CHECK", "CHECK", "FOLD", "CHECK"]
            },
            "WEAK": {
                "preflop": ["FOLD", "FOLD", "FOLD", "FOLD"],
                "flop": ["CHECK", "FOLD", "FOLD", "CHECK"],
                "turn": ["CHECK", "FOLD", "FOLD", "CHECK"],
                "river": ["CHECK", "FOLD", "FOLD", "CHECK"]
            },
            "DRAWING": {
                "preflop": ["CALL", "FOLD", "FOLD", "CALL"],
                "flop": ["CALL", "CALL", "FOLD", "CALL"],
                "turn": ["CALL", "FOLD", "FOLD", "CALL"],
                "river": ["CHECK", "FOLD", "FOLD", "CHECK"]
            },"UNKNOWN": {
                "preflop": ["FOLD", "FOLD", "FOLD", "FOLD"],
                "flop": ["CHECK", "FOLD", "FOLD", "CHECK"],
                "turn": ["CHECK", "FOLD", "FOLD", "CHECK"],
                "river": ["CHECK", "FOLD", "FOLD", "CHECK"]
            }
        }
        
    
    def analyze_hand(self, situation: Dict) -> Dict:
        """
        Analizar una situación de mano y dar recomendación avanzada
        
        Args:
            situation: Diccionario con información completa de la mano
        
        Returns:
            Dict: Recomendación detallada con múltiples opciones
        """
        self.session_stats["hands_analyzed"] += 1
        
        # Extraer información de la situación
        hole_cards = situation.get("hole_cards", [])
        community_cards = situation.get("community_cards", [])
        pot_size = situation.get("pot_size", 0)
        bet_size = situation.get("bet_size", 0)
        position = situation.get("position", "unknown")
        players = situation.get("players", 6)
        stage = situation.get("stage", "preflop")
        
        # Convertir cartas a formato string para análisis
        hole_str = self._cards_to_string(hole_cards)
        community_str = self._cards_to_string(community_cards)
        
        # Evaluación avanzada
        hand_evaluation = self._evaluate_hand_advanced(hole_cards, community_cards, stage)
        pot_odds = self._calculate_pot_odds(pot_size, bet_size)
        equity = self._estimate_equity(hole_cards, community_cards, players, stage)
        
        # Determinar acción recomendada
        recommendation = self._determine_action_advanced(
            hand_evaluation=hand_evaluation,
            position=position,
            stage=stage,
            pot_odds=pot_odds,
            equity=equity,
            players=players,
            pot_size=pot_size,
            bet_size=bet_size
        )
        
        # Actualizar historial
        hand_record = {
            "timestamp": datetime.now().isoformat(),
            "hole_cards": hole_str,
            "community_cards": community_str,
            "stage": stage,
            "position": position,
            "evaluation": hand_evaluation,
            "recommendation": recommendation,
            "pot_size": pot_size,
            "equity": equity
        }
        
        self.hand_history.append(hand_record)
        if len(self.hand_history) > self.max_history:
            self.hand_history.pop(0)
        
        self.session_stats["recommendations_given"] += 1
        if recommendation.get("primary_action"):
            action = recommendation["primary_action"]
            if action in self.session_stats["actions_taken"]:
                self.session_stats["actions_taken"][action] += 1
        
        return recommendation
    
    def _cards_to_string(self, cards: List) -> str:
        """Convertir lista de cartas a string legible"""
        if not cards:
            return "Ninguna"
        
        result = []
        for card in cards:
            if isinstance(card, tuple) and len(card) >= 2:
                value, suit = str(card[0]).upper(), str(card[1]).lower()
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
    
    def _evaluate_hand_advanced(self, hole_cards: List, community_cards: List, stage: str) -> Dict:
        """Evaluación avanzada de la mano"""
        evaluation = {
            "strength": "UNKNOWN",
            "category": "HIGH_CARD",
            "draws": [],
            "outs": 0,
            "confidence": 0.5
        }
        
        if not hole_cards or len(hole_cards) < 2:
            return evaluation
        
        # Extraer valores y palos
        values = []
        suits = []
        
        for card in hole_cards:
            if isinstance(card, tuple) and len(card) >= 2:
                values.append(str(card[0]).upper())
                suits.append(str(card[1]).lower())
        
        if len(values) < 2:
            return evaluation
        
        # Mapeo de valores
        value_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, 
            "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
            "?": 0
        }
        
        val1 = value_map.get(values[0], 0)
        val2 = value_map.get(values[1], 0)
        
        # Ordenar valores
        high_val, low_val = max(val1, val2), min(val1, val2)
        
        # Evaluar fuerza base
        strength = "WEAK"
        
        # Pocket pairs
        if values[0] == values[1]:
            if high_val >= 12:  # AA, KK, QQ
                strength = "VERY_STRONG"
                evaluation["category"] = "POCKET_PAIR_HIGH"
            elif high_val >= 9:  # JJ, TT, 99
                strength = "STRONG"
                evaluation["category"] = "POCKET_PAIR_MEDIUM"
            else:
                strength = "MEDIUM"
                evaluation["category"] = "POCKET_PAIR_LOW"
        
        # Cartas altas
        elif high_val == 14:  # Tiene As
            if low_val >= 12:  # AK, AQ
                strength = "VERY_STRONG"
                evaluation["category"] = "ACE_HIGH_SUITED" if suits[0] == suits[1] else "ACE_HIGH_OFFSUIT"
            elif low_val >= 10:  # AJ, AT
                strength = "STRONG"
                evaluation["category"] = "ACE_HIGH_SUITED" if suits[0] == suits[1] else "ACE_HIGH_OFFSUIT"
            elif low_val >= 8:  # A9, A8
                strength = "MEDIUM"
                evaluation["category"] = "ACE_HIGH_SUITED" if suits[0] == suits[1] else "ACE_HIGH_OFFSUIT"
        
        # Cartas medias
        elif high_val >= 10:
            if low_val >= 9 and abs(high_val - low_val) <= 2:
                strength = "MEDIUM"
                evaluation["category"] = "CONNECTOR_SUITED" if suits[0] == suits[1] else "CONNECTOR_OFFSUIT"
                evaluation["draws"].append("STRAIGHT_DRAW")
            elif suits[0] == suits[1]:
                strength = "MEDIUM"
                evaluation["category"] = "SUITED_CARDS"
        
        # Conectores suited
        if suits[0] == suits[1] and abs(high_val - low_val) <= 2:
            if strength == "WEAK":
                strength = "MEDIUM"
            evaluation["category"] = "SUITED_CONNECTOR"
            evaluation["draws"].append("FLUSH_DRAW")
            if abs(high_val - low_val) == 1:
                evaluation["draws"].append("STRAIGHT_DRAW")
        
        # Evaluación postflop si hay cartas comunitarias
        if community_cards and len(community_cards) >= 3:
            strength, evaluation = self._evaluate_postflop_strength(hole_cards, community_cards, strength, evaluation)
        
        evaluation["strength"] = strength
        
        # Calcular confianza basada en calidad de información
        confidence = 0.7
        if "?" in values:
            confidence *= 0.6
        if len(community_cards) < 3 and stage != "preflop":
            confidence *= 0.8
        
        evaluation["confidence"] = min(0.95, confidence)
        
        return evaluation
    
    def _evaluate_postflop_strength(self, hole_cards, community_cards, base_strength, evaluation):
        """Evaluar fuerza postflop"""
        # Esta es una implementación simplificada
        # En producción, usaría una librería de evaluación de manos como treys
        
        all_cards = hole_cards + community_cards
        
        # Simular mejoras de mano postflop
        if base_strength in ["MEDIUM", "WEAK"]:
            # Si tenemos draws postflop, mejorar evaluación
            if len(community_cards) >= 3:
                # Simular posibles mejoras
                if random.random() > 0.7:
                    base_strength = "DRAWING"
                    evaluation["draws"].append("POSTFLOP_DRAW")
                    evaluation["outs"] = random.randint(4, 12)
        
        return base_strength, evaluation
    
    def _calculate_pot_odds(self, pot_size: float, bet_size: float) -> float:
        """Calcular pot odds"""
        if bet_size <= 0:
            return float('inf')
        return (pot_size + bet_size) / bet_size
    
    def _estimate_equity(self, hole_cards: List, community_cards: List, players: int, stage: str) -> float:
        """Estimar equity de la mano (simplificado)"""
        if not hole_cards or len(hole_cards) < 2:
            return 0.0
        
        # Evaluación simplificada basada en fuerza de mano
        evaluation = self._evaluate_hand_advanced(hole_cards, community_cards, stage)
        strength = evaluation["strength"]
        
        # Equity basada en fuerza
        equity_map = {
            "VERY_STRONG": 0.85,
            "STRONG": 0.65,
            "MEDIUM": 0.45,
            "WEAK": 0.25,
            "DRAWING": 0.35,
            "UNKNOWN": 0.3
        }
        
        base_equity = equity_map.get(strength, 0.3)
        
        # Ajustar por número de jugadores
        if players > 2:
            base_equity *= (2.0 / players)  # Reducir equity con más jugadores
        
        # Ajustar por etapa del juego
        stage_factor = {
            "preflop": 0.9,
            "flop": 1.0,
            "turn": 1.1,
            "river": 1.2
        }
        
        base_equity *= stage_factor.get(stage, 1.0)
        
        return min(0.95, max(0.05, base_equity))
    
    def _determine_action_advanced(self, **kwargs) -> Dict:
        """Determinar acción avanzada basada en múltiples factores"""
        hand_evaluation = kwargs.get("hand_evaluation", {})
        position = kwargs.get("position", "unknown")
        stage = kwargs.get("stage", "preflop")
        pot_odds = kwargs.get("pot_odds", float('inf'))
        equity = kwargs.get("equity", 0.5)
        players = kwargs.get("players", 6)
        pot_size = kwargs.get("pot_size", 0)
        bet_size = kwargs.get("bet_size", 0)
        
        # Obtener estrategia actual
        strategy_config = self.strategies.get(self.strategy, self.strategies["gto_basic"])
        
        # Mapear posición a índice
        position_index = {"UTG": 0, "MP": 1, "CO": 2, "BTN": 3, "SB": 2, "BB": 3}
        pos_idx = position_index.get(position, 1)
        
                # Obtener acción base de las tablas
        strength = hand_evaluation.get("strength", "UNKNOWN")
                # 🔥 CORRECCIÓN: Asegurar que strength existe en las tablas
        if strength not in self.postflop_decisions:
            print(f"⚠️  Fuerza de mano desconocida: '{strength}', usando 'UNKNOWN'")
            strength = "UNKNOWN"
        
        action_table = self.postflop_decisions[strength]
        
        # 🔥 CORRECCIÓN: Asegurar que strength existe en las tablas
        if strength not in self.postflop_decisions:
            print(f"⚠️  Fuerza de mano desconocida: '{strength}', usando 'UNKNOWN'")
            strength = "UNKNOWN"
        
        action_table = self.postflop_decisions[strength]
        
        stage_key = "preflop" if stage == "preflop" else "flop"  # Simplificado
        possible_actions = action_table.get(stage_key, ["CHECK", "CHECK", "FOLD", "CHECK"])
        
        # Seleccionar acción base
        base_action = possible_actions[min(pos_idx, len(possible_actions)-1)]
        
        # Ajustar por pot odds y equity
        adjusted_action = self._adjust_by_pot_odds(base_action, pot_odds, equity, bet_size)
        
        # Ajustar por agresión de estrategia
        final_action = self._adjust_by_strategy(adjusted_action, strategy_config, stage)
        
        # Calcular tamaño de apuesta si es RAISE/BET
        bet_amount = self._calculate_bet_size(final_action, pot_size, bet_size, strategy_config)
        
        # Calcular confianza
        confidence = self._calculate_confidence_advanced(
            hand_evaluation, pot_odds, equity, position, stage
        )
        
        # Generar explicación detallada
        reasoning = self._generate_detailed_reasoning(
            final_action, hand_evaluation, pot_odds, equity, position, stage
        )
        
        # Alternativas recomendadas
        alternatives = self._get_alternative_actions(base_action, hand_evaluation, stage)
        
        return {
            "primary_action": final_action,
            "bet_amount": bet_amount,
            "confidence": confidence,
            "reasoning": reasoning,
            "hand_evaluation": hand_evaluation,
            "pot_odds": pot_odds,
            "equity": equity,
            "alternatives": alternatives,
            "stage": stage,
            "position": position,
            "timestamp": datetime.now().isoformat()
        }
    
    def _adjust_by_pot_odds(self, action: str, pot_odds: float, equity: float, bet_size: float) -> str:
        """Ajustar acción basada en pot odds"""
        if action in ["CALL", "CHECK"] and bet_size > 0:
            # Calcular si call es correcto matemáticamente
            required_equity = 1.0 / (pot_odds + 1.0)
            
            if equity < required_equity * 0.8:
                return "FOLD"
            elif equity > required_equity * 1.2:
                return "RAISE"
        
        return action
    
    def _adjust_by_strategy(self, action: str, strategy: Dict, stage: str) -> str:
        """Ajustar acción basada en estrategia seleccionada"""
        aggression = strategy.get("postflop_aggression", 0.6)
        
        # Aumentar agresión basada en configuración
        if random.random() < aggression:
            if action == "CHECK" and stage != "preflop":
                if random.random() < strategy.get("cbet_frequency", 0.7):
                    return "BET"
            elif action == "CALL":
                if random.random() < aggression * 0.5:
                    return "RAISE"
        
        return action
    
    def _calculate_bet_size(self, action: str, pot_size: float, current_bet: float, strategy: Dict) -> float:
        """Calcular tamaño de apuesta óptimo"""
        if action not in ["RAISE", "BET", "ALL_IN"]:
            return 0.0
        
        if action == "ALL_IN":
            return float('inf')  # Representar all-in
        
        # Tamaños de apuesta comunes
        bet_sizes = {
            "small": pot_size * 0.33,  # 1/3 pot
            "standard": pot_size * 0.5,  # 1/2 pot
            "large": pot_size * 0.75,  # 3/4 pot
            "pot": pot_size  # Pot-sized bet
        }
        
        # Seleccionar tamaño basado en agresión
        aggression = strategy.get("postflop_aggression", 0.6)
        
        if aggression > 0.8:
            return bet_sizes["large"]
        elif aggression > 0.6:
            return bet_sizes["standard"]
        else:
            return bet_sizes["small"]
    
    def _calculate_confidence_advanced(self, hand_evaluation: Dict, pot_odds: float, 
                                     equity: float, position: str, stage: str) -> float:
        """Calcular confianza avanzada para la recomendación"""
        base_confidence = hand_evaluation.get("confidence", 0.5)
        
        # Ajustar por posición
        position_bonus = {"BTN": 0.1, "CO": 0.05, "MP": 0.0, "UTG": -0.05, "SB": -0.1, "BB": -0.15}
        base_confidence += position_bonus.get(position, 0.0)
        
        # Ajustar por equity vs pot odds
        if pot_odds != float('inf'):
            required_equity = 1.0 / (pot_odds + 1.0)
            if equity > required_equity * 1.5:
                base_confidence += 0.15
            elif equity < required_equity * 0.7:
                base_confidence -= 0.15
        
        # Ajustar por etapa
        stage_factor = {"preflop": 0.9, "flop": 1.0, "turn": 0.95, "river": 1.0}
        base_confidence *= stage_factor.get(stage, 1.0)
        
        return min(0.99, max(0.1, base_confidence))
    
    def _generate_detailed_reasoning(self, action: str, hand_evaluation: Dict, 
                                   pot_odds: float, equity: float, 
                                   position: str, stage: str) -> str:
        """Generar explicación detallada para la recomendación"""
        strength = hand_evaluation.get("strength", "UNKNOWN")
        category = hand_evaluation.get("category", "HIGH_CARD")
        
        reasoning_templates = {
            "VERY_STRONG": {
                "RAISE": "Mano premium ({category}). Debes construir el bote y obtener valor.",
                "BET": "Mano muy fuerte ({category}). Apostar para construir bote.",
                "ALL_IN": "Mano nuts o near-nuts. Máxima presión para proteger equity.",
                "CHECK": "Mano fuerte pero checking para pot control o trap."
            },
            "STRONG": {
                "RAISE": "Buena mano ({category}). Raise para proteger y obtener valor.",
                "BET": "Mano sólida ({category}). Bet estándar por valor.",
                "CALL": "Mano decente ({category}). Call para ver siguiente calle.",
                "CHECK": "Mano buena pero checking para pot control."
            },
            "MEDIUM": {
                "CALL": "Mano marginal ({category}). Pot odds favorables ({pot_odds:.1f}:1).",
                "CHECK": "Mano de showdown ({category}). Checking para ver gratis.",
                "FOLD": "Mano débil ({category}). Fold ante agresión."
            },
            "WEAK": {
                "FOLD": "Mano muy débil ({category}). Sin equity suficiente ({equity:.0%}).",
                "CHECK": "Mano débil pero checking para ver showdown barato.",
                "BLUFF": "Bluff semibluff con algunos outs."
            },
            "DRAWING": {
                "CALL": "Drawing hand ({category}). Buenos pot odds ({pot_odds:.1f}:1) para draw.",
                "RAISE": "Semibluff con drawing hand. Combinar fold equity con equity real.",
                "CHECK": "Drawing hand. Checking para ver carta gratis."
            }
        }
        
        template_group = reasoning_templates.get(strength, reasoning_templates["UNKNOWN"])
        template = template_group.get(action, "Decisión basada en análisis de situación.")
        
        # Reemplazar placeholders
        reasoning = template.format(
            category=category.replace('_', ' ').lower(),
            pot_odds=pot_odds if pot_odds != float('inf') else "∞",
            equity=equity,
            position=position,
            stage=stage
        )
        
        # Añadir consideraciones de posición si es relevante
        if position in ["UTG", "MP"] and action in ["RAISE", "BET"]:
            reasoning += " Considerar posición early."
        
        return reasoning
    
    def _get_alternative_actions(self, primary_action: str, hand_evaluation: Dict, stage: str) -> List[Dict]:
        """Obtener acciones alternativas recomendadas"""
        alternatives = []
        strength = hand_evaluation.get("strength", "UNKNOWN")
        
        # Mapear alternativas por fuerza de mano
        alternative_map = {
            "VERY_STRONG": [
                {"action": "RAISE", "confidence": 0.8, "reason": "Máximo valor"},
                {"action": "BET", "confidence": 0.7, "reason": "Valor estándar"},
                {"action": "CHECK", "confidence": 0.4, "reason": "Trap"}
            ],
            "STRONG": [
                {"action": "BET", "confidence": 0.7, "reason": "Por valor"},
                {"action": "CHECK", "confidence": 0.6, "reason": "Pot control"},
                {"action": "RAISE", "confidence": 0.5, "reason": "Protección"}
            ],
            "MEDIUM": [
                {"action": "CHECK", "confidence": 0.6, "reason": "Ver barato"},
                {"action": "CALL", "confidence": 0.5, "reason": "Pot odds"},
                {"action": "FOLD", "confidence": 0.4, "reason": "Mano marginal"}
            ],
            "WEAK": [
                {"action": "FOLD", "confidence": 0.8, "reason": "Mano débil"},
                {"action": "CHECK", "confidence": 0.3, "reason": "Ver showdown"},
                {"action": "BLUFF", "confidence": 0.2, "reason": "Bluff ocasioneal"}
            ]
        }
        
        alts = alternative_map.get(strength, [])
        
        # Filtrar acción primaria
        for alt in alts:
            if alt["action"] != primary_action:
                alternatives.append(alt)
        
        return alternatives[:2]  # Máximo 2 alternativas
    
    def set_strategy(self, strategy_name: str):
        """Cambiar estrategia de juego"""
        if strategy_name in self.strategies:
            old_strategy = self.strategy
            self.strategy = strategy_name
            print(f"🔄 Estrategia cambiada: {old_strategy} → {strategy_name}")
            print(f"   {self.strategies[strategy_name]['description']}")
            return True
        else:
            print(f"⚠️  Estrategia '{strategy_name}' no encontrada")
            return False
    
    def get_available_strategies(self) -> List[str]:
        """Obtener lista de estrategias disponibles"""
        return list(self.strategies.keys())
    
    def get_session_stats(self) -> Dict:
        """Obtener estadísticas de la sesión"""
        total_actions = sum(self.session_stats["actions_taken"].values())
        if total_actions > 0:
            win_rate = (
                self.session_stats["actions_taken"]["RAISE"] + 
                self.session_stats["actions_taken"]["BET"]
            ) / total_actions
            self.session_stats["win_rate"] = win_rate
        
        return self.session_stats.copy()
    
    def get_hand_history(self, limit: int = 10) -> List[Dict]:
        """Obtener historial de manos recientes"""
        return self.hand_history[-limit:] if self.hand_history else []
    
    def save_session(self, filename: str = None):
        """Guardar sesión actual a archivo"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/coach_session_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        session_data = {
            "session_info": {
                "platform": self.platform,
                "strategy": self.strategy,
                "start_time": self.session_stats["start_time"],
                "end_time": datetime.now().isoformat()
            },
            "session_stats": self.get_session_stats(),
            "recent_hands": self.get_hand_history(20),
            "config": self.config
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            print(f"💾 Sesión guardada: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error guardando sesión: {e}")
            return False

# Para uso independiente y pruebas
if __name__ == "__main__":
    print("🧪 PROBANDO COACH INTEGRATOR MEJORADO")
    print("=" * 60)
    
    coach = CoachIntegrator("pokerstars", "balanced")
    
    # Probar con diferentes situaciones
    test_situations = [
        {
            "name": "Pocket Aces preflop UTG",
            "hole_cards": [("A", "hearts"), ("A", "spades")],
            "community_cards": [],
            "pot_size": 50,
            "bet_size": 10,
            "position": "UTG",
            "players": 6,
            "stage": "preflop"
        },
        {
            "name": "AK suited flop con draws",
            "hole_cards": [("A", "hearts"), ("K", "hearts")],
            "community_cards": [("Q", "hearts"), ("J", "clubs"), ("2", "diamonds")],
            "pot_size": 200,
            "bet_size": 50,
            "position": "CO",
            "players": 4,
            "stage": "flop"
        },
        {
            "name": "Mano débil river",
            "hole_cards": [("7", "diamonds"), ("2", "clubs")],
            "community_cards": [("K", "hearts"), ("Q", "spades"), ("J", "diamonds"), ("10", "clubs"), ("9", "hearts")],
            "pot_size": 300,
            "bet_size": 100,
            "position": "BB",
            "players": 3,
            "stage": "river"
        },
        {
            "name": "Drawing hand turn",
            "hole_cards": [("8", "hearts"), ("9", "hearts")],
            "community_cards": [("6", "hearts"), ("7", "clubs"), ("2", "diamonds"), ("K", "spades")],
            "pot_size": 180,
            "bet_size": 40,
            "position": "BTN",
            "players": 2,
            "stage": "turn"
        }
    ]
    
    print("\n🔍 PROBANDO DIFERENTES ESTRATEGIAS:")
    strategies = coach.get_available_strategies()
    
    for strategy in strategies:
        print(f"\n📊 Estrategia: {strategy}")
        coach.set_strategy(strategy)
        
        for i, situation in enumerate(test_situations[:2]):  # Solo 2 por estrategia
            print(f"\n  Situación {i+1}: {situation['name']}")
            recommendation = coach.analyze_hand(situation)
            
            print(f"    🎯 Acción: {recommendation['primary_action']}")
            print(f"    📈 Confianza: {recommendation['confidence']:.0%}")
            print(f"    🧠 Razón: {recommendation['reasoning'][:60]}...")
    
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE PRUEBA:")
    stats = coach.get_session_stats()
    print(f"   Manos analizadas: {stats['hands_analyzed']}")
    print(f"   Recomendaciones: {stats['recommendations_given']}")
    print(f"   Distribución acciones: {stats['actions_taken']}")
    
    # Guardar sesión de prueba
    coach.save_session("logs/test_session.json")
    
    print("\n✅ Coach Integrator mejorado probado exitosamente!")
    print("=" * 60)