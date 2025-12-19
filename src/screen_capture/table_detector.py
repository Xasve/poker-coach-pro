import cv2
import numpy as np

class TableDetector:
    def __init__(self):
        pass
    
    def detect(self, screenshot):
        # Simulación para pruebas
        height, width = screenshot.shape[:2]
        return {
            "region": (width//4, height//4, width//2, height//2),
            "confidence": 0.95,
            "type": "poker_table"
        }
