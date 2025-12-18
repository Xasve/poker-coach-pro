"""
Integrador principal que une todos los componentes - VERSIÓN CORREGIDA
"""
import time
import logging
from typing import Optional, Dict, Any

# Asegurar que podemos importar desde src
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class PokerCoachIntegrator:
    """Integrador principal que conecta todos los componentes"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.ggpoker_adapter = None
        self.poker_engine = None
        self.overlay = None
        self.is_running = False
        self.demo_mode = False
        
    def initialize(self) -> bool:
        """Inicializar todos los componentes - VERSIÓN COMPATIBLE"""
        try:
            logger.info("Inicializando Poker Coach Pro...")
            
            # 1. Inicializar motor de poker
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            logger.info(" Motor de poker inicializado")
            
            # 2. Inicializar overlay
            from src.overlay.overlay_gui import PokerOverlay
            self.overlay = PokerOverlay()
            self.overlay.start()
            logger.info(" Overlay inicializado")
            
            # 3. Inicializar adaptador GG Poker - SIN PARÁMETROS
            # (basado en el error: no acepta poker_engine y overlay)
            from src.platforms.ggpoker_adapter import GGPokerAdapter
            
            # Intentar diferentes firmas de constructor
            try:
                # Intentar con parámetros
                self.ggpoker_adapter = GGPokerAdapter(
                    poker_engine=self.poker_engine,
                    overlay=self.overlay
                )
                logger.info(" Adaptador GG Poker inicializado (con parámetros)")
            except TypeError as e:
                if "unexpected keyword argument" in str(e):
                    # Intentar sin parámetros
                    self.ggpoker_adapter = GGPokerAdapter()
                    logger.info(" Adaptador GG Poker inicializado (sin parámetros)")
                else:
                    raise
            
            # 4. Verificar si GG Poker está activo
            try:
                if hasattr(self.ggpoker_adapter, 'is_ggpoker_active'):
                    self.demo_mode = not self.ggpoker_adapter.is_ggpoker_active()
                else:
                    # Si no tiene el método, probar captura
                    logger.warning("Adaptador no tiene método is_ggpoker_active, probando captura...")
                    try:
                        test_state = self.ggpoker_adapter.capture_and_analyze()
                        self.demo_mode = test_state is None or not getattr(test_state, 'is_valid', lambda: False)()
                    except:
                        self.demo_mode = True
            except Exception as e:
                logger.warning(f"Error verificando GG Poker: {e}, usando modo demo")
                self.demo_mode = True
            
            if self.demo_mode:
                logger.warning("  Modo demo activado - GG Poker no detectado")
                if self.overlay:
                    self.overlay.show_message("MODO DEMO", color="yellow")
            else:
                logger.info(" GG Poker detectado - Modo real activo")
                if self.overlay:
                    self.overlay.show_message("GG POKER DETECTADO", color="green")
            
            return True
            
        except Exception as e:
            logger.error(f" Error inicializando: {e}", exc_info=True)
            return False
    
    def run(self):
        """Ejecutar bucle principal"""
        self.is_running = True
        logger.info("Iniciando bucle principal...")
        
        try:
            while self.is_running:
                try:
                    # Verificar modo actual
                    current_demo_mode = self._check_current_mode()
                    
                    if current_demo_mode != self.demo_mode:
                        self.demo_mode = current_demo_mode
                        if self.overlay:
                            if self.demo_mode:
                                logger.info("Cambiando a modo demo")
                                self.overlay.show_message("MODO DEMO", color="yellow")
                            else:
                                logger.info("Cambiando a modo real")
                                self.overlay.show_message("GG POKER DETECTADO", color="green")
                    
                    if self.demo_mode:
                        self._run_demo_mode()
                    else:
                        self._run_real_mode()
                        
                    # Esperar antes de siguiente iteración
                    time.sleep(1.5)
                    
                except KeyboardInterrupt:
                    logger.info("Interrupción por usuario")
                    break
                except Exception as e:
                    logger.error(f"Error en bucle principal: {e}")
                    time.sleep(2)
                    
        finally:
            self.shutdown()
    
    def _check_current_mode(self) -> bool:
        """Verificar si estamos en modo demo o real"""
        if not self.ggpoker_adapter:
            return True
            
        try:
            if hasattr(self.ggpoker_adapter, 'is_ggpoker_active'):
                return not self.ggpoker_adapter.is_ggpoker_active()
            
            # Intentar captura para verificar
            state = self.ggpoker_adapter.capture_and_analyze()
            if state is None:
                return True
                
            # Verificar si el estado es válido
            if hasattr(state, 'is_valid'):
                return not state.is_valid()
            else:
                # Si no tiene método is_valid, asumir demo si no hay datos
                return not bool(getattr(state, 'hero_cards', None))
                
        except Exception:
            return True  # Si hay error, modo demo
    
    def _run_demo_mode(self):
        """Ejecutar en modo demo"""
        try:
            # Generar estado de juego simulado
            demo_state = self._generate_demo_state()
            
            # Tomar decisión
            decision = self.poker_engine.make_decision(demo_state)
            
            # Mostrar en overlay
            if decision and self.overlay:
                self.overlay.update_recommendation(
                    action=decision.get("action", "FOLD"),
                    confidence=decision.get("confidence", 0.5),
                    reason=decision.get("reason", "Demo mode"),
                    alternatives=decision.get("alternatives", [])
                )
        except Exception as e:
            logger.error(f"Error en modo demo: {e}")
    
    def _run_real_mode(self):
        """Ejecutar en modo real con GG Poker"""
        try:
            # Capturar y analizar pantalla
            game_state = self.ggpoker_adapter.capture_and_analyze()
            
            if game_state:
                # Convertir a dict para poker_engine
                if hasattr(game_state, 'to_dict'):
                    state_dict = game_state.to_dict()
                elif hasattr(game_state, '__dict__'):
                    state_dict = vars(game_state)
                else:
                    state_dict = game_state
                
                # Tomar decisión
                decision = self.poker_engine.make_decision(state_dict)
                
                if decision and self.overlay:
                    # Mostrar recomendación
                    self.overlay.update_recommendation(
                        action=decision.get("action", "CHECK"),
                        confidence=decision.get("confidence", 0.7),
                        reason=decision.get("reason", ""),
                        alternatives=decision.get("alternatives", [])
                    )
                    
                    # Guardar en historial si existe el método
                    if hasattr(self.ggpoker_adapter, 'save_hand_history'):
                        self.ggpoker_adapter.save_hand_history(game_state, decision)
        except Exception as e:
            logger.error(f"Error en modo real: {e}")
    
    def _generate_demo_state(self) -> Dict[str, Any]:
        """Generar estado de juego demo"""
        import random
        
        streets = ["preflop", "flop", "turn", "river"]
        positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
        actions = ["FOLD", "CHECK", "CALL", "RAISE", "ALL-IN"]
        
        community_cards = ["Js", "8c", "2h", "Td", "As"]
        num_community = random.randint(0, 5)
        
        return {
            "hero_cards": ["Ah", "Kd"],
            "community_cards": community_cards[:num_community],
            "street": random.choice(streets),
            "position": random.choice(positions),
            "pot": random.randint(100, 1000),
            "stack": random.randint(1000, 5000),
            "to_call": random.randint(0, 200),
            "min_raise": random.randint(50, 400),
            "max_raise": random.randint(500, 2000),
            "actions_available": random.sample(actions, random.randint(2, 4))
        }
    
    def shutdown(self):
        """Apagar todos los componentes"""
        logger.info("Apagando Poker Coach Pro...")
        self.is_running = False
        
        if self.overlay:
            self.overlay.stop()
        
        logger.info(" Poker Coach Pro apagado correctamente")
