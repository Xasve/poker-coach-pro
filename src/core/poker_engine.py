"""
Archivo: poker_engine.py
Ruta: src/core/poker_engine.py
Motor principal de decisiones del Poker Coach Pro
"""

import random
from typing import Dict, List, Tuple, Optional
from enum import Enum
import json
import os

class Action(Enum):
    """Acciones disponibles en poker"""
    FOLD = "FOLD"
    CHECK = "CHECK"
    CALL = "CALL"
    BET = "BET"
    RAISE = "RAISE"
    ALL_IN = "ALL-IN"

class PokerEngine:
    """Motor principal de decisiones de poker"""
    
    def __init__(self, platform="ggpoker", mode="cash"):
        self.platform = platform
        self.mode = mode
        self.load_config()
        
        # Rangos preflop básicos
        self.preflop_ranges = self.load_preflop_ranges()
        
        # Historial de decisiones
        self.hand_history = []
        
    def load_config(self):
        """Cargar configuración de la plataforma"""
        config_path = f"config/{self.platform}_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
            
    def load_preflop_ranges(self) -> Dict:
        """Cargar rangos preflop según posición y modo"""
        
        # Rangos para 6-max Cash Games (GG Poker style)
        cash_ranges = {
            "UTG": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "AJs", "KQs", "AKo"],
            "MP": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "AJs", "ATs", 
                  "KQs", "KJs", "QJs", "AKo", "AQo"],
            "CO": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AQs", 
                  "AJs", "ATs", "A9s", "KQs", "KJs", "KTs", "QJs", "QTs", "JTs",
                  "AKo", "AQo", "AJo", "KQo"],
            "BTN": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
                   "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s",
                   "KQs", "KJs", "KTs", "K9s", "QJs", "QTs", "Q9s", "JTs", "J9s",
                   "T9s", "98s", "AKo", "AQo", "AJo", "ATo", "KQo", "KJo"],
            "SB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44",
                  "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s",
                  "KQs", "KJs", "KTs", "K9s", "QJs", "QTs", "Q9s", "JTs", "J9s",
                  "T9s", "98s", "87s", "AKo", "AQo", "AJo", "ATo", "KQo", "KJo", "QJo"],
            "BB": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                  "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                  "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                  "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                  "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                  "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                  "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                  "87s", "86s", "85s", "84s", "83s", "82s",
                  "76s", "75s", "74s", "73s", "72s",
                  "65s", "64s", "63s", "62s",
                  "54s", "53s", "52s",
                  "43s", "42s",
                  "32s",
                  "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                  "KQo", "KJo", "KTo", "K9o", "K8o", "K7o", "K6o", "K5o", "K4o", "K3o", "K2o",
                  "QJo", "QTo", "Q9o", "Q8o", "Q7o", "Q6o", "Q5o", "Q4o", "Q3o", "Q2o",
                  "JTo", "J9o", "J8o", "J7o", "J6o", "J5o", "J4o", "J3o", "J2o",
                  "T9o", "T8o", "T7o", "T6o", "T5o", "T4o", "T3o", "T2o",
                  "98o", "97o", "96o", "95o", "94o", "93o", "92o",
                  "87o", "86o", "85o", "84o", "83o", "82o",
                  "76o", "75o", "74o", "73o", "72o",
                  "65o", "64o", "63o", "62o",
                  "54o", "53o", "52o",
                  "43o", "42o",
                  "32o"]
        }
        
        # Ajustes para torneos (más tight)
        tournament_ranges = {}
        for position in cash_ranges:
            # En torneos jugamos 20-30% menos manos
            tournament_ranges[position] = cash_ranges[position][:int(len(cash_ranges[position]) * 0.7)]
            
        return tournament_ranges if self.mode == "tournament" else cash_ranges
    
    def get_decision(self, game_state: Dict, mode: str = "cash") -> Dict:
        """
        Obtener decisión óptima basada en el estado del juego
        
        Args:
            game_state: Diccionario con estado del juego
            mode: Modo de juego ('cash' o 'tournament')
            
        Returns:
            Dict con decisión y explicación
        """
        
        # Validar estado mínimo
        if not game_state or 'hero_cards' not in game_state:
            return self._get_default_decision()
        
        # Determinar fase del juego
        if game_state.get('street') == 'preflop':
            decision = self._preflop_decision(game_state, mode)
        else:
            decision = self._postflop_decision(game_state, mode)
        
        # Ajustar por modo torneo si es necesario
        if mode == "tournament":
            decision = self._adjust_for_tournament(decision, game_state)
        
        # Guardar en historial
        self.hand_history.append({
            'game_state': game_state,
            'decision': decision,
            'timestamp': time.time()
        })
        
        return decision
    
    def _preflop_decision(self, game_state: Dict, mode: str) -> Dict:
        """Tomar decisión preflop"""
        
        hero_cards = game_state.get('hero_cards', [])
        position = game_state.get('position', '')
        action_to_us = game_state.get('action_to_us', False)
        pot_size = game_state.get('pot_size', 0)
        bet_to_call = game_state.get('bet_to_call', 0)
        
        # Convertir cartas a formato de rango
        card_str = self._cards_to_string(hero_cards)
        
        # Verificar si está en rango para la posición
        if position in self.preflop_ranges:
            in_range = card_str in self.preflop_ranges[position]
        else:
            in_range = False
        
        # Lógica básica de decisión
        if not action_to_us:
            # Somos primeros en actuar
            if in_range:
                return {
                    'action': Action.RAISE.value,
                    'size': self._get_preflop_raise_size(position),
                    'confidence': 85,
                    'reason': f"Mano fuerte para posición {position}. Abrir estándar.",
                    'alternatives': [Action.FOLD.value]
                }
            else:
                return {
                    'action': Action.FOLD.value,
                    'size': 0,
                    'confidence': 90,
                    'reason': f"Mano fuera de rango para {position}. Fold disciplinado.",
                    'alternatives': []
                }
        else:
            # Hay acción antes que nosotros
            if bet_to_call > 0:
                # Hay que pagar apuesta
                pot_odds = bet_to_call / (pot_size + bet_to_call)
                
                if in_range and pot_odds < 0.3:  # Buena relación riesgo/recompensa
                    return {
                        'action': Action.CALL.value,
                        'size': bet_to_call,
                        'confidence': 75,
                        'reason': f"Mano jugable con buenas pot odds ({pot_odds:.1%}).",
                        'alternatives': [Action.RAISE.value, Action.FOLD.value]
                    }
                else:
                    return {
                        'action': Action.FOLD.value,
                        'size': 0,
                        'confidence': 80,
                        'reason': "Mano débil o malas odds. Fold.",
                        'alternatives': []
                    }
        
        # Decisión por defecto si no se cumple nada
        return {
            'action': Action.FOLD.value,
            'size': 0,
            'confidence': 60,
            'reason': "Situación marginal. Fold conservador.",
            'alternatives': []
        }
    
    def _postflop_decision(self, game_state: Dict, mode: str) -> Dict:
        """Tomar decisión postflop"""
        
        street = game_state.get('street', 'flop')
        hero_cards = game_state.get('hero_cards', [])
        board_cards = game_state.get('board_cards', [])
        position = game_state.get('position', '')
        pot_size = game_state.get('pot_size', 0)
        bet_to_call = game_state.get('bet_to_call', 0)
        
        # Evaluar fuerza de mano
        hand_strength = self._evaluate_hand_strength(hero_cards, board_cards)
        
        if bet_to_call > 0:
            # Hay apuesta que pagar
            pot_odds = bet_to_call / (pot_size + bet_to_call)
            
            if hand_strength > 0.7:  # Mano muy fuerte
                return {
                    'action': Action.RAISE.value,
                    'size': pot_size * 0.75,  # Raise 75% del pot
                    'confidence': 85,
                    'reason': "Mano muy fuerte. Raise por value.",
                    'alternatives': [Action.CALL.value]
                }
            elif hand_strength > 0.4 and pot_odds < 0.25:  # Mano decente con buenas odds
                return {
                    'action': Action.CALL.value,
                    'size': bet_to_call,
                    'confidence': 70,
                    'reason': f"Mano jugable con buenas odds ({pot_odds:.1%}).",
                    'alternatives': [Action.FOLD.value]
                }
            else:
                return {
                    'action': Action.FOLD.value,
                    'size': 0,
                    'confidence': 80,
                    'reason': "Mano débil o odds insuficientes.",
                    'alternatives': []
                }
        else:
            # Sin apuesta que pagar (podemos apostar o checkear)
            if hand_strength > 0.6:
                return {
                    'action': Action.BET.value,
                    'size': pot_size * 0.5,  # Bet 50% del pot
                    'confidence': 80,
                    'reason': "Mano fuerte. Bet por value.",
                    'alternatives': [Action.CHECK.value]
                }
            elif hand_strength > 0.3 and street == 'flop':
                return {
                    'action': Action.BET.value,
                    'size': pot_size * 0.33,  # C-bet estándar
                    'confidence': 65,
                    'reason': "C-bet estándar con algo de equity.",
                    'alternatives': [Action.CHECK.value]
                }
            else:
                return {
                    'action': Action.CHECK.value,
                    'size': 0,
                    'confidence': 75,
                    'reason': "Mano débil. Check y ver desarrollo.",
                    'alternatives': [Action.BET.value]
                }
    
    def _adjust_for_tournament(self, decision: Dict, game_state: Dict) -> Dict:
        """Ajustar decisión para modo torneo"""
        
        # En torneos, ser más conservador con stack pequeño
        stack_bb = game_state.get('stack_bb', 100)
        
        if stack_bb < 20:  # Stack corto
            if decision['action'] in [Action.CALL.value, Action.RAISE.value]:
                # Ser más agresivo con stack corto
                if 'size' in decision and decision['size'] > 0:
                    decision['size'] = min(decision['size'] * 1.2, stack_bb)
                decision['reason'] += " Stack corto: juego push/fold."
        
        elif stack_bb > 50:  # Stack profundo
            if decision['action'] == Action.RAISE.value:
                # Reducir tamaño de apuesta con stack profundo
                if 'size' in decision:
                    decision['size'] = decision['size'] * 0.8
        
        return decision
    
    def _get_preflop_raise_size(self, position: str) -> float:
        """Obtener tamaño de raise preflop según posición y plataforma"""
        
        if self.platform == "ggpoker":
            # GG Poker usa 2.2BB estándar
            base_size = 2.2
        else:  # pokerstars
            # PokerStars usa 2.5BB estándar
            base_size = 2.5
        
        # Ajustar por posición
        adjustments = {
            'UTG': 1.0,
            'MP': 1.0,
            'CO': 0.95,  # Un poco menos desde CO
            'BTN': 0.9,  # Menos desde BTN
            'SB': 3.0,   # Desde SB raise más grande
        }
        
        adjustment = adjustments.get(position, 1.0)
        return base_size * adjustment
    
    def _cards_to_string(self, cards: List) -> str:
        """Convertir lista de cartas a formato de rango"""
        if not cards or len(cards) < 2:
            return ""
        
        # Ordenar cartas por valor
        values = []
        suits = []
        
        for card in cards:
            if len(card) >= 2:
                values.append(card[0].upper())
                suits.append(card[1].lower())
        
        # Determinar si son suited
        if len(suits) == 2 and suits[0] == suits[1]:
            suited = "s"
        else:
            suited = "o"
        
        # Ordenar valores (A high)
        value_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            value_order[str(i)] = i
        
        if len(values) == 2:
            val1 = value_order.get(values[0], 0)
            val2 = value_order.get(values[1], 0)
            
            if val1 == val2:
                return f"{values[0]}{values[1]}"  # Pocket pair
            elif val1 > val2:
                return f"{values[0]}{values[1]}{suited}"
            else:
                return f"{values[1]}{values[0]}{suited}"
        
        return ""
    
    def _evaluate_hand_strength(self, hero_cards: List, board_cards: List) -> float:
        """
        Evaluar fuerza de mano simplificada (0-1)
        """
        if not hero_cards or len(hero_cards) < 2:
            return 0.0
        
        # Evaluación simplificada
        # En un sistema real usaríamos equity calculator
        card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            card_values[str(i)] = i
        
        # Valor de las cartas hole
        hole_strength = 0
        for card in hero_cards:
            if len(card) > 0:
                value = card_values.get(card[0].upper(), 0)
                hole_strength += value / 14
        
        hole_strength = hole_strength / 2  # Normalizar
        
        # Bonus por suited
        if len(hero_cards) >= 2:
            if hero_cards[0][-1] == hero_cards[1][-1]:
                hole_strength += 0.1
        
        # Bonus por connectedness
        if len(hero_cards) >= 2:
            val1 = card_values.get(hero_cards[0][0].upper(), 0)
            val2 = card_values.get(hero_cards[1][0].upper(), 0)
            if abs(val1 - val2) <= 2:
                hole_strength += 0.1
        
        return min(hole_strength, 1.0)
    
    def _get_default_decision(self) -> Dict:
        """Decisión por defecto cuando no hay información suficiente"""
        return {
            'action': Action.FOLD.value,
            'size': 0,
            'confidence': 50,
            'reason': "Información insuficiente. Fold conservador.",
            'alternatives': []
        }

# Versión simplificada para inicio rápido
class SimplePokerEngine(PokerEngine):
    """Versión simplificada del motor para pruebas"""
    
    def get_simple_decision(self, street="preflop", position="BTN", has_good_cards=True) -> Dict:
        """Decisión simplificada para testing"""
        
        situations = {
            "preflop": [
                ("RAISE", "2.2BB", "Open estándar desde posición tardía", 85),
                ("FOLD", "", "Mano débil, disciplina", 90),
                ("CALL", "1BB", "Defensa ciega con mano jugable", 70)
            ],
            "flop": [
                ("BET", "33% pot", "C-bet estándar", 80),
                ("CHECK", "", "Board peligroso", 75),
                ("RAISE", "2.5x", "Aumentar con mano fuerte", 85)
            ],
            "turn": [
                ("BET", "60% pot", "Continuar agresión", 70),
                ("CHECK", "", "Controlar olla", 65)
            ],
            "river": [
                ("BET", "70% pot", "Value bet fino", 75),
                ("CHECK", "", "Mostdown, no value", 60)
            ]
        }
        
        street_sits = situations.get(street, situations["preflop"])
        action, size, reason, confidence = random.choice(street_sits)
        
        return {
            'action': action,
            'size': size,
            'confidence': confidence,
            'reason': reason,
            'alternatives': []
        }

# Para importaciones
import time