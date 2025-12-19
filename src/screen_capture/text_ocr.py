import cv2
import numpy as np

class TextOCR:
    """OCR simple para poker"""
    
    def __init__(self):
        self.ocr_available = False
        
        # Intentar importar pytesseract
        try:
            import pytesseract
            self.ocr_available = True
            print("✅ Tesseract OCR disponible")
        except ImportError:
            print("⚠️  Tesseract no disponible, usando modo simple")
    
    def extract_text(self, image, region=None):
        """Extraer texto (simulación si no hay OCR)"""
        if not self.ocr_available:
            # Valores simulados para desarrollo
            return "$42.50" if np.random.random() > 0.5 else "$125.75"
        
        # Aquí iría el código real de OCR
        return "Texto extraído"
