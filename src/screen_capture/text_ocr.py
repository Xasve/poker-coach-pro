"""
OCR básico para textos
"""
class TextOCR:
    def __init__(self, platform: str = \"pokerstars\"):
        self.platform = platform
        print(f\"TextOCR inicializado para {platform}\")
    
    def extract_amounts(self, screenshot):
        \"\"\"Extraer montos (simulado)\"\"\"
        import random
        return {
            \"pot\": random.randint(100, 1000),
            \"stack\": random.randint(1000, 5000),
            \"to_call\": random.randint(0, 200),
            \"min_raise\": random.randint(50, 400),
            \"max_raise\": random.randint(500, 2000)
        }
