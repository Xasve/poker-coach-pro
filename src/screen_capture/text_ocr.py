# src/screen_capture/text_ocr.py
class TextOCR:
    def __init__(self):
        """Inicializador CORREGIDO: ahora no toma argumentos"""
        print("🔤 TextOCR inicializado (modo simulado)")
        # En una implementación real, aquí inicializaríamos pytesseract
    
    def extract_text(self, image, region=None):
        """Extraer texto de una región de la imagen (simulado)"""
        # Esta es una implementación simulada
        # En producción, usaríamos pytesseract o EasyOCR
        
        print("📝 Extrayendo texto (modo simulado)...")
        
        # Simular extracción de montos comunes
        simulated_texts = [
            "$0.50", "$1.00", "$2.00", "$5.00", 
            "$10.00", "$25.00", "$50.00", "$100.00"
        ]
        
        import random
        return random.choice(simulated_texts)
    
    def recognize_pot_size(self, image):
        """Reconocer el tamaño del bote (simulado)"""
        return self.extract_text(image)
    
    def recognize_stack_sizes(self, image):
        """Reconocer los stacks de los jugadores (simulado)"""
        # Simular stacks para 6 jugadores
        import random
        return [random.randint(50, 500) for _ in range(6)]