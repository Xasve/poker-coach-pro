# auto_capture_system.py - Versión corregida y robusta
import os
import sys
import time
import json
from datetime import datetime

# Añadir src al path
sys.path.insert(0, "src")

# Manejo de importaciones condicionales
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️  OpenCV no disponible")

try:
    from card_detector import CardDetector
    DETECTOR_AVAILABLE = True
except ImportError as e:
    DETECTOR_AVAILABLE = False
    print(f"⚠️  CardDetector no disponible: {e}")

try:
    from auto_template_capturer import AutoTemplateCapturer
    CAPTURER_AVAILABLE = True
except ImportError as e:
    CAPTURER_AVAILABLE = False
    print(f"⚠️  Capturador no disponible: {e}")

try:
    from card_classifier import CardClassifier
    CLASSIFIER_AVAILABLE = True
except ImportError as e:
    CLASSIFIER_AVAILABLE = False
    print(f"⚠️  Clasificador no disponible: {e}")

class AutoCaptureSystem:
    """Sistema completo de captura automática - Versión robusta"""
    
    def __init__(self):
        self.mode = "BASIC"
        self.detector = None
        self.capturer = None
        self.classifier = None
        self.session_id = None
        
        # Inicializar componentes disponibles
        self.initialize_components()
    
    def initialize_components(self):
        """Inicializar componentes disponibles"""
        print("🔄 INICIALIZANDO COMPONENTES...")
        
        # Verificar configuración mínima
        config_file = "config/pokerstars_coords.json"
        if not os.path.exists(config_file):
            print("⚠️  No hay configuración de PokerStars")
            print("💡 Ejecuta: python detect_coords.py")
            self.mode = "UNCONFIGURED"
            return False
        
        # Crear carpetas necesarias
        os.makedirs("data/card_templates/pokerstars_real", exist_ok=True)
        os.makedirs("data/card_templates/auto_captured", exist_ok=True)
        
        # Inicializar componentes según disponibilidad
        if DETECTOR_AVAILABLE:
            try:
                self.detector = CardDetector()
                print("✅ Detector de cartas: OK")
            except:
                print("⚠️  Error inicializando detector")
        
        if CAPTURER_AVAILABLE:
            try:
                self.capturer = AutoTemplateCapturer()
                print("✅ Capturador automático: OK")
            except:
                print("⚠️  Error inicializando capturador")
        
        if CLASSIFIER_AVAILABLE:
            try:
                self.classifier = CardClassifier()
                print("✅ Clasificador: OK")
            except:
                print("⚠️  Error inicializando clasificador")
        
        print(f"\n🎯 MODO: {self.mode}")
        return True
    
    def show_main_menu(self):
        """Mostrar menú principal del sistema"""
        print("\n" + "=" * 60)
        print("🎴 SISTEMA DE CAPTURA AUTOMÁTICA")
        print("=" * 60)
        
        # Estado del sistema
        print("📊 ESTADO DEL SISTEMA:")
        print(f"   • Detector: {'✅' if self.detector else '❌'}")
        print(f"   • Capturador: {'✅' if self.capturer else '❌'}")
        print(f"   • Clasificador: {'✅' if self.classifier else '❌'}")
        
        print("\n🎮 OPCIONES DISPONIBLES:")
        
        # Opción 1 siempre disponible
        print("1. 📸 Captura Rápida (2 minutos)")
        
        # Otras opciones condicionales
        if self.capturer:
            print("2. 🎬 Captura Extendida (5 minutos)")
            print("3. ⏱️  Captura Personalizada")
        
        if self.classifier and self.get_session_count() > 0:
            print("4. 🎯 Clasificar Última Sesión")
            print("5. 🔄 Clasificar Todas las Sesiones")
        
        print("6. 📁 Ver Sesiones Guardadas")
        print("7. 📊 Ver Estadísticas")
        print("8. ⚙️  Configuración")
        print("9. 🚪 Volver al Menú Principal")
        print("=" * 60)
        
        try:
            choice = int(input("\n👉 Selecciona opción: "))
            return choice
        except:
            return 0
    
    def get_session_count(self):
        """Obtener número de sesiones disponibles"""
        capture_path = "data/card_templates/auto_captured"
        if not os.path.exists(capture_path):
            return 0
        
        sessions = [d for d in os.listdir(capture_path) 
                   if os.path.isdir(os.path.join(capture_path, d))]
        return len(sessions)
    
    def run_quick_capture(self):
        """Captura rápida de 2 minutos"""
        print("\n⚡ CAPTURA RÁPIDA (2 minutos)")
        print("=" * 50)
        
        if not self.capturer:
            print("❌ Capturador no disponible")
            print("💡 Instala las dependencias necesarias")
            return
        
        print("Preparando captura...")
        print("💡 Asegúrate de tener PokerStars abierto y visible")
        
        input("\nPresiona Enter para comenzar (Ctrl+C para cancelar)...")
        
        try:
            # Configurar y ejecutar captura
            self.capturer.setup_capture_folders()
            self.session_id = self.capturer.session_id
            
            print("\n🎬 CAPTURANDO...")
            print("⏱️  Duración: 2 minutos")
            print("📸 Capturando cada 2 segundos")
            
            # Captura simplificada
            self.simple_capture(120, 2)  # 120 segundos, intervalo 2s
            
            print("\n✅ Captura rápida completada")
            
            # Preguntar si clasificar
            if self.classifier:
                self.ask_classification()
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Captura cancelada")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def simple_capture(self, duration_seconds, interval):
        """Captura simplificada"""
        import mss
        
        start_time = time.time()
        capture_count = 0
        
        with mss.mss() as sct:
            # Cargar configuración
            config_file = "config/pokerstars_coords.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    mesa = config.get("pokerstars_regions", {}).get("mesa", [0,0,1920,1080])
            else:
                mesa = [0, 0, 1920, 1080]
            
            monitor = {
                "top": mesa[1],
                "left": mesa[0],
                "width": min(mesa[2], 800),
                "height": min(mesa[3], 600)
            }
            
            while time.time() - start_time < duration_seconds:
                elapsed = time.time() - start_time
                remaining = duration_seconds - elapsed
                
                print(f"\r⏱️  {int(elapsed)}s / {duration_seconds}s | 📸 {capture_count} cartas", end="")
                
                try:
                    # Capturar pantalla
                    screenshot = np.array(sct.grab(monitor))
                    
                    # Guardar cada 10 segundos
                    if capture_count % 5 == 0:
                        timestamp = datetime.now().strftime("%H%M%S_%f")[:-3]
                        filename = f"card_{capture_count:04d}_{timestamp}.png"
                        
                        raw_path = os.path.join(self.capturer.session_folder, "raw_captures", filename)
                        cv2.imwrite(raw_path, screenshot)
                        
                        capture_count += 1
                
                except Exception as e:
                    print(f"\n⚠️  Error capturando: {e}")
                
                time.sleep(interval)
        
        print(f"\n\n📊 Total capturado: {capture_count} imágenes")
    
    def run_extended_capture(self):
        """Captura extendida de 5 minutos"""
        if not self.capturer:
            print("❌ Capturador no disponible")
            return
        
        print("\n🎬 CAPTURA EXTENDIDA (5 minutos)")
        print("=" * 50)
        
        try:
            self.capturer.continuous_capture_mode(duration_seconds=300, interval=1.5)
            self.session_id = self.capturer.session_id
            
            if self.classifier:
                self.ask_classification()
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run_custom_capture(self):
        """Captura personalizada"""
        if not self.capturer:
            print("❌ Capturador no disponible")
            return
        
        print("\n⏱️  CAPTURA PERSONALIZADA")
        print("=" * 50)
        
        try:
            minutes = int(input("Duración en minutos (1-30): "))
            if 1 <= minutes <= 30:
                seconds = minutes * 60
                
                interval = float(input("Intervalo entre capturas (0.5-5 segundos): "))
                if 0.5 <= interval <= 5:
                    self.capturer.continuous_capture_mode(
                        duration_seconds=seconds,
                        interval=interval
                    )
                    self.session_id = self.capturer.session_id
                    
                    if self.classifier:
                        self.ask_classification()
                else:
                    print("❌ Intervalo fuera de rango")
            else:
                print("❌ Duración fuera de rango")
                
        except ValueError:
            print("❌ Entrada inválida")
    
    def ask_classification(self):
        """Preguntar si clasificar"""
        if not self.classifier:
            return
        
        response = input("\n¿Clasificar automáticamente las cartas? (s/n): ")
        if response.lower() == 's':
            print("🔍 Clasificando...")
            
            if self.session_id:
                results = self.classifier.auto_classify_session(self.session_id)
                if results:
                    print(f"✅ Clasificadas {len(results)} cartas")
            else:
                print("❌ No hay sesión para clasificar")
    
    def classify_last_session(self):
        """Clasificar la última sesión"""
        if not self.classifier:
            print("❌ Clasificador no disponible")
            return
        
        sessions = self.get_sessions_list()
        if not sessions:
            print("❌ No hay sesiones para clasificar")
            return
        
        last_session = sessions[-1]  # La más reciente
        print(f"\n🎯 CLASIFICANDO SESIÓN: {last_session['id']}")
        
        results = self.classifier.auto_classify_session(last_session["id"])
        if results:
            print(f"✅ Clasificadas {len(results)} cartas")
    
    def classify_all_sessions(self):
        """Clasificar todas las sesiones"""
        if not self.classifier:
            print("❌ Clasificador no disponible")
            return
        
        sessions = self.get_sessions_list()
        if not sessions:
            print("❌ No hay sesiones para clasificar")
            return
        
        print(f"\n🔄 CLASIFICANDO {len(sessions)} SESIONES...")
        
        for session in sessions:
            print(f"\n📁 Sesión: {session['id']}")
            results = self.classifier.auto_classify_session(session["id"])
            if results:
                print(f"   ✅ {len(results)} cartas clasificadas")
        
        print("\n🎉 ¡Todas las sesiones clasificadas!")
    
    def get_sessions_list(self):
        """Obtener lista de sesiones"""
        capture_path = "data/card_templates/auto_captured"
        if not os.path.exists(capture_path):
            return []
        
        sessions = []
        for item in sorted(os.listdir(capture_path)):
            session_path = os.path.join(capture_path, item)
            if os.path.isdir(session_path):
                # Contar cartas
                raw_path = os.path.join(session_path, "raw_captures")
                card_count = 0
                if os.path.exists(raw_path):
                    card_count = len([f for f in os.listdir(raw_path) 
                                    if f.endswith('.png')])
                
                sessions.append({
                    "id": item,
                    "path": session_path,
                    "cards": card_count
                })
        
        return sessions
    
    def view_sessions(self):
        """Ver sesiones guardadas"""
        print("\n📁 SESIONES DE CAPTURA")
        print("=" * 50)
        
        sessions = self.get_sessions_list()
        
        if not sessions:
            print("📭 No hay sesiones de captura")
            print("\n💡 Ejecuta una captura primero")
            return
        
        print(f"📊 Total: {len(sessions)} sesiones")
        print("\n📋 LISTA:")
        print("-" * 50)
        
        total_cards = 0
        for i, session in enumerate(sessions, 1):
            print(f"{i:2}. {session['id']:20} {session['cards']:3} cartas")
            total_cards += session["cards"]
        
        print("-" * 50)
        print(f"   TOTAL CARTAS: {total_cards}")
        
        # Mostrar opciones
        if sessions and self.classifier:
            print("\n🎯 OPCIONES:")
            print("   c - Clasificar última sesión")
            print("   a - Clasificar todas")
            print("   número - Seleccionar sesión específica")
            
            choice = input("\n👉 Opción (Enter para volver): ")
            
            if choice.lower() == 'c':
                self.classify_last_session()
            elif choice.lower() == 'a':
                self.classify_all_sessions()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sessions):
                    session_id = sessions[idx]["id"]
                    print(f"\n🔍 Procesando sesión: {session_id}")
                    self.classifier.auto_classify_session(session_id)
    
    def show_statistics(self):
        """Mostrar estadísticas"""
        print("\n📊 ESTADÍSTICAS DEL SISTEMA")
        print("=" * 50)
        
        # Templates organizados
        templates_path = "data/card_templates/pokerstars_real"
        template_count = 0
        suit_counts = {}
        
        if os.path.exists(templates_path):
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            for suit in suits:
                suit_path = os.path.join(templates_path, suit)
                if os.path.exists(suit_path):
                    count = len([f for f in os.listdir(suit_path) 
                               if f.endswith(('.png', '.jpg', '.jpeg'))])
                    suit_counts[suit] = count
                    template_count += count
        
        print("\n🎴 TEMPLATES ORGANIZADOS:")
        if template_count > 0:
            for suit, count in suit_counts.items():
                if count > 0:
                    print(f"   {suit.upper():10} {count:3}")
            print(f"\n   TOTAL:      {template_count:3}")
        else:
            print("   📭 No hay templates organizados")
        
        # Sesiones de captura
        sessions = self.get_sessions_list()
        print(f"\n📁 SESIONES DE CAPTURA: {len(sessions)}")
        
        if sessions:
            total_cards = sum(s["cards"] for s in sessions)
            print(f"   📸 Total cartas capturadas: {total_cards}")
            print(f"   📈 Promedio por sesión: {total_cards // len(sessions) if sessions else 0}")
        
        # Evaluación
        print("\n📈 EVALUACIÓN:")
        if template_count >= 100:
            print("   ✅ EXCELENTE: Más de 100 templates")
            print("   🎯 El sistema de reconocimiento debería funcionar bien")
        elif template_count >= 20:
            print("   📊 BUENO: Más de 20 templates")
            print("   💡 Podría mejorar con más capturas")
        elif template_count > 0:
            print("   ⚠️  MÍNIMO: Menos de 20 templates")
            print("   🔄 Se recomienda capturar más cartas")
        else:
            print("   ❌ INSUFICIENTE: No hay templates")
            print("   🚀 Ejecuta capturas para comenzar")
    
    def show_configuration(self):
        """Mostrar y ajustar configuración"""
        print("\n⚙️  CONFIGURACIÓN")
        print("=" * 50)
        
        config_file = "config/pokerstars_coords.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print("✅ Configuración cargada:")
            print(f"   Resolución: {config.get('screen_resolution', 'Desconocida')}")
            print(f"   Detectada: {config.get('detected_at', 'Desconocido')}")
            
            regions = config.get("pokerstars_regions", {})
            print(f"   Regiones configuradas: {len(regions)}")
        else:
            print("❌ No hay configuración")
            print("\n💡 Para configurar:")
            print("   1. Abre PokerStars en una mesa")
            print("   2. Ejecuta: python detect_coords.py")
        
        print("\n🔧 OPCIONES:")
        print("   1. Re-detectar PokerStars")
        print("   2. Ver configuración detallada")
        print("   3. Volver")
        
        try:
            choice = int(input("\n👉 Opción: "))
            
            if choice == 1:
                print("\n🔍 Redetectando PokerStars...")
                os.system("python detect_coords.py")
            elif choice == 2:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        print("\n📄 CONFIGURACIÓN DETALLADA:")
                        print(json.dumps(json.load(f), indent=2))
                input("\nPresiona Enter para continuar...")
                
        except:
            print("❌ Entrada inválida")
    
    def run(self):
        """Ejecutar sistema principal"""
        print("🎴 SISTEMA DE CAPTURA AUTOMÁTICA")
        print("=" * 70)
        
        # Verificar estado inicial
        if self.mode == "UNCONFIGURED":
            print("\n⚠️  Sistema no configurado")
            print("💡 Ejecuta primero: python detect_coords.py")
            response = input("¿Ejecutar ahora? (s/n): ")
            if response.lower() == 's':
                os.system("python detect_coords.py")
            else:
                return
        
        # Bucle principal
        while True:
            choice = self.show_main_menu()
            
            if choice == 1:
                self.run_quick_capture()
            elif choice == 2 and self.capturer:
                self.run_extended_capture()
            elif choice == 3 and self.capturer:
                self.run_custom_capture()
            elif choice == 4 and self.classifier:
                self.classify_last_session()
            elif choice == 5 and self.classifier:
                self.classify_all_sessions()
            elif choice == 6:
                self.view_sessions()
            elif choice == 7:
                self.show_statistics()
            elif choice == 8:
                self.show_configuration()
            elif choice == 9:
                print("\n👋 Volviendo al menú principal...")
                break
            else:
                print("\n❌ Opción inválida o no disponible")
            
            if choice != 9:
                input("\nPresiona Enter para continuar...")

def main():
    """Punto de entrada principal"""
    try:
        system = AutoCaptureSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Sistema interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
