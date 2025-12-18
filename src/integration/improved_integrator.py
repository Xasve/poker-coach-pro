"""
Integrador mejorado para Poker Coach Pro
"""
import time
import logging
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ImprovedPokerCoach:
    """Coach mejorado sin problemas de threading"""
    
    def __init__(self):
        self.poker_engine = None
        self.running = False
        self.hand_number = 1
        
    def initialize(self):
        """Inicializar solo PokerEngine (sin overlay problemático)"""
        print(" Inicializando Poker Coach Pro...")
        
        try:
            # Importar y crear PokerEngine
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            print(" PokerEngine inicializado")
            
            # No usar overlay por ahora (problemas de threading)
            print("  Overlay desactivado (problemas de threading en Windows)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando: {e}")
            print(f" Error: {e}")
            return False
    
    def run_demo(self):
        """Ejecutar modo demo mejorado"""
        print("\n" + "=" * 60)
        print(" POKER COACH PRO - MODO DEMO")
        print("=" * 60)
        
        print("\n INSTRUCCIONES:")
        print(" El sistema generará manos de poker aleatorias")
        print(" Tomará decisiones basadas en estrategia GTO")
        print(" Presiona Ctrl+C para salir")
        print("=" * 60)
        
        while self.running:
            try:
                self._play_demo_hand()
                self.hand_number += 1
                
                # Pausa entre manos
                print("\n Preparando siguiente mano... (Ctrl+C para salir)")
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n Saliendo...")
                break
            except Exception as e:
                print(f"\n Error: {e}")
                time.sleep(2)
    
    def _play_demo_hand(self):
        """Jugar una mano demo"""
        print(f"\n{'='*40}")
        print(f" MANO #{self.hand_number}")
        print(f"{'='*40}")
        
        # Generar estado realista
        state = self._create_realistic_state()
        
        # Mostrar información
        self._display_hand_info(state)
        
        # Tomar decisión
        decision = self.poker_engine.make_decision(state)
        
        # Mostrar recomendación
        self._display_recommendation(decision)
    
    def _create_realistic_state(self) -> Dict[str, Any]:
        """Crear estado de juego realista"""
        # Mazo completo
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        # Crear mazo y barajar
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        # Repartir cartas únicas
        hero_cards = [deck.pop(), deck.pop()]
        
        # Determinar calle y cartas comunitarias
        streets = [
            ("PREFLOP", 0),
            ("FLOP", 3), 
            ("TURN", 4),
            ("RIVER", 5)
        ]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        # Posiciones
        positions = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']
        position = random.choice(positions)
        
        # Valores realistas
        pot_base = random.choice([100, 200, 300, 400, 500])
        pot = pot_base + random.randint(0, 200)
        
        stack = random.choice([1000, 1500, 2000, 2500, 3000])
        
        # Calcular to_call basado en posición y pot
        if position in ['SB', 'BB']:
            to_call = random.choice([0, 10, 20, 40])
        else:
            to_call = random.randint(0, pot // 4)
        
        return {
            "hero_cards": hero_cards,
            "community_cards": community_cards,
            "street": street_name.lower(),
            "position": position,
            "pot": pot,
            "stack": stack,
            "to_call": to_call,
            "min_raise": max(20, to_call * 2),
            "max_raise": stack,
            "actions_available": self._get_available_actions(to_call, position)
        }
    
    def _get_available_actions(self, to_call: int, position: str) -> list:
        """Obtener acciones disponibles basadas en la situación"""
        actions = []
        
        if to_call > 0:
            actions.extend(['FOLD', 'CALL'])
            if position != 'UTG':  # Más agresivo en posiciones tardías
                actions.append('RAISE')
        else:
            actions.extend(['CHECK', 'BET'])
        
        # Siempre disponible (si stack alcanza)
        actions.append('ALL-IN')
        
        return list(set(actions))  # Remover duplicados
    
    def _display_hand_info(self, state: Dict[str, Any]):
        """Mostrar información de la mano"""
        print(f"\n INFORMACIÓN DE LA MANO:")
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
    
    def _display_recommendation(self, decision: Dict[str, Any]):
        """Mostrar recomendación"""
        print(f"\n RECOMENDACIÓN DEL COACH:")
        print(f"{'='*30}")
        
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', 'Sin razón específica')
        
        # Color según acción
        if action == 'FOLD':
            color = ""
        elif action in ['RAISE', 'BET', 'ALL-IN']:
            color = ""
        else:
            color = ""
        
        print(f"{color} Acción: {action}")
        print(f" Confianza: {confidence:.0f}%")
        print(f" Razón: {reason}")
        
        # Mostrar alternativas si existen
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n Alternativas consideradas:")
            for alt in alternatives[:3]:  # Mostrar máximo 3
                print(f"    {alt}")
    
    def start(self):
        """Iniciar coach"""
        if not self.initialize():
            return False
            
        self.running = True
        self.run_demo()
        return True
    
    def stop(self):
        """Detener coach"""
        self.running = False
        print("\n Coach detenido correctamente")
