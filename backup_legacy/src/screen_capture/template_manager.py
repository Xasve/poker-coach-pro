# src/screen_capture/template_manager.py
"""
Manejador de templates de cartas con sistema de fallback
"""
import cv2
import numpy as np
import os
import json

class CardTemplateManager:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        self.template_dir = f"data/card_templates/{platform}"
        self.fallback_dir = "data/card_templates/fallback"
        self.fallback_templates = {}
        
        # Crear directorio de fallback si no existe
        os.makedirs(self.fallback_dir, exist_ok=True)
        
        # Inicializar templates
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Inicializar templates, crear fallbacks si no existen"""
        print(f"🃏 Inicializando templates para {self.platform}...")
        
        # Verificar si hay templates reales
        has_real_templates = self._check_real_templates()
        
        if not has_real_templates:
            print("⚠️  No se encontraron templates reales, creando sistema de fallback...")
            self._create_fallback_templates()
    
    def _check_real_templates(self):
        """Verificar si existen templates reales"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Verificar al menos un template por palo
        for suit in suits:
            suit_dir = os.path.join(self.template_dir, suit)
            if os.path.exists(suit_dir):
                # Contar templates en este palo
                templates = [f for f in os.listdir(suit_dir) if f.endswith('.png')]
                if len(templates) >= 13:  # Todos los valores
                    return True
        
        return False
    
    def _create_fallback_templates(self):
        """Crear templates de fallback básicos"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        print(f"🎨 Generando {len(values) * len(suits)} templates de fallback...")
        
        for suit in suits:
            for value in values:
                # Crear imagen de template
                img = np.zeros((96, 71, 3), dtype=np.uint8)  # Tamaño estándar
                
                # Color de fondo según palo
                if suit in ['hearts', 'diamonds']:
                    bg_color = (50, 50, 100)  # Azul oscuro para rojos
                    text_color = (0, 0, 255)   # Texto rojo
                else:
                    bg_color = (100, 50, 50)   # Rojo oscuro para negros
                    text_color = (255, 255, 255) # Texto blanco
                
                img[:] = bg_color
                
                # Añadir borde
                cv2.rectangle(img, (0, 0), (70, 95), (200, 200, 200), 2)
                
                # Añadir texto del valor
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(value, font, 0.7, 2)[0]
                text_x = (71 - text_size[0]) // 2
                text_y = 35
                cv2.putText(img, value, (text_x, text_y), font, 0.7, text_color, 2)
                
                # Añadir símbolo del palo
                suit_symbol = self._get_suit_symbol(suit)
                suit_size = cv2.getTextSize(suit_symbol, font, 0.5, 2)[0]
                suit_x = (71 - suit_size[0]) // 2
                suit_y = 65
                cv2.putText(img, suit_symbol, (suit_x, suit_y), font, 0.5, text_color, 2)
                
                # Guardar template
                template_key = f"{value}_{suit}"
                template_path = os.path.join(self.fallback_dir, f"{template_key}.png")
                cv2.imwrite(template_path, img)
                
                self.fallback_templates[template_key] = img
        
        print(f"✅ Templates de fallback creados en: {self.fallback_dir}")
        
        # Guardar metadata
        metadata = {
            "platform": self.platform,
            "template_count": len(self.fallback_templates),
            "type": "fallback",
            "created": "auto-generated"
        }
        
        with open(os.path.join(self.fallback_dir, "metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _get_suit_symbol(self, suit):
        """Obtener símbolo Unicode para el palo"""
        symbols = {
            'hearts': '♥',
            'diamonds': '♦',
            'clubs': '♣',
            'spades': '♠'
        }
        return symbols.get(suit, suit[0].upper())
    
    def get_template(self, value, suit):
        """Obtener template de carta"""
        template_key = f"{value}_{suit}"
        
        # 1. Intentar con templates reales
        real_path = os.path.join(self.template_dir, suit, f"{value}.png")
        if os.path.exists(real_path):
            return cv2.imread(real_path)
        
        # 2. Intentar con templates reales en directorio principal
        real_path2 = os.path.join(self.template_dir, f"{value}_{suit}.png")
        if os.path.exists(real_path2):
            return cv2.imread(real_path2)
        
        # 3. Usar fallback
        if template_key in self.fallback_templates:
            return self.fallback_templates[template_key].copy()
        
        # 4. Fallback alternativo
        fallback_path = os.path.join(self.fallback_dir, f"{template_key}.png")
        if os.path.exists(fallback_path):
            return cv2.imread(fallback_path)
        
        # 5. Crear template simple en tiempo real
        print(f"⚠️  Creando template dinámico para {value}{suit[0].upper()}")
        return self._create_dynamic_template(value, suit)
    
    def _create_dynamic_template(self, value, suit):
        """Crear template dinámico en tiempo real"""
        img = np.zeros((96, 71, 3), dtype=np.uint8)
        
        # Color según palo
        if suit in ['hearts', 'diamonds']:
            color = (0, 0, 255)  # Rojo
            bg_color = (30, 30, 60)  # Fondo azul oscuro
        else:
            color = (255, 255, 255)  # Blanco
            bg_color = (60, 30, 30)  # Fondo rojo oscuro
        
        img[:] = bg_color
        
        # Texto simple
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"{value}{suit[0].upper()}"
        text_size = cv2.getTextSize(text, font, 0.5, 1)[0]
        text_x = (71 - text_size[0]) // 2
        text_y = 48
        cv2.putText(img, text, (text_x, text_y), font, 0.5, color, 1)
        
        return img
    
    def save_custom_template(self, image, value, suit):
        """Guardar una imagen como template personalizado"""
        suit_dir = os.path.join(self.template_dir, suit)
        os.makedirs(suit_dir, exist_ok=True)
        
        template_path = os.path.join(suit_dir, f"{value}.png")
        cv2.imwrite(template_path, image)
        print(f"💾 Template guardado: {template_path}")
        
        return template_path