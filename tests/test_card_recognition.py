"""
test_card_recognition.py - Pruebas básicas para el reconocedor de cartas
Versión simplificada que no requiere dependencias externas
"""

import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Prueba que podemos importar los módulos principales"""
    print("🧪 Probando imports...")
    
    try:
        # Intentar importar CardRecognizer
        from screen_capture.card_recognizer import CardRecognizer, Card
        print("  ✅ CardRecognizer importado correctamente")
        
        # Probar creación de objeto Card
        test_card = Card(rank='A', suit='h', confidence=0.95, position=(100, 200))
        print(f"  ✅ Objeto Card creado: {test_card}")
        
        return True
    except ImportError as e:
        print(f"  ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False

def test_card_recognizer_initialization():
    """Prueba la inicialización del CardRecognizer"""
    print("\n🧪 Probando inicialización de CardRecognizer...")
    
    try:
        from screen_capture.card_recognizer import CardRecognizer
        
        # Inicializar con diferentes configuraciones
        recognizer1 = CardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
        recognizer2 = CardRecognizer(platform="pokerstars", stealth_level="MEDIUM")
        
        print(f"  ✅ Reconocedor 1 creado: {recognizer1.platform}, {recognizer1.stealth_level}")
        print(f"  ✅ Reconocedor 2 creado: {recognizer2.platform}, {recognizer2.stealth_level}")
        
        # Probar obtención de estadísticas
        stats = recognizer1.get_stats()
        print(f"  ✅ Estadísticas obtenidas: {len(stats)} items")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_basic_functionality():
    """Prueba funcionalidades básicas sin requerir OpenCV"""
    print("\n🧪 Probando funcionalidades básicas...")
    
    try:
        from screen_capture.card_recognizer import CardRecognizer
        import numpy as np
        
        # Crear reconocedor
        recognizer = CardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
        
        # Crear imagen de prueba simple (sin OpenCV)
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Configuración de región
        region_config = {"x1": 0.2, "y1": 0.2, "x2": 0.8, "y2": 0.8}
        
        print("  ✅ Imagen de prueba y configuración creadas")
        
        # Probar actualización de estadísticas
        recognizer._update_stats(0.5, [])
        stats = recognizer.get_stats()
        print(f"  ✅ Estadísticas actualizadas: total_recognitions={stats['total_recognitions']}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("POKER COACH PRO - PRUEBAS BÁSICAS DE CARD RECOGNIZER")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Ejecutar pruebas
    if test_imports():
        tests_passed += 1
    
    if test_card_recognizer_initialization():
        tests_passed += 1
    
    if test_basic_functionality():
        tests_passed += 1
    
    # Resultados
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DE LAS PRUEBAS:")
    print(f"   Pruebas pasadas: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("   ✅ ¡Todas las pruebas pasaron!")
    else:
        print(f"   ⚠️  {total_tests - tests_passed} prueba(s) fallaron")
    
    print("=" * 60)
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)