# src/screen_capture/card_recognizer.py (Versión Corregida)
import cv2
import numpy as np
import os
import sys

# Añadir el directorio padre al path para importaciones relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .template_manager import CardTemplateManager
except ImportError:
    # Si falla la importación relativa, intentar absoluta
    try:
        from template_manager import CardTemplateManager
    except ImportError:
        print("⚠️  No se pudo importar CardTemplateManager")
        # Crear una clase placeholder
        class CardTemplateManager:
            def __init__(self, platform="pokerstars"):
                self.platform = platform
            def get_template(self, value, suit):
                return None

# src/screen_capture/card_recognizer.py - Solo la parte corregida del constructor
class CardRecognizer:
    def __init__(self, platform="pokerstars", stealth_level=1):
        # 🔥 CORRECCIÓN: Asegurar que platform sea string
        self.platform = str(platform) if platform else "pokerstars"
        self.stealth_level = int(stealth_level) if stealth_level else 1
        
        # 🔥 CORRECCIÓN: Pasar string al template manager
        self.template_manager = CardTemplateManager(self.platform)
        
        # Umbrales de confianza
        self.confidence_threshold = 0.7
        
        print(f"🃏 CardRecognizer inicializado para {self.platform}")
    
    # ... (el resto del código permanece igual)
    
    def recognize_cards(self, image, card_positions=None):
        """
        Reconocer cartas en una imagen.
        
        Returns:
            list: Lista de tuplas (value, suit, confidence) o strings "valor+palo"
        """
        if image is None:
            return []
        
        if card_positions is None:
            # Usar posiciones por defecto si no se especifican
            card_positions = self._get_default_positions(image)
        
        recognized = []
        
        for i, (x, y, w, h) in enumerate(card_positions):
            # Asegurarse de que la región esté dentro de la imagen
            if (y + h <= image.shape[0] and x + w <= image.shape[1] and 
                w > 0 and h > 0):
                
                card_img = image[y:y+h, x:x+w]
                
                # Simular reconocimiento para pruebas
                value, suit, conf = self._simulate_recognition(card_img, i)
                
                if conf > self.confidence_threshold:
                    # Devolver como tupla O como string, pero consistentemente
                    recognized.append((value, suit, conf))
                else:
                    recognized.append(("?", "?", conf))
        
        return recognized
    
    def _get_default_positions(self, image):
        """Obtener posiciones por defecto para cartas"""
        height, width = image.shape[:2]
        
        # Posiciones relativas al centro (ajustables)
        return [
            (width//2 - 35, height//2 - 50, 71, 96),   # Carta 1
            (width//2 + 35, height//2 - 50, 71, 96),   # Carta 2
        ]
    
    def _simulate_recognition(self, card_image, index):
        """Simular reconocimiento para pruebas (remplazar con lógica real)"""
        # Valores y palos de ejemplo para simulación
        sample_cards = [
            ("A", "hearts", 0.95),
            ("K", "spades", 0.90),
            ("Q", "diamonds", 0.85),
            ("J", "clubs", 0.80),
            ("10", "hearts", 0.75)
        ]
        
        # Usar índice módulo longitud para no salirse de la lista
        idx = index % len(sample_cards)
        return sample_cards[idx]
    
    def set_confidence_threshold(self, threshold):
        """Establecer umbral de confianza"""
        self.confidence_threshold = max(0.1, min(0.99, threshold))
        print(f"📊 Umbral de confianza ajustado a: {self.confidence_threshold}")

# 🔥 CORRECCIÓN IMPORTANTE: NO exportar una clase 'Card' si no existe
# Solo exportar CardRecognizer