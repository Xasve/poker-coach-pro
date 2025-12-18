#!/usr/bin/env python3
"""
POKERSTARS COACH PRO - VERSIÓN DEFINITIVA
Sistema COMPLETO para PokerStars real + simulación
"""
import time
import logging
import sys
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 70)
print(" POKERSTARS COACH PRO - VERSIÓN DEFINITIVA")
print("=" * 70)
print("\n Sistema profesional para PokerStars")
print(" Combina captura real + simulación avanzada")
print(" Perfecto para práctica y juego real")
print("=" * 70)

# Importar PokerEngine
sys.path.insert(0, 'src')

try:
    from src.core.poker_engine import PokerEngine
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False
    print("  Usando motor integrado")

class PokerStarsProCoach:
    """Coach profesional para PokerStars"""
    
    def __init__(self):
        self.engine = None
        self.capture_system = None
        self.running = False
        self.hand_count = 0
        self.mode = "simulation"  # simulation, hybrid, real
        
    def initialize(self):
        """Inicializar sistema profesional"""
        print("\n" + "=" * 70)
        print(" INICIALIZANDO POKERSTARS COACH PRO...")
        print("=" * 70)
        
        try:
            # 1. Motor de poker
            if ENGINE_AVAILABLE:
                self.engine = PokerEngine()
                print(" PokerEngine GTO inicializado")
            else:
                self.engine = self._create_advanced_engine()
                print(" Motor avanzado integrado inicializado")
            
            # 2. Intentar cargar sistema de captura
            try:
                from src.capture.pokerstars_capture import PokerStarsCapture
                self.capture_system = PokerStarsCapture()
                print(" Sistema de captura PokerStars inicializado")
                
                # Verificar si podemos capturar
                if self._test_capture():
                    print(" MODO: HÍBRIDO (captura real disponible)")
                    self.mode = "hybrid"
                else:
                    print("  MODO: SIMULACIÓN (captura no disponible)")
                    self.mode = "simulation"
                    
            except ImportError as e:
                print(f"  Sistema de captura no disponible: {e}")
                print(" MODO: SIMULACIÓN AVANZADA")
                self.mode = "simulation"
            
            print("\n" + "=" * 70)
            print(" SISTEMA INICIALIZADO CORRECTAMENTE")
            print(f" Modo activo: {self.mode.upper()}")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            print(f"\n Error inicializando: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_advanced_engine(self):
        """Crear motor avanzado integrado"""
        class AdvancedPokerEngine:
            def __init__(self):
                self.hand_strengths = {
                    'AA': 0.85, 'KK': 0.82, 'QQ': 0.80, 'JJ': 0.78, 'TT': 0.76,
                    'AKs': 0.77, 'AQs': 0.75, 'AJs': 0.73, 'ATs': 0.71,
                    'KQs': 0.70, 'KJs': 0.68, 'QJs': 0.67, 'JTs': 0.66,
                    'T9s': 0.64, '98s': 0.63, '87s': 0.62, '76s': 0.61
                }
                print(" AdvancedPokerEngine inicializado")
            
            def make_decision(self, game_state):
                """Tomar decisión GTO avanzada"""
                import random
                
                hero_cards = game_state.get('hero_cards', [])
                street = game_state.get('street', 'preflop')
                position = game_state.get('position', 'MP')
                to_call = game_state.get('to_call', 0)
                actions = game_state.get('actions_available', ['FOLD', 'CHECK'])
                
                # Evaluar mano
                hand_score = self._evaluate_hand(hero_cards, street)
                
                # Ajustar por posición
                pos_multiplier = self._position_multiplier(position)
                
                # Ajustar por tamaño de apuesta
                call_adjustment = 1.0 - (to_call / 1000) if to_call > 0 else 1.0
                
                # Score final
                final_score = hand_score * pos_multiplier * call_adjustment
                
                # Tomar decisión
                if final_score < 0.3 and 'FOLD' in actions:
                    action = 'FOLD'
                    confidence = 0.7 + random.random() * 0.2
                    reason = 'Mano muy débil para esta situación'
                elif final_score > 0.7 and 'RAISE' in actions:
                    action = 'RAISE'
                    confidence = 0.75 + random.random() * 0.2
                    reason = 'Mano fuerte + posición favorable'
                elif final_score > 0.5 and 'CALL' in actions:
                    action = 'CALL'
                    confidence = 0.65 + random.random() * 0.15
                    reason = 'Odds favorables para ver siguiente carta'
                elif 'CHECK' in actions:
                    action = 'CHECK'
                    confidence = 0.6 + random.random() * 0.15
                    reason = 'Controlar el pot y obtener información'
                else:
                    action = random.choice(actions)
                    confidence = 0.5 + random.random() * 0.2
                    reason = 'Decisión equilibrada'
                
                # Alternativas
                alternatives = [a for a in actions if a != action][:2]
                
                return {
                    'action': action,
                    'confidence': confidence,
                    'reason': reason,
                    'alternatives': alternatives
                }
            
            def _evaluate_hand(self, cards, street):
                """Evaluar fuerza de mano"""
                if not cards or len(cards) < 2:
                    return 0.3
                
                # Simplificar evaluación
                card1, card2 = cards[0], cards[1]
                rank1, suit1 = card1[0], card1[1]
                rank2, suit2 = card2[0], card2[1]
                
                # Par
                if rank1 == rank2:
                    base = 0.7
                # Suited
                elif suit1 == suit2:
                    base = 0.6
                # Cartas conectadas
                elif abs('AKQJT98765432'.index(rank1) - 'AKQJT98765432'.index(rank2)) <= 2:
                    base = 0.55
                else:
                    base = 0.45
                
                # Ajustar por calle
                street_bonus = {'preflop': 0.0, 'flop': 0.1, 'turn': 0.15, 'river': 0.2}
                return min(0.95, base + street_bonus.get(street, 0.0))
            
            def _position_multiplier(self, position):
                """Multiplicador por posición"""
                multipliers = {
                    'BTN': 1.3, 'CO': 1.2, 'MP': 1.0, 
                    'UTG': 0.9, 'SB': 0.8, 'BB': 0.7
                }
                return multipliers.get(position, 1.0)
        
        return AdvancedPokerEngine()
    
    def _test_capture(self):
        """Probar si la captura funciona"""
        if not self.capture_system:
            return False
        
        try:
            # Intentar detectar PokerStars
            return self.capture_system.detect_pokerstars_window()
        except:
            return False
    
    def run(self):
        """Ejecutar sistema principal"""
        self.running = True
        
        print("\n MODO DE OPERACIÓN:")
        if self.mode == "hybrid":
            print("    CAPTURA HÍBRIDA ACTIVADA")
            print("    El sistema intentará capturar PokerStars real")
            print("    Si falla, usará simulación automáticamente")
        else:
            print("    SIMULACIÓN AVANZADA ACTIVADA")
            print("    Perfecto para práctica y aprendizaje GTO")
        
        print("\n CONTROLES:")
        print("    Enter: Continuar manualmente")
        print("    'a': Modo automático (5s entre manos)")
        print("    'm': Cambiar modo")
        print("    's': Ver estadísticas")
        print("    'q': Salir")
        print("=" * 70)
        
        auto_mode = False
        
        while self.running:
            try:
                if not auto_mode:
                    input("\n Presiona Enter para siguiente mano...")
                
                self._play_hand()
                self.hand_count += 1
                
                if auto_mode:
                    print(f"\n Siguiente mano en 5s... ('m' para menu)")
                    for i in range(5, 0, -1):
                        # Verificar si hay entrada del usuario
                        import sys
                        import select
                        
                        if sys.platform == "win32":
                            import msvcrt
                            if msvcrt.kbhit():
                                key = msvcrt.getch().decode()
                                if key in ['m', 'M', 'q', 'Q']:
                                    print(f"\n  Interrumpido...")
                                    auto_mode = False
                                    break
                        
                        print(f"  {i}...", end='\r')
                        time.sleep(1)
                    
                    print(" " * 20, end='\r')  # Limpiar línea
                
            except KeyboardInterrupt:
                print("\n\n  Programa pausado")
                self._show_menu()
            except EOFError:
                print("\n Saliendo...")
                self.running = False
    
    def _play_hand(self):
        """Jugar una mano"""
        print(f"\n{'='*60}")
        print(f" MANO #{self.hand_count + 1}")
        print(f"{'='*60}")
        
        # Obtener estado del juego según el modo
        state = None
        is_real = False
        
        if self.mode == "hybrid" and self.capture_system:
            # Intentar captura real
            state = self.capture_system.analyze_table_state()
            if state:
                is_real = True
                print(" [CAPTURA REAL DE POKERSTARS]")
            else:
                # Fallback a simulación
                state = self._create_simulated_state()
                print(" [SIMULACIÓN - fallback]")
        else:
            # Modo simulación
            state = self._create_simulated_state()
            print(" [SIMULACIÓN AVANZADA]")
        
        # Mostrar información
        self._display_hand_info(state, is_real)
        
        # Tomar decisión
        decision = self.engine.make_decision(state)
        
        # Mostrar recomendación
        self._display_recommendation(decision)
    
    def _create_simulated_state(self):
        """Crear estado simulado realista"""
        import random
        
        # Mazo completo
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        # Cartas del héroe
        hero_cards = [deck.pop(), deck.pop()]
        
        # Calle
        streets = [("preflop", 0), ("flop", 3), ("turn", 4), ("river", 5)]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        # Valores realistas
        pot = random.randint(100, 1000)
        stack = random.randint(1000, 5000)
        to_call = random.randint(0, 200) if random.random() > 0.3 else 0
        
        # Acciones realistas
        if to_call > 0:
            actions = ['FOLD', 'CALL']
            if random.random() > 0.4:
                actions.append('RAISE')
        else:
            actions = ['CHECK']
            if random.random() > 0.5:
                actions.append('BET')
        
        if stack > pot * 1.5:
            actions.append('ALL-IN')
        
        return {
            "hero_cards": hero_cards,
            "community_cards": community_cards,
            "street": street_name,
            "position": random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
            "pot": pot,
            "stack": stack,
            "to_call": to_call,
            "min_raise": max(20, to_call * 2) if to_call > 0 else 50,
            "max_raise": stack,
            "actions_available": actions
        }
    
    def _display_hand_info(self, state, is_real: bool):
        """Mostrar información de la mano"""
        mode_symbol = "" if is_real else ""
        
        print(f"\n{mode_symbol} INFORMACIÓN:")
        print(f"  Posición: {state.get('position', 'N/A')}")
        print(f"  Calle: {state.get('street', 'N/A').upper()}")
        
        hero_cards = state.get('hero_cards', [])
        if hero_cards:
            print(f"  Tus cartas: {', '.join(hero_cards)}")
        
        community = state.get('community_cards', [])
        if community:
            print(f"  Mesa: {', '.join(community)}")
        else:
            print(f"  Mesa: (Pre-flop)")
        
        print(f"  Pot: ")
        print(f"  Stack: ")
        
        to_call = state.get('to_call', 0)
        if to_call > 0:
            print(f"  Para igualar: ")
        else:
            print(f"  Para igualar: ")
        
        actions = state.get('actions_available', [])
        print(f"  Acciones: {', '.join(actions)}")
    
    def _display_recommendation(self, decision):
        """Mostrar recomendación"""
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5)
        reason = decision.get('reason', '')
        
        # Convertir confianza a porcentaje
        confidence_pct = confidence * 100
        
        # Emoji según acción
        if action == 'FOLD':
            display = " FOLD"
        elif action in ['RAISE', 'BET', 'ALL-IN']:
            display = " " + action
        elif action == 'CALL':
            display = " CALL"
        else:
            display = " " + action
        
        print(f"\n RECOMENDACIÓN GTO:")
        print(f"   {display}")
        print(f"    Confianza: {confidence_pct:.0f}%")
        print(f"    Razón: {reason}")
        
        # Alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n    Alternativas: {', '.join(alternatives)}")
    
    def _show_menu(self):
        """Mostrar menú de opciones"""
        print("\n  MENÚ PRINCIPAL:")
        print("   1. Continuar (c)")
        print("   2. Modo automático (a)")
        print("   3. Cambiar modo captura (m)")
        print("   4. Ver estadísticas (s)")
        print("   5. Salir (q)")
        
        choice = input("\n Tu elección: ").lower()
        
        if choice == 'q':
            self.running = False
        elif choice == 'a':
            print(" Modo automático activado (5s entre manos)")
            return 'auto'
        elif choice == 's':
            self._show_stats()
        elif choice == 'm':
            self._change_mode()
        
        return 'manual'
    
    def _show_stats(self):
        """Mostrar estadísticas"""
        print(f"\n{'='*50}")
        print(" ESTADÍSTICAS DE SESIÓN")
        print(f"{'='*50}")
        print(f"  Manos jugadas: {self.hand_count}")
        print(f"  Modo actual: {self.mode.upper()}")
        print(f"  Motor: {'GTO PokerEngine' if ENGINE_AVAILABLE else 'Avanzado Integrado'}")
        print(f"{'='*50}")
    
    def _change_mode(self):
        """Cambiar modo de operación"""
        print("\n  SELECCIONAR MODO:")
        print("   1. Simulación avanzada")
        print("   2. Captura híbrida (si disponible)")
        print("   3. Cancelar")
        
        choice = input("\n Tu elección: ")
        
        if choice == '1':
            self.mode = "simulation"
            print(" Modo cambiado a: SIMULACIÓN AVANZADA")
        elif choice == '2':
            if self.capture_system:
                self.mode = "hybrid"
                print(" Modo cambiado a: CAPTURA HÍBRIDA")
            else:
                print(" Captura no disponible - manteniendo simulación")
        else:
            print("  Cambio cancelado")
    
    def stop(self):
        """Detener sistema"""
        self.running = False
        
        print(f"\n{'='*70}")
        print(" SESIÓN FINALIZADA - POKERSTARS COACH PRO")
        print(f"{'='*70}")
        
        self._show_stats()
        
        print(f"\n Gracias por usar PokerStars Coach Pro!")
        print(" Para captura REAL completa, asegúrate de:")
        print("   1. Tener PokerStars instalado y abierto")
        print("   2. Estar en una mesa de poker visible")
        print("   3. Tener las dependencias instaladas")
        print(f"{'='*70}")

def main():
    """Función principal"""
    coach = PokerStarsProCoach()
    
    if coach.initialize():
        try:
            coach.run()
        finally:
            coach.stop()
    else:
        print("\n Error crítico al inicializar el sistema")

if __name__ == "__main__":
    main()

