"""
Core poker engine module for Poker Coach Pro
"""
from .poker_engine import PokerEngine

# GameState y Recommendation pueden no existir, los manejamos condicionalmente
try:
    from .poker_engine import GameState
except ImportError:
    class GameState:
        """Clase dummy si no existe en poker_engine.py"""
        pass

try:
    from .poker_engine import Recommendation
except ImportError:
    class Recommendation:
        """Clase dummy si no existe en poker_engine.py"""
        pass

__all__ = ['PokerEngine', 'GameState', 'Recommendation']
