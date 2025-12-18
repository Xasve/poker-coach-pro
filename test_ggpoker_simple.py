"""
test_ggpoker_simple.py - Prueba simple del adaptador GG Poker
Ejecutar desde la raíz: python test_ggpoker_simple.py
"""

import sys
import os
import numpy as np

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_simple():
    print("🧪 PRUEBA SIMPLE: GGPokerAdapter")
    print("=" * 50)
    
    try:
        # Importar componentes individualmente primero
        print("1. Probando imports...")
        
        from screen_capture.adaptive_recognizer import AdaptiveCardRecognizer
        print("   ✅ AdaptiveCardRecognizer importado")
        
        from screen_capture.table_detector import TableDetector
        print("   ✅ TableDetector importado")
        
        from screen_capture.text_ocr import TextOCR
        print("   ✅ TextOCR importado")
        
        from screen_capture.stealth_capture import StealthScreenCapture
        print("   ✅ StealthScreenCapture importado")
        
        # Ahora importar el adaptador
        print("\n2. Importando GGPokerAdapter...")
        from platforms.ggpoker_adapter import GGPokerAdapter, test_ggpoker_adapter
        
        print("   ✅ GGPokerAdapter importado correctamente")
        
        # Ejecutar test
        print("\n3. Ejecutando test del adaptador...")
        print("-" * 40)
        
        # Ejecutar la función de test que está en el archivo
        success = test_ggpoker_adapter()
        
        if success:
            print("\n✅ ¡TODO FUNCIONA CORRECTAMENTE!")
            print("\n🎯 SIGUIENTE PASO:")
            print("   Ejecuta: python start_ggpoker_coach.py")
        else:
            print("\n⚠️  Algunas pruebas fallaron")
            
        return success
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("   1. Asegúrate de que todos los archivos existen:")
        print("      - src/screen_capture/adaptive_recognizer.py")
        print("      - src/screen_capture/table_detector.py")
        print("      - src/screen_capture/text_ocr.py")
        print("      - src/screen_capture/stealth_capture.py")
        print("\n   2. Verifica la estructura de directorios:")
        print("      poker-coach-pro/")
        print("      ├── src/")
        print("      │   ├── platforms/")
        print("      │   └── screen_capture/")
        print("      └── test_ggpoker_simple.py (este archivo)")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple()