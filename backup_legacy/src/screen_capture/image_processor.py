"""
image_processor.py - Procesamiento de imágenes para poker
"""

import cv2
import numpy as np
import logging
from typing import Tuple, Optional

class ImageProcessor:
    """Procesador de imágenes para análisis de poker"""
    
    def __init__(self, platform: str = "ggpoker"):
        self.platform = platform
        self.logger = logging.getLogger(__name__)
        
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)
        
        self.logger.info(f"ImageProcessor inicializado para {platform}")
    
    def preprocess_table_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocesar imagen de la mesa"""
        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Mejorar contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        return enhanced
    
    def detect_edges(self, image: np.ndarray) -> np.ndarray:
        """Detectar bordes en la imagen"""
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Detectar bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        return edges
    
    def find_contours(self, image: np.ndarray):
        """Encontrar contornos en la imagen"""
        # Encontrar contornos
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        return contours
    
    def crop_region(self, image: np.ndarray, 
                   x1: float, y1: float, 
                   x2: float, y2: float) -> np.ndarray:
        """Recortar región de la imagen (coordenadas relativas 0-1)"""
        h, w = image.shape[:2]
        
        # Convertir a píxeles absolutos
        abs_x1 = int(w * x1)
        abs_y1 = int(h * y1)
        abs_x2 = int(w * x2)
        abs_y2 = int(h * y2)
        
        # Asegurar límites válidos
        abs_x1 = max(0, min(abs_x1, w))
        abs_x2 = max(0, min(abs_x2, w))
        abs_y1 = max(0, min(abs_y1, h))
        abs_y2 = max(0, min(abs_y2, h))
        
        # Recortar
        cropped = image[abs_y1:abs_y2, abs_x1:abs_x2]
        
        return cropped
    
    def resize_image(self, image: np.ndarray, 
                    width: int = None, height: int = None) -> np.ndarray:
        """Redimensionar imagen manteniendo aspecto"""
        if width is None and height is None:
            return image
        
        h, w = image.shape[:2]
        
        if width is None:
            ratio = height / h
            width = int(w * ratio)
        elif height is None:
            ratio = width / w
            height = int(h * ratio)
        
        return cv2.resize(image, (width, height))

# Exportar la clase
__all__ = ['ImageProcessor']