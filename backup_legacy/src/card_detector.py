# card_detector.py - Sistema avanzado de detección de cartas
import cv2
import numpy as np
import os
import json
from datetime import datetime
from pathlib import Path

class CardDetector:
    """Sistema avanzado para detectar y reconocer cartas"""
    
    def __init__(self, templates_path="data/card_templates/pokerstars_real"):
        self.templates_path = templates_path
        self.templates = self.load_templates()
        self.card_positions = []
        
    def load_templates(self):
        """Cargar templates de cartas existentes"""
        templates = {}
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        
        for suit in suits:
            suit_path = os.path.join(self.templates_path, suit)
            if os.path.exists(suit_path):
                for file in os.listdir(suit_path):
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        card_name = file.split('.')[0]
                        template_path = os.path.join(suit_path, file)
                        img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            templates[f"{card_name}_{suit}"] = img
        
        print(f"📚 Templates cargados: {len(templates)}")
        return templates
    
    def detect_cards_in_region(self, image, region):
        """Detectar cartas en una región específica"""
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        
        if roi.size == 0:
            return []
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo
        binary = cv2.adaptiveThreshold(gray, 255, 
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 11, 2)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
        
        cards = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 5000:  # Tamaño esperado de cartas
                x_card, y_card, w_card, h_card = cv2.boundingRect(contour)
                
                # Ajustar coordenadas globales
                card_global = (x + x_card, y + y_card, w_card, h_card)
                
                # Extraer la carta
                card_img = roi[y_card:y_card+h_card, x_card:x_card+w_card]
                
                # Reconocer carta
                card_info = self.recognize_card(card_img)
                
                if card_info:
                    cards.append({
                        "position": card_global,
                        "image": card_img,
                        "info": card_info,
                        "confidence": card_info["confidence"]
                    })
        
        return cards
    
    def recognize_card(self, card_image):
        """Reconocer una carta individual usando template matching"""
        if card_image.size == 0:
            return None
        
        # Preprocesar imagen de la carta
        gray_card = cv2.cvtColor(card_image, cv2.COLOR_BGR2GRAY)
        gray_card = cv2.resize(gray_card, (70, 95))  # Tamaño estándar
        
        best_match = None
        best_score = 0
        
        for card_name, template in self.templates.items():
            # Redimensionar template si es necesario
            template_resized = cv2.resize(template, (70, 95))
            
            # Template matching
            result = cv2.matchTemplate(gray_card, template_resized, 
                                    cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val > best_score:
                best_score = max_val
                best_match = card_name
        
        if best_match and best_score > 0.7:  # Umbral de confianza
            # Parsear nombre de la carta
            parts = best_match.split('_')
            if len(parts) >= 2:
                value = parts[0]
                suit = parts[1]
                
                return {
                    "value": value,
                    "suit": suit,
                    "confidence": float(best_score),
                    "notation": f"{value[0]}{suit[0]}"  # Ej: Ah para Ace of hearts
                }
        
        return None
    
    def auto_capture_unknown_cards(self, image, regions):
        """Capturar automáticamente cartas no reconocidas"""
        unknown_cards = []
        
        for region in regions:
            cards = self.detect_cards_in_region(image, region)
            
            for card in cards:
                if card["confidence"] < 0.7:  # Baja confianza = carta desconocida
                    unknown_cards.append(card)
        
        return unknown_cards
    
    def save_unknown_card(self, card_image, card_position):
        """Guardar carta desconocida para clasificación posterior"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"unknown_card_{timestamp}.png"
        
        save_path = os.path.join(self.templates_path, "uncategorized", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        cv2.imwrite(save_path, card_image)
        print(f" Carta desconocida guardada: {save_path}")
        
        # Guardar metadatos
        metadata = {
            "filename": filename,
            "timestamp": timestamp,
            "position": card_position,
            "size": card_image.shape[:2]
        }
        
        metadata_path = save_path.replace('.png', '.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return save_path

# Exportar para uso en otros módulos
if __name__ == "__main__":
    detector = CardDetector()
    print("✅ Sistema de detección de cartas inicializado")
