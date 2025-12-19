# src/platforms/pokerstars_adapter.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from screen_capture.stealth_capture import StealthScreenCapture
    from screen_capture.card_recognizer import CardRecognizer
    from screen_capture.table_detector import TableDetector
    from screen_capture.text_ocr import TextOCR
except ImportError as e:
    print(f"⚠️  Error importando módulos de screen_capture: {e}")
    # Definir clases placeholder para evitar errores de importación
    class StealthScreenCapture: pass
    class CardRecognizer: pass
    class TableDetector: pass
    class TextOCR: pass

class PokerStarsAdapter:
    def __init__(self, stealth_level=1):
        # 🔥 CORRECCIÓN CRÍTICA: Definir el atributo 'platform' PRIMERO
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        self.capture_delay = max(0.1, 0.5 / stealth_level)  # Más sigiloso = más lento
        
        print(f"🎴 Inicializando adaptador para {self.platform}...")
        
        # 🔥 CORRECCIÓN: Pasar los argumentos CORRECTOS a cada constructor
        # Basado en los errores, ajustamos:
        try:
            self.screen_capturer = StealthScreenCapture(stealth_level=stealth_level, platform=self.platform)
            self.card_recognizer = CardRecognizer(platform=self.platform)
            self.table_detector = TableDetector()  # ✅ Ahora sin argumentos
            self.text_ocr = TextOCR()  # ✅ Ahora sin argumentos
            
            print("✅ Todos los componentes del adaptador inicializados")
            
        except Exception as e:
            print(f"❌ Error inicializando componentes: {e}")
            # Asegurarse de que los atributos existan incluso si falla la inicialización
            self.screen_capturer = None
            self.card_recognizer = None
            self.table_detector = None
            self.text_ocr = None
    
    def capture_table(self):
        """Capturar la pantalla donde está la mesa"""
        if self.screen_capturer:
            return self.screen_capturer.capture_screen()
        return None
    
    def detect_table(self, screenshot):
        """Detectar si hay una mesa de poker en la captura"""
        if self.table_detector:
            return self.table_detector.detect(screenshot)
        return False
    
    def recognize_hole_cards(self, screenshot):
        """Reconocer las cartas propias (hole cards)"""
        if self.card_recognizer:
            # Posiciones aproximadas de las hole cards (ajustar según resolución)
            card_positions = [
                (960, 800, 71, 96),   # Hole card 1 (centro-abajo, izquierda)
                (1031, 800, 71, 96)   # Hole card 2 (centro-abajo, derecha)
            ]
            return self.card_recognizer.recognize_cards(screenshot, card_positions)
        return []
    
    def recognize_community_cards(self, screenshot):
        """Reconocer las cartas comunitarias"""
        if self.card_recognizer:
            # Posiciones aproximadas de las cartas comunitarias
            card_positions = [
                (750, 400, 71, 96),   # Flop 1
                (821, 400, 71, 96),   # Flop 2
                (892, 400, 71, 96),   # Flop 3
                (963, 400, 71, 96),   # Turn
                (1034, 400, 71, 96)   # River
            ]
            return self.card_recognizer.recognize_cards(screenshot, card_positions)
        return []
    
    def get_table_info(self, screenshot):
        """Obtener información general de la mesa"""
        return {
            "platform": self.platform,
            "stealth_level": self.stealth_level,
            "table_detected": self.detect_table(screenshot) if screenshot is not None else False,
            "timestamp": "2024-01-01 12:00:00"  # Placeholder
        }