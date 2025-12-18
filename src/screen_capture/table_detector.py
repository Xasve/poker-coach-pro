"""
Table Detector básico
"""
class TableDetector:
    def __init__(self, platform: str = \"pokerstars\"):
        self.platform = platform
        print(f\"TableDetector inicializado para {platform}\")
    
    def detect_table(self, screenshot):
        \"\"\"Detectar mesa (simulado)\"\"\"
        import random
        return {
            \"found\": random.random() > 0.3,
            \"position\": (100, 100, 800, 600),
            \"confidence\": random.uniform(0.7, 0.95)
        }
