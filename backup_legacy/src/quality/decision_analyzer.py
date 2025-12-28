"""
Archivo: decision_analyzer.py
Ruta: src/quality/decision_analyzer.py
Analizador avanzado de decisiones con comparación GTO
"""

import json
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class GTOAnalysis:
    """Análisis de teoría de juegos para una decisión"""
    ev: float  # Valor esperado
    frequency: float  # Frecuencia GTO para esta acción
    exploitability: float  # Cuán explotable es la decisión
    indifference_points: List[float]  # Puntos de indiferencia
    range_advantage: float  # Ventaja de rango

class DecisionAnalyzer:
    """Analizador avanzado de decisiones de poker"""
    
    def __init__(self):
        self.gto_baselines = self.load_gto_baselines()
        self.ev_calculator = EVCalculator()
        self.range_analyzer = RangeAnalyzer()
    
    def analyze_decision_gto(self, game_state: Dict, decision: Dict) -> GTOAnalysis:
        """
        Analizar decisión desde perspectiva GTO
        
        Args:
            game_state: Estado del juego
            decision: Decisión a analizar
            
        Returns:
            Análisis GTO
        """
        
        # 1. Calcular EV aproximado
        ev = self.ev_calculator.estimate_ev(game_state, decision)
        
        # 2. Determinar frecuencia GTO para esta acción
        frequency = self.calculate_gto_frequency(game_state, decision)
        
        # 3. Calcular explotabilidad
        exploitability = self.calculate_exploitability(game_state, decision)
        
        # 4. Puntos de indiferencia
        indifference_points = self.find_indifference_points(game_state, decision)
        
        # 5. Ventaja de rango
        range_advantage = self.range_analyzer.calculate_range_advantage(game_state)
        
        return GTOAnalysis(
            ev=ev,
            frequency=frequency,
            exploitability=exploitability,
            indifference_points=indifference_points,
            range_advantage=range_advantage
        )
    
    def calculate_gto_frequency(self, game_state: Dict, decision: Dict) -> float:
        """Calcular frecuencia GTO para esta acción"""
        
        # Basado en soluciones GTO simplificadas
        action = decision.get('action', '').upper()
        street = game_state.get('street', '').lower()
        position = game_state.get('position', '').upper()
        
        # Frecuencias GTO aproximadas por situación
        gto_frequencies = {
            'preflop': {
                'UTG': {'RAISE': 0.15, 'CALL': 0.03, 'FOLD': 0.82},
                'MP': {'RAISE': 0.18, 'CALL': 0.05, 'FOLD': 0.77},
                'CO': {'RAISE': 0.25, 'CALL': 0.08, 'FOLD': 0.67},
                'BTN': {'RAISE': 0.40, 'CALL': 0.12, 'FOLD': 0.48},
                'SB': {'RAISE': 0.35, 'CALL': 0.25, 'FOLD': 0.40},
                'BB': {'RAISE': 0.10, 'CALL': 0.40, 'FOLD': 0.50}
            },
            'flop': {
                'IP': {'BET': 0.70, 'CHECK': 0.30},
                'OOP': {'BET': 0.40, 'CHECK': 0.60}
            },
            'turn': {
                'IP': {'BET': 0.50, 'CHECK': 0.50},
                'OOP': {'BET': 0.30, 'CHECK': 0.70}
            },
            'river': {
                'IP': {'BET': 0.40, 'CHECK': 0.60},
                'OOP': {'BET': 0.25, 'CHECK': 0.75}
            }
        }
        
        # Determinar clave
        if street == 'preflop':
            key = position
        else:
            # Determinar si está in position (IP) o out of position (OOP)
            # Simplificación: BTN/CO = IP, SB/BB = OOP
            if position in ['BTN', 'CO']:
                pos_key = 'IP'
            else:
                pos_key = 'OOP'
            
            if street in gto_frequencies:
                frequencies = gto_frequencies[street].get(pos_key, {})
                return frequencies.get(action, 0.0)
        
        return 0.0
    
    def calculate_exploitability(self, game_state: Dict, decision: Dict) -> float:
        """Calcular cuán explotable es la decisión"""
        
        # Factores que aumentan explotabilidad:
        # 1. Acciones demasiado predecibles
        # 2. Tamaños de apuesta fijos
        # 3. Rangos desbalanceados
        # 4. Frecuencias extremas
        
        exploitability_score = 0.0
        
        action = decision.get('action', '').upper()
        
        # Check 1: ¿Es siempre la misma acción en esta situación?
        # (Esto requeriría historial, por ahora simplificamos)
        
        # Check 2: ¿Tamaño de apuesta fijo o variable?
        if 'size' in decision:
            size_str = decision['size']
            # En sistema real, verificaríamos variabilidad histórica
        
        # Check 3: ¿Balance de rangos?
        # (Análisis complejo, simplificado)
        
        return min(1.0, max(0.0, exploitability_score))
    
    def find_indifference_points(self, game_state: Dict, decision: Dict) -> List[float]:
        """Encontrar puntos de indiferencia para la decisión"""
        
        # Puntos donde EV de diferentes acciones es igual
        # Simplificado para implementación básica
        
        indifference_points = []
        
        # Ejemplo: Para call vs fold, el punto de indiferencia es cuando
        # pot_odds = equity_required
        
        pot_size = game_state.get('pot_size', 0)
        bet_to_call = game_state.get('bet_to_call', 0)
        
        if bet_to_call > 0 and pot_size > 0:
            pot_odds = bet_to_call / (pot_size + bet_to_call)
            indifference_points.append(pot_odds)
        
        return indifference_points
    
    def load_gto_baselines(self) -> Dict:
        """Cargar líneas base GTO para comparación"""
        
        return {
            'preflop_rfi': {  # Raise First In frequencies
                'UTG': 0.152, 'MP': 0.184, 'CO': 0.254, 'BTN': 0.402, 'SB': 0.352
            },
            '3bet_frequencies': {
                'vs_UTG': 0.048, 'vs_MP': 0.055, 'vs_CO': 0.075, 'vs_BTN': 0.098, 'vs_SB': 0.112
            },
            'cbet_frequencies': {
                'flop_ip': 0.68, 'flop_oop': 0.42,
                'turn_ip': 0.51, 'turn_oop': 0.31,
                'river_ip': 0.42, 'river_oop': 0.26
            },
            'defense_frequencies': {
                'bb_vs_utg': 0.38, 'bb_vs_btn': 0.52,
                'sb_vs_btn': 0.42, 'bb_vs_sb': 0.45
            }
        }

class EVCalculator:
    """Calculadora de valor esperado (EV)"""
    
    def estimate_ev(self, game_state: Dict, decision: Dict) -> float:
        """Estimar EV de una decisión"""
        
        action = decision.get('action', '').upper()
        street = game_state.get('street', '').lower()
        
        # EV base por acción (simplificado)
        ev_base = {
            'FOLD': 0.0,
            'CHECK': 0.1,  # Pequeño EV por ver siguiente carta gratis
            'CALL': 0.2,   # EV positivo si hay buenas odds
            'BET': 0.3,    # EV por fold equity y value
            'RAISE': 0.4,  # Más EV que bet por mayor fold equity
            'ALL-IN': 0.5  # Máximo EV pero también máximo riesgo
        }.get(action, 0.0)
        
        # Ajustar por situación
        adjustments = self.calculate_ev_adjustments(game_state, decision)
        
        return max(-1.0, min(1.0, ev_base + adjustments))
    
    def calculate_ev_adjustments(self, game_state: Dict, decision: Dict) -> float:
        """Calcular ajustes al EV basado en situación"""
        
        adjustments = 0.0
        
        # 1. Ajuste por posición
        position = game_state.get('position', '').upper()
        position_adj = {
            'BTN': 0.15, 'CO': 0.10, 'MP': 0.0, 'UTG': -0.05, 'SB': -0.10, 'BB': -0.05
        }.get(position, 0.0)
        
        adjustments += position_adj
        
        # 2. Ajuste por stack size
        stack_bb = game_state.get('stack_bb', 100)
        if stack_bb < 20:
            adjustments += 0.1  # Más agresivo con stack corto
        elif stack_bb > 100:
            adjustments -= 0.05  # Más conservador con stack profundo
        
        # 3. Ajuste por número de jugadores
        players = game_state.get('active_players', 6)
        if players <= 3:
            adjustments += 0.1  # Más agresivo en mesas cortas
        elif players >= 9:
            adjustments -= 0.05  # Más conservador en mesas llenas
        
        return adjustments

class RangeAnalyzer:
    """Analizador de rangos y ventajas de rango"""
    
    def calculate_range_advantage(self, game_state: Dict) -> float:
        """Calcular ventaja de rango"""
        
        # Ventaja de rango basada en posición y situación
        position = game_state.get('position', '').upper()
        street = game_state.get('street', '').lower()
        
        # Ventaja base por posición
        position_advantage = {
            'BTN': 0.3, 'CO': 0.2, 'MP': 0.1, 'UTG': 0.05, 'SB': -0.1, 'BB': -0.15
        }.get(position, 0.0)
        
        # Ajustar por calle
        if street == 'preflop':
            street_multiplier = 1.0
        elif street == 'flop':
            street_multiplier = 0.8
        elif street == 'turn':
            street_multiplier = 0.6
        else:  # river
            street_multiplier = 0.4
        
        return position_advantage * street_multiplier
    
    def analyze_range_balance(self, game_state: Dict, decision: Dict) -> Dict:
        """Analizar balance del rango"""
        
        return {
            'value_hands': 0.3,  # % de manos de value en el rango
            'bluffs': 0.2,       # % de bluffs en el rango
            'balance_ratio': 0.67,  # Ratio value:bluff (ideal: 2:1 = 0.67)
            'polarization': 0.5,    # Grado de polarización del rango
            'nuts_advantage': 0.1   # Ventaja en manos nuts
        }