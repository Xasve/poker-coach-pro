# poker_coach_integrator.py - NUEVO ARCHIVO
import sys
import os
import time
import yaml

class PokerCoachIntegrator:
    """Integrador principal del sistema Poker Coach Pro"""
    
    def __init__(self, config_path=None):
        """Inicializar integrador
        
        Args:
            config_path: str - Ruta al archivo de configuración YAML
        """
        self.config_path = config_path
        self.config = {}
        self.adapter = None
        self.engine = None
        self.overlay = None
        self.running = False
        
        print("[Integrator] Inicializando Poker Coach Pro...")
    
    def initialize(self):
        """Inicializar todos los componentes"""
        try:
            # 1. Cargar configuración
            self._load_config()
            
            # 2. Inicializar adaptador de plataforma
            self._initialize_adapter()
            
            # 3. Inicializar motor GTO
            self._initialize_engine()
            
            # 4. Inicializar overlay (opcional)
            self._initialize_overlay()
            
            print("[Integrator] Inicialización completada")
            return True
            
        except Exception as e:
            print(f"[ERROR] Falló inicialización: {e}")
            return False
    
    def _load_config(self):
        """Cargar configuración desde archivo YAML"""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"[Integrator] Configuración cargada: {self.config_path}")
        else:
            # Configuración por defecto
            self.config = {
                'platforms': {'default': 'pokerstars'},
                'capture': {'stealth_level': 'MEDIUM'},
                'overlay': {'enabled': False}
            }
            print("[Integrator] Usando configuración por defecto")
    
    def _initialize_adapter(self):
        """Inicializar adaptador de plataforma"""
        platform = self.config.get('platforms', {}).get('default', 'pokerstars')
        stealth_level = self.config.get('capture', {}).get('stealth_level', 'MEDIUM')
        
        if platform == 'pokerstars':
            from platforms.pokerstars_adapter import PokerStarsAdapter
            self.adapter = PokerStarsAdapter(stealth_level=stealth_level)
            print(f"[Integrator] Adaptador PokerStars creado (stealth: {stealth_level})")
        elif platform == 'ggpoker':
            from platforms.ggpoker_adapter import GGPokerAdapter
            self.adapter = GGPokerAdapter(stealth_level=stealth_level)
            print(f"[Integrator] Adaptador GGPoker creado")
        else:
            raise ValueError(f"Plataforma no soportada: {platform}")
    
    def _initialize_engine(self):
        """Inicializar motor GTO"""
        from core.poker_engine import PokerEngine
        self.engine = PokerEngine()
        print("[Integrator] Motor GTO inicializado")
    
    def _initialize_overlay(self):
        """Inicializar overlay GUI"""
        overlay_enabled = self.config.get('overlay', {}).get('enabled', False)
        
        if overlay_enabled:
            try:
                from overlay.gui_overlay import PokerOverlay
                self.overlay = PokerOverlay()
                print("[Integrator] Overlay inicializado")
            except ImportError:
                print("[Integrator] Overlay no disponible")
                self.overlay = None
        else:
            print("[Integrator] Overlay deshabilitado en configuración")
            self.overlay = None
    
    def detect_platform(self):
        """Detectar plataforma automáticamente (simulado)"""
        # Por ahora retornamos la plataforma configurada
        return self.config.get('platforms', {}).get('default', 'pokerstars')
    
    def run_single_iteration(self):
        """Ejecutar una iteración del análisis"""
        try:
            # 1. Capturar y analizar mesa
            if not self.adapter:
                print("[ERROR] Adaptador no inicializado")
                return False
            
            # Iniciar captura si no está activa
            self.adapter.start()
            
            # Obtener estado de la mesa
            table_state = self.adapter.get_table_state()
            
            if not table_state:
                print("[INFO] No se detectó mesa de poker")
                return False
            
            # 2. Analizar con motor GTO si hay datos válidos
            if table_state.get('cards') or table_state.get('simulated'):
                decision = self.engine.analyze_hand(
                    hole_cards=table_state.get('cards', {}).get('hero', []),
                    community_cards=table_state.get('cards', {}).get('community', []),
                    pot_size=table_state.get('pot', 0),
                    position=table_state.get('position', 'middle')
                )
                
                # 3. Mostrar resultados
                print(f"\n[ANALISIS] Recomendación: {decision.get('action', 'CHECK')}")
                print(f"          Confianza: {decision.get('confidence', 0):.1%}")
                print(f"          Pot: {table_state.get('pot', 0)}")
                
                # 4. Actualizar overlay si está activo
                if self.overlay:
                    self.overlay.update_display(decision)
                
                return True
            else:
                print("[INFO] No hay cartas para analizar")
                return False
                
        except Exception as e:
            print(f"[ERROR] Iteración fallida: {e}")
            return False
    
    def run_continuous(self, interval=1.0):
        """Ejecutar análisis continuo"""
        print(f"[Integrator] Iniciando análisis continuo (intervalo: {interval}s)")
        print("Presiona Ctrl+C para detener")
        
        self.running = True
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                print(f"\n--- Iteración {iteration} ---")
                
                success = self.run_single_iteration()
                
                if not success and iteration > 3:
                    print("[INFO] No se detecta actividad de poker, pausando...")
                    time.sleep(5)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[Integrator] Detenido por usuario")
        except Exception as e:
            print(f"[ERROR] Error en ejecución continua: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpiar recursos"""
        print("[Integrator] Limpiando recursos...")
        
        if self.adapter:
            self.adapter.stop()
        
        if self.overlay:
            self.overlay.close()
        
        self.running = False
        print("[Integrator] Limpieza completada")

# Función principal para ejecución directa
def main():
    """Función principal para ejecutar el integrador"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Poker Coach Pro - Sistema de análisis GTO')
    parser.add_argument('--config', default='config/default_config.yaml',
                       help='Ruta al archivo de configuración')
    parser.add_argument('--interval', type=float, default=2.0,
                       help='Intervalo entre análisis (segundos)')
    
    args = parser.parse_args()
    
    # Crear y ejecutar integrador
    integrator = PokerCoachIntegrator(config_path=args.config)
    
    if integrator.initialize():
        integrator.run_continuous(interval=args.interval)
    else:
        print("[ERROR] No se pudo inicializar el sistema")

if __name__ == "__main__":
    main()