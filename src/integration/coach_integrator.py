"""
Integrador principal que une todos los componentes
"""
import time
import logging
from typing import Optional, Dict, Any

# Asegurar que podemos importar desde src
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.core.poker_engine import PokerEngine
    from src.overlay.overlay_gui import PokerOverlay
    from src.platforms.ggpoker_adapter import GGPokerAdapter
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f" Error de importación: {e}")
    print("Intentando imports alternativos...")
    
    # Intentar imports relativos
    try:
        from core.poker_engine import PokerEngine
        from overlay.overlay_gui import PokerOverlay
        from platforms.ggpoker_adapter import GGPokerAdapter
        IMPORT_SUCCESS = True
    except ImportError:
        IMPORT_SUCCESS = False

logger = logging.getLogger(__name__)

class PokerCoachIntegrator:
    """Integrador principal que conecta todos los componentes"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        if not IMPORT_SUCCESS:
            raise ImportError("No se pudieron importar los módulos necesarios")
            
        self.config = config or {}
        self.ggpoker_adapter = None
        self.poker_engine = None
        self.overlay = None
        self.is_running = False
        self.demo_mode = False
        
    def initialize(self) -> bool:
        """Inicializar todos los componentes"""
        try:
            logger.info("Inicializando Poker Coach Pro...")
            
            # 1. Inicializar motor de poker
            self.poker_engine = PokerEngine()
            logger.info(" Motor de poker inicializado")
            
            # 2. Inicializar overlay
            self.overlay = PokerOverlay()
            self.overlay.start()
            logger.info(" Overlay inicializado")
            
            # 3. Inicializar adaptador GG Poker
            self.ggpoker_adapter = GGPokerAdapter(
                poker_engine=self.poker_engine,
                overlay=self.overlay
            )
            logger.info(" Adaptador GG Poker inicializado")
            
            # 4. Verificar si GG Poker está activo
            try:
                self.demo_mode = not self.ggpoker_adapter.is_ggpoker_active()
            except:
                self.demo_mode = True  # Si falla, modo demo por defecto
            
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
            logger.error(f" Error inicializando: {e}")
            return False
    
    def run(self):
        """Ejecutar bucle principal"""
        self.is_running = True
        logger.info("Iniciando bucle principal...")
        
        try:
            while self.is_running:
                try:
                    # Verificar si debemos cambiar entre demo/real
                    try:
                        current_demo_mode = not self.ggpoker_adapter.is_ggpoker_active()
                        if current_demo_mode != self.demo_mode:
                            self.demo_mode = current_demo_mode
                            if self.overlay:
                                if self.demo_mode:
                                    logger.info("Cambiando a modo demo")
                                    self.overlay.show_message("MODO DEMO", color="yellow")
                                else:
                                    logger.info("Cambiando a modo real")
                                    self.overlay.show_message("GG POKER DETECTADO", color="green")
                    except:
                        pass  # Si falla, mantener modo actual
                    
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
            
            if game_state and hasattr(game_state, 'is_valid') and game_state.is_valid():
                # Tomar decisión
                decision = self.poker_engine.make_decision(
                    game_state.to_dict() if hasattr(game_state, 'to_dict') else vars(game_state)
                )
                
                if decision and self.overlay:
                    # Mostrar recomendación
                    self.overlay.update_recommendation(
                        action=decision.get("action", "CHECK"),
                        confidence=decision.get("confidence", 0.7),
                        reason=decision.get("reason", ""),
                        alternatives=decision.get("alternatives", [])
                    )
                    
                    # Guardar en historial
                    if hasattr(self.ggpoker_adapter, 'save_hand_history'):
                        self.ggpoker_adapter.save_hand_history(
                            game_state, decision
                        )
        except Exception as e:
            logger.error(f"Error en modo real: {e}")
    
    def _generate_demo_state(self) -> Dict[str, Any]:
        """Generar estado de juego demo"""
        import random
        
        streets = ["preflop", "flop", "turn", "river"]
        positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
        
        return {
            "hero_cards": ["Ah", "Kd"],
            "community_cards": ["Js", "8c", "2h"][:random.randint(0, 3)],
            "street": random.choice(streets),
            "position": random.choice(positions),
            "pot": random.randint(100, 1000),
            "stack": random.randint(1000, 5000),
            "to_call": random.randint(0, 200),
            "min_raise": random.randint(50, 400),
            "max_raise": random.randint(500, 2000),
            "actions_available": ["FOLD", "CHECK", "CALL", "RAISE"]
        }
    
    def shutdown(self):
        """Apagar todos los componentes"""
        logger.info("Apagando Poker Coach Pro...")
        self.is_running = False
        
        if self.overlay:
            self.overlay.stop()
        
        logger.info(" Poker Coach Pro apagado correctamente")
