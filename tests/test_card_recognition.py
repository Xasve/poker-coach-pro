"""
test_card_recognition.py - Pruebas para el reconocedor de cartas
"""

import unittest
import cv2
import numpy as np
import tempfile
import os
from pathlib import Path

# Importar módulos a testear
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.screen_capture.card_recognizer import CardRecognizer, Card
from src.utils.image_utils import ImageUtils

class TestCardRecognizer(unittest.TestCase):
    """Clase de pruebas para CardRecognizer"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.recognizer = CardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
        self.test_dir = tempfile.mkdtemp()
        
        # Crear templates de prueba simples
        self._create_test_templates()
    
    def _create_test_templates(self):
        """Crear templates de prueba simples"""
        template_dir = Path("data/card_templates")
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear algunas cartas de prueba
        ranks = ['A', 'K', 'Q']
        suits = ['s', 'h']
        
        for rank in ranks:
            for suit in suits:
                # Crear imagen simple de carta
                img = np.zeros((120, 80), dtype=np.uint8)
                
                # Dibujar rectángulo blanco
                cv2.rectangle(img, (5, 5), (75, 115), 255, 2)
                
                # Añadir texto simple
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, f"{rank}{suit}", (10, 60), 
                           font, 0.7, 255, 2)
                
                # Guardar template
                template_path = template_dir / f"{rank}{suit}.png"
                cv2.imwrite(str(template_path), img)
    
    def test_card_initialization(self):
        """Prueba de inicialización de objeto Card"""
        card = Card(rank='A', suit='h', confidence=0.95, position=(100, 200))
        
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, 'h')
        self.assertEqual(card.confidence, 0.95)
        self.assertEqual(card.position, (100, 200))
        self.assertEqual(str(card), 'Ah')
        self.assertEqual(card.to_poker_format(), 'Ah')
    
    def test_recognizer_initialization(self):
        """Prueba de inicialización de CardRecognizer"""
        self.assertEqual(self.recognizer.platform, "ggpoker")
        self.assertEqual(self.recognizer.stealth_level, "MINIMUM")
        self.assertIn("MINIMUM", self.recognizer.confidence_thresholds)
        self.assertIsInstance(self.recognizer.templates, dict)
    
    def test_preprocess_image(self):
        """Prueba de preprocesamiento de imagen"""
        # Crear imagen de prueba
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Llamar a método privado (usaremos reflexión para pruebas)
        processed = self.recognizer._preprocess_image(test_image)
        
        # Verificar resultados
        self.assertIsInstance(processed, np.ndarray)
        self.assertEqual(len(processed.shape), 2)  # Debe ser grayscale
        self.assertEqual(processed.dtype, np.uint8)
    
    def test_extract_roi_valid(self):
        """Prueba de extracción de región válida"""
        # Crear imagen de prueba
        test_image = np.zeros((200, 300, 3), dtype=np.uint8)
        
        # Configuración de región
        region_config = {
            'x1': 0.2,
            'y1': 0.3,
            'x2': 0.8,
            'y2': 0.7
        }
        
        # Extraer ROI
        roi = self.recognizer._extract_roi(test_image, region_config)
        
        # Verificar
        self.assertIsNotNone(roi)
        self.assertEqual(roi.shape[0], 80)  # 200 * (0.7 - 0.3) = 80
        self.assertEqual(roi.shape[1], 180)  # 300 * (0.8 - 0.2) = 180
    
    def test_extract_roi_invalid(self):
        """Prueba de extracción de región inválida"""
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Región inválida (x2 <= x1)
        region_config = {
            'x1': 0.8,
            'y1': 0.3,
            'x2': 0.2,
            'y2': 0.7
        }
        
        roi = self.recognizer._extract_roi(test_image, region_config)
        self.assertIsNone(roi)
    
    def test_validate_recognition_valid(self):
        """Prueba de validación con cartas válidas"""
        cards = [
            Card('A', 'h', 0.95, (100, 200)),
            Card('K', 's', 0.90, (150, 200))
        ]
        
        is_valid = self.recognizer._validate_recognition(cards)
        self.assertTrue(is_valid)
    
    def test_validate_recognition_low_confidence(self):
        """Prueba de validación con confianza baja"""
        cards = [
            Card('A', 'h', 0.70, (100, 200)),  # Confianza muy baja
            Card('K', 's', 0.90, (150, 200))
        ]
        
        is_valid = self.recognizer._validate_recognition(cards)
        self.assertFalse(is_valid)
    
    def test_validate_recognition_duplicates(self):
        """Prueba de validación con cartas duplicadas"""
        cards = [
            Card('A', 'h', 0.95, (100, 200)),
            Card('A', 'h', 0.95, (150, 200))  # Duplicada
        ]
        
        is_valid = self.recognizer._validate_recognition(cards)
        self.assertFalse(is_valid)
    
    def test_stats_tracking(self):
        """Prueba de seguimiento de estadísticas"""
        # Verificar estadísticas iniciales
        initial_stats = self.recognizer.get_stats()
        self.assertEqual(initial_stats['total_recognitions'], 0)
        self.assertEqual(initial_stats['successful_recognitions'], 0)
        
        # Simular algunas operaciones
        self.recognizer._update_stats(0.5, [
            Card('A', 'h', 0.95, (100, 200)),
            Card('K', 's', 0.92, (150, 200))
        ])
        
        # Verificar estadísticas actualizadas
        updated_stats = self.recognizer.get_stats()
        self.assertEqual(updated_stats['total_recognitions'], 1)
        self.assertGreater(updated_stats['avg_confidence'], 0)
        
        # Reiniciar estadísticas
        self.recognizer.reset_stats()
        reset_stats = self.recognizer.get_stats()
        self.assertEqual(reset_stats['total_recognitions'], 0)
    
    def test_image_utils_resize(self):
        """Prueba de utilidad de redimensionamiento"""
        # Crear imagen de prueba
        test_image = np.zeros((200, 300, 3), dtype=np.uint8)
        
        # Redimensionar
        resized = ImageUtils.resize_image(test_image, width=150)
        
        # Verificar
        self.assertEqual(resized.shape[1], 150)  # Ancho correcto
        self.assertEqual(resized.shape[0], 100)  # Alto proporcional
    
    def test_image_utils_crop(self):
        """Prueba de utilidad de recorte"""
        # Crear imagen de prueba con patrón
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = 255  # Cuadrado blanco en el centro
        
        # Recortar centro
        cropped = ImageUtils.crop_relative(test_image, 0.25, 0.25, 0.75, 0.75)
        
        # Verificar
        self.assertEqual(cropped.shape[0], 50)
        self.assertEqual(cropped.shape[1], 50)
        self.assertTrue(np.all(cropped == 255))  # Todo blanco
    
    def test_stealth_delay_applied(self):
        """Prueba que se aplique el delay de stealth"""
        # Este test verificaría que el delay se aplica
        # En práctica, usaríamos mocking para time.sleep
        pass
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        # Eliminar templates de prueba
        template_dir = Path("data/card_templates")
        if template_dir.exists():
            for file in template_dir.glob("*.png"):
                file.unlink()
            template_dir.rmdir()
        
        # Eliminar directorio temporal
        import shutil
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()