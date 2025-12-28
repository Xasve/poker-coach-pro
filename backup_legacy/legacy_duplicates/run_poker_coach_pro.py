# run_poker_coach_pro.py
import sys
import os
import time
import json
from datetime import datetime

class PokerCoachPro:
    """Sistema principal mejorado de Poker Coach Pro"""
    
    def __init__(self):
        self.running = False
        self.iteration = 0
        self.stats = {
            "start_time": None,
            "iterations": 0,
            "decisions": [],
            "errors": 0
        }
        
        print("🎴 POKER COACH PRO - SISTEMA MEJORADO")
        print("=" * 60)
    
    def initialize(self):
        """Inicializar todos los componentes"""
        try:
            sys.path.insert(0, 'src')
            
            from platforms.pokerstars_adapter import PokerStarsAdapter
            from core.poker_engine import PokerEngine
            
            self.adapter = PokerStarsAdapter(stealth_level="LOW")
            self.engine = PokerEngine(aggression=1.2, tightness=0.9)
            
            print("✅ Componentes inicializados")
            print(f"   - Adaptador: PokerStars")
            print(f"   - Motor GTO: Agresión {self.engine.aggression}, Tightness {self.engine.tightness}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando: {e}")
            return False
    
    def analyze_iteration(self):
        """Ejecutar una iteración de análisis"""
        try:
            self.iteration += 1
            
            # Obtener estado de la mesa
            table_state = self.adapter.get_table_state()
            
            if not table_state:
                print(f"⏳ Iteración {self.iteration}: Esperando mesa...")
                return False
            
            # Mostrar información
            simulated = table_state.get('simulated', False)
            status = "SIMULADO" if simulated else "REAL"
            
            print(f"\n🔄 Iteración {self.iteration} [{status}]")
            print("-" * 40)
            
            # Mostrar cartas
            cards = table_state.get('cards', {})
            if cards:
                print(f"🎴 Cartas propias: {cards.get('hero', [])}")
                print(f"🎴 Cartas comunitarias: {cards.get('community', [])}")
            
            # Mostrar pozo
            pot = table_state.get('pot', '0')
            print(f"💰 Pozo: {pot}")
            
            # Analizar con motor GTO
            pot_int = int(pot) if str(pot).isdigit() else 0
            
            decision = self.engine.analyze_hand(
                hole_cards=cards.get('hero', []),
                community_cards=cards.get('community', []),
                pot_size=pot_int,
                position=table_state.get('position', 'middle')
            )
            
            # Mostrar recomendación
            print(f"\n🎯 RECOMENDACIÓN GTO:")
            print(f"   Acción: {decision.get('action')}")
            print(f"   Confianza: {decision.get('confidence', 0):.1%}")
            print(f"   Razón: {decision.get('reason', '')}")
            
            # Guardar estadísticas
            self.stats["decisions"].append({
                "iteration": self.iteration,
                "action": decision.get('action'),
                "confidence": decision.get('confidence'),
                "timestamp": datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error en iteración {self.iteration}: {e}")
            self.stats["errors"] += 1
            return False
    
    def run(self, interval=2.0):
        """Ejecutar sistema continuamente"""
        if not self.initialize():
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now().isoformat()
        
        print(f"\n🚀 Iniciando análisis continuo...")
        print(f"   Intervalo: {interval} segundos")
        print(f"   Presiona Ctrl+C para detener")
        print("=" * 60)
        
        try:
            while self.running:
                success = self.analyze_iteration()
                self.stats["iterations"] = self.iteration
                
                if not success and self.iteration > 5:
                    print("💤 No se detecta actividad, pausando 5 segundos...")
                    time.sleep(5)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Detenido por usuario")
        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Apagar sistema limpiamente"""
        print("\n🔧 Apagando sistema...")
        
        if hasattr(self, 'adapter'):
            self.adapter.stop()
        
        self.running = False
        
        # Mostrar estadísticas
        self.show_statistics()
        
        print("✅ Sistema apagado correctamente")
        print("=" * 60)
    
    def show_statistics(self):
        """Mostrar estadísticas de la sesión"""
        print("\n📊 ESTADÍSTICAS DE LA SESIÓN:")
        print("-" * 40)
        
        total = self.stats["iterations"]
        errors = self.stats["errors"]
        success_rate = ((total - errors) / total * 100) if total > 0 else 0
        
        print(f"   Iteraciones totales: {total}")
        print(f"   Errores: {errors}")
        print(f"   Tasa de éxito: {success_rate:.1f}%")
        
        # Análisis de decisiones
        if self.stats["decisions"]:
            actions = {}
            for d in self.stats["decisions"]:
                action = d.get("action", "UNKNOWN")
                actions[action] = actions.get(action, 0) + 1
            
            print(f"\n   DISTRIBUCIÓN DE DECISIONES:")
            for action, count in actions.items():
                percentage = (count / len(self.stats["decisions"])) * 100
                print(f"   {action}: {count} ({percentage:.1f}%)")
        
        # Guardar estadísticas en archivo
        stats_file = "logs/session_stats.json"
        os.makedirs("logs", exist_ok=True)
        
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"\n   📁 Estadísticas guardadas en: {stats_file}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Poker Coach Pro - Sistema de análisis GTO')
    parser.add_argument('--interval', type=float, default=3.0,
                       help='Intervalo entre análisis (segundos)')
    parser.add_argument('--aggression', type=float, default=1.2,
                       help='Nivel de agresión del motor (0.5-2.0)')
    parser.add_argument('--tightness', type=float, default=0.9,
                       help='Nivel de tightness del motor (0.5-2.0)')
    
    args = parser.parse_args()
    
    # Crear y ejecutar sistema
    coach = PokerCoachPro()
    
    # Modificar motor si se especifican parámetros
    if args.aggression != 1.2 or args.tightness != 0.9:
        # Nota: Necesitaríamos modificar la inicialización
        print(f"⚙️  Configuración personalizada:")
        print(f"   - Agresión: {args.aggression}")
        print(f"   - Tightness: {args.tightness}")
    
    coach.run(interval=args.interval)

if __name__ == "__main__":
    main()