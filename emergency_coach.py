#!/usr/bin/env python3
"""
Poker Coach Pro - Versión de emergencia para PokerStars
"""
import time
import logging
import random
from typing import Dict, Any

# Configurar logging simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyPokerStarsCoach:
    """Coach de emergencia - Funciona sin componentes problemáticos"""
    
    def __init__(self):
        self.running = False
        self.hand_count = 0
        
    def initialize(self):
        """Inicialización mínima"""
        print(" Inicializando Poker Coach Pro (Modo Emergencia)...")
        
        try:
            # Solo cargar PokerEngine
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            print(" PokerEngine inicializado")
            
            print("  Modo: SIMULACIÓN (sin captura real)")
            print(" Para captura real, necesitas resolver los errores de OpenCV")
            
            return True
            
        except Exception as e:
            print(f" Error: {e}")
            return False
    
    def run(self):
        """Ejecutar modo simulación"""
        self.running = True
        
        print("\n" + "=" * 60)
        print(" POKER COACH PRO - MODO SIMULACIÓN")
        print("=" * 60)
        print("\n  ADVERTENCIA: Este es un modo de simulación")
        print("   No se está capturando PokerStars real")
        print("   Se generan manos aleatorias para practicar")
        print("\n Perfecto para aprender estrategias GTO")
        print("=" * 60)
        
        time.sleep(2)
        
        while self.running:
            try:
                self._play_simulated_hand()
                self.hand_count += 1
                
                print(f"\n Siguiente mano en 5s... (Ctrl+C para salir)")
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n Saliendo...")
                self.running = False
                break
            except Exception as e:
                print(f"\n Error: {e}")
                time.sleep(2)
    
    def _play_simulated_hand(self):
        """Jugar una mano simulada"""
        print(f"\n{'='*40}")
        print(f" MANO #{self.hand_count + 1} (SIMULADA)")
        print(f"{'='*40}")
        
        # Generar estado realista
        state = self._generate_realistic_state()
        
        # Mostrar información
        print(f"\n INFORMACIÓN:")
        print(f"  Posición: {state['position']}")
        print(f"  Calle: {state['street'].upper()}")
        print(f"  Tus cartas: {', '.join(state['hero_cards'])}")
        
        if state['community_cards']:
            print(f"  Mesa: {', '.join(state['community_cards'])}")
        else:
            print(f"  Mesa: (Pre-flop)")
        
        print(f"  Pot: ")
        print(f"  Tu stack: ")
        
        if state['to_call'] > 0:
            print(f"  Para igualar: ")
        else:
            print(f"  Para igualar: (Sin apuesta por igualar)")
        
        print(f"  Acciones disponibles: {', '.join(state['actions_available'])}")
        
        # Tomar decisión
        decision = self.poker_engine.make_decision(state)
        
        # Mostrar recomendación
        print(f"\n RECOMENDACIÓN GTO:")
        print(f"{'='*30}")
        
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', 'Sin razón específica')
        
        # Color según acción
        if action == 'FOLD':
            emoji = ""
        elif action in ['RAISE', 'BET', 'ALL-IN']:
            emoji = ""
        elif action == 'CALL':
            emoji = ""
        else:
            emoji = ""
        
        print(f"{emoji} Acción: {action}")
        print(f" Confianza: {confidence:.0f}%")
        print(f" Razón: {reason}")
        
        # Mostrar alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n Alternativas consideradas:")
            for alt in alternatives[:3]:
                print(f"    {alt}")
    
    def _generate_realistic_state(self) -> Dict[str, Any]:
        """Generar estado de juego realista"""
        # Mazo completo
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        # Crear mazo y barajar
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        # Repartir cartas únicas
        hero_cards = [deck.pop(), deck.pop()]
        
        # Determinar calle
        streets = [
            ("preflop", 0),
            ("flop", 3), 
            ("turn", 4),
            ("river", 5)
        ]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        # Posición realista
        positions = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']
        position = random.choice(positions)
        
        # Valores realistas
        pot_base = random.choice([100, 200, 300, 400, 500])
        pot = pot_base + random.randint(0, 200)
        
        stack = random.choice([1000, 1500, 2000, 2500, 3000])
        
        # Calcular to_call basado en posición
        if position in ['SB', 'BB']:
            to_call = random.choice([0, 10, 20, 40])
        else:
            to_call = random.randint(0, pot // 4)
        
        # Acciones disponibles realistas
        if to_call > 0:
            actions = ['FOLD', 'CALL']
            if random.random() > 0.3:  # 70% chance de poder subir
                actions.append('RAISE')
        else:
            actions = ['CHECK']
            if random.random() > 0.5:  # 50% chance de poder apostar
                actions.append('BET')
        
        # Siempre disponible si hay suficiente stack
        if stack > pot * 2:
            actions.append('ALL-IN')
        
        return {
            "hero_cards": hero_cards,
            "community_cards": community_cards,
            "street": street_name,
            "position": position,
            "pot": pot,
            "stack": stack,
            "to_call": to_call,
            "min_raise": max(20, to_call * 2),
            "max_raise": stack,
            "actions_available": actions
        }
    
    def stop(self):
        """Detener coach"""
        self.running = False
        print(f"\n Sesión terminada - Manos jugadas: {self.hand_count}")
        print(" Gracias por usar Poker Coach Pro!")

def main():
    """Función principal"""
    print("=" * 60)
    print(" POKER COACH PRO - VERSIÓN DE EMERGENCIA")
    print("=" * 60)
    print("\n  MODO SIMULACIÓN ACTIVADO")
    print(" Perfecto para:")
    print("    Aprender estrategias GTO")
    print("    Practicar decisiones en diferentes situaciones")
    print("    Entender rangos de manos")
    print("=" * 60)
    
    time.sleep(1)
    
    coach = EmergencyPokerStarsCoach()
    
    if coach.initialize():
        try:
            coach.run()
        finally:
            coach.stop()
    else:
        print("\n Error al inicializar el sistema")

if __name__ == "__main__":
    main()
