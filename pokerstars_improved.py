"""
POKERSTARS LIVE ASSISTANT - VERSIÓN MEJORADA
Con umbrales ajustados y mejor detección
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

class PokerStarsImprovedAssistant:
    """Versión mejorada con detección ajustada"""
    
    def __init__(self):
        print("🎮 POKERSTARS IMPROVED ASSISTANT v1.1")
        print("=" * 50)
        
        # Inicializar componentes
        if HAS_SUGGESTER:
            self.suggester = ActionSuggester()
        
        # Estado del sistema
        self.table_region = None
        self.hand_history = []
        
        # UMBRALES AJUSTADOS (basados en tus screenshots)
        self.thresholds = {
            "buttons_active": 40,      # Ajustado de 160 a 40
            "cards_bright_preflop": 50, # Ajustado de 180 a 50
            "cards_bright_flop": 30,    # Ajustado de 140 a 30
            "cards_bright_turn": 20,    # Ajustado de 100 a 20
            "min_button_area": 1000     # Área mínima para botones
        }
        
        # Crear carpetas necesarias
        os.makedirs("debug", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        print(f"⚙️  Umbrales configurados: {self.thresholds}")
    
    def load_config(self):
        """Cargar configuración desde archivo"""
        try:
            config_path = "config/window_config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
            
            # Convertir lista a tupla
            self.table_region = tuple(config["table_region"])
            
            print("📂 Configuración cargada automáticamente")
            print(f"   Región: {self.table_region}")
            
            return True
        except:
            return False
    
    def analyze_with_threshold_adjustment(self):
        """Análisis con ajuste automático de umbrales"""
        print(f"\n🔍 ANALIZANDO MESA ({datetime.now().strftime('%H:%M:%S')})")
        
        # 1. Capturar
        screenshot = self.capture_table()
        if screenshot is None:
            print("   ❌ Error: No se pudo capturar pantalla")
            return None
        
        # 2. Información básica
        h, w = screenshot.shape[:2]
        print(f"   📏 Resolución: {w}x{h}")
        
        # 3. Convertir a diferentes formatos para análisis
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        
        # 4. ANÁLISIS DETALLADO POR ÁREAS
        
        # Área de cartas del jugador
        card_area = gray[int(h*0.70):int(h*0.85), int(w*0.45):int(w*0.55)]
        card_brightness = np.mean(card_area)
        card_std = np.std(card_area)  # Desviación estándar (variación)
        
        # Área de botones (3 zonas: FOLD, CALL, RAISE)
        button_fold = gray[int(h*0.85):int(h*0.92), int(w*0.60):int(w*0.67)]
        button_call = gray[int(h*0.85):int(h*0.92), int(w*0.67):int(w*0.74)]
        button_raise = gray[int(h*0.85):int(h*0.92), int(w*0.74):int(w*0.81)]
        
        button_brightness = np.mean([np.mean(button_fold), np.mean(button_call), np.mean(button_raise)])
        
        # Detección por COLOR (más robusta que solo brillo)
        # PokerStars usa colores específicos:
        # FOLD: Rojo, CALL/CHECK: Verde, RAISE/BET: Azul/Naranja
        
        # Convertir áreas de botones a HSV para detección de color
        fold_area_hsv = hsv[int(h*0.85):int(h*0.92), int(w*0.60):int(w*0.67)]
        call_area_hsv = hsv[int(h*0.85):int(h*0.92), int(w*0.67):int(w*0.74)]
        raise_area_hsv = hsv[int(h*0.85):int(h*0.92), int(w*0.74):int(w*0.81)]
        
        # Detectar colores
        fold_red = self.detect_color(fold_area_hsv, 'red')
        call_green = self.detect_color(call_area_hsv, 'green')
        raise_blue = self.detect_color(raise_area_hsv, 'blue')
        
        print(f"\n   📊 ANÁLISIS DETALLADO:")
        print(f"   💡 Cartas - Brillo: {card_brightness:.1f}, Variación: {card_std:.1f}")
        print(f"   🎮 Botones - Brillo: {button_brightness:.1f}")
        print(f"   🔴 FOLD (rojo): {fold_red:.1f}%")
        print(f"   🟢 CALL (verde): {call_green:.1f}%")
        print(f"   🔵 RAISE (azul): {raise_blue:.1f}%")
        
        # 5. Determinar estado del juego MÁS PRECISO
        is_our_turn = (fold_red > 10 or call_green > 10 or raise_blue > 10 or 
                      button_brightness > self.thresholds["buttons_active"])
        
        game_phase = self.determine_game_phase_improved(card_brightness, card_std)
        
        # Determinar qué botones están realmente activos
        available_actions = []
        if fold_red > 10:
            available_actions.append("FOLD")
        if call_green > 10:
            available_actions.append("CALL")
        if raise_blue > 10:
            available_actions.append("RAISE")
        
        # Si no detectamos por color pero hay brillo, asumimos todas disponibles
        if not available_actions and is_our_turn:
            available_actions = ["FOLD", "CALL", "RAISE"]
        
        game_state = {
            "is_our_turn": is_our_turn,
            "game_phase": game_phase,
            "available_actions": available_actions,
            "analysis": {
                "card_brightness": card_brightness,
                "card_variation": card_std,
                "button_brightness": button_brightness,
                "fold_red": fold_red,
                "call_green": call_green,
                "raise_blue": raise_blue
            }
        }
        
        print(f"\n   🎮 ESTADO FINAL:")
        print(f"   Fase: {game_phase}")
        print(f"   Tu turno: {'✅ SÍ' if is_our_turn else '❌ NO'}")
        if is_our_turn:
            print(f"   Acciones disponibles: {', '.join(available_actions)}")
        
        return game_state, screenshot
    
    def detect_color(self, hsv_area, color):
        """Detectar porcentaje de un color en un área HSV"""
        if color == 'red':
            # Rojo tiene dos rangos en HSV
            lower1 = np.array([0, 100, 100])
            upper1 = np.array([10, 255, 255])
            lower2 = np.array([160, 100, 100])
            upper2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv_area, lower1, upper1)
            mask2 = cv2.inRange(hsv_area, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        
        elif color == 'green':
            lower = np.array([40, 100, 100])
            upper = np.array([80, 255, 255])
            mask = cv2.inRange(hsv_area, lower, upper)
        
        elif color == 'blue':
            lower = np.array([100, 100, 100])
            upper = np.array([140, 255, 255])
            mask = cv2.inRange(hsv_area, lower, upper)
        else:
            return 0
        
        # Calcular porcentaje del área que tiene ese color
        total_pixels = hsv_area.shape[0] * hsv_area.shape[1]
        if total_pixels == 0:
            return 0
        
        colored_pixels = cv2.countNonZero(mask)
        percentage = (colored_pixels / total_pixels) * 100
        
        return percentage
    
    def determine_game_phase_improved(self, brightness, variation):
        """Determinar fase del juego con más precisión"""
        if brightness > self.thresholds["cards_bright_preflop"]:
            return "PREFLOP"
        elif brightness > self.thresholds["cards_bright_flop"]:
            if variation > 15:  # Más variación = probablemente hay cartas
                return "FLOP"
            else:
                return "PREFLOP"
        elif brightness > self.thresholds["cards_bright_turn"]:
            return "TURN"
        else:
            return "RIVER"
    
    def detect_hero_cards_basic(self, screenshot):
        """Detección básica de cartas del jugador"""
        h, w = screenshot.shape[:2]
        
        # Área específica para cartas del hero (ajustar según tema PokerStars)
        # Normalmente en la parte inferior-central
        hero_card_area = screenshot[int(h*0.80):int(h*0.90), 
                                   int(w*0.40):int(w*0.60)]
        
        # Guardar para análisis
        cv2.imwrite("debug/hero_cards_area.png", hero_card_area)
        
        # Para MVP: retornar placeholder
        # EN PRÓXIMAS VERSIONES: implementar OCR
        return ["??", "??"]
    
    def detect_stack_size(self, screenshot):
        """Intentar detectar stack size"""
        h, w = screenshot.shape[:2]
        
        # Área donde normalmente está el stack (parte inferior)
        stack_area = screenshot[int(h*0.90):int(h*0.97), 
                               int(w*0.45):int(w*0.55)]
        
        # Guardar para análisis
        cv2.imwrite("debug/stack_area.png", stack_area)
        
        # Para MVP: retornar placeholder
        return "??"
    
    def get_improved_suggestion(self, game_state):
        """Sugerencia mejorada con más información"""
        if not game_state["is_our_turn"]:
            return {
                "action": "WAIT",
                "confidence": 0.95,
                "reasoning": "No es tu turno (botones no activos)"
            }
        
        # Usar ActionSuggester si está disponible
        if HAS_SUGGESTER:
            try:
                # Detectar cartas y stack para análisis completo
                # (Por ahora placeholders)
                hero_cards = ["??", "??"]
                board_cards = []
                
                analysis = self.suggester.analyze_situation(
                    hero_cards=hero_cards,
                    board_cards=board_cards,
                    game_state=game_state
                )
                suggestion = self.suggester.suggest_action(analysis)
                return suggestion
            except Exception as e:
                print(f"   ⚠️  Error en suggester: {e}")
        
        # Lógica mejorada basada en detección de botones
        analysis = game_state["analysis"]
        
        # Si solo hay FOLD disponible (situación difícil)
        if len(game_state["available_actions"]) == 1 and game_state["available_actions"][0] == "FOLD":
            return {
                "action": "FOLD",
                "confidence": 0.8,
                "reasoning": "Solo FOLD disponible (situación difícil)"
            }
        
        # Basado en qué botones están más "fuertes" (más color)
        fold_strength = analysis["fold_red"]
        call_strength = analysis["call_green"]
        raise_strength = analysis["raise_blue"]
        
        if raise_strength > 20 and raise_strength > call_strength:
            action = "RAISE"
            reasoning = "Botón RAISE claramente visible"
        elif call_strength > 15:
            action = "CALL"
            reasoning = "Botón CALL visible"
        elif fold_strength > 20:
            action = "FOLD"
            reasoning = "Botón FOLD prominente (situación difícil)"
        else:
            # Basado en brillo general
            if analysis["button_brightness"] > 50:
                action = "RAISE"
                reasoning = "Botones brillantes (posición agresiva)"
            elif analysis["button_brightness"] > 30:
                action = "CALL"
                reasoning = "Botones moderadamente brillantes"
            else:
                action = "CHECK"
                reasoning = "Botones poco visibles"
        
        confidence = min(0.9, 0.5 + (analysis["button_brightness"] / 100))
        
        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "details": {
                "fold_strength": fold_strength,
                "call_strength": call_strength,
                "raise_strength": raise_strength
            }
        }
    
    def capture_table(self):
        """Capturar la mesa"""
        if not self.table_region:
            print("❌ No hay región configurada")
            return None
        
        try:
            x, y, w, h = self.table_region
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            return screenshot_bgr
        except Exception as e:
            print(f"❌ Error capturando: {e}")
            return None
    
    def save_detailed_analysis(self, screenshot, game_state):
        """Guardar análisis detallado para debugging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Guardar screenshot completo
        cv2.imwrite(f"debug/full_{timestamp}.png", screenshot)
        
        # 2. Guardar áreas específicas
        h, w = screenshot.shape[:2]
        
        # Cartas
        cards = screenshot[int(h*0.70):int(h*0.85), int(w*0.45):int(w*0.55)]
        cv2.imwrite(f"debug/cards_{timestamp}.png", cards)
        
        # Botones
        buttons = screenshot[int(h*0.85):int(h*0.92), int(w*0.60):int(w*0.81)]
        cv2.imwrite(f"debug/buttons_{timestamp}.png", buttons)
        
        # 3. Guardar datos de análisis
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "thresholds": self.thresholds,
            "resolution": f"{w}x{h}"
        }
        
        with open(f"debug/analysis_{timestamp}.json", "w") as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"💾 Análisis guardado: debug/analysis_{timestamp}.json")
    
    def run_analysis_cycle(self):
        """Ciclo completo de análisis mejorado"""
        result = self.analyze_with_threshold_adjustment()
        if not result:
            return None
        
        game_state, screenshot = result
        
        # Guardar análisis detallado si es nuestro turno
        if game_state["is_our_turn"]:
            self.save_detailed_analysis(screenshot, game_state)
        
        # Obtener sugerencia
        suggestion = self.get_improved_suggestion(game_state)
        
        # Guardar en historial
        hand_data = {
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "suggestion": suggestion
        }
        self.hand_history.append(hand_data)
        
        return suggestion
    
    def show_suggestion(self, suggestion):
        """Mostrar sugerencia"""
        if not suggestion:
            return
        
        action_display = {
            "FOLD": "🔴 FOLD",
            "CHECK": "🟡 CHECK", 
            "CALL": "🟢 CALL",
            "RAISE": "🟢 RAISE",
            "BET": "🟢 BET",
            "ALL_IN": "⚫ ALL-IN",
            "WAIT": "⚪ WAIT"
        }
        
        action_text = action_display.get(suggestion["action"], f"⚪ {suggestion['action']}")
        
        print("\n" + "=" * 60)
        print("💡 SUGERENCIA MEJORADA")
        print("=" * 60)
        print(f"🎯 ACCIÓN: {action_text}")
        print(f"📊 CONFIANZA: {suggestion.get('confidence', 0.5):.0%}")
        print(f"🧠 RAZÓN: {suggestion.get('reasoning', '')}")
        
        if "details" in suggestion:
            details = suggestion["details"]
            print(f"\n📈 DETALLES DE DETECCIÓN:")
            print(f"   🔴 FOLD: {details.get('fold_strength', 0):.1f}%")
            print(f"   🟢 CALL: {details.get('call_strength', 0):.1f}%")
            print(f"   🔵 RAISE: {details.get('raise_strength', 0):.1f}%")
        
        print("=" * 60)
        print("👉 TÚ EJECUTAS ESTA ACCIÓN MANUALMENTE")
        print("=" * 60)
    
    def calibrate_thresholds(self):
        """Calibrar umbrales automáticamente"""
        print("\n🎯 CALIBRANDO UMBRALES...")
        
        screenshot = self.capture_table()
        if screenshot is None:
            return
        
        h, w = screenshot.shape[:2]
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # Analizar varias áreas
        areas = {
            "cards": gray[int(h*0.70):int(h*0.85), int(w*0.45):int(w*0.55)],
            "buttons": gray[int(h*0.85):int(h*0.92), int(w*0.60):int(w*0.81)],
            "table": gray[int(h*0.30):int(h*0.70), int(w*0.30):int(w*0.70)]
        }
        
        print("\n📊 MEDICIONES ACTUALES:")
        for name, area in areas.items():
            brightness = np.mean(area)
            std = np.std(area)
            print(f"   {name}: brillo={brightness:.1f}, variación={std:.1f}")
        
        # Ajustar umbrales basado en mediciones
        buttons_bright = np.mean(areas["buttons"])
        cards_bright = np.mean(areas["cards"])
        
        self.thresholds["buttons_active"] = max(30, buttons_bright * 1.5)
        self.thresholds["cards_bright_preflop"] = max(40, cards_bright * 1.3)
        self.thresholds["cards_bright_flop"] = max(25, cards_bright * 1.1)
        self.thresholds["cards_bright_turn"] = max(15, cards_bright * 0.9)
        
        print(f"\n✅ UMBRALES AJUSTADOS: {self.thresholds}")
        
        # Guardar configuración
        config = {
            "thresholds": self.thresholds,
            "calibration_time": datetime.now().isoformat(),
            "measurements": {k: float(np.mean(v)) for k, v in areas.items()}
        }
        
        with open("config/thresholds.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("💾 Configuración guardada en config/thresholds.json")
    
    def run(self):
        """Ejecutar asistente"""
        print("\n🔧 INICIALIZANDO SISTEMA MEJORADO...")
        
        # Cargar configuración
        if not self.load_config():
            print("❌ Necesitas ejecutar pokerstars_final.py primero para configurar")
            print("   Ejecuta: python pokerstars_final.py")
            return
        
        # Preguntar por calibración
        print("\n⚙️  ¿Deseas calibrar umbrales automáticamente?")
        print("   (Recomendado si es la primera vez o cambiaste de mesa)")
        calibrate = input("   Calibrar? (s/n): ").strip().lower()
        
        if calibrate == 's':
            self.calibrate_thresholds()
        
        print("\n" + "=" * 50)
        print("✅ SISTEMA MEJORADO LISTO")
        print("=" * 50)
        
        while True:
            print("\n🎮 COMANDOS MEJORADOS:")
            print("   [Enter] - Analizar mesa")
            print("   c       - Calibrar umbrales")
            print("   d       - Debug (guardar análisis completo)")
            print("   h       - Historial")
            print("   q       - Salir")
            
            cmd = input("\n👉 Comando: ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'c':
                self.calibrate_thresholds()
            elif cmd == 'd':
                self.save_complete_debug()
            elif cmd == 'h':
                self.show_history()
            else:
                suggestion = self.run_analysis_cycle()
                if suggestion:
                    self.show_suggestion(suggestion)
    
    def save_complete_debug(self):
        """Guardar debug completo"""
        screenshot = self.capture_table()
        if screenshot:
            self.save_detailed_analysis(screenshot, {"debug": True})
            print("✅ Debug completo guardado")
        else:
            print("❌ No se pudo capturar para debug")
    
    def show_history(self):
        """Mostrar historial"""
        if not self.hand_history:
            print("\n📭 No hay historial")
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
            if "details" in sugg:
                det = sugg["details"]
                print(f"   Detección: F{det.get('fold_strength',0):.0f}%")
                print(f"              C{det.get('call_strength',0):.0f}%")
                print(f"              R{det.get('raise_strength',0):.0f}%")

def main():
    """Función principal"""
    print("🎴 POKERSTARS IMPROVED ASSISTANT")
    print("🤖 Detección mejorada con umbrales ajustados")
    print("🎯 Calibración automática + análisis por color")
    print("-" * 50)
    
    try:
        assistant = PokerStarsImprovedAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n🛑 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n✅ Programa terminado")

if __name__ == "__main__":
    main()