"""
Archivo: decision_validator_fixed.py
Ruta: src/quality/decision_validator_fixed.py
Sistema de validación CORREGIDO y simplificado
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum

class DecisionQuality(Enum):
    """Niveles de calidad de decisión"""
    EXCELLENT = "EXCELENTE"
    GOOD = "BUENA"
    ACCEPTABLE = "ACEPTABLE"
    QUESTIONABLE = "CUESTIONABLE"
    BAD = "MALA"

class SimpleDecisionValidator:
    """
    Validador SIMPLIFICADO de decisiones de poker
    Versión corregida y funcional
    """
    
    def __init__(self, platform="ggpoker"):
        self.platform = platform
        
        # Cargar reglas básicas
        self.validation_rules = self.load_simple_rules()
        
        # Historial
        self.validation_history = []
        self.stats = {
            'total_validations': 0,
            'excellent': 0, 'good': 0, 'acceptable': 0,
            'questionable': 0, 'bad': 0
        }
    
    def load_simple_rules(self) -> Dict:
        """Cargar reglas simples de validación"""
        return {
            'preflop_ranges': self.get_preflop_ranges(),
            'standard_sizings': self.get_standard_sizings(),
            'equity_requirements': self.get_equity_requirements(),
            'common_mistakes': self.get_common_mistakes()
        }
    
    def get_preflop_ranges(self) -> Dict:
        """Obtener rangos preflop básicos"""
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
            },
            'SB': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AQs', 'AJs'],
                'strong': ['77', '66', '55', 'ATs', 'A9s', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs'],
                'marginal': ['44', '33', '22', 'AJo', 'KQo', 'QJo', 'JTo'],
                'weak': ['A8s-A2s', 'K9s-K2s', 'Q9s', 'J9s', 'T9s', '98s', '87s']
            },
            'BB': {
                'premium': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AKs', 'AQs', 'AJs', 'ATs'],
                'strong': ['66', '55', '44', '33', '22', 'A9s-A2s', 'KQs', 'KJs', 'KTs', 'K9s', 'QJs', 'QTs', 'Q9s', 'JTs', 'J9s', 'T9s', '98s'],
                'marginal': ['AJo-A2o', 'KQo-K9o', 'QJo-Q9o', 'JTo-J9o', 'T9o-T8o', '98o-97o'],
                'weak': ['K8o-K2o', 'Q8o-Q2o', 'J8o-J2o', 'T7o-T2o', '96o-92o', '87o-82o', '76o-72o', '65o-62o', '54o-52o', '43o-42o', '32o']
            }
        }
    
    def get_standard_sizings(self) -> Dict:
        """Obtener tamaños estándar de apuestas"""
        return {
            'preflop': {
                'open': {
                    'UTG': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'MP': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'CO': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'BTN': {'min': 2.0, 'max': 2.5, 'optimal': 2.2},
                    'SB': {'min': 2.5, 'max': 4.0, 'optimal': 3.0}
                },
                '3bet_ip': {'min': 2.8, 'max': 3.5, 'optimal': 3.0},
                '3bet_oop': {'min': 3.5, 'max': 4.5, 'optimal': 3.8}
            },
            'postflop': {
                'cbet_flop': {'min': 0.25, 'max': 0.75, 'optimal': 0.33},
                'turn_barrel': {'min': 0.50, 'max': 0.90, 'optimal': 0.65},
                'river_value': {'min': 0.50, 'max': 1.20, 'optimal': 0.70}
            }
        }
    
    def get_equity_requirements(self) -> Dict:
        """Obtener requerimientos de equity"""
        return {
            'call_preflop': 0.40,
            'call_flop': 0.35,
            'call_turn': 0.30,
            'call_river': 0.25,
            'semi_bluff': 0.25,
            'value_bet': 0.55
        }
    
    def get_common_mistakes(self) -> List[str]:
        """Obtener errores comunes"""
        return [
            "Fold con mano premium",
            "Call con malas pot odds",
            "Raise demasiado pequeño",
            "Raise demasiado grande",
            "No defender BB suficiente",
            "Jugar demasiado loose desde EP",
            "C-bet en flops peligrosos",
            "No considerar posición"
        ]
    
    def validate_decision(self, game_state: Dict, decision: Dict) -> Dict:
        """
        Validar una decisión (versión simplificada)
        """
        validation = {
            'quality': DecisionQuality.ACCEPTABLE.value,
            'score': 70,
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'analysis': {}
        }
        
        # Validación básica
        self.validate_basics(game_state, decision, validation)
        
        # Validación específica por calle
        street = game_state.get('street', 'preflop').lower()
        
        if street == 'preflop':
            self.validate_preflop(game_state, decision, validation)
        else:
            self.validate_postflop(game_state, decision, validation)
        
        # Validar tamaño
        self.validate_sizing(game_state, decision, validation)
        
        # Calcular puntuación final
        validation['score'] = self.calculate_score(validation)
        validation['quality'] = self.score_to_quality(validation['score']).value
        
        # Actualizar estadísticas
        self.update_stats(validation['quality'])
        
        # Guardar en historial
        self.save_to_history(game_state, decision, validation)
        
        return validation
    
    def validate_basics(self, game_state: Dict, decision: Dict, validation: Dict):
        """Validación básica"""
        action = decision.get('action', '').upper()
        
        # Verificar acción válida
        valid_actions = ['FOLD', 'CHECK', 'CALL', 'BET', 'RAISE', 'ALL-IN']
        if action not in valid_actions:
            validation['weaknesses'].append(f"Acción inválida: {action}")
        
        # Verificar consistencia
        if action == 'FOLD' and game_state.get('bet_to_call', 0) == 0:
            validation['suggestions'].append("Considerar CHECK en lugar de FOLD")
        
        if action == 'CHECK' and game_state.get('bet_to_call', 0) > 0:
            validation['weaknesses'].append("No se puede check con apuesta pendiente")
    
    def validate_preflop(self, game_state: Dict, decision: Dict, validation: Dict):
        """Validación preflop"""
        position = game_state.get('position', '').upper()
        action = decision.get('action', '').upper()
        hand_cards = game_state.get('hero_cards', [])
        
        # Convertir mano a formato de rango
        hand_str = self.cards_to_range_format(hand_cards)
        
        # Obtener rango para posición
        ranges = self.validation_rules['preflop_ranges'].get(position, {})
        
        # Verificar si mano está en rango
        if hand_str:
            hand_category = None
            
            for category, hands in ranges.items():
                if hand_str in hands:
                    hand_category = category
                    break
            
            # Evaluar decisión basada en categoría
            if hand_category:
                if hand_category == 'premium':
                    if action not in ['RAISE', 'ALL-IN']:
                        validation['weaknesses'].append(
                            f"Mano premium {hand_str} pero acción: {action}"
                        )
                    else:
                        validation['strengths'].append(
                            f"Mano premium {hand_str}, acción correcta"
                        )
                
                elif hand_category == 'weak' and position in ['UTG', 'MP']:
                    if action != 'FOLD':
                        validation['weaknesses'].append(
                            f"Mano débil {hand_str} desde {position}, debería ser FOLD"
                        )
                
                elif hand_category == 'marginal':
                    validation['suggestions'].append(
                        f"Mano marginal {hand_str}, revisar si decisión es correcta"
                    )
    
    def validate_postflop(self, game_state: Dict, decision: Dict, validation: Dict):
        """Validación postflop simplificada"""
        street = game_state.get('street', '').lower()
        action = decision.get('action', '').upper()
        bet_to_call = game_state.get('bet_to_call', 0)
        pot_size = game_state.get('pot_size', 0)
        
        # Validar calls basados en pot odds
        if action == 'CALL' and bet_to_call > 0 and pot_size > 0:
            pot_odds = bet_to_call / (pot_size + bet_to_call)
            
            # Equity requerida para esta calle
            equity_key = f'call_{street}'
            required_equity = self.validation_rules['equity_requirements'].get(equity_key, 0.3)
            
            if pot_odds > required_equity + 0.1:
                validation['weaknesses'].append(
                    f"Call con malas pot odds: {pot_odds:.1%}"
                )
            elif pot_odds < required_equity - 0.05:
                validation['strengths'].append(
                    f"Call con buenas pot odds: {pot_odds:.1%}"
                )
    
    def validate_sizing(self, game_state: Dict, decision: Dict, validation: Dict):
        """Validar tamaño de apuesta"""
        action = decision.get('action', '').upper()
        size_str = decision.get('size', '')
        street = game_state.get('street', '').lower()
        
        if action in ['BET', 'RAISE'] and size_str:
            # Intentar extraer tamaño
            size_pct = self.extract_bet_size(size_str)
            
            if size_pct > 0:
                # Obtener rangos óptimos
                if street == 'preflop':
                    position = game_state.get('position', '').upper()
                    sizings = self.validation_rules['standard_sizings']['preflop']['open']
                    optimal_range = sizings.get(position, {'min': 2.0, 'max': 2.5, 'optimal': 2.2})
                    
                    if size_pct < optimal_range['min'] * 100:
                        validation['weaknesses'].append(
                            f"Raise muy pequeño: {size_pct:.0f}%"
                        )
                    elif size_pct > optimal_range['max'] * 100:
                        validation['weaknesses'].append(
                            f"Raise muy grande: {size_pct:.0f}%"
                        )
                    else:
                        validation['strengths'].append(
                            f"Tamaño adecuado: {size_pct:.0f}%"
                        )
                
                else:
                    # Postflop
                    if street == 'flop':
                        optimal = self.validation_rules['standard_sizings']['postflop']['cbet_flop']
                    elif street == 'turn':
                        optimal = self.validation_rules['standard_sizings']['postflop']['turn_barrel']
                    else:  # river
                        optimal = self.validation_rules['standard_sizings']['postflop']['river_value']
                    
                    min_pct = optimal['min'] * 100
                    max_pct = optimal['max'] * 100
                    optimal_pct = optimal['optimal'] * 100
                    
                    if size_pct < min_pct:
                        validation['weaknesses'].append(
                            f"Apuesta muy pequeña: {size_pct:.0f}%"
                        )
                    elif size_pct > max_pct:
                        validation['weaknesses'].append(
                            f"Apuesta muy grande: {size_pct:.0f}%"
                        )
                    elif abs(size_pct - optimal_pct) < 10:
                        validation['strengths'].append(
                            f"Tamaño óptimo: {size_pct:.0f}%"
                        )
                    else:
                        validation['suggestions'].append(
                            f"Tamaño {size_pct:.0f}% OK, óptimo: {optimal_pct:.0f}%"
                        )
    
    def extract_bet_size(self, size_str: str) -> float:
        """Extraer tamaño de apuesta como porcentaje"""
        
        # Formato: "33% pot", "0.5x pot", "2.2BB"
        
        if '%' in size_str:
            try:
                return float(size_str.split('%')[0].strip())
            except:
                pass
        elif 'pot' in size_str.lower():
            try:
                multiplier = float(size_str.split('x')[0].strip())
                return multiplier * 100
            except:
                pass
        elif 'BB' in size_str.upper():
            try:
                bbs = float(size_str.upper().replace('BB', '').strip())
                return bbs * 100  # Aproximación
            except:
                pass
        
        return 0.0
    
    def cards_to_range_format(self, cards: List[str]) -> str:
        """Convertir cartas a formato de rango"""
        if not cards or len(cards) < 2:
            return ""
        
        # Tomar primeras dos cartas
        card1 = cards[0] if len(cards) > 0 else ''
        card2 = cards[1] if len(cards) > 1 else ''
        
        if not card1 or not card2:
            return ""
        
        # Valores
        values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            values[str(i)] = i
        
        val1 = values.get(card1[0].upper(), 0)
        val2 = values.get(card2[0].upper(), 0)
        
        # Pareja
        if card1[0].upper() == card2[0].upper():
            return card1[0].upper() + card2[0].upper()
        
        # Determinar si es suited
        suited = len(card1) > 1 and len(card2) > 1 and card1[-1] == card2[-1]
        suffix = "s" if suited else "o"
        
        # Ordenar de mayor a menor
        if val1 > val2:
            return card1[0].upper() + card2[0].upper() + suffix
        else:
            return card2[0].upper() + card1[0].upper() + suffix
    
    def calculate_score(self, validation: Dict) -> int:
        """Calcular puntuación de 0-100"""
        base = 70
        
        # Ajustar por fortalezas y debilidades
        strengths = len(validation.get('strengths', []))
        weaknesses = len(validation.get('weaknesses', []))
        suggestions = len(validation.get('suggestions', []))
        
        base += strengths * 5
        base -= weaknesses * 10
        base -= suggestions * 3
        
        return max(0, min(100, base))
    
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
        """Actualizar estadísticas"""
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
        """Guardar en historial"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'game_state': game_state,
            'decision': decision,
            'validation': validation,
            'quality': validation['quality'],
            'score': validation['score']
        }
        
        self.validation_history.append(record)
        
        # Limitar tamaño
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
    
    def generate_quality_report(self) -> str:
        """Generar reporte de calidad"""
        total = self.stats['total_validations']
        
        if total == 0:
            return "No hay validaciones registradas"
        
        percentages = {
            'excellent': self.stats['excellent'] / total * 100,
            'good': self.stats['good'] / total * 100,
            'acceptable': self.stats['acceptable'] / total * 100,
            'questionable': self.stats['questionable'] / total * 100,
            'bad': self.stats['bad'] / total * 100
        }
        
        report = []
        report.append("=" * 60)
        report.append("📊 REPORTE DE CALIDAD - DECISIONES DE POKER")
        report.append("=" * 60)
        report.append(f"Total decisiones validadas: {total}")
        report.append("")
        report.append("📈 DISTRIBUCIÓN DE CALIDAD:")
        report.append(f"  Excelente:  {percentages['excellent']:5.1f}%")
        report.append(f"  Buena:      {percentages['good']:5.1f}%")
        report.append(f"  Aceptable:  {percentages['acceptable']:5.1f}%")
        report.append(f"  Cuestionable: {percentages['questionable']:5.1f}%")
        report.append(f"  Mala:       {percentages['bad']:5.1f}%")
        
        # Calcular puntuación promedio
        if self.validation_history:
            avg_score = sum(r['score'] for r in self.validation_history) / len(self.validation_history)
            report.append(f"\n🎯 Puntuación promedio: {avg_score:.1f}/100")
        
        # Errores comunes recientes
        recent_weaknesses = []
        for record in self.validation_history[-10:]:
            if 'weaknesses' in record['validation']:
                recent_weaknesses.extend(record['validation']['weaknesses'])
        
        if recent_weaknesses:
            from collections import Counter
            common = Counter(recent_weaknesses).most_common(3)
            
            report.append("\n⚠️  ERRORES COMUNES RECIENTES:")
            for error, count in common:
                report.append(f"  • {error} ({count} veces)")
        
        report.append("=" * 60)
        
        return "\n".join(report)