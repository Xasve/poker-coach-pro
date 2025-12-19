#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

print("="*50)
print(" VERIFICACI?N POST-REPARACI?N")
print("="*50)

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    adapter = PokerStarsAdapter()
    print(" REPARACI?N EXITOSA!")
    print("\nEl sistema deber?a funcionar ahora.")
    print("\n Ejecuta: python test_pokerstars.py")
except TypeError as e:
    print(f" Error persistente: {e}")
    print("\n El problema puede ser diferente.")
except Exception as e:
    print(f"  Otro error: {e}")

print("="*50)
