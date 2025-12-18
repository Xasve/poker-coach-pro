"""
image_utils.py - Utilidades para procesamiento de imágenes
"""

import cv2
import numpy as np
import os
from typing import Tuple, Optional, List

class ImageUtils:
    """Clase de utilidades para procesamiento de imágenes"""
    
    @staticmethod
    def resize_image(image: np.ndarray, width: int = None, 
                    height: int = None) -> np.ndarray:
        """
        Redimensionar imagen manteniendo aspecto
        
        Args:
            image: Imagen a redimensionar
            width: Ancho deseado
            height: Alto deseado
            
        Returns:
            Imagen redimensionada
        """
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
    
    @staticmethod
    def crop_relative(image: np.ndarray, x1: float, y1: float, 
                     x2: float, y2: float) -> np.ndarray:
        """
        Recortar imagen usando coordenadas relativas (0-1)
        
        Args:
            image: Imagen original
            x1, y1: Esquina superior izquierda (relativa)
            x2, y2: Esquina inferior derecha (relativa)
            
        Returns:
            Imagen recortada
        """
        h, w = image.shape[:2]
        abs_x1 = int(w * x1)
        abs_y1 = int(h * y1)
        abs_x2 = int(w * x2)
        abs_y2 = int(h * y2)
        
        # Asegurar límites válidos
        abs_x1 = max(0, min(abs_x1, w))
        abs_x2 = max(0, min(abs_x2, w))
        abs_y1 = max(0, min(abs_y1, h))
        abs_y2 = max(0, min(abs_y2, h))
        
        return image[abs_y1:abs_y2, abs_x1:abs_x2]
    
    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Convertir imagen a escala de grises
        
        Args:
            image: Imagen en color
            
        Returns:
            Imagen en escala de grises
        """
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """
        Mejorar contraste de la imagen
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Imagen con contraste mejorado
        """
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(image) if len(image.shape) == 2 else clahe.apply(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    
    @staticmethod
    def find_edges(image: np.ndarray) -> np.ndarray:
        """
        Encontrar bordes usando Canny
        
        Args:
            image: Imagen de entrada
            
        Returns:
            Mapa de bordes
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Aplicar desenfoque gaussiano
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detectar bordes
        edges = cv2.Canny(blurred, 50, 150)
        return edges
    
    @staticmethod
    def save_image(image: np.ndarray, path: str, 
                  create_dir: bool = True) -> bool:
        """
        Guardar imagen en disco
        
        Args:
            image: Imagen a guardar
            path: Ruta donde guardar
            create_dir: Crear directorio si no existe
            
        Returns:
            True si se guardó correctamente
        """
        if create_dir:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        
        try:
            cv2.imwrite(path, image)
            return True
        except Exception as e:
            print(f"Error guardando imagen: {e}")
            return False
    
    @staticmethod
    def show_image(image: np.ndarray, title: str = "Image", 
                  wait_time: int = 0):
        """
        Mostrar imagen (solo para debugging)
        
        Args:
            image: Imagen a mostrar
            title: Título de la ventana
            wait_time: Tiempo de espera en ms (0=espera indefinida)
        """
        cv2.imshow(title, image)
        cv2.waitKey(wait_time)
        if wait_time == 0:
            cv2.destroyAllWindows()
    
    @staticmethod
    def draw_rectangles(image: np.ndarray, rectangles: List[Tuple], 
                       color: Tuple = (0, 255, 0), thickness: int = 2) -> np.ndarray:
        """
        Dibujar rectángulos en una imagen
        
        Args:
            image: Imagen original
            rectangles: Lista de rectángulos (x, y, w, h)
            color: Color BGR
            thickness: Grosor de línea
            
        Returns:
            Imagen con rectángulos dibujados
        """
        result = image.copy()
        for rect in rectangles:
            x, y, w, h = rect
            cv2.rectangle(result, (x, y), (x + w, y + h), color, thickness)
        return result