#!/usr/bin/env python3
"""
Poker Coach Pro - Versión mínima funcional
"""
import time
import random

print("=" * 60)
print(" POKER COACH PRO - VERSIÓN MÍNIMA")
print("=" * 60)

class MinimalPokerEngine:
    """Motor mínimo de poker"""
    
    def make_decision(self, game_state):
        """Tomar decisión simple"""
        actions = game_state.get('actions_available', ['FOLD', 'CHECK', 'CALL', 'RAISE'])
        
        # Lógica simple
        if 'RAISE' in actions and random.random() > 0.5:
            return {"action": "RAISE", "confidence": 0.7, "reason": "Agresivo"}
        elif 'CALL' in actions:
            return {"action": "CALL", "confidence": 0.6, "reason": "Pasivo"}
        else:
            return {"action": "FOLD", "confidence": 0.8, "reason": "Mano débil"}

def generate_demo_state():
    """Generar estado demo"""
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    suits = ['', '', '', '']
    
    hero = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(2)]
    
    streets = ['PREFLOP', 'FLOP', 'TURN', 'RIVER']
    street = random.choice(streets)
    
    num_community = {'PREFLOP': 0, 'FLOP': 3, 'TURN': 4, 'RIVER': 5}[street]
    community = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(num_community)]
    
    return {
        "hero_cards": hero,
        "community_cards": community,
        "street": street,
        "position": random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
        "pot": random.randint(100, 1000),
        "to_call": random.randint(0, 200),
        "actions_available": random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
    }

def main():
    """Función principal"""
    engine = MinimalPokerEngine()
    hand_num = 1
    
    print(" Sistema iniciado - Modo Demo")
    print("=" * 50)
    
    try:
        while True:
            print(f"\\n MANO #{hand_num}")
            print("-" * 30)
            
            # Generar estado
            state = generate_demo_state()
            
            # Mostrar info
            print(f"Posición: {state['position']}")
            print(f"Calle: {state['street']}")
            print(f"Tus cartas: {' '.join(state['hero_cards'])}")
            if state['community_cards']:
                print(f"Mesa: {' '.join(state['community_cards'])}")
            print(f"Pot: ")
            print(f"Para igualar: ")
            print(f"Acciones posibles: {', '.join(state['actions_available'])}")
            
            # Tomar decisión
            decision = engine.make_decision(state)
            
            # Mostrar resultado
            print(f"\\n RECOMENDACIÓN:")
            print(f" Acción: {decision['action']}")
            print(f" Confianza: {decision['confidence']*100:.0f}%")
            print(f" Razón: {decision['reason']}")
            
            hand_num += 1
            
            print("\\n Próxima mano en 5s... (Ctrl+C para salir)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\\n Programa terminado")

if __name__ == "__main__":
    main()
