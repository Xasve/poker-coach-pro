#!/usr/bin/env python3
"""
Poker Coach Pro - Versión híbrida (intenta captura real, fallback a simulación)
"""
import time
import logging
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HybridPokerStarsCoach:
    """Coach híbrido - Intenta captura real, si falla usa simulación"""
    
    def __init__(self):
        self.poker_engine = None
        self.adapter = None
        self.running = False
        self.real_mode = False  # True = captura real, False = simulación
        self.hand_count = 0
        
    def initialize(self):
        """Inicializar intentando todos los métodos"""
        print(" Inicializando Poker Coach Pro (Modo Híbrido)...")
        
        try:
            # 1. Siempre cargar PokerEngine
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            print(" PokerEngine inicializado")
            
            # 2. Intentar adaptador real
            try:
                from src.platforms.pokerstars_adapter_nocapture import PokerStarsAdapterNoCapture as PokerStarsAdapter
                self.adapter = PokerStarsAdapter()
                print(" PokerStarsAdapter (real) inicializado")
                
                # Verificar si funciona
                if self._test_real_capture():
                    self.real_mode = True
                    print(" MODO: CAPTURA REAL (PokerStars activo)")
                else:
                    self.real_mode = False
                    print("  MODO: SIMULACIÓN (captura real falló)")
                    
            except Exception as e:
                print(f"  Adaptador real falló: {e}")
                
                # Intentar adaptador simple
                try:
                    # from src.platforms.simple_pokerstars_adapter import SimplePokerStarsAdapter
                    self.adapter = SimplePokerStarsAdapter()
                    print(" SimplePokerStarsAdapter inicializado")
                    self.real_mode = False
                    print("  MODO: SIMULACIÓN (usando adaptador simple)")
                except Exception as e2:
                    print(f"  Adaptador simple también falló: {e2}")
                    print(" MODO: SIMULACIÓN INTERNA")
                    self.adapter = None
                    self.real_mode = False
            
            return True
            
        except Exception as e:
            print(f" Error crítico: {e}")
            return False
    
    def _test_real_capture(self) -> bool:
        """Probar si la captura real funciona"""
        if not self.adapter:
            return False
        
        try:
            # Probar captura
            state = self.adapter.capture_and_analyze()
            
            if state:
                print(f" Prueba exitosa: {getattr(state, 'street', 'unknown')}")
                return True
            else:
                print(" Prueba falló: estado None")
                return False
                
        except Exception as e:
            print(f" Prueba falló con error: {e}")
            return False
    
    def run(self):
        """Ejecutar bucle principal"""
        self.running = True
        
        print("\n" + "=" * 60)
        print(" POKER COACH PRO - MODO HÍBRIDO")
        print("=" * 60)
        
        if self.real_mode:
            print(" Conectado a PokerStars real")
            print(" Analizando mesa en tiempo real...")
        else:
            print("  Modo simulación activado")
            print(" Perfecto para práctica y aprendizaje GTO")
            print(" Se generarán situaciones realistas de poker")
        
        print("\n  Ctrl+C para pausar, Ctrl+C dos veces para salir")
        print("=" * 60)
        
        time.sleep(1)
        
        last_state_hash = ""
        
        while self.running:
            try:
                # Obtener estado actual
                current_state = self._get_current_state()
                
                if current_state:
                    # Crear hash para detectar cambios
                    state_hash = self._create_state_hash(current_state)
                    
                    # Solo procesar si es un estado nuevo
                    if state_hash != last_state_hash and state_hash:
                        self.hand_count += 1
                        
                        # Mostrar información
                        self._display_hand_info(current_state, self.hand_count)
                        
                        # Tomar decisión
                        decision = self.poker_engine.make_decision(current_state)
                        
                        # Mostrar recomendación
                        self._display_recommendation(decision)
                        
                        # Guardar en historial si hay adapter
                        if self.adapter and hasattr(self.adapter, 'save_hand_history'):
                            self.adapter.save_hand_history(current_state, decision)
                        
                        last_state_hash = state_hash
                
                # Pausa según modo
                delay = 1.0 if self.real_mode else 5.0
                time.sleep(delay)
                
            except KeyboardInterrupt:
                print("\n  Pausado. Presiona Enter para continuar, Ctrl+C para salir")
                try:
                    input()
                    print("  Continuando...")
                except KeyboardInterrupt:
                    print("\n Saliendo...")
                    self.running = False
                    break
    
    def _get_current_state(self) -> Optional[Dict[str, Any]]:
        """Obtener estado actual según el modo"""
        if self.real_mode and self.adapter:
            # Modo real con adapter
            state = self.adapter.capture_and_analyze()
            if state:
                if hasattr(state, 'to_dict'):
                    return state.to_dict()
                return state
        
        # Modo simulación (generar estado)
        return self._generate_simulated_state()
    
    def _generate_simulated_state(self) -> Dict[str, Any]:
        """Generar estado simulado"""
        import random
        
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        # Crear mazo
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        
        # Cartas
        hero_cards = [deck.pop(), deck.pop()]
        
        # Calle
        streets = [("preflop", 0), ("flop", 3), ("turn", 4), ("river", 5)]
        street_name, num_community = random.choice(streets)
        community_cards = [deck.pop() for _ in range(num_community)] if num_community > 0 else []
        
        return {
            "hero_cards": hero_cards,
            "community_cards": community_cards,
            "street": street_name,
            "position": random.choice(['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']),
            "pot": random.randint(100, 1000),
            "stack": random.randint(1000, 5000),
            "to_call": random.randint(0, 200),
            "min_raise": random.randint(50, 400),
            "max_raise": random.randint(500, 2000),
            "actions_available": random.sample(['FOLD', 'CHECK', 'CALL', 'RAISE', 'ALL-IN'], 3)
        }
    
    def _create_state_hash(self, state: Dict[str, Any]) -> str:
        """Crear hash único para el estado"""
        return str(state.get('hero_cards', [])) + str(state.get('street', ''))
    
    def _display_hand_info(self, state: Dict[str, Any], hand_number: int):
        """Mostrar información de la mano"""
        mode_indicator = "" if self.real_mode else ""
        
        print(f"\n{'='*40}")
        print(f"{mode_indicator} MANO #{hand_number} - {state['street'].upper()}")
        print(f"{'='*40}")
        
        print(f" Posición: {state['position']}")
        print(f" Tus cartas: {', '.join(state['hero_cards'])}")
        
        if state['community_cards']:
            print(f" Mesa: {', '.join(state['community_cards'])}")
        
        print(f" Pot: ")
        print(f" Stack: ")
        
        if state['to_call'] > 0:
            print(f" Para igualar: ")
        
        print(f" Acciones: {', '.join(state['actions_available'])}")
    
    def _display_recommendation(self, decision: Dict[str, Any]):
        """Mostrar recomendación"""
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', '')
        
        # Emoji según acción
        if action == 'FOLD':
            emoji = ""
        elif action in ['RAISE', 'BET', 'ALL-IN']:
            emoji = ""
        elif action == 'CALL':
            emoji = ""
        else:
            emoji = ""
        
        print(f"\n {emoji} RECOMENDACIÓN GTO:")
        print(f"   Acción: {action}")
        print(f"   Confianza: {confidence:.0f}%")
        print(f"   Razón: {reason}")
        
        # Alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n Alternativas: {', '.join(alternatives[:3])}")
    
    def stop(self):
        """Detener coach"""
        self.running = False
        
        print(f"\n{'='*40}")
        print(" RESUMEN DE SESIÓN")
        print(f"{'='*40}")
        print(f"  Manos analizadas: {self.hand_count}")
        print(f"  Modo: {'REAL' if self.real_mode else 'SIMULACIÓN'}")
        print(f"  Plataforma: PokerStars")
        print(f"{'='*40}")
        print(" Gracias por usar Poker Coach Pro!")

def main():
    """Función principal"""
    print("=" * 60)
    print(" POKER COACH PRO - VERSIÓN HÍBRIDA")
    print("=" * 60)
    print("\nEsta versión intentará:")
    print("1. Conectar con PokerStars real (si está disponible)")
    print("2. Si falla, usar simulación realista")
    print("3. Siempre dar recomendaciones GTO precisas")
    print("=" * 60)
    
    time.sleep(1)
    
    coach = HybridPokerStarsCoach()
    
    if coach.initialize():
        try:
            coach.run()
        finally:
            coach.stop()
    else:
        print("\n Error crítico al inicializar")

if __name__ == "__main__":
    main()
