# src/screen_capture/card_recognizer.py - Versión mejorada para reconocimiento real
import cv2
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .template_manager import CardTemplateManager
except ImportError:
    from template_manager import CardTemplateManager

class CardRecognizer:
    def __init__(self, platform="pokerstars", stealth_level=1):
        self.platform = platform
        self.stealth_level = stealth_level
        
        # Inicializar template manager
        self.template_manager = CardTemplateManager(platform)
        
        # Umbral de confianza más realista
        self.confidence_threshold = 0.65
        
        # Posiciones específicas para PokerStars 1920x1080
        self.card_positions = self._load_card_positions()
        
        print(f"🃏 CardRecognizer inicializado para {platform} (modo REAL)")
    
    def _load_card_positions(self):
        """Cargar posiciones de cartas para 1920x1080"""
        return {
            "hole_cards": [
                (850, 930, 71, 96),   # Hole card 1
                (1000, 930, 71, 96)   # Hole card 2
            ],
            "community_cards": [
                (780, 480, 71, 96),   # Flop 1
                (870, 480, 71, 96),   # Flop 2
                (960, 480, 71, 96),   # Flop 3
                (1050, 480, 71, 96),  # Turn
                (1140, 480, 71, 96)   # River
            ]
        }
    
    def recognize_cards(self, image, card_type="hole_cards"):
        """
        Reconocer cartas REALES usando template matching
        """
        if image is None:
            return []
        
        positions = self.card_positions.get(card_type, [])
        recognized = []
        
        for i, (x, y, w, h) in enumerate(positions):
            # Verificar que la región esté dentro de la imagen
            if (y + h <= image.shape[0] and x + w <= image.shape[1] and 
                w > 0 and h > 0):
                
                # Extraer región de la carta
                card_region = image[y:y+h, x:x+w]
                
                if card_region.size == 0:
                    continue
                
                # Intentar reconocer la carta
                result = self._recognize_single_card(card_region)
                
                if result:
                    value, suit, confidence = result
                    if confidence > self.confidence_threshold:
                        recognized.append((value, suit, confidence))
                    else:
                        recognized.append(("?", "?", confidence))
                else:
                    recognized.append(("?", "?", 0.0))
        
        return recognized
    
    def _recognize_single_card(self, card_image):
        """
        Reconocer una sola carta usando template matching real
        """
        try:
            # Preprocesar imagen de carta
            processed = self._preprocess_card(card_image)
            
            # Valores y palos a probar
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            
            best_match = None
            best_confidence = 0
            
            for value in values:
                for suit in suits:
                    # Obtener template
                    template = self.template_manager.get_template(value, suit)
                    
                    if template is None:
                        continue
                    
                    # Redimensionar template si es necesario
                    if template.shape[:2] != processed.shape[:2]:
                        template = cv2.resize(template, (processed.shape[1], processed.shape[0]))
                    
                    # Convertir a escala de grises
                    card_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    
                    # Template matching
                    result = cv2.matchTemplate(card_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    
                    if max_val > best_confidence:
                        best_confidence = max_val
                        best_match = (value, suit, max_val)
            
            return best_match if best_confidence > 0.3 else None
            
        except Exception as e:
            print(f"⚠️  Error en reconocimiento de carta: {e}")
            return None
    
    def _preprocess_card(self, image):
        """Preprocesar imagen de carta para mejor reconocimiento"""
        try:
            # Mejorar contraste
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge((l, a, b))
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Reducir ruido
            denoised = cv2.medianBlur(enhanced, 3)
            
            return denoised
        except:
            return image
    
    def set_positions(self, positions_dict):
        """Establecer nuevas posiciones de cartas"""
        self.card_positions.update(positions_dict)
        print("✅ Posiciones de cartas actualizadas")