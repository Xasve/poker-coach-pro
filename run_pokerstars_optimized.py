# run_pokerstars_optimized.py - Sistema completo optimizado (CORREGIDO)
import sys
import os
import time
import json
from datetime import datetime

print("🚀 POKER COACH PRO - SISTEMA COMPLETO OPTIMIZADO")
print("=" * 60)

sys.path.insert(0, 'src')

class PokerCoachPro:
    def __init__(self, platform="pokerstars", stealth_level=2):
        self.platform = platform
        self.stealth_level = stealth_level
        self.running = False
        
        # Estadísticas
        self.stats = {
            "start_time": None,
            "captures": 0,
            "tables_detected": 0,
            "hands_analyzed": 0,  # 🔥 CORREGIDO: era 'hands_analizadas'
            "recommendations_given": 0
        }
        
        # Cargar configuración
        self.config = self.load_config()
        
        print(f"🎴 Inicializando Poker Coach Pro para {platform}...")
        
    def load_config(self):
        """Cargar configuración desde archivos"""
        config = {
            "stealth_level": self.stealth_level,
            "confidence_threshold": 0.7,
            "min_table_detections": 3,
            "save_debug_images": True
        }
        
        # Intentar cargar configuración desde archivo
        config_path = "config/settings.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                    print("✅ Configuración cargada desde archivo")
            except:
                print("⚠️  No se pudo cargar configuración, usando defaults")
        
        return config
    
    def initialize_components(self):
        """Inicializar todos los componentes del sistema"""
        try:
            from platforms.pokerstars_adapter import PokerStarsAdapter
            from integration.coach_integrator import CoachIntegrator
            
            self.adapter = PokerStarsAdapter(
                stealth_level=self.config["stealth_level"]
            )
            
            self.coach = CoachIntegrator(platform=self.platform)
            
            print("✅ Todos los componentes inicializados")
            return True
            
        except ImportError as e:
            print(f"❌ Error importando componentes: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inicializando: {e}")
            return False
    
    def run(self):
        """Ejecutar el sistema principal"""
        if not self.initialize_components():
            print("❌ No se pudieron inicializar componentes")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now().isoformat()  # 🔥 Usar string ISO
        
        print(f"\n🔧 CONFIGURACIÓN:")
        print(f"   Plataforma: {self.platform}")
        print(f"   Nivel sigilo: {self.stealth_level}")
        print(f"   Delay captura: {self.adapter.capture_delay}s")
        print(f"   Umbral confianza: {self.config['confidence_threshold']}")
        
        print("\n🎯 INSTRUCCIONES:")
        print("1. Abre PokerStars y siéntate en una mesa")
        print("2. Asegúrate de que la mesa sea visible")
        print("3. El sistema analizará automáticamente")
        print("4. Presiona Ctrl+C para detener")
        print("\n⏳ Iniciando en 3 segundos...")
        time.sleep(3)
        
        print("\n📡 INICIANDO ANÁLISIS EN TIEMPO REAL...")
        print("-" * 50)
        
        # Variables para estado del juego
        consecutive_detections = 0
        
        try:
            while self.running:
                self.stats["captures"] += 1
                
                # Capturar pantalla
                screenshot = self.adapter.capture_table()
                if screenshot is None:
                    time.sleep(0.5)
                    continue
                
                # Detectar mesa
                table_detected = self.adapter.detect_table(screenshot)
                
                if table_detected:
                    consecutive_detections += 1
                    self.stats["tables_detected"] += 1
                    
                    print(f"✅ Mesa detectada ({consecutive_detections}/{self.config['min_table_detections']})")
                    
                    # Solo analizar después de varias detecciones consecutivas
                    if consecutive_detections >= self.config["min_table_detections"]:
                        self.analyze_table(screenshot)
                        consecutive_detections = 0  # Resetear después de analizar
                
                else:
                    consecutive_detections = 0
                    if self.stats["captures"] % 10 == 0:
                        print(f"   🔍 Buscando mesa... ({self.stats['captures']} capturas)")
                
                # Delay entre iteraciones
                time.sleep(self.adapter.capture_delay)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema detenido por el usuario")
        except Exception as e:
            print(f"\n⚠️  Error durante ejecución: {e}")
        finally:
            self.shutdown()
    
    def analyze_table(self, screenshot):
        """Analizar la mesa de poker"""
        self.stats["hands_analyzed"] += 1  # 🔥 CORREGIDO
        
        print(f"\n📊 ANÁLISIS #{self.stats['hands_analyzed']}")  # 🔥 CORREGIDO
        print("   " + "-" * 40)
        
        # 1. Reconocer cartas
        hole_cards = self.adapter.recognize_hole_cards(screenshot)
        community_cards = self.adapter.recognize_community_cards(screenshot)
        
        print(f"   👤 Tus cartas: {hole_cards}")
        print(f"   🎯 Mesa: {community_cards}")
        
        # 2. Reconocer montos (simulado por ahora)
        pot_size = 100  # Placeholder
        print(f"   💰 Bote: ${pot_size}")
        
        # 3. Determinar etapa del juego
        stage = "preflop"
        if len(community_cards) >= 5:
            stage = "river"
        elif len(community_cards) >= 4:
            stage = "turn"
        elif len(community_cards) >= 3:
            stage = "flop"
        
        # 4. Preparar situación para análisis
        situation = {
            "hole_cards": hole_cards,
            "community_cards": community_cards,
            "pot_size": pot_size,
            "position": "BTN",  # Placeholder - en versión real detectar posición
            "players": 6,
            "stage": stage
        }
        
        # 5. Obtener recomendación del coach
        try:
            recommendation = self.coach.analyze_hand(situation)
            
            if recommendation:
                self.stats["recommendations_given"] += 1
                
                # Mostrar recomendación
                action = recommendation.get("action", "CHECK")
                confidence = recommendation.get("confidence", 0.5)
                reasoning = recommendation.get("reasoning", "")
                
                print(f"   💡 RECOMENDACIÓN: {action}")
                print(f"   📈 Confianza: {confidence:.0%}")
                
                if reasoning:
                    print(f"   🧠 Razón: {reasoning}")
                
                # Mostrar en overlay (simulado)
                self.show_overlay(action, confidence)
            
        except Exception as e:
            print(f"   ⚠️  Error en análisis: {e}")
    
    def show_overlay(self, action, confidence):
        """Mostrar recomendación en overlay (simulado)"""
        action_symbols = {
            "FOLD": "❌",
            "CHECK": "⏸️",
            "CALL": "✅", 
            "RAISE": "🔥",
            "ALL_IN": "🚀"
        }
        
        symbol = action_symbols.get(action, "❓")
        print(f"   🎯 OVERLAY: {symbol} {action} ({confidence:.0%})")
    
    def shutdown(self):
        """Apagar el sistema y mostrar estadísticas"""
        self.running = False
        
        # Calcular tiempo de ejecución
        end_time = datetime.now()
        if self.stats["start_time"]:
            try:
                start_time = datetime.fromisoformat(self.stats["start_time"])
                runtime = end_time - start_time
                runtime_seconds = runtime.total_seconds()
            except:
                runtime_seconds = 0
        else:
            runtime_seconds = 0
        
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS FINALES DE LA SESIÓN:")
        print(f"   Tiempo ejecución: {runtime_seconds:.1f}s")
        print(f"   Capturas totales: {self.stats['captures']}")
        print(f"   Mesas detectadas: {self.stats['tables_detected']}")
        print(f"   Manos analizadas: {self.stats['hands_analyzed']}")
        print(f"   Recomendaciones: {self.stats['recommendations_given']}")
        
        if runtime_seconds > 0:
            captures_per_sec = self.stats["captures"] / runtime_seconds
            print(f"   Capturas/segundo: {captures_per_sec:.1f}")
        
        if self.stats["captures"] > 0:
            detection_rate = (self.stats["tables_detected"] / self.stats["captures"]) * 100
            print(f"   Tasa detección: {detection_rate:.1f}%")
        
        # Guardar estadísticas
        stats_dir = "logs/sessions"
        os.makedirs(stats_dir, exist_ok=True)
        
        stats_file = os.path.join(stats_dir, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # 🔥 CORREGIDO: Asegurar que todos los valores sean JSON serializables
        session_stats = {
            "timestamp": datetime.now().isoformat(),  # String ISO
            "runtime_seconds": runtime_seconds,
            "captures": self.stats["captures"],
            "tables_detected": self.stats["tables_detected"],
            "hands_analyzed": self.stats["hands_analyzed"],
            "recommendations_given": self.stats["recommendations_given"],
            "config": self.config
        }
        
        try:
            with open(stats_file, 'w') as f:
                json.dump(session_stats, f, indent=2)
            print(f"\n💾 Estadísticas guardadas: {stats_file}")
        except Exception as e:
            print(f"⚠️  No se pudieron guardar estadísticas: {e}")
        
        print("\n🎯 Poker Coach Pro - Sesión finalizada")
        print("=" * 60)

def main():
    """Función principal"""
    coach = PokerCoachPro(platform="pokerstars", stealth_level=1)  # 🔥 Nivel 1 para más rápido
    coach.run()

if __name__ == "__main__":
    main()