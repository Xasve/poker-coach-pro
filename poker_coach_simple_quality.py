#!/usr/bin/env python3
"""
Poker Coach Pro - Versión SIMPLE con validación de calidad
Funciona SIN errores
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from datetime import datetime
import json

class SimpleQualityValidator:
    """Validador de calidad SIMPLE integrado"""
    
    def __init__(self):
        self.stats = {
            'total': 0,
            'excellent': 0, 'good': 0, 'acceptable': 0,
            'questionable': 0, 'bad': 0
        }
        self.history = []
    
    def validate_decision(self, street, position, hand_cards, action, size=""):
        """Validar decisión de manera simple"""
        
        # Convertir cartas a formato legible
        hand_str = self.format_hand(hand_cards)
        
        # Puntuación base
        score = 70
        
        # Análisis
        strengths = []
        weaknesses = []
        suggestions = []
        
        # 1. Análisis preflop
        if street == "preflop":
            # Evaluar mano
            hand_strength = self.evaluate_hand_strength(hand_cards)
            
            # Rangos por posición
            if position == "UTG":
                if hand_strength > 0.7:  # Mano premium
                    if action == "RAISE":
                        strengths.append("Mano premium, raise correcto desde UTG")
                        score += 20
                    else:
                        weaknesses.append("Mano premium debería raise desde UTG")
                        score -= 20
                elif hand_strength < 0.3:  # Mano débil
                    if action == "FOLD":
                        strengths.append("Mano débil, fold correcto desde UTG")
                        score += 15
                    else:
                        weaknesses.append("Mano débil no debería jugarse desde UTG")
                        score -= 15
            
            elif position == "BTN":
                if hand_strength > 0.5:  # Mano decente
                    if action == "RAISE":
                        strengths.append("Mano decente, raise correcto desde BTN")
                        score += 15
                elif hand_strength < 0.2:  # Mano muy débil
                    if action != "FOLD":
                        weaknesses.append("Mano muy débil desde BTN, considerar fold")
                        score -= 10
        
        # 2. Validar tamaño de apuesta
        if action in ["RAISE", "BET"] and size:
            sizing_score = self.validate_sizing(street, position, size)
            score += sizing_score
            
            if sizing_score > 5:
                strengths.append("Tamaño de apuesta adecuado")
            elif sizing_score < -5:
                weaknesses.append("Tamaño de apuesta podría mejorarse")
        
        # 3. Validar acciones básicas
        if action == "FOLD" and street == "preflop" and position == "BTN":
            suggestions.append("Desde BTN considera jugar más manos")
            score -= 5
        
        if action == "CALL" and street == "preflop" and position == "UTG":
            suggestions.append("Desde UTG, fold o raise, evitar call")
            score -= 10
        
        # Calcular calidad final
        score = max(0, min(100, score))
        
        quality = self.score_to_quality(score)
        
        # Actualizar estadísticas
        self.update_stats(quality)
        
        # Guardar en historial
        self.save_to_history(street, position, hand_str, action, size, quality, score)
        
        return {
            'quality': quality,
            'score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions
        }
    
    def format_hand(self, cards):
        """Formatear mano para display"""
        if not cards:
            return ""
        return " ".join(cards[:2]) if len(cards) >= 2 else cards[0]
    
    def evaluate_hand_strength(self, cards):
        """Evaluar fuerza de mano simple (0-1)"""
        if not cards or len(cards) < 2:
            return 0.0
        
        # Valores de cartas
        values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            values[str(i)] = i
        
        card1 = cards[0] if len(cards) > 0 else ''
        card2 = cards[1] if len(cards) > 1 else ''
        
        if not card1 or not card2:
            return 0.0
        
        val1 = values.get(card1[0].upper(), 0)
        val2 = values.get(card2[0].upper(), 0)
        
        # Fuerza base
        strength = max(val1, val2) / 14
        
        # Bonus por pareja
        if card1[0].upper() == card2[0].upper():
            strength += 0.2
        
        # Bonus por suited
        if len(card1) > 1 and len(card2) > 1 and card1[-1] == card2[-1]:
            strength += 0.1
        
        return min(1.0, strength)
    
    def validate_sizing(self, street, position, size_str):
        """Validar tamaño de apuesta"""
        
        # Extraer número
        try:
            if 'BB' in size_str:
                size = float(size_str.replace('BB', '').strip())
            elif '%' in size_str:
                size = float(size_str.replace('%', '').strip()) / 100
            else:
                return 0
        except:
            return 0
        
        # Tamaños estándar
        if street == "preflop":
            if position == "UTG":
                optimal = 2.2
            elif position == "BTN":
                optimal = 2.2
            else:
                optimal = 2.2
            
            if abs(size - optimal) < 0.3:
                return 10
            elif abs(size - optimal) < 0.5:
                return 5
            else:
                return -5
        
        return 0
    
    def score_to_quality(self, score):
        """Convertir puntuación a calidad"""
        if score >= 90:
            return "EXCELENTE"
        elif score >= 75:
            return "BUENA"
        elif score >= 60:
            return "ACEPTABLE"
        elif score >= 40:
            return "CUESTIONABLE"
        else:
            return "MALA"
    
    def update_stats(self, quality):
        """Actualizar estadísticas"""
        self.stats['total'] += 1
        
        if quality == "EXCELENTE":
            self.stats['excellent'] += 1
        elif quality == "BUENA":
            self.stats['good'] += 1
        elif quality == "ACEPTABLE":
            self.stats['acceptable'] += 1
        elif quality == "CUESTIONABLE":
            self.stats['questionable'] += 1
        elif quality == "MALA":
            self.stats['bad'] += 1
    
    def save_to_history(self, street, position, hand, action, size, quality, score):
        """Guardar en historial"""
        record = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'street': street,
            'position': position,
            'hand': hand,
            'action': action,
            'size': size,
            'quality': quality,
            'score': score
        }
        self.history.append(record)
    
    def get_stats_report(self):
        """Obtener reporte de estadísticas"""
        total = self.stats['total']
        
        if total == 0:
            return "No hay decisiones validadas aún"
        
        report = []
        report.append("=" * 40)
        report.append("📊 ESTADÍSTICAS DE CALIDAD")
        report.append("=" * 40)
        report.append(f"Total decisiones: {total}")
        
        for quality in ['excellent', 'good', 'acceptable', 'questionable', 'bad']:
            count = self.stats[quality]
            percentage = (count / total * 100) if total > 0 else 0
            report.append(f"{quality.capitalize():12} {count:3} ({percentage:5.1f}%)")
        
        # Calcular promedio
        if self.history:
            avg_score = sum(r['score'] for r in self.history) / len(self.history)
            report.append(f"\nPuntuación promedio: {avg_score:.1f}/100")
        
        report.append("=" * 40)
        
        return "\n".join(report)

class PokerCoachSimpleQuality:
    """Poker Coach con validación simple integrada"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poker Coach Pro - Con Validación Simple")
        self.window.geometry("800x600")
        
        # Validador
        self.validator = SimpleQualityValidator()
        
        # Variables
        self.streets = ["preflop", "flop", "turn", "river"]
        self.positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        self.actions = ["FOLD", "CHECK", "CALL", "BET", "RAISE", "ALL-IN"]
        
        self.current_validation = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz"""
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="🎴 POKER COACH PRO - VALIDACIÓN DE CALIDAD", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        # Frame para controles
        controls_frame = ttk.LabelFrame(main_frame, text="Configurar Situación", padding=10)
        controls_frame.pack(fill='x', pady=10)
        
        # Calle
        ttk.Label(controls_frame, text="Calle:").grid(row=0, column=0, padx=5, pady=5)
        self.street_var = tk.StringVar(value="preflop")
        street_combo = ttk.Combobox(controls_frame, textvariable=self.street_var,
                                   values=self.streets, width=10, state='readonly')
        street_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Posición
        ttk.Label(controls_frame, text="Posición:").grid(row=0, column=2, padx=5, pady=5)
        self.position_var = tk.StringVar(value="BTN")
        position_combo = ttk.Combobox(controls_frame, textvariable=self.position_var,
                                     values=self.positions, width=8, state='readonly')
        position_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Cartas
        ttk.Label(controls_frame, text="Tus cartas:").grid(row=0, column=4, padx=5, pady=5)
        self.cards_var = tk.StringVar(value="Ah Ks")
        cards_entry = ttk.Entry(controls_frame, textvariable=self.cards_var, width=10)
        cards_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Botón para situación aleatoria
        ttk.Button(controls_frame, text="🎲 Situación Aleatoria", 
                  command=self.random_situation).grid(row=0, column=6, padx=10, pady=5)
        
        # Frame para decisión
        decision_frame = ttk.LabelFrame(main_frame, text="Tomar Decisión", padding=10)
        decision_frame.pack(fill='x', pady=10)
        
        # Botones de acción
        action_frame = ttk.Frame(decision_frame)
        action_frame.pack(pady=10)
        
        for i, action in enumerate(self.actions):
            btn = ttk.Button(action_frame, text=action, width=10,
                            command=lambda a=action: self.set_action(a))
            btn.grid(row=0, column=i, padx=2)
        
        # Tamaño de apuesta
        size_frame = ttk.Frame(decision_frame)
        size_frame.pack(pady=10)
        
        ttk.Label(size_frame, text="Tamaño:").pack(side='left', padx=5)
        self.size_var = tk.StringVar(value="2.2BB")
        size_entry = ttk.Entry(size_frame, textvariable=self.size_var, width=10)
        size_entry.pack(side='left', padx=5)
        
        # Botones principales
        button_frame = ttk.Frame(decision_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="✅ Validar Calidad", 
                  command=self.validate_quality, width=20).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="📊 Ver Estadísticas", 
                  command=self.show_stats, width=20).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🔄 Nueva Mano", 
                  command=self.new_hand, width=20).pack(side='left', padx=5)
        
        # Display de resultado
        result_frame = ttk.LabelFrame(main_frame, text="Resultado de Validación", padding=10)
        result_frame.pack(fill='both', expand=True, pady=10)
        
        # Calidad
        self.quality_label = ttk.Label(result_frame, text="Calidad: --", 
                                      font=('Arial', 14, 'bold'))
        self.quality_label.pack(pady=10)
        
        # Puntuación
        self.score_label = ttk.Label(result_frame, text="Puntuación: --/100")
        self.score_label.pack(pady=5)
        
        # Frame para detalles
        details_frame = ttk.Frame(result_frame)
        details_frame.pack(fill='both', expand=True, pady=10)
        
        # Text area para detalles
        self.details_text = tk.Text(details_frame, height=10, width=60,
                                   font=('Arial', 10), wrap='word')
        scrollbar = ttk.Scrollbar(details_frame, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)
        
        self.details_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar colores iniciales
        self.update_quality_display("--", 0)
    
    def random_situation(self):
        """Generar situación aleatoria"""
        # Calles
        self.street_var.set(random.choice(self.streets))
        
        # Posiciones
        self.position_var.set(random.choice(self.positions))
        
        # Cartas aleatorias
        values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['h', 'd', 'c', 's']
        
        card1 = random.choice(values) + random.choice(suits)
        card2 = random.choice(values) + random.choice(suits)
        
        self.cards_var.set(f"{card1} {card2}")
        
        # Acción aleatoria
        self.set_action(random.choice(self.actions))
        
        # Tamaño aleatorio
        if self.street_var.get() == "preflop":
            self.size_var.set(f"{random.uniform(2.0, 2.5):.1f}BB")
        else:
            self.size_var.set(f"{random.randint(25, 75)}% pot")
        
        # Limpiar resultado anterior
        self.clear_result()
    
    def set_action(self, action):
        """Establecer acción"""
        self.current_action = action
        
        # Habilitar/deshabilitar tamaño según acción
        if action in ["BET", "RAISE"]:
            self.size_var.set("2.2BB" if self.street_var.get() == "preflop" else "33% pot")
        else:
            self.size_var.set("")
    
    def validate_quality(self):
        """Validar calidad de la decisión"""
        
        # Obtener datos
        street = self.street_var.get()
        position = self.position_var.get()
        cards = self.cards_var.get().split()
        action = self.current_action if hasattr(self, 'current_action') else "FOLD"
        size = self.size_var.get()
        
        # Validar
        validation = self.validator.validate_decision(street, position, cards, action, size)
        self.current_validation = validation
        
        # Actualizar display
        self.update_quality_display(validation['quality'], validation['score'])
        
        # Mostrar detalles
        self.show_validation_details(validation)
    
    def update_quality_display(self, quality, score):
        """Actualizar display de calidad"""
        
        # Colores según calidad
        colors = {
            "EXCELENTE": "#4CAF50",  # Verde
            "BUENA": "#2196F3",      # Azul
            "ACEPTABLE": "#FFC107",  # Amarillo
            "CUESTIONABLE": "#FF9800", # Naranja
            "MALA": "#F44336",       # Rojo
            "--": "#757575"          # Gris
        }
        
        color = colors.get(quality, "#757575")
        
        self.quality_label.config(text=f"Calidad: {quality}", foreground=color)
        self.score_label.config(text=f"Puntuación: {score}/100")
    
    def show_validation_details(self, validation):
        """Mostrar detalles de validación"""
        
        self.details_text.delete(1.0, tk.END)
        
        # Construir texto
        text = f"Puntuación: {validation['score']}/100\n"
        text += f"Calidad: {validation['quality']}\n\n"
        
        if validation.get('strengths'):
            text += "✅ FORTALEZAS:\n"
            for strength in validation['strengths']:
                text += f"• {strength}\n"
            text += "\n"
        
        if validation.get('weaknesses'):
            text += "⚠️  DEBILIDADES:\n"
            for weakness in validation['weaknesses']:
                text += f"• {weakness}\n"
            text += "\n"
        
        if validation.get('suggestions'):
            text += "💡 SUGERENCIAS:\n"
            for suggestion in validation['suggestions']:
                text += f"• {suggestion}\n"
        
        if not validation.get('strengths') and not validation.get('weaknesses') and not validation.get('suggestions'):
            text += "No se encontraron análisis específicos para esta situación."
        
        self.details_text.insert(1.0, text)
        self.details_text.config(state='normal')
    
    def show_stats(self):
        """Mostrar estadísticas"""
        report = self.validator.get_stats_report()
        
        # Crear ventana para estadísticas
        stats_window = tk.Toplevel(self.window)
        stats_window.title("📊 Estadísticas de Calidad")
        stats_window.geometry("400x400")
        
        # Text widget para mostrar reporte
        text_widget = tk.Text(stats_window, wrap='word', font=('Arial', 10))
        text_widget.insert(1.0, report)
        text_widget.config(state='disabled')
        
        scrollbar = ttk.Scrollbar(stats_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Botón para cerrar
        ttk.Button(stats_window, text="Cerrar", 
                  command=stats_window.destroy).pack(pady=10)
    
    def new_hand(self):
        """Nueva mano"""
        self.random_situation()
        self.clear_result()
    
    def clear_result(self):
        """Limpiar resultado anterior"""
        self.update_quality_display("--", 0)
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, "Haz clic en 'Validar Calidad' para analizar tu decisión.")
    
    def run(self):
        """Ejecutar aplicación"""
        self.window.mainloop()

def main():
    """Función principal"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║  POKER COACH PRO - VALIDACIÓN SIMPLE ║
    ║      Versión que SÍ funciona         ║
    ╚══════════════════════════════════════╝
    """)
    
    print("🚀 Iniciando aplicación...")
    print("💡 Usa 'Situación Aleatoria' para generar diferentes situaciones")
    print("🎯 Luego selecciona una acción y haz clic en 'Validar Calidad'")
    print("📊 Usa 'Ver Estadísticas' para ver tu progreso\n")
    
    app = PokerCoachSimpleQuality()
    app.run()

if __name__ == "__main__":
    main()