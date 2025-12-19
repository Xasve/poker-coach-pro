# pokerstars_adapter.py - MÉTODO AÑADIDO
# ... (código existente)

class PokerStarsAdapter:
    def __init__(self, stealth_level="MEDIUM"):
        self.platform = "pokerstars"
        self.stealth_level = stealth_level
        
        print(f"🔄 Inicializando PokerStarsAdapter con nivel stealth: {stealth_level}")
        
        # Inicializar componentes
        self.capture_system = StealthScreenCapture(self.platform, self.stealth_level)
        self.table_detector = TableDetector()
        self.card_recognizer = CardRecognizer(platform=self.platform)
        self.text_ocr = TextOCR()
        
        print("✅ PokerStarsAdapter inicializado correctamente")
    
    def start(self):
        """Iniciar el sistema de captura"""
        print("🎴 Iniciando captura de PokerStars...")
        return self.capture_system.start_capture()
    
    def stop(self):
        """Detener el sistema de captura"""
        print("⏹️ Deteniendo captura...")
        return self.capture_system.stop_capture()
    
    def get_table_state(self):
        """Obtener el estado completo de la mesa (MÉTODO NUEVO)"""
        try:
            # 1. Capturar pantalla
            screenshot = self.capture_system.capture_screen()
            
            if screenshot is None:
                print("⚠️  No se pudo capturar pantalla")
                return None
            
            # 2. Detectar mesa
            print("🔍 Detectando mesa...")
            table_info = self.table_detector.detect(screenshot)
            
            if not table_info:
                print("⚠️  No se detectó mesa de poker")
                # Modo simulado para pruebas
                return self._get_simulated_state()
            
            print(f"✅ Mesa detectada en: {table_info.get('region')}")
            
            # 3. Reconocer cartas
            print("🃏 Reconociendo cartas...")
            cards_info = self.card_recognizer.recognize(screenshot, table_info.get("region", (0, 0, 1920, 1080)))
            
            # 4. Extraer texto (pozo, apuestas)
            print("🔤 Extrayendo texto...")
            pot_region = (table_info["region"][0] + 100, table_info["region"][1] + 50, 200, 40)
            pot_text = self.text_ocr.extract_text(screenshot, pot_region)
            
            # 5. Preparar estado
            state = {
                "table": table_info,
                "cards": cards_info,
                "pot": pot_text,
                "platform": self.platform,
                "timestamp": time.time()
            }
            
            print(f"✅ Estado obtenido: {len(state)} elementos")
            return state
            
        except Exception as e:
            print(f"❌ Error obteniendo estado: {e}")
            # Retornar estado simulado en caso de error
            return self._get_simulated_state()
    
    def _get_simulated_state(self):
        """Retornar estado simulado para pruebas"""
        return {
            "simulated": True,
            "cards": {
                "hero": ["Ah", "Ks"],
                "community": ["Qd", "Jc", "Th", "9s", "2d"]
            },
            "pot": "1250",
            "players": 6,
            "position": "middle",
            "platform": self.platform,
            "timestamp": time.time()
        }
    
    def analyze_table_state(self):
        """Alias para compatibilidad"""
        return self.get_table_state()

# Añadir import time al inicio del archivo si no está
import time