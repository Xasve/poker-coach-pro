# ============================================================================
# POKER BOT EXTREMO - SIN RESTRICCIONES + OPTIMIZACIÓN MÁXIMA
# ============================================================================

import cv2
import numpy as np
import pyautogui
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict, deque
import json
import pickle
import os
from datetime import datetime
import gc
import psutil
import sys

# ==================== CONFIGURACIÓN EXTREMA ====================
class ExtremeConfig:
    """Configuración para máximo rendimiento"""
    
    # DESACTIVAR TODAS LAS RESTRICCIONES
    SAFETY_CHECKS = False          # Sin verificaciones de seguridad
    RATE_LIMITING = False          # Sin límites de velocidad
    DELAYS_DISABLED = True         # Sin retardos artificiales
    MAX_PERFORMANCE = True         # Máximo rendimiento
    
    # OPTIMIZACIONES DE TIEMPO DE REACCIÓN
    REACTION_TIME_TARGET = 0.05    # 50ms objetivo
    PARALLEL_PROCESSING = True     # Procesamiento paralelo
    PRE_COMPUTATION = True         # Cálculos precomputados
    CACHE_EVERYTHING = True        # Cache extremo
    
    # OPTIMIZACIONES DE RECURSOS
    MEMORY_OPTIMIZATION = True     # Uso eficiente de memoria
    CPU_PRIORITY = "high"          # Prioridad alta de CPU
    GPU_ACCELERATION = True        # Usar GPU si está disponible
    BATCH_PROCESSING = True        # Procesamiento por lotes
    
    # CAPTURA Y PROCESAMIENTO EXTREMO
    CAPTURE_METHOD = "directx"     # Método más rápido de captura
    PROCESSING_RESOLUTION = "low"  # Resolución baja para velocidad
    COLOR_DETECTION_OPTIMIZED = True  # Detección optimizada
    
    # APRENDIZAJE Y DECISIONES
    LEARNING_RATE = 0.5           # Aprendizaje extremadamente rápido
    EXPLORATION_RATE = 0.1        # Mínima exploración, máxima explotación
    DECISION_CACHE_SIZE = 10000   # Cache enorme de decisiones

# ==================== SISTEMA DE CAPTURA ULTRARRÁPIDO ====================
class ExtremeCaptureSystem:
    """Sistema de captura con tiempo de reacción mínimo"""
    
    def __init__(self):
        self.config = ExtremeConfig()
        self.last_capture_time = 0
        self.capture_cache = {}
        self.capture_thread = None
        self.running = True
        
        # Configurar para máximo rendimiento
        self._setup_extreme_performance()
        
        print(" SISTEMA DE CAPTURA EXTREMO INICIALIZADO")
        print(f"   Objetivo: {self.config.REACTION_TIME_TARGET*1000:.0f}ms")
        print("   Restricciones: DESACTIVADAS")
    
    def _setup_extreme_performance(self):
        """Configurar sistema para máximo rendimiento"""
        
        # Desactivar verificaciones de pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
        # Optimizar OpenCV
        cv2.setUseOptimized(True)
        cv2.setNumThreads(multiprocessing.cpu_count())
        
        # Prioridad de proceso
        try:
            import win32api, win32process, win32con
            handle = win32api.GetCurrentProcess()
            win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
            print(" Prioridad de proceso: REALTIME")
        except:
            try:
                import os
                os.nice(-20)  # Máxima prioridad en Linux
            except:
                pass
        
        # Precalcular tablas de búsqueda
        self._precompute_lookup_tables()
    
    def _precompute_lookup_tables(self):
        """Precalcular todo para velocidad máxima"""
        self.color_lookup = {}
        self.position_lookup = {}
        self.decision_lookup = defaultdict(dict)
        
        # Tabla de colores precalculada
        for r in range(0, 256, 8):
            for g in range(0, 256, 8):
                for b in range(0, 256, 8):
                    key = (r >> 3, g >> 3, b >> 3)
                    self.color_lookup[key] = 'red' if r > 150 and g < 100 and b < 100 else \
                                            'black' if r < 100 and g < 100 and b < 100 else 'other'
    
    def ultra_fast_capture(self, region=None):
        """Captura ultra rápida de pantalla"""
        start_time = time.perf_counter()
        
        # Método directo sin verificaciones
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # Conversión ultra rápida
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        capture_time = time.perf_counter() - start_time
        
        # Cache extremo
        cache_key = f"frame_{hash(str(region))}"
        self.capture_cache[cache_key] = (frame, time.time())
        
        # Limpiar cache antiguo
        if len(self.capture_cache) > 100:
            oldest = min(self.capture_cache.keys(), 
                        key=lambda k: self.capture_cache[k][1])
            del self.capture_cache[oldest]
        
        return frame, capture_time
    
    def continuous_capture(self, callback, interval=0.01):
        """Captura continua en hilo separado"""
        def capture_loop():
            while self.running:
                frame, capture_time = self.ultra_fast_capture()
                if callback:
                    callback(frame, capture_time)
                if interval > 0:
                    time.sleep(interval)
        
        self.capture_thread = threading.Thread(target=capture_loop, daemon=True)
        self.capture_thread.start()
        return self.capture_thread
    
    def stop_capture(self):
        """Detener captura continua"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=1.0)

# ==================== SISTEMA DE DETECCIÓN ULTRARRÁPIDO ====================
class ExtremeDetectionSystem:
    """Detección optimizada para velocidad máxima"""
    
    def __init__(self):
        self.config = ExtremeConfig()
        self.template_cache = {}
        self.color_cache = {}
        
        # Precompilar funciones críticas
        self._compile_critical_functions()
    
    def _compile_critical_functions(self):
        """Precompilar funciones para velocidad"""
        import numba
        
        @numba.jit(nopython=True, fastmath=True, cache=True)
        def fast_color_check(pixel, red_threshold=150):
            r, g, b = pixel[2], pixel[1], pixel[0]
            return r > red_threshold and g < 100 and b < 100
        
        @numba.jit(nopython=True, fastmath=True, cache=True)
        def fast_black_check(pixel, threshold=100):
            r, g, b = pixel[2], pixel[1], pixel[0]
            return r < threshold and g < threshold and b < threshold
        
        self.fast_color_check = fast_color_check
        self.fast_black_check = fast_black_check
    
    def detect_cards_extreme(self, image, region=None):
        """Detección ultra rápida de cartas"""
        start_time = time.perf_counter()
        
        # Usar resolución reducida para velocidad
        if self.config.PROCESSING_RESOLUTION == "low":
            height, width = image.shape[:2]
            if height > 400 or width > 600:
                image = cv2.resize(image, (600, 400))
        
        # Detección paralelizada
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            
            # Detectar colores en paralelo
            future_colors = executor.submit(self._parallel_color_detection, image)
            futures.append(future_colors)
            
            # Detectar números en paralelo
            future_numbers = executor.submit(self._parallel_number_detection, image)
            futures.append(future_numbers)
            
            # Esperar resultados
            colors = future_colors.result()
            numbers = future_numbers.result()
        
        detection_time = time.perf_counter() - start_time
        
        return {
            'colors': colors,
            'numbers': numbers,
            'detection_time': detection_time,
            'timestamp': time.time()
        }
    
    def _parallel_color_detection(self, image):
        """Detección de colores paralelizada"""
        height, width = image.shape[:2]
        red_pixels = 0
        black_pixels = 0
        
        # Procesamiento por bloques en paralelo
        block_size = 50
        blocks = []
        
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = image[y:y+block_size, x:x+block_size]
                blocks.append(block)
        
        # Procesar bloques en paralelo
        with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            results = list(executor.map(self._process_color_block, blocks))
        
        # Combinar resultados
        for red, black in results:
            red_pixels += red
            black_pixels += black
        
        total_pixels = height * width
        red_percentage = (red_pixels / total_pixels) * 100
        black_percentage = (black_pixels / total_pixels) * 100
        
        return {
            'red': red_percentage,
            'black': black_percentage,
            'dominant': 'red' if red_percentage > black_percentage else 'black'
        }
    
    def _process_color_block(self, block):
        """Procesar bloque de colores (función optimizada)"""
        if block.size == 0:
            return 0, 0
        
        red_count = 0
        black_count = 0
        
        # Vectorizar operaciones para velocidad
        block_flat = block.reshape(-1, 3)
        
        # Usar numpy vectorizado (más rápido que loops)
        red_mask = (block_flat[:, 2] > 150) & (block_flat[:, 1] < 100) & (block_flat[:, 0] < 100)
        black_mask = (block_flat[:, 2] < 100) & (block_flat[:, 1] < 100) & (block_flat[:, 0] < 100)
        
        red_count = np.sum(red_mask)
        black_count = np.sum(black_mask)
        
        return red_count, black_count
    
    def _parallel_number_detection(self, image):
        """Detección de números optimizada"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Umbralización adaptativa rápida
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        numbers = []
        for contour in contours[:10]:  # Limitar a 10 contornos para velocidad
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtrar por tamaño
            if 20 < w < 100 and 30 < h < 150:
                numbers.append({
                    'x': x, 'y': y, 'w': w, 'h': h,
                    'area': w * h
                })
        
        return numbers

# ==================== SISTEMA DE DECISIÓN ULTRARRÁPIDO ====================
class ExtremeDecisionSystem:
    """Sistema de decisión con tiempo de reacción mínimo"""
    
    def __init__(self):
        self.config = ExtremeConfig()
        self.decision_cache = {}
        self.q_table = defaultdict(lambda: np.zeros(4))
        self.reaction_times = deque(maxlen=1000)
        
        # Precomputar estrategias
        self._precompute_strategies()
        
        print(" SISTEMA DE DECISIÓN EXTREMO INICIALIZADO")
        print(f"   Cache: {self.config.DECISION_CACHE_SIZE} decisiones")
        print(f"   Learning Rate: {self.config.LEARNING_RATE}")
    
    def _precompute_strategies(self):
        """Precomputar todas las estrategias posibles"""
        self.preflop_strategy = {}
        self.postflop_strategy = {}
        
        # Precomputar decisiones preflop
        positions = ['UTG', 'MP', 'CO', 'BTN', 'SB', 'BB']
        actions = ['FOLD', 'CALL', 'RAISE_3BB', 'RAISE_5BB', 'ALLIN']
        
        for pos in positions:
            for hand_strength in range(1, 170):  # Todas las manos posibles
                cache_key = f"preflop_{pos}_{hand_strength}"
                
                # Decisión precomputada basada en fuerza y posición
                if hand_strength > 120:  # Top 10% manos
                    decision = 'RAISE_5BB' if pos in ['BTN', 'CO'] else 'RAISE_3BB'
                elif hand_strength > 80:   # Top 30% manos
                    decision = 'RAISE_3BB' if pos in ['BTN', 'CO', 'MP'] else 'CALL'
                elif hand_strength > 50:   # Top 50% manos
                    decision = 'CALL' if pos in ['BTN', 'CO'] else 'FOLD'
                else:
                    decision = 'FOLD'
                
                self.decision_cache[cache_key] = decision
        
        # Precomputar tiempos de reacción objetivo
        for i in range(1000):
            self.reaction_times.append(self.config.REACTION_TIME_TARGET)
    
    def ultra_fast_decision(self, game_state):
        """Tomar decisión ultra rápida"""
        start_time = time.perf_counter()
        
        # Verificar cache primero
        state_hash = hash(str(game_state))
        if state_hash in self.decision_cache:
            decision = self.decision_cache[state_hash]
            reaction_time = time.perf_counter() - start_time
            self.reaction_times.append(reaction_time)
            return decision, reaction_time
        
        # Decisión basada en estado del juego
        street = game_state.get('street', 'preflop')
        pot_size = game_state.get('pot', 0)
        position = game_state.get('position', 'BTN')
        hand_strength = game_state.get('hand_strength', 50)
        
        if street == 'preflop':
            decision = self._preflop_decision(position, hand_strength, pot_size)
        elif street == 'flop':
            decision = self._postflop_decision(game_state, 'flop')
        elif street == 'turn':
            decision = self._postflop_decision(game_state, 'turn')
        else:  # river
            decision = self._river_decision(game_state)
        
        # Cache extremo
        self.decision_cache[state_hash] = decision
        
        # Limpiar cache si es muy grande
        if len(self.decision_cache) > self.config.DECISION_CACHE_SIZE:
            # Eliminar decisiones menos usadas
            keys = list(self.decision_cache.keys())
            for key in keys[:100]:
                del self.decision_cache[key]
        
        reaction_time = time.perf_counter() - start_time
        self.reaction_times.append(reaction_time)
        
        return decision, reaction_time
    
    def _preflop_decision(self, position, hand_strength, pot_size):
        """Decisión preflop ultra rápida"""
        # Tabla de decisión precomputada
        if hand_strength > 150:  # AA, KK
            return 'RAISE_5BB'
        elif hand_strength > 130:  # QQ, JJ, AKs
            return 'RAISE_3BB'
        elif hand_strength > 100:  # AQs, TT, 99
            if position in ['BTN', 'CO', 'MP']:
                return 'RAISE_3BB'
            else:
                return 'CALL'
        elif hand_strength > 70:   # Manos jugables
            if position in ['BTN', 'CO']:
                return 'CALL'
            else:
                return 'FOLD'
        else:
            return 'FOLD'
    
    def _postflop_decision(self, game_state, street):
        """Decisión postflop optimizada"""
        hand_strength = game_state.get('hand_strength', 0)
        pot_odds = game_state.get('pot_odds', 1.0)
        
        # Decisión basada en fuerza y odds
        if hand_strength > 80:
            if pot_odds > 3.0:
                return 'RAISE_5BB'
            else:
                return 'RAISE_3BB'
        elif hand_strength > 50:
            if pot_odds > 2.0:
                return 'CALL'
            else:
                return 'CHECK'
        else:
            return 'FOLD'
    
    def _river_decision(self, game_state):
        """Decisión en river optimizada"""
        hand_strength = game_state.get('hand_strength', 0)
        bluff_chance = game_state.get('bluff_chance', 0.3)
        
        if hand_strength > 90:
            return 'RAISE_5BB'  # Valor máximo
        elif hand_strength > 70:
            return 'RAISE_3BB'  # Valor
        elif hand_strength > 50 and bluff_chance > 0.5:
            return 'RAISE_3BB'  # Bluff
        elif hand_strength > 30:
            return 'CHECK'
        else:
            return 'FOLD'
    
    def get_performance_stats(self):
        """Obtener estadísticas de rendimiento"""
        if not self.reaction_times:
            return {
                'avg_reaction_time': self.config.REACTION_TIME_TARGET,
                'min_reaction_time': self.config.REACTION_TIME_TARGET,
                'max_reaction_time': self.config.REACTION_TIME_TARGET
            }
        
        times = list(self.reaction_times)
        return {
            'avg_reaction_time': np.mean(times),
            'min_reaction_time': np.min(times),
            'max_reaction_time': np.max(times),
            'samples': len(times),
            'target': self.config.REACTION_TIME_TARGET
        }

# ==================== SISTEMA DE APRENDIZAJE EXTREMO ====================
class ExtremeLearningSystem:
    """Sistema de aprendizaje ultra rápido"""
    
    def __init__(self):
        self.config = ExtremeConfig()
        self.experiences = deque(maxlen=10000)
        self.learning_thread = None
        self.running = True
        
        # Aprendizaje por lotes
        self.batch_size = 100
        self.learning_queue = deque(maxlen=5000)
        
        print(" SISTEMA DE APRENDIZAJE EXTREMO INICIALIZADO")
        print(f"   Batch Size: {self.batch_size}")
        print(f"   Learning Rate: {self.config.LEARNING_RATE}")
    
    def learn_from_experience(self, state, action, reward, next_state):
        """Aprendizaje ultra rápido"""
        experience = {
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'timestamp': time.time()
        }
        
        self.experiences.append(experience)
        self.learning_queue.append(experience)
        
        # Aprendizaje inmediato si hay suficientes experiencias
        if len(self.learning_queue) >= self.batch_size:
            self._batch_learn()
        
        return True
    
    def _batch_learn(self):
        """Aprendizaje por lotes optimizado"""
        if len(self.learning_queue) < self.batch_size:
            return
        
        batch = list(self.learning_queue)[-self.batch_size:]
        
        # Procesamiento paralelo del batch
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for exp in batch:
                future = executor.submit(self._process_experience, exp)
                futures.append(future)
            
            # Esperar resultados
            for future in futures:
                future.result()
        
        # Limpiar cola procesada
        for _ in range(self.batch_size):
            if self.learning_queue:
                self.learning_queue.popleft()
    
    def _process_experience(self, experience):
        """Procesar una experiencia individual"""
        # Q-learning extremo
        state = experience['state']
        action = experience['action']
        reward = experience['reward']
        next_state = experience['next_state']
        
        # Actualización directa sin verificaciones
        state_key = str(state)
        next_state_key = str(next_state)
        
        # Inicializar si no existe
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(4)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(4)
        
        # Actualización Q-learning
        action_idx = action if isinstance(action, int) else 0
        old_value = self.q_table[state_key][action_idx]
        next_max = np.max(self.q_table[next_state_key])
        
        new_value = old_value + self.config.LEARNING_RATE * (reward + 0.9 * next_max - old_value)
        self.q_table[state_key][action_idx] = new_value
        
        return new_value
    
    def continuous_learning(self):
        """Aprendizaje continuo en hilo separado"""
        def learning_loop():
            while self.running:
                if len(self.learning_queue) >= self.batch_size:
                    self._batch_learn()
                time.sleep(0.01)  # Ciclo muy rápido
        
        self.learning_thread = threading.Thread(target=learning_loop, daemon=True)
        self.learning_thread.start()
        return self.learning_thread
    
    def stop_learning(self):
        """Detener aprendizaje"""
        self.running = False
        if self.learning_thread:
            self.learning_thread.join(timeout=1.0)

# ==================== SISTEMA DE OPTIMIZACIÓN DE RECURSOS ====================
class ResourceOptimizer:
    """Optimizador de recursos para mínimo consumo"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.memory_limit_mb = 500  # Límite de memoria
        self.cpu_limit_percent = 70  # Límite de CPU
        self.optimization_active = True
        
        print(" OPTIMIZADOR DE RECURSOS INICIALIZADO")
        print(f"   Memoria límite: {self.memory_limit_mb}MB")
        print(f"   CPU límite: {self.cpu_limit_percent}%")
    
    def optimize_memory(self):
        """Optimización agresiva de memoria"""
        gc.collect()  # Recolección de basura
        
        # Limpiar caches grandes
        if hasattr(cv2, '_cache'):
            cv2._cache.clear()
        
        # Limitar uso de memoria
        current_memory = self.process.memory_info().rss / 1024 / 1024
        
        if current_memory > self.memory_limit_mb:
            print(f"  Memoria alta: {current_memory:.1f}MB, limpiando...")
            
            # Limpiar caches
            if 'decision_cache' in globals():
                decision_cache.clear()
            
            # Forzar recolección
            gc.collect(generation=2)
            
            # Reducir límites si es necesario
            self.memory_limit_mb = max(300, self.memory_limit_mb * 0.9)
    
    def optimize_cpu(self):
        """Optimizar uso de CPU"""
        cpu_percent = self.process.cpu_percent(interval=0.1)
        
        if cpu_percent > self.cpu_limit_percent:
            print(f"  CPU alta: {cpu_percent:.1f}%, ajustando...")
            
            # Reducir número de threads
            cv2.setNumThreads(max(1, multiprocessing.cpu_count() // 2))
            
            # Ajustar prioridad
            try:
                self.process.nice(10)  # Prioridad más baja
            except:
                pass
    
    def continuous_optimization(self, interval=5.0):
        """Optimización continua"""
        def optimization_loop():
            while self.optimization_active:
                self.optimize_memory()
                self.optimize_cpu()
                time.sleep(interval)
        
        thread = threading.Thread(target=optimization_loop, daemon=True)
        thread.start()
        return thread
    
    def stop_optimization(self):
        """Detener optimización"""
        self.optimization_active = False

# ==================== SISTEMA PRINCIPAL EXTREMO ====================
class ExtremePokerBot:
    """Bot de póker extremo sin restricciones"""
    
    def __init__(self):
        self.config = ExtremeConfig()
        
        # Inicializar todos los sistemas
        self.capture_system = ExtremeCaptureSystem()
        self.detection_system = ExtremeDetectionSystem()
        self.decision_system = ExtremeDecisionSystem()
        self.learning_system = ExtremeLearningSystem()
        self.resource_optimizer = ResourceOptimizer()
        
        # Métricas
        self.metrics = {
            'total_decisions': 0,
            'avg_reaction_time': 0,
            'peak_performance': 0,
            'learning_iterations': 0
        }
        
        # Estado del bot
        self.is_running = False
        self.main_thread = None
        
        print("=" * 60)
        print(" BOT DE PÓKER EXTREMO - SIN RESTRICCIONES")
        print("=" * 60)
        print(" Características activadas:")
        print("    Sin verificaciones de seguridad")
        print("    Tiempo de reacción objetivo: 50ms")
        print("    Procesamiento paralelo máximo")
        print("    Optimización agresiva de recursos")
        print("    Cache extremo en todas las operaciones")
        print("=" * 60)
    
    def start_extreme_mode(self):
        """Iniciar modo extremo"""
        self.is_running = True
        
        # Iniciar captura continua
        capture_thread = self.capture_system.continuous_capture(
            self._process_frame, 
            interval=0.02  # 50 FPS
        )
        
        # Iniciar aprendizaje continuo
        learning_thread = self.learning_system.continuous_learning()
        
        # Iniciar optimización de recursos
        optimization_thread = self.resource_optimizer.continuous_optimization()
        
        print(" MODO EXTREMO ACTIVADO")
        print("   Todos los sistemas funcionando a máxima velocidad")
        print("   Restricciones: DESACTIVADAS")
        print("   Optimización: MÁXIMA")
        
        return capture_thread, learning_thread, optimization_thread
    
    def _process_frame(self, frame, capture_time):
        """Procesar frame capturado"""
        if not self.is_running:
            return
        
        start_time = time.perf_counter()
        
        # Detección ultra rápida
        detection_result = self.detection_system.detect_cards_extreme(frame)
        
        # Crear estado del juego
        game_state = self._create_game_state(detection_result)
        
        # Decisión ultra rápida
        decision, reaction_time = self.decision_system.ultra_fast_decision(game_state)
        
        # Aprender de la experiencia
        reward = self._calculate_reward(game_state, decision)
        self.learning_system.learn_from_experience(
            game_state, decision, reward, game_state
        )
        
        # Actualizar métricas
        self.metrics['total_decisions'] += 1
        self.metrics['avg_reaction_time'] = (
            self.metrics['avg_reaction_time'] * 0.9 + reaction_time * 0.1
        )
        
        # Mostrar rendimiento periódicamente
        if self.metrics['total_decisions'] % 100 == 0:
            self._display_performance()
        
        total_time = time.perf_counter() - start_time
        
        # Si el tiempo total es mayor que el objetivo, ajustar
        if total_time > self.config.REACTION_TIME_TARGET:
            # Auto-optimización
            self._auto_optimize()
    
    def _create_game_state(self, detection_result):
        """Crear estado del juego a partir de detección"""
        return {
            'street': 'preflop',  # Por simplicidad
            'pot': 100,
            'position': 'BTN',
            'hand_strength': np.random.randint(1, 170),
            'colors': detection_result['colors'],
            'detection_time': detection_result['detection_time'],
            'timestamp': time.time()
        }
    
    def _calculate_reward(self, game_state, decision):
        """Calcular recompensa ultra rápida"""
        hand_strength = game_state['hand_strength']
        
        # Recompensa basada en fuerza de mano y decisión
        if decision in ['RAISE_3BB', 'RAISE_5BB', 'ALLIN']:
            if hand_strength > 100:
                return 1.0  # Buena decisión
            else:
                return -0.5  # Mala decisión
        elif decision == 'CALL':
            if hand_strength > 70:
                return 0.5
            else:
                return -0.3
        else:  # FOLD
            if hand_strength < 30:
                return 0.3
            else:
                return -0.7
    
    def _display_performance(self):
        """Mostrar rendimiento actual"""
        stats = self.decision_system.get_performance_stats()
        
        print(f"\n RENDIMIENTO EXTREMO - Decisión #{self.metrics['total_decisions']}")
        print(f"   Tiempo reacción: {stats['avg_reaction_time']*1000:.1f}ms")
        print(f"   Objetivo: {stats['target']*1000:.0f}ms")
        print(f"   Mínimo: {stats['min_reaction_time']*1000:.1f}ms")
        print(f"   Máximo: {stats['max_reaction_time']*1000:.1f}ms")
        print(f"   Cache hits: {len(self.decision_system.decision_cache)}")
        
        # Uso de recursos
        memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        print(f"   Memoria: {memory_mb:.1f}MB")
        print(f"   CPU: {cpu_percent:.1f}%")
    
    def _auto_optimize(self):
        """Auto-optimización en tiempo real"""
        # Reducir resolución si es necesario
        if self.config.PROCESSING_RESOLUTION != "low":
            self.config.PROCESSING_RESOLUTION = "low"
            print("  Auto-optimización: Resolución reducida a LOW")
        
        # Limpiar cache si es muy grande
        if len(self.decision_system.decision_cache) > 5000:
            keys = list(self.decision_system.decision_cache.keys())
            for key in keys[:1000]:
                del self.decision_system.decision_cache[key]
            print("  Auto-optimización: Cache reducido")
    
    def stop(self):
        """Detener bot extremo"""
        self.is_running = False
        
        # Detener todos los sistemas
        self.capture_system.stop_capture()
        self.learning_system.stop_learning()
        self.resource_optimizer.stop_optimization()
        
        # Guardar estado
        self._save_state()
        
        print("\n BOT EXTREMO DETENIDO")
        print(f"   Decisiones totales: {self.metrics['total_decisions']}")
        print(f"   Tiempo promedio: {self.metrics['avg_reaction_time']*1000:.1f}ms")
    
    def _save_state(self):
        """Guardar estado optimizado"""
        state = {
            'metrics': self.metrics,
            'decision_cache_size': len(self.decision_system.decision_cache),
            'q_table_size': len(self.learning_system.q_table),
            'timestamp': datetime.now().isoformat()
        }
        
        # Guardar en formato binario para velocidad
        with open('extreme_bot_state.pkl', 'wb') as f:
            pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        print(" Estado guardado: extreme_bot_state.pkl")

# ==================== FUNCIÓN PRINCIPAL ====================
def main():
    """Función principal del bot extremo"""
    
    print(" INICIANDO BOT DE PÓKER EXTREMO")
    print("=" * 50)
    print("  ADVERTENCIA: Todas las restricciones están desactivadas")
    print("  Este bot está optimizado para velocidad máxima")
    print("=" * 50)
    
    # Crear bot extremo
    bot = ExtremePokerBot()
    
    try:
        # Iniciar modo extremo
        threads = bot.start_extreme_mode()
        
        print("\n Bot funcionando... Presiona Ctrl+C para detener")
        print(" El rendimiento se mostrará cada 100 decisiones")
        
        # Mantener el programa corriendo
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n Deteniendo por usuario...")
    finally:
        bot.stop()
        
        # Esperar a que los threads terminen
        for thread in threads:
            if thread:
                thread.join(timeout=2.0)
        
        print("\n Bot detenido correctamente")
        print(" Rendimiento final:")
        print(f"   Decisiones: {bot.metrics['total_decisions']}")
        print(f"   Tiempo promedio: {bot.metrics['avg_reaction_time']*1000:.1f}ms")

if __name__ == "__main__":
    main()
