# auto_capture_system.py - Sistema completo unificado
import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Añadir src al path
sys.path.insert(0, "src")

from card_detector import CardDetector
from auto_template_capturer import AutoTemplateCapturer
from card_classifier import CardClassifier

class AutoCaptureSystem:
    """Sistema completo de captura automática"""
    
    def __init__(self):
        self.mode = "FULL_AUTO"
        self.detector = None
        self.capturer = None
        self.classifier = None
        self.session_id = None
        
    def initialize_components(self):
        """Inicializar todos los componentes"""
        print(" Inicializando componentes...")
        
        # Verificar configuración
        if not os.path.exists("config/pokerstars_coords.json"):
            print(" No hay configuración de PokerStars")
            print("   Ejecuta primero: python detect_coords.py")
            return False
        
        # Inicializar componentes
        self.detector = CardDetector()
        self.capturer = AutoTemplateCapturer()
        self.classifier = CardClassifier()
        
        print(" Componentes inicializados")
        return True
    
    def capture_mode_menu(self):
        """Mostrar menú de modos de captura"""
        print("\n SISTEMA DE CAPTURA AUTOMÁTICA")
        print("=" * 60)
        print("Selecciona el modo de captura:")
        print("1.  Captura Continua (5 minutos)")
        print("2.   Captura por Tiempo (configurable)")
        print("3.  Captura por Cantidad (N cartas)")
        print("4.  Detección Inteligente (solo detecta)")
        print("5.  Procesar Sesión Existente")
        print("6.  Generar Reportes")
        print("7.  Salir")
        
        try:
            choice = int(input("\nOpción (1-7): "))
            return choice
        except ValueError:
            return 0
    
    def run_continuous_capture(self, duration_minutes=5):
        """Ejecutar captura continua"""
        print(f"\n INICIANDO CAPTURA CONTINUA")
        print(f"   Duración: {duration_minutes} minutos")
        print("   Asegúrate de tener PokerStars abierto y visible")
        print("   Presiona Ctrl+C para detener antes de tiempo")
        print("=" * 50)
        
        # Iniciar captura
        duration_seconds = duration_minutes * 60
        self.capturer.continuous_capture_mode(
            duration_seconds=duration_seconds,
            interval=1.5  # Captura cada 1.5 segundos
        )
        
        # Obtener ID de sesión
        self.session_id = self.capturer.session_id
        
        # Preguntar si clasificar automáticamente
        if self.session_id:
            self.ask_for_classification()
    
    def run_timed_capture(self):
        """Captura por tiempo configurable"""
        try:
            minutes = int(input("\n  Duración en minutos (1-60): "))
            if 1 <= minutes <= 60:
                self.run_continuous_capture(minutes)
            else:
                print(" Duración fuera de rango")
        except ValueError:
            print(" Entrada inválida")
    
    def run_quantity_capture(self):
        """Captura hasta obtener N cartas"""
        try:
            target_cards = int(input("\n Cantidad de cartas a capturar (10-1000): "))
            if 10 <= target_cards <= 1000:
                print(f"\n Objetivo: {target_cards} cartas")
                print("   El sistema capturará hasta alcanzar el objetivo")
                print("   Puede tomar varios minutos...")
                
                # Implementar captura por cantidad
                self.capture_until_quantity(target_cards)
            else:
                print(" Cantidad fuera de rango")
        except ValueError:
            print(" Entrada inválida")
    
    def capture_until_quantity(self, target_quantity):
        """Capturar hasta alcanzar una cantidad específica"""
        if not self.capturer:
            self.capturer = AutoTemplateCapturer()
        
        self.capturer.setup_capture_folders()
        start_time = time.time()
        
        try:
            while self.capturer.captured_count < target_quantity:
                elapsed_minutes = (time.time() - start_time) / 60
                print(f"\n Cartas: {self.capturer.captured_count}/{target_quantity}")
                print(f"   Tiempo: {elapsed_minutes:.1f} minutos")
                
                # Capturar una iteración
                screenshot = self.capturer.capture_table_screenshot()
                if screenshot is None:
                    print("    Fallo captura, reintentando...")
                    time.sleep(2)
                    continue
                
                candidates = self.capturer.detect_card_candidates(screenshot)
                
                for candidate in candidates:
                    if self.capturer.captured_count >= target_quantity:
                        break
                    
                    card_img = candidate["image"]
                    mean_brightness = np.mean(cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY))
                    
                    if 30 < mean_brightness < 220:
                        self.capturer.save_card_candidate(card_img, candidate)
                
                # Si no hay progreso, esperar un poco
                if len(candidates) == 0:
                    print("   ⏸️  No se detectaron cartas, esperando...")
                    time.sleep(3)
                else:
                    time.sleep(1)
                
                # Timeout de seguridad (10 minutos máximo)
                if elapsed_minutes > 10:
                    print(" Timeout alcanzado (10 minutos)")
                    break
        
        except KeyboardInterrupt:
            print("\n\n  Captura interrumpida")
        
        finally:
            self.session_id = self.capturer.session_id
            self.capturer.generate_session_report()
            
            if self.capturer.captured_count > 0:
                self.ask_for_classification()
    
    def ask_for_classification(self):
        """Preguntar si clasificar automáticamente"""
        print("\n" + "=" * 50)
        response = input("¿Clasificar automáticamente las cartas capturadas? (s/n): ")
        
        if response.lower() == 's':
            print("🔍 Iniciando clasificación automática...")
            self.classify_captured_cards()
    
    def classify_captured_cards(self):
        """Clasificar cartas capturadas"""
        if not self.session_id:
            print("❌ No hay sesión para clasificar")
            return
        
        if not self.classifier:
            self.classifier = CardClassifier()
        
        # Clasificar la sesión actual
        results = self.classifier.auto_classify_session(self.session_id)
        
        if results:
            print(f"\n Clasificación completada: {len(results)} cartas")
            
            # Generar reporte visual
            print(" Generando reporte visual...")
            self.classifier.generate_clustering_report(self.session_id)
            
            # Mostrar resumen
            self.show_classification_summary(results)
    
    def show_classification_summary(self, results):
        """Mostrar resumen de clasificación"""
        suits_count = {}
        for card in results:
            suit = card.get("suit", "unknown")
            suits_count[suit] = suits_count.get(suit, 0) + 1
        
        print("\n RESUMEN DE CLASIFICACIÓN:")
        print("=" * 40)
        
        total = len(results)
        for suit, count in suits_count.items():
            percentage = (count / total) * 100
            print(f"   {suit.upper():10} {count:3} cartas ({percentage:.1f}%)")
        
        print(f"\n   TOTAL:      {total:3} cartas")
        
        # Guardar resumen
        summary = {
            "session_id": self.session_id,
            "classification_date": str(datetime.now()),
            "total_cards": total,
            "suits_distribution": suits_count,
            "unknown_values": sum(1 for c in results if c.get("value") == "unknown")
        }
        
        summary_path = f"data/card_templates/auto_captured/{self.session_id}/classification_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n Resumen guardado: {summary_path}")
    
    def process_existing_session(self):
        """Procesar una sesión existente"""
        classifier = CardClassifier()
        
        if not classifier.sessions:
            print(" No hay sesiones disponibles")
            return
        
        print("\n SESIONES DISPONIBLES:")
        for i, session in enumerate(classifier.sessions):
            # Contar cartas en la sesión
            raw_path = os.path.join(session["path"], "raw_captures")
            card_count = len([f for f in os.listdir(raw_path) 
                            if f.endswith('.png')]) if os.path.exists(raw_path) else 0
            
            print(f"   {i+1}. {session['id']} ({card_count} cartas)")
        
        try:
            choice = int(input("\nSelecciona sesión (número): "))
            if 1 <= choice <= len(classifier.sessions):
                session_id = classifier.sessions[choice-1]["id"]
                self.session_id = session_id
                
                # Clasificar
                print(f"\n Clasificando sesión: {session_id}")
                results = classifier.auto_classify_session(session_id)
                
                if results:
                    self.show_classification_summary(results)
                    classifier.generate_clustering_report(session_id)
            else:
                print(" Selección inválida")
        except ValueError:
            print(" Entrada inválida")
    
    def generate_reports(self):
        """Generar reportes del sistema"""
        print("\n GENERACIÓN DE REPORTES")
        print("=" * 50)
        
        # Contar templates existentes
        templates_path = "data/card_templates/pokerstars_real"
        total_templates = 0
        suit_counts = {}
        
        if os.path.exists(templates_path):
            for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
                suit_path = os.path.join(templates_path, suit)
                if os.path.exists(suit_path):
                    count = len([f for f in os.listdir(suit_path) 
                               if f.endswith(('.png', '.jpg', '.jpeg'))])
                    suit_counts[suit] = count
                    total_templates += count
        
        print("\n ESTADÍSTICAS DE TEMPLATES:")
        print("=" * 40)
        for suit, count in suit_counts.items():
            print(f"   {suit.upper():10} {count:3} templates")
        
        print(f"\n   TOTAL:      {total_templates:3} templates")
        
        # Contar sesiones de captura
        capture_path = "data/card_templates/auto_captured"
        session_count = 0
        total_captured = 0
        
        if os.path.exists(capture_path):
            for item in os.listdir(capture_path):
                session_dir = os.path.join(capture_path, item)
                if os.path.isdir(session_dir):
                    session_count += 1
                    
                    # Contar cartas en esta sesión
                    raw_path = os.path.join(session_dir, "raw_captures")
                    if os.path.exists(raw_path):
                        card_count = len([f for f in os.listdir(raw_path) 
                                        if f.endswith('.png')])
                        total_captured += card_count
        
        print(f"\n SESIONES DE CAPTURA:")
        print(f"   Sesiones:   {session_count}")
        print(f"   Cartas totales capturadas: {total_captured}")
        
        # Guardar reporte general
        report = {
            "report_date": str(datetime.now()),
            "templates": {
                "total": total_templates,
                "by_suit": suit_counts
            },
            "capture_sessions": {
                "total_sessions": session_count,
                "total_captured_cards": total_captured,
                "average_per_session": total_captured / session_count if session_count > 0 else 0
            },
            "system_status": "ACTIVE"
        }
        
        report_path = "logs/capture_system_report.json"
        os.makedirs("logs", exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n Reporte guardado: {report_path}")
    
    def run(self):
        """Ejecutar sistema principal"""
        if not self.initialize_components():
            return
        
        while True:
            choice = self.capture_mode_menu()
            
            if choice == 1:
                self.run_continuous_capture(5)
            elif choice == 2:
                self.run_timed_capture()
            elif choice == 3:
                self.run_quantity_capture()
            elif choice == 4:
                print("\n Modo detección inteligente (próximamente)")
                print("   Este modo solo detecta cartas sin capturarlas")
            elif choice == 5:
                self.process_existing_session()
            elif choice == 6:
                self.generate_reports()
            elif choice == 7:
                print("\n Hasta pronto!")
                break
            else:
                print(" Opción inválida")
            
            input("\nPresiona Enter para continuar...")

# Función principal
def main():
    """Punto de entrada principal"""
    print(" POKER COACH PRO - SISTEMA DE CAPTURA AUTOMÁTICA")
    print("=" * 70)
    
    system = AutoCaptureSystem()
    system.run()

if __name__ == "__main__":
    main()
