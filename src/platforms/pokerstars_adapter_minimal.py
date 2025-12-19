# pokerstars_adapter_minimal.py - Adaptador mínimo
class PokerStarsAdapter:
    def __init__(self, stealth_level=1):
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        print(f"🎴 Adaptador mínimo para {self.platform}")
    
    def capture_table(self):
        print("📸 Captura simulada")
        return None
    
    def detect_table(self, screenshot):
        print("🔍 Detección simulada: SIEMPRE VERDADERO")
        return True
    
    def recognize_hole_cards(self, screenshot):
        # Cartas simuladas para pruebas
        return [("A", "hearts", 0.95), ("K", "spades", 0.90)]
    
    def recognize_community_cards(self, screenshot):
        return []
    
    def get_table_info(self, screenshot):
        return {"platform": self.platform, "table_detected": True}
