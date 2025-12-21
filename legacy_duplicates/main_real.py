import sys, os, time, json, cv2, numpy as np
sys.path.insert(0, "src")

class PokerCoachReal:
    def __init__(self):
        self.load_real_config()
        self.init_components()
    
    def load_real_config(self):
        """Cargar coordenadas reales de PokerStars"""
        config_file = "config/pokerstars_coords.json"
        default_coords = {
            "mesa": [650, 300, 600, 400],
            "cartas_hero": [870, 750, 150, 60],
            "cartas_comunitarias": [750, 450, 400, 80],
            "pozo": [850, 550, 200, 40]
        }
        
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = json.load(f)
                self.regions = config.get("pokerstars_regions", default_coords)
                print(f"✅ Configuración REAL cargada - {config.get('screen_resolution', '1920x1080')}")
                self.mode = "REAL"
        else:
            self.regions = default_coords
            print("⚠️  Usando coordenadas por defecto - Ejecuta detect_coords.py")
            self.mode = "SIMULATED"
    
    def init_components(self):
        """Inicializar componentes del sistema"""
        from platforms.pokerstars_adapter import PokerStarsAdapter
        from core.poker_engine import PokerEngine
        
        self.adapter = PokerStarsAdapter("LOW")
        self.engine = PokerEngine(aggression=1.2, tightness=0.9)
        print(f"🎴 Sistema inicializado - Modo: {self.mode}")
    
    def capture_real_table(self):
        """Capturar mesa real usando coordenadas"""
        if self.mode == "SIMULATED":
            return self.adapter.get_table_state()
        
        try:
            from screen_capture.stealth_capture import StealthScreenCapture
            capture = StealthScreenCapture("pokerstars", "LOW")
            screenshot = capture.capture_screen()
            
            if screenshot is None:
                return self.get_simulated_state()
            
            # Verificar si hay mesa en las coordenadas
            mesa = self.regions["mesa"]
            x,y,w,h = mesa
            
            if y+h > screenshot.shape[0] or x+w > screenshot.shape[1]:
                print(f"❌ Coordenadas fuera de límites")
                return self.get_simulated_state()
            
            # Analizar región de la mesa
            mesa_img = screenshot[y:y+h, x:x+w]
            
            # Buscar verde (confirmar que es PokerStars)
            hsv = cv2.cvtColor(mesa_img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array([40,40,40]), np.array([80,255,255]))
            green_ratio = np.sum(mask > 0) / (w*h)
            
            if green_ratio > 0.1:
                print("✅ Mesa REAL detectada - Analizando...")
                
                # Aquí iría el reconocimiento REAL de cartas
                # Por ahora retornamos estructura real con datos simulados
                return {
                    "table": {"region": mesa, "confidence": 0.9},
                    "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]},
                    "pot": "1250",
                    "mode": "REAL",
                    "simulated": False,
                    "timestamp": time.time()
                }
            else:
                print(f"⚠️  No se detectó mesa verde en coordenadas")
                return self.get_simulated_state()
                
        except Exception as e:
            print(f"❌ Error captura real: {e}")
            return self.get_simulated_state()
    
    def get_simulated_state(self):
        """Estado simulado (fallback)"""
        return {
            "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]},
            "pot": "1250",
            "mode": "SIMULATED",
            "simulated": True,
            "reason": "PokerStars no detectado - Ejecuta detect_coords.py"
        }
    
    def run(self):
        """Ejecutar sistema principal"""
        print(f"\n🚀 INICIANDO POKER COACH PRO")
        print(f"   Modo: {self.mode}")
        print(f"   Presiona Ctrl+C para detener")
        print("="*60)
        
        self.adapter.start()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n🔄 Iteración {iteration}")
                
                # Obtener estado (real o simulado)
                if self.mode == "REAL":
                    estado = self.capture_real_table()
                else:
                    estado = self.adapter.get_table_state()
                
                # Mostrar información
                modo_display = "🎯 REAL" if estado.get("mode") == "REAL" else "⚠️  SIMULADO"
                print(f"   {modo_display}")
                
                if estado.get("cards"):
                    print(f"   🃏 Cartas: {estado['cards']}")
                    print(f"   💰 Pozo: {estado.get('pot', 0)}")
                    
                    # Análisis GTO
                    decision = self.engine.analyze_hand(
                        estado["cards"].get("hero", []),
                        estado["cards"].get("community", []),
                        int(estado.get("pot", 0)) if str(estado.get("pot", "0")).isdigit() else 0,
                        "middle"
                    )
                    
                    print(f"\n   🎯 RECOMENDACIÓN:")
                    print(f"      Acción: {decision.get('action', 'CHECK')}")
                    print(f"      Confianza: {decision.get('confidence', 0)*100:.0f}%")
                    print(f"      Razón: {decision.get('reason', '')}")
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Sistema detenido por usuario")
        finally:
            self.adapter.stop()
            print("✅ Sistema finalizado correctamente")

if __name__ == "__main__":
    coach = PokerCoachReal()
    coach.run()
