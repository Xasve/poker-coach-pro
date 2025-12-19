import sys, os, time, threading, json
from datetime import datetime

class PokerCoachMonitor:
    def __init__(self):
        self.stats = {
            "session_start": datetime.now().isoformat(),
            "iterations": 0,
            "real_detections": 0,
            "simulated_detections": 0,
            "decisions": {"RAISE": 0, "CALL": 0, "CHECK": 0, "FOLD": 0},
            "errors": [],
            "performance": []
        }
        self.running = True
        
    def log_iteration(self, mode, decision, processing_time):
        """Registrar iteración"""
        self.stats["iterations"] += 1
        
        if mode == "REAL":
            self.stats["real_detections"] += 1
        else:
            self.stats["simulated_detections"] += 1
        
        if decision in self.stats["decisions"]:
            self.stats["decisions"][decision] += 1
        
        self.stats["performance"].append({
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time,
            "mode": mode
        })
        
        # Mantener solo últimos 100 registros de performance
        if len(self.stats["performance"]) > 100:
            self.stats["performance"] = self.stats["performance"][-100:]
    
    def log_error(self, error_type, message):
        """Registrar error"""
        self.stats["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": message
        })
    
    def display_dashboard(self):
        """Mostrar dashboard en tiempo real"""
        os.system("cls" if os.name == "nt" else "clear")
        
        total = self.stats["iterations"]
        real_pct = (self.stats["real_detections"] / total * 100) if total > 0 else 0
        
        print(" DASHBOARD POKER COACH PRO - TIEMPO REAL")
        print("="*60)
        print(f" Sesión iniciada: {self.stats['session_start'][11:19]}")
        print(f" Iteraciones: {total}")
        print(f" Detecciones REALES: {self.stats['real_detections']} ({real_pct:.1f}%)")
        print(f" Detecciones SIMULADAS: {self.stats['simulated_detections']}")
        print(f"\n DECISIONES TOMADAS:")
        
        for action, count in self.stats["decisions"].items():
            if total > 0:
                pct = (count / total * 100)
                bar = "" * int(pct / 5)
                print(f"   {action:6} {bar:20} {count:3} ({pct:.1f}%)")
        
        if self.stats["errors"]:
            print(f"\n  ERRORES ({len(self.stats['errors'])}):")
            for err in self.stats["errors"][-3:]:  # Mostrar últimos 3
                print(f"    {err['timestamp'][11:19]} - {err['type']}: {err['message'][:50]}")
        
        print("\n" + "="*60)
        print("ℹ  Actualizando cada 5 segundos... Ctrl+C para salir")
    
    def auto_save_stats(self):
        """Guardar estadísticas automáticamente"""
        while self.running:
            time.sleep(30)  # Guardar cada 30 segundos
            self.save_stats()
    
    def save_stats(self):
        """Guardar estadísticas a archivo"""
        os.makedirs("logs", exist_ok=True)
        filename = f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w") as f:
            json.dump(self.stats, f, indent=2)
        
        print(f" Estadísticas guardadas: {filename}")
    
    def start(self):
        """Iniciar monitor"""
        print(" Iniciando monitor en tiempo real...")
        
        # Hilo para guardado automático
        save_thread = threading.Thread(target=self.auto_save_stats)
        save_thread.daemon = True
        save_thread.start()
        
        try:
            while self.running:
                self.display_dashboard()
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n  Deteniendo monitor...")
        finally:
            self.running = False
            self.save_stats()
            print(" Monitor detenido")

if __name__ == "__main__":
    monitor = PokerCoachMonitor()
    monitor.start()
