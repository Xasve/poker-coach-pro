"""
Archivo: game_state.py
Ruta: src/core/game_state.py
Clase para manejar el estado del juego y validaciones
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum

class Street(Enum):
    """Calles del poker"""
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"

class Position(Enum):
    """Posiciones en la mesa"""
    UTG = "UTG"
    MP = "MP"
    CO = "CO"
    BTN = "BTN"
    SB = "SB"
    BB = "BB"

class GameState:
    """Clase para manejar el estado completo del juego"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.reset_state()
        
        # Historial de manos
        self.hand_history = []
        self.current_hand = {}
        
        # Estadísticas
        self.session_stats = {
            'hands_played': 0,
            'vpip': 0,
            'pfr': 0,
            'aggression_factor': 0,
            'winnings': 0.0,
            'session_start': datetime.now()
        }
    
    def reset_state(self):
        """Resetear estado para nueva mano"""
        self.hero_cards = []
        self.board_cards = []
        self.pot_size = 0.0
        self.bet_to_call = 0.0
        self.hero_stack = 100.0
        self.opponent_stacks = {}
        self.street = Street.PREFLOP
        self.position = Position.BTN
        self.action_to_us = False
        self.buttons_visible = []
        self.table_size = 6
        self.hand_id = None
        self.timestamp = datetime.now()
        
        # Información de la mesa
        self.table_id = ""
        self.stakes = "NL10"
        self.game_type = "cash"
        self.players = []
        
        # Acciones previas
        self.action_history = []
    
    def update_from_adapter(self, adapter_data: Dict):
        """Actualizar estado desde datos del adaptador"""
        
        # Validar datos básicos
        if not adapter_data or 'platform' not in adapter_data:
            return False
        
        # Actualizar campos
        self.hero_cards = adapter_data.get('hero_cards', [])
        self.board_cards = adapter_data.get('board_cards', [])
        self.pot_size = float(adapter_data.get('pot_size', 0))
        self.bet_to_call = float(adapter_data.get('bet_to_call', 0))
        self.hero_stack = float(adapter_data.get('hero_stack', 100))
        
        # Determinar street
        street_str = adapter_data.get('street', 'preflop')
        self.street = Street(street_str.lower())
        
        # Determinar posición
        position_str = adapter_data.get('position', 'BTN')
        try:
            self.position = Position(position_str.upper())
        except:
            self.position = Position.BTN
        
        self.action_to_us = bool(adapter_data.get('action_to_us', False))
        self.buttons_visible = adapter_data.get('buttons_visible', [])
        
        # Calcular información derivada
        self.calculate_derived_info()
        
        # Registrar en historial
        self.record_action("state_update", adapter_data)
        
        return True
    
    def calculate_derived_info(self):
        """Calcular información derivada del estado"""
        
        # Stack en BBs
        if self.bet_to_call > 0:
            self.stack_bb = self.hero_stack / self.bet_to_call
        else:
            self.stack_bb = self.hero_stack / 1.0  # Asumiendo BB = 1
        
        # Pot odds
        if self.bet_to_call > 0 and self.pot_size > 0:
            self.pot_odds = self.bet_to_call / (self.pot_size + self.bet_to_call)
        else:
            self.pot_odds = 0.0
        
        # Número de jugadores
        self.active_players = self.table_size  # Simplificado
        
        # Manos por hora estimadas
        self.hands_per_hour = self.estimate_hands_per_hour()
    
    def estimate_hands_per_hour(self) -> float:
        """Estimar manos por hora basado en plataforma y tipo"""
        base_rates = {
            'ggpoker': {'cash': 85, 'tournament': 45},
            'pokerstars': {'cash': 80, 'tournament': 40}
        }
        
        platform_rates = base_rates.get(self.platform, base_rates['ggpoker'])
        return platform_rates.get(self.game_type, 70)
    
    def record_action(self, action_type: str, data: Dict):
        """Registrar acción en el historial"""
        action_record = {
            'timestamp': datetime.now(),
            'type': action_type,
            'data': data,
            'street': self.street.value,
            'pot': self.pot_size,
            'bet_to_call': self.bet_to_call
        }
        
        self.action_history.append(action_record)
        
        # Mantener historial limitado
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-100:]
    
    def get_hand_strength(self) -> float:
        """Obtener fuerza de mano actual (0-1)"""
        
        if not self.hero_cards or len(self.hero_cards) < 2:
            return 0.0
        
        # Evaluación simplificada
        # En implementación real usaríamos librería de evaluación de manos
        
        card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            card_values[str(i)] = i
        
        # Evaluar hole cards
        hole_score = 0
        cards = self.hero_cards[:2]  # Tomar solo las dos hole cards
        
        for card in cards:
            if len(card) > 0:
                value = card[0].upper()
                hole_score += card_values.get(value, 0) / 14
        
        hole_score = hole_score / 2  # Promedio de dos cartas
        
        # Bonus por suited
        if len(cards) >= 2:
            if len(cards[0]) > 1 and len(cards[1]) > 1:
                if cards[0][-1] == cards[1][-1]:
                    hole_score += 0.1
        
        # Bonus por pareja
        if len(cards) >= 2:
            if cards[0][0].upper() == cards[1][0].upper():
                hole_score += 0.2
        
        return min(1.0, max(0.0, hole_score))
    
    def get_equity_estimate(self) -> float:
        """Obtener estimación de equity"""
        
        if self.street == Street.PREFLOP:
            # Equity preflop basada en fuerza de mano
            hand_strength = self.get_hand_strength()
            
            # Mapear a equity aproximada contra rango aleatorio
            if hand_strength > 0.8:
                return 0.65  # Manos premium
            elif hand_strength > 0.6:
                return 0.55  # Manos fuertes
            elif hand_strength > 0.4:
                return 0.45  # Manos decentes
            else:
                return 0.35  # Manos débiles
        
        else:
            # Para postflop, estimación más compleja
            # Por ahora devolver valor basado en fuerza de mano
            hand_strength = self.get_hand_strength()
            
            # Ajustar por street
            street_multiplier = {
                Street.FLOP: 1.0,
                Street.TURN: 1.1,
                Street.RIVER: 1.2
            }
            
            base_equity = hand_strength * 0.7
            multiplier = street_multiplier.get(self.street, 1.0)
            
            return min(0.95, base_equity * multiplier)
    
    def get_decision_context(self) -> Dict:
        """Obtener contexto para toma de decisión"""
        
        return {
            'platform': self.platform,
            'street': self.street.value,
            'position': self.position.value,
            'hero_cards': self.hero_cards,
            'board_cards': self.board_cards,
            'pot_size': self.pot_size,
            'bet_to_call': self.bet_to_call,
            'stack_bb': self.stack_bb,
            'pot_odds': self.pot_odds,
            'hand_strength': self.get_hand_strength(),
            'equity_estimate': self.get_equity_estimate(),
            'action_to_us': self.action_to_us,
            'buttons_visible': self.buttons_visible,
            'game_type': self.game_type,
            'stakes': self.stakes,
            'active_players': self.active_players
        }
    
    def validate_state(self) -> Tuple[bool, List[str]]:
        """Validar estado actual del juego"""
        
        warnings = []
        
        # Validar cartas
        if len(self.hero_cards) > 0:
            for card in self.hero_cards:
                if not self.is_valid_card(card):
                    warnings.append(f"Carta inválida: {card}")
        
        # Validar montos
        if self.pot_size < 0:
            warnings.append(f"Pot negativo: {self.pot_size}")
            self.pot_size = 0
        
        if self.bet_to_call < 0:
            warnings.append(f"Bet to call negativo: {self.bet_to_call}")
            self.bet_to_call = 0
        
        if self.hero_stack < 0:
            warnings.append(f"Stack negativo: {self.hero_stack}")
            self.hero_stack = 0
        
        # Validar consistencia
        if self.street != Street.PREFLOP and len(self.board_cards) == 0:
            warnings.append(f"Street {self.street.value} sin cartas comunitarias")
        
        return len(warnings) == 0, warnings
    
    def is_valid_card(self, card: str) -> bool:
        """Validar formato de carta"""
        if not card or len(card) < 2:
            return False
        
        # Valor
        value = card[0].upper()
        valid_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        
        if value not in valid_values:
            return False
        
        # Palo
        suit = card[-1].lower()
        valid_suits = ['h', 'd', 'c', 's']  # corazones, diamantes, tréboles, picas
        
        return suit in valid_suits
    
    def save_hand_history(self, decision: Dict):
        """Guardar historial de mano completa"""
        
        hand_record = {
            'hand_id': self.hand_id or f"hand_{int(time.time())}",
            'timestamp': self.timestamp,
            'platform': self.platform,
            'game_type': self.game_type,
            'stakes': self.stakes,
            'final_state': self.get_decision_context(),
            'action_history': self.action_history.copy(),
            'decision_made': decision,
            'session_stats': self.session_stats.copy()
        }
        
        self.hand_history.append(hand_record)
        
        # Actualizar estadísticas
        self.update_session_stats(decision)
        
        # Limitar tamaño del historial
        if len(self.hand_history) > 1000:
            self.hand_history = self.hand_history[-1000:]
        
        # Guardar en archivo periódicamente
        if len(self.hand_history) % 10 == 0:
            self.save_to_file()
    
    def update_session_stats(self, decision: Dict):
        """Actualizar estadísticas de sesión"""
        self.session_stats['hands_played'] += 1
        
        # VPIP (Voluntarily Put $ In Pot)
        action = decision.get('action', '').upper()
        if action in ['CALL', 'RAISE', 'BET']:
            self.session_stats['vpip'] += 1
        
        # PFR (Preflop Raise)
        if self.street == Street.PREFLOP and action == 'RAISE':
            self.session_stats['pfr'] += 1
        
        # Recalcular porcentajes
        if self.session_stats['hands_played'] > 0:
            vpip_pct = self.session_stats['vpip'] / self.session_stats['hands_played']
            pfr_pct = self.session_stats['pfr'] / self.session_stats['hands_played']
            
            self.session_stats['vpip_percentage'] = vpip_pct
            self.session_stats['pfr_percentage'] = pfr_pct
    
    def save_to_file(self):
        """Guardar historial en archivo"""
        try:
            import os
            import json
            from datetime import datetime
            
            # Crear directorio si no existe
            os.makedirs('data/hand_history', exist_ok=True)
            
            # Nombre de archivo con fecha
            date_str = datetime.now().strftime('%Y%m%d')
            filename = f"data/hand_history/{self.platform}_{date_str}.json"
            
            # Guardar
            with open(filename, 'w') as f:
                json.dump(self.hand_history, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Error guardando historial: {e}")
    
    def get_session_summary(self) -> Dict:
        """Obtener resumen de sesión"""
        
        duration = datetime.now() - self.session_stats['session_start']
        
        return {
            'platform': self.platform,
            'game_type': self.game_type,
            'stakes': self.stakes,
            'session_duration': str(duration),
            'hands_played': self.session_stats['hands_played'],
            'vpip': f"{self.session_stats.get('vpip_percentage', 0):.1%}",
            'pfr': f"{self.session_stats.get('pfr_percentage', 0):.1%}",
            'winnings': f"${self.session_stats.get('winnings', 0):.2f}",
            'hands_per_hour': int(self.hand_history[-1] if self.hand_history else 0),
            'start_time': self.session_stats['session_start'].strftime('%H:%M'),
            'current_time': datetime.now().strftime('%H:%M')
        }
    
    def __str__(self) -> str:
        """Representación en string del estado"""
        
        context = self.get_decision_context()
        
        return f"""
        ┌─ ESTADO DEL JUEGO ──────────────────────────
        │ Plataforma: {self.platform:>10}
        │ Tipo: {self.game_type:>13}
        │ Stakes: {self.stakes:>12}
        │ 
        │ Calle: {self.street.value:>12}
        │ Posición: {self.position.value:>10}
        │ 
        │ Cartas Hero: {', '.join(self.hero_cards):>8}
        │ Cartas Mesa: {', '.join(self.board_cards):>8}
        │ 
        │ Pot: ${self.pot_size:>10.2f}
        │ Stack: ${self.hero_stack:>9.2f} ({self.stack_bb:.1f} BB)
        │ Bet to Call: ${self.bet_to_call:>6.2f}
        │ Pot Odds: {self.pot_odds:>11.1%}
        │ 
        │ Fuerza Mano: {self.get_hand_strength():>9.1%}
        │ Equity Est.: {self.get_equity_estimate():>9.1%}
        │ 
        │ Acción a Nosotros: {'SÍ' if self.action_to_us else 'NO':>8}
        │ Botones: {', '.join(self.buttons_visible):>8}
        └─────────────────────────────────────────────
        """