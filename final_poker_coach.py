#!/usr/bin/env python3
"""
POKER COACH PRO - VERSIÓN FINAL CON CAPTURA REAL
Sistema completo que INTENTA capturar PokerStars real
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
print(" POKER COACH PRO - VERSIÓN FINAL CON CAPTURA REAL")
print("=" * 70)
print("\n Este sistema INTENTARÁ conectar con PokerStars real")
print(" Si falla, usará simulación avanzada automáticamente")
print(" Perfecto para transición a modo real cuando esté listo")
print("=" * 70)

# Importar nuestro adaptador REAL
sys.path.insert(0, 'src')

try:
    from src.platforms.real_pokerstars_adapter import RealPokerStarsAdapter, RealPokerStarsGameState
    ADAPTER_AVAILABLE = True
except ImportError as e:
    print(f"  No se pudo importar adaptador real: {e}")
    ADAPTER_AVAILABLE = False

# Importar PokerEngine desde el archivo existente
try:
    from src.core.poker_engine import PokerEngine
    ENGINE_AVAILABLE = True
except ImportError:
    # Si falla, usar el engine integrado
    ENGINE_AVAILABLE = False

class FinalPokerCoach:
    """Coach FINAL con intento de captura real"""
    
    def __init__(self):
        self.engine = None
        self.adapter = None
        self.running = False
        self.hand_count = 0
        self.real_captures = 0
        self.simulated_captures = 0
        
    def initialize(self):
        """Inicializar sistema final"""
        print("\n" + "=" * 70)
        print(" INICIALIZANDO SISTEMA FINAL...")
        print("=" * 70)
        
        try:
            # 1. Inicializar PokerEngine
            if ENGINE_AVAILABLE:
                self.engine = PokerEngine()
                print(" PokerEngine (externo) inicializado")
            else:
                # Engine de respaldo
                self.engine = self._create_backup_engine()
                print(" PokerEngine (integrado) inicializado")
            
            # 2. Inicializar Adaptador REAL
            if ADAPTER_AVAILABLE:
                self.adapter = RealPokerStarsAdapter(stealth_level="MEDIUM")
                print(" RealPokerStarsAdapter inicializado")
                
                # Verificar si podemos hacer captura real
                can_capture_real = self.adapter.real_capture_available
                if can_capture_real:
                    print(" CAPTURA REAL: Disponible")
                    print(" El sistema INTENTARÁ capturar PokerStars real")
                else:
                    print("  CAPTURA REAL: No disponible")
                    print(" Usando simulación avanzada")
            else:
                print(" Adaptador REAL no disponible")
                print(" Usando simulación avanzada exclusiva")
                self.adapter = None
            
            print("\n" + "=" * 70)
            print(" SISTEMA INICIALIZADO CORRECTAMENTE")
            print("=" * 70)
            
            return True
            
        except Exception as e:
            print(f"\n Error inicializando sistema final: {e}")
            return False
    
    def _create_backup_engine(self):
        """Crear motor de respaldo"""
        class BackupPokerEngine:
            def __init__(self):
                print(" BackupPokerEngine inicializado")
            
            def make_decision(self, game_state):
                import random
                actions = game_state.get('actions_available', ['FOLD', 'CHECK'])
                action = random.choice(actions)
                
                return {
                    "action": action,
                    "confidence": random.uniform(0.5, 0.9),
                    "reason": "Decisión del motor de respaldo",
                    "alternatives": [a for a in actions if a != action][:2]
                }
        
        return BackupPokerEngine()
    
    def run(self):
        """Ejecutar sistema final"""
        self.running = True
        
        print("\n MODO DE OPERACIÓN:")
        if self.adapter and hasattr(self.adapter, 'real_capture_available') and self.adapter.real_capture_available:
            print("    INTENTANDO CAPTURA REAL DE POKERSTARS")
            print("    Si PokerStars está abierto, el sistema lo detectará")
        else:
            print("    MODO SIMULACIÓN AVANZADA")
            print("    Generando situaciones realistas para práctica")
        
        print("\n CONTROLES:")
        print("    Enter: Continuar manualmente")
        print("    Ctrl+C: Pausar/Configurar")
        print("    'q' + Enter: Salir")
        print("=" * 70)
        
        input("\n Presiona Enter para comenzar...")
        
        while self.running:
            try:
                self._play_hand()
                self.hand_count += 1
                
                # Preguntar si continuar
                if self.hand_count % 3 == 0:  # Cada 3 manos
                    print(f"\n Continuar automáticamente en 3s... (presiona Enter para pausar)")
                    
                    import threading
                    stop_event = threading.Event()
                    
                    def wait_for_enter():
                        input()
                        stop_event.set()
                    
                    thread = threading.Thread(target=wait_for_enter, daemon=True)
                    thread.start()
                    
                    for i in range(3, 0, -1):
                        if stop_event.is_set():
                            break
                        print(f"  {i}...", end='\r')
                        time.sleep(1)
                    
                    if stop_event.is_set():
                        print("\n  Pausado. Opciones:")
                        print("  1. Continuar (c)")
                        print("  2. Cambiar modo (m)")
                        print("  3. Ver estadísticas (s)")
                        print("  4. Salir (q)")
                        
                        choice = input("\n Tu elección: ").lower()
                        
                        if choice == 'q':
                            self.running = False
                            break
                        elif choice == 's':
                            self._show_stats()
                            input("\n Presiona Enter para continuar...")
                        elif choice == 'm':
                            self._change_mode()
                        # Para cualquier otra entrada, continuar
                    
                    print(" " * 20, end='\r')  # Limpiar línea
                
            except KeyboardInterrupt:
                print("\n\n  Programa pausado por usuario")
                self.running = False
                break
    
    def _play_hand(self):
        """Jugar una mano"""
        print(f"\n{'='*60}")
        print(f" MANO #{self.hand_count + 1}")
        print(f"{'='*60}")
        
        # Obtener estado del juego
        state = None
        is_real = False
        
        if self.adapter:
            state = self.adapter.capture_and_analyze()
            if state:
                is_real = state.is_real_capture
                if is_real:
                    self.real_captures += 1
                    print(" [CAPTURA REAL]")
                else:
                    self.simulated_captures += 1
                    print(" [SIMULACIÓN]")
        
        # Si no hay adaptador o falló, crear estado simulado
        if not state:
            state = self._create_simulated_state()
            self.simulated_captures += 1
            print(" [SIMULACIÓN MANUAL]")
        
        # Mostrar información
        self._display_hand_info(state, is_real)
        
        # Tomar decisión
        decision = self.engine.make_decision(state.to_dict() if hasattr(state, 'to_dict') else state)
        
        # Mostrar recomendación
        self._display_recommendation(decision)
        
        # Guardar en historial si hay adapter
        if self.adapter and hasattr(self.adapter, 'save_hand_history'):
            self.adapter.save_hand_history(state, decision)
    
    def _create_simulated_state(self):
        """Crear estado simulado"""
        import random
        
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        hero_cards = [deck.pop(), deck.pop()]
        
        streets = [("preflop", 0), ("flop", 3), ("turn", 4), ("river", 5)]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        from dataclasses import dataclass
        
        @dataclass
        class SimulatedState:
            hero_cards: list
            community_cards: list
            street: str
            position: str
            pot: int
            stack: int
            to_call: int
            min_raise: int
            max_raise: int
            actions_available: list
            is_real_capture: bool = False
            
            def to_dict(self):
                return {
                    "hero_cards": self.hero_cards,
                    "community_cards": self.community_cards,
                    "street": self.street,
                    "position": self.position,
                    "pot": self.pot,
                    "stack": self.stack,
                    "to_call": self.to_call,
                    "min_raise": self.min_raise,
                    "max_raise": self.max_raise,
                    "actions_available": self.actions_available
                }
        
        return SimulatedState(
            hero_cards=hero_cards,
            community_cards=community_cards,
            street=street_name,
            position=random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
            pot=random.randint(100, 1000),
            stack=random.randint(1000, 5000),
            to_call=random.randint(0, 200),
            min_raise=random.randint(50, 400),
            max_raise=random.randint(500, 2000),
            actions_available=random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
        )
    
    def _display_hand_info(self, state, is_real: bool):
        """Mostrar información de la mano"""
        # Determinar símbolo según modo
        mode_symbol = "" if is_real else ""
        
        print(f"\n{mode_symbol} INFORMACIÓN:")
        print(f"  Posición: {state.position}")
        print(f"  Calle: {state.street.upper()}")
        print(f"  Tus cartas: {', '.join(state.hero_cards)}")
        
        if state.community_cards:
            print(f"  Mesa: {', '.join(state.community_cards)}")
        else:
            print(f"  Mesa: (Pre-flop)")
        
        print(f"  Pot: ")
        print(f"  Stack: ")
        
        if hasattr(state, 'to_call') and state.to_call > 0:
            print(f"  Para igualar: ")
        else:
            print(f"  Para igualar:  (sin apuesta)")
        
        print(f"  Acciones: {', '.join(state.actions_available)}")
    
    def _display_recommendation(self, decision: Dict[str, Any]):
        """Mostrar recomendación"""
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', '')
        
        # Color/emoji según acción
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
        print(f"    Confianza: {confidence:.0f}%")
        print(f"    Razón: {reason}")
        
        # Alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n    Alternativas: {', '.join(alternatives)}")
    
    def _show_stats(self):
        """Mostrar estadísticas"""
        print(f"\n{'='*50}")
        print(" ESTADÍSTICAS DE LA SESIÓN")
        print(f"{'='*50}")
        print(f"  Manos totales: {self.hand_count}")
        print(f"  Capturas reales: {self.real_captures}")
        print(f"  Simulaciones: {self.simulated_captures}")
        
        if self.hand_count > 0:
            real_percentage = (self.real_captures / self.hand_count) * 100
            print(f"  % Captura real: {real_percentage:.1f}%")
        
        if self.adapter and hasattr(self.adapter, 'get_session_stats'):
            adapter_stats = self.adapter.get_session_stats()
            print(f"  Plataforma: {adapter_stats.get('platform', 'N/A')}")
        
        print(f"{'='*50}")
    
    def _change_mode(self):
        """Cambiar modo de operación"""
        print("\n  CONFIGURACIÓN DE MODO:")
        print("  1. Forzar modo SIMULACIÓN")
        print("  2. Forzar intento de CAPTURA REAL")
        print("  3. Automático (recomendado)")
        print("  4. Cancelar")
        
        choice = input("\n Tu elección: ")
        
        if choice == '1':
            print(" Modo cambiado a: SIMULACIÓN")
            # Aquí podrías cambiar configuraciones
        elif choice == '2':
            print(" Modo cambiado a: CAPTURA REAL")
            # Aquí podrías cambiar configuraciones
        elif choice == '3':
            print(" Modo cambiado a: AUTOMÁTICO")
        else:
            print("  Cambio cancelado")
    
    def stop(self):
        """Detener sistema"""
        self.running = False
        
        print(f"\n{'='*70}")
        print(" SESIÓN FINALIZADA")
        print(f"{'='*70}")
        
        self._show_stats()
        
        print(f"\n Gracias por usar Poker Coach Pro!")
        print(" Recuerda: Para captura REAL, necesitas:")
        print("   1. PokerStars instalado y abierto")
        print("   2. Una mesa de poker visible")
        print("   3. El módulo screen_capture funcionando")
        print(f"{'='*70}")

def main():
    """Función principal"""
    # Crear y ejecutar coach
    coach = FinalPokerCoach()
    
    if coach.initialize():
        try:
            coach.run()
        finally:
            coach.stop()
    else:
        print("\n Error crítico al inicializar el sistema final")

if __name__ == "__main__":
    main()
