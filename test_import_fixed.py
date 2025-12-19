# test_import_fixed.py
import sys
import os

print("=== TEST DE IMPORTACIÓN CORREGIDO ===")
print("=" * 50)

# Forzar encoding UTF-8 para todo
import locale
locale.getpreferredencoding = lambda: 'UTF-8'

# Añadir src al path
sys.path.insert(0, 'src')

print("1. Verificando encoding del sistema...")
print(f"   Encoding por defecto: {locale.getpreferredencoding()}")

print("\n2. Probando importación con encoding forzado...")
try:
    # Leer el archivo con encoding correcto primero
    adapter_path = "src/platforms/pokerstars_adapter.py"
    
    with open(adapter_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        print(f"   ✅ Archivo leído: {len(content)} caracteres")
    
    # Ahora importar
    from platforms.pokerstars_adapter import PokerStarsAdapter
    print("   ✅ PokerStarsAdapter importado")
    
    # Crear instancia
    adapter = PokerStarsAdapter(stealth_level="LOW")
    print("   ✅ Instancia creada")
    
    print("\n3. Probando ciclo básico...")
    
    # Iniciar
    start_result = adapter.start()
    print(f"   - start(): {start_result}")
    
    # Obtener estado
    import time
    time.sleep(1)
    
    state = adapter.get_table_state()
    print(f"   - get_table_state(): {state is not None}")
    
    if state:
        print(f"     Keys: {list(state.keys())}")
        if 'simulated' in state:
            print("     Modo: SIMULADO")
        else:
            print("     Modo: REAL")
    
    # Detener
    stop_result = adapter.stop()
    print(f"   - stop(): {stop_result}")
    
    print("\n✅ IMPORTACIÓN EXITOSA")
    
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print("\n💡 Posible problema de encoding en el archivo")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    
    # Mostrar error específico
    import traceback
    traceback.print_exc()
    
except Exception as e:
    print(f"❌ Error inesperado: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("✅ Test completado")