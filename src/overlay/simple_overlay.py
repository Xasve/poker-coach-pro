"""
Overlay simplificado que evita problemas de threading
"""
import tkinter as tk
from tkinter import font
import threading
import time

class SimpleOverlay:
    """Overlay minimalista sin problemas de threading"""
    
    def __init__(self):
        self.root = None
        self.label = None
        self.running = False
        
    def start(self):
        """Iniciar overlay en el hilo principal"""
        try:
            # Crear ventana
            self.root = tk.Tk()
            self.root.title("Poker Coach Pro")
            self.root.attributes('-topmost', True)
            self.root.attributes('-alpha', 0.9)
            self.root.geometry("300x150+50+50")
            self.root.configure(bg='black')
            
            # Configurar label
            custom_font = font.Font(family="Consolas", size=12)
            self.label = tk.Label(
                self.root,
                text="Poker Coach Pro\n---\nEsperando...",
                font=custom_font,
                fg="white",
                bg="black",
                justify="left"
            )
            self.label.pack(expand=True, fill='both', padx=10, pady=10)
            
            # Botón para cerrar
            close_btn = tk.Button(
                self.root,
                text="Cerrar",
                command=self.stop,
                bg="red",
                fg="white"
            )
            close_btn.pack(pady=5)
            
            self.running = True
            print(" Overlay iniciado (sin threading)")
            
        except Exception as e:
            print(f"  Error iniciando overlay: {e}")
            self.root = None
    
    def update(self, text: str, color: str = "white"):
        """Actualizar texto del overlay"""
        if self.root and self.label:
            try:
                self.label.config(text=text, fg=color)
            except:
                pass
    
    def stop(self):
        """Detener overlay"""
        self.running = False
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        print(" Overlay detenido")
    
    def run(self):
        """Ejecutar loop principal (debe llamarse desde main thread)"""
        if self.root:
            self.root.mainloop()

# Versión que funciona con threading en Windows
class ThreadSafeOverlay:
    """Overlay que usa cola para actualizaciones thread-safe"""
    
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.running = False
        
    def show(self, text: str):
        """Mostrar texto (thread-safe)"""
        with self.lock:
            print(f"\n{'='*40}")
            print(" OVERLAY (Simulado):")
            print(f"{'='*40}")
            print(text)
            print(f"{'='*40}")
    
    def update_recommendation(self, decision: dict):
        """Mostrar recomendación"""
        action = decision.get('action', 'CHECK')
        confidence = decision.get('confidence', 0.5) * 100
        reason = decision.get('reason', '')
        
        text = f""" RECOMENDACIÓN:
        
Acción: {action}
Confianza: {confidence:.0f}%
Razón: {reason}

Alternativas: {', '.join(decision.get('alternatives', []))}"""
        
        self.show(text)
