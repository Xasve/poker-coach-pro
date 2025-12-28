"""
Wrappers de compatibilidad para diferentes versiones de componentes
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OverlayWrapper:
    """Wrapper para compatibilidad con PokerOverlay"""
    
    def __init__(self, overlay_instance):
        self.overlay = overlay_instance
        self._detect_method_signature()
    
    def _detect_method_signature(self):
        """Detectar la firma del método update_recommendation"""
        import inspect
        
        try:
            sig = inspect.signature(self.overlay.update_recommendation)
            params = list(sig.parameters.keys())
            
            if len(params) == 1 and params[0] == 'self':
                # Método sin parámetros o solo self
                self.method_type = 'no_params'
            elif len(params) == 2 and 'decision' in params[1]:
                # Método con parámetro 'decision'
                self.method_type = 'decision_dict'
            elif len(params) >= 4:
                # Método con parámetros individuales
                self.method_type = 'individual_params'
            else:
                # Intentar detectar por nombres comunes
                self.method_type = 'unknown'
                
            logger.info(f"Overlay method type detected: {self.method_type}")
            
        except Exception as e:
            logger.warning(f"Could not detect overlay method signature: {e}")
            self.method_type = 'unknown'
    
    def update_recommendation(self, action: str, confidence: float, 
                            reason: str = "", alternatives: list = None):
        """Actualizar recomendación en overlay (compatible)"""
        if not self.overlay:
            return
            
        try:
            # Crear diccionario de decisión
            decision_dict = {
                "action": action,
                "confidence": confidence,
                "reason": reason,
                "alternatives": alternatives or []
            }
            
            # Intentar diferentes formas de llamar al método
            if self.method_type == 'individual_params':
                self.overlay.update_recommendation(
                    action=action,
                    confidence=confidence,
                    reason=reason,
                    alternatives=alternatives or []
                )
            elif self.method_type == 'decision_dict':
                self.overlay.update_recommendation(decision_dict)
            else:
                # Método por defecto - intentar llamadas comunes
                try:
                    self.overlay.update_recommendation(decision_dict)
                except TypeError:
                    try:
                        self.overlay.update_recommendation(
                            action, confidence, reason, alternatives or []
                        )
                    except TypeError:
                        # Crear texto y usar show_message
                        text = f"{action} ({confidence:.0%})\n{reason}"
                        if hasattr(self.overlay, 'show_message'):
                            self.overlay.show_message(text, color="green" if confidence > 0.6 else "yellow")
                        elif hasattr(self.overlay, 'update_text'):
                            self.overlay.update_text(text)
                            
        except Exception as e:
            logger.error(f"Error updating overlay: {e}")

class GGAdapterWrapper:
    """Wrapper para compatibilidad con GGPokerAdapter"""
    
    def __init__(self, adapter_instance):
        self.adapter = adapter_instance
    
    def is_ggpoker_active(self) -> bool:
        """Verificar si GG Poker está activo (múltiples métodos)"""
        try:
            # Método 1: Verificar si el método existe directamente
            if hasattr(self.adapter, 'is_ggpoker_active'):
                return self.adapter.is_ggpoker_active()
            
            # Método 2: Intentar captura para verificar
            try:
                state = self.adapter.capture_and_analyze()
                if state is None:
                    return False
                    
                # Verificar si el estado tiene datos válidos
                if hasattr(state, 'is_valid'):
                    return state.is_valid()
                elif hasattr(state, 'hero_cards'):
                    return bool(state.hero_cards)
                elif hasattr(state, '__dict__'):
                    # Verificar si tiene algún dato de juego
                    state_dict = vars(state)
                    return any(key in state_dict for key in 
                              ['hero_cards', 'community_cards', 'pot', 'street'])
            except:
                return False
                
        except Exception:
            return False
    
    def capture_and_analyze(self):
        """Wrapper para capture_and_analyze"""
        return self.adapter.capture_and_analyze()
    
    def save_hand_history(self, game_state, decision):
        """Wrapper para save_hand_history"""
        if hasattr(self.adapter, 'save_hand_history'):
            self.adapter.save_hand_history(game_state, decision)

class PokerEngineWrapper:
    """Wrapper para PokerEngine"""
    
    def __init__(self, engine_instance):
        self.engine = engine_instance
    
    def make_decision(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Tomar decisión compatible"""
        try:
            return self.engine.make_decision(game_state)
        except Exception as e:
            logger.error(f"Error in engine decision: {e}")
            # Decisión por defecto
            return {
                "action": "FOLD",
                "confidence": 0.5,
                "reason": f"Error: {str(e)[:50]}",
                "alternatives": ["CHECK", "CALL"]
            }
