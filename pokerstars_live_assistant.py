"""
POKERSTARS LIVE ASSISTANT - Sistema principal
Modo asistente: bot sugiere, tú ejecutas
"""

import sys
import os
import time
import json
from datetime import datetime

# Añadir src al path
sys.path.insert(0, 'src')

try:
    from integration.pokerstars_live_detector import PokerStarsLiveDetector
    from integration.action_suggester import ActionSuggester
    from utils.screen_capturer import ScreenCapturer
    from utils.window_selector import WindowSelector
    from core.learning_system import PokerCoachProCompleteSystem
    import pyautogui
    import cv2
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("📦 Instala dependencias: pip install -r requirements.txt")
    sys.exit(1)

class PokerStarsLiveAssistant:
    """Sistema principal de asistencia en vivo"""
    
    def __init__(self):
        print("🎮 POKERSTARS LIVE ASSISTANT v1.0")
        print("=" * 50)
        
        # Inicializar componentes
        self.window_selector = WindowSelector()
        self.capturer = ScreenCapturer()
        self.detector = PokerStarsLiveDetector()
        self.suggester = ActionSuggester()
        self.coach = PokerCoachProCompleteSystem()
        
        # Estado del sistema
        self.table_region = None
        self.is_running = False
        self.hand_history = []
        self.config = self.load_config()
        
    def load_config(self):
        """Cargar configuración del sistema"""
        config_path = os.path.join('config', 'live_config.json')
        default_config = {
            "scan_interval": 1.0,
            "save_screenshots": False,
            "screenshot_path": "debug_screenshots",
            "log_level": "INFO",
            "mode": "assistant"
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config
    
    def setup(self):
        """Configuración inicial interactiva"""
        print("\n🔧 CONFIGURACIÓN INICIAL")
        print("1. Asegúrate de tener PokerStars abierto")
        print("2. Abre una mesa de Texas Hold'em")
        print("3. Maximiza la ventana para mejor detección")
        
        input("\n📋 Presiona Enter cuando estés listo...")
        
        # Seleccionar ventana de PokerStars
        print("\n🎯 Seleccionando ventana de PokerStars...")
        self.table_region = self.window_selector.select_window_interactive()
        
        if not self.table_region:
            print("❌ No se pudo seleccionar ventana. Usando pantalla completa.")
            self.table_region = (0, 0, 1920, 1080)  # Default 1080p
        
        print(f"✅ Región configurada: {self.table_region}")
        
        # Calibrar detector
        print("\n🎨 Calibrando detector...")
        screenshot = self.capturer.capture_region(self.table_region)
        if screenshot is not None:
            calibration_result = self.detector.calibrate(screenshot)
            if calibration_result:
                print("✅ Calibración exitosa")
            else:
                print("⚠️  Calibración básica, puede necesitar ajustes")
        else:
            print("❌ No se pudo capturar pantalla")
            return False
        
        # Mostrar instrucciones
        self.show_instructions()
        return True
    
    def show_instructions(self):
        """Mostrar instrucciones de uso"""
        print("\n" + "=" * 50)
        print("📖 INSTRUCCIONES DE USO:")
        print("=" * 50)
        print("🎮 MODO ASISTENTE ACTIVADO")
        print("• El bot analizará la mesa y sugerirá acciones")
        print("• TÚ ejecutarás las acciones manualmente")
        print("• Sugerencias basadas en GTO y situación actual")
        print("\n🔧 COMANDOS DISPONIBLES:")
        print("• Enter: Analizar mesa actual")
        print("• 's': Guardar screenshot para debugging")
        print("• 'c': Cambiar región de captura")
        print("• 'l': Ver último análisis")
        print("• 'h': Mostrar historial de manos")
        print("• 'q': Salir")
        print("=" * 50)
    
    def analyze_table(self):
        """Analizar la mesa y sugerir acción"""
        print(f"\n📸 Capturando mesa... ({datetime.now().strftime('%H:%M:%S')})")
        
        # 1. Capturar pantalla
        screenshot = self.capturer.capture_region(self.table_region)
        if screenshot is None:
            print("❌ Error capturando pantalla")
            return None
        
        # 2. Detectar estado del juego
        game_state = self.detector.detect_game_state(screenshot)
        
        if not game_state or game_state.get("game_phase") == "UNKNOWN":
            print("⚠️  No se pudo detectar estado del juego")
            return None
        
        # 3. Detectar cartas del jugador
        hero_cards = self.detector.detect_hero_cards(screenshot)
        
        # 4. Detectar cartas comunitarias
        board_cards = self.detector.detect_board_cards(screenshot)
        
        # 5. Analizar situación
        analysis = self.suggester.analyze_situation(
            hero_cards=hero_cards,
            board_cards=board_cards,
            game_state=game_state
        )
        
        # 6. Sugerir acción
        suggestion = self.suggester.suggest_action(analysis)
        
        # 7. Guardar en historial
        hand_data = {
            "timestamp": datetime.now().isoformat(),
            "hero_cards": hero_cards,
            "board_cards": board_cards,
            "game_state": game_state,
            "analysis": analysis,
            "suggestion": suggestion
        }
        self.hand_history.append(hand_data)
        
        return suggestion
    
    def display_suggestion(self, suggestion):
        """Mostrar sugerencia de forma clara"""
        if not suggestion:
            print("❌ No se pudo generar sugerencia")
            return
        
        print("\n" + "=" * 50)
        print("💡 SUGERENCIA DE ACCIÓN")
        print("=" * 50)
        
        action = suggestion.get("action", "CHECK")
        confidence = suggestion.get("confidence", 0)
        reasoning = suggestion.get("reasoning", "Sin análisis disponible")
        
        # Color según acción
        action_colors = {
            "FOLD": "🔴",
            "CHECK": "🟡", 
            "CALL": "🟢",
            "BET": "🟢",
            "RAISE": "🟢",
            "ALL_IN": "⚫"
        }
        
        emoji = action_colors.get(action, "⚪")
        
        print(f"{emoji} ACCIÓN: {action}")
        print(f"📊 CONFIANZA: {confidence:.1%}")
        print(f"🧠 RAZONAMIENTO: {reasoning}")
        
        if "bet_size" in suggestion:
            print(f"💰 TAMAÑO APUESTA: {suggestion['bet_size']}")
        
        print("=" * 50)
        print("👉 Tú ejecuta esta acción manualmente")
        print("=" * 50)
    
    def save_debug_screenshot(self):
        """Guardar screenshot para debugging"""
        if not os.path.exists("debug_screenshots"):
            os.makedirs("debug_screenshots")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug_screenshots/debug_{timestamp}.png"
        
        screenshot = self.capturer.capture_region(self.table_region)
        if screenshot is not None:
            cv2.imwrite(filename, screenshot)
            print(f"📁 Screenshot guardado: {filename}")
            return True
        return False
    
    def run(self):
        """Bucle principal del asistente"""
        if not self.setup():
            print("❌ Configuración fallida. Saliendo...")
            return
        
        self.is_running = True
        
        print("\n✅ Sistema listo. Presiona Enter para analizar mesa...")
        
        while self.is_running:
            user_input = input("\n🎮 Comando (Enter=analizar, s=save, h=historial, q=salir): ").strip().lower()
            
            if user_input == 'q':
                print("\n👋 Saliendo del sistema...")
                self.is_running = False
                break
            
            elif user_input == 's':
                self.save_debug_screenshot()
                continue
            
            elif user_input == 'h':
                self.show_hand_history()
                continue
            
            elif user_input == 'c':
                print("\n🔄 Cambiando región de captura...")
                self.table_region = self.window_selector.select_window_interactive()
                continue
            
            elif user_input == 'l' and self.hand_history:
                last_suggestion = self.hand_history[-1].get("suggestion")
                if last_suggestion:
                    self.display_suggestion(last_suggestion)
                continue
            
            else:
                # Análisis normal
                suggestion = self.analyze_table()
                if suggestion:
                    self.display_suggestion(suggestion)
    
    def show_hand_history(self):
        """Mostrar historial de manos recientes"""
        if not self.hand_history:
            print("\n📭 No hay historial de manos todavía")
            return
        
        print(f"\n📊 HISTORIAL DE MANOS ({len(self.hand_history)} registros)")
        print("=" * 60)
        
        for i, hand in enumerate(self.hand_history[-5:]):  # Mostrar últimas 5
            idx = len(self.hand_history) - 5 + i
            suggestion = hand.get("suggestion", {})
            
            print(f"\nManos #{idx+1} - {hand['timestamp'][11:19]}")
            print(f"  Cartas: {hand.get('hero_cards', ['??', '??'])}")
            print(f"  Mesa: {hand.get('board_cards', [])}")
            print(f"  Acción: {suggestion.get('action', 'N/A')}")
            print(f"  Confianza: {suggestion.get('confidence', 0):.1%}")
        
        print("=" * 60)

def main():
    """Función principal"""
    print("🎴 POKERSTARS LIVE ASSISTANT")
    print("🤖 Bot GTO + 🧠 Tu ejecución = 💰 Ganador")
    print("-" * 50)
    
    try:
        assistant = PokerStarsLiveAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Programa terminado. ¡Buena suerte en las mesas!")

if __name__ == "__main__":
    main()