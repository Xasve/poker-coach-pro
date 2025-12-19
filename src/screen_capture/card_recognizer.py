import cv2
import numpy as np
import os

class CardRecognizer:
    def __init__(self, platform="pokerstars"):
        self.platform = platform
        print(f"CardRecognizer para {platform}")
    
    def recognize(self, screenshot, table_region):
        # Simulación para pruebas
        return {
            "hero": ["Ah", "Ks"],
            "community": ["Qd", "Jc", "Th"],
            "confidence": 0.9
        }
