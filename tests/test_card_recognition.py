"""
test_card_recognition.py - Pruebas completas para el sistema de reconocimiento de cartas
Versión funcional sin dependencias de módulos no implementados
"""

import sys
import os
import unittest
import tempfile
from pathlib import Path
import numpy as np

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestCardRecognizer(unittest.TestCase):
    """Clase de pruebas unitarias para CardRecognizer"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.test_dir = tempfile.mkdtemp()
        
        # Crear directorio de templates temporal
        self.template_dir = Path("data/card_templates/ggpoker")
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear algunos templates de prueba básicos
        self._create_test_templates()
    
    def _create_test_templates(self):
        """Crear templates de prueba básicos usando NumPy"""
        # Solo crear templates si OpenCV está disponible
        try:
            import cv2
            
            # Crear templates básicos
            ranks = ['A', 'K', 'Q']
            suits = ['h', 's']
            
            for rank in ranks:
                for suit in suits:
                    # Crear imagen simple
                    template = np.zeros((120, 80), dtype=np.uint8)
                    
                    # Dibujar rectángulo
                    cv2.rectangle(template, (5, 5), (75, 115), 255, 2)
                    
                    # Añadir texto
                    cv2.putText(template, f"{rank}{suit}", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
                    
                    # Guardar template
                    template_path = self.template_dir / f"{rank}{suit}.png"
                    cv2.imwrite(str(template_path), template)
                    
            print(f"  ✅ Templates de prueba creados: {len(ranks) * len(suits)}")
            
        except ImportError:
            print("  ⚠️  OpenCV no disponible - usando templates simulados")
            # Crear archivos vacíos para simular templates
            ranks = ['A', 'K', 'Q']
            suits = ['h', 's']
            
            for rank in ranks:
                for suit in suits:
                    template_path = self.template_dir / f"{rank}{suit}.png"
                    template_path.touch()  # Crear archivo vacío
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        # Limpiar templates de prueba
        import shutil
        if Path("data/card_templates/ggpoker").exists():
            shutil.rmtree("data/card_templates/ggpoker", ignore_errors=True)
        if Path("data/card_templates").exists():
            # Intentar eliminar si está vacío
            try:
                Path("data/card_templates").rmdir()
            except:
                pass
        
        # Limpiar directorio temporal
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_import_card_recognizer(self):
        """Prueba que podemos importar CardRecognizer"""
        print("\n🧪 Test: Importar CardRecognizer")
        try:
            from screen_capture.card_recognizer import CardRecognizer, Card
            self.assertTrue(True, "CardRecognizer importado correctamente")
            print("  ✅ CardRecognizer importado correctamente")
            
            # Probar creación de objeto Card
            test_card = Card(rank='A', suit='h', confidence=0.95, position=(100, 200))
            self.assertEqual(test_card.rank, 'A')
            self.assertEqual(test_card.suit, 'h')
            self.assertEqual(str(test_card), 'Ah')
            print("  ✅ Objeto Card creado y validado")
            
        except ImportError as e:
            self.fail(f"No se pudo importar CardRecognizer: {e}")
    
    def test_card_recognizer_initialization(self):
        """Prueba la inicialización del CardRecognizer"""
        print("\n🧪 Test: Inicialización de CardRecognizer")
        try:
            from screen_capture.card_recognizer import CardRecognizer
            
            # Probar diferentes configuraciones
            recognizer1 = CardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
            recognizer2 = CardRecognizer(platform="pokerstars", stealth_level="MEDIUM")
            
            self.assertEqual(recognizer1.platform, "ggpoker")
            self.assertEqual(recognizer1.stealth_level, "MINIMUM")
            self.assertEqual(recognizer2.platform, "pokerstars")
            self.assertEqual(recognizer2.stealth_level, "MEDIUM")
            
            print(f"  ✅ Reconocedor 1: {recognizer1.platform}, {recognizer1.stealth_level}")
            print(f"  ✅ Reconocedor 2: {recognizer2.platform}, {recognizer2.stealth_level}")
            
            # Probar obtención de estadísticas
            stats = recognizer1.get_stats()
            self.assertIn("total_recognitions", stats)
            self.assertIn("templates_loaded", stats)
            print(f"  ✅ Estadísticas obtenidas: {len(stats)} items")
            
        except Exception as e:
            self.fail(f"Error en inicialización: {e}")
    
    def test_card_object_functionality(self):
        """Prueba la funcionalidad del objeto Card"""
        print("\n🧪 Test: Funcionalidad del objeto Card")
        from screen_capture.card_recognizer import Card
        
        # Crear diferentes cartas
        cards = [
            Card('A', 'h', 0.95, (100, 200)),
            Card('K', 's', 0.92, (150, 200)),
            Card('Q', 'd', 0.89, (200, 200)),
            Card('10', 'c', 0.87, (250, 200))
        ]
        
        # Verificar propiedades
        self.assertEqual(cards[0].to_poker_format(), 'Ah')
        self.assertEqual(cards[1].to_poker_format(), 'Ks')
        self.assertEqual(str(cards[2]), 'Qd')
        self.assertEqual(cards[3].rank, '10')
        
        print(f"  ✅ {len(cards)} objetos Card creados y validados")
    
    def test_region_extraction(self):
        """Prueba la extracción de regiones de interés"""
        print("\n🧪 Test: Extracción de regiones")
        try:
            from screen_capture.card_recognizer import CardRecognizer
            
            recognizer = CardRecognizer()
            
            # Crear imagen de prueba
            test_image = np.zeros((600, 800, 3), dtype=np.uint8)
            test_image[100:500, 200:600] = 255  # Área blanca en el centro
            
            # Configuración de región
            region_config = {
                "x1": 0.25,  # 200px
                "y1": 0.25,  # 150px
                "x2": 0.75,  # 600px
                "y2": 0.75   # 450px
            }
            
            # Extraer ROI
            roi = recognizer._extract_roi(test_image, region_config)
            
            self.assertIsNotNone(roi, "ROI no debería ser None")
            self.assertEqual(roi.shape[0], 300)  # 450-150 = 300
            self.assertEqual(roi.shape[1], 400)  # 600-200 = 400
            
            print(f"  ✅ ROI extraída: {roi.shape}")
            
        except Exception as e:
            self.fail(f"Error en extracción de región: {e}")
    
    def test_image_preprocessing(self):
        """Prueba el preprocesamiento de imágenes"""
        print("\n🧪 Test: Preprocesamiento de imágenes")
        try:
            from screen_capture.card_recognizer import CardRecognizer
            import cv2
            
            recognizer = CardRecognizer()
            
            # Crear imagen de prueba (gradiente)
            test_image = np.zeros((100, 100), dtype=np.uint8)
            for i in range(100):
                test_image[:, i] = i * 2
            
            # Aplicar preprocesamiento
            processed = recognizer._preprocess_image(test_image)
            
            self.assertIsNotNone(processed)
            self.assertEqual(processed.shape, test_image.shape)
            
            print(f"  ✅ Imagen preprocesada: {processed.shape}")
            
        except ImportError:
            print("  ⚠️  OpenCV no disponible - omitiendo prueba de preprocesamiento")
            self.skipTest("OpenCV no instalado")
        except Exception as e:
            self.fail(f"Error en preprocesamiento: {e}")
    
    def test_stealth_delay_simulation(self):
        """Prueba la simulación de delays de stealth"""
        print("\n🧪 Test: Delays de stealth")
        try:
            from screen_capture.card_recognizer import CardRecognizer
            import time
            
            recognizer = CardRecognizer(stealth_level="MEDIUM")
            
            # Medir tiempo antes y después del delay
            start_time = time.time()
            recognizer._apply_stealth_delay()
            elapsed_time = time.time() - start_time
            
            # El delay debería estar entre 0.15 y 0.30 segundos para MEDIUM
            self.assertGreaterEqual(elapsed_time, 0.14)  # Margen mínimo
            self.assertLessEqual(elapsed_time, 0.35)     # Margen máximo
            
            print(f"  ✅ Delay aplicado: {elapsed_time:.3f}s")
            
        except Exception as e:
            self.fail(f"Error en delay de stealth: {e}")
    
    def test_statistics_tracking(self):
        """Prueba el seguimiento de estadísticas"""
        print("\n🧪 Test: Seguimiento de estadísticas")
        from screen_capture.card_recognizer import CardRecognizer, Card
        
        recognizer = CardRecognizer()
        
        # Estadísticas iniciales
        initial_stats = recognizer.get_stats()
        self.assertEqual(initial_stats["total_recognitions"], 0)
        self.assertEqual(initial_stats["successful_recognitions"], 0)
        
        # Simular actualizaciones
        recognizer._update_stats(0.5, [
            Card('A', 'h', 0.95, (100, 200)),
            Card('K', 's', 0.92, (150, 200))
        ])
        
        recognizer._update_stats(0.3, [])
        
        # Verificar estadísticas actualizadas
        updated_stats = recognizer.get_stats()
        self.assertEqual(updated_stats["total_recognitions"], 2)
        self.assertGreater(updated_stats["avg_confidence"], 0)
        
        print(f"  ✅ Estadísticas iniciales: total={initial_stats['total_recognitions']}")
        print(f"  ✅ Estadísticas actualizadas: total={updated_stats['total_recognitions']}, avg_conf={updated_stats['avg_confidence']:.3f}")
    
    def test_validation_logic(self):
        """Prueba la lógica de validación"""
        print("\n🧪 Test: Lógica de validación")
        from screen_capture.card_recognizer import CardRecognizer, Card
        
        recognizer = CardRecognizer(stealth_level="MEDIUM")
        
        # Caso válido
        valid_cards = [
            Card('A', 'h', 0.95, (100, 200)),
            Card('K', 's', 0.92, (150, 200))
        ]
        is_valid = recognizer._validate_recognition(valid_cards)
        self.assertTrue(is_valid, "Cartas válidas deberían pasar validación")
        
        # Caso con confianza baja
        low_confidence_cards = [
            Card('A', 'h', 0.70, (100, 200)),  # Debajo del umbral MEDIUM (0.85)
            Card('K', 's', 0.92, (150, 200))
        ]
        is_valid_low = recognizer._validate_recognition(low_confidence_cards)
        self.assertFalse(is_valid_low, "Cartas con confianza baja deberían fallar")
        
        # Caso con duplicados
        duplicate_cards = [
            Card('A', 'h', 0.95, (100, 200)),
            Card('A', 'h', 0.95, (150, 200))  # Duplicada
        ]
        is_valid_dup = recognizer._validate_recognition(duplicate_cards)
        self.assertFalse(is_valid_dup, "Cartas duplicadas deberían fallar")
        
        print("  ✅ Lógica de validación probada (válidas, baja confianza, duplicadas)")
    
    def test_recognizer_integration(self):
        """Prueba de integración básica del reconocedor"""
        print("\n🧪 Test: Integración básica")
        try:
            from screen_capture.card_recognizer import CardRecognizer
            import cv2
            
            recognizer = CardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
            
            # Crear una imagen de prueba más realista
            test_image = np.zeros((400, 600, 3), dtype=np.uint8)
            
            # Dibujar "cartas" simples (rectángulos con texto)
            cv2.rectangle(test_image, (200, 250), (280, 370), (255, 255, 255), -1)  # Carta 1
            cv2.rectangle(test_image, (300, 250), (380, 370), (255, 255, 255), -1)  # Carta 2
            
            # Añadir "texto" de carta
            cv2.putText(test_image, "Ah", (210, 320), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(test_image, "Ks", (310, 320), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            # Configuración de región (hero cards)
            region_config = {
                "x1": 200/600,  # ~0.333
                "y1": 250/400,  # 0.625
                "x2": 380/600,  # ~0.633
                "y2": 370/400   # 0.925
            }
            
            # Intentar reconocimiento
            cards = recognizer.recognize_cards_in_region(test_image, region_config)
            
            # En este caso, es posible que no reconozca las cartas reales
            # pero debería manejar la imagen sin errores
            self.assertIsInstance(cards, list)
            
            print(f"  ✅ Proceso de reconocimiento completado")
            print(f"  ✅ Cartas detectadas: {len(cards)}")
            
            if cards:
                for card in cards:
                    print(f"    - {card} (confianza: {card.confidence:.3f})")
            
        except ImportError:
            print("  ⚠️  OpenCV no disponible - omitiendo prueba de integración")
            self.skipTest("OpenCV no instalado")
        except Exception as e:
            self.fail(f"Error en prueba de integración: {e}")

def run_all_tests():
    """Ejecutar todas las pruebas y mostrar resultados"""
    print("=" * 70)
    print("🎴 POKER COACH PRO - PRUEBAS COMPLETAS DE RECONOCIMIENTO")
    print("=" * 70)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCardRecognizer)
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2, descriptions=False)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Total de pruebas: {result.testsRun}")
    print(f"   Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print(f"   Fallos: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"     ❌ {test.id()}")
    
    if result.errors:
        print(f"   Errores: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"     ⚠️  {test.id()}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) 
                   / result.testsRun * 100) if result.testsRun > 0 else 0
    
    print(f"   Tasa de éxito: {success_rate:.1f}%")
    print("=" * 70)
    
    return result.wasSuccessful()

def quick_test():
    """Prueba rápida sin unittest para diagnóstico"""
    print("🧪 PRUEBA RÁPIDA - DIAGNÓSTICO")
    print("-" * 40)
    
    try:
        # Verificar imports
        print("1. Verificando imports...")
        from screen_capture.card_recognizer import CardRecognizer, Card
        print("   ✅ CardRecognizer importado")
        
        # Verificar creación
        print("2. Inicializando CardRecognizer...")
        recognizer = CardRecognizer()
        print(f"   ✅ Inicializado: {recognizer.platform}, {recognizer.stealth_level}")
        
        # Verificar templates
        stats = recognizer.get_stats()
        print(f"   ✅ Templates cargados: {stats['templates_loaded']}")
        
        # Verificar objeto Card
        print("3. Probando objeto Card...")
        test_card = Card('A', 'h', 0.95, (100, 200))
        print(f"   ✅ Card creado: {test_card}")
        
        print("\n✅ PRUEBA RÁPIDA EXITOSA")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar prueba rápida primero
    if quick_test():
        print("\n" + "=" * 70)
        print("✅ Prueba rápida exitosa. Ejecutando pruebas completas...")
        print("=" * 70)
        
        # Ejecutar todas las pruebas
        success = run_all_tests()
        
        # Salir con código apropiado
        sys.exit(0 if success else 1)
    else:
        print("\n❌ La prueba rápida falló. Revisa los errores arriba.")
        sys.exit(1)