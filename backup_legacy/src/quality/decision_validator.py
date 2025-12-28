"""
Archivo: decision_validator.py
Ruta: src/quality/decision_validator.py
Sistema de validación y calibración de decisiones de poker
Basado en principios GTO y estrategia profesional
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum

class DecisionQuality(Enum):
    """Niveles de calidad de decisión"""
    EXCELLENT = "EXCELENTE"  # +EV claro, estrategia óptima
    GOOD = "BUENA"          # +EV, estrategia sólida
    ACCEPTABLE = "ACEPTABLE" # Marginal, depende del contexto
    QUESTIONABLE = "CUESTIONABLE" # -EV potencial
    BAD = "MALA"            # -EV claro, error estratégico

class DecisionValidator:
    """
    Validador profesional de decisiones de poker
    Basado en 20+ años de experiencia y principios GTO
    """
    
    def __init__(self, platform="ggpoker"):
        self.platform = platform
        self.validation_rules = self.load_validation_rules()
        self.calibration_data = self.load_calibration_data()
        
        # Historial de validaciones
        self.validation_history = []
        self.stats = {
            'total_validations': 0,
            'excellent': 0,
            'good': 0,
            'acceptable': 0,
            'questionable': 0,
            'bad': 0
        }
    
    def load_validation_rules(self) -> Dict:
        """Cargar reglas de validación por situación"""
        
        return {
            'preflop': {
                'position_ranges': self.load_position_ranges(),
                'sizing_rules': self.load_sizing_rules(),
                'common_mistakes': self.load_common_mistakes()
            },
            'postflop': {
                'cbet_frequencies': self.load_cbet_frequencies(),
                'barreling_rules': self.load_barreling_rules(),
                'value_betting': self.load_value_betting_rules()
            },
            'tournament': {
                'icm_adjustments': self.load_icm_adjustments(),
                'bubble_play': self.load_bubble_rules(),
                'final_table': self.load_final_table_rules()
            }
        }
    
    def load_calibration_data(self) -> Dict:
        """Cargar datos de calibración de rangos y equity"""
        return {
            'hand_strengths': {
                'AA': 1.00, 'KK': 0.95, 'QQ': 0.90, 'JJ': 0.85, 'TT': 0.80,
                'AKs': 0.82, 'AQs': 0.78, 'AJs': 0.75, 'ATs': 0.72,
                'AKo': 0.75, 'AQo': 0.70, 'AJo': 0.65,
                'KQs': 0.68, 'KJs': 0.65, 'KTs': 0.62,
                'QJs': 0.63, 'QTs': 0.60, 'JTs': 0.58,
                'T9s': 0.55, '98s': 0.52, '87s': 0.50, '76s': 0.48
            },
            'equity_requirements': {
                'call_preflop': 0.40,  # Equity mínima para call preflop
                'call_flop': 0.35,     # Equity mínima para call flop
                'call_turn': 0.30,     # Equity mínima para call turn
                'call_river': 0.25,    # Equity mínima para call river
                'semi_bluff': 0.25,    # Equity mínima para semi-bluff
                'value_bet': 0.55      # Equity mínima para value bet
            },
            'sizing_standards': {
                'preflop_open': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                '3bet_ip': {'min': 2.8, 'max': 3.5, 'optimal': 3.0},
                '3bet_oop': {'min': 3.5, 'max': 4.5, 'optimal': 3.8},
                'cbet_flop': {'min': 0.25, 'max': 0.75, 'optimal': 0.33},
                'turn_barrel': {'min': 0.50, 'max': 0.90, 'optimal': 0.65},
                'river_value': {'min': 0.50, 'max': 1.20, 'optimal': 0.70}
            }
        }
    
    def validate_decision(self, game_state: Dict, decision: Dict) -> Dict:
        """
        Validar una decisión completa
        
        Args:
            game_state: Estado del juego
            decision: Decisión a validar
            
        Returns:
            Dict con análisis de calidad
        """
        validation_result = {
            'quality': DecisionQuality.ACCEPTABLE.value,
            'score': 70,  # 0-100
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'gto_comparison': {},
            'exploitative_adjustment': None,
            'confidence': 0
        }
        
        # 1. Validación básica
        basic_validation = self.validate_basics(game_state, decision)
        validation_result.update(basic_validation)
        
        # 2. Validación específica por calle
        if game_state.get('street') == 'preflop':
            preflop_validation = self.validate_preflop(game_state, decision)
            validation_result.update(preflop_validation)
        else:
            postflop_validation = self.validate_postflop(game_state, decision)
            validation_result.update(postflop_validation)
        
        # 3. Validación de tamaño de apuesta
        sizing_validation = self.validate_bet_sizing(game_state, decision)
        validation_result.update(sizing_validation)
        
        # 4. Validación de rango
        range_validation = self.validate_range(game_state, decision)
        validation_result.update(range_validation)
        
        # 5. Validación de equity y odds
        equity_validation = self.validate_equity(game_state, decision)
        validation_result.update(equity_validation)
        
        # 6. Calcular puntuación final
        final_score = self.calculate_final_score(validation_result)
        validation_result['score'] = final_score
        validation_result['quality'] = self.score_to_quality(final_score).value
        
        # 7. Actualizar estadísticas
        self.update_stats(validation_result['quality'])
        
        # 8. Guardar en historial
        self.save_to_history(game_state, decision, validation_result)
        
        return validation_result
    
    def validate_basics(self, game_state: Dict, decision: Dict) -> Dict:
        """Validación básica de la decisión"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        action = decision.get('action', '').upper()
        
        # Verificar acción válida
        valid_actions = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE', 'ALL-IN']
        if action not in valid_actions:
            result['weaknesses'].append(f"Acción inválida: {action}")
            result['suggestions'].append("Usar solo acciones estándar de poker")
        
        # Verificar consistencia
        if action in ['BET', 'RAISE'] and not decision.get('size'):
            result['weaknesses'].append(f"Acción {action} sin tamaño especificado")
            result['suggestions'].append("Especificar tamaño de apuesta")
        
        # Verificar lógica básica
        if action == 'FOLD' and game_state.get('bet_to_call', 0) == 0:
            result['weaknesses'].append("Fold cuando no hay que pagar nada")
            result['suggestions'].append("Considerar CHECK en lugar de FOLD")
        
        if action == 'CHECK' and game_state.get('bet_to_call', 0) > 0:
            result['weaknesses'].append("Intentar check cuando hay apuesta que pagar")
            result['suggestions'].append("No se puede check con apuesta pendiente")
        
        return result
    
    def validate_preflop(self, game_state: Dict, decision: Dict) -> Dict:
        """Validación específica preflop"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        position = game_state.get('position', '').upper()
        action = decision.get('action', '').upper()
        hand_cards = game_state.get('hero_cards', [])
        
        # Convertir mano a formato de rango
        hand_str = self.cards_to_range_format(hand_cards)
        
        # Cargar rangos por posición
        position_ranges = self.load_position_ranges()
        
        if position in position_ranges:
            optimal_range = position_ranges[position]
            
            # Verificar si mano está en rango óptimo
            if hand_str in optimal_range['premium']:
                if action != 'RAISE' and action != 'ALL-IN':
                    result['weaknesses'].append(
                        f"Mano premium {hand_str} pero acción: {action}"
                    )
                    result['suggestions'].append("Con mano premium, RAISE es estándar")
                else:
                    result['strengths'].append(
                        f"Mano premium {hand_str}, acción correcta: {action}"
                    )
            
            elif hand_str in optimal_range['strong']:
                if action == 'FOLD' and not game_state.get('action_to_us', False):
                    result['weaknesses'].append(
                        f"Mano fuerte {hand_str} fold desde {position}"
                    )
                    result['suggestions'].append("Considerar RAISE con mano fuerte")
            
            elif hand_str in optimal_range['marginal']:
                if action == 'RAISE' and position in ['UTG', 'MP']:
                    result['weaknesses'].append(
                        f"Mano marginal {hand_str}, RAISE desde {position} muy loose"
                    )
                    result['suggestions'].append("Considerar FOLD o CALL si hay acción")
            
            elif hand_str in optimal_range['weak']:
                if action != 'FOLD' and position in ['UTG', 'MP']:
                    result['weaknesses'].append(
                        f"Mano débil {hand_str}, {action} desde {position}"
                    )
                    result['suggestions'].append("Fold con manos débiles desde EP")
        
        # Validar tamaño de raise preflop
        if action == 'RAISE':
            sizing_result = self.validate_preflop_sizing(game_state, decision)
            result['weaknesses'].extend(sizing_result.get('weaknesses', []))
            result['strengths'].extend(sizing_result.get('strengths', []))
            result['suggestions'].extend(sizing_result.get('suggestions', []))
        
        return result
    
    def validate_preflop_sizing(self, game_state: Dict, decision: Dict) -> Dict:
        """Validar tamaño de apuesta preflop"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        position = game_state.get('position', '').upper()
        size_str = decision.get('size', '')
        
        if 'BB' in size_str:
            try:
                # Extraer número de BBs
                size_bb = float(size_str.replace('BB', '').strip())
                
                # Tamaños estándar por posición
                standard_sizes = {
                    'UTG': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'MP': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'CO': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'BTN': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'SB': {'min': 2.5, 'max': 4.0, 'optimal': 3.0}
                }
                
                if position in standard_sizes:
                    std = standard_sizes[position]
                    
                    if size_bb < std['min']:
                        result['weaknesses'].append(
                            f"Raise muy pequeño: {size_bb}BB desde {position}"
                        )
                        result['suggestions'].append(
                            f"Tamaño estándar: {std['optimal']}BB"
                        )
                    elif size_bb > std['max']:
                        result['weaknesses'].append(
                            f"Raise muy grande: {size_bb}BB desde {position}"
                        )
                        result['suggestions'].append(
                            f"Tamaño estándar: {std['optimal']}BB"
                        )
                    elif abs(size_bb - std['optimal']) < 0.3:
                        result['strengths'].append(
                            f"Tamaño óptimo: {size_bb}BB desde {position}"
                        )
                    else:
                        result['suggestions'].append(
                            f"Tamaño {size_bb}BB OK, óptimo: {std['optimal']}BB"
                        )
            
            except ValueError:
                result['weaknesses'].append(f"Tamaño inválido: {size_str}")
        
        return result
    
    def validate_postflop(self, game_state: Dict, decision: Dict) -> Dict:
        """Validación específica postflop"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        street = game_state.get('street', '').lower()
        action = decision.get('action', '').upper()
        pot_size = game_state.get('pot_size', 0)
        bet_to_call = game_state.get('bet_to_call', 0)
        
        # Validar decisiones de call basadas en pot odds
        if action == 'CALL' and bet_to_call > 0 and pot_size > 0:
            pot_odds = bet_to_call / (pot_size + bet_to_call)
            
            # Equity estimada requerida
            required_equity = self.calibration_data['equity_requirements'][f'call_{street}']
            
            if pot_odds > required_equity + 0.1:  # Malas odds
                result['weaknesses'].append(
                    f"Call con malas pot odds: {pot_odds:.1%} (necesitas ~{required_equity:.0%})"
                )
                result['suggestions'].append("Considerar FOLD con odds insuficientes")
            elif pot_odds < required_equity - 0.05:  # Buenas odds
                result['strengths'].append(
                    f"Call con buenas pot odds: {pot_odds:.1%}"
                )
        
        # Validar c-bets en flop
        if street == 'flop' and action == 'BET':
            cbet_validation = self.validate_cbet(game_state, decision)
            result.update(cbet_validation)
        
        # Validar barrels en turn/river
        if street in ['turn', 'river'] and action == 'BET':
            barrel_validation = self.validate_barrel(game_state, decision)
            result.update(barrel_validation)
        
        # Validar value bets
        if action in ['BET', 'RAISE'] and street == 'river':
            value_validation = self.validate_value_bet(game_state, decision)
            result.update(value_validation)
        
        return result
    
    def validate_cbet(self, game_state: Dict, decision: Dict) -> Dict:
        """Validar continuation bet en flop"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        board_cards = game_state.get('board_cards', [])
        position = game_state.get('position', '').upper()
        
        # Evaluar textura del flop
        texture = self.analyze_board_texture(board_cards)
        
        # Frecuencias de c-bet recomendadas por textura
        cbet_frequencies = {
            'dry': 0.70,      # Flops secos: alta frecuencia
            'wet': 0.40,      # Flops húmedos: baja frecuencia
            'paired': 0.30,   # Flops paired: muy baja frecuencia
            'monotone': 0.20  # Flops monotone: frecuencia mínima
        }
        
        # Tamaño de c-bet recomendado
        recommended_sizes = {
            'dry': 0.33,      # 33% del pot
            'wet': 0.50,      # 50% del pot
            'paired': 0.66,   # 66% del pot (o check)
            'monotone': 0.75  # 75% del pot (o check)
        }
        
        texture_type = texture.get('type', 'dry')
        
        # Verificar si c-bet es apropiado
        if position in ['BTN', 'CO']:  # Posiciones favorables
            result['strengths'].append(
                f"C-bet desde {position} en flop {texture_type}"
            )
        elif position in ['SB', 'BB']:  # Posiciones desfavorables
            if texture_type in ['wet', 'paired', 'monotone']:
                result['suggestions'].append(
                    f"Considerar check OOP en flop {texture_type}"
                )
        
        # Verificar tamaño de c-bet
        size_str = decision.get('size', '')
        if '%' in size_str or 'pot' in size_str.lower():
            try:
                size_pct = self.extract_bet_size_percentage(size_str)
                recommended = recommended_sizes.get(texture_type, 0.33) * 100
                
                if abs(size_pct - recommended) > 15:
                    result['suggestions'].append(
                        f"C-bet size: {size_pct:.0f}% (recomendado: {recommended:.0f}% para flop {texture_type})"
                    )
                else:
                    result['strengths'].append(
                        f"Tamaño de c-bet óptimo: {size_pct:.0f}%"
                    )
            except:
                pass
        
        return result
    
    def validate_bet_sizing(self, game_state: Dict, decision: Dict) -> Dict:
        """Validar tamaño de apuesta en general"""
        result = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'sizing_analysis': {}
        }
        
        action = decision.get('action', '').upper()
        size_str = decision.get('size', '')
        street = game_state.get('street', '').lower()
        pot_size = game_state.get('pot_size', 0)
        
        if action in ['BET', 'RAISE'] and size_str:
            try:
                # Convertir tamaño a porcentaje del pot
                size_pct = self.extract_bet_size_percentage(size_str)
                
                # Rangos óptimos por calle
                optimal_ranges = {
                    'preflop': {'min': 200, 'max': 250, 'optimal': 220},  # En % de BB
                    'flop': {'min': 25, 'max': 75, 'optimal': 33},
                    'turn': {'min': 50, 'max': 90, 'optimal': 65},
                    'river': {'min': 50, 'max': 120, 'optimal': 70}
                }
                
                if street in optimal_ranges:
                    optimal = optimal_ranges[street]
                    
                    result['sizing_analysis'] = {
                        'actual': size_pct,
                        'optimal_min': optimal['min'],
                        'optimal_max': optimal['max'],
                        'optimal_target': optimal['optimal'],
                        'street': street
                    }
                    
                    if size_pct < optimal['min']:
                        result['weaknesses'].append(
                            f"Apuesta muy pequeña: {size_pct:.0f}% del pot"
                        )
                        result['suggestions'].append(
                            f"Tamaño recomendado: {optimal['optimal']:.0f}%"
                        )
                    elif size_pct > optimal['max']:
                        result['weaknesses'].append(
                            f"Apuesta muy grande: {size_pct:.0f}% del pot"
                        )
                        result['suggestions'].append(
                            f"Tamaño recomendado: {optimal['optimal']:.0f}%"
                        )
                    elif abs(size_pct - optimal['optimal']) < 10:
                        result['strengths'].append(
                            f"Tamaño óptimo: {size_pct:.0f}% del pot"
                        )
                    else:
                        result['suggestions'].append(
                            f"Tamaño {size_pct:.0f}% OK, óptimo: {optimal['optimal']:.0f}%"
                        )
            
            except ValueError:
                result['weaknesses'].append(f"Tamaño inválido: {size_str}")
        
        return result
    
    def validate_range(self, game_state: Dict, decision: Dict) -> Dict:
        """Validar consistencia con rango y balance"""
        result = {
            'range_analysis': {},
            'balance_check': None
        }
        
        # Análisis simplificado de rango
        # En implementación real, usaríamos solvers para esto
        
        return result
    
    def validate_equity(self, game_state: Dict, decision: Dict) -> Dict:
        """Validar decisiones basadas en equity"""
        result = {
            'equity_analysis': {},
            'odds_evaluation': None
        }
        
        hand_cards = game_state.get('hero_cards', [])
        board_cards = game_state.get('board_cards', [])
        pot_size = game_state.get('pot_size', 0)
        bet_to_call = game_state.get('bet_to_call', 0)
        action = decision.get('action', '').upper()
        
        # Calcular equity estimada
        estimated_equity = self.estimate_hand_equity(hand_cards, board_cards)
        
        # Calcular pot odds si hay apuesta que pagar
        if bet_to_call > 0:
            pot_odds = bet_to_call / (pot_size + bet_to_call) if pot_size > 0 else 1.0
            
            result['equity_analysis'] = {
                'estimated_equity': estimated_equity,
                'pot_odds': pot_odds,
                'profitable_call': estimated_equity > pot_odds
            }
            
            if action == 'CALL' and estimated_equity < pot_odds - 0.05:
                result['weaknesses'] = result.get('weaknesses', [])
                result['weaknesses'].append(
                    f"Call -EV: Equity {estimated_equity:.1%} < Pot Odds {pot_odds:.1%}"
                )
            elif action == 'FOLD' and estimated_equity > pot_odds + 0.1:
                result['weaknesses'] = result.get('weaknesses', [])
                result['weaknesses'].append(
                    f"Fold +EV perdido: Equity {estimated_equity:.1%} > Pot Odds {pot_odds:.1%}"
                )
        
        return result
    
    def analyze_board_texture(self, board_cards: List[str]) -> Dict:
        """Analizar textura del board"""
        if len(board_cards) < 3:
            return {'type': 'unknown', 'description': 'Board incompleto'}
        
        # Extraer valores y palos
        values = []
        suits = []
        
        for card in board_cards[:3]:  # Solo flop para textura
            if len(card) >= 2:
                values.append(card[0].upper())
                suits.append(card[-1].lower())
        
        # Determinar tipo de textura
        texture_info = {
            'type': 'dry',
            'description': 'Flop estándar',
            'connectedness': 'low',
            'suitedness': 'rainbow'
        }
        
        # Verificar si es paired
        if len(values) >= 2 and values[0] == values[1]:
            texture_info['type'] = 'paired'
            texture_info['description'] = 'Flop paired'
        
        # Verificar conectividad
        value_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            value_order[str(i)] = i
        
        numeric_values = []
        for v in values:
            numeric_values.append(value_order.get(v, 0))
        
        numeric_values.sort()
        
        gaps = 0
        for i in range(len(numeric_values) - 1):
            gap = numeric_values[i+1] - numeric_values[i]
            if gap <= 2:
                texture_info['connectedness'] = 'high'
                texture_info['type'] = 'wet'
                texture_info['description'] = 'Flop conectado'
        
        # Verificar suitedness
        if len(set(suits)) == 1:
            texture_info['suitedness'] = 'monotone'
            texture_info['type'] = 'monotone'
            texture_info['description'] = 'Flop monotone'
        elif len(set(suits)) == 2:
            texture_info['suitedness'] = 'twotone'
            texture_info['type'] = 'wet'
        
        return texture_info
    
    def extract_bet_size_percentage(self, size_str: str) -> float:
        """Extraer porcentaje de tamaño de apuesta del string"""
        
        # Formato: "33% pot", "0.5x pot", "2.2BB", etc.
        
        if '%' in size_str:
            # Formato porcentaje: "33% pot"
            try:
                return float(size_str.split('%')[0].strip())
            except:
                pass
        elif 'pot' in size_str.lower():
            # Formato multiplicador: "0.5x pot"
            try:
                multiplier = float(size_str.split('x')[0].strip())
                return multiplier * 100
            except:
                pass
        elif 'BB' in size_str.upper():
            # Formato BBs: "2.2BB"
            try:
                bbs = float(size_str.upper().replace('BB', '').strip())
                return bbs * 100  # Convertir a % del pot (aproximado)
            except:
                pass
        
        return 0.0
    
    def estimate_hand_equity(self, hero_cards: List[str], board_cards: List[str]) -> float:
        """Estimar equity de la mano (simplificado)"""
        
        if not hero_cards or len(hero_cards) < 2:
            return 0.0
        
        # Convertir a formato de rango
        hand_str = self.cards_to_range_format(hero_cards)
        
        # Equity aproximada basada en fuerza de mano
        hand_strengths = self.calibration_data['hand_strengths']
        
        if hand_str in hand_strengths:
            base_equity = hand_strengths[hand_str]
        else:
            # Estimar basado en componentes
            base_equity = 0.5
        
        # Ajustar por board
        if board_cards:
            # Reducir equity si el board es peligroso
            texture = self.analyze_board_texture(board_cards)
            if texture['type'] in ['wet', 'paired', 'monotone']:
                base_equity *= 0.8
        
        return min(0.95, max(0.05, base_equity))
    
    def cards_to_range_format(self, cards: List[str]) -> str:
        """Convertir cartas a formato de rango (ej: "AKs", "QQ")"""
        if not cards or len(cards) < 2:
            return ""
        
        # Ordenar valores
        value_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            value_order[str(i)] = i
        
        val1 = value_order.get(cards[0][0].upper(), 0)
        val2 = value_order.get(cards[1][0].upper(), 0)
        
        if val1 == val2:
            # Pocket pair
            return cards[0][0].upper() + cards[1][0].upper()
        else:
            # Determinar si es suited
            suited = len(cards[0]) > 1 and len(cards[1]) > 1 and cards[0][-1] == cards[1][-1]
            suffix = "s" if suited else "o"
            
            # Ordenar de mayor a menor
            if val1 > val2:
                return cards[0][0].upper() + cards[1][0].upper() + suffix
            else:
                return cards[1][0].upper() + cards[0][0].upper() + suffix
    
    def load_position_ranges(self) -> Dict:
        """Cargar rangos óptimos por posición"""
        return {
            'UTG': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs', 'AQs'],
                'strong': ['99', '88', 'AJs', 'ATs', 'KQs'],
                'marginal': ['77', '66', 'AJo', 'KQo', 'KJs'],
                'weak': ['55-22', 'A9s-A2s', 'KTs', 'QJs', 'JTs']
            },
            'MP': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs', 'AQs', 'AJs'],
                'strong': ['99', '88', '77', 'ATs', 'KQs', 'KJs', 'QJs'],
                'marginal': ['66', '55', 'AJo', 'KQo', 'QJo', 'JTo'],
                'weak': ['44-22', 'A9s-A2s', 'KTs-K9s', 'QTs', 'JTs', 'T9s']
            },
            'CO': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AQs', 'AJs', 'ATs'],
                'strong': ['88', '77', '66', 'A9s', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs', 'JTs'],
                'marginal': ['55', '44', '33', 'AJo', 'KQo', 'QJo', 'JTo', 'T9o'],
                'weak': ['22', 'A8s-A2s', 'K9s-K2s', 'Q9s', 'J9s', 'T9s', '98s']
            },
            'BTN': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AKs', 'AQs', 'AJs', 'ATs', 'A9s'],
                'strong': ['66', '55', '44', '33', '22', 'A8s-A2s', 'KQs', 'KJs', 'KTs', 'K9s', 'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s'],
                'marginal': ['AJo-ATo', 'KQo', 'KJo', 'QJo', 'JTo', 'T9o', '98o'],
                'weak': ['A9o-A2o', 'K9o-K2o', 'Q9o-Q2o', 'J9o-J2o', 'T8o', '97o', '87o']
            }
        }
    
    def calculate_final_score(self, validation_result: Dict) -> int:
        """Calcular puntuación final de calidad"""
        
        base_score = 70  # Puntuación base
        
        # Ajustar por fortalezas y debilidades
        strengths = len(validation_result.get('strengths', []))
        weaknesses = len(validation_result.get('weaknesses', []))
        
        # Bonificación por fortalezas
        base_score += strengths * 5
        
        # Penalización por debilidades
        base_score -= weaknesses * 10
        
        # Ajustar por sugerencias (menos grave que debilidades)
        suggestions = len(validation_result.get('suggestions', []))
        base_score -= suggestions * 3
        
        # Limitar rango
        return max(0, min(100, base_score))
    
    def score_to_quality(self, score: int) -> DecisionQuality:
        """Convertir puntuación a calidad"""
        if score >= 90:
            return DecisionQuality.EXCELLENT
        elif score >= 75:
            return DecisionQuality.GOOD
        elif score >= 60:
            return DecisionQuality.ACCEPTABLE
        elif score >= 40:
            return DecisionQuality.QUESTIONABLE
        else:
            return DecisionQuality.BAD
    
    def update_stats(self, quality: str):
        """Actualizar estadísticas de validación"""
        self.stats['total_validations'] += 1
        
        if quality == DecisionQuality.EXCELLENT.value:
            self.stats['excellent'] += 1
        elif quality == DecisionQuality.GOOD.value:
            self.stats['good'] += 1
        elif quality == DecisionQuality.ACCEPTABLE.value:
            self.stats['acceptable'] += 1
        elif quality == DecisionQuality.QUESTIONABLE.value:
            self.stats['questionable'] += 1
        elif quality == DecisionQuality.BAD.value:
            self.stats['bad'] += 1
    
    def save_to_history(self, game_state: Dict, decision: Dict, validation: Dict):
        """Guardar validación en historial"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'game_state': game_state,
            'decision': decision,
            'validation': validation,
            'quality': validation['quality'],
            'score': validation['score']
        }
        
        self.validation_history.append(record)
        
        # Limitar tamaño del historial
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]
    
    def get_validation_stats(self) -> Dict:
        """Obtener estadísticas de validación"""
        total = self.stats['total_validations']
        
        if total == 0:
            percentages = {k: 0 for k in self.stats.keys() if k != 'total_validations'}
        else:
            percentages = {
                'excellent': self.stats['excellent'] / total * 100,
                'good': self.stats['good'] / total * 100,
                'acceptable': self.stats['acceptable'] / total * 100,
                'questionable': self.stats['questionable'] / total * 100,
                'bad': self.stats['bad'] / total * 100
            }
        
        return {
            'total_validations': total,
            'percentages': percentages,
            'average_score': self.calculate_average_score(),
            'recent_trend': self.get_recent_trend()
        }
    
    def calculate_average_score(self) -> float:
        """Calcular puntuación promedio del historial"""
        if not self.validation_history:
            return 0.0
        
        total_score = sum(record['score'] for record in self.validation_history)
        return total_score / len(self.validation_history)
    
    def get_recent_trend(self) -> str:
        """Obtener tendencia reciente de calidad"""
        if len(self.validation_history) < 10:
            return "INSUFICIENT_DATA"
        
        # Últimas 10 validaciones
        recent = self.validation_history[-10:]
        recent_scores = [r['score'] for r in recent]
        
        # Primera mitad vs segunda mitad
        first_half = recent_scores[:5]
        second_half = recent_scores[5:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        if avg_second > avg_first + 5:
            return "IMPROVING"
        elif avg_second < avg_first - 5:
            return "DECLINING"
        else:
            return "STABLE"
    
    def generate_quality_report(self) -> str:
        """Generar reporte de calidad"""
        stats = self.get_validation_stats()
        
        report = []
        report.append("=" * 60)
        report.append("📊 REPORTE DE CALIDAD - DECISIONES DE POKER")
        report.append("=" * 60)
        report.append(f"Total decisiones validadas: {stats['total_validations']}")
        report.append(f"Puntuación promedio: {stats['average_score']:.1f}/100")
        report.append(f"Tendencia: {stats['recent_trend']}")
        report.append("")
        report.append("📈 DISTRIBUCIÓN DE CALIDAD:")
        report.append(f"  Excelente:  {stats['percentages']['excellent']:5.1f}%")
        report.append(f"  Buena:      {stats['percentages']['good']:5.1f}%")
        report.append(f"  Aceptable:  {stats['percentages']['acceptable']:5.1f}%")
        report.append(f"  Cuestionable: {stats['percentages']['questionable']:5.1f}%")
        report.append(f"  Mala:       {stats['percentages']['bad']:5.1f}%")
        report.append("")
        
        # Áreas de mejora
        if self.validation_history:
            recent_weaknesses = []
            for record in self.validation_history[-20:]:
                if 'weaknesses' in record['validation']:
                    recent_weaknesses.extend(record['validation']['weaknesses'])
            
            if recent_weaknesses:
                from collections import Counter
                common_weaknesses = Counter(recent_weaknesses).most_common(3)
                
                report.append("⚠️  ÁREAS DE MEJORA COMUNES:")
                for weakness, count in common_weaknesses:
                    report.append(f"  • {weakness} ({count} veces)")
        
        report.append("=" * 60)
        
        return "\n".join(report)