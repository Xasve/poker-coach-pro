"""
Archivo: cash_strategy.py
Ruta: src/strategies/cash_strategy.py
Estrategias específicas para Cash Games
"""

from enum import Enum
import random
from typing import Dict, List

class CashGameStrategy:
    """Estrategias para Cash Games (dinero real)"""
    
    def __init__(self, platform="ggpoker", stakes="NL10"):
        self.platform = platform
        self.stakes = stakes
        self.vpip = 0.0  # Voluntarily Put $ In Pot
        self.pfr = 0.0   # Preflop Raise
        self.agg_factor = 0.0
        
        # Cargar ajustes por stakes
        self.load_stakes_adjustments()
        
        # Estadísticas de sesión
        self.session_stats = {
            'hands_played': 0,
            'vpip_count': 0,
            'pfr_count': 0,
            'winnings': 0.0,
            'big_blinds_won': 0.0
        }
    
    def load_stakes_adjustments(self):
        """Cargar ajustes según nivel de stakes"""
        
        # Ajustes por stakes (más tight en stakes bajos, más agresivo en altos)
        self.stakes_adjustments = {
            'NL2': {'vpip_target': 0.18, 'pfr_target': 0.14, 'aggression': 2.5},
            'NL5': {'vpip_target': 0.19, 'pfr_target': 0.15, 'aggression': 2.7},
            'NL10': {'vpip_target': 0.20, 'pfr_target': 0.16, 'aggression': 2.8},
            'NL25': {'vpip_target': 0.21, 'pfr_target': 0.17, 'aggression': 2.9},
            'NL50': {'vpip_target': 0.22, 'pfr_target': 0.18, 'aggression': 3.0},
            'NL100': {'vpip_target': 0.23, 'pfr_target': 0.19, 'aggression': 3.1},
            'NL200+': {'vpip_target': 0.24, 'pfr_target': 0.20, 'aggression': 3.2}
        }
        
        # Ajustes específicos por plataforma
        if self.platform == "ggpoker":
            # GG Poker es más loose, jugar más tight
            for stakes in self.stakes_adjustments:
                self.stakes_adjustments[stakes]['vpip_target'] *= 0.95
                self.stakes_adjustments[stakes]['aggression'] *= 1.05
        elif self.platform == "pokerstars":
            # PokerStars más regular, juego standard
            pass
    
    def get_preflop_decision(self, game_state: Dict) -> Dict:
        """Decisión preflop para cash games"""
        
        position = game_state.get('position', 'BTN')
        hero_cards = game_state.get('hero_cards', [])
        action_to_us = game_state.get('action_to_us', False)
        bet_to_call = game_state.get('bet_to_call', 0)
        
        # Evaluar fuerza de mano
        hand_strength = self.evaluate_hand_preflop(hero_cards)
        
        # Rangos por posición para cash games
        position_ranges = self.get_position_ranges(position)
        
        # Verificar si mano está en rango
        hand_in_range = self.is_hand_in_range(hero_cards, position_ranges)
        
        if not action_to_us:
            # Primer en actuar
            if hand_in_range:
                # Determinar tamaño de raise
                raise_size = self.get_open_raise_size(position)
                
                return {
                    'action': 'RAISE',
                    'size': raise_size,
                    'confidence': 85,
                    'reason': f"Mano top {position_ranges['percentage']}% para {position}. Open estándar.",
                    'alternatives': ['FOLD']
                }
            else:
                return {
                    'action': 'FOLD',
                    'size': 0,
                    'confidence': 90,
                    'reason': f"Mano fuera de rango ({position_ranges['percentage']}% range). Fold disciplinado.",
                    'alternatives': []
                }
        
        else:
            # Hay acción antes
            if bet_to_call > 0:
                # Calcular pot odds
                pot_size = game_state.get('pot_size', 0)
                pot_odds = bet_to_call / (pot_size + bet_to_call)
                
                if hand_in_range and pot_odds < 0.25:
                    # Buena mano con buenas odds
                    return {
                        'action': 'CALL',
                        'size': bet_to_call,
                        'confidence': 75,
                        'reason': f"Mano jugable con pot odds {pot_odds:.1%}. Call.",
                        'alternatives': ['RAISE', 'FOLD']
                    }
                elif hand_strength > 0.8:
                    # Mano muy fuerte, considerar 3-bet
                    threebet_size = bet_to_call * 3
                    return {
                        'action': 'RAISE',
                        'size': threebet_size,
                        'confidence': 80,
                        'reason': "Mano premium. 3-bet por value.",
                        'alternatives': ['CALL', 'FOLD']
                    }
                else:
                    # Fold
                    return {
                        'action': 'FOLD',
                        'size': 0,
                        'confidence': 85,
                        'reason': f"Mano débil o pot odds insuficientes ({pot_odds:.1%}).",
                        'alternatives': []
                    }
        
        # Decisión por defecto
        return {
            'action': 'FOLD',
            'size': 0,
            'confidence': 70,
            'reason': "Situación marginal. Fold conservador.",
            'alternatives': []
        }
    
    def get_position_ranges(self, position: str) -> Dict:
        """Obtener rangos por posición para cash games"""
        
        # Rangos aproximados por posición (porcentaje de manos)
        ranges = {
            'UTG': {'percentage': 15, 'description': 'Muy tight'},
            'MP': {'percentage': 20, 'description': 'Tight'},
            'CO': {'percentage': 28, 'description': 'Moderado'},
            'BTN': {'percentage': 40, 'description': 'Wide'},
            'SB': {'percentage': 35, 'description': 'Defensivo'},
            'BB': {'percentage': 45, 'description': 'Wide defensivo'}
        }
        
        # Ajustar por plataforma
        if self.platform == "ggpoker":
            # GG Poker más loose, jugar más tight
            for pos in ranges:
                ranges[pos]['percentage'] = max(10, ranges[pos]['percentage'] - 3)
        elif self.platform == "pokerstars":
            # PokerStars más regular
            pass
        
        return ranges.get(position, ranges['BTN'])
    
    def evaluate_hand_preflop(self, cards: List[str]) -> float:
        """Evaluar fuerza de mano preflop (0-1)"""
        
        if not cards or len(cards) < 2:
            return 0.0
        
        card1 = cards[0] if len(cards) > 0 else ''
        card2 = cards[1] if len(cards) > 1 else ''
        
        if not card1 or not card2:
            return 0.0
        
        # Valores de cartas
        values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            values[str(i)] = i
        
        val1 = values.get(card1[0].upper(), 0)
        val2 = values.get(card2[0].upper(), 0)
        
        # Evaluar pares
        if val1 == val2:
            # Pocket pair
            pair_strength = val1 / 14
            return 0.5 + (pair_strength * 0.5)
        
        # Evaluar suited
        suited = len(card1) > 1 and len(card2) > 1 and card1[-1] == card2[-1]
        
        # Evaluar conectividad
        gap = abs(val1 - val2)
        
        # Calcular fuerza base
        high_card = max(val1, val2)
        strength = high_card / 14
        
        # Ajustar por suited
        if suited:
            strength += 0.15
        
        # Ajustar por gap
        if gap == 1:
            strength += 0.10  # Conectadas
        elif gap == 2:
            strength += 0.05  # One gap
        elif gap > 4:
            strength -= 0.10  # Desconectadas
        
        # Ajustar por ser Ace
        if 'A' in card1.upper() or 'A' in card2.upper():
            strength += 0.10
        
        return max(0.0, min(1.0, strength))
    
    def is_hand_in_range(self, cards: List[str], position_range: Dict) -> bool:
        """Determinar si mano está en rango para posición"""
        
        hand_strength = self.evaluate_hand_preflop(cards)
        
        # Convertir porcentaje de rango a umbral de fuerza
        percentage = position_range.get('percentage', 30)
        threshold = percentage / 100 * 0.8  # Ajuste empírico
        
        return hand_strength >= threshold
    
    def get_open_raise_size(self, position: str) -> str:
        """Obtener tamaño de raise preflop"""
        
        if self.platform == "ggpoker":
            base_size = 2.2
        else:  # pokerstars
            base_size = 2.5
        
        # Ajustes por posición
        adjustments = {
            'UTG': 1.0,
            'MP': 1.0,
            'CO': 0.95,
            'BTN': 0.9,
            'SB': 3.0,  # Desde SB raise más grande
            'BB': 1.0
        }
        
        adj = adjustments.get(position, 1.0)
        size = base_size * adj
        
        return f"{size:.1f}BB"
    
    def update_session_stats(self, action: str, pot_result: float = 0):
        """Actualizar estadísticas de sesión"""
        
        self.session_stats['hands_played'] += 1
        
        if action in ['CALL', 'RAISE', 'BET']:
            self.session_stats['vpip_count'] += 1
        
        if action == 'RAISE':
            self.session_stats['pfr_count'] += 1
        
        if pot_result != 0:
            self.session_stats['winnings'] += pot_result
            self.session_stats['big_blinds_won'] += pot_result
        
        # Calcular VPIP/PFR actual
        if self.session_stats['hands_played'] > 0:
            self.vpip = self.session_stats['vpip_count'] / self.session_stats['hands_played']
            self.pfr = self.session_stats['pfr_count'] / self.session_stats['hands_played']
    
    def get_session_summary(self) -> Dict:
        """Obtener resumen de sesión"""
        
        bb_per_100 = 0
        if self.session_stats['hands_played'] >= 100:
            bb_per_100 = (self.session_stats['big_blinds_won'] / 
                         self.session_stats['hands_played']) * 100
        
        return {
            'hands_played': self.session_stats['hands_played'],
            'vpip': f"{self.vpip:.1%}",
            'pfr': f"{self.pfr:.1%}",
            'winnings': f"${self.session_stats['winnings']:.2f}",
            'bb_won': f"{self.session_stats['big_blinds_won']:.1f}",
            'bb_per_100': f"{bb_per_100:.1f}",
            'target_vpip': f"{self.stakes_adjustments.get(self.stakes, {}).get('vpip_target', 0.20):.1%}",
            'target_pfr': f"{self.stakes_adjustments.get(self.stakes, {}).get('pfr_target', 0.16):.1%}"
        }