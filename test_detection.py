import sys
import os
import time

print(" POKER COACH PRO - PRUEBA DE DETECCIÓN")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

try:
    # Importar componentes
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("1. Creando adaptador PokerStars...")
    adapter = PokerStarsAdapter(stealth_level="LOW")
    print(" Adaptador creado")
    
    print("\n2. Iniciando captura...")
    adapter.start()
    print(" Captura iniciada")
    
    print("\n3. Probando detección de mesa (5 intentos)...")
    print("=" * 60)
    
    for i in range(1, 6):
        print(f"\n--- Intento {i} ---")
        
        # Esperar 1 segundo entre intentos
        time.sleep(1)
        
        # Intentar detectar mesa
        table_state = adapter.get_table_state()
        
        if table_state:
            print(" MESA DETECTADA!")
            print(f"   - Tipo: {'SIMULADA' if table_state.get('simulated') else 'REAL'}")
            print(f"   - Cartas propias: {table_state.get('cards', {}).get('hero', [])}")
            print(f"   - Cartas comunitarias: {table_state.get('cards', {}).get('community', [])}")
            print(f"   - Pozo: {table_state.get('pot', 'N/A')}")
            
            if not table_state.get('simulated'):
                print("\n PokerStars detectado correctamente!")
                print("   El sistema está funcionando en modo REAL")
                break
            else:
                print("\n  Sistema en modo SIMULADO")
                print("   Esto significa que:")
                print("   1. PokerStars no está abierto, O")
                print("   2. No puede detectar la mesa, O")
                print("   3. No hay templates de cartas")
        else:
            print(" No se pudo obtener estado de la mesa")
    
    print("\n4. Deteniendo sistema...")
    adapter.stop()
    print(" Sistema detenido")
    
except Exception as e:
    print(f"\n ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print(" PRUEBA COMPLETADA")
print("\n RESULTADO: El sistema " + ("FUNCIONA" if 'table_state' in locals() and table_state else "NO DETECTA POKERSTARS"))
