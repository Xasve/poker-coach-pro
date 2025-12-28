# auto_capture_system.py - VERSIÓN CON MEJOR INTEGRACIÓN
import os
import sys
import time
import json
from datetime import datetime

# Añadir src al path
sys.path.insert(0, "src")

# Manejo de importaciones
try:
    from card_detector import CardDetector
    DETECTOR_AVAILABLE = True
except ImportError as e:
    DETECTOR_AVAILABLE = False
    print(f"  CardDetector no disponible: {e}")

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
    print(f"  Clasificador no disponible: {e}")

class AutoCaptureSystem:
    """Sistema completo de captura automática - VERSIÓN MEJORADA"""
    
    def __init__(self):
        self.session_id = None
        self.capturer = None
        self.classifier = None
        
        self.initialize_system()
    
    def initialize_system(self):
        """Inicializar sistema"""
        print("🔄 INICIALIZANDO SISTEMA...")
        
        # Verificar configuración
        config_file = "config/pokerstars_coords.json"
        if not os.path.exists(config_file):
            print("⚠️  No hay configuración de PokerStars")
            print("💡 Ejecuta: python detect_coords.py")
            print("   O usa pantalla completa (modo básico)")
        
        # Crear carpetas necesarias
        self.create_required_folders()
        
        # Inicializar componentes
        if CAPTURER_AVAILABLE:
            try:
                self.capturer = AutoTemplateCapturer()
                print(" Capturador: LISTO")
            except Exception as e:
                print(f"  Error inicializando capturador: {e}")
        
        if CLASSIFIER_AVAILABLE:
            try:
                self.classifier = CardClassifier()
                print(" Clasificador: LISTO")
            except Exception as e:
                print(f"  Error inicializando clasificador: {e}")
        
        print(f"\n SISTEMA INICIALIZADO")
        print(f"   Capturador: {'' if self.capturer else ''}")
        print(f"   Clasificador: {'' if self.classifier else ''}")
    
    def create_required_folders(self):
        """Crear carpetas necesarias"""
        folders = [
            "data/card_templates/pokerstars_real",
            "data/card_templates/pokerstars_real/hearts",
            "data/card_templates/pokerstars_real/diamonds",
            "data/card_templates/pokerstars_real/clubs",
            "data/card_templates/pokerstars_real/spades",
            "data/card_templates/auto_captured",
            "logs",
            "debug"
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        print("\n" + "=" * 60)
        print(" SISTEMA DE CAPTURA AUTOMÁTICA")
        print("=" * 60)
        
        # Información de estado
        sessions_count = self.count_sessions()
        templates_count = self.count_templates()
        
        print(f" ESTADO ACTUAL:")
        print(f"    Sesiones: {sessions_count}")
        print(f"    Templates: {templates_count}")
        
        print("\n OPCIONES PRINCIPALES:")
        print("1.  Captura Rápida (2 minutos)")
        
        if self.capturer:
            print("2.  Captura Extendida (5 minutos)")
            print("3.   Captura Personalizada")
        
        if self.classifier and sessions_count > 0:
            print("4.  Clasificar Última Sesión")
            print("5.  Clasificar Todas las Sesiones")
        
        print("6.  Ver Sesiones Guardadas")
        print("7.  Ver Estadísticas Completas")
        print("8.  Diagnóstico del Sistema")
        print("9.   Configuración y Ayuda")
        print("0.  Volver al Menú Principal")
        print("=" * 60)
        
        try:
            choice = input("\n Selecciona opción: ")
            return int(choice) if choice.isdigit() else 0
        except:
            return 0
    
    def count_sessions(self):
        """Contar sesiones disponibles"""
        base_path = "data/card_templates/auto_captured"
        if not os.path.exists(base_path):
            return 0
        
        sessions = [d for d in os.listdir(base_path) 
                if os.path.isdir(os.path.join(base_path, d))]
        return len(sessions)
    
    def count_templates(self):
        """Contar templates organizados"""
        base_path = "data/card_templates/pokerstars_real"
        if not os.path.exists(base_path):
            return 0
        
        total = 0
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for suit in suits:
            suit_path = os.path.join(base_path, suit)
            if os.path.exists(suit_path):
                count = len([f for f in os.listdir(suit_path) 
                        if f.endswith(('.png', '.jpg', '.jpeg'))])
                total += count
        
        return total
    
    def run_quick_capture(self):
        """Captura rápida mejorada"""
        if not self.capturer:
            print(" Capturador no disponible")
            return
        
        print("\n" + "=" * 60)
        print(" CAPTURA RÁPIDA MEJORADA")
        print("=" * 60)
        
        print(" INSTRUCCIONES:")
        print("   1. Abre PokerStars en una mesa")
        print("   2. Asegúrate que la ventana sea VISIBLE")
        print("   3. No minimices la ventana")
        print("   4. Presiona Enter para comenzar")
        
        input("\n Presiona Enter cuando estés listo (Ctrl+C para cancelar)...")
        
        try:
            print("\n INICIANDO CAPTURA...")
            
            # Ejecutar captura
            self.capturer.simple_capture_mode(duration_seconds=120, interval=2)
            
            # Obtener ID de sesión
            self.session_id = self.capturer.session_id
            
            print(f"\n CAPTURA COMPLETADA")
            print(f"    Sesión: {self.session_id}")
            print(f"    Imágenes: {self.capturer.captured_count}")
            
            # Preguntar por clasificación automática
            if self.classifier and self.capturer.captured_count > 0:
                self.ask_auto_classification()
                
        except KeyboardInterrupt:
            print("\n\n  Captura cancelada por usuario")
        except Exception as e:
            print(f"\n Error durante captura: {e}")
    
    def ask_auto_classification(self):
        """Preguntar por clasificación automática"""
        if not self.classifier or not self.session_id:
            return
        
        print("\n" + "=" * 50)
        response = input("Clasificar automáticamente las imágenes capturadas? (s/n): ")
        
        if response.lower() == 's':
            print(" Iniciando clasificación...")
            
            # Dar un pequeño tiempo para que se guarden todos los archivos
            time.sleep(1)
            
            # Clasificar sesión
            success = self.classify_session(self.session_id)
            
            if success:
                print(" Clasificación completada exitosamente")
            else:
                print(" Error en clasificación")
                print(" Puedes intentar clasificar manualmente más tarde")
    
    def classify_session(self, session_id):
        """Clasificar una sesión específica"""
        if not self.classifier:
            print(" Clasificador no disponible")
            return False
        
        try:
            print(f"\n CLASIFICANDO SESIÓN: {session_id}")
            
            # Buscar sesión en el clasificador
            session = self.classifier.get_session_by_id(session_id)
            
            if not session:
                print(f" Sesión no encontrada en clasificador: {session_id}")
                print(" El clasificador buscará automáticamente...")
            
            # Ejecutar clasificación
            results = self.classifier.auto_classify_session(session_id)
            
            if results:
                print(f" {len(results)} imágenes clasificadas")
                return True
            else:
                print(" No se pudieron clasificar imágenes")
                return False
                
        except Exception as e:
            print(f" Error clasificando sesión: {e}")
            return False
    
    def classify_latest_session(self):
        """Clasificar la sesión más reciente"""
        if not self.classifier:
            print(" Clasificador no disponible")
            return
        
        # Obtener sesión más reciente
        latest = self.classifier.get_latest_session()
        
        if not latest:
            print(" No hay sesiones para clasificar")
            return
        
        print(f"\n CLASIFICANDO SESIÓN MÁS RECIENTE:")
        print(f"    {latest['id']}")
        print(f"    {latest['card_count']} imágenes")
        
        self.classify_session(latest["id"])
    
    def classify_all_sessions(self):
        """Clasificar todas las sesiones"""
        if not self.classifier:
            print(" Clasificador no disponible")
            return
        
        sessions = self.get_valid_sessions()
        
        if not sessions:
            print(" No hay sesiones válidas para clasificar")
            return
        
        print(f"\n CLASIFICANDO {len(sessions)} SESIONES...")
        
        for session in sessions:
            print(f"\n{'='*50}")
            print(f" Sesión: {session['id']} ({session['card_count']} imágenes)")
            
            self.classify_session(session["id"])
            
            # Pequeña pausa entre sesiones
            time.sleep(1)
        
        print("\n Todas las sesiones clasificadas!")
    
    def get_valid_sessions(self):
        """Obtener sesiones válidas para clasificación"""
        if not self.classifier:
            return []
        
        return [s for s in self.classifier.sessions if s["card_count"] > 0]
    
    def view_sessions(self):
        """Ver sesiones guardadas"""
        print("\n" + "=" * 60)
        print(" SESIONES DE CAPTURA GUARDADAS")
        print("=" * 60)
        
        sessions = self.get_valid_sessions()
        
        if not sessions:
            print("�� No hay sesiones de captura")
            print("\n💡 Ejecuta una captura primero (opción 1)")
            return
        
        print(f"📊 Total sesiones: {len(sessions)}")
        print("\n📋 LISTA DE SESIONES (más recientes primero):")
        print("-" * 60)
        
        total_images = 0
        for i, session in enumerate(sessions[:10], 1):  # Mostrar primeras 10
            print(f"{i:2}. {session['id']} - {session['card_count']:3} imágenes")
            total_images += session["card_count"]
        
        if len(sessions) > 10:
            print(f"   ... y {len(sessions) - 10} sesiones más")
        
        print("-" * 60)
        print(f" Total imágenes capturadas: {total_images}")
        
        # Opciones adicionales
        if sessions and self.classifier:
            print("\n OPCIONES:")
            print("   n - Clasificar por número (ej: 1 para la primera)")
            print("   u - Clasificar la más reciente")
            print("   a - Clasificar todas")
            print("   Enter - Volver al menú")
            
            choice = input("\n👉 Opción: ").strip().lower()
            
            if choice == 'u':
                self.classify_latest_session()
            elif choice == 'a':
                self.classify_all_sessions()
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sessions):
                    self.classify_session(sessions[idx]["id"])
                else:
                    print(" Número fuera de rango")
    
    def show_statistics(self):
        """Mostrar estadísticas completas"""
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS COMPLETAS DEL SISTEMA")
        print("=" * 60)
        
        # Templates organizados
        print("\n TEMPLATES ORGANIZADOS:")
        templates_path = "data/card_templates/pokerstars_real"
        
        if os.path.exists(templates_path):
            suits = ['hearts', 'diamonds', 'clubs', 'spades']
            suit_counts = {}
            total_templates = 0
            
            for suit in suits:
                suit_path = os.path.join(templates_path, suit)
                if os.path.exists(suit_path):
                    count = len([f for f in os.listdir(suit_path) 
                            if f.endswith(('.png', '.jpg', '.jpeg'))])
                    suit_counts[suit] = count
                    total_templates += count
            
            if total_templates > 0:
                for suit, count in suit_counts.items():
                    if count > 0:
                        percentage = (count / total_templates) * 100
                        print(f"   {suit.upper():10} {count:3} ({percentage:.1f}%)")
                
                print(f"\n    TOTAL:      {total_templates:3}")
                
                # Evaluación
                if total_templates >= 100:
                    print("    EXCELENTE para reconocimiento")
                elif total_templates >= 50:
                    print("    BUENO para pruebas")
                elif total_templates >= 20:
                    print("     MÍNIMO aceptable")
                else:
                    print("    INSUFICIENTE, captura más cartas")
            else:
                print("    No hay templates organizados")
        else:
            print("    Carpeta no existe")
        
        # Sesiones de captura
        print("\n SESIONES DE CAPTURA:")
        sessions = self.get_valid_sessions()
        
        if sessions:
            total_sessions = len(sessions)
            total_images = sum(s["card_count"] for s in sessions)
            avg_images = total_images / total_sessions if total_sessions > 0 else 0
            
            print(f"    Sesiones:     {total_sessions:3}")
            print(f"    Imágenes:     {total_images:3}")
            print(f"    Promedio/sesión: {avg_images:.1f}")
            
            # Última sesión
            if sessions:
                latest = sessions[0]
                print(f"    Última sesión: {latest['id']} ({latest['card_count']} imágenes)")
        else:
            print("    No hay sesiones")
        
        # Recomendaciones
        print("\n RECOMENDACIONES:")
        
        templates_needed = max(0, 50 - self.count_templates())
        if templates_needed > 0:
            print(f"   1.  Captura al menos {templates_needed} cartas más")
        
        if sessions:
            unclassified = [s for s in sessions if not os.path.exists(os.path.join(s["path"], "classification_results.json"))]
            if unclassified:
                print(f"   2.  Clasifica {len(unclassified)} sesiones pendientes")
        
        print("   3.  Usa diferentes mesas/styles en PokerStars")
    
    def run_diagnosis(self):
        """Ejecutar diagnóstico del sistema"""
        print("\n" + "=" * 60)
        print(" DIAGNÓSTICO DEL SISTEMA")
        print("=" * 60)
        
        print("Ejecutando diagnóstico completo...")
        
        # Importar y ejecutar diagnóstico
        try:
            import subprocess
            subprocess.run([sys.executable, "diagnose_sessions.py"])
        except Exception as e:
            print(f" Error ejecutando diagnóstico: {e}")
            print("\n Ejecuta manualmente: python diagnose_sessions.py")
    
    def show_configuration_help(self):
        """Mostrar configuración y ayuda"""
        print("\n" + "=" * 60)
        print("  CONFIGURACIÓN Y AYUDA")
        print("=" * 60)
        
        print("\n CONFIGURACIÓN ACTUAL:")
        
        config_file = "config/pokerstars_coords.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                print(f"    Configuración cargada")
                print(f"    Resolución: {config.get('screen_resolution', 'Desconocida')}")
                print(f"    Detectada: {config.get('detected_at', 'Desconocido')}")
            except:
                print("    Error leyendo configuración")
        else:
            print("    No hay configuración")
            print("\n Para configurar:")
            print("   1. Abre PokerStars")
            print("   2. Ejecuta: python detect_coords.py")
        
        print("\n FLUJO DE TRABAJO RECOMENDADO:")
        print("   1.   Configura PokerStars (si no está configurado)")
        print("   2.  Captura cartas (opción 1)")
        print("   3.  Clasifica automáticamente")
        print("   4.  Repite para diferentes cartas/posiciones")
        
        print("\n SOLUCIÓN DE PROBLEMAS:")
        print("    Si no detecta PokerStars: verifica ventana visible")
        print("    Si no captura: aumenta brillo/contraste de mesa")
        print("    Si no clasifica: verifica diagnose_sessions.py")
        
        input("\n Presiona Enter para volver...")
    
    def run(self):
        """Ejecutar sistema principal"""
        print(" SISTEMA DE CAPTURA AUTOMÁTICA - VERSIÓN MEJORADA")
        print("=" * 70)
        
        while True:
            choice = self.show_main_menu()
            
            if choice == 1:
                self.run_quick_capture()
            elif choice == 2 and self.capturer:
                print("\n Captura extendida (próximamente)")
                # self.run_extended_capture()
            elif choice == 3 and self.capturer:
                print("\n Captura personalizada (próximamente)")
                # self.run_custom_capture()
            elif choice == 4 and self.classifier:
                self.classify_latest_session()
            elif choice == 5 and self.classifier:
                self.classify_all_sessions()
            elif choice == 6:
                self.view_sessions()
            elif choice == 7:
                self.show_statistics()
            elif choice == 8:
                self.run_diagnosis()
            elif choice == 9:
                self.show_configuration_help()
            elif choice == 0:
                print("\n Volviendo al menú principal...")
                break
            else:
                print("\n Opción no válida o no disponible")
            
            if choice != 0:
                input("\n Presiona Enter para continuar...")

def main():
    """Función principal"""
    try:
        system = AutoCaptureSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n  Sistema interrumpido por usuario")
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        print(" Ejecuta: python diagnose_sessions.py para diagnóstico")

if __name__ == "__main__":
    main()
