# En src/screen_capture/stealth_capture.py
class StealthScreenCapture:
    def __init__(self, stealth_level=1, platform="pokerstars"):
        """Constructor con parámetros opcionales"""
        self.stealth_level = max(1, min(3, int(stealth_level)))
        self.platform = str(platform) if platform else "pokerstars"
        self.capture_method = None
        self.delay_between_captures = self._calculate_delay()
        self._initialize_capture_method()
        
    def _calculate_delay(self):
        """Calcula delay basado en nivel de stealth"""
        delays = {1: 0.3, 2: 0.7, 3: 1.5}
        return delays.get(self.stealth_level, 0.5)
        
    def _initialize_capture_method(self):
        """Inicializa método de captura"""
        try:
            import mss
            self.capture_method = mss.mss()
            print(f"✅ Captura stealth nivel {self.stealth_level} para {self.platform}")
        except Exception as e:
            print(f"⚠️ Error inicializando MSS: {e}")
            self.capture_method = None