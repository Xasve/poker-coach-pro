
"""
Integrador simplificado y estable para Poker Coach Pro
"""
import time
import logging
import random
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SimplePokerCoach:
    """Coach simplificado que funciona"""
    
    def __init__(self):
        self.poker_engine = None
        self.overlay = None
        self.running = False
        self.demo_mode = True
        
    def initialize(self):
        """Inicializar componentes"""
        print(" Inicializando Simple Poker Coach...")
        
        try:
            # Importar y crear PokerEngine
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            print(" PokerEngine inicializado")
            
            # Inicializar overlay
            self._init_overlay()
            
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando: {e}")
            print(f" Error: {e}")
            return False
    
    def _init_overlay(self):
        """Inicializar overlay de forma segura"""
        try:
            from src.overlay.overlay_gui import PokerOverlay
            
            self.overlay = PokerOverlay()
            
            # Iniciar en hilo
            import threading
            def run():
                try:
                    self.overlay.start()
                except Exception as e:
                    print(f"Overlay error: {e}")
            
            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            
            time.sleep(0.5)  # Esperar inicialización
            print(" Overlay inicializado")
            
        except Exception as e:
            print(f"  Overlay no disponible: {e}")
            self.overlay = None
    
    def _update_overlay(self, decision: Dict[str, Any]):
        """Actualizar overlay"""
        if not self.overlay:
            return
            
        try:
            # Crear diccionario compatible
            overlay_data = {
                "action": decision.get("action", "CHECK"),
                "confidence": decision.get("confidence", 0.5),
                "reason": decision.get("reason", ""),
                "alternatives": decision.get("alternatives", [])
            }
            
            # Llamar al método
            self.overlay.update_recommendation(overlay_data)
            
        except Exception as e:
            print(f"  Error actualizando overlay: {e}")
    
    def run_demo(self):
        """Ejecutar modo demo"""
        print("\n MODO DEMO ACTIVADO")
        print("=" * 50)
        
        hand_num = 1
        
        while self.running:
            try:
                print(f"\n MANO #{hand_num}")
                print("-" * 30)
                
                # Generar estado demo
                state = self._create_demo_state()
                
                # Mostrar info
                print(f"Posición: {state['position']}")
                print(f"Calle: {state['street']}")
                print(f"Cartas: {', '.join(state['hero_cards'])}")
                if state['community_cards']:
                    print(f"Comunidad: {', '.join(state['community_cards'])}")
                print(f"Pot: ")
                print(f"Para igualar: ")
                
                # Tomar decisión
                decision = self.poker_engine.make_decision(state)
                
                # Mostrar resultado
                print(f"\n RECOMENDACIÓN:")
                print(f"Acción: {decision.get('action', 'N/A')}")
                print(f"Confianza: {decision.get('confidence', 0)*100:.0f}%")
                print(f"Razón: {decision.get('reason', 'N/A')}")
                
                # Actualizar overlay
                self._update_overlay(decision)
                
                # Esperar
                print(f"\n Esperando... (Ctrl+C para salir)")
                hand_num += 1
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n Saliendo...")
                break
            except Exception as e:
                print(f" Error: {e}")
                time.sleep(2)
    
    def _create_demo_state(self) -> Dict[str, Any]:
        """Crear estado de demo"""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        # Cartas
        hero = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(2)]
        
        # Calle
        streets = ['preflop', 'flop', 'turn', 'river']
        street = random.choice(streets)
        
        # Cartas comunitarias
        num_comm = {'preflop': 0, 'flop': 3, 'turn': 4, 'river': 5}[street]
        community = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(num_comm)]
        
        return {
            "hero_cards": hero,
            "community_cards": community,
            "street": street,
            "position": random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
            "pot": random.randint(100, 1000),
            "stack": random.randint(1000, 5000),
            "to_call": random.randint(0, 300),
            "min_raise": random.randint(50, 400),
            "max_raise": random.randint(500, 2000),
            "actions_available": random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
        }
    
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
        if self.overlay:
            try:
                self.overlay.stop()
            except:
                pass
        print(" Coach detenido")
