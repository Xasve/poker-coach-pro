import sys
import os
import time
import cv2

print(" PRUEBA COMPLETA DEL SISTEMA POKER COACH")
print("=" * 70)

# Configurar path
sys.path.insert(0, 'src')

def test_componente(nombre, funcion):
    print(f"\n🧪 {nombre}...")
    try:
        resultado = funcion()
        print(f"    {resultado}")
        return True
    except Exception as e:
        print(f"    Error: {type(e).__name__}: {e}")
        return False

def main():
    # Test 1: Dependencias básicas
    def test_dependencias():
        import numpy as np
        import cv2
        from PIL import Image
        import mss
        return f"NumPy {np.__version__}, OpenCV {cv2.__version__}, MSS {mss.__version__}"
    
    # Test 2: Captura de pantalla
    def test_captura():
        from screen_capture.stealth_capture import StealthScreenCapture
        captura = StealthScreenCapture("pokerstars", "LOW")
        screenshot = captura.capture_screen()
        
        if screenshot is not None:
            # Guardar captura para verificar
            os.makedirs("debug", exist_ok=True)
            cv2.imwrite("debug/test_captura.jpg", screenshot)
            return f"Captura OK: {screenshot.shape}"
        return "Captura falló"
    
    # Test 3: Adaptador PokerStars
    def test_adaptador():
        from platforms.pokerstars_adapter import PokerStarsAdapter
        adapter = PokerStarsAdapter(stealth_level="LOW")
        adapter.start()
        time.sleep(1)
        
        estado = adapter.get_table_state()
        adapter.stop()
        
        if estado:
            tipo = "SIMULADO" if estado.get('simulated') else "REAL"
            return f"Adaptador OK - Modo: {tipo}"
        return "Adaptador falló"
    
    # Test 4: Motor GTO
    def test_motor():
        from core.poker_engine import PokerEngine
        motor = PokerEngine()
        decision = motor.analyze_hand(
            hole_cards=["Ah", "Ks"],
            community_cards=["Qd", "Jc", "Th"],
            pot_size=1250,
            position="middle"
        )
        return f"Motor OK - Decisión: {decision.get('action')}"
    
    # Ejecutar tests
    tests = [
        ("Dependencias", test_dependencias),
        ("Captura de pantalla", test_captura),
        ("Adaptador PokerStars", test_adaptador),
        ("Motor GTO", test_motor)
    ]
    
    resultados = []
    for nombre, funcion in tests:
        if test_componente(nombre, funcion):
            resultados.append(True)
        else:
            resultados.append(False)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print(" RESUMEN DE PRUEBAS:")
    
    for i, (nombre, _) in enumerate(tests):
        estado = " PASÓ" if resultados[i] else " FALLÓ"
        print(f"   {i+1}. {nombre}: {estado}")
    
    # Recomendaciones
    print("\n RECOMENDACIONES:")
    
    if not resultados[2]:  # Si falló adaptador
        print("   1. Abre PokerStars en tu computadora")
        print("   2. Asegúrate de que la ventana sea visible")
        print("   3. Verifica que tengas templates en data/card_templates/pokerstars/")
    
    if all(resultados):
        print("    Todo funciona! Ejecuta: python run_poker_coach_simple.py")
    else:
        print("    Revisa los componentes que fallaron")
    
    return all(resultados)

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
