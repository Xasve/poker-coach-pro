"""
overlay_gui.py - Interfaz overlay transparente para mostrar recomendaciones
Usa tkinter para crear ventana siempre visible sobre GG Poker
"""

import tkinter as tk
from tkinter import font
import threading
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class Recommendation:
    """Recomendación para mostrar en overlay"""
    action: str  # "FOLD", "CALL", "RAISE", "CHECK", "BET"
    amount: float  # Cantidad si aplica
    confidence: float  # 0.0 a 1.0
    reason: str  # Explicación
    alternatives: List[str]  # Alternativas posibles
    
    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "amount": round(self.amount, 2),
            "confidence": round(self.confidence, 3),
            "reason": self.reason,
            "alternatives": self.alternatives
        }

class PokerOverlay:
    """Ventana overlay transparente para mostrar recomendaciones"""
    
    def __init__(self, position: str = "top_right", theme: str = "dark"):
        """
        Inicializar overlay
        
        Args:
            position: 'top_right', 'top_left', 'bottom_right', 'bottom_left', 'center'
            theme: 'dark' o 'light'
        """
        self.position = position
        self.theme = theme
        self.current_recommendation: Optional[Recommendation] = None
        
        # Configuración de colores por tema
        self.colors = self._get_theme_colors(theme)
        
        # Crear ventana principal
        self.root = tk.Tk()
        self._setup_window()
        
        # Crear widgets
        self._create_widgets()
        
        # Hilo para actualizaciones
        self.update_thread = None
        self.running = True
        
        print(f"✅ Overlay inicializado (posición: {position}, tema: {theme})")
    
    def _get_theme_colors(self, theme: str) -> Dict:
        """Obtener colores según el tema"""
        if theme == "dark":
            return {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "highlight": "#2a2a2a",
                "border": "#333333",
                "fold": "#ff6b6b",
                "call": "#4ecdc4",
                "raise": "#45b7d1",
                "check": "#96ceb4",
                "bet": "#feca57"
            }
        else:  # light theme
            return {
                "bg": "#ffffff",
                "fg": "#333333",
                "highlight": "#f0f0f0",
                "border": "#cccccc",
                "fold": "#ff4757",
                "call": "#2ed573",
                "raise": "#1e90ff",
                "check": "#7bed9f",
                "bet": "#ffa502"
            }
    
    def _setup_window(self):
        """Configurar propiedades de la ventana"""
        # Hacer ventana transparente
        self.root.overrideredirect(True)  # Sin bordes
        self.root.attributes('-topmost', True)  # Siempre visible
        self.root.attributes('-alpha', 0.9)  # Transparencia
        
        # Configurar tamaño
        width, height = 350, 220
        self.root.geometry(f"{width}x{height}")
        
        # Posicionar ventana
        self._position_window(width, height)
        
        # Color de fondo
        self.root.configure(bg=self.colors["bg"])
    
    def _position_window(self, width: int, height: int):
        """Posicionar ventana según configuración"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        positions = {
            "top_right": (screen_width - width - 10, 10),
            "top_left": (10, 10),
            "bottom_right": (screen_width - width - 10, screen_height - height - 50),
            "bottom_left": (10, screen_height - height - 50),
            "center": ((screen_width - width) // 2, (screen_height - height) // 2)
        }
        
        x, y = positions.get(self.position, positions["top_right"])
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Marco principal con borde
        main_frame = tk.Frame(self.root, bg=self.colors["border"], padx=1, pady=1)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Marco interno
        inner_frame = tk.Frame(main_frame, bg=self.colors["bg"], padx=15, pady=15)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.title_label = tk.Label(
            inner_frame,
            text="🎴 POKER COACH PRO",
            font=title_font,
            fg=self.colors["fg"],
            bg=self.colors["bg"]
        )
        self.title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Recomendación principal
        self.recommendation_label = tk.Label(
            inner_frame,
            text="Esperando análisis...",
            font=font.Font(family="Helvetica", size=16, weight="bold"),
            fg=self.colors["fg"],
            bg=self.colors["bg"]
        )
        self.recommendation_label.pack(anchor=tk.W, pady=(5, 5))
        
        # Cantidad (si aplica)
        self.amount_label = tk.Label(
            inner_frame,
            text="",
            font=font.Font(family="Helvetica", size=14),
            fg=self.colors["fg"],
            bg=self.colors["bg"]
        )
        self.amount_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Razón/explicación
        self.reason_label = tk.Label(
            inner_frame,
            text="El sistema está aprendiendo...",
            font=font.Font(family="Helvetica", size=10),
            fg=self.colors["fg"],
            bg=self.colors["bg"],
            wraplength=300,
            justify=tk.LEFT
        )
        self.reason_label.pack(anchor=tk.W, pady=(5, 10))
        
        # Barra de confianza
        confidence_frame = tk.Frame(inner_frame, bg=self.colors["bg"])
        confidence_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.confidence_label = tk.Label(
            confidence_frame,
            text="Confianza: 0%",
            font=font.Font(family="Helvetica", size=9),
            fg=self.colors["fg"],
            bg=self.colors["bg"]
        )
        self.confidence_label.pack(side=tk.LEFT)
        
        self.confidence_bar = tk.Canvas(
            confidence_frame,
            width=200,
            height=10,
            bg=self.colors["highlight"],
            highlightthickness=0
        )
        self.confidence_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Alternativas
        self.alternatives_label = tk.Label(
            inner_frame,
            text="Alternativas: -",
            font=font.Font(family="Helvetica", size=9),
            fg=self.colors["fg"],
            bg=self.colors["bg"],
            wraplength=300,
            justify=tk.LEFT
        )
        self.alternatives_label.pack(anchor=tk.W, pady=(10, 0))
        
        # Contador de manos
        self.hand_counter_label = tk.Label(
            inner_frame,
            text="Manos analizadas: 0",
            font=font.Font(family="Helvetica", size=8),
            fg=self.colors["fg"],
            bg=self.colors["bg"]
        )
        self.hand_counter_label.pack(anchor=tk.E, pady=(10, 0))
    
    def update_recommendation(self, recommendation: Recommendation, hand_count: int = 0):
        """Actualizar overlay con nueva recomendación"""
        self.current_recommendation = recommendation
        
        # Obtener color basado en acción
        action_color = self.colors.get(recommendation.action.lower(), self.colors["fg"])
        
        # Actualizar título con acción
        self.title_label.config(text=f"🎴 POKER COACH - {recommendation.action}")
        
        # Actualizar recomendación principal
        self.recommendation_label.config(
            text=f"{recommendation.action}",
            fg=action_color
        )
        
        # Actualizar cantidad si aplica
        if recommendation.amount > 0:
            self.amount_label.config(text=f"${recommendation.amount:.2f}")
        else:
            self.amount_label.config(text="")
        
        # Actualizar razón
        self.reason_label.config(text=recommendation.reason)
        
        # Actualizar barra de confianza
        confidence_percent = int(recommendation.confidence * 100)
        self.confidence_label.config(text=f"Confianza: {confidence_percent}%")
        
        # Dibujar barra de confianza
        self.confidence_bar.delete("all")
        bar_width = 200 * recommendation.confidence
        
        # Color de barra basado en confianza
        if confidence_percent >= 80:
            bar_color = "#2ecc71"  # Verde
        elif confidence_percent >= 60:
            bar_color = "#f39c12"  # Naranja
        else:
            bar_color = "#e74c3c"  # Rojo
        
        self.confidence_bar.create_rectangle(
            0, 0, bar_width, 10,
            fill=bar_color,
            outline=""
        )
        
        # Actualizar alternativas
        if recommendation.alternatives:
            alt_text = " | ".join(recommendation.alternatives)
            self.alternatives_label.config(text=f"Alternativas: {alt_text}")
        
        # Actualizar contador de manos
        self.hand_counter_label.config(text=f"Manos analizadas: {hand_count}")
    
    def show_waiting_message(self):
        """Mostrar mensaje de espera"""
        self.title_label.config(text="🎴 POKER COACH PRO")
        self.recommendation_label.config(text="Analizando mesa...", fg=self.colors["fg"])
        self.amount_label.config(text="")
        self.reason_label.config(text="Detectando cartas y montos...")
        self.confidence_label.config(text="Confianza: --%")
        self.confidence_bar.delete("all")
        self.alternatives_label.config(text="Alternativas: -")
    
    def show_error_message(self, error: str):
        """Mostrar mensaje de error"""
        self.title_label.config(text="🎴 POKER COACH - ERROR")
        self.recommendation_label.config(text="Error de análisis", fg="#e74c3c")
        self.amount_label.config(text="")
        self.reason_label.config(text=error)
        self.confidence_label.config(text="Confianza: 0%")
        self.confidence_bar.delete("all")
    
    def start(self):
        """Iniciar overlay en hilo separado"""
        self.update_thread = threading.Thread(target=self._run_overlay, daemon=True)
        self.update_thread.start()
    
    def _run_overlay(self):
        """Ejecutar loop principal de tkinter"""
        self.root.mainloop()
    
    def stop(self):
        """Detener overlay"""
        self.running = False
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def save_config(self):
        """Guardar configuración del overlay"""
        config = {
            "position": self.position,
            "theme": self.theme,
            "colors": self.colors
        }
        
        config_path = Path("config/overlay_config.json")
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuración de overlay guardada: {config_path}")

# ============================================================================
# PRUEBAS Y EJEMPLOS
# ============================================================================

def test_overlay():
    """Probar el sistema de overlay"""
    print("🧪 TEST: Poker Overlay GUI")
    print("=" * 60)
    
    try:
        # Crear overlay
        overlay = PokerOverlay(position="top_right", theme="dark")
        
        # Crear recomendaciones de prueba
        test_recommendations = [
            Recommendation(
                action="RAISE",
                amount=5.50,
                confidence=0.85,
                reason="Pareja alta en posición favorable",
                alternatives=["CALL", "FOLD"]
            ),
            Recommendation(
                action="FOLD", 
                amount=0.0,
                confidence=0.65,
                reason="Mano débil fuera de posición",
                alternatives=["CALL", "CHECK"]
            ),
            Recommendation(
                action="CALL",
                amount=2.25,
                confidence=0.92,
                reason="Odds del pot favorables con proyecto de color",
                alternatives=["RAISE", "FOLD"]
            )
        ]
        
        print("✅ Overlay creado")
        print("🎯 Mostrando recomendaciones de prueba...")
        
        # Iniciar overlay en hilo separado
        overlay.start()
        
        # Ciclo de prueba
        hand_count = 0
        for i, recommendation in enumerate(test_recommendations):
            print(f"\n📋 Recomendación {i+1}: {recommendation.action}")
            
            # Actualizar overlay
            overlay.update_recommendation(recommendation, hand_count + i)
            
            # Esperar 3 segundos
            import time
            time.sleep(3)
        
        # Mostrar mensaje de espera
        overlay.show_waiting_message()
        time.sleep(2)
        
        # Guardar configuración
        overlay.save_config()
        
        print("\n✅ Test de overlay completado")
        print("⚠️  Presiona Ctrl+C para cerrar la ventana de overlay")
        
        # Mantener abierto
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Cerrando overlay...")
            overlay.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de overlay: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_overlay()