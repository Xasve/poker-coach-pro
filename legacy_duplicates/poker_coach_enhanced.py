import sys
import os
import time
import json
import cv2
import numpy as np
from datetime import datetime

# Añadir src al path
sys.path.insert(0, "src")

class EnhancedPokerCoach:
    def __init__(self):
        self.config = self.load_config()
        self.templates_loaded = False
        self.card_templates = {}
        
        print(" POKER COACH PRO - SISTEMA MEJORADO")
        print("=" * 60)
        
        # Cargar templates reales
        self.load_real_templates()
    
    def load_config(self):
        """Cargar configuración de ventana"""
        config_path = "config/window_config.json"
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        else:
            print("  No hay configuración de ventana. Ejecuta window_selector.py")
            return {
                "window_name": "PokerStars",
                "regions": {
                    "mesa": [100, 100, 800, 600],
                    "cartas_jugador": [400, 500, 150, 50],
                    "cartas_mesa": [300, 300, 400, 80],
                    "pozo": [350, 250, 200, 40]
                }
            }
    
    def load_real_templates(self):
        """Cargar templates reales de cartas"""
        templates_dir = "data/card_templates/pokerstars_real"
        
        if not os.path.exists(templates_dir):
            print(" No hay templates reales. Ejecuta capture_templates.py")
            print(" Usando modo SIMULADO (cartas predefinidas)")
            return
        
        suits = ["hearts", "diamonds", "clubs", "spades"]
        values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        
        templates_loaded = 0
        for suit in suits:
            for value in values:
                template_path = f"{templates_dir}/{suit}/{value}.png"
                if os.path.exists(template_path):
                    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        key = f"{value}{suit[0]}"  # Ej: "Ah" para As de corazones
                        self.card_templates[key] = template
                        templates_loaded += 1
        
        if templates_loaded > 0:
            print(f" Cargados {templates_loaded} templates reales de cartas")
            self.templates_loaded = True
        else:
            print("  No se pudieron cargar templates. Usando modo SIMULADO")
    
    def recognize_cards_real(self, card_region):
        """Reconocer cartas usando templates reales"""
        if not self.templates_loaded or card_region is None:
            return {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]}
        
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(card_region, cv2.COLOR_BGR2GRAY)
            
            # Buscar coincidencias
            detected_cards = []
            
            for card_name, template in self.card_templates.items():
                # Ajustar tamaño del template si es necesario
                if template.shape[0] > gray.shape[0] or template.shape[1] > gray.shape[1]:
                    continue
                
                # Realizar template matching
                result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # Si la coincidencia es buena (> 0.8)
                if max_val > 0.8:
                    detected_cards.append(card_name)
            
            # Separar cartas de hero y comunidad (simplificado)
            if detected_cards:
                return {
                    "hero": detected_cards[:2] if len(detected_cards) >= 2 else ["?", "?"],
                    "community": detected_cards[2:5] if len(detected_cards) >= 5 else []
                }
        
        except Exception as e:
            print(f"  Error en reconocimiento: {e}")
        
        return {"hero": ["?", "?"], "community": []}
    
    def capture_screen_region(self, region):
        """Capturar una región específica de la pantalla"""
        try:
            import mss
            
            x, y, w, h = region
            
            with mss.mss() as sct:
                monitor = {
                    "left": x,
                    "top": y,
                    "width": w,
                    "height": h
                }
                
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)
                
                # Convertir BGRA a BGR
                if img.shape[2] == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                return img
        
        except Exception as e:
            print(f" Error capturando región {region}: {e}")
            return None
    
    def extract_pot_value(self, pot_region):
        """Extraer valor del pozo usando OCR simple"""
        if pot_region is None:
            return "1250"
        
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(pot_region, cv2.COLOR_BGR2GRAY)
            
            # Umbralizar para mejor contraste
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Intentar OCR con pytesseract si está disponible
            try:
                import pytesseract
                text = pytesseract.image_to_string(thresh, config='--psm 7 digits')
                if text.strip():
                    return text.strip()
            except:
                pass
            
            # Si no hay OCR, retornar valor simulado
            return "1250"
        
        except Exception as e:
            print(f"  Error en OCR: {e}")
            return "1250"
    
    def analyze_table(self):
        """Analizar la mesa completa"""
        regions = self.config["regions"]
        
        # Capturar cada región
        mesa_img = self.capture_screen_region(regions["mesa"])
        cartas_hero_img = self.capture_screen_region(regions["cartas_jugador"])
        cartas_mesa_img = self.capture_screen_region(regions["cartas_mesa"])
        pozo_img = self.capture_screen_region(regions["pozo"])
        
        # Guardar para depuración
        if mesa_img is not None:
            os.makedirs("debug", exist_ok=True)
            timestamp = datetime.now().strftime("%H%M%S")
            cv2.imwrite(f"debug/mesa_{timestamp}.jpg", mesa_img)
        
        # Reconocer cartas
        if self.templates_loaded and cartas_hero_img is not None:
            cards_info = self.recognize_cards_real(cartas_hero_img)
        else:
            cards_info = {"hero": ["Ah", "Ks"], "community": ["Qd", "Jc", "Th"]}
        
        # Extraer pozo
        pot_value = self.extract_pot_value(pozo_img)
        
        return {
            "cards": cards_info,
            "pot": pot_value,
            "real_mode": self.templates_loaded,
            "templates_count": len(self.card_templates),
            "timestamp": time.time()
        }
    
    def run_analysis(self):
        """Ejecutar análisis continuo"""
        from platforms.pokerstars_adapter import PokerStarsAdapter
        from core.poker_engine import PokerEngine
        
        adapter = PokerStarsAdapter("LOW")
        engine = PokerEngine()
        
        adapter.start()
        
        print(f"\n INICIANDO ANÁLISIS {'REAL' if self.templates_loaded else 'SIMULADO'}")
        print(f"   Templates cargados: {len(self.card_templates)}/52")
        print("   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n Iteración {iteration}")
                
                # Analizar mesa
                table_data = self.analyze_table()
                
                # Mostrar información
                mode = "REAL " if table_data["real_mode"] else "SIMULADO "
                print(f"   Modo: {mode}")
                print(f"   Tus cartas: {table_data['cards']['hero']}")
                print(f"   Mesa: {table_data['cards']['community']}")
                print(f"   Pozo: ${table_data['pot']}")
                
                # Analizar con motor GTO
                pot_int = int(table_data["pot"]) if table_data["pot"].isdigit() else 0
                
                decision = engine.analyze_hand(
                    hole_cards=table_data["cards"]["hero"],
                    community_cards=table_data["cards"]["community"],
                    pot_size=pot_int,
                    position="middle"
                )
                
                print(f"\n    RECOMENDACIÓN:")
                print(f"      Acción: {decision.get('action', 'CHECK')}")
                print(f"      Confianza: {decision.get('confidence', 0)*100:.1f}%")
                print(f"      Razón: {decision.get('reason', '')}")
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            print("\n\n  Detenido por usuario")
        except Exception as e:
            print(f"\n Error: {e}")
        finally:
            adapter.stop()
            print("\n Sistema detenido")

if __name__ == "__main__":
    coach = EnhancedPokerCoach()
    coach.run_analysis()
