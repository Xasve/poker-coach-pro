"""
Archivo: quality_dashboard.py
Ruta: src/quality/quality_dashboard.py
Dashboard visual para monitorear calidad de decisiones
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import json

class QualityDashboard:
    """Dashboard visual de calidad de decisiones"""
    
    def __init__(self, decision_validator):
        self.validator = decision_validator
        self.window = None
        
    def show(self):
        """Mostrar dashboard"""
        self.window = tk.Toplevel()
        self.window.title("📊 Dashboard de Calidad - Poker Coach Pro")
        self.window.geometry("1200x800")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interfaz del dashboard"""
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Resumen General
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text='📈 Resumen General')
        self.create_summary_tab(tab1)
        
        # Pestaña 2: Análisis Detallado
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='🔍 Análisis Detallado')
        self.create_analysis_tab(tab2)
        
        # Pestaña 3: Historial
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text='📋 Historial')
        self.create_history_tab(tab3)
        
        # Pestaña 4: Comparación GTO
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text='🎯 Comparación GTO')
        self.create_gto_tab(tab4)
        
        # Pestaña 5: Áreas de Mejora
        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text='⚠️ Áreas de Mejora')
        self.create_improvement_tab(tab5)
        
    def create_summary_tab(self, parent):
        """Crear pestaña de resumen general"""
        
        # Obtener estadísticas
        stats = self.validator.get_validation_stats()
        
        # Frame para métricas principales
        metrics_frame = ttk.Frame(parent)
        metrics_frame.pack(fill='x', padx=20, pady=20)
        
        # Métrica 1: Total decisiones
        self.create_metric_card(
            metrics_frame, 
            "Total Decisiones", 
            str(stats['total_validations']),
            row=0, col=0
        )
        
        # Métrica 2: Puntuación promedio
        self.create_metric_card(
            metrics_frame,
            "Puntuación Promedio",
            f"{stats['average_score']:.1f}/100",
            row=0, col=1
        )
        
        # Métrica 3: Tendencia
        trend_colors = {
            'IMPROVING': 'green',
            'STABLE': 'orange',
            'DECLINING': 'red',
            'INSUFICIENT_DATA': 'gray'
        }
        self.create_metric_card(
            metrics_frame,
            "Tendencia",
            stats['recent_trend'],
            row=0, col=2,
            color=trend_colors.get(stats['recent_trend'], 'black')
        )
        
        # Gráfico de distribución de calidad
        self.create_quality_chart(parent, stats)
        
        # Frame para distribución porcentual
        dist_frame = ttk.LabelFrame(parent, text="Distribución de Calidad", padding=10)
        dist_frame.pack(fill='x', padx=20, pady=10)
        
        for quality, percentage in stats['percentages'].items():
            label = ttk.Label(dist_frame, text=f"{quality.capitalize()}: {percentage:.1f}%")
            label.pack(anchor='w', padx=10, pady=2)
            
            # Barra de progreso
            progress = ttk.Progressbar(dist_frame, length=300, mode='determinate')
            progress['value'] = percentage
            progress.pack(padx=10, pady=2)
    
    def create_analysis_tab(self, parent):
        """Crear pestaña de análisis detallado"""
        
        # Frame para análisis reciente
        recent_frame = ttk.LabelFrame(parent, text="Últimas Decisiones", padding=10)
        recent_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview para mostrar decisiones recientes
        columns = ('#1', '#2', '#3', '#4', '#5', '#6')
        tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=15)
        
        # Definir columnas
        tree.heading('#1', text='Hora')
        tree.heading('#2', text='Situación')
        tree.heading('#3', text='Decisión')
        tree.heading('#4', text='Calidad')
        tree.heading('#5', text='Puntuación')
        tree.heading('#6', text='Análisis')
        
        tree.column('#1', width=80)
        tree.column('#2', width=100)
        tree.column('#3', width=100)
        tree.column('#4', width=100)
        tree.column('#5', width=80)
        tree.column('#6', width=300)
        
        # Agregar datos
        recent_decisions = self.validator.validation_history[-20:]  # Últimas 20
        
        for decision in recent_decisions:
            # Formatear hora
            timestamp = datetime.fromisoformat(decision['timestamp'])
            hora = timestamp.strftime('%H:%M')
            
            # Obtener datos
            game_state = decision['game_state']
            decision_data = decision['decision']
            validation = decision['validation']
            
            # Información de situación
            situacion = f"{game_state.get('street', '')} {game_state.get('position', '')}"
            
            # Información de decisión
            accion = decision_data.get('action', '')
            tamaño = decision_data.get('size', '')
            decision_str = f"{accion} {tamaño}".strip()
            
            # Calidad y puntuación
            calidad = validation.get('quality', '')
            puntuacion = validation.get('score', 0)
            
            # Análisis resumido
            fortalezas = len(validation.get('strengths', []))
            debilidades = len(validation.get('weaknesses', []))
            analisis = f"✓{fortalezas} ✗{debilidades}"
            
            tree.insert('', 'end', values=(
                hora, situacion, decision_str, calidad, puntuacion, analisis
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botón para ver detalles
        def show_details():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                self.show_decision_details(item['values'])
        
        ttk.Button(parent, text="Ver Detalles de Decisión Seleccionada", 
                  command=show_details).pack(pady=10)
    
    def create_history_tab(self, parent):
        """Crear pestaña de historial"""
        
        # Gráfico de evolución temporal
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        history = self.validator.validation_history
        if history:
            timestamps = []
            scores = []
            
            for i, record in enumerate(history[-50:]):  # Últimas 50
                timestamps.append(i)
                scores.append(record['score'])
            
            # Crear gráfico
            ax.plot(timestamps, scores, 'b-', linewidth=2, marker='o', markersize=4)
            ax.axhline(y=90, color='g', linestyle='--', alpha=0.5, label='Excelente (90+)')
            ax.axhline(y=75, color='y', linestyle='--', alpha=0.5, label='Buena (75+)')
            ax.axhline(y=60, color='r', linestyle='--', alpha=0.5, label='Aceptable (60+)')
            
            ax.set_xlabel('Decisiones (recientes →)')
            ax.set_ylabel('Puntuación')
            ax.set_title('Evolución de Calidad de Decisiones')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Embed en Tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
        else:
            label = ttk.Label(parent, text="No hay datos históricos disponibles")
            label.pack(pady=50)
    
    def create_gto_tab(self, parent):
        """Crear pestaña de comparación GTO"""
        
        # Frame para comparaciones
        gto_frame = ttk.Frame(parent)
        gto_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title = ttk.Label(gto_frame, text="Comparación con Estrategia GTO", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Explicación GTO
        explanation = """
        GTO (Game Theory Optimal) es la estrategia perfectamente balanceada
        que no puede ser explotada por los oponentes. 
        
        Comparar con GTO nos ayuda a identificar:
        1. Decisiones demasiado explotables
        2. Rangos desbalanceados  
        3. Frecuencias subóptimas
        4. Oportunidades de explotación
        
        Una buena estrategia mezcla GTO con ajustes explotativos.
        """
        
        ttk.Label(gto_frame, text=explanation, justify='left', 
                 wraplength=800).pack(pady=10)
        
        # Métricas GTO
        metrics = [
            ("RFI Frecuencia", "Frecuencia de Raise First In", "15-25%"),
            ("3-Bet Frecuencia", "Frecuencia de 3-bet vs opens", "8-12%"),
            ("C-Bet Frecuencia", "Continuation bet en flop", "65-75%"),
            ("Check-Raise", "Frecuencia de check-raise", "15-25%"),
            ("Bluff Ratio", "Proporción value:bluff", "2:1")
        ]
        
        for metric, description, gto_range in metrics:
            frame = ttk.Frame(gto_frame)
            frame.pack(fill='x', pady=5)
            
            ttk.Label(frame, text=metric, width=20, anchor='w').pack(side='left')
            ttk.Label(frame, text=description, width=40, anchor='w').pack(side='left')
            ttk.Label(frame, text=gto_range, width=15, anchor='w').pack(side='left')
            
            # Barra de progreso para nuestra frecuencia
            progress = ttk.Progressbar(frame, length=200, mode='determinate')
            progress['value'] = 50  # Placeholder
            progress.pack(side='left', padx=10)
    
    def create_improvement_tab(self, parent):
        """Crear pestaña de áreas de mejora"""
        
        # Obtener debilidades comunes
        weaknesses = []
        for record in self.validator.validation_history[-50:]:
            if 'weaknesses' in record['validation']:
                weaknesses.extend(record['validation']['weaknesses'])
        
        from collections import Counter
        common_weaknesses = Counter(weaknesses).most_common(10)
        
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if common_weaknesses:
            title = ttk.Label(main_frame, text="🔍 Áreas de Mejora Identificadas",
                             font=('Arial', 14, 'bold'))
            title.pack(pady=10)
            
            for i, (weakness, count) in enumerate(common_weaknesses):
                frame = ttk.Frame(main_frame)
                frame.pack(fill='x', pady=5)
                
                # Número y debilidad
                ttk.Label(frame, text=f"{i+1}.", width=3).pack(side='left')
                ttk.Label(frame, text=weakness, wraplength=600, 
                         justify='left').pack(side='left', fill='x', expand=True)
                
                # Frecuencia
                ttk.Label(frame, text=f"({count} veces)", width=10).pack(side='right')
            
            # Recomendaciones de mejora
            ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
            
            rec_title = ttk.Label(main_frame, text="💡 Plan de Mejora Recomendado",
                                 font=('Arial', 12, 'bold'))
            rec_title.pack(pady=10)
            
            recommendations = [
                "1. Estudiar rangos preflop por posición",
                "2. Practicar cálculo de pot odds en tiempo real",
                "3. Analizar hand histories con software específico",
                "4. Estudiar soluciones GTO para spots comunes",
                "5. Jugar sesiones focales en una habilidad a la vez"
            ]
            
            for rec in recommendations:
                ttk.Label(main_frame, text=rec, anchor='w').pack(fill='x', pady=2)
        else:
            ttk.Label(main_frame, text="🎉 ¡No se identificaron áreas de mejora críticas!",
                     font=('Arial', 12, 'bold')).pack(pady=50)
            
            ttk.Label(main_frame, text="Tus decisiones son consistentemente sólidas.",
                     font=('Arial', 10)).pack()
    
    def create_metric_card(self, parent, title, value, row, col, color='black'):
        """Crear tarjeta de métrica"""
        
        frame = ttk.Frame(parent, relief='solid', borderwidth=1)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Título
        ttk.Label(frame, text=title, font=('Arial', 10)).pack(pady=(10, 5))
        
        # Valor
        ttk.Label(frame, text=value, font=('Arial', 24, 'bold'), 
                 foreground=color).pack(pady=5)
        
        # Configurar grid
        parent.columnconfigure(col, weight=1)
    
    def create_quality_chart(self, parent, stats):
        """Crear gráfico de calidad"""
        
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Datos
            labels = ['Excelente', 'Buena', 'Aceptable', 'Cuestionable', 'Mala']
            values = [
                stats['percentages']['excellent'],
                stats['percentages']['good'],
                stats['percentages']['acceptable'],
                stats['percentages']['questionable'],
                stats['percentages']['bad']
            ]
            
            colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
            
            # Crear gráfico de barras
            bars = ax.bar(labels, values, color=colors)
            
            # Agregar valores en las barras
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f'{value:.1f}%', ha='center', va='bottom')
            
            ax.set_ylabel('Porcentaje (%)')
            ax.set_title('Distribución de Calidad de Decisiones')
            ax.set_ylim(0, 100)
            
            # Embed en Tkinter
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='x', padx=20, pady=10)
            
        except ImportError:
            # Fallback si matplotlib no está instalado
            ttk.Label(parent, text="Instala matplotlib para ver gráficos: pip install matplotlib").pack(pady=20)
    
    def show_decision_details(self, decision_data):
        """Mostrar detalles de una decisión específica"""
        
        details_window = tk.Toplevel(self.window)
        details_window.title("Detalles de Decisión")
        details_window.geometry("800x600")
        
        # Buscar decisión completa en el historial
        hora_buscada = decision_data[0]
        
        for record in self.validator.validation_history:
            timestamp = datetime.fromisoformat(record['timestamp'])
            hora = timestamp.strftime('%H:%M')
            
            if hora == hora_buscada:
                self.display_decision_details(details_window, record)
                break
    
    def display_decision_details(self, parent, record):
        """Mostrar detalles completos de una decisión"""
        
        # Frame principal con scroll
        main_frame = ttk.Frame(parent)
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
        game_state = record['game_state']
        decision = record['decision']
        validation = record['validation']
        
        # Sección 1: Información de la situación
        ttk.Label(scrollable_frame, text="📋 INFORMACIÓN DE LA SITUACIÓN", 
                 font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 5))
        
        situacion_info = f"""
        Plataforma: {game_state.get('platform', 'N/A')}
        Calle: {game_state.get('street', 'N/A')}
        Posición: {game_state.get('position', 'N/A')}
        Cartas Hero: {', '.join(game_state.get('hero_cards', []))}
        Cartas Mesa: {', '.join(game_state.get('board_cards', []))}
        Pot: ${game_state.get('pot_size', 0):.2f}
        Stack: {game_state.get('stack_bb', 0):.1f} BB
        Apuesta a Pagar: ${game_state.get('bet_to_call', 0):.2f}
        """
        
        ttk.Label(scrollable_frame, text=situacion_info, justify='left').pack(
            anchor='w', padx=40, pady=5
        )
        
        # Sección 2: Decisión tomada
        ttk.Label(scrollable_frame, text="🎯 DECISIÓN TOMADA", 
                 font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 5))
        
        decision_info = f"""
        Acción: {decision.get('action', 'N/A')}
        Tamaño: {decision.get('size', 'N/A')}
        Confianza: {decision.get('confidence', 'N/A')}%
        Razón: {decision.get('reason', 'N/A')}
        Alternativas: {', '.join(decision.get('alternatives', []))}
        """
        
        ttk.Label(scrollable_frame, text=decision_info, justify='left').pack(
            anchor='w', padx=40, pady=5
        )
        
        # Sección 3: Validación
        ttk.Label(scrollable_frame, text="📊 VALIDACIÓN", 
                 font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 5))
        
        calidad_color = {
            'EXCELENTE': 'green',
            'BUENA': '#8BC34A',
            'ACEPTABLE': 'orange',
            'CUESTIONABLE': '#FF9800',
            'MALA': 'red'
        }.get(validation.get('quality', ''), 'black')
        
        ttk.Label(scrollable_frame, 
                 text=f"Calidad: {validation.get('quality', 'N/A')}",
                 foreground=calidad_color,
                 font=('Arial', 11, 'bold')).pack(anchor='w', padx=40, pady=2)
        
        ttk.Label(scrollable_frame, 
                 text=f"Puntuación: {validation.get('score', 0)}/100").pack(
            anchor='w', padx=40, pady=2
        )
        
        # Fortalezas
        strengths = validation.get('strengths', [])
        if strengths:
            ttk.Label(scrollable_frame, text="✅ Fortalezas:", 
                     font=('Arial', 10, 'bold')).pack(anchor='w', padx=40, pady=(10, 2))
            
            for strength in strengths:
                ttk.Label(scrollable_frame, text=f"  • {strength}", 
                         justify='left').pack(anchor='w', padx=50, pady=1)
        
        # Debilidades
        weaknesses = validation.get('weaknesses', [])
        if weaknesses:
            ttk.Label(scrollable_frame, text="⚠️ Debilidades:", 
                     font=('Arial', 10, 'bold')).pack(anchor='w', padx=40, pady=(10, 2))
            
            for weakness in weaknesses:
                ttk.Label(scrollable_frame, text=f"  • {weakness}", 
                         justify='left').pack(anchor='w', padx=50, pady=1)
        
        # Sugerencias
        suggestions = validation.get('suggestions', [])
        if suggestions:
            ttk.Label(scrollable_frame, text="💡 Sugerencias:", 
                     font=('Arial', 10, 'bold')).pack(anchor='w', padx=40, pady=(10, 2))
            
            for suggestion in suggestions:
                ttk.Label(scrollable_frame, text=f"  • {suggestion}", 
                         justify='left').pack(anchor='w', padx=50, pady=1)
        
        # Análisis de sizing
        if 'sizing_analysis' in validation:
            sizing = validation['sizing_analysis']
            ttk.Label(scrollable_frame, text="📏 Análisis de Tamaño:", 
                     font=('Arial', 10, 'bold')).pack(anchor='w', padx=40, pady=(10, 2))
            
            sizing_info = f"""
            Tamaño actual: {sizing.get('actual', 0):.0f}%
            Rango óptimo: {sizing.get('optimal_min', 0):.0f}-{sizing.get('optimal_max', 0):.0f}%
            Target óptimo: {sizing.get('optimal_target', 0):.0f}%
            """
            
            ttk.Label(scrollable_frame, text=sizing_info, justify='left').pack(
                anchor='w', padx=50, pady=2
            )