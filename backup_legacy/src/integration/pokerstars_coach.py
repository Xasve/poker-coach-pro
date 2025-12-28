"""
Integrador específico para PokerStars
"""
import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PokerStarsCoach:
    """Coach especializado para PokerStars"""
    
    def __init__(self):
        self.poker_engine = None
        self.pokerstars_adapter = None
        self.overlay = None
        self.running = False
        self.demo_mode = False
        self.hand_count = 0
        
    def initialize(self):
        """Inicializar todos los componentes"""
        print(" Inicializando PokerStars Coach...")
        
        try:
            # 1. Inicializar motor de poker
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            print(" PokerEngine inicializado")
            
            # 2. Inicializar adaptador PokerStars
            from src.platforms.pokerstars_adapter import PokerStarsAdapter
            self.pokerstars_adapter = PokerStarsAdapter()
            print(" PokerStarsAdapter inicializado")
            
            # 3. Verificar si PokerStars está activo
            self.demo_mode = not self.pokerstars_adapter.is_pokerstars_active()
            
            if self.demo_mode:
                print("  Modo demo activado - PokerStars no detectado")
                print(" Asegúrate de tener PokerStars abierto y visible")
            else:
                print(" PokerStars detectado - Modo tiempo real")
            
            # 4. Inicializar overlay simple (sin threading)
            self._init_simple_overlay()
            
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando: {e}")
            print(f" Error: {e}")
            return False
    
    def _init_simple_overlay(self):
        """Inicializar overlay simplificado"""
        try:
            # Intentar importar overlay simple
            from src.overlay.simple_overlay import ThreadSafeOverlay
            self.overlay = ThreadSafeOverlay()
            print(" Overlay inicializado (modo texto)")
        except:
            print("  Overlay no disponible - usando consola")
            self.overlay = None
    
    def run(self):
        """Ejecutar bucle principal"""
        self.running = True
        
        if self.demo_mode:
            self._run_demo_mode()
        else:
            self._run_real_mode()
    
    def _run_real_mode(self):
        """Ejecutar en modo real con PokerStars"""
        print("\n" + "=" * 60)
        print(" POKER COACH PRO - MODO POKERSTARS")
        print("=" * 60)
        print("\n Conectado a PokerStars")
        print(" El sistema analizará cada mano en tiempo real")
        print(" Recomendaciones GTO aparecerán automáticamente")
        print("\n  Presiona Ctrl+C para pausar/continuar")
        print("  Presiona Ctrl+Q para salir")
        print("=" * 60)
        
        last_state = None
        
        while self.running:
            try:
                # 1. Capturar y analizar estado actual
                current_state = self.pokerstars_adapter.capture_and_analyze()
                
                if current_state and current_state.is_valid():
                    # Solo procesar si es un estado nuevo
                    if self._is_new_state(current_state, last_state):
                        self.hand_count += 1
                        
                        # 2. Mostrar información
                        self._display_hand_info(current_state, self.hand_count)
                        
                        # 3. Tomar decisión
                        decision = self.poker_engine.make_decision(current_state.to_dict())
                        
                        # 4. Mostrar recomendación
                        self._display_recommendation(decision)
                        
                        # 5. Guardar en historial
                        self.pokerstars_adapter.save_hand_history(current_state, decision)
                        
                        last_state = current_state
                
                # Pequeña pausa para no saturar CPU
                time.sleep(1.0)
                
            except KeyboardInterrupt:
                print("\n  Pausado. Presiona Ctrl+C para continuar, Ctrl+Q para salir")
                try:
                    while True:
                        time.sleep(0.1)
                except KeyboardInterrupt:
                    print("  Continuando...")
                    continue
    
    def _run_demo_mode(self):
        """Ejecutar en modo demo"""
        print("\n" + "=" * 60)
        print(" POKER COACH PRO - MODO DEMO")
        print("=" * 60)
        print("\n  PokerStars no detectado")
        print(" Para modo tiempo real:")
        print("   1. Abre PokerStars")
        print("   2. Asegúrate de que la mesa sea visible")
        print("   3. Reinicia el programa")
        print("\n Ejecutando modo demo de práctica...")
        print("=" * 60)
        
        # Usar el integrador mejorado para demo
        from src.integration.improved_integrator import ImprovedPokerCoach
        demo_coach = ImprovedPokerCoach()
        demo_coach.running = True
        demo_coach.run_demo()
    
    def _is_new_state(self, current_state, last_state) -> bool:
        """Verificar si el estado es nuevo"""
        if last_state is None:
            return True
        
        # Comparar cartas del héroe
        if current_state.hero_cards != last_state.hero_cards:
            return True
        
        # Comparar cartas comunitarias
        if current_state.community_cards != last_state.community_cards:
            return True
        
        return False
    
    def _display_hand_info(self, state, hand_number):
        """Mostrar información de la mano"""
        print(f"\n{'='*40}")
        print(f" MANO #{hand_number} - {state.street.upper()}")
        print(f"{'='*40}")
        
        print(f" Posición: {state.position}")
        print(f" Tus cartas: {', '.join(state.hero_cards) if state.hero_cards else 'No detectadas'}")
        
        if state.community_cards:
            print(f" Mesa: {', '.join(state.community_cards)}")
        
        print(f" Pot: ")
        print(f" Stack: ")
        
        if state.to_call > 0:
            print(f" Para igualar: ")
        
        print(f" Acciones: {', '.join(state.actions_available)}")
    
    def _display_recommendation(self, decision: Dict[str, Any]):
        """Mostrar recomendación"""
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', '')
        
        # Determinar color/emoji según acción
        if action == 'FOLD':
            emoji = ""
        elif action in ['RAISE', 'BET', 'ALL-IN']:
            emoji = ""
        elif action == 'CALL':
            emoji = ""
        else:
            emoji = ""
        
        print(f"\n {emoji} RECOMENDACIÓN:")
        print(f"   Acción: {action}")
        print(f"   Confianza: {confidence:.0f}%")
        print(f"   Razón: {reason}")
        
        # Mostrar en overlay si está disponible
        if self.overlay:
            self.overlay.update_recommendation(decision)
        
        # Mostrar alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            print(f"\n Alternativas: {', '.join(alternatives[:3])}")
    
    def stop(self):
        """Detener coach"""
        self.running = False
        print("\n PokerStars Coach detenido")
        
        # Mostrar estadísticas
        if self.pokerstars_adapter:
            stats = self.pokerstars_adapter.get_session_stats()
            print(f"\n Estadísticas de sesión:")
            print(f"   Manos analizadas: {stats['total_hands']}")
            print(f"   Plataforma: {stats['platform']}")
