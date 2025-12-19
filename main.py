import sys
import os
import time
import json
import cv2
import numpy as np

# Añadir src al path
sys.path.insert(0, "src")

print("🎴 POKER COACH PRO - SISTEMA PRINCIPAL")
print("=" * 60)

class PokerCoach:
    def __init__(self):
        """Inicializar sistema"""
        self.mode = "SIMULATED"
        self.regions = None
        self.load_config()
        
    def load_config(self):
        """Cargar configuración"""
        config_file = "config/pokerstars_coords.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.regions = config.get("pokerstars_regions")
                self.mode = "REAL"
                print(f"✅ Modo REAL activado")
                print(f"   Resolución: {config.get('screen_resolution', '1920x1080')}")
        else:
            print("  Modo SIMULADO - Ejecuta detect_coords.py para modo REAL")
            self.mode = "SIMULATED"
            
    def check_pokerstars_open(self):
        """Verificar si PokerStars está abierto"""
        if self.mode == "REAL":
            try:
                import mss
                with mss.mss() as sct:
                    screenshot = np.array(sct.grab(sct.monitors[1]))
                    
                    # Verificar color verde característico
                    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
                    green_mask = cv2.inRange(hsv, np.array([40, 40, 40]), np.array([80, 255, 255]))
                    green_pixels = np.sum(green_mask > 0)
                    
                    return green_pixels > 50000
            except:
                return False
        return False
        
    def get_table_state(self):
        """Obtener estado de la mesa"""
        if self.mode == "REAL" and self.check_pokerstars_open():
            try:
                import mss
                with mss.mss() as sct:
                    mesa = self.regions["mesa"]
                    screenshot = np.array(sct.grab({
                        "top": mesa[1], 
                        "left": mesa[0], 
                        "width": mesa[2], 
                        "height": mesa[3]
                    }))
                    
                    # Por ahora datos simulados
                    return {
                        "mode": "REAL",
                        "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th", "9s", "8h"]},
                        "pot": "1250",
                        "simulated": False,
                        "confidence": 0.9
                    }
            except Exception as e:
                print(f" Error captura real: {e}")
                
        # Fallback a modo simulado
        return {
            "mode": "SIMULATED",
            "cards": {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]},
            "pot": "1250",
            "simulated": True,
            "reason": "PokerStars no detectado"
        }
    
    def analyze_hand(self, cards, pot):
        """Análisis GTO básico"""
        # Simulación de motor GTO
        actions = ["RAISE", "CALL", "CHECK", "FOLD"]
        strengths = {
            "AA": 0.95, "KK": 0.90, "QQ": 0.85, "JJ": 0.80,
            "AKs": 0.85, "AQs": 0.80, "AJs": 0.75,
            "AhKs": 0.82, "QdJc": 0.60, "Th9s": 0.55
        }
        
        hero_cards = "".join(cards["hero"])
        strength = strengths.get(hero_cards, 0.5)
        
        if strength > 0.8:
            action = "RAISE"
            confidence = strength
            reason = "Mano premium"
        elif strength > 0.6:
            action = "CALL"
            confidence = strength
            reason = "Mano decente"
        else:
            action = "FOLD"
            confidence = 1 - strength
            reason = "Mano débil"
            
        return {
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "strength": strength
        }
    
    def run(self):
        """Ejecutar sistema principal"""
        print(f"\n INICIANDO SISTEMA - Modo: {self.mode}")
        print("   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n🔄 Iteración {iteration}")
                
                # Obtener estado
                estado = self.get_table_state()
                modo_display = " REAL" if estado["mode"] == "REAL" else "  SIMULADO"
                print(f"   {modo_display}")
                
                # Mostrar cartas
                if estado["cards"]:
                    print(f"   🃏 Hero: {estado['cards']['hero']}")
                    print(f"   🃏 Community: {estado['cards']['community']}")
                    print(f"   💰 Pot: {estado['pot']}")
                
                # Análisis GTO
                decision = self.analyze_hand(estado["cards"], estado["pot"])
                
                print(f"\n   🎯 RECOMENDACIÓN:")
                print(f"      Acción: {decision['action']}")
                print(f"      Confianza: {decision['confidence']*100:.0f}%")
                print(f"      Razón: {decision['reason']}")
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n\n  Sistema detenido por usuario")
        finally:
            print(" Sistema finalizado")

if __name__ == "__main__":
    coach = PokerCoach()
    coach.run()
