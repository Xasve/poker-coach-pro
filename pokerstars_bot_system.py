#!/usr/bin/env python3
"""
POKERSTARS BOT SYSTEM - Sistema completo para PokerStars real
Conecta detección, análisis y decisiones profesionales.
"""

import os
import sys
import time
import json
import signal
import threading
from pathlib import Path
from datetime import datetime

# Configurar paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

class PokerStarsBotSystem:
    """Sistema completo de bot para PokerStars."""
    
    def __init__(self, mode="ASSIST"):
        """
        Modos disponibles:
        - ASSIST: Solo muestra decisiones (recomendado)
        - SEMI_AUTO: Sugiere y pregunta antes de actuar
        - AUTO: Ejecuta acciones automáticamente (avanzado)
        """
        self.mode = mode
        self.running = False
        self.session_start = datetime.now()
        self.hands_played = 0
        self.decisions_made = 0
        self.config = self.load_config()
        
        print("=" * 70)
        print("🤖 POKERSTARS BOT SYSTEM - PROFESIONAL 20+ AÑOS")
        print("=" * 70)
        print(f"Modo: {mode}")
        print(f"Inicio: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Inicializar componentes
        self.components = self.initialize_components()
        
        if not self.components:
            print("❌ No se pudieron inicializar componentes críticos")
            return
        
        print("\n✅ SISTEMA INICIALIZADO CORRECTAMENTE")
        print("   Componentes listos:", ", ".join(self.components.keys()))
    
    def load_config(self):
        """Carga configuración del sistema."""
        config_path = project_root / "config" / "bot_config.json"
        
        default_config = {
            "scan_interval": 1.0,  # Segundos entre escaneos
            "confidence_threshold": 0.7,
            "auto_bet_sizes": {
                "preflop_raise": 3.0,
                "cbet_flop": 0.67,
                "turn_bet": 0.75,
                "river_bet": 0.85
            },
            "table_settings": {
                "theme": "classic",
                "scan_region": None  # Se calibrará automáticamente
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                # Combinar con defaults
                default_config.update(user_config)
            except:
                pass
        
        # Guardar configuración
        config_path.parent.mkdir(exist_ok=True, parents=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def initialize_components(self):
        """Inicializa todos los componentes del sistema."""
        components = {}
        
        print("\n🔧 INICIALIZANDO COMPONENTES...")
        
        # 1. Sistema de aprendizaje GTO
        try:
            from core.learning_system import PokerCoachProCompleteSystem
            components['learning'] = PokerCoachProCompleteSystem()
            print("   ✅ Sistema de aprendizaje GTO")
        except Exception as e:
            print(f"   ❌ Sistema GTO: {str(e)[:40]}")
            return None
        
        # 2. Detector de cartas PokerStars
        try:
            from core.card_recognizer import PokerStarsCardDetector
            components['detector'] = PokerStarsCardDetector()
            print("   ✅ Detector de cartas PokerStars")
        except Exception as e:
            print(f"   ⚠️  Detector: {str(e)[:40]}")
            print("   ℹ️  Funcionará en modo simulación")
            components['detector'] = None
        
        # 3. Analizador GTO
        try:
            from core.card_recognizer import GTOAnalyzer
            components['analyzer'] = GTOAnalyzer()
            print("   ✅ Analizador GTO")
        except Exception as e:
            print(f"   ⚠️  Analizador: No disponible")
            components['analyzer'] = None
        
        # 4. Selector de ventanas (para calibración)
        try:
            from utils.window_selector import WindowSelector
            components['selector'] = WindowSelector()
            print("   ✅ Selector de ventanas")
        except Exception as e:
            print(f"   ⚠️  Selector: {str(e)[:40]}")
            components['selector'] = None
        
        # 5. Motor de decisiones profesional
        components['decision_engine'] = ProfessionalDecisionEngine()
        print("   ✅ Motor de decisiones profesional")
        
        return components
    
    def calibrate_table(self):
        """Calibra la posición de la mesa de PokerStars."""
        print("\n🎯 CALIBRACIÓN DE MESA")
        print("=" * 50)
        
        if 'selector' not in self.components or not self.components['selector']:
            print("❌ Selector no disponible para calibración")
            return False
        
        print("1. Abre PokerStars y coloca una mesa visible")
        print("2. Este proceso capturará las coordenadas de la mesa")
        print("3. Las coordenadas se guardarán para futuras sesiones")
        print()
        
        input("Presiona Enter cuando estés listo...")
        
        try:
            selector = self.components['selector']
            
            # Usar método disponible
            if hasattr(selector, 'capture_region_interactive'):
                region = selector.capture_region_interactive("pokerstars_table")
                if region:
                    self.config['table_settings']['scan_region'] = region
                    self.save_config()
                    print(f"✅ Mesa calibrada: {region}")
                    return True
            elif hasattr(selector, 'select_window_interactive'):
                window = selector.select_window_interactive("pokerstars_table")
                if window:
                    self.config['table_settings']['scan_region'] = window
                    self.save_config()
                    print(f"✅ Ventana calibrada: {window}")
                    return True
            
            print("⚠️  Métodos de calibración no disponibles")
            return False
            
        except Exception as e:
            print(f"❌ Error en calibración: {e}")
            return False
    
    def save_config(self):
        """Guarda la configuración actual."""
        config_path = project_root / "config" / "bot_config.json"
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def scan_table(self):
        """Escanea la mesa de PokerStars en busca de información."""
        print("\n🔍 ESCANEANDO MESA...")
        
        # Si no hay detector, usar simulación
        if not self.components.get('detector'):
            return self.simulate_table_scan()
        
        try:
            detector = self.components['detector']
            
            # Intentar detectar cartas
            if hasattr(detector, 'detect_hero_cards'):
                hero_cards = detector.detect_hero_cards()
                print(f"   🃏 Tus cartas: {hero_cards}")
            else:
                hero_cards = ["A♠", "K♠"]  # Simulación
                print(f"   🃏 Tus cartas (simulado): {hero_cards}")
            
            # Detectar board si está disponible
            board_cards = []
            if hasattr(detector, 'detect_board_cards'):
                board_cards = detector.detect_board_cards()
                if board_cards:
                    print(f"   📊 Board: {' '.join(board_cards)}")
            
            # Detectar acción
            action_info = self.detect_action()
            
            return {
                "hero_cards": hero_cards,
                "board_cards": board_cards,
                "phase": self.determine_phase(board_cards),
                "action_to": action_info.get("action", "NONE"),
                "pot_size": action_info.get("pot", 0),
                "to_call": action_info.get("to_call", 0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error en escaneo: {e}")
            return self.simulate_table_scan()
    
    def simulate_table_scan(self):
        """Simula un escaneo de mesa para desarrollo."""
        phases = ["preflop", "flop", "turn", "river"]
        current_phase = phases[self.hands_played % 4]
        
        # Cartas de ejemplo
        hero_cards = [
            ["A♠", "K♠"], ["Q♠", "Q♥"], ["J♣", "10♣"], 
            ["9♥", "9♦"], ["A♦", "K♦"], ["Q♥", "J♥"]
        ][self.hands_played % 6]
        
        # Board según fase
        board_map = {
            "preflop": [],
            "flop": ["Q♠", "10♠", "2♥"],
            "turn": ["Q♠", "10♠", "2♥", "K♦"],
            "river": ["Q♠", "10♠", "2♥", "K♦", "4♣"]
        }
        
        return {
            "hero_cards": hero_cards,
            "board_cards": board_map[current_phase],
            "phase": current_phase,
            "action_to": "RAISE" if self.hands_played % 3 == 0 else "NONE",
            "pot_size": 15 + (self.hands_played * 5),
            "to_call": 3 if self.hands_played % 2 == 0 else 0,
            "simulated": True
        }
    
    def detect_action(self):
        """Detecta la acción actual en la mesa."""
        # Esto se integraría con OCR real
        return {
            "action": "NONE",
            "pot": 15,
            "to_call": 0,
            "last_raiser": None
        }
    
    def determine_phase(self, board_cards):
        """Determina la fase del juego basado en el board."""
        if not board_cards:
            return "preflop"
        elif len(board_cards) == 3:
            return "flop"
        elif len(board_cards) == 4:
            return "turn"
        elif len(board_cards) == 5:
            return "river"
        return "unknown"
    
    def make_decision(self, table_state):
        """Toma una decisión profesional basada en el estado de la mesa."""
        engine = self.components['decision_engine']
        
        # Preparar estado del juego
        game_state = {
            "phase": table_state["phase"],
            "hand": table_state["hero_cards"],
            "board": table_state["board_cards"],
            "pot": table_state["pot_size"],
            "to_call": table_state["to_call"],
            "action_to": table_state["action_to"],
            "position": self.estimate_position(),
            "opponents": self.estimate_opponents()
        }
        
        # Tomar decisión
        decision = engine.make_professional_decision(game_state)
        
        # Registrar estadísticas
        self.decisions_made += 1
        if table_state.get("simulated"):
            self.hands_played += 1
        
        return decision
    
    def estimate_position(self):
        """Estima la posición actual (simplificado)."""
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        return positions[self.hands_played % 6]
    
    def estimate_opponents(self):
        """Estima información de oponentes (simplificado)."""
        return [
            {"vpip": 25, "pfr": 18, "stack": 100},
            {"vpip": 30, "pfr": 22, "stack": 85},
            {"vpip": 18, "pfr": 15, "stack": 120},
            {"vpip": 35, "pfr": 25, "stack": 75},
            {"vpip": 22, "pfr": 19, "stack": 95}
        ]
    
    def execute_decision(self, decision, table_state):
        """Ejecuta la decisión tomada según el modo."""
        action = decision["action"]
        reason = decision.get("reason", "")
        
        print(f"\n🤔 DECISIÓN: {action}")
        print(f"📝 Razón: {reason}")
        
        if self.mode == "ASSIST":
            # Solo muestra la decisión
            print("💡 Modo ASISTENTE: Tú ejecutas la acción manualmente")
            print(f"   Acción recomendada: {action}")
            if "amount" in decision:
                print(f"   Tamaño recomendado: {decision['amount']}bb")
        
        elif self.mode == "SEMI_AUTO":
            # Pregunta antes de ejecutar
            print(f"\n⚠️  Ejecutar acción '{action}'?")
            confirm = input("   (s/n): ").lower()
            
            if confirm in ['s', 'si', 'sí', 'y', 'yes']:
                print(f"   ✅ Ejecutando {action}...")
                # Aquí iría la ejecución real
            else:
                print("   ❌ Acción cancelada por el usuario")
        
        elif self.mode == "AUTO":
            # Ejecuta automáticamente (AVANZADO)
            print(f"⚡ Ejecutando {action} automáticamente...")
            # Código para ejecución real iría aquí
            # self.perform_action(action, decision.get("amount"))
        
        # Mostrar análisis detallado
        if "analysis" in decision:
            print("\n📊 ANÁLISIS DETALLADO:")
            for key, value in decision["analysis"].items():
                print(f"   • {key}: {value}")
    
    def run_continuous(self):
        """Ejecuta el sistema en modo continuo."""
        print("\n🚀 INICIANDO SISTEMA EN MODO CONTINUO")
        print("=" * 50)
        print("Presiona Ctrl+C para detener")
        print("-" * 50)
        
        self.running = True
        scan_count = 0
        
        try:
            while self.running:
                scan_count += 1
                print(f"\n📡 Escaneo #{scan_count}")
                print("-" * 30)
                
                # Escanear mesa
                table_state = self.scan_table()
                
                # Tomar decisión
                decision = self.make_decision(table_state)
                
                # Ejecutar decisión
                self.execute_decision(decision, table_state)
                
                # Esperar antes del siguiente escaneo
                print(f"\n⏱️  Esperando {self.config['scan_interval']}s...")
                time.sleep(self.config['scan_interval'])
                
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido por el usuario")
        finally:
            self.show_session_summary()
    
    def show_session_summary(self):
        """Muestra resumen de la sesión."""
        duration = datetime.now() - self.session_start
        
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE SESIÓN")
        print("=" * 70)
        print(f"⏱️  Duración: {duration}")
        print(f"🃏 Manos procesadas: {self.hands_played}")
        print(f"🤔 Decisiones tomadas: {self.decisions_made}")
        print(f"🎯 Modo: {self.mode}")
        print(f"💾 Configuración guardada en: config/bot_config.json")
        print("=" * 70)
    
    def interactive_menu(self):
        """Menú interactivo del sistema."""
        while True:
            print("\n" + "=" * 70)
            print("🎮 MENÚ PRINCIPAL - POKERSTARS BOT SYSTEM")
            print("=" * 70)
            print("1. 🔍 Escanear mesa actual (una vez)")
            print("2. 🚀 Ejecutar en modo continuo")
            print("3. 🎯 Calibrar mesa PokerStars")
            print("4. ⚙️  Configurar modo (Actual: " + self.mode + ")")
            print("5. 📊 Ver estadísticas de sesión")
            print("6. 💾 Guardar configuración")
            print("0. 🚪 Salir")
            print("=" * 70)
            
            try:
                choice = input("\nSelección: ").strip()
                
                if choice == "1":
                    self.single_scan_mode()
                elif choice == "2":
                    self.run_continuous()
                elif choice == "3":
                    self.calibrate_table()
                elif choice == "4":
                    self.configure_mode()
                elif choice == "5":
                    self.show_session_summary()
                elif choice == "6":
                    self.save_config()
                    print("✅ Configuración guardada")
                elif choice == "0":
                    print("\n👋 ¡Hasta la próxima sesión!")
                    break
                else:
                    print("❌ Opción inválida")
            
            except KeyboardInterrupt:
                print("\n\n⚠️  Operación cancelada")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def single_scan_mode(self):
        """Modo de escaneo único."""
        print("\n🔍 MODO ESCANEO ÚNICO")
        print("=" * 50)
        
        table_state = self.scan_table()
        print(f"\n📋 ESTADO DE MESA:")
        print(f"   Fase: {table_state['phase']}")
        print(f"   Tus cartas: {' '.join(table_state['hero_cards'])}")
        if table_state['board_cards']:
            print(f"   Board: {' '.join(table_state['board_cards'])}")
        print(f"   Bote: ${table_state['pot_size']}")
        print(f"   Para call: ${table_state['to_call']}")
        
        decision = self.make_decision(table_state)
        self.execute_decision(decision, table_state)
    
    def configure_mode(self):
        """Configura el modo de operación."""
        print("\n⚙️  CONFIGURAR MODO DE OPERACIÓN")
        print("=" * 50)
        print("Modos disponibles:")
        print("  1. ASSIST - Solo muestra decisiones (RECOMENDADO)")
        print("  2. SEMI_AUTO - Pregunta antes de ejecutar")
        print("  3. AUTO - Ejecuta automáticamente (AVANZADO)")
        
        choice = input("\nSeleccionar modo (1-3): ").strip()
        
        if choice == "1":
            self.mode = "ASSIST"
            print("✅ Modo: ASISTENTE (solo muestra decisiones)")
        elif choice == "2":
            self.mode = "SEMI_AUTO"
            print("✅ Modo: SEMI-AUTOMÁTICO (pregunta antes de actuar)")
        elif choice == "3":
            self.mode = "AUTO"
            print("⚠️  Modo: AUTOMÁTICO (ejecuta acciones directamente)")
            print("   ¡ADVERTENCIA! Usa bajo tu responsabilidad")
        else:
            print("❌ Opción inválida, manteniendo modo actual")

class ProfessionalDecisionEngine:
    """Motor de decisiones profesionales (versión simplificada)."""
    
    def __init__(self):
        self.experience_years = 20
        
    def make_professional_decision(self, game_state):
        """Toma una decisión profesional."""
        phase = game_state.get("phase", "preflop")
        
        # Decisiones por fase
        if phase == "preflop":
            return self.preflop_decision(game_state)
        elif phase == "flop":
            return self.flop_decision(game_state)
        elif phase == "turn":
            return self.turn_decision(game_state)
        elif phase == "river":
            return self.river_decision(game_state)
        else:
            return {"action": "FOLD", "reason": "Fase desconocida"}
    
    def preflop_decision(self, game_state):
        """Decisión preflop profesional."""
        hand = game_state.get("hand", [])
        action_to = game_state.get("action_to", "NONE")
        
        # Evaluar mano
        hand_str = self.format_hand(hand)
        hand_type = self.classify_hand(hand)
        
        if action_to == "NONE":
            if hand_type in ["AA", "KK", "QQ", "AKs"]:
                return {"action": "RAISE", "amount": 3.0, "reason": f"Mano premium {hand_str}"}
            elif hand_type in ["JJ", "TT", "AQ", "AJs"]:
                return {"action": "RAISE", "amount": 2.5, "reason": f"Mano fuerte {hand_str}"}
            else:
                return {"action": "FOLD", "reason": f"Mano muy débil {hand_str}"}
        
        elif action_to == "RAISE":
            if hand_type in ["AA", "KK", "QQ", "AKs"]:
                return {"action": "3BET", "amount": 9.0, "reason": f"3-bet con premium {hand_str}"}
            elif hand_type in ["JJ", "TT", "AQ"]:
                return {"action": "CALL", "reason": f"Call con mano fuerte {hand_str}"}
            else:
                return {"action": "FOLD", "reason": f"Fold vs raise {hand_str}"}
        
        return {"action": "FOLD", "reason": "Situación compleja"}
    
    def flop_decision(self, game_state):
        """Decisión en flop profesional."""
        hand = game_state.get("hand", [])
        board = game_state.get("board", [])
        
        # Evaluación simplificada
        if len(board) < 3:
            return {"action": "CHECK", "reason": "Board incompleto"}
        
        hand_str = self.format_hand(hand)
        board_str = self.format_hand(board)
        
        # Lógica básica
        if self.has_flush_draw(hand, board) or self.has_straight_draw(hand, board):
            return {"action": "BET", "amount": 0.67, "reason": f"Draw fuerte {hand_str} en {board_str}"}
        elif self.has_pair(hand, board):
            return {"action": "BET", "amount": 0.5, "reason": f"Par con {hand_str} en {board_str}"}
        else:
            return {"action": "CHECK", "reason": f"Mano débil {hand_str} en {board_str}"}
    
    def turn_decision(self, game_state):
        """Decisión en turn."""
        return {"action": "CHECK", "reason": "Juego cauteloso en turn"}
    
    def river_decision(self, game_state):
        """Decisión en river."""
        return {"action": "BET", "amount": 0.75, "reason": "Value bet en river"}
    
    def classify_hand(self, hand):
        """Clasifica una mano preflop."""
        if not hand or len(hand) < 2:
            return "UNKNOWN"
        
        # Simplificación
        cards = [str(c).upper() for c in hand]
        ranks = [c[0] if len(c) > 1 else c for c in cards]
        
        # Pares
        if len(set(ranks)) == 1:
            return ranks[0] * 2  # "AA", "KK", etc.
        
        # Cartas altas
        if 'A' in ranks:
            if 'K' in ranks:
                return "AKs" if cards[0][-1] == cards[1][-1] else "AKo"
            elif 'Q' in ranks:
                return "AQ"
        
        return "MEDIUM"
    
    def format_hand(self, cards):
        """Formatea cartas para display."""
        return " ".join(str(c).upper() for c in cards) if cards else "N/A"
    
    def has_flush_draw(self, hand, board):
        """Detecta draw a color."""
        all_cards = hand + board
        suits = [c[-1] if isinstance(c, str) and len(c) > 1 else '' for c in all_cards]
        
        from collections import Counter
        suit_counts = Counter(suits)
        return any(count >= 4 for count in suit_counts.values())
    
    def has_straight_draw(self, hand, board):
        """Detecta draw a escalera."""
        # Simplificación
        return len(board) >= 3
    
    def has_pair(self, hand, board):
        """Detecta si hay par."""
        all_ranks = []
        for card in hand + board:
            if isinstance(card, str) and card:
                all_ranks.append(card[0])
        
        from collections import Counter
        rank_counts = Counter(all_ranks)
        return any(count >= 2 for count in rank_counts.values())

def signal_handler(sig, frame):
    """Maneja señales de interrupción."""
    print("\n\n🛑 Sistema detenido")
    sys.exit(0)

def main():
    """Función principal."""
    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 70)
    print("🤖 POKERSTARS BOT SYSTEM - VERSIÓN 1.0")
    print("=" * 70)
    print("Sistema profesional para PokerStars")
    print("Con experiencia de juego de 20+ años")
    print("=" * 70)
    
    # Seleccionar modo inicial
    print("\n🎯 SELECCIONAR MODO INICIAL:")
    print("1. Modo ASISTENTE (recomendado para empezar)")
    print("2. Modo SEMI-AUTOMÁTICO")
    print("3. Modo AUTOMÁTICO (avanzado)")
    
    mode_choice = input("\nSelección (1-3, default 1): ").strip()
    
    mode_map = {"1": "ASSIST", "2": "SEMI_AUTO", "3": "AUTO"}
    initial_mode = mode_map.get(mode_choice, "ASSIST")
    
    # Crear sistema
    try:
        bot_system = PokerStarsBotSystem(mode=initial_mode)
        
        if bot_system.components:
            bot_system.interactive_menu()
        else:
            print("\n❌ No se pudo inicializar el sistema")
            print("💡 Verifica que los módulos en src/ estén correctos")
    
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()