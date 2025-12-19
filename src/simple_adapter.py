import time
import random

class SimplePokerAdapter:
    """Adaptador simple para pruebas"""
    
    def __init__(self):
        self.running = False
        self.hands = [
            {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"], "pot": "1250"},
            {"hero": ["QQ", "JJ"], "community": ["9s", "8h", "7d"], "pot": "800"},
            {"hero": ["Ac", "Kd"], "community": ["Qh", "Js", "Tc"], "pot": "2100"},
            {"hero": ["TT", "99"], "community": ["Ad", "Kh", "Qc"], "pot": "500"},
            {"hero": ["AK", "AQ"], "community": ["Jd", "Th", "9s"], "pot": "1500"}
        ]
        self.current_hand = 0
        
    def start(self):
        """Iniciar adaptador"""
        self.running = True
        print("🔄 Adaptador iniciado (modo simulado)")
        
    def stop(self):
        """Detener adaptador"""
        self.running = False
        print("⏹️ Adaptador detenido")
        
    def get_table_state(self):
        """Obtener estado simulado de la mesa"""
        if not self.running:
            return None
            
        hand = self.hands[self.current_hand]
        self.current_hand = (self.current_hand + 1) % len(self.hands)
        
        # Añadir variabilidad
        pot_variation = random.randint(-200, 200)
        pot = int(hand["pot"]) + pot_variation
        
        return {
            "cards": {
                "hero": hand["hero"],
                "community": hand["community"][:random.randint(3, 5)]
            },
            "pot": str(max(100, pot)),
            "mode": "SIMULATED",
            "simulated": True,
            "timestamp": time.time()
        }

# Exportar para uso en main.py
if __name__ == "__main__":
    adapter = SimplePokerAdapter()
    adapter.start()
    
    for i in range(5):
        state = adapter.get_table_state()
        print(f"\nMano {i+1}:")
        print(f"  Hero: {state['cards']['hero']}")
        print(f"  Community: {state['cards']['community']}")
        print(f"  Pot: {state['pot']}")
        time.sleep(1)
    
    adapter.stop()
