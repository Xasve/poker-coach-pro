#!/usr/bin/env python3
"""
Poker Coach Pro - Versión SUPER SIMPLE para comenzar
Funciona de inmediato sin muchos archivos
"""

import tkinter as tk
from tkinter import ttk
import random
import time

class SimplePokerCoach:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poker Coach Pro - SIMPLE")
        self.window.attributes('-topmost', True)
        self.window.geometry("400x300+100+100")
        self.window.configure(bg='#0A1E32')
        
        self.setup_ui()
        self.start_analysis()
    
    def setup_ui(self):
        # Título
        title = tk.Label(self.window, text="🎴 POKER COACH PRO", 
                        font=("Arial", 16, "bold"), fg="#FFD700", bg="#0A1E32")
        title.pack(pady=10)
        
        # Plataforma
        self.platform_label = tk.Label(self.window, text="Plataforma: GG Poker",
                                      font=("Arial", 12), fg="white", bg="#0A1E32")
        self.platform_label.pack()
        
        # Recomendación principal
        self.action_label = tk.Label(self.window, text="ANALIZANDO...",
                                   font=("Arial", 24, "bold"), fg="white", bg="#8B0000")
        self.action_label.pack(pady=20, ipadx=20, ipady=10)
        
        # Explicación
        self.explanation_label = tk.Label(self.window, text="Esperando primera mano...",
                                        font=("Arial", 10), fg="#CCCCCC", bg="#0A1E32",
                                        wraplength=350, justify="center")
        self.explanation_label.pack(pady=10)
        
        # Información adicional
        info_frame = tk.Frame(self.window, bg="#0A1E32")
        info_frame.pack(pady=10)
        
        self.confidence_label = tk.Label(info_frame, text="Confianza: --%",
                                       font=("Arial", 9), fg="#90EE90", bg="#0A1E32")
        self.confidence_label.pack(side="left", padx=10)
        
        self.timer_label = tk.Label(info_frame, text="Tiempo: 0s",
                                   font=("Arial", 9), fg="#ADD8E6", bg="#0A1E32")
        self.timer_label.pack(side="left", padx=10)
        
        # Botón para simular
        tk.Button(self.window, text="SIMULAR DECISIÓN", command=self.simulate_decision,
                 font=("Arial", 10), bg="#006400", fg="white", padx=20, pady=5).pack(pady=10)
        
        # Instrucciones
        instructions = """
        INSTRUCCIONES:
        1. Abre GG Poker o PokerStars
        2. Coloca esta ventana al lado
        3. Sigue las recomendaciones
        4. Usa el botón para practicar
        """
        
        tk.Label(self.window, text=instructions, font=("Arial", 8), 
                fg="#888888", bg="#0A1E32", justify="left").pack(pady=10)
    
    def simulate_decision(self):
        """Simular una decisión de poker"""
        situations = [
            {
                "action": "RAISE",
                "size": "2.2BB",
                "confidence": random.randint(75, 95),
                "explanation": "Mano fuerte en posición. Open estándar para robar ciegas."
            },
            {
                "action": "FOLD",
                "size": "",
                "confidence": random.randint(80, 90),
                "explanation": "Mano débil fuera de posición. Fold disciplinado."
            },
            {
                "action": "CALL",
                "size": "1BB",
                "confidence": random.randint(65, 80),
                "explanation": "Defensa de ciega con odds decentes. Ver flop."
            },
            {
                "action": "ALL-IN",
                "size": "25BB",
                "confidence": random.randint(85, 99),
                "explanation": "Mano premium con stack corto. Maximizar fold equity."
            }
        ]
        
        situation = random.choice(situations)
        
        # Actualizar interfaz
        self.action_label.config(text=situation["action"])
        
        # Color según acción
        colors = {
            "RAISE": "#8B0000",    # Rojo oscuro
            "FOLD": "#2F4F4F",     # Gris oscuro
            "CALL": "#FF8C00",     # Naranja
            "ALL-IN": "#8B0000"    # Rojo oscuro
        }
        
        self.action_label.config(bg=colors.get(situation["action"], "#8B0000"))
        
        # Actualizar texto
        size_text = f"Tamaño: {situation['size']}" if situation["size"] else ""
        self.explanation_label.config(
            text=f"{situation['explanation']}\n{size_text}"
        )
        
        # Actualizar confianza
        self.confidence_label.config(
            text=f"Confianza: {situation['confidence']}%",
            fg="#90EE90" if situation['confidence'] > 70 else "#FFB6C1"
        )
    
    def start_analysis(self):
        """Iniciar análisis automático simulado"""
        self.analysis_count = 0
        
        def analyze():
            self.analysis_count += 1
            self.timer_label.config(text=f"Análisis: {self.analysis_count}")
            
            # Ocasionalmente simular decisión automática
            if random.random() < 0.3:  # 30% de probabilidad
                self.simulate_decision()
            
            # Programar próximo análisis
            self.window.after(3000, analyze)  # Cada 3 segundos
        
        # Iniciar primer análisis después de 2 segundos
        self.window.after(2000, analyze)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.window.mainloop()

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("🔍 Verificando dependencias...")
    
    dependencies = [
        ("tkinter", "tkinter"),  # Normalmente viene con Python
        ("random", "random"),
        ("time", "time")
    ]
    
    missing = []
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Faltan dependencias: {', '.join(missing)}")
        print("📦 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def main():
    """Función principal"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║      POKER COACH PRO - SIMPLE        ║
    ║      Versión inicial de prueba       ║
    ╚══════════════════════════════════════╝
    """)
    
    # Verificar dependencias mínimas
    if not check_dependencies():
        response = input("\n¿Continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            return
    
    # Iniciar coach
    print("\n🚀 Iniciando Poker Coach Pro...")
    print("📺 Se abrirá una ventana con overlay")
    print("🎯 Usa el botón 'SIMULAR DECISIÓN' para practicar")
    print("⏸️  Cierra la ventana para salir\n")
    
    try:
        coach = SimplePokerCoach()
        coach.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()