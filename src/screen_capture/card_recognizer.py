# src/screen_capture/card_recognizer.py
import cv2
import numpy as np
import os
import sys
from typing import List, Tuple, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .template_manager import CardTemplateManager
except ImportError:
    # Para uso independiente
    from template_manager import CardTemplateManager

class CardRecognizer:
    def __init__(self, platform="pokerstars", stealth_level=1):
        self.platform = platform
        self.stealth_level = stealth_level
        self.template_manager = CardTemplateManager(platform)
        
        # Umbrales de confianza
        self.confidence_threshold = 0.7
        self.min_template_size = (50, 70)  # Tamaño mínimo de template
        
        print(f"🃏 CardRecognizer inicializado para {platform}")
    
    def recognize_cards(self, image, card_positions=None):
        """
        Reconocer cartas en una imagen
        
        Args:
            image: Imagen de entrada (BGR)
            card_positions: Lista de (x, y, w, h) para cada carta (opcional)
            
        Returns:
            Lista de tuplas (value, suit, confidence)
        """
        if card_positions is None:
            # Detectar cartas automáticamente
            card_positions = self._detect_card_positions(image)
        
        recognized_cards = []
        
        for i, (x, y, w, h) in enumerate(card_positions):
            # Extraer región de la carta
            if y + h <= image.shape[0] and x + w <= image.shape[1]:
                card_region = image[y:y+h, x:x+w]
                
                # Reconocer esta carta
                value, suit, confidence = self._recognize_single_card(card_region)
                
                if confidence > self.confidence_threshold:
                    recognized_cards.append((value, suit, confidence))
                    print(f"  Carta {i+1}: {value}{suit} (confianza: {confidence:.2f})")
                else:
                    recognized_cards.append(("?", "?", confidence))
                    print(f"  Carta {i+1}: No reconocida (confianza: {confidence:.2f})")
        
        return recognized_cards
    
    def _detect_card_positions(self, image):
        """Detectar posiciones de cartas en la imagen"""
        # Para PokerStars, las cartas suelen estar en posiciones fijas
        # Esta es una implementación básica que asume posiciones estándar
        
        height, width = image.shape[:2]
        
        # Posiciones relativas estándar para mesa de 6 jugadores
        # (ajustar según necesidades)
        relative_positions = [
            (width // 2 - 180, height // 2 - 60, 71, 96),  # Carta 1 (comunitaria)
            (width // 2 - 90, height // 2 - 60, 71, 96),   # Carta 2
            (width // 2, height // 2 - 60, 71, 96),        # Carta 3
            (width // 2 + 90, height // 2 - 60, 71, 96),   # Carta 4
            (width // 2 + 180, height // 2 - 60, 71, 96),  # Carta 5
            
            # Cartas del jugador (abajo centro)
            (width // 2 - 110, height - 150, 71, 96),      # Hole card 1
            (width // 2 + 40, height - 150, 71, 96),       # Hole card 2
        ]
        
        return relative_positions
    
    def _recognize_single_card(self, card_image):
        """
        Reconocer una sola carta
        
        Returns:
            (value, suit, confidence)
        """
        # Preprocesar imagen
        processed = self._preprocess_card(card_image)
        
        # Valores y palos posibles
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        
        best_match = ("?", "?", 0.0)
        
        for value in values:
            for suit in suits:
                # Obtener template
                template = self.template_manager.get_template(value, suit)
                
                if template is None:
                    continue
                
                # Redimensionar template si es necesario
                if template.shape != card_image.shape[:2]:
                    template = cv2.resize(template, (card_image.shape[1], card_image.shape[0]))
                
                # Comparar usando template matching
                try:
                    # Convertir a escala de grises
                    card_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
                    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                    
                    # Template matching
                    result = cv2.matchTemplate(card_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(result)
                    
                    if max_val > best_match[2]:
                        best_match = (value, suit, max_val)
                        
                        # Si tenemos confianza muy alta, podemos parar
                        if max_val > 0.9:
                            return best_match
                
                except Exception as e:
                    # Error en matching, continuar con siguiente
                    continue
        
        return best_match
    
    def _preprocess_card(self, image):
        """Preprocesar imagen de carta"""
        # Convertir a HSV para mejor detección de colores
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Reducir ruido
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Mejorar contraste
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def set_confidence_threshold(self, threshold):
        """Establecer umbral de confianza"""
        self.confidence_threshold = max(0.1, min(0.99, threshold))
        print(f"📊 Umbral de confianza ajustado a: {self.confidence_threshold}")
    
    def get_diagnostic_info(self):
        """Obtener información de diagnóstico"""
        return {
            "platform": self.platform,
            "stealth_level": self.stealth_level,
            "confidence_threshold": self.confidence_threshold,
            "template_manager": "CardTemplateManager"
        }