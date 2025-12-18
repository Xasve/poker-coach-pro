"""
Archivo: overlay_gui.py
Ruta: src/overlay/overlay_gui.py
Interfaz gráfica overlay para mostrar recomendaciones
"""

import tkinter as tk
from tkinter import ttk, font
import json
import os
from datetime import datetime

class OverlayGUI:
    """Clase principal para la interfaz overlay"""
    
    def __init__(self, platform="ggpoker"):
        self.platform = platform
        self.window = None
        self.is_visible = False
        self.last_decision = None
        
        # Cargar configuración
        self.load_config()
        
        # Inicializar colores según plataforma
        self.setup_colors()
        
    def load_config(self):
        """Cargar configuración del overlay"""
        config_path = "config/general_settings.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f).get('overlay', {})
        else:
            self.config = {}
    
    def setup_colors(self):
        """Configurar colores según plataforma"""
        if self.platform == "ggpoker":
            self.colors = {
                'bg': '#0A1E32',  # Azul oscuro GG Poker
                'fg': '#FFFFFF',
                'accent': '#FFD700',  # Dorado GG
                'raise_bg': '#8B0000',  # Rojo oscuro para raise
                'call_bg': '#FF8C00',   # Naranja para call
                'fold_bg': '#2F4F4F',   # Gris oscuro para fold
                'check_bg': '#006400',  # Verde oscuro para check
                'allin_bg': '#8B0000',  # Rojo para all-in
            }
        else:  # pokerstars
            self.colors = {
                'bg': '#006633',  # Verde PokerStars
                'fg': '#FFFFFF',
                'accent': '#FF9900',  # Naranja PokerStars
                'raise_bg': '#CC0000',  # Rojo para raise
                'call_bg': '#FF6600',   # Naranja para call
                'fold_bg': '#666666',   # Gris para fold
                'check_bg': '#009900',  # Verde para check
                'allin_bg': '#990000',  # Rojo oscuro para all-in
            }
    
    def show(self):
        """Mostrar la ventana overlay"""
        if self.window:
            self.window.deiconify()
            return
            
        self.window = tk.Tk()
        self.window.title("Poker Coach Pro")
        self.window.attributes('-topmost', True)
        self.window.attributes('-alpha', self.config.get('transparency', 0.9))
        self.window.overrideredirect(True)  # Sin bordes
        
        # Configurar posición
        position = self.config.get('position', 'top_right')
        self.set_position(position)
        
        # Establecer tamaño
        self.window.geometry("400x280")
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear widgets
        self.create_widgets()
        
        # Iniciar actualización de tiempo
        self.update_timer()
        
        self.is_visible = True
        self.window.mainloop()
    
    def set_position(self, position):
        """Posicionar ventana según configuración"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        positions = {
            'top_right': (screen_width - 420, 50),
            'top_left': (50, 50),
            'bottom_right': (screen_width - 420, screen_height - 330),
            'bottom_left': (50, screen_height - 330),
            'center': ((screen_width - 400) // 2, (screen_height - 280) // 2)
        }
        
        x, y = positions.get(position, positions['top_right'])
        self.window.geometry(f"+{x}+{y}")
    
    def setup_styles(self):
        """Configurar estilos de tkinter"""
        style = ttk.Style()
        
        # Configurar fuentes
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=self.config.get('font_size', 12))
        
        # Configurar colores
        self.window.configure(bg=self.colors['bg'])
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Título
        title_text = f"🎴 Poker Coach Pro - {self.platform.upper()} 🎴"
        title_label = tk.Label(main_frame, text=title_text,
                             font=("Arial", 14, "bold"),
                             fg=self.colors['accent'],
                             bg=self.colors['bg'])
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Acción principal
        self.action_label = tk.Label(main_frame, text="ANALIZANDO...",
                                   font=("Arial", 24, "bold"),
                                   fg="white",
                                   bg=self.colors['bg'])
        self.action_label.grid(row=1, column=0, pady=5)
        
        # Tamaño de apuesta
        self.size_label = tk.Label(main_frame, text="",
                                 font=("Arial", 18),
                                 fg=self.colors['accent'],
                                 bg=self.colors['bg'])
        self.size_label.grid(row=2, column=0, pady=5)
        
        # Razón/Explicación
        self.reason_label = tk.Label(main_frame, text="Inicializando sistema...",
                                   font=("Arial", 10),
                                   fg="white",
                                   bg=self.colors['bg'],
                                   wraplength=380,
                                   justify="left")
        self.reason_label.grid(row=3, column=0, pady=10)
        
        # Alternativas
        self.alternatives_label = tk.Label(main_frame, text="",
                                         font=("Arial", 9, "italic"),
                                         fg="#CCCCCC",
                                         bg=self.colors['bg'],
                                         wraplength=380,
                                         justify="left")
        self.alternatives_label.grid(row=4, column=0, pady=5)
        
        # Información adicional
        info_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        info_frame.grid(row=5, column=0, pady=10)
        
        # Confianza
        self.confidence_label = tk.Label(info_frame, text="Confianza: --%",
                                       font=("Arial", 9),
                                       fg="#90EE90",
                                       bg=self.colors['bg'])
        self.confidence_label.pack(side="left", padx=10)
        
        # Tiempo
        self.timer_label = tk.Label(info_frame, text="⏱ 00:00",
                                  font=("Arial", 9),
                                  fg="#ADD8E6",
                                  bg=self.colors['bg'])
        self.timer_label.pack(side="left", padx=10)
        
        # Botones de control
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.grid(row=6, column=0, pady=(10, 0))
        
        # Botón para mover
        move_btn = tk.Button(control_frame, text="📌 Mover",
                           command=self.toggle_movable,
                           font=("Arial", 8),
                           bg="#444444",
                           fg="white",
                           relief="flat",
                           padx=5)
        move_btn.pack(side="left", padx=2)
        
        # Botón para ocultar
        hide_btn = tk.Button(control_frame, text="👁 Ocultar",
                           command=self.hide,
                           font=("Arial", 8),
                           bg="#444444",
                           fg="white",
                           relief="flat",
                           padx=5)
        hide_btn.pack(side="left", padx=2)
        
        # Botón para salir
        exit_btn = tk.Button(control_frame, text="❌ Salir",
                           command=self.close,
                           font=("Arial", 8),
                           bg="#8B0000",
                           fg="white",
                           relief="flat",
                           padx=5)
        exit_btn.pack(side="left", padx=2)
        
        # Configurar grid weights
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Hacer ventana arrastrable
        self.make_draggable()
    
    def make_draggable(self):
        """Hacer la ventana arrastrable"""
        def start_drag(event):
            self.window.x = event.x
            self.window.y = event.y
        
        def drag(event):
            deltax = event.x - self.window.x
            deltay = event.y - self.window.y
            x = self.window.winfo_x() + deltax
            y = self.window.winfo_y() + deltay
            self.window.geometry(f"+{x}+{y}")
        
        # Bind eventos a la ventana
        self.window.bind("<ButtonPress-1>", start_drag)
        self.window.bind("<B1-Motion>", drag)
    
    def toggle_movable(self):
        """Alternar entre modo móvil y fijo"""
        if self.window.attributes('-alpha') == 0.3:
            self.window.attributes('-alpha', 0.9)
        else:
            self.window.attributes('-alpha', 0.3)
    
    def update_decision(self, decision):
        """Actualizar la interfaz con nueva decisión"""
        if not self.is_visible or not self.window:
            return
        
        self.last_decision = decision
        
        # Actualizar acción principal
        action = decision.get('action', 'ANALIZANDO')
        self.action_label.config(text=action)
        
        # Colorear según acción
        action_colors = {
            'RAISE': self.colors['raise_bg'],
            'BET': self.colors['raise_bg'],
            'CALL': self.colors['call_bg'],
            'FOLD': self.colors['fold_bg'],
            'CHECK': self.colors['check_bg'],
            'ALL-IN': self.colors['allin_bg']
        }
        
        color = action_colors.get(action, self.colors['bg'])
        self.action_label.config(bg=color)
        
        # Actualizar tamaño
        size = decision.get('size', '')
        if size:
            self.size_label.config(text=f"Tamaño: {size}")
        else:
            self.size_label.config(text="")
        
        # Actualizar razón
        reason = decision.get('reason', '')
        self.reason_label.config(text=reason)
        
        # Actualizar alternativas
        alternatives = decision.get('alternatives', [])
        if alternatives:
            alt_text = f"Alternativas: {', '.join(alternatives)}"
            self.alternatives_label.config(text=alt_text)
        else:
            self.alternatives_label.config(text="")
        
        # Actualizar confianza
        confidence = decision.get('confidence', 0)
        confidence_color = "#90EE90" if confidence > 70 else "#FFB6C1" if confidence > 40 else "#FFA07A"
        self.confidence_label.config(
            text=f"Confianza: {confidence}%",
            fg=confidence_color
        )
        
        # Resetear timer
        self.timer_seconds = 0
        
        # Forzar actualización
        self.window.update()
    
    def update_timer(self):
        """Actualizar el timer cada segundo"""
        if hasattr(self, 'timer_seconds'):
            self.timer_seconds += 1
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.timer_label.config(text=f"⏱ {minutes:02d}:{seconds:02d}")
        
        # Programar próxima actualización
        if self.window:
            self.window.after(1000, self.update_timer)
    
    def hide(self):
        """Ocultar la ventana"""
        if self.window:
            self.window.withdraw()
            self.is_visible = False
    
    def close(self):
        """Cerrar la ventana"""
        if self.window:
            self.window.quit()
            self.window.destroy()
            self.is_visible = False
    
    def run(self):
        """Mantener la ventana abierta (para versiones simples)"""
        if not self.is_visible:
            self.show()


class SimpleOverlay:
    """Versión simplificada del overlay para inicio rápido"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_simple_overlay()
        
    def setup_simple_overlay(self):
        """Configurar overlay simplificado"""
        self.root.title("Poker Coach Pro")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.geometry("300x200+100+100")
        self.root.configure(bg='#0A1E32', bd=2, relief='solid')
        
        # Título
        title = tk.Label(self.root, text="POKER COACH", 
                        font=("Arial", 14, "bold"),
                        fg="#FFD700", bg="#0A1E32")
        title.pack(pady=10)
        
        # Recomendación
        self.reco_label = tk.Label(self.root, text="CARGANDO...",
                                 font=("Arial", 20, "bold"),
                                 fg="white", bg="#8B0000")
        self.reco_label.pack(pady=20)
        
        # Información
        self.info_label = tk.Label(self.root, text="Iniciando sistema...",
                                 font=("Arial", 10),
                                 fg="white", bg="#0A1E32")
        self.info_label.pack()
        
        # Hacer arrastrable
        self.make_draggable_simple()
        
    def make_draggable_simple(self):
        """Hacer ventana arrastrable (versión simple)"""
        def start_drag(event):
            self.root.x = event.x
            self.root.y = event.y
        
        def drag(event):
            x = self.root.winfo_x() + event.x - self.root.x
            y = self.root.winfo_y() + event.y - self.root.y
            self.root.geometry(f"+{x}+{y}")
        
        self.root.bind("<ButtonPress-1>", start_drag)
        self.root.bind("<B1-Motion>", drag)
    
    def update(self, action="FOLD", reason=""):
        """Actualizar overlay simple"""
        self.reco_label.config(text=action)
        self.info_label.config(text=reason[:50])
        self.root.update()
    
    def run(self):
        """Ejecutar overlay simple"""
        try:
            self.root.mainloop()
        except:
            pass