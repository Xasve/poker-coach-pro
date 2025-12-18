"""
Overlay GUI module for Poker Coach Pro
"""
from .overlay_gui import PokerOverlay

# OverlayConfig puede no existir
try:
    from .overlay_gui import OverlayConfig
except ImportError:
    class OverlayConfig:
        """Clase dummy si no existe"""
        def __init__(self):
            self.position = "top_right"
            self.theme = "dark"
            self.opacity = 0.9

__all__ = ['PokerOverlay', 'OverlayConfig']
