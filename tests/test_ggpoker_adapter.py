"""
test_ggpoker.py - Prueba rápida del adaptador GG Poker
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from platforms.ggpoker_adapter import test_ggpoker_adapter
    print("🎴 POKER COACH PRO - TEST GG POKER ADAPTER")
    print("=" * 50)
    
    if test_ggpoker_adapter():
        print("\n✅ ¡ADAPTADOR GG POKER FUNCIONANDO!")
    else:
        print("\n❌ Adaptador con problemas")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    import traceback
    traceback.print_exc()