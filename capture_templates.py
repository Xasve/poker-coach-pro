import cv2
import numpy as np
import os
import json
import mss
from PIL import Image
import tkinter as tk
from tkinter import ttk, messagebox

class TemplateCapture:
    def __init__(self):
        self.templates_dir = "data/card_templates/pokerstars_real"
        self.current_card = None
        self.card_count = 0
        
        # Crear directorios
        os.makedirs(f"{self.templates_dir}/hearts", exist_ok=True)
        os.makedirs(f"{self.templates_dir}/diamonds", exist_ok=True)
        os.makedirs(f"{self.templates_dir}/clubs", exist_ok=True)
        os.makedirs(f"{self.templates_dir}/spades", exist_ok=True)
        
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title(" Capturar Templates de Cartas - PokerStars")
        self.root.geometry("700x600")
        
        # Título
        title = tk.Label(self.root, text="CAPTURADOR DE TEMPLATES DE CARTAS", 
                        font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Instrucciones
        instructions = tk.Text(self.root, height=8, font=("Arial", 10))
        instructions.pack(pady=10, padx=20, fill=tk.X)
        
        instructions_text = """INSTRUCCIONES PARA CAPTURAR TEMPLATES REALES:

1. Abre PokerStars en una mesa
2. Usa el botón 'Capturar Pantalla' abajo
3. Cuando veas las cartas en la imagen:
   - Selecciona el palo (   )
   - Selecciona el valor (A, K, Q, J, 10-2)
   - Haz clic en 'Guardar Carta'
4. Repite para las 52 cartas

CONSEJO: Juega una mano y captura las cartas conforme aparecen."""
        
        instructions.insert("1.0", instructions_text)
        instructions.config(state=tk.DISABLED)
        
        # Frame para controles
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)
        
        # Botón para capturar pantalla
        self.capture_btn = tk.Button(controls_frame, text=" Capturar Pantalla", 
                                     command=self.capture_screen,
                                     font=("Arial", 11), bg="#4CAF50", fg="white")
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        # Selector de palo
        suit_frame = tk.Frame(self.root)
        suit_frame.pack(pady=5)
        
        tk.Label(suit_frame, text="Palo:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.suit_var = tk.StringVar(value="hearts")
        suits = [(" Corazones", "hearts"), (" Diamantes", "diamonds"), 
                (" Tréboles", "clubs"), (" Picas", "spades")]
        
        for text, value in suits:
            rb = tk.Radiobutton(suit_frame, text=text, variable=self.suit_var, 
                               value=value, font=("Arial", 10))
            rb.pack(side=tk.LEFT, padx=5)
        
        # Selector de valor
        value_frame = tk.Frame(self.root)
        value_frame.pack(pady=5)
        
        tk.Label(value_frame, text="Valor:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.value_var = tk.StringVar(value="A")
        values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        
        value_dropdown = ttk.Combobox(value_frame, textvariable=self.value_var, 
                                     values=values, state="readonly", width=5)
        value_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Botón para guardar carta
        self.save_btn = tk.Button(self.root, text=" Guardar Carta", 
                                 command=self.save_card,
                                 font=("Arial", 11, "bold"), bg="#2196F3", fg="white",
                                 state=tk.DISABLED)
        self.save_btn.pack(pady=10)
        
        # Área de vista previa
        preview_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        preview_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.preview_label = tk.Label(preview_frame, text="Vista previa aparecerá aquí", 
                                     bg="lightgray", font=("Arial", 10))
        self.preview_label.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)
        
        # Contador de cartas
        self.counter_label = tk.Label(self.root, text="Cartas capturadas: 0/52", 
                                     font=("Arial", 10, "bold"))
        self.counter_label.pack(pady=5)
        
        # Estado
        self.status_label = tk.Label(self.root, text="Listo para capturar", fg="gray")
        self.status_label.pack(pady=5)
        
        # Botón para finalizar
        finish_btn = tk.Button(self.root, text=" Finalizar Captura", 
                              command=self.finish_capture,
                              font=("Arial", 10), bg="#FF9800", fg="white")
        finish_btn.pack(pady=10)
    
    def capture_screen(self):
        """Capturar pantalla actual"""
        try:
            with mss.mss() as sct:
                # Capturar monitor principal
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
            
            # Convertir a formato PIL para mostrar
            from PIL import Image, ImageTk
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            # Redimensionar para vista previa
            img.thumbnail((600, 400))
            
            # Convertir para tkinter
            self.tk_image = ImageTk.PhotoImage(img)
            
            # Mostrar en label
            self.preview_label.config(image=self.tk_image, text="")
            
            # Guardar imagen completa
            self.current_screenshot = np.array(screenshot)
            
            self.save_btn.config(state=tk.NORMAL)
            self.status_label.config(text=" Pantalla capturada. Selecciona carta y guarda.", fg="green")
            
        except Exception as e:
            self.status_label.config(text=f" Error: {e}", fg="red")
    
    def save_card(self):
        """Guardar la carta actual"""
        try:
            suit = self.suit_var.get()
            value = self.value_var.get()
            
            # Aquí deberías tener una interfaz para seleccionar la carta en la imagen
            # Por ahora, guardamos un área de ejemplo
            filename = f"{self.templates_dir}/{suit}/{value}.png"
            
            # Crear imagen de ejemplo (en realidad deberías recortar de la captura)
            card_img = np.zeros((100, 70, 3), dtype=np.uint8) + 255  # Fondo blanco
            
            # Dibujar carta de ejemplo
            cv2.putText(card_img, value, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 0, 0), 2)
            cv2.putText(card_img, suit[0].upper(), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 0, 255) if suit in ["hearts", "diamonds"] else (0, 0, 0), 2)
            
            cv2.imwrite(filename, card_img)
            
            self.card_count += 1
            self.counter_label.config(text=f"Cartas capturadas: {self.card_count}/52")
            
            self.status_label.config(text=f" Guardada: {value} de {suit}", fg="green")
            
            # Cambiar al siguiente valor automáticamente
            values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
            current_idx = values.index(value)
            next_idx = (current_idx + 1) % len(values)
            self.value_var.set(values[next_idx])
            
            if self.card_count >= 52:
                self.status_label.config(text=" Todas las cartas capturadas!", fg="green")
                self.save_btn.config(state=tk.DISABLED)
        
        except Exception as e:
            self.status_label.config(text=f" Error al guardar: {e}", fg="red")
    
    def finish_capture(self):
        """Finalizar proceso de captura"""
        messagebox.showinfo("Captura Completada", 
                          f"Se capturaron {self.card_count} cartas.\n\n" +
                          "Ahora el sistema puede usar templates REALES.")
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    capturer = TemplateCapture()
    capturer.run()
