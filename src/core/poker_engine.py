"""
poker_engine.py - Motor principal de decisiones de poker
Implementa lógica GTO básica para decisiones preflop/postflop
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class HandStrength:
    """Fuerza evaluada de una mano"""
    hand_type: str  # 'high_card', 'pair', 'two_pair', 'three_of_a_kind', etc.
    rank: int  # 1-14 (2-A)
    kickers: List[int]  # Cartas adicionales para desempate
    equity: float  # 0.0 a 1.0
    
    def __str__(self):
        type_names = {
            'high_card': 'Carta Alta',
            'pair': 'Pareja',
            'two_pair': 'Doble Pareja',
            'three_of_a_kind': 'Trio',
            'straight': 'Escalera',
            'flush': 'Color',
            'full_house': 'Full House',
            'four_of_a_kind': 'Póker',
            'straight_flush': 'Escalera de Color',
            'royal_flush': 'Escalera Real'
        }
        return f"{type_names.get(self.hand_type, self.hand_type)} ({self.equity:.1%})"

class PokerEngine:
    """Motor principal de decisiones de poker"""
    
    def __init__(self, aggression_factor: float = 1.0, tightness_factor: float = 1.0):
        """
        Inicializar motor de poker
        
        Args:
            aggression_factor: 0.5=pasivo, 1.0=normal, 1.5=agresivo
            tightness_factor: 0.5=loose, 1.0=normal, 1.5=tight
        """
        self.aggression_factor = max(0.1, min(2.0, aggression_factor))
        self.tightness_factor = max(0.1, min(2.0, tightness_factor))
        
        # Cargar rangos preflop
        self.preflop_ranges = self._load_preflop_ranges()
        
        # Cargar estrategias postflop
        self.postflop_strategies = self._load_postflop_strategies()
        
        # Estadísticas
        self.decisions_made = 0
        self.average_confidence = 0.0
        
        print(f"✅ PokerEngine inicializado (agresión: {aggression_factor}, tightness: {tightness_factor})")
    
    def _load_preflop_ranges(self) -> Dict[str, List[str]]:
        """Cargar rangos preflop GTO para 6-max"""
        # Rangos básicos GTO (simplificados)
        return {
            "UTG": [
                "AA", "KK", "QQ", "JJ", "TT", "99",
                "AKs", "AQs", "AJs", "ATs",
                "AKo", "AQo",
                "KQs", "KJs",
                "QJs", "JTs", "T9s", "98s"
            ],
            "MP": [
                "AA", "KK", "QQ", "JJ", "TT", "99", "88",
                "AKs", "AQs", "AJs", "ATs", "A9s",
                "AKo", "AQo", "AJo",
                "KQs", "KJs", "KTs",
                "QJs", "QTs",
                "JTs", "T9s", "98s", "87s"
            ],
            "CO": [
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "AKo", "AQo", "AJo", "ATo",
                "KQs", "KJs", "KTs", "K9s",
                "QJs", "QTs", "Q9s",
                "JTs", "J9s",
                "T9s", "T8s",
                "98s", "97s",
                "87s", "86s",
                "76s", "65s", "54s"
            ],
            "BTN": [
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "AKo", "AQo", "AJo", "ATo", "A9o",
                "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                "KQo", "KJo", "KTo",
                "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                "QJo", "QTo",
                "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                "JTo",
                "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                "87s", "86s", "85s", "84s", "83s", "82s",
                "76s", "75s", "74s", "73s", "72s",
                "65s", "64s", "63s", "62s",
                "54s", "53s", "52s",
                "43s", "42s",
                "32s"
            ],
            "SB": [
                # Similar a BTN pero más tight
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s",
                "AKo", "AQo", "AJo",
                "KQs", "KJs", "KTs", "K9s",
                "QJs", "QTs", "Q9s",
                "JTs", "J9s",
                "T9s", "T8s",
                "98s", "97s",
                "87s", "86s",
                "76s", "65s"
            ],
            "BB": [
                # Defensa amplia contra steals
                "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66", "55", "44", "33", "22",
                "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
                "AKo", "AQo", "AJo", "ATo", "A9o", "A8o", "A7o", "A6o", "A5o", "A4o", "A3o", "A2o",
                "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s",
                "KQo", "KJo", "KTo", "K9o",
                "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s",
                "QJo", "QTo", "Q9o",
                "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s",
                "JTo", "J9o",
                "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s",
                "T9o", "T8o",
                "98s", "97s", "96s", "95s", "94s", "93s", "92s",
                "98o", "97o",
                "87s", "86s", "85s", "84s", "83s", "82s",
                "87o", "86o",
                "76s", "75s", "74s", "73s", "72s",
                "76o",
                "65s", "64s", "63s", "62s",
                "65o",
                "54s", "53s", "52s",
                "54o",
                "43s", "42s",
                "32s"
            ]
        }
    
    def _load_postflop_strategies(self) -> Dict[str, Dict]:
        """Cargar estrategias postflop básicas"""
        return {
            "cbet_frequencies": {
                "dry": 0.7,      # Flops secos: 70% c-bet
                "wet": 0.4,      # Flops húmedos: 40% c-bet
                "paired": 0.3,   # Flops pareados: 30% c-bet
                "monotone": 0.2  # Flops monocolor: 20% c-bet
            },
            "bet_sizings": {
                "dry": 0.33,     # 33% del pot
                "wet": 0.50,     # 50% del pot
                "paired": 0.66,  # 66% del pot
                "value": 0.75,   # 75% del pot para value bets
                "bluff": 0.45    # 45% del pot para bluffs
            },
            "continuation_ranges": {
                "overpairs": 1.0,      # Siempre continuar con overpairs
                "top_pair": 0.8,       # 80% con top pair
                "middle_pair": 0.5,    # 50% con middle pair
                "weak_pair": 0.2,      # 20% con weak pair
                "draws": 0.7,          # 70% con draws fuertes
                "air": 0.3             # 30% con nada (bluffs balanceados)
            }
        }
    
    def evaluate_hand_strength(self, hero_cards: List[str], board_cards: List[str]) -> HandStrength:
        """
        Evaluar fuerza de la mano actual
        
        Args:
            hero_cards: Lista de 2 cartas del hero (ej: ['Ah', 'Ks'])
            board_cards: Lista de 0-5 cartas del board
            
        Returns:
            HandStrength con evaluación
        """
        # Convertir cartas a formato numérico
        all_cards = hero_cards + board_cards
        numeric_cards = self._cards_to_numeric(all_cards)
        
        if len(board_cards) == 0:
            # Evaluación preflop
            return self._evaluate_preflop_hand(hero_cards)
        else:
            # Evaluación postflop
            return self._evaluate_postflop_hand(numeric_cards)
    
    def _cards_to_numeric(self, cards: List[str]) -> List[Tuple[int, int]]:
        """Convertir cartas a formato numérico (rank, suit)"""
        rank_map = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        suit_map = {'s': 0, 'h': 1, 'd': 2, 'c': 3}
        
        numeric = []
        for card in cards:
            if len(card) >= 2:
                rank = rank_map.get(card[0].upper(), 0)
                suit = suit_map.get(card[-1].lower(), 0)
                numeric.append((rank, suit))
        
        return numeric
    
    def _evaluate_preflop_hand(self, hero_cards: List[str]) -> HandStrength:
        """Evaluar fuerza de mano preflop"""
        if len(hero_cards) != 2:
            return HandStrength(hand_type='unknown', rank=0, kickers=[], equity=0.5)
        
        # Simplificación: clasificar manos preflop
        card1, card2 = hero_cards
        rank1, suit1 = card1[0], card1[-1]
        rank2, suit2 = card2[0], card2[-1]
        
        # Pareja
        if rank1 == rank2:
            rank_value = self._rank_to_value(rank1)
            # Equity aproximada de parejas
            equity_map = {14: 0.85, 13: 0.82, 12: 0.80, 11: 0.78, 10: 0.75}
            equity = equity_map.get(rank_value, 0.65)
            return HandStrength(
                hand_type='pair',
                rank=rank_value,
                kickers=[rank_value],
                equity=equity
            )
        
        # Cartas suited
        elif suit1 == suit2:
            rank_value = max(self._rank_to_value(rank1), self._rank_to_value(rank2))
            # Equity aproximada de suited connectors
            equity = 0.55 if abs(self._rank_to_value(rank1) - self._rank_to_value(rank2)) <= 4 else 0.48
            return HandStrength(
                hand_type='suited',
                rank=rank_value,
                kickers=[min(self._rank_to_value(rank1), self._rank_to_value(rank2))],
                equity=equity
            )
        
        # Cartas offsuit
        else:
            rank_value = max(self._rank_to_value(rank1), self._rank_to_value(rank2))
            equity = 0.45
            return HandStrength(
                hand_type='offsuit',
                rank=rank_value,
                kickers=[min(self._rank_to_value(rank1), self._rank_to_value(rank2))],
                equity=equity
            )
    
    def _rank_to_value(self, rank: str) -> int:
        """Convertir rank de carta a valor numérico"""
        rank_map = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return rank_map.get(rank.upper(), 0)
    
    def _evaluate_postflop_hand(self, cards: List[Tuple[int, int]]) -> HandStrength:
        """Evaluar fuerza de mano postflop (simplificado)"""
        # Implementación simplificada - en realidad necesitaría hand evaluator completo
        ranks = [card[0] for card in cards]
        suits = [card[1] for card in cards]
        
        # Contar frecuencias de ranks
        rank_counts = {}
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        # Verificar posibles manos (simplificado)
        sorted_ranks = sorted(ranks, reverse=True)
        
        # Verificar póker
        for rank, count in rank_counts.items():
            if count == 4:
                return HandStrength(
                    hand_type='four_of_a_kind',
                    rank=rank,
                    kickers=[max(r for r in ranks if r != rank)],
                    equity=0.95
                )
        
        # Verificar full house
        three_of_a_kind = None
        pair = None
        for rank, count in rank_counts.items():
            if count == 3:
                three_of_a_kind = rank
            elif count == 2:
                pair = rank
        
        if three_of_a_kind and pair:
            return HandStrength(
                hand_type='full_house',
                rank=three_of_a_kind,
                kickers=[pair],
                equity=0.90
            )
        
        # Verificar color (simplificado)
        suit_counts = {}
        for suit in suits:
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
        
        for suit, count in suit_counts.items():
            if count >= 5:
                # Encontrar la carta más alta del color
                flush_ranks = [r for r, s in zip(ranks, suits) if s == suit]
                high_card = max(flush_ranks)
                return HandStrength(
                    hand_type='flush',
                    rank=high_card,
                    kickers=sorted(flush_ranks, reverse=True)[:5],
                    equity=0.85
                )
        
        # Verificar escalera (simplificado)
        unique_ranks = sorted(set(ranks))
        straight_length = 1
        max_straight_rank = unique_ranks[0]
        
        for i in range(1, len(unique_ranks)):
            if unique_ranks[i] == unique_ranks[i-1] + 1:
                straight_length += 1
                if straight_length >= 5:
                    max_straight_rank = unique_ranks[i]
            else:
                straight_length = 1
        
        if straight_length >= 5:
            return HandStrength(
                hand_type='straight',
                rank=max_straight_rank,
                kickers=[max_straight_rank - i for i in range(5)],
                equity=0.80
            )
        
        # Verificar trio
        for rank, count in rank_counts.items():
            if count == 3:
                kickers = sorted([r for r in ranks if r != rank], reverse=True)[:2]
                return HandStrength(
                    hand_type='three_of_a_kind',
                    rank=rank,
                    kickers=kickers,
                    equity=0.70
                )
        
        # Verificar doble pareja
        pairs = sorted([rank for rank, count in rank_counts.items() if count == 2], reverse=True)
        if len(pairs) >= 2:
            kicker = max([r for r in ranks if r not in pairs[:2]])
            return HandStrength(
                hand_type='two_pair',
                rank=pairs[0],
                kickers=[pairs[1], kicker],
                equity=0.55
            )
        
        # Verificar pareja
        if len(pairs) == 1:
            kickers = sorted([r for r in ranks if r != pairs[0]], reverse=True)[:3]
            return HandStrength(
                hand_type='pair',
                rank=pairs[0],
                kickers=kickers,
                equity=0.40
            )
        
        # Carta alta
        return HandStrength(
            hand_type='high_card',
            rank=max(ranks),
            kickers=sorted(ranks, reverse=True)[:5],
            equity=0.15
        )
    
    def make_decision(self, game_state: Dict) -> Dict:
        """
        Tomar decisión basada en el estado del juego
        
        Args:
            game_state: Diccionario con estado del juego de GGPokerAdapter
            
        Returns:
            Dict con decisión y detalles
        """
        self.decisions_made += 1
        
        try:
            hero_cards = game_state.get('hero_cards', [])
            board_cards = game_state.get('board_cards', [])
            current_street = game_state.get('current_street', 'preflop')
            hero_position = game_state.get('hero_position', 'BTN')
            pot_amount = game_state.get('pot_amount', 0)
            hero_stack = game_state.get('hero_stack', 100)
            available_actions = game_state.get('available_actions', {})
            
            # Evaluar fuerza de mano
            hand_strength = self.evaluate_hand_strength(hero_cards, board_cards)
            
            # Tomar decisión basada en calle
            if current_street == 'preflop':
                decision = self._preflop_decision(
                    hero_cards, hero_position, pot_amount, hand_strength, available_actions
                )
            else:
                decision = self._postflop_decision(
                    hero_cards, board_cards, current_street, pot_amount, hand_strength, available_actions
                )
            
            # Ajustar por factores de agresión/tightness
            decision = self._adjust_decision_by_factors(decision, hand_strength)
            
            # Calcular confianza
            confidence = self._calculate_decision_confidence(decision, hand_strength)
            
            # Actualizar estadísticas
            self._update_stats(confidence)
            
            return {
                "action": decision["action"],
                "amount": decision.get("amount", 0),
                "confidence": confidence,
                "reason": decision["reason"],
                "alternatives": decision.get("alternatives", []),
                "hand_strength": str(hand_strength),
                "equity": hand_strength.equity,
                "decision_id": self.decisions_made
            }
            
        except Exception as e:
            print(f"❌ Error en make_decision: {e}")
            # Decisión por defecto en caso de error
            return {
                "action": "CHECK" if "check" in game_state.get('available_actions', {}) else "FOLD",
                "amount": 0,
                "confidence": 0.3,
                "reason": f"Error en análisis: {str(e)[:50]}",
                "alternatives": ["FOLD", "CHECK"],
                "hand_strength": "Desconocida",
                "equity": 0.5,
                "decision_id": self.decisions_made
            }
    
    def _preflop_decision(self, hero_cards: List[str], position: str, 
                         pot: float, hand_strength: HandStrength, 
                         available_actions: Dict) -> Dict:
        """Tomar decisión preflop"""
        # Verificar si la mano está en el rango para la posición
        hand_str = ''.join(sorted([c[0] for c in hero_cards]))
        suited = hero_cards[0][-1] == hero_cards[1][-1] if len(hero_cards) == 2 else False
        
        if suited:
            hand_str += 's'
        
        position_range = self.preflop_ranges.get(position, [])
        
        # Decisión basada en rango y fuerza
        if hand_strength.equity >= 0.75 or hand_str in position_range[:10]:
            # Mano premium
            return {
                "action": "RAISE",
                "amount": pot * 0.75 if pot > 0 else 2.2,  # 2.2BB standard
                "reason": "Mano premium en rango de apertura",
                "alternatives": ["CALL", "FOLD"]
            }
        elif hand_strength.equity >= 0.60 or hand_str in position_range:
            # Mano jugable
            return {
                "action": "CALL" if "call" in available_actions else "CHECK",
                "amount": pot * 0.25 if pot > 0 else 0,
                "reason": "Mano jugable dentro de rango",
                "alternatives": ["RAISE", "FOLD"]
            }
        else:
            # Mano débil
            return {
                "action": "FOLD",
                "amount": 0,
                "reason": "Mano fuera de rango óptimo",
                "alternatives": ["CALL", "CHECK"]
            }
    
    def _postflop_decision(self, hero_cards: List[str], board_cards: List[str],
                          street: str, pot: float, hand_strength: HandStrength,
                          available_actions: Dict) -> Dict:
        """Tomar decisión postflop"""
        
        # Basado en fuerza de mano
        if hand_strength.equity >= 0.80:
            # Mano muy fuerte - value bet
            bet_size = pot * self.postflop_strategies["bet_sizings"]["value"]
            return {
                "action": "BET" if "bet" in available_actions else "RAISE",
                "amount": bet_size,
                "reason": f"Mano fuerte: {hand_strength}",
                "alternatives": ["CHECK", "CALL"]
            }
        elif hand_strength.equity >= 0.60:
            # Mano decente - continuation bet o call
            if street == "flop" and len(board_cards) == 3:
                # C-bet en flop
                cbet_freq = self.postflop_strategies["cbet_frequencies"]["dry"]
                if np.random.random() < cbet_freq:
                    bet_size = pot * self.postflop_strategies["bet_sizings"]["dry"]
                    return {
                        "action": "BET",
                        "amount": bet_size,
                        "reason": f"C-bet estándar con {hand_strength}",
                        "alternatives": ["CHECK", "FOLD"]
                    }
            
            return {
                "action": "CALL" if "call" in available_actions else "CHECK",
                "amount": pot * 0.33 if pot > 0 else 0,
                "reason": f"Mano jugable: {hand_strength}",
                "alternatives": ["FOLD", "RAISE"]
            }
        elif hand_strength.equity >= 0.40:
            # Mano marginal - bluff o fold
            bluff_freq = 0.3  # 30% de bluffs
            if np.random.random() < bluff_freq:
                bet_size = pot * self.postflop_strategies["bet_sizings"]["bluff"]
                return {
                    "action": "BET",
                    "amount": bet_size,
                    "reason": "Bluff balanceado",
                    "alternatives": ["FOLD", "CHECK"]
                }
            else:
                return {
                    "action": "FOLD",
                    "amount": 0,
                    "reason": "Mano demasiado débil para continuar",
                    "alternatives": ["CHECK", "CALL"]
                }
        else:
            # Mano muy débil
            return {
                "action": "FOLD",
                "amount": 0,
                "reason": "Mano sin valor",
                "alternatives": ["CHECK", "CALL"]
            }
    
    def _adjust_decision_by_factors(self, decision: Dict, hand_strength: HandStrength) -> Dict:
        """Ajustar decisión basado en factores de agresión/tightness"""
        action = decision["action"]
        
        # Ajustar por agresión
        if self.aggression_factor > 1.0:
            # Más agresivo
            if action in ["CALL", "CHECK"]:
                # Convertir algunos calls/checks en raises/bets
                if hand_strength.equity > 0.5 and np.random.random() < 0.3:
                    decision["action"] = "RAISE" if action == "CALL" else "BET"
                    decision["amount"] = decision.get("amount", 0) * 1.5
                    decision["reason"] += " (ajustado: modo agresivo)"
        
        elif self.aggression_factor < 1.0:
            # Más pasivo
            if action in ["RAISE", "BET"]:
                # Convertir algunos raises/bets en calls/checks
                if hand_strength.equity < 0.7 and np.random.random() < 0.3:
                    decision["action"] = "CALL" if action == "RAISE" else "CHECK"
                    decision["amount"] = 0
                    decision["reason"] += " (ajustado: modo pasivo)"
        
        # Ajustar por tightness
        if self.tightness_factor > 1.0:
            # Más tight
            if action in ["CALL", "RAISE", "BET"]:
                if hand_strength.equity < 0.6 and np.random.random() < 0.4:
                    decision["action"] = "FOLD"
                    decision["amount"] = 0
                    decision["reason"] += " (ajustado: modo tight)"
        
        elif self.tightness_factor < 1.0:
            # Más loose
            if action == "FOLD":
                if hand_strength.equity > 0.3 and np.random.random() < 0.3:
                    decision["action"] = "CALL"
                    decision["reason"] += " (ajustado: modo loose)"
        
        return decision
    
    def _calculate_decision_confidence(self, decision: Dict, hand_strength: HandStrength) -> float:
        """Calcular confianza en la decisión"""
        base_confidence = hand_strength.equity
        
        # Ajustar por acción
        action_confidence = {
            "FOLD": 0.8,
            "CHECK": 0.7,
            "CALL": 0.75,
            "RAISE": 0.65,
            "BET": 0.60
        }.get(decision["action"], 0.5)
        
        # Confianza combinada
        confidence = (base_confidence * 0.6) + (action_confidence * 0.4)
        
        # Limitar entre 0.1 y 0.95
        return max(0.1, min(0.95, confidence))
    
    def _update_stats(self, confidence: float):
        """Actualizar estadísticas"""
        # Promedio móvil de confianza
        if self.decisions_made == 1:
            self.average_confidence = confidence
        else:
            self.average_confidence = (
                (self.average_confidence * (self.decisions_made - 1) + confidence) 
                / self.decisions_made
            )
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas del motor"""
        return {
            "decisions_made": self.decisions_made,
            "average_confidence": round(self.average_confidence, 3),
            "aggression_factor": self.aggression_factor,
            "tightness_factor": self.tightness_factor
        }
    
    def save_config(self):
        """Guardar configuración del motor"""
        config = {
            "aggression_factor": self.aggression_factor,
            "tightness_factor": self.tightness_factor,
            "preflop_ranges_summary": {
                pos: len(ranges) for pos, ranges in self.preflop_ranges.items()
            },
            "stats": self.get_stats()
        }
        
        config_path = Path("config/poker_engine_config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuración de motor guardada: {config_path}")

# ============================================================================
# PRUEBAS
# ============================================================================

def test_poker_engine():
    """Probar el motor de decisiones"""
    print("🧪 TEST: Poker Engine")
    print("=" * 60)
    
    try:
        # Crear motor
        engine = PokerEngine(aggression_factor=1.0, tightness_factor=1.0)
        
        # Estados de juego de prueba
        test_states = [
            {
                "hero_cards": ["Ah", "Ks"],
                "board_cards": [],
                "current_street": "preflop",
                "hero_position": "BTN",
                "pot_amount": 5.0,
                "hero_stack": 100.0,
                "available_actions": {"fold": True, "call": True, "raise": True}
            },
            {
                "hero_cards": ["7c", "2d"],
                "board_cards": ["Ah", "Ks", "Qd"],
                "current_street": "flop",
                "hero_position": "BB",
                "pot_amount": 15.0,
                "hero_stack": 85.0,
                "available_actions": {"fold": True, "check": True, "bet": True}
            },
            {
                "hero_cards": ["Th", "Th"],
                "board_cards": ["9s", "8d", "2c", "Jh"],
                "current_street": "turn",
                "hero_position": "CO",
                "pot_amount": 25.0,
                "hero_stack": 75.0,
                "available_actions": {"fold": True, "call": True, "raise": True}
            }
        ]
        
        print("🎯 Probando decisiones...")
        
        for i, state in enumerate(test_states):
            print(f"\n📋 Estado de prueba {i+1}:")
            print(f"   Hero: {state['hero_cards']}")
            print(f"   Board: {state['board_cards']}")
            print(f"   Street: {state['current_street']}")
            print(f"   Posición: {state['hero_position']}")
            
            # Tomar decisión
            decision = engine.make_decision(state)
            
            print(f"   🤖 DECISIÓN: {decision['action']}")
            print(f"      Cantidad: ${decision.get('amount', 0):.2f}")
            print(f"      Confianza: {decision['confidence']:.1%}")
            print(f"      Razón: {decision['reason']}")
            print(f"      Fuerza de mano: {decision['hand_strength']}")
        
        # Mostrar estadísticas
        print(f"\n📊 Estadísticas del motor:")
        stats = engine.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Guardar configuración
        engine.save_config()
        
        print("\n✅ Test de motor completado")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de motor: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_poker_engine()

# poker_engine.py - MÉTODO AÑADIDO
# ... (código existente)

class PokerEngine:
    def __init__(self, aggression=1.0, tightness=1.0):
        self.aggression = max(0.5, min(2.0, aggression))
        self.tightness = max(0.5, min(2.0, tightness))
        self.decision_cache = {}
        print(f"✅ PokerEngine inicializado (agresión: {self.aggression}, tightness: {self.tightness})")
    
    def analyze_hand(self, hole_cards=None, community_cards=None, pot_size=0, position="middle"):
        """Analizar una mano y retornar recomendación GTO (MÉTODO NUEVO)"""
        
        print(f"🧠 Analizando mano...")
        print(f"   Cartas propias: {hole_cards}")
        print(f"   Cartas comunitarias: {community_cards}")
        print(f"   Pozo: {pot_size}")
        print(f"   Posición: {position}")
        
        # Validar entrada
        if not hole_cards or len(hole_cards) < 2:
            return self._get_default_decision("CHECK", "Esperando cartas", 0.5)
        
        # Calcular fuerza de la mano
        hand_strength = self._calculate_hand_strength(hole_cards, community_cards)
        
        # Ajustar por posición
        position_multiplier = self._get_position_multiplier(position)
        
        # Ajustar por tamaño del pozo
        pot_multiplier = self._get_pot_multiplier(pot_size)
        
        # Calcular decisión
        decision = self._calculate_decision(
            hand_strength, 
            position_multiplier, 
            pot_multiplier
        )
        
        return decision
    
    def _calculate_hand_strength(self, hole_cards, community_cards):
        """Calcular fuerza aproximada de la mano"""
        # Mapeo básico de cartas
        rank_values = {
            '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
            '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13
        }
        
        # Calcular valor base
        total_value = 0
        for card in hole_cards:
            if len(card) >= 2:
                rank = card[0].upper()
                if rank in rank_values:
                    total_value += rank_values[rank]
        
        # Ajustar por parejas, etc.
        if len(hole_cards) >= 2:
            rank1 = hole_cards[0][0].upper() if hole_cards[0] else ''
            rank2 = hole_cards[1][0].upper() if hole_cards[1] else ''
            
            if rank1 == rank2:
                total_value *= 1.5  # Pareja
            elif self._are_cards_suited(hole_cards):
                total_value *= 1.2  # Mismo palo
            elif self._are_cards_connected(hole_cards):
                total_value *= 1.1  # Cartas conectadas
        
        # Normalizar a 0-1
        max_value = 26 * 1.5  # Máximo posible (AA)
        strength = min(1.0, total_value / max_value)
        
        return strength
    
    def _are_cards_suited(self, cards):
        """Verificar si las cartas son del mismo palo"""
        if len(cards) < 2:
            return False
        suits = [card[-1].lower() for card in cards if len(card) >= 2]
        return len(set(suits)) == 1
    
    def _are_cards_connected(self, cards):
        """Verificar si las cartas están conectadas"""
        if len(cards) < 2:
            return False
        
        rank_order = '23456789TJQKA'
        ranks = []
        
        for card in cards:
            if len(card) >= 2:
                rank = card[0].upper()
                if rank in rank_order:
                    ranks.append(rank_order.index(rank))
        
        if len(ranks) < 2:
            return False
        
        ranks.sort()
        return abs(ranks[0] - ranks[1]) <= 1
    
    def _get_position_multiplier(self, position):
        """Multiplicador basado en posición"""
        multipliers = {
            'early': 0.8,
            'middle': 1.0,
            'late': 1.2,
            'button': 1.3
        }
        return multipliers.get(position.lower(), 1.0)
    
    def _get_pot_multiplier(self, pot_size):
        """Multiplicador basado en tamaño del pozo"""
        if pot_size <= 0:
            return 1.0
        elif pot_size < 500:
            return 0.9
        elif pot_size > 2000:
            return 1.1
        else:
            return 1.0
    
    def _calculate_decision(self, hand_strength, position_multiplier, pot_multiplier):
        """Calcular decisión final"""
        # Valor base
        base_value = hand_strength * position_multiplier * pot_multiplier
        
        # Ajustar por agresividad
        adjusted_value = base_value * self.aggression
        
        # Determinar acción
        if adjusted_value > 0.8:
            action = "RAISE"
            confidence = min(0.95, adjusted_value)
            reason = "Mano muy fuerte"
        elif adjusted_value > 0.6:
            action = "CALL"
            confidence = adjusted_value * 0.9
            reason = "Mano buena"
        elif adjusted_value > 0.4:
            action = "CHECK"
            confidence = adjusted_value * 0.8
            reason = "Mano promedio"
        elif adjusted_value > 0.2:
            action = "FOLD"
            confidence = (1 - adjusted_value) * 0.7
            reason = "Mano débil"
        else:
            action = "FOLD"
            confidence = 0.9
            reason = "Mano muy débil"
        
        # Ajustar por tightness
        if self.tightness > 1.2 and action in ["CALL", "RAISE"]:
            if adjusted_value < 0.7:
                action = "FOLD"
                reason = f"{reason} (jugador tight)"
        
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand_strength": hand_strength,
            "adjusted_value": adjusted_value,
            "position_multiplier": position_multiplier,
            "pot_multiplier": pot_multiplier
        }
    
    def _get_default_decision(self, action, reason, confidence):
        """Retornar decisión por defecto"""
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "hand_strength": 0.5,
            "adjusted_value": 0.5
        }
    
    def get_recommendation(self, game_state):
        """Alias para compatibilidad"""
        return self.analyze_hand(
            hole_cards=game_state.get('hole_cards'),
            community_cards=game_state.get('community_cards'),
            pot_size=game_state.get('pot_size', 0),
            position=game_state.get('position', 'middle')
        )