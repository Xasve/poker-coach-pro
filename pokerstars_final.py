"""
POKERSTARS LIVE ASSISTANT - VERSIÓN FINAL
Configuración 100% manual para evitar errores
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
    from integration.action_suggester import ActionSuggester
    print("✅ ActionSuggester cargado")
    HAS_SUGGESTER = True
except:
    print("⚠️  ActionSuggester no disponible, usando lógica básica")
    HAS_SUGGESTER = False

class PokerStarsFinalAssistant:
    """Versión final con configuración manual garantizada"""
    
    def __init__(self):
        print("🎮 POKERSTARS FINAL ASSISTANT v1.0")
        print("=" * 50)
        
        # Inicializar componentes
        if HAS_SUGGESTER:
            self.suggester = ActionSuggester()
        
        # Estado del sistema
        self.table_region = None
        self.hand_history = []
        
        # Crear carpetas necesarias
        os.makedirs("debug", exist_ok=True)
        os.makedirs("config", exist_ok=True)
    
    def setup_window_manual(self):
        """Configuración manual paso a paso"""
        print("\n" + "=" * 50)
        print("🎯 CONFIGURACIÓN DE VENTANA - PASO A PASO")
        print("=" * 50)
        
        print("\n📋 PREPARACIÓN:")
        print("1. Abre PokerStars")
        print("2. Abre una mesa de Texas Hold'em")
        print("3. Maximiza la ventana de PokerStars")
        print("4. NO minimices esta ventana de consola")
        
        input("\n✅ Presiona Enter CUANDO TODO ESTÉ LISTO...")
        
        print("\n" + "=" * 50)
        print("🖱️  PASO 1: ESQUINA SUPERIOR IZQUIERDA")
        print("=" * 50)
        print("• Mueve el mouse a la ESQUINA SUPERIOR IZQUIERDA")
        print("  de la mesa de PokerStars")
        print("• Debe ser donde empieza el área de juego")
        print("• Normalmente cerca de donde están las cartas comunitarias")
        
        input("\n🖱️  Presiona Enter cuando el mouse esté en posición...")
        
        x1, y1 = pyautogui.position()
        print(f"📍 Coordenadas capturadas: ({x1}, {y1})")
        
        print("\n" + "=" * 50)
        print("🖱️  PASO 2: ESQUINA INFERIOR DERECHA")
        print("=" * 50)
        print("• Mueve el mouse a la ESQUINA INFERIOR DERECHA")
        print("• Debe incluir los botones de acción (FOLD, CALL, RAISE)")
        print("• Incluye también el área de apuestas")
        
        input("\n🖱️  Presiona Enter cuando el mouse esté en posición...")
        
        x2, y2 = pyautogui.position()
        print(f"📍 Coordenadas capturadas: ({x2}, {y2})")
        
        # Calcular región (asegurar valores positivos)
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        self.table_region = (left, top, width, height)
        
        print("\n" + "=" * 50)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 50)
        print(f"📏 Región: X={left}, Y={top}")
        print(f"📐 Tamaño: {width}x{height}")
        
        # Validar tamaño mínimo
        if width < 100 or height < 100:
            print("⚠️  Advertencia: Región muy pequeña, puede no funcionar bien")
        
        # Guardar configuración
        self.save_config()
        
        # Mostrar preview
        self.show_preview()
        
        return True
    
    def show_preview(self):
        """Mostrar preview de la región"""
        print("\n👁️  CAPTURANDO PREVIEW...")
        screenshot = self.capture_table()
        
        if screenshot is not None:
            # Mostrar información
            h, w = screenshot.shape[:2]
            print(f"   Preview: {w}x{h} píxeles")
            
            # Guardar preview
            preview_path = "debug/preview_region.png"
            cv2.imwrite(preview_path, screenshot)
            print(f"   Preview guardado en: {preview_path}")
            
            # Mostrar áreas de interés
            print("\n   📍 Áreas de interés:")
            print(f"      Cartas: ({int(w*0.45)}, {int(h*0.70)}) a ({int(w*0.55)}, {int(h*0.85)})")
            print(f"      Botones: ({int(w*0.60)}, {int(h*0.85)}) a ({int(w*0.80)}, {int(h*0.92)})")
        else:
            print("   ❌ No se pudo capturar preview")
    
    def save_config(self):
        """Guardar configuración en archivo"""
        if not self.table_region:
            return
        
        config = {
            "table_region": self.table_region,
            "timestamp": datetime.now().isoformat(),
            "screen_resolution": pyautogui.size()
        }
        
        try:
            config_path = "config/window_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            print(f"💾 Configuración guardada en: {config_path}")
        except Exception as e:
            print(f"⚠️  No se pudo guardar configuración: {e}")
    
    def load_config(self):
        """Cargar configuración desde archivo"""
        try:
            config_path = "config/window_config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Convertir lista a tupla
            self.table_region = tuple(config["table_region"])
            
            print("📂 Configuración cargada automáticamente")
            print(f"   Última configuración: {config.get('timestamp', 'N/A')}")
            
            return True
        except:
            return False
    
    def capture_table(self):
        """Capturar la mesa - versión robusta"""
        if not self.table_region:
            return None
        
        try:
            x, y, w, h = self.table_region
            
            # Validar parámetros
            if w <= 10 or h <= 10:
                print(f"❌ Región inválida: {w}x{h} (muy pequeña)")
                return None
            
            # Verificar que esté dentro de la pantalla
            screen_width, screen_height = pyautogui.size()
            if x < 0 or y < 0 or (x + w) > screen_width or (y + h) > screen_height:
                print(f"⚠️  Región fuera de pantalla: {x},{y} {w}x{h}")
                print(f"   Pantalla: {screen_width}x{screen_height}")
            
            # Capturar
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            return screenshot_bgr
            
        except Exception as e:
            print(f"❌ Error capturando pantalla: {e}")
            return None
    
    def analyze_table(self):
        """Análisis principal de la mesa"""
        print(f"\n🔍 ANALIZANDO MESA ({datetime.now().strftime('%H:%M:%S')})")
        
        # 1. Capturar
        screenshot = self.capture_table()
        if screenshot is None:
            print("   ❌ Error: No se pudo capturar pantalla")
            return None
        
        # 2. Mostrar información básica
        h, w = screenshot.shape[:2]
        print(f"   📏 Resolución capturada: {w}x{h}")
        
        # 3. Convertir a escala de grises para análisis
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # 4. Analizar áreas clave
        # Área de cartas del jugador (70-85% desde arriba, centro)
        card_area = gray[int(h*0.70):int(h*0.85), int(w*0.45):int(w*0.55)]
        card_brightness = np.mean(card_area)
        
        # Área de botones de acción (85-92% desde arriba, lado derecho)
        button_area = gray[int(h*0.85):int(h*0.92), int(w*0.60):int(w*0.80)]
        button_brightness = np.mean(button_area)
        
        print(f"   💡 Brillo cartas: {card_brightness:.1f}")
        print(f"   💡 Brillo botones: {button_brightness:.1f}")
        
        # 5. Determinar estado del juego
        game_state = {
            "is_our_turn": button_brightness > 160,
            "game_phase": self.determine_game_phase(card_brightness),
            "available_actions": ["FOLD", "CALL", "RAISE"] if button_brightness > 160 else [],
            "analysis": {
                "card_brightness": card_brightness,
                "button_brightness": button_brightness
            }
        }
        
        print(f"   🎮 Fase detectada: {game_state['game_phase']}")
        print(f"   👤 Tu turno: {'✅ SÍ' if game_state['is_our_turn'] else '❌ NO'}")
        
        return game_state, screenshot
    
    def determine_game_phase(self, card_brightness):
        """Determinar fase del juego basado en brillo"""
        if card_brightness > 180:
            return "PREFLOP"
        elif card_brightness > 140:
            return "FLOP"
        elif card_brightness > 100:
            return "TURN"
        else:
            return "RIVER"
    
    def get_suggestion(self, game_state):
        """Obtener sugerencia de acción"""
        if not game_state["is_our_turn"]:
            return {
                "action": "WAIT",
                "confidence": 0.95,
                "reasoning": "No es tu turno (botones no activos)"
            }
        
        # Usar ActionSuggester si está disponible
        if HAS_SUGGESTER:
            try:
                analysis = self.suggester.analyze_situation(
                    hero_cards=["??", "??"],
                    board_cards=[],
                    game_state=game_state
                )
                suggestion = self.suggester.suggest_action(analysis)
                return suggestion
            except Exception as e:
                print(f"   ⚠️  Error en suggester: {e}")
        
        # Lógica de respaldo basada en brillo
        button_brightness = game_state["analysis"]["button_brightness"]
        
        if button_brightness > 200:
            action = "RAISE"
            reasoning = "Botones muy brillantes (acción agresiva disponible)"
        elif button_brightness > 170:
            action = "CALL"
            reasoning = "Botones visibles (acción disponible)"
        else:
            action = "CHECK"
            reasoning = "Botones poco visibles (solo check disponible)"
        
        return {
            "action": action,
            "confidence": 0.7,
            "reasoning": reasoning,
            "brightness": button_brightness
        }
    
    def run_analysis(self):
        """Ejecutar análisis completo"""
        result = self.analyze_table()
        if not result:
            return None
        
        game_state, screenshot = result
        
        # Obtener sugerencia
        suggestion = self.get_suggestion(game_state)
        
        # Guardar en historial
        hand_data = {
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "suggestion": suggestion
        }
        self.hand_history.append(hand_data)
        
        return suggestion
    
    def show_suggestion(self, suggestion):
        """Mostrar sugerencia de forma clara"""
        if not suggestion:
            return
        
        # Emojis y colores para cada acción
        action_display = {
            "FOLD": "🔴 FOLD (Tirar)",
            "CHECK": "🟡 CHECK (Pasar)",
            "CALL": "🟢 CALL (Igualar)",
            "RAISE": "🟢 RAISE (Subir)",
            "BET": "🟢 BET (Apostar)",
            "ALL_IN": "⚫ ALL-IN (Ir con todo)",
            "WAIT": "⚪ WAIT (Esperar)"
        }
        
        action_text = action_display.get(suggestion["action"], f"⚪ {suggestion['action']}")
        
        print("\n" + "=" * 60)
        print("💡 SUGERENCIA DEL ASISTENTE")
        print("=" * 60)
        print(f"🎯 ACCIÓN: {action_text}")
        print(f"📊 CONFIANZA: {suggestion.get('confidence', 0.5):.0%}")
        print(f"🧠 RAZÓN: {suggestion.get('reasoning', '')}")
        
        if "brightness" in suggestion:
            print(f"💡 BRILO BOTONES: {suggestion['brightness']:.1f}")
        
        print("=" * 60)
        print("👉 TÚ EJECUTAS ESTA ACCIÓN MANUALMENTE EN POKERSTARS")
        print("=" * 60)
    
    def save_screenshot_debug(self):
        """Guardar screenshot para debugging"""
        if not self.table_region:
            print("❌ No hay región configurada")
            return False
        
        screenshot = self.capture_table()
        if screenshot is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug/screenshot_{timestamp}.png"
            cv2.imwrite(filename, screenshot)
            print(f"💾 Screenshot guardado: {filename}")
            
            # También guardar análisis
            self.save_analysis_report(screenshot)
            return True
        
        return False
    
    def save_analysis_report(self, screenshot):
        """Guardar reporte de análisis"""
        try:
            h, w = screenshot.shape[:2]
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "resolution": f"{w}x{h}",
                "region": self.table_region,
                "analysis_points": {
                    "cards_area": (int(w*0.45), int(h*0.70), int(w*0.55), int(h*0.85)),
                    "buttons_area": (int(w*0.60), int(h*0.85), int(w*0.80), int(h*0.92))
                }
            }
            
            report_path = f"debug/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            
            print(f"📊 Reporte de análisis guardado")
            
        except Exception as e:
            print(f"⚠️  No se pudo guardar reporte: {e}")
    
    def show_history(self):
        """Mostrar historial"""
        if not self.hand_history:
            print("\n📭 No hay historial de manos")
            return
        
        print(f"\n📊 HISTORIAL ({len(self.hand_history)} manos)")
        print("=" * 60)
        
        for i, hand in enumerate(self.hand_history[-5:]):
            idx = len(self.hand_history) - 5 + i
            sugg = hand.get("suggestion", {})
            time_str = hand.get("timestamp", "N/A")[11:19]
            
            print(f"\n#{idx+1} - {time_str}")
            print(f"   Acción: {sugg.get('action', 'N/A')}")
            print(f"   Confianza: {sugg.get('confidence', 0):.0%}")
            
            if "reasoning" in sugg:
                reason = sugg["reasoning"]
                if len(reason) > 40:
                    reason = reason[:37] + "..."
                print(f"   Razón: {reason}")
        
        print("=" * 60)
    
    def run(self):
        """Ejecutar el asistente principal"""
        print("\n🔧 INICIALIZANDO SISTEMA...")
        
        # Intentar cargar configuración previa
        if self.load_config():
            print(f"   Región cargada: {self.table_region}")
            
            # Preguntar si usar o reconfigurar
            choice = input("\n¿Usar esta configuración? (s=usar, n=reconfigurar): ").strip().lower()
            if choice == 'n':
                self.setup_window_manual()
        else:
            # Configuración inicial obligatoria
            print("   No hay configuración previa")
            self.setup_window_manual()
        
        print("\n" + "=" * 50)
        print("✅ SISTEMA LISTO PARA USAR")
        print("=" * 50)
        
        # Bucle principal
        while True:
            print("\n🎮 COMANDOS:")
            print("   [Enter] - Analizar mesa actual")
            print("   s       - Guardar screenshot")
            print("   h       - Ver historial")
            print("   c       - Cambiar configuración")
            print("   q       - Salir")
            
            cmd = input("\n👉 Tu comando: ").strip().lower()
            
            if cmd == 'q':
                print("\n👋 Saliendo del sistema...")
                break
            
            elif cmd == 's':
                print("\n💾 Guardando screenshot...")
                self.save_screenshot_debug()
            
            elif cmd == 'h':
                self.show_history()
            
            elif cmd == 'c':
                print("\n🔄 Reconfigurando...")
                self.setup_window_manual()
            
            else:
                # Análisis normal
                suggestion = self.run_analysis()
                if suggestion:
                    self.show_suggestion(suggestion)
                
                # Preguntar si guardar
                if suggestion and suggestion.get("action") != "WAIT":
                    save = input("\n¿Guardar análisis de esta mano? (s/n): ").strip().lower()
                    if save == 's':
                        self.save_screenshot_debug()

def main():
    """Función principal"""
    print("🎴 POKERSTARS FINAL ASSISTANT")
    print("🤖 Configuración manual garantizada")
    print("🎯 Bot sugiere → Tú ejecutas")
    print("-" * 50)
    
    try:
        assistant = PokerStarsFinalAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n✅ Programa terminado. ¡Buena suerte en las mesas!")

if __name__ == "__main__":
    main()