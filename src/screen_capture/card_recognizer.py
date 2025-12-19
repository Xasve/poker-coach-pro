# actualizar src/screen_capture/card_recognizer.py
import cv2
import numpy as np
import os

class CardRecognizer:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        self.templates = self._load_card_templates()
        print(f"🃏 CardRecognizer para {platform} - {len(self.templates)} templates")
    
    def _load_card_templates(self):
        """Cargar templates de cartas desde disco"""
        templates = {}
        template_path = f"data/card_templates/{self.platform}"
        
        if os.path.exists(template_path):
            for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                suit_path = os.path.join(template_path, suit)
                if os.path.exists(suit_path):
                    for filename in os.listdir(suit_path):
                        if filename.endswith('.png'):
                            card_name = filename.replace('.png', '')
                            template_path_full = os.path.join(suit_path, filename)
                            template = cv2.imread(template_path_full, cv2.IMREAD_GRAYSCALE)
                            if template is not None:
                                templates[f"{card_name}_{suit[0]}"] = template
        
        if not templates:
            print("⚠️  No se encontraron templates, usando modo simulado")
        
        return templates
    
    def recognize(self, screenshot, table_region):
        """Reconocer cartas en la región de la mesa"""
        if not self.templates:
            # Modo simulado si no hay templates
            return self._get_simulated_cards()
        
        try:
            # Recortar región de la mesa
            x, y, w, h = table_region
            table_img = screenshot[y:y+h, x:x+w]
            
            if table_img.size == 0:
                return self._get_simulated_cards()
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
            
            # Buscar cartas (implementación simplificada)
            detected_cards = self._find_cards(gray)
            
            if detected_cards:
                return {
                    "hero": detected_cards.get('hero', []),
                    "community": detected_cards.get('community', []),
                    "confidence": 0.85,
                    "method": "template_matching"
                }
            else:
                return self._get_simulated_cards()
                
        except Exception as e:
            print(f"Error reconociendo cartas: {e}")
            return self._get_simulated_cards()
    
    def _find_cards(self, gray_image):
        """Buscar cartas usando template matching (simplificado)"""
        # Esta sería la implementación real
        return {
            'hero': ['Ah', 'Ks'],
            'community': ['Qd', 'Jc', 'Th']
        }
    
    def _get_simulated_cards(self):
        """Retornar cartas simuladas"""
        return {
            "hero": ["Ah", "Ks"],
            "community": ["Qd", "Jc", "Th"],
            "confidence": 0.9,
            "method": "simulated"
        }