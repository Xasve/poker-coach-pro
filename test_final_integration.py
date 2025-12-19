# test_final_integration.py

import sys
import os
import time

# Añadir src al path
sys.path.insert(0, 'src')

def test_pokerstars_system():
    """Prueba completa del sistema PokerStars"""
    
    print("🧪 INICIANDO PRUEBA DEL SISTEMA POKERSTARS")
    print("=" * 50)
    
    try:
        # 1. Importar adaptador
        from platforms.pokerstars_adapter import PokerStarsAdapter
        print("✅ PokerStarsAdapter importado correctamente")
        
        # 2. Crear instancia
        adapter = PokerStarsAdapter(stealth_level="MEDIUM")
        print("✅ Adaptador instanciado")
        
        # 3. Probar inicio
        print("🔍 Probando captura de pantalla...")
        success = adapter.start()
        
        if success:
            print("✅ Captura iniciada")
            
            # 4. Esperar un momento para captura
            time.sleep(2)
            
            # 5. Probar detección básica
            print("🔍 Analizando estado de la mesa...")
            table_state = adapter.analyze_table_state()
            
            if table_state:
                print(f"✅ Mesa detectada: {table_state['table']}")
                print(f"📊 Información obtenida:")
                print(f"   - Plataforma: {table_state['platform']}")
                print(f"   - Cartas: {table_state.get('cards', 'No detectadas')}")
                print(f"   - Pozo: {table_state.get('pot', 'No detectado')}")
            else:
                print("⚠️  No se pudo detectar la mesa (¿PokerStars abierto?)")
            
            # 6. Detener
            adapter.stop()
            print("✅ Sistema detenido correctamente")
            
        else:
            print("❌ No se pudo iniciar la captura")
            
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)
    print("🧪 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_pokerstars_system()