"""
Integrador principal que une todos los componentes - VERSIÓN CON WRAPPERS
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
        
        # Wrappers
        self.overlay_wrapper = None
        self.adapter_wrapper = None
        self.engine_wrapper = None
        
    def initialize(self) -> bool:
        """Inicializar todos los componentes con wrappers de compatibilidad"""
        try:
            logger.info("Inicializando Poker Coach Pro con wrappers...")
            
            # 1. Inicializar motor de poker
            from src.core.poker_engine import PokerEngine
            self.poker_engine = PokerEngine()
            from src.integration.compatibility_wrappers import PokerEngineWrapper
            self.engine_wrapper = PokerEngineWrapper(self.poker_engine)
            logger.info(" Motor de poker inicializado y envuelto")
            
            # 2. Inicializar overlay
            from src.overlay.overlay_gui import PokerOverlay
            self.overlay = PokerOverlay()
            self.overlay.start()
            from src.integration.compatibility_wrappers import OverlayWrapper
            self.overlay_wrapper = OverlayWrapper(self.overlay)
            logger.info(" Overlay inicializado y envuelto")
            
            # 3. Inicializar adaptador GG Poker
            from src.platforms.ggpoker_adapter import GGPokerAdapter
            from src.integration.compatibility_wrappers import GGAdapterWrapper
            
            # Intentar crear adapter con diferentes firmas
            adapter_created = False
            for attempt in [
                lambda: GGPokerAdapter(),  # Sin parámetros
                lambda: GGPokerAdapter(poker_engine=self.poker_engine),  # Solo engine
                lambda: GGPokerAdapter(poker_engine=self.poker_engine, overlay=self.overlay),  # Ambos
                lambda: GGPokerAdapter(None, None)  # Parámetros posicionales
            ]:
                try:
                    self.ggpoker_adapter = attempt()
                    adapter_created = True
                    logger.info(f" Adaptador GG Poker creado con firma: {attempt.__name__}")
                    break
                except TypeError as e:
                    continue
                except Exception as e:
                    logger.warning(f"Intento fallido: {e}")
                    continue
            
            if not adapter_created:
                # Último intento: inspeccionar firma
                import inspect
                try:
                    sig = inspect.signature(GGPokerAdapter.__init__)
                    params = list(sig.parameters.keys())[1:]  # Excluir self
                    kwargs = {}
                    if 'poker_engine' in params:
                        kwargs['poker_engine'] = self.poker_engine
                    if 'overlay' in params:
                        kwargs['overlay'] = self.overlay
                    
                    self.ggpoker_adapter = GGPokerAdapter(**kwargs)
                    adapter_created = True
                    logger.info(f" Adaptador creado con kwargs: {kwargs.keys()}")
                except:
                    # Crear sin parámetros y rezar
                    self.ggpoker_adapter = GGPokerAdapter()
            
            self.adapter_wrapper = GGAdapterWrapper(self.ggpoker_adapter)
            logger.info(" Adaptador GG Poker inicializado y envuelto")
            
            # 4. Verificar si GG Poker está activo usando wrapper
            self.demo_mode = not self.adapter_wrapper.is_ggpoker_active()
            
            if self.demo_mode:
                logger.warning("  Modo demo activado - GG Poker no detectado")
                if self.overlay_wrapper:
                    self.overlay_wrapper.update_recommendation(
                        action="DEMO",
                        confidence=0.0,
                        reason="Modo demo - GG Poker no detectado",
                        alternatives=[]
                    )
            else:
                logger.info(" GG Poker detectado - Modo real activo")
                if self.overlay_wrapper:
                    self.overlay_wrapper.update_recommendation(
                        action="READY",
                        confidence=1.0,
                        reason="GG Poker detectado - Modo tiempo real",
                        alternatives=[]
                    )
            
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
                    current_demo_mode = not self.adapter_wrapper.is_ggpoker_active()
                    
                    if current_demo_mode != self.demo_mode:
                        self.demo_mode = current_demo_mode
                        if self.overlay_wrapper:
                            if self.demo_mode:
                                logger.info("Cambiando a modo demo")
                                self.overlay_wrapper.update_recommendation(
                                    action="DEMO",
                                    confidence=0.5,
                                    reason="Cambiado a modo demo",
                                    alternatives=[]
                                )
                            else:
                                logger.info("Cambiando a modo real")
                                self.overlay_wrapper.update_recommendation(
                                    action="READY",
                                    confidence=0.9,
                                    reason="GG Poker detectado - Modo real",
                                    alternatives=[]
                                )
                    
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
    
    def _run_demo_mode(self):
        """Ejecutar en modo demo"""
        try:
            # Generar estado de juego simulado
            demo_state = self._generate_demo_state()
            
            # Tomar decisión usando wrapper
            decision = self.engine_wrapper.make_decision(demo_state)
            
            # Mostrar en overlay usando wrapper
            if decision and self.overlay_wrapper:
                self.overlay_wrapper.update_recommendation(
                    action=decision.get("action", "FOLD"),
                    confidence=decision.get("confidence", 0.5),
                    reason=decision.get("reason", "Demo mode")[:100],
                    alternatives=decision.get("alternatives", [])
                )
        except Exception as e:
            logger.error(f"Error en modo demo: {e}")
    
    def _run_real_mode(self):
        """Ejecutar en modo real con GG Poker"""
        try:
            # Capturar y analizar pantalla usando wrapper
            game_state = self.adapter_wrapper.capture_and_analyze()
            
            if game_state:
                # Convertir a dict para poker_engine
                if hasattr(game_state, 'to_dict'):
                    state_dict = game_state.to_dict()
                elif hasattr(game_state, '__dict__'):
                    state_dict = vars(game_state)
                elif isinstance(game_state, dict):
                    state_dict = game_state
                else:
                    state_dict = {"raw_state": game_state}
                
                # Tomar decisión usando wrapper
                decision = self.engine_wrapper.make_decision(state_dict)
                
                if decision and self.overlay_wrapper:
                    # Mostrar recomendación usando wrapper
                    self.overlay_wrapper.update_recommendation(
                        action=decision.get("action", "CHECK"),
                        confidence=decision.get("confidence", 0.7),
                        reason=decision.get("reason", "")[:100],
                        alternatives=decision.get("alternatives", [])
                    )
                    
                    # Guardar en historial usando wrapper
                    self.adapter_wrapper.save_hand_history(game_state, decision)
        except Exception as e:
            logger.error(f"Error en modo real: {e}")
    
    def _generate_demo_state(self) -> Dict[str, Any]:
        """Generar estado de juego demo"""
        import random
        
        streets = ["preflop", "flop", "turn", "river"]
        positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
        actions = ["FOLD", "CHECK", "CALL", "RAISE", "ALL-IN"]
        
        # Generar cartas aleatorias para demo
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['h', 'd', 'c', 's']
        
        hero_cards = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(2)]
        community = [f"{random.choice(ranks)}{random.choice(suits)}" for _ in range(random.randint(0, 5))]
        
        return {
            "hero_cards": hero_cards,
            "community_cards": community,
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
            try:
                self.overlay.stop()
            except:
                pass
        
        logger.info(" Poker Coach Pro apagado correctamente")
