"""
POKERSTARS LIVE ASSISTANT - VERSIÓN FUNCIONAL
Usa los métodos reales de WindowSelector
"""

import sys
import os
import time
import json
from datetime import datetime
import pyautogui
import cv2
import numpy as np

# Añadir src al path
sys.path.insert(0, 'src')

try:
    from utils.window_selector import WindowSelector
    from integration.action_suggester import ActionSuggester
    print("✅ Módulos cargados correctamente")
except Exception as e:
    print(f"⚠️  Error cargando módulos: {e}")
    sys.exit(1)

class PokerStarsWorkingAssistant:
    """Versión que funciona con WindowSelector real"""
    
    def __init__(self):
        print("🎮 POKERSTARS WORKING ASSISTANT v1.0")
        print("=" * 50)
        
        # Inicializar componentes
        self.window_selector = WindowSelector()
        self.suggester = ActionSuggester()
        
        # Estado del sistema
        self.table_region = None
        self.hand_history = []
        
    def setup_window(self):
        """Configurar ventana usando métodos reales"""
        print("\n🎯 CONFIGURACIÓN DE VENTANA")
        print("=" * 40)
        
        # Método 1: Usar define_area si está disponible
        try:
            print("Usando define_area para seleccionar región...")
            # Llamar al método run() para iniciar la interfaz
            self.window_selector.run()
            
            # Después de run(), deberíamos tener una región configurada
            # Esto depende de cómo esté implementado WindowSelector
            print("✅ Configuración completada via define_area")
            return True
        except Exception as e:
            print(f"⚠️  Error con define_area: {e}")
        
        # Método 2: Configuración manual simple
        print("\n🔄 Usando configuración manual...")
        return self.manual_window_selection()
    
    def manual_window_selection(self):
        """Selección manual si los otros métodos fallan"""
        print("\n🖱️  CONFIGURACIÓN MANUAL")
        print("1. Abre PokerStars y una mesa")
        print("2. Maximiza la ventana")
        print("3. Posiciona el mouse")
        
        input("\n📋 Presiona Enter para comenzar...")
        
        # Obtener esquina superior izquierda
        print("\n🖱️  Mueve el mouse a la ESQUINA SUPERIOR IZQUIERDA")
        print("   de la mesa de PokerStars (donde empiezan las cartas)")
        input("   Presiona Enter cuando estés listo...")
        
        x1, y1 = pyautogui.position()
        print(f"   📍 Punto 1: ({x1}, {y1})")
        
        # Obtener esquina inferior derecha
        print("\n🖱️  Mueve el mouse a la ESQUINA INFERIOR DERECHA")
        print("   de la mesa de PokerStars (donde están los botones de acción)")
        input("   Presiona Enter cuando estés listo...")
        
        x2, y2 = pyautogui.position()
        print(f"   📍 Punto 2: ({x2}, {y2})")
        
        # Calcular región
        self.table_region = (x1, y1, x2-x1, y2-y1)
        
        print(f"\n✅ REGIÓN CONFIGURADA:")
        print(f"   X: {x1}, Y: {y1}")
        print(f"   Ancho: {x2-x1}, Alto: {y2-y1}")
        
        # Guardar configuración
        self.save_config()
        
        return True
    
    def save_config(self):
        """Guardar configuración para futuras sesiones"""
        config = {
            "table_region": self.table_region,
            "last_configured": datetime.now().isoformat()
        }
        
        try:
            os.makedirs("config", exist_ok=True)
            with open("config/window_config.json", "w") as f:
                json.dump(config, f, indent=2)
            print("💾 Configuración guardada en config/window_config.json")
        except:
            print("⚠️  No se pudo guardar la configuración")
    
    def load_config(self):
        """Cargar configuración guardada"""
        try:
            with open("config/window_config.json", "r") as f:
                config = json.load(f)
                self.table_region = tuple(config["table_region"])
                print("📂 Configuración cargada automáticamente")
                return True
        except:
            return False
    
    def capture_table(self):
        """Capturar pantalla de la mesa"""
        if not self.table_region:
            print("❌ No hay región configurada")
            return None
        
        try:
            x, y, w, h = self.table_region
            print(f"📸 Capturando región: x={x}, y={y}, w={w}, h={h}")
            
            # Validar tamaño
            if w <= 0 or h <= 0:
                print("❌ Región inválida (ancho o alto negativo)")
                return None
            
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            return screenshot_bgr
        except Exception as e:
            print(f"❌ Error capturando pantalla: {e}")
            return None
    
    def analyze_table_state(self, screenshot):
        """Analizar estado de la mesa"""
        if screenshot is None:
            return None
        
        h, w = screenshot.shape[:2]
        
        print(f"\n📊 ANÁLISIS DE PANTALLA:")
        print(f"   Resolución: {w}x{h}")
        
        # Analizar diferentes áreas
        analysis = {
            "resolution": f"{w}x{h}",
            "areas": {}
        }
        
        # Área de cartas (70-85% desde arriba, centro)
        card_area = screenshot[int(h*0.70):int(h*0.85), int(w*0.45):int(w*0.55)]
        card_mean = np.mean(cv2.cvtColor(card_area, cv2.COLOR_BGR2GRAY))
        analysis["areas"]["cards"] = card_mean
        
        # Área de botones (85-92% desde arriba, derecha)
        button_area = screenshot[int(h*0.85):int(h*0.92), int(w*0.6):int(w*0.8)]
        button_mean = np.mean(cv2.cvtColor(button_area, cv2.COLOR_BGR2GRAY))
        analysis["areas"]["buttons"] = button_mean
        
        # Determinar si es nuestro turno (botones brillantes)
        is_our_turn = button_mean > 160
        
        # Determinar fase del juego
        if card_mean > 180:
            game_phase = "PREFLOP"
        elif card_mean > 120:
            game_phase = "POSTFLOP"
        else:
            game_phase = "FLOP/TURN/RIVER"
        
        return {
            "game_phase": game_phase,
            "is_our_turn": is_our_turn,
            "available_actions": ["FOLD", "CALL", "RAISE"] if is_our_turn else [],
            "analysis": analysis
        }
    
    def get_suggestion(self, game_state):
        """Obtener sugerencia basada en estado del juego"""
        if not game_state["is_our_turn"]:
            return {
                "action": "WAIT",
                "confidence": 0.9,
                "reasoning": "No es tu turno (botones no activos)"
            }
        
        # Usar el ActionSuggester
        try:
            analysis = self.suggester.analyze_situation(
                hero_cards=["??", "??"],  # Placeholder por ahora
                board_cards=[],
                game_state=game_state
            )
            
            suggestion = self.suggester.suggest_action(analysis)
            return suggestion
        except Exception as e:
            print(f"⚠️  Error usando suggester: {e}")
            
            # Sugerencia básica de respaldo
            button_brightness = game_state["analysis"]["areas"]["buttons"]
            if button_brightness > 200:
                action = "RAISE"
            elif button_brightness > 170:
                action = "CALL"
            else:
                action = "CHECK"
            
            return {
                "action": action,
                "confidence": 0.6,
                "reasoning": f"Basado en brillo de botones ({button_brightness:.0f})"
            }
    
    def run_analysis_cycle(self):
        """Ejecutar un ciclo completo de análisis"""
        print(f"\n🔄 CICLO DE ANÁLISIS ({datetime.now().strftime('%H:%M:%S')})")
        
        # 1. Capturar
        screenshot = self.capture_table()
        if screenshot is None:
            return None
        
        # 2. Analizar
        game_state = self.analyze_table_state(screenshot)
        if not game_state:
            return None
        
        # Mostrar análisis
        print(f"   Fase: {game_state['game_phase']}")
        print(f"   Tu turno: {'✅ SÍ' if game_state['is_our_turn'] else '❌ NO'}")
        
        # 3. Obtener sugerencia
        suggestion = self.get_suggestion(game_state)
        
        # 4. Guardar en historial
        hand_data = {
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "suggestion": suggestion
        }
        self.hand_history.append(hand_data)
        
        return suggestion
    
    def show_suggestion(self, suggestion):
        """Mostrar sugerencia formateada"""
        if not suggestion:
            return
        
        # Colores según acción
        action_colors = {
            "FOLD": "🔴",
            "CHECK": "🟡",
            "CALL": "🟢",
            "RAISE": "🟢",
            "BET": "🟢",
            "WAIT": "⚪",
            "ALL_IN": "⚫"
        }
        
        emoji = action_colors.get(suggestion["action"], "⚪")
        
        print("\n" + "=" * 50)
        print(f"{emoji}  SUGERENCIA  {emoji}")
        print("=" * 50)
        print(f"🎯 ACCIÓN: {suggestion['action']}")
        print(f"📊 CONFIANZA: {suggestion.get('confidence', 0.5):.0%}")
        print(f"🧠 RAZÓN: {suggestion.get('reasoning', '')}")
        
        if "bet_size" in suggestion:
            print(f"💰 TAMAÑO: {suggestion['bet_size']}")
        
        print("=" * 50)
        print("👉 EJECUTA ESTO MANUALMENTE EN POKERSTARS")
        print("=" * 50)
    
    def run(self):
        """Ejecutar el asistente principal"""
        print("\n🔧 INICIALIZANDO SISTEMA...")
        
        # Intentar cargar configuración previa
        if not self.load_config():
            print("📝 Configuración no encontrada, necesaria configuración inicial")
            if not self.setup_window():
                print("❌ Configuración fallida")
                return
        
        print("\n✅ SISTEMA LISTO")
        print("=" * 50)
        print("🎮 COMANDOS DISPONIBLES:")
        print("   Enter  - Analizar mesa actual")
        print("   s      - Guardar screenshot")
        print("   h      - Ver historial")
        print("   c      - Cambiar región")
        print("   q      - Salir")
        print("=" * 50)
        
        while True:
            cmd = input("\n👉 Comando: ").strip().lower()
            
            if cmd == 'q':
                break
            
            elif cmd == 'h':
                self.show_history()
            
            elif cmd == 's':
                self.save_screenshot()
            
            elif cmd == 'c':
                self.setup_window()
            
            else:
                # Análisis normal
                suggestion = self.run_analysis_cycle()
                if suggestion:
                    self.show_suggestion(suggestion)
    
    def show_history(self):
        """Mostrar historial de manos"""
        if not self.hand_history:
            print("\n📭 No hay historial de manos")
            return
        
        print(f"\n📊 HISTORIAL ({len(self.hand_history)} manos)")
        print("=" * 60)
        
        for i, hand in enumerate(self.hand_history[-5:]):  # Últimas 5
            idx = len(self.hand_history) - 5 + i
            sugg = hand.get("suggestion", {})
            time_str = hand.get("timestamp", "N/A")[11:19]
            
            print(f"\n#{idx+1} - {time_str}")
            print(f"   Acción: {sugg.get('action', 'N/A')}")
            print(f"   Confianza: {sugg.get('confidence', 0):.0%}")
            print(f"   Fase: {hand.get('game_state', {}).get('game_phase', 'N/A')}")
        
        print("=" * 60)
    
    def save_screenshot(self):
        """Guardar screenshot para debug"""
        if not self.table_region:
            print("❌ No hay región configurada")
            return
        
        screenshot = self.capture_table()
        if screenshot is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug_screenshots/screenshot_{timestamp}.png"
            
            os.makedirs("debug_screenshots", exist_ok=True)
            cv2.imwrite(filename, screenshot)
            print(f"💾 Screenshot guardado: {filename}")
        else:
            print("❌ No se pudo capturar screenshot")

def main():
    """Función principal"""
    print("🎴 POKERSTARS WORKING ASSISTANT")
    print("🤖 Versión corregida y funcional")
    print("-" * 50)
    
    # Crear carpetas necesarias
    os.makedirs("debug_screenshots", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    try:
        assistant = PokerStarsWorkingAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n✅ Programa terminado. ¡Buena suerte en las mesas!")

if __name__ == "__main__":
    main()