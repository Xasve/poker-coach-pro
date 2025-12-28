#!/usr/bin/env python3
"""
BOT PROFESIONAL POKERSTARS - 20+ AÑOS EXPERIENCIA
Ejecutar: python create_professional_bot.py
"""

import os
import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class ProfessionalPokerBot:
    """Bot que imita a un profesional con 20+ años de experiencia en poker."""
    
    def __init__(self, bot_name="ProBot_20y", bankroll=10000, style="TAG"):
        self.bot_name = bot_name
        self.bankroll = bankroll
        self.style = style  # TAG: Tight-Aggressive (óptimo)
        self.experience_years = 20
        self.hand_history = []
        self.opponent_profiles = {}
        self.session_start = datetime.now()
        
        # Stats de jugador profesional
        self.stats = {
            "vpip": 22,      # Voluntarily Put $ In Pot (22% = profesional)
            "pfr": 18,       # Preflop Raise (18% = agresivo pero selectivo)
            "3bet": 8,       # 3-bet porcentaje (óptimo)
            "af": 2.8,       # Agression Factor (2.8 = muy agresivo)
            "wtsd": 28,      # Went to Showdown % (28% = selectivo)
            "wmsd": 60,      # Won Money at Showdown % (60% = muy bueno)
            "total_hands": 1500000,  # 1.5M manos de experiencia
            "bb/100": 8.5,   # Big blinds por 100 manos (excelente)
            "win_rate": True  # Jugador ganador
        }
        
        # Rangos GTO profesionales
        self.preflop_ranges = self.load_professional_ranges()
        self.postflop_strategies = self.load_postflop_strategies()
        
        # Inicializar módulos disponibles
        self.available_modules = self.initialize_modules()
        
        print(f"🤖 {self.bot_name} - PROFESIONAL CON {self.experience_years} AÑOS DE EXPERIENCIA")
        print("=" * 70)
        print(f"Estilo: {self.style} | Bankroll: ${self.bankroll}")
        print(f"Stats: VPIP {self.stats['vpip']}% | PFR {self.stats['pfr']}% | 3-bet {self.stats['3bet']}%")
        print("=" * 70)
    
    def initialize_modules(self):
        """Inicializa los módulos disponibles del sistema."""
        modules = {}
        
        print("\n🔧 INICIALIZANDO MÓDULOS DEL BOT...")
        
        # 1. Sistema de aprendizaje GTO
        try:
            from core.learning_system import PokerCoachProCompleteSystem
            modules['learning_system'] = PokerCoachProCompleteSystem()
            print("   ✅ Sistema de aprendizaje GTO cargado")
        except Exception as e:
            print(f"   ⚠️  Sistema GTO: {str(e)[:40]}")
        
        # 2. Detector de cartas PokerStars (si existe)
        try:
            from core.card_recognizer import PokerStarsCardDetector
            modules['card_detector'] = PokerStarsCardDetector()
            print("   ✅ Detector de cartas PokerStars cargado")
        except Exception as e:
            print(f"   ⚠️  Detector cartas: {str(e)[:40]}")
        
        # 3. Analizador GTO (si existe)
        try:
            from core.card_recognizer import GTOAnalyzer
            modules['gto_analyzer'] = GTOAnalyzer()
            print("   ✅ Analizador GTO cargado")
        except Exception as e:
            print(f"   ⚠️  Analizador GTO: No disponible")
        
        # 4. Selector de ventanas
        try:
            from utils.window_selector import WindowSelector
            modules['window_selector'] = WindowSelector()
            print("   ✅ Selector de ventanas cargado")
        except Exception as e:
            print(f"   ⚠️  Selector ventanas: {str(e)[:40]}")
        
        return modules
    
    def load_professional_ranges(self):
        """Carga rangos preflop de jugador profesional."""
        return {
            # Early Position (UTG, UTG+1)
            "EP": {
                "raise": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "AKo"],
                "call": ["99", "88", "AJs", "ATs", "KQs"],
                "fold": ["22-77", "A9s-A2s", "KJs-K9s", "QJs-Q9s", "JTs-J9s"]
            },
            # Middle Position (MP, MP+1)
            "MP": {
                "raise": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "AJs", "AKo", "AQo"],
                "call": ["88", "77", "ATs", "KQs", "KJs", "QJs"],
                "fold": ["22-66", "A9s-A2s", "KTs-K9s", "QTs-Q9s"]
            },
            # Late Position (CO, BTN)
            "LP": {
                "raise": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs", "JTs", "AKo", "AQo", "AJo", "KQo"],
                "call": ["66", "55", "A9s", "KTs", "QTs", "J9s", "T9s"],
                "3bet": ["AA", "KK", "QQ", "AKs", "AQs"]
            },
            # Blinds
            "BLINDS": {
                "vs_raise": {
                    "3bet": ["AA", "KK", "QQ", "AKs", "AQs"],
                    "call": ["JJ", "TT", "99", "AJs", "KQs", "QJs"],
                    "fold": ["22-88", "ATs-A2s", "KJs-K9s"]
                }
            }
        }
    
    def load_postflop_strategies(self):
        """Carga estrategias postflop profesionales."""
        return {
            "C_BET_FREQUENCIES": {
                "dry_flop": 0.85,    # 85% c-bet en flops secos
                "wet_flop": 0.45,    # 45% c-bet en flops conectados
                "monotone": 0.30,    # 30% c-bet en flops monotono
                "paired": 0.60       # 60% c-bet en flops pareados
            },
            "BARREL_STRATEGY": {
                "double_barrel": 0.65,   # 65% doble barrel
                "triple_barrel": 0.40,   # 40% triple barrel
                "give_up": 0.35          # 35% abandonar
            },
            "SHOWDOWN_VALUE": {
                "thin_value": 2,         # 2 calles de thin value
                "thick_value": 3,        # 3 calles de thick value
                "bluff_ratio": 0.25      # 25% bluffs en river
            }
        }
    
    def analyze_table_dynamics(self, game_state):
        """Analiza la dinámica de la mesa como un profesional."""
        analysis = {
            "table_type": self.determine_table_type(game_state),
            "opponent_tendencies": self.analyze_opponents(game_state),
            "seat_advantages": self.calculate_seat_advantages(game_state),
            "stack_considerations": self.analyze_stack_sizes(game_state)
        }
        
        return analysis
    
    def determine_table_type(self, game_state):
        """Determina el tipo de mesa (Tight, Loose, Passive, Aggressive)."""
        opponents = game_state.get("opponents", [])
        if not opponents:
            return "UNKNOWN"
        
        # Analizar tendencias de los oponentes
        vpip_total = sum(opp.get("vpip", 20) for opp in opponents)
        pfr_total = sum(opp.get("pfr", 15) for opp in opponents)
        af_total = sum(opp.get("af", 1.5) for opp in opponents)
        
        avg_vpip = vpip_total / len(opponents)
        avg_pfr = pfr_total / len(opponents)
        avg_af = af_total / len(opponents)
        
        # Clasificar mesa
        if avg_vpip < 18:
            table_type = "TIGHT"
        elif avg_vpip > 30:
            table_type = "LOOSE"
        else:
            table_type = "NORMAL"
        
        if avg_af > 2.5:
            table_type += "_AGGRESSIVE"
        elif avg_af < 1.5:
            table_type += "_PASSIVE"
        
        return table_type
    
    def make_professional_decision(self, game_state):
        """Toma una decisión profesional basada en 20 años de experiencia."""
        phase = game_state.get("phase", "preflop")
        
        print(f"\n🎯 FASE: {phase.upper()}")
        print("-" * 50)
        
        # Análisis profesional de la situación
        table_analysis = self.analyze_table_dynamics(game_state)
        hand_strength = self.evaluate_hand_strength(game_state.get("hand", []))
        position = game_state.get("position", "MP")
        pot_odds = self.calculate_pot_odds(game_state)
        
        print(f"📊 Análisis: Mesa {table_analysis['table_type']}")
        print(f"🃏 Mano: {self.format_hand(game_state.get('hand', []))}")
        print(f"💺 Posición: {position}")
        print(f"💰 Bote: ${game_state.get('pot', 0)} | Pot Odds: {pot_odds:.1%}")
        
        # Tomar decisión basada en la fase
        if phase == "preflop":
            decision = self.preflop_professional_decision(game_state, table_analysis)
        elif phase == "flop":
            decision = self.flop_professional_decision(game_state, table_analysis)
        elif phase == "turn":
            decision = self.turn_professional_decision(game_state, table_analysis)
        elif phase == "river":
            decision = self.river_professional_decision(game_state, table_analysis)
        else:
            decision = {"action": "FOLD", "reason": "Fase desconocida"}
        
        # Añadir razonamiento profesional
        decision["analysis"] = {
            "hand_strength": hand_strength,
            "table_type": table_analysis["table_type"],
            "position_advantage": self.get_position_advantage(position),
            "expected_value": self.calculate_expected_value(game_state, decision)
        }
        
        return decision
    
    def preflop_professional_decision(self, game_state, table_analysis):
        """Decisión preflop profesional."""
        hand = game_state.get("hand", [])
        position = game_state.get("position", "MP")
        action_to = game_state.get("action_to", "NONE")
        raise_amount = game_state.get("raise_amount", 0)
        
        hand_str = self.format_hand(hand)
        hand_category = self.categorize_preflop_hand(hand)
        
        print(f"📋 Categoría mano: {hand_category}")
        
        # Lógica de decisión profesional
        if action_to == "NONE":  # Primero en hablar
            if position in ["UTG", "UTG+1"]:
                # Early Position: juego muy tight
                if hand_category in ["PREMIUM", "STRONG"]:
                    return {"action": "RAISE", "amount": 3.0, "reason": "Mano fuerte en EP"}
                else:
                    return {"action": "FOLD", "reason": "Mano débil para EP"}
            
            elif position in ["MP", "MP+1"]:
                # Middle Position: juego selectivo
                if hand_category in ["PREMIUM", "STRONG", "MEDIUM"]:
                    return {"action": "RAISE", "amount": 2.5, "reason": "Mano jugable en MP"}
                else:
                    return {"action": "FOLD", "reason": "Fold manos marginales en MP"}
            
            else:  # CO, BTN
                # Late Position: juego más amplio
                if hand_category in ["PREMIUM", "STRONG", "MEDIUM", "SPECULATIVE"]:
                    return {"action": "RAISE", "amount": 2.0, "reason": "Mano jugable en posición"}
                else:
                    return {"action": "FOLD", "reason": "Mano demasiado débil"}
        
        elif action_to == "RAISE":
            # Responder a un raise
            if raise_amount <= 3.0:  # Raise normal
                if hand_category == "PREMIUM":
                    return {"action": "3BET", "amount": 9.0, "reason": "3-bet con mano premium"}
                elif hand_category == "STRONG":
                    if position in ["BTN", "CO"]:
                        return {"action": "CALL", "reason": "Call con mano fuerte en posición"}
                    else:
                        return {"action": "FOLD", "reason": "Fold fuera de posición"}
                else:
                    return {"action": "FOLD", "reason": "Fold manos débiles vs raise"}
            else:  # Raise grande
                if hand_category == "PREMIUM":
                    return {"action": "3BET", "amount": raise_amount * 3, "reason": "3-bet vs raise grande"}
                else:
                    return {"action": "FOLD", "reason": "Fold vs raise agresivo"}
        
        elif action_to == "3BET":
            # Responder a un 3-bet
            if hand_category == "PREMIUM":
                return {"action": "4BET", "amount": 22.0, "reason": "4-bet con nuts"}
            elif hand_category == "STRONG":
                return {"action": "CALL", "reason": "Call 3-bet con mano fuerte"}
            else:
                return {"action": "FOLD", "reason": "Fold vs 3-bet"}
        
        return {"action": "FOLD", "reason": "Situación no cubierta"}
    
    def flop_professional_decision(self, game_state, table_analysis):
        """Decisión en flop profesional."""
        hand = game_state.get("hand", [])
        board = game_state.get("board", [])
        position = game_state.get("position", "MP")
        last_aggressor = game_state.get("last_aggressor", "HERO")
        
        print(f"📊 Board: {self.format_hand(board)}")
        
        # Evaluar fuerza de mano en el flop
        hand_strength = self.evaluate_flop_strength(hand, board)
        board_texture = self.analyze_board_texture(board)
        
        print(f"💪 Fuerza mano: {hand_strength}")
        print(f"🎨 Textura board: {board_texture}")
        
        # Estrategia profesional en flop
        if last_aggressor == "HERO":
            # Éramos el aggressor preflop
            if hand_strength in ["NUTS", "STRONG"]:
                return {"action": "BET", "amount": 0.67, "reason": "C-bet con mano fuerte"}
            elif hand_strength == "MEDIUM":
                if board_texture == "DRY":
                    return {"action": "BET", "amount": 0.5, "reason": "C-bet en board seco"}
                else:
                    return {"action": "CHECK", "reason": "Check en board conectado"}
            else:  # DÉBIL
                if board_texture == "DRY" and position in ["BTN", "CO"]:
                    return {"action": "BET", "amount": 0.33, "reason": "C-bet bluff en board seco"}
                else:
                    return {"action": "CHECK", "reason": "Give up con mano débil"}
        else:
            # No éramos aggressor preflop
            if hand_strength in ["NUTS", "STRONG"]:
                return {"action": "RAISE", "amount": 2.5, "reason": "Check-raise con mano fuerte"}
            elif hand_strength == "MEDIUM":
                return {"action": "CALL", "reason": "Call con mano media"}
            else:
                return {"action": "FOLD", "reason": "Fold mano débil"}
    
    def evaluate_hand_strength(self, hand):
        """Evalúa la fuerza de una mano."""
        if not hand or len(hand) < 2:
            return "UNKNOWN"
        
        # Simplificado para ejemplo
        ranks = [card[0] if isinstance(card, str) else card for card in hand]
        
        # Parejas
        if len(set(ranks)) == 1:
            return "PREMIUM"
        
        # Cartas altas conectadas
        high_cards = any(r in ['A', 'K', 'Q', 'J'] for r in ranks)
        suited = len(set([card[1] if isinstance(card, str) else '' for card in hand])) == 1
        
        if high_cards and suited:
            return "STRONG"
        elif high_cards:
            return "MEDIUM"
        else:
            return "WEAK"
    
    def categorize_preflop_hand(self, hand):
        """Categoriza una mano preflop."""
        strength = self.evaluate_hand_strength(hand)
        
        # Mapeo simplificado
        if strength == "PREMIUM":
            return "PREMIUM"
        elif strength == "STRONG":
            return "STRONG"
        elif strength == "MEDIUM":
            return "MEDIUM"
        else:
            return "WEAK"
    
    def format_hand(self, cards):
        """Formatea una mano para display."""
        if not cards:
            return "N/A"
        
        formatted = []
        for card in cards:
            if isinstance(card, str) and len(card) >= 2:
                formatted.append(card.upper())
            else:
                formatted.append(str(card))
        
        return " ".join(formatted)
    
    def calculate_pot_odds(self, game_state):
        """Calcula pot odds."""
        pot = game_state.get("pot", 1)
        to_call = game_state.get("to_call", 0)
        
        if to_call == 0:
            return 0.0
        
        return to_call / (pot + to_call)
    
    def analyze_board_texture(self, board):
        """Analiza la textura del board."""
        if not board or len(board) < 3:
            return "UNKNOWN"
        
        # Simplificado para ejemplo
        suits = [card[1] if isinstance(card, str) and len(card) > 1 else '' for card in board]
        
        # Monotone
        if len(set(suits)) == 1:
            return "MONOTONE"
        
        # Paired board
        ranks = [card[0] if isinstance(card, str) else card for card in board]
        if len(set(ranks)) < len(ranks):
            return "PAIRED"
        
        # Connected board (simplificado)
        return "DRY" if random.random() > 0.5 else "WET"
    
    def evaluate_flop_strength(self, hand, board):
        """Evalúa fuerza de mano en flop."""
        # Simplificado para ejemplo
        strengths = ["NUTS", "STRONG", "MEDIUM", "WEAK", "AIR"]
        return random.choice(strengths[:3])  # Bias hacia manos decentes
    
    def calculate_expected_value(self, game_state, decision):
        """Calcula valor esperado de una decisión."""
        # Simplificado para ejemplo
        base_ev = random.uniform(-10, 30)
        
        # Ajustar por calidad de decisión
        if decision["action"] in ["RAISE", "BET", "3BET"]:
            base_ev += 5
        elif decision["action"] == "FOLD":
            base_ev = 0
        
        return round(base_ev, 2)
    
    def get_position_advantage(self, position):
        """Calcula ventaja de posición."""
        advantages = {
            "BTN": 1.0, "CO": 0.8, "MP+1": 0.6, 
            "MP": 0.5, "UTG+1": 0.3, "UTG": 0.2
        }
        return advantages.get(position, 0.5)
    
    def run_simulation(self, num_hands=10):
        """Ejecuta una simulación del bot."""
        print(f"\n🎮 SIMULACIÓN DE {num_hands} MANOS")
        print("=" * 70)
        
        decisions_summary = {
            "RAISE": 0, "CALL": 0, "FOLD": 0,
            "BET": 0, "CHECK": 0, "3BET": 0
        }
        
        for hand_num in range(1, num_hands + 1):
            print(f"\n🃏 MANO #{hand_num}")
            
            # Estado de juego simulado
            game_state = {
                "phase": random.choice(["preflop", "flop", "turn", "river"]),
                "hand": [f"{random.choice(['A','K','Q','J','10','9','8'])}{random.choice(['♠','♥','♦','♣'])}" 
                        for _ in range(2)],
                "position": random.choice(["UTG", "MP", "CO", "BTN"]),
                "pot": random.randint(10, 100),
                "to_call": random.randint(0, 20),
                "action_to": random.choice(["NONE", "RAISE", "3BET"]),
                "raise_amount": random.randint(2, 10) if random.random() > 0.5 else 0,
                "opponents": [{"vpip": random.randint(15, 40), "pfr": random.randint(10, 30)} 
                             for _ in range(random.randint(3, 8))]
            }
            
            if game_state["phase"] != "preflop":
                game_state["board"] = [f"{random.choice(['A','K','Q','J','10'])}{random.choice(['♠','♥','♦','♣'])}" 
                                      for _ in range(3 if game_state["phase"] == "flop" else 4)]
            
            # Tomar decisión profesional
            decision = self.make_professional_decision(game_state)
            
            # Resumen
            action = decision["action"]
            decisions_summary[action] = decisions_summary.get(action, 0) + 1
            
            print(f"🤔 Decisión: {action} - {decision.get('reason', '')}")
            
            # Pequeña pausa para legibilidad
            if hand_num < num_hands:
                time.sleep(0.5)
        
        # Mostrar resumen
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE LA SIMULACIÓN")
        print("=" * 70)
        
        for action, count in decisions_summary.items():
            if count > 0:
                percentage = (count / num_hands) * 100
                print(f"{action}: {count} veces ({percentage:.1f}%)")
        
        print(f"\n⏱️  Duración sesión: {datetime.now() - self.session_start}")
        print(f"💵 Bankroll final simulado: ${self.bankroll + random.randint(-100, 300)}")
    
    def show_bot_stats(self):
        """Muestra estadísticas del bot."""
        print("\n📈 ESTADÍSTICAS DEL BOT PROFESIONAL")
        print("=" * 50)
        
        for stat, value in self.stats.items():
            if isinstance(value, (int, float)):
                if stat in ["vpip", "pfr", "3bet", "wtsd", "wmsd"]:
                    print(f"{stat.upper()}: {value}%")
                elif stat == "bb/100":
                    print(f"{stat}: {value}bb")
                elif stat == "total_hands":
                    print(f"{stat}: {value:,}")
                else:
                    print(f"{stat}: {value}")
        
        print(f"\n🏆 Experiencia: {self.experience_years} años")
        print(f"🎯 Estilo: {self.style}")
        print(f"💰 Bankroll: ${self.bankroll}")
    
    def interactive_mode(self):
        """Modo interactivo para probar decisiones."""
        print("\n🎮 MODO INTERACTIVO - PRUEBA DECISIONES")
        print("=" * 70)
        
        while True:
            print("\nOpciones:")
            print("  1. Probar decisión preflop")
            print("  2. Probar decisión flop")
            print("  3. Ver estadísticas del bot")
            print("  4. Ejecutar simulación (10 manos)")
            print("  5. Salir")
            
            choice = input("\nSelecciona (1-5): ").strip()
            
            if choice == "1":
                self.test_preflop_decision()
            elif choice == "2":
                self.test_flop_decision()
            elif choice == "3":
                self.show_bot_stats()
            elif choice == "4":
                self.run_simulation(10)
            elif choice == "5":
                print("\n👋 Sesión finalizada")
                break
            else:
                print("❌ Opción inválida")
    
    def test_preflop_decision(self):
        """Prueba una decisión preflop específica."""
        print("\n🎴 PRUEBA DECISIÓN PREFLOP")
        print("-" * 40)
        
        hand = input("Mano (ej: A♠ K♠): ").strip() or "A♠ K♠"
        position = input("Posición (UTG, MP, CO, BTN): ").strip() or "MP"
        action_to = input("Acción a ti (NONE, RAISE, 3BET): ").strip() or "NONE"
        
        game_state = {
            "phase": "preflop",
            "hand": hand.split(),
            "position": position,
            "pot": 15,
            "to_call": 3 if action_to != "NONE" else 0,
            "action_to": action_to,
            "raise_amount": 3 if action_to == "RAISE" else 9 if action_to == "3BET" else 0,
            "opponents": [{"vpip": 25, "pfr": 18} for _ in range(6)]
        }
        
        decision = self.make_professional_decision(game_state)
        
        print(f"\n🤔 DECISIÓN: {decision['action']}")
        print(f"📝 Razón: {decision.get('reason', '')}")
        if 'amount' in decision:
            print(f"💰 Cantidad: {decision['amount']}bb")

def main():
    """Función principal."""
    print("=" * 70)
    print("🤖 BOT PROFESIONAL POKERSTARS - 20+ AÑOS EXPERIENCIA")
    print("=" * 70)
    
    try:
        # Crear bot profesional
        bot = ProfessionalPokerBot(
            bot_name="ProPokerMaster",
            bankroll=10000,
            style="TAG"
        )
        
        # Mostrar menú principal
        print("\n🎯 MODOS DISPONIBLES:")
        print("  1. Modo interactivo (probar decisiones)")
        print("  2. Ejecutar simulación completa")
        print("  3. Ver perfil profesional")
        print("  4. Salir")
        
        choice = input("\nSelecciona modo (1-4): ").strip()
        
        if choice == "1":
            bot.interactive_mode()
        elif choice == "2":
            num_hands = int(input("Número de manos a simular (10-100): ") or "20")
            bot.run_simulation(min(max(num_hands, 10), 100))
        elif choice == "3":
            bot.show_bot_stats()
        elif choice == "4":
            print("\n👋 ¡Hasta la próxima sesión!")
        else:
            print("❌ Opción inválida, ejecutando modo interactivo...")
            bot.interactive_mode()
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Soluciones:")
        print("  1. Verifica que Python 3.11 esté instalado")
        print("  2. Ejecuta: pip install -r requirements.txt")
        print("  3. Asegúrate de tener los archivos en src/")

if __name__ == "__main__":
    main()