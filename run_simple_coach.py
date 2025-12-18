#!/usr/bin/env python3
"""
Script principal simplificado para Poker Coach Pro
"""
import os
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("=" * 60)
print(" POKER COACH PRO - VERSIÓN SIMPLIFICADA")
print("=" * 60)

# Aplicar fixes primero
print(" Aplicando fixes automáticos...")
try:
    import subprocess
    result = subprocess.run([sys.executable, "fix_all_problems.py"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("  Errores:", result.stderr)
except:
    print("  No se pudieron aplicar fixes automáticos")

print("\n Iniciando sistema...")

try:
    from src.integration.simple_integrator import SimplePokerCoach
    
    coach = SimplePokerCoach()
    if coach.start():
        print("\n Sistema ejecutándose correctamente")
    else:
        print("\n Error al iniciar el sistema")
        
except ImportError as e:
    print(f"\n Error de importación: {e}")
    print("\n Soluciones:")
    print("1. Ejecuta: python fix_all_problems.py")
    print("2. Verifica que los archivos existan en src/")
    
except Exception as e:
    print(f"\n Error: {e}")
    import traceback
    traceback.print_exc()

print("\n Programa terminado")
