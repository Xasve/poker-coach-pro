#!/usr/bin/env python3
"""
Poker Coach Pro con sistema de calidad integrado
Versión mejorada con validación en tiempo real
"""

import tkinter as tk
from tkinter import ttk
import random
import time
import json
from datetime import datetime
import sys
import os

# Agregar src al path si existe
if os.path.exists("src"):
    sys.path.append("src")

class PokerCoachWithQuality:
    """Poker Coach con sistema de validación de calidad"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Poker Coach Pro - Con Validación de Calidad")
        self.window.attributes('-topmost', True)
        self.window.geometry("900x700")
        
        # Intentar cargar el validador
        self.validator = self.load_validator()
        
        # Historial de decisiones
        self.decision_history = []
        self.quality_stats = {
            'total': 0,
            'excellent': 0,
            'good': 0,
            'acceptable': 0,
            'questionable': 0,
            'bad': 0
        }
        
        self.setup_ui()
        
    def load_validator(self):
        """Cargar validador de decisiones"""
        try:
            # Intentar importar desde src/quality
            from quality.decision_validator import DecisionValidator
            print("✅ Sistema de validación de calidad cargado")
            return DecisionValidator(platform="ggpoker")
        except ImportError:
            print("⚠️  Sistema de validación no disponible")
            print("📦 Ejecuta: pip install -r requirements.txt")
            return None
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Coach principal
        coach_tab = ttk.Frame(notebook)
        notebook.add(coach_tab, text='🎴 Coach Principal')
        self.setup_coach_tab(coach_tab)
        
        # Pestaña 2: Validación de calidad
        if self.validator:
            quality_tab = ttk.Frame(notebook)
            notebook.add(quality_tab, text='📊 Validación')
            self.setup_quality_tab(quality_tab)
        
        # Pestaña 3: Historial
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text='📋 Historial')
        self.setup_history_tab(history_tab)
        
        # Pestaña 4: Aprendizaje
        learn_tab = ttk.Frame(notebook)
        notebook.add(learn_tab, text='🎓 Aprendizaje')
        self.setup_learn_tab(learn_tab)
        
    def setup_coach_tab(self, parent):
        """Configurar pestaña del coach"""
        
        # Frame superior: Información del juego
        game_frame = ttk.LabelFrame(parent, text="Información del Juego", padding=10)
        game_frame.pack(fill='x', padx=10, pady=10)
        
        # Controles para simular diferentes situaciones
        controls_frame = ttk.Frame(game_frame)
        controls_frame.pack(fill='x', pady=5)
        
        # Calle
        ttk.Label(controls_frame, text="Calle:").grid(row=0, column=0, padx=5)
        self.street_var = tk.StringVar(value="preflop")
        street_combo = ttk.Combobox(controls_frame, textvariable=self.street_var,
                                   values=["preflop", "flop", "turn", "river"],
                                   width=10, state='readonly')
        street_combo.grid(row=0, column=1, padx=5)
        
        # Posición
        ttk.Label(controls_frame, text="Posición:").grid(row=0, column=2, padx=5)
        self.position_var = tk.StringVar(value="BTN")
        position_combo = ttk.Combobox(controls_frame, textvariable=self.position_var,
                                     values=["UTG", "MP", "CO", "BTN", "SB", "BB"],
                                     width=8, state='readonly')
        position_combo.grid(row=0, column=3, padx=5)
        
        # Cartas
        ttk.Label(controls_frame, text="Tus cartas:").grid(row=0, column=4, padx=5)
        self.cards_var = tk.StringVar(value="Ah Ks")
        cards_entry = ttk.Entry(controls_frame, textvariable=self.cards_var, width=10)
        cards_entry.grid(row=0, column=5, padx=5)
        
        # Botón para generar situación aleatoria
        ttk.Button(controls_frame, text="Situación Aleatoria", 
                  command=self.random_situation).grid(row=0, column=6, padx=10)
        
        # Display de situación actual
        situation_frame = ttk.Frame(game_frame)
        situation_frame.pack(fill='x', pady=10)
        
        self.situation_label = ttk.Label(situation_frame, 
                                        text="Preflop | BTN | Cartas: Ah Ks",
                                        font=('Arial', 10, 'bold'))
        self.situation_label.pack()
        
        # Display de decisión
        decision_frame = ttk.LabelFrame(parent, text="Recomendación", padding=20)
        decision_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.decision_label = ttk.Label(decision_frame, text="ANALIZANDO...",
                                       font=('Arial', 32, 'bold'))
        self.decision_label.pack(pady=20)
        
        self.size_label = ttk.Label(decision_frame, text="",
                                   font=('Arial', 20))
        self.size_label.pack()
        
        self.reason_label = ttk.Label(decision_frame, text="",
                                     font=('Arial', 12), wraplength=600,
                                     justify='center')
        self.reason_label.pack(pady=20)
        
        # Frame para botones
        button_frame = ttk.Frame(decision_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="🔍 Analizar Mano", 
                  command=self.analyze_hand, width=20).pack(side='left', padx=10)
        
        ttk.Button(button_frame, text="🎯 Validar Calidad", 
                  command=self.validate_quality, width=20).pack(side='left', padx=10)
        
        ttk.Button(button_frame, text="🔄 Siguiente Mano", 
                  command=self.next_hand, width=20).pack(side='left', padx=10)
        
        # Información de calidad si hay validador
        if self.validator:
            quality_frame = ttk.Frame(parent)
            quality_frame.pack(fill='x', padx=10, pady=10)
            
            self.quality_label = ttk.Label(quality_frame, text="Calidad: --")
            self.quality_label.pack(side='left', padx=10)
            
            self.score_label = ttk.Label(quality_frame, text="Puntuación: --/100")
            self.score_label.pack(side='left', padx=10)
    
    def setup_quality_tab(self, parent):
        """Configurar pestaña de validación de calidad"""
        
        # Frame para estadísticas
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas de Calidad", padding=10)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Treeview para mostrar métricas
        columns = ('Métrica', 'Valor', 'Descripción')
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', 
                                 command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame para últimas validaciones
        recent_frame = ttk.LabelFrame(parent, text="Últimas Validaciones", padding=10)
        recent_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview para validaciones recientes
        recent_columns = ('Hora', 'Situación', 'Decisión', 'Calidad', 'Puntuación')
        self.recent_tree = ttk.Treeview(recent_frame, columns=recent_columns, 
                                       show='headings', height=10)
        
        for col in recent_columns:
            self.recent_tree.heading(col, text=col)
        
        self.recent_tree.column('Hora', width=80)
        self.recent_tree.column('Situación', width=100)
        self.recent_tree.column('Decisión', width=100)
        self.recent_tree.column('Calidad', width=100)
        self.recent_tree.column('Puntuación', width=80)
        
        # Scrollbar
        recent_scrollbar = ttk.Scrollbar(recent_frame, orient='vertical',
                                        command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=recent_scrollbar.set)
        
        self.recent_tree.pack(side='left', fill='both', expand=True)
        recent_scrollbar.pack(side='right', fill='y')
        
        # Botón para actualizar
        ttk.Button(parent, text="Actualizar Estadísticas", 
                  command=self.update_quality_stats).pack(pady=10)
    
    def setup_history_tab(self, parent):
        """Configurar pestaña de historial"""
        
        # Treeview para historial
        columns = ('ID', 'Hora', 'Situación', 'Decisión', 'Calidad', 'Puntuación')
        self.history_tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column('ID', width=50)
        self.history_tree.column('Hora', width=80)
        self.history_tree.column('Situación', width=120)
        self.history_tree.column('Decisión', width=120)
        self.history_tree.column('Calidad', width=100)
        self.history_tree.column('Puntuación', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', 
                                 command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Botones de control
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Exportar Historial", 
                  command=self.export_history).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Limpiar Historial", 
                  command=self.clear_history).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Ver Detalles", 
                  command=self.show_history_details).pack(side='left', padx=5)
    
    def setup_learn_tab(self, parent):
        """Configurar pestaña de aprendizaje"""
        
        # Frame para lecciones
        lessons_frame = ttk.LabelFrame(parent, text="Lecciones de Estrategia", padding=10)
        lessons_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Texto con lecciones
        lessons_text = """
        🎯 LECCIONES DE POKER PROFESIONAL
        
        1. RANGOS POR POSICIÓN (6-max):
           • UTG: 15% de manos (TT+, AQ+, AJs+, KQs)
           • MP: 18% de manos (77+, AT+, KQ, KJs, QJs)
           • CO: 25% de manos (55+, A8+, KT+, QTs, JTs)
           • BTN: 40% de manos (22+, A2+, K9+, Q9+, J9+, T8s+)
           • SB: Juega como BTN pero fold más
           • BB: Defiende 40-50% de manos
        
        2. TAMAÑOS DE APUESTA (GG Poker):
           • Open preflop: 2.2BB
           • 3-bet in position: 3x
           • 3-bet out of position: 3.5x
           • C-bet flop: 33% del pot
           • Turn barrel: 65% del pot
           • River value bet: 70% del pot
        
        3. CONSEJOS CLAVE:
           • En posición, juega MÁS manos
           • Fuera de posición, juega MENOS manos
           • Fold AQo desde UTG en mesas full
           • C-bet el 70% en flops dry
           • En torneos, sé agresivo en burbuja
        
        4. CÁLCULO DE POT ODDS:
           • Pot Odds = Apuesta a pagar / (Pot total + Apuesta a pagar)
           • Ejemplo: Pot $10, apuesta $5 → Odds = 5 / (10+5) = 33%
           • Necesitas >33% de equity para call profitable
        
        5. EQUITY MÍNIMA REQUERIDA:
           • Call preflop: 40%
           • Call flop: 35%
           • Call turn: 30%
           • Call river: 25%
           • Semi-bluff: 25%
           • Value bet: 55%
        """
        
        text_widget = tk.Text(lessons_frame, wrap='word', height=25, width=80,
                             font=('Arial', 10))
        text_widget.insert('1.0', lessons_text)
        text_widget.config(state='disabled')
        
        scrollbar = ttk.Scrollbar(lessons_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def random_situation(self):
        """Generar situación aleatoria"""
        streets = ["preflop", "flop", "turn", "river"]
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]
        
        # Valores de cartas y palos
        values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['h', 'd', 'c', 's']  # hearts, diamonds, clubs, spades
        
        # Generar cartas aleatorias
        card1 = random.choice(values) + random.choice(suits)
        card2 = random.choice(values) + random.choice(suits)
        
        # Actualizar variables
        self.street_var.set(random.choice(streets))
        self.position_var.set(random.choice(positions))
        self.cards_var.set(f"{card1} {card2}")
        
        # Actualizar display
        self.update_situation_display()
    
    def update_situation_display(self):
        """Actualizar display de situación"""
        street = self.street_var.get()
        position = self.position_var.get()
        cards = self.cards_var.get()
        
        display_text = f"{street.upper()} | {position} | Cartas: {cards}"
        self.situation_label.config(text=display_text)
    
    def analyze_hand(self):
        """Analizar la mano actual"""
        
        # Obtener datos de la situación
        street = self.street_var.get()
        position = self.position_var.get()
        cards = self.cards_var.get().split()
        
        # Generar decisión basada en situación
        decision = self.generate_decision(street, position, cards)
        
        # Actualizar display
        self.decision_label.config(text=decision['action'])
        
        # Color según acción
        action_colors = {
            'RAISE': 'red',
            'BET': 'red',
            'CALL': 'orange',
            'FOLD': 'gray',
            'CHECK': 'green',
            'ALL-IN': 'dark red'
        }
        
        color = action_colors.get(decision['action'], 'black')
        self.decision_label.config(foreground=color)
        
        # Actualizar tamaño y razón
        self.size_label.config(text=decision.get('size', ''))
        self.reason_label.config(text=decision.get('reason', ''))
        
        # Guardar decisión actual
        self.current_decision = decision
        self.current_game_state = {
            'street': street,
            'position': position,
            'hero_cards': cards,
            'board_cards': [],
            'pot_size': random.uniform(2, 10),
            'bet_to_call': 0 if street == 'preflop' else random.uniform(0, 5),
            'stack_bb': random.uniform(20, 200),
            'action_to_us': True
        }
    
    def generate_decision(self, street, position, cards):
        """Generar decisión basada en situación"""
        
        # Evaluar fuerza de mano
        hand_strength = self.evaluate_hand_strength(cards)
        
        # Decisiones preflop
        if street == 'preflop':
            if hand_strength > 0.7:
                # Manos premium
                sizes = {'UTG': '2.2BB', 'MP': '2.2BB', 'CO': '2.2BB', 'BTN': '2.2BB', 'SB': '3BB', 'BB': '--'}
                return {
                    'action': 'RAISE',
                    'size': sizes.get(position, '2.2BB'),
                    'reason': f'Mano premium. Open estándar desde {position}.'
                }
            elif hand_strength > 0.4 and position in ['CO', 'BTN']:
                # Manos decentes en posición tardía
                return {
                    'action': 'RAISE',
                    'size': '2.2BB',
                    'reason': f'Mano jugable en posición {position}. Open para robar ciegas.'
                }
            elif hand_strength > 0.3 and position == 'BB':
                # Defensa de BB
                return {
                    'action': 'CALL',
                    'size': '1BB',
                    'reason': 'Defensa de big blind con mano decente.'
                }
            else:
                # Fold
                return {
                    'action': 'FOLD',
                    'size': '',
                    'reason': f'Mano débil para posición {position}. Fold disciplinado.'
                }
        
        # Decisiones postflop (simplificadas)
        else:
            if hand_strength > 0.6:
                return {
                    'action': 'BET',
                    'size': '50% pot',
                    'reason': 'Mano fuerte. Bet por value.'
                }
            elif hand_strength > 0.3:
                return {
                    'action': 'CHECK',
                    'size': '',
                    'reason': 'Mano marginal. Check y ver desarrollo.'
                }
            else:
                return {
                    'action': 'FOLD',
                    'size': '',
                    'reason': 'Mano débil. Fold.'
                }
    
    def evaluate_hand_strength(self, cards):
        """Evaluar fuerza de mano (0-1)"""
        if not cards or len(cards) < 2:
            return 0.0
        
        # Valores de cartas
        values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for i in range(2, 10):
            values[str(i)] = i
        
        # Evaluar las dos primeras cartas
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
        
        # Bonus por conectadas
        if abs(val1 - val2) <= 2:
            strength += 0.05
        
        return min(1.0, strength)
    
    def validate_quality(self):
        """Validar calidad de la decisión actual"""
        
        if not hasattr(self, 'current_decision') or not hasattr(self, 'current_game_state'):
            print("⚠️  Primero analiza una mano")
            return
        
        if not self.validator:
            print("❌ Sistema de validación no disponible")
            return
        
        # Validar decisión
        validation = self.validator.validate_decision(
            self.current_game_state, 
            self.current_decision
        )
        
        # Actualizar display de calidad
        self.quality_label.config(text=f"Calidad: {validation['quality']}")
        self.score_label.config(text=f"Puntuación: {validation['score']}/100")
        
        # Guardar en historial
        self.save_to_history(validation)
        
        # Mostrar detalles en nueva ventana
        self.show_validation_details(validation)
    
    def show_validation_details(self, validation):
        """Mostrar detalles de la validación"""
        
        details_window = tk.Toplevel(self.window)
        details_window.title("Detalles de Validación")
        details_window.geometry("600x500")
        
        # Frame principal
        main_frame = ttk.Frame(details_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Calidad
        calidad_frame = ttk.Frame(main_frame)
        calidad_frame.pack(fill='x', pady=10)
        
        ttk.Label(calidad_frame, text="Calidad:", 
                 font=('Arial', 12, 'bold')).pack(side='left')
        
        calidad_color = {
            'EXCELENTE': 'green',
            'BUENA': '#8BC34A',
            'ACEPTABLE': 'orange',
            'CUESTIONABLE': '#FF9800',
            'MALA': 'red'
        }.get(validation['quality'], 'black')
        
        ttk.Label(calidad_frame, text=validation['quality'],
                 font=('Arial', 12, 'bold'),
                 foreground=calidad_color).pack(side='left', padx=10)
        
        # Puntuación
        ttk.Label(main_frame, text=f"Puntuación: {validation['score']}/100",
                 font=('Arial', 11)).pack(anchor='w', pady=5)
        
        # Fortalezas
        if validation.get('strengths'):
            ttk.Label(main_frame, text="✅ Fortalezas:",
                     font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
            
            for strength in validation['strengths']:
                ttk.Label(main_frame, text=f"• {strength}",
                         wraplength=500, justify='left').pack(anchor='w', padx=20)
        
        # Debilidades
        if validation.get('weaknesses'):
            ttk.Label(main_frame, text="⚠️  Debilidades:",
                     font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
            
            for weakness in validation['weaknesses']:
                ttk.Label(main_frame, text=f"• {weakness}",
                         wraplength=500, justify='left').pack(anchor='w', padx=20)
        
        # Sugerencias
        if validation.get('suggestions'):
            ttk.Label(main_frame, text="💡 Sugerencias:",
                     font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
            
            for suggestion in validation['suggestions']:
                ttk.Label(main_frame, text=f"• {suggestion}",
                         wraplength=500, justify='left').pack(anchor='w', padx=20)
        
        # Botón para cerrar
        ttk.Button(main_frame, text="Cerrar", 
                  command=details_window.destroy).pack(pady=20)
    
    def save_to_history(self, validation):
        """Guardar decisión en historial"""
        
        record = {
            'id': len(self.decision_history) + 1,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'situation': f"{self.street_var.get()} {self.position_var.get()}",
            'decision': self.current_decision['action'],
            'quality': validation['quality'],
            'score': validation['score'],
            'full_validation': validation
        }
        
        self.decision_history.append(record)
        
        # Actualizar estadísticas
        self.quality_stats['total'] += 1
        if validation['quality'] == 'EXCELENTE':
            self.quality_stats['excellent'] += 1
        elif validation['quality'] == 'BUENA':
            self.quality_stats['good'] += 1
        elif validation['quality'] == 'ACEPTABLE':
            self.quality_stats['acceptable'] += 1
        elif validation['quality'] == 'CUESTIONABLE':
            self.quality_stats['questionable'] += 1
        elif validation['quality'] == 'MALA':
            self.quality_stats['bad'] += 1
        
        # Actualizar árbol de historial
        self.update_history_tree()
        
        # Actualizar árbol de validaciones recientes
        self.update_recent_tree()
    
    def update_history_tree(self):
        """Actualizar árbol de historial"""
        
        # Limpiar árbol
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Agregar registros (máximo 50)
        for record in self.decision_history[-50:]:
            self.history_tree.insert('', 'end', values=(
                record['id'],
                record['timestamp'],
                record['situation'],
                record['decision'],
                record['quality'],
                record['score']
            ))
    
    def update_recent_tree(self):
        """Actualizar árbol de validaciones recientes"""
        
        if not hasattr(self, 'recent_tree'):
            return
        
        # Limpiar árbol
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        # Agregar últimos 10 registros
        for record in self.decision_history[-10:]:
            self.recent_tree.insert('', 'end', values=(
                record['timestamp'],
                record['situation'],
                record['decision'],
                record['quality'],
                record['score']
            ))
    
    def update_quality_stats(self):
        """Actualizar estadísticas de calidad"""
        
        if not hasattr(self, 'stats_tree'):
            return
        
        # Limpiar árbol
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Calcular porcentajes
        total = self.quality_stats['total']
        
        if total > 0:
            percentages = {
                'Excelente': self.quality_stats['excellent'] / total * 100,
                'Buena': self.quality_stats['good'] / total * 100,
                'Aceptable': self.quality_stats['acceptable'] / total * 100,
                'Cuestionable': self.quality_stats['questionable'] / total * 100,
                'Mala': self.quality_stats['bad'] / total * 100
            }
            
            # Puntuación promedio
            if self.decision_history:
                avg_score = sum(r['score'] for r in self.decision_history) / len(self.decision_history)
            else:
                avg_score = 0
            
            # Agregar métricas
            metrics = [
                ('Total Decisiones', str(total), 'Número total de decisiones analizadas'),
                ('Puntuación Promedio', f'{avg_score:.1f}/100', 'Puntuación promedio de calidad'),
                ('Excelente', f'{percentages["Excelente"]:.1f}%', 'Decisiones de calidad excelente'),
                ('Buena', f'{percentages["Buena"]:.1f}%', 'Decisiones de calidad buena'),
                ('Aceptable', f'{percentages["Aceptable"]:.1f}%', 'Decisiones de calidad aceptable'),
                ('Cuestionable', f'{percentages["Cuestionable"]:.1f}%', 'Decisiones cuestionables'),
                ('Mala', f'{percentages["Mala"]:.1f}%', 'Decisiones de mala calidad')
            ]
            
            for metric, value, description in metrics:
                self.stats_tree.insert('', 'end', values=(metric, value, description))
    
    def next_hand(self):
        """Generar siguiente mano aleatoria"""
        self.random_situation()
        self.analyze_hand()
        
        # Limpiar validación anterior
        self.quality_label.config(text="Calidad: --")
        self.score_label.config(text="Puntuación: --/100")
    
    def export_history(self):
        """Exportar historial a archivo JSON"""
        try:
            filename = f"poker_decisions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.decision_history, f, indent=2, default=str)
            
            print(f"✅ Historial exportado a: {filename}")
            
        except Exception as e:
            print(f"❌ Error exportando historial: {e}")
    
    def clear_history(self):
        """Limpiar historial"""
        self.decision_history = []
        self.quality_stats = {k: 0 for k in self.quality_stats.keys()}
        self.update_history_tree()
        
        if hasattr(self, 'recent_tree'):
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
        
        if hasattr(self, 'stats_tree'):
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
        
        print("✅ Historial limpiado")
    
    def show_history_details(self):
        """Mostrar detalles del registro seleccionado"""
        selection = self.history_tree.selection()
        
        if not selection:
            print("⚠️  Selecciona un registro del historial")
            return
        
        item = self.history_tree.item(selection[0])
        record_id = item['values'][0]
        
        # Buscar registro completo
        for record in self.decision_history:
            if record['id'] == record_id:
                self.show_record_details(record)
                break
    
    def show_record_details(self, record):
        """Mostrar detalles de un registro"""
        
        details_window = tk.Toplevel(self.window)
        details_window.title(f"Detalles de Decisión #{record['id']}")
        details_window.geometry("700x600")
        
        # Frame principal con scroll
        main_frame = ttk.Frame(details_window)
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Contenido
        ttk.Label(scrollable_frame, text=f"Decisión #{record['id']}",
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(scrollable_frame, text=f"Hora: {record['timestamp']}").pack(anchor='w', padx=20)
        ttk.Label(scrollable_frame, text=f"Situación: {record['situation']}").pack(anchor='w', padx=20)
        ttk.Label(scrollable_frame, text=f"Decisión: {record['decision']}").pack(anchor='w', padx=20)
        
        # Calidad con color
        calidad_color = {
            'EXCELENTE': 'green',
            'BUENA': '#8BC34A',
            'ACEPTABLE': 'orange',
            'CUESTIONABLE': '#FF9800',
            'MALA': 'red'
        }.get(record['quality'], 'black')
        
        ttk.Label(scrollable_frame, text=f"Calidad: {record['quality']}",
                 foreground=calidad_color).pack(anchor='w', padx=20)
        
        ttk.Label(scrollable_frame, text=f"Puntuación: {record['score']}/100").pack(anchor='w', padx=20)
        
        # Detalles de validación si están disponibles
        if 'full_validation' in record:
            validation = record['full_validation']
            
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=20, padx=20)
            
            ttk.Label(scrollable_frame, text="Análisis Detallado:",
                     font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=10)
            
            if validation.get('strengths'):
                ttk.Label(scrollable_frame, text="✅ Fortalezas:",
                         font=('Arial', 10, 'bold')).pack(anchor='w', padx=30, pady=5)
                
                for strength in validation['strengths']:
                    ttk.Label(scrollable_frame, text=f"• {strength}",
                             wraplength=600, justify='left').pack(anchor='w', padx=50)
            
            if validation.get('weaknesses'):
                ttk.Label(scrollable_frame, text="⚠️  Debilidades:",
                         font=('Arial', 10, 'bold')).pack(anchor='w', padx=30, pady=10)
                
                for weakness in validation['weaknesses']:
                    ttk.Label(scrollable_frame, text=f"• {weakness}",
                             wraplength=600, justify='left').pack(anchor='w', padx=50)
            
            if validation.get('suggestions'):
                ttk.Label(scrollable_frame, text="💡 Sugerencias:",
                         font=('Arial', 10, 'bold')).pack(anchor='w', padx=30, pady=10)
                
                for suggestion in validation['suggestions']:
                    ttk.Label(scrollable_frame, text=f"• {suggestion}",
                             wraplength=600, justify='left').pack(anchor='w', padx=50)
        
        # Botón para cerrar
        ttk.Button(scrollable_frame, text="Cerrar",
                  command=details_window.destroy).pack(pady=20)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.window.mainloop()

def main():
    """Función principal"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║  POKER COACH PRO - CON VALIDACIÓN    ║
    ║      Sistema de calidad integrado    ║
    ╚══════════════════════════════════════╝
    """)
    
    print("🚀 Iniciando aplicación...")
    print("📊 Sistema de validación de calidad activado")
    print("🎓 Modo aprendizaje integrado")
    print("\n💡 Usa 'Situación Aleatoria' para practicar diferentes spots")
    print("🔍 Luego haz clic en 'Validar Calidad' para analizar tu decisión")
    
    app = PokerCoachWithQuality()
    app.run()

if __name__ == "__main__":
    main()