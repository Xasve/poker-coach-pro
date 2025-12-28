import tkinter as tk\nfrom tkinter import messagebox
from tkinter import ttk
import pyautogui
import mss
import cv2
import numpy as np
import json
import os

class WindowSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("�� Poker Coach Pro - Selector de Ventana")
        self.root.geometry("600x500")
        
        self.selected_window = None
        self.regions = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title_label = tk.Label(self.root, text="POKER COACH PRO", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Instrucciones
        instructions = tk.Label(self.root, text="Selecciona la ventana de PokerStars y define las áreas:", 
                               font=("Arial", 10))
        instructions.pack(pady=5)
        
        # Lista de ventanas
        self.window_listbox = tk.Listbox(self.root, height=8, font=("Arial", 10))
        self.window_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Botón para actualizar ventanas
        refresh_btn = tk.Button(self.root, text=" Actualizar Ventanas", 
                               command=self.refresh_windows, font=("Arial", 10))
        refresh_btn.pack(pady=5)
        
        # Botón para capturar ventana seleccionada
        capture_btn = tk.Button(self.root, text=" Capturar Ventana", 
                               command=self.capture_window, font=("Arial", 10, "bold"),
                               bg="#4CAF50", fg="white")
        capture_btn.pack(pady=10)
        
        # Áreas a configurar
        areas_frame = tk.Frame(self.root)
        areas_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.areas = {
            "mesa": {"label": "Mesa completa", "coords": []},
            "cartas_jugador": {"label": "Tus cartas", "coords": []},
            "cartas_mesa": {"label": "Cartas comunitarias", "coords": []},
            "pozo": {"label": "Área del pozo", "coords": []}
        }
        
        row = 0
        for area_id, area_info in self.areas.items():
            frame = tk.Frame(areas_frame)
            frame.grid(row=row, column=0, sticky="w", pady=2)
            
            label = tk.Label(frame, text=area_info["label"], width=20, anchor="w")
            label.pack(side=tk.LEFT)
            
            coords_label = tk.Label(frame, text="No definido", fg="red")
            coords_label.pack(side=tk.LEFT, padx=10)
            area_info["coords_label"] = coords_label
            
            define_btn = tk.Button(frame, text="Definir", 
                                  command=lambda aid=area_id: self.define_area(aid))
            define_btn.pack(side=tk.LEFT, padx=5)
            
            row += 1
        
        # Botón para guardar configuración
        save_btn = tk.Button(self.root, text=" Guardar Configuración", 
                            command=self.save_configuration,
                            font=("Arial", 12, "bold"), bg="#2196F3", fg="white")
        save_btn.pack(pady=20)
        
        # Estado
        self.status_label = tk.Label(self.root, text="Listo", fg="gray")
        self.status_label.pack(pady=5)
        
        self.refresh_windows()
    
    def refresh_windows(self):
        """Obtener lista de ventanas abiertas"""
        self.window_listbox.delete(0, tk.END)
        
        try:
            # Usar pyautogui para obtener ventanas (simplificado)
            windows = ["PokerStars - Mesa Principal",
                      "PokerStars - Torneo",
                      "PokerStars - Caja Registradora",
                      "PokerStars - Ventana de Chat"]
            
            for window in windows:
                self.window_listbox.insert(tk.END, window)
            
            # Agregar ventana actual como primera opción
            self.window_listbox.insert(0, "[ACTUAL] PokerStars Game Window")
            
        except Exception as e:
            self.window_listbox.insert(tk.END, f"Error: {e}")
    
    def capture_window(self):
        """Capturar la ventana seleccionada"""
        selection = self.window_listbox.curselection()
        if not selection:
            self.status_label.config(text=" Selecciona una ventana primero", fg="red")
            return
        
        window_name = self.window_listbox.get(selection[0])
        self.selected_window = window_name
        
        # Capturar pantalla completa
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
        
        # Convertir y guardar
        img = np.array(screenshot)
        os.makedirs("config", exist_ok=True)
        cv2.imwrite("config/window_preview.jpg", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
        
        self.status_label.config(text=f" Ventana '{window_name}' capturada", fg="green")
        
        # Mostrar mensaje para definir áreas
        messagebox.showinfo("Definir Áreas", 
                              "Ahora define las áreas importantes:\n\n" +
                              "1. Haz clic en 'Definir' junto a 'Mesa completa'\n" +
                              "2. Dibuja un rectángulo alrededor de toda la mesa\n" +
                              "3. Repite para las otras áreas")
    
    def define_area(self, area_id):
        """Iniciar definición de área"""
        if not self.selected_window:
            self.status_label.config(text=" Captura una ventana primero", fg="red")
            return
        
        self.status_label.config(text=f" Define: {self.areas[area_id]['label']} - Arrastra en la imagen", fg="blue")
        
        # Aquí iría el código para selección con ratón
        # Por ahora, usaremos coordenadas predefinidas
        predefined = {
            "mesa": [100, 100, 800, 600],
            "cartas_jugador": [400, 500, 150, 50],
            "cartas_mesa": [300, 300, 400, 80],
            "pozo": [350, 250, 200, 40]
        }
        
        self.regions[area_id] = predefined[area_id]
        self.areas[area_id]["coords_label"].config(
            text=str(predefined[area_id]), 
            fg="green"
        )
        
        self.status_label.config(text=f" {self.areas[area_id]['label']} definida", fg="green")
    
    def save_configuration(self):
        """Guardar configuración en archivo"""
        if not self.regions:
            self.status_label.config(text=" Define al menos un área primero", fg="red")
            return
        
        config = {
            "window_name": self.selected_window or "PokerStars",
            "regions": self.regions,
            "screen_resolution": f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}"
        }
        
        with open("config/window_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        self.status_label.config(text=" Configuración guardada en config/window_config.json", fg="green")
        
        # Mostrar resumen
        summary = " CONFIGURACIÓN GUARDADA:\n\n"
        for area_id, coords in self.regions.items():
            summary += f"{self.areas[area_id]['label']}: {coords}\n"
        
        messagebox.showinfo("Configuración Guardada", summary)
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    selector = WindowSelector()
    selector.run()
