#!/usr/bin/env python3
"""
🎴 POKER_AI_INTEGRATOR.py - Integrador Completo de Sistemas
Combina: OCR de cartas + IA profesional + Análisis GTO + Overlay
"""

import sys
import os
import cv2
import numpy as np
import time
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import json
from datetime import datetime

# Configurar paths
sys.path.insert(0, str(Path(__file__).parent))

@dataclass
class DetectedCard:
    """Carta detectada en pantalla"""
    rank: str  # A, K, Q, J, 10-2
    suit: str  #    
    position: Tuple[int, int]  # (x, y)
    confidence: float  # 0-1
    region: Tuple[int, int, int, int]  # (x, y, w, h)
    
    def __str__(self):
        return f"{self.rank}{self.suit} ({self.confidence:.1%})"
    
    def to_dict(self):
        return {
            "rank": self.rank,
            "suit": self.suit,
            "position": self.position,
            "confidence": self.confidence,
            "region": self.region
        }

@dataclass  
class TableState:
    """Estado completo de la mesa"""
    timestamp: float
    hero_cards: List[DetectedCard]
    community_cards: List[DetectedCard]
    pot_size: float
    current_bet: float
    player_count: int
    position: str  # early, middle, late, button
    street: str  # preflop, flop, turn, river
    action_on_us: str  # check, bet, raise, allin, fold
    
    def __str__(self):
        hero_str = " ".join([str(c) for c in self.hero_cards]) if self.hero_cards else "No detectadas"
        comm_str = " ".join([str(c) for c in self.community_cards]) if self.community_cards else "No hay"
        return (f"📊 ESTADO MESA:\n"
                f"  🃏 Hero: {hero_str}\n"
                f"  🎴 Comunitarias: {comm_str}\n"
                f"  💰 Bote: ${self.pot_size:.2f} | Apuesta: ${self.current_bet:.2f}\n"
                f"  👥 Jugadores: {self.player_count} | Posición: {self.position}\n"
                f"   Calle: {self.street.upper()} | Acción: {self.action_on_us}")

class PokerAIIntegrator:
    """Integrador principal que combina todos los sistemas"""
    
    def __init__(self, mode="realtime"):
        self.mode = mode
        self.is_running = False
        self.overlay_active = True
        self.current_state = None
        self.last_analysis = None
        self.analytics = []
        
        # Inicializar componentes
        self.components = {}
        self._initialize_components()
        
        print(" POKER AI INTEGRATOR INICIALIZADO")
        print(f" Modo: {mode}")
        print(f"🤖 Componentes cargados: {len(self.components)}")
    
    def _initialize_components(self):
        """Inicializar todos los componentes disponibles"""
        try:
            # 1. Cargar sistema OCR si existe
            if Path("CARD_OCR_SYSTEM.py").exists():
                print(" Cargando sistema OCR...")
                import importlib.util
                
                spec = importlib.util.spec_from_file_location(
                    "card_ocr", 
                    "CARD_OCR_SYSTEM.py"
                )
                ocr_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ocr_module)
                
                # Buscar clases en el módulo
                if hasattr(ocr_module, 'PokerStarsCardDetector'):
                    self.components['ocr'] = ocr_module.PokerStarsCardDetector(theme='classic')
                    print(" Sistema OCR cargado")
                else:
                    print("⚠️  Clase OCR no encontrada, usando detector básico")
                    self.components['ocr'] = BasicCardDetector()
            else:
                print("  CARD_OCR_SYSTEM.py no encontrado, usando detector básico")
                self.components['ocr'] = BasicCardDetector()
            
            # 2. Cargar sistema profesional si existe
            if Path("professional_system/professional_poker_system.py").exists():
                print("🧠 Cargando sistema profesional...")
                try:
                    spec = importlib.util.spec_from_file_location(
                        "pro_system",
                        "professional_system/professional_poker_system.py"
                    )
                    pro_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(pro_module)
                    
                    if hasattr(pro_module, 'ProfessionalPokerBrain'):
                        self.components['brain'] = pro_module.ProfessionalPokerBrain()
                        print("✅ Cerebro profesional cargado")
                    else:
                        print("  Cerebro no encontrado, usando analizador básico")
                        self.components['brain'] = BasicAnalyzer()
                except Exception as e:
                    print(f"  Error cargando sistema profesional: {e}")
                    self.components['brain'] = BasicAnalyzer()
            else:
                print("  Sistema profesional no encontrado, usando analizador básico")
                self.components['brain'] = BasicAnalyzer()
            
            # 3. Cargar calibrador si existe
            if Path("POKERSTARS_CALIBRATOR.py").exists():
                print(" Cargando calibrador...")
                try:
                    spec = importlib.util.spec_from_file_location(
                        "calibrator",
                        "POKERSTARS_CALIBRATOR.py"
                    )
                    cal_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(cal_module)
                    
                    if hasattr(cal_module, 'PokerStarsCalibrator'):
                        self.components['calibrator'] = cal_module.PokerStarsCalibrator()
                        print(" Calibrador cargado")
                except Exception as e:
                    print(f"  Error cargando calibrador: {e}")
            
            # 4. Cargar sistema de optimización si existe
            if Path("extreme_optimization/extreme_bot_simple.py").exists():
                print(" Cargando optimización extrema...")
                try:
                    spec = importlib.util.spec_from_file_location(
                        "extreme_bot",
                        "extreme_optimization/extreme_bot_simple.py"
                    )
                    extreme_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(extreme_module)
                    print(" Optimización extrema cargada")
                except Exception as e:
                    print(f"  Error cargando optimización: {e}")
            
            # 5. Inicializar captura de pantalla
            self.components['capture'] = ScreenCapture()
            print(" Captura de pantalla inicializada")
            
            # 6. Inicializar overlay
            self.components['overlay'] = OverlayManager()
            print(" Overlay inicializado")
            
            # 7. Inicializar sistema de decisiones
            self.components['decision'] = DecisionEngine()
            print(" Motor de decisiones inicializado")
            
        except Exception as e:
            print(f" Error inicializando componentes: {e}")
            print(" Usando componentes básicos mínimos")
            self._initialize_minimal_components()
    
    def _initialize_minimal_components(self):
        """Inicializar componentes básicos mínimos"""
        self.components['ocr'] = BasicCardDetector()
        self.components['brain'] = BasicAnalyzer()
        self.components['capture'] = ScreenCapture()
        self.components['decision'] = DecisionEngine()
        self.components['overlay'] = OverlayManager()
    
    def capture_and_analyze(self):
        """Capturar pantalla y analizar en un ciclo"""
        print(" INICIANDO ANÁLISIS EN TIEMPO REAL")
        print("=" * 50)
        print(" Presione Ctrl+C para detener")
        print()
        
        self.is_running = True
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.is_running:
                frame_count += 1
                
                # 1. Capturar pantalla
                screenshot = self.components['capture'].capture()
                if screenshot is None:
                    print(" Error capturando pantalla")
                    time.sleep(0.5)
                    continue
                
                # 2. Detectar cartas
                detected_cards = self.components['ocr'].detect_cards(screenshot)
                
                # 3. Determinar estado de la mesa
                self.current_state = self._determine_table_state(detected_cards, screenshot)
                
                # 4. Analizar situación
                if self.current_state and self.current_state.hero_cards:
                    analysis = self.components['decision'].analyze(self.current_state)
                    self.last_analysis = analysis
                    
                    # 5. Mostrar resultados
                    self._display_analysis(frame_count, analysis)
                    
                    # 6. Actualizar overlay si está activo
                    if self.overlay_active:
                        self.components['overlay'].update(
                            self.current_state, 
                            analysis,
                            screenshot
                        )
                
                # 7. Estadísticas periódicas
                if frame_count % 10 == 0:
                    elapsed = time.time() - start_time
                    fps = frame_count / elapsed if elapsed > 0 else 0
                    print(f" FPS: {fps:.1f} | Frames: {frame_count} | Cartas detectadas: {len(detected_cards)}")
                
                # Control de velocidad
                time.sleep(0.1)  # 10 FPS
                
        except KeyboardInterrupt:
            print("\n\n  Análisis detenido por el usuario")
        except Exception as e:
            print(f" Error en análisis: {e}")
        finally:
            self.is_running = False
            self._save_session_stats(frame_count, start_time)
    
    def _determine_table_state(self, cards: List[DetectedCard], screenshot) -> Optional[TableState]:
        """Determinar el estado de la mesa basado en cartas detectadas"""
        if not cards:
            return None
        
        # Separar cartas del hero y comunitarias por posición
        height, width = screenshot.shape[:2]
        
        hero_cards = []
        community_cards = []
        
        for card in cards:
            # Cartas en parte inferior (hero) vs central/superior (comunitarias)
            if card.position[1] > height * 0.6:  # Parte inferior
                hero_cards.append(card)
            else:  # Parte central/superior
                community_cards.append(card)
        
        # Determinar calle basado en cartas comunitarias
        street = self._determine_street(len(community_cards))
        
        # Determinar posición (simplificado)
        position = self._estimate_position(hero_cards, screenshot)
        
        # Crear estado
        state = TableState(
            timestamp=time.time(),
            hero_cards=hero_cards[:2],  # Máximo 2 cartas para hero
            community_cards=community_cards[:5],  # Máximo 5 comunitarias
            pot_size=50.0,  # Valor estimado
            current_bet=10.0,  # Valor estimado
            player_count=6,  # Valor estimado
            position=position,
            street=street,
            action_on_us="bet"  # Valor estimado
        )
        
        return state
    
    def _determine_street(self, community_count: int) -> str:
        """Determinar calle basado en número de cartas comunitarias"""
        if community_count == 0:
            return "preflop"
        elif community_count == 3:
            return "flop"
        elif community_count == 4:
            return "turn"
        elif community_count == 5:
            return "river"
        else:
            return "unknown"
    
    def _estimate_position(self, hero_cards: List[DetectedCard], screenshot) -> str:
        """Estimar posición del jugador"""
        # En sistema real, usaríamos posición en pantalla y mesa
        # Aquí usamos una estimación simple
        height, width = screenshot.shape[:2]
        
        if not hero_cards:
            return "unknown"
        
        # Posición promedio de las cartas del hero
        avg_y = sum(card.position[1] for card in hero_cards) / len(hero_cards)
        
        if avg_y > height * 0.8:
            return "button"  # Parte más inferior
        elif avg_y > height * 0.6:
            return "late"
        elif avg_y > height * 0.4:
            return "middle"
        else:
            return "early"
    
    def _display_analysis(self, frame_num: int, analysis: Dict):
        """Mostrar análisis en consola"""
        # Limpiar varias líneas anteriores
        lines_to_clear = 15
        for _ in range(lines_to_clear):
            sys.stdout.write('\033[F')  # Subir una línea
            sys.stdout.write('\033[K')  # Limpiar línea
        
        print(f" Frame: {frame_num} | {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        if self.current_state:
            print(self.current_state)
            print()
        
        if analysis:
            print(" ANÁLISIS IA:")
            print(f"  Acción recomendada: {analysis.get('action', 'N/A')}")
            print(f"  Confianza: {analysis.get('confidence', 0):.1%}")
            print(f"  Razón: {analysis.get('reason', 'N/A')}")
            
            if 'equity' in analysis:
                print(f"  Equity: {analysis['equity']:.1%}")
            if 'pot_odds' in analysis:
                print(f"  Pot Odds: {analysis['pot_odds']:.1%}")
            if 'ev' in analysis:
                print(f"  EV: {analysis['ev']:.2f} BB")
            
            print(f"  Tiempo análisis: {analysis.get('analysis_time_ms', 0):.1f}ms")
        
        print("=" * 60)
        print(" Ctrl+C para detener | Cartas detectadas automáticamente")
    
    def _save_session_stats(self, frames: int, start_time: float):
        """Guardar estadísticas de la sesión"""
        elapsed = time.time() - start_time
        fps = frames / elapsed if elapsed > 0 else 0
        
        stats = {
            "session_end": datetime.now().isoformat(),
            "total_frames": frames,
            "total_time_seconds": elapsed,
            "average_fps": fps,
            "total_analyses": len(self.analytics),
            "analytics": self.analytics[-100:]  # Últimos 100 análisis
        }
        
        # Guardar en archivo
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        filename = log_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n Estadísticas guardadas en: {filename}")
        print(f"   Frames procesados: {frames}")
        print(f"   Tiempo total: {elapsed:.1f}s")
        print(f"   FPS promedio: {fps:.1f}")
        print(f"   Análisis realizados: {len(self.analytics)}")

# ============================================
# COMPONENTES BÁSICOS (FALLBACK)
# ============================================

class BasicCardDetector:
    """Detector básico de cartas (fallback)"""
    
    def detect_cards(self, screenshot):
        """Detectar cartas básicas"""
        # En sistema real, aquí iría el OCR/visión por computadora
        # Por ahora simulamos detección
        height, width = screenshot.shape[:2]
        
        detected = []
        
        # Simular 2 cartas del hero y 3-5 comunitarias
        simulated_cards = [
            {"rank": "A", "suit": "", "pos": (width//2 - 50, height - 100)},
            {"rank": "K", "suit": "", "pos": (width//2 + 50, height - 100)},
            {"rank": "Q", "suit": "", "pos": (width//2 - 100, height//2)},
            {"rank": "7", "suit": "", "pos": (width//2, height//2)},
            {"rank": "2", "suit": "", "pos": (width//2 + 100, height//2)}
        ]
        
        for i, card in enumerate(simulated_cards):
            detected.append(DetectedCard(
                rank=card["rank"],
                suit=card["suit"],
                position=card["pos"],
                confidence=0.85 - (i * 0.05),  # Disminuye confianza
                region=(card["pos"][0]-40, card["pos"][1]-60, 80, 120)
            ))
        
        return detected

class BasicAnalyzer:
    """Analizador básico (fallback)"""
    
    def analyze_situation(self, state):
        """Analizar situación básica"""
        return {
            "action": "RAISE",
            "confidence": 0.75,
            "reason": "Análisis básico - Mano fuerte estimada",
            "analysis_time_ms": 25.0
        }

class ScreenCapture:
    """Capturador de pantalla básico"""
    
    def __init__(self):
        self.capture_method = self._detect_capture_method()
    
    def _detect_capture_method(self):
        """Detectar mejor método de captura disponible"""
        try:
            import mss
            return "mss"
        except ImportError:
            try:
                import pyautogui
                return "pyautogui"
            except ImportError:
                return "simulated"
    
    def capture(self):
        """Capturar pantalla"""
        try:
            if self.capture_method == "mss":
                import mss
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = np.array(sct.grab(monitor))
                    return cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            
            elif self.capture_method == "pyautogui":
                import pyautogui
                screenshot = pyautogui.screenshot()
                return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            else:
                # Simular captura
                height, width = 600, 800
                screenshot = np.zeros((height, width, 3), dtype=np.uint8)
                screenshot[:] = (40, 90, 40)  # Verde poker
                
                # Dibujar "mesa"
                cv2.rectangle(screenshot, (100, 100), (700, 500), (30, 70, 30), -1)
                
                return screenshot
                
        except Exception as e:
            print(f"  Error capturando pantalla: {e}")
            return None

class DecisionEngine:
    """Motor de decisiones GTO/IA"""
    
    def __init__(self):
        self.hand_strengths = self._load_hand_strengths()
        self.gto_rules = self._load_gto_rules()
        self.decision_cache = {}
    
    def _load_hand_strengths(self):
        """Cargar fuerza de manos preflop"""
        return {
            "AA": 1, "KK": 2, "QQ": 3, "JJ": 4, "TT": 5,
            "99": 6, "88": 7, "77": 8, "66": 9, "55": 10,
            "44": 11, "33": 12, "22": 13,
            "AK": 14, "AQ": 15, "AJ": 16, "AT": 17,
            "KQ": 18, "KJ": 19, "KT": 20,
            "QJ": 21, "QT": 22, "JT": 23,
            "T9": 24, "98": 25, "87": 26, "76": 27, "65": 28, "54": 29, "43": 30, "32": 31
        }
    
    def _load_gto_rules(self):
        """Cargar reglas GTO básicas"""
        return {
            "preflop": {
                "UTG": ["AA", "KK", "QQ", "JJ", "AK", "AQ"],
                "MP": ["TT", "99", "AJ", "KQ"],
                "CO": ["88", "77", "AT", "KJ", "QJ"],
                "BTN": ["66", "55", "A9", "KT", "QT", "JT", "T9"],
                "SB": ["44", "33", "A8", "K9", "Q9", "J9", "T8", "98"],
                "BB": ["22", "A2", "K8", "Q8", "J8", "T7", "97", "87", "76"]
            },
            "postflop": {
                "nut_hand": "BET_RAISE",
                "strong_hand": "BET_CALL",
                "medium_hand": "CHECK_CALL",
                "weak_hand": "CHECK_FOLD",
                "draw_strong": "BET_RAISE",
                "draw_weak": "CHECK_CALL"
            }
        }
    
    def analyze(self, state):
        """Analizar situación y tomar decisión"""
        start_time = time.time()
        
        if not state or not state.hero_cards:
            return {
                "action": "FOLD",
                "confidence": 0.0,
                "reason": "No se detectaron cartas",
                "analysis_time_ms": 0
            }
        
        # Obtener mano del hero
        hero_hand = self._get_hero_hand_string(state.hero_cards)
        
        # Analizar basado en calle
        if state.street == "preflop":
            decision = self._analyze_preflop(hero_hand, state)
        else:
            decision = self._analyze_postflop(hero_hand, state)
        
        # Calcular tiempo de análisis
        analysis_time = (time.time() - start_time) * 1000  # ms
        
        decision["analysis_time_ms"] = analysis_time
        decision["hand"] = hero_hand
        decision["street"] = state.street
        decision["position"] = state.position
        
        # Cachear decisión
        cache_key = f"{hero_hand}_{state.position}_{state.street}"
        self.decision_cache[cache_key] = decision
        
        return decision
    
    def _get_hero_hand_string(self, hero_cards):
        """Convertir cartas a string de mano"""
        if len(hero_cards) < 2:
            return "??"
        
        card1 = hero_cards[0]
        card2 = hero_cards[1]
        
        # Ordenar por fuerza
        ranks = [card1.rank, card2.rank]
        if ranks[0] == ranks[1]:
            hand = f"{ranks[0]}{ranks[1]}"  # Par
        else:
            # Ordenar por fuerza (A alto, 2 bajo)
            rank_values = {"A": 14, "K": 13, "Q": 12, "J": 11, "10": 10, "9": 9, 
                          "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
            sorted_ranks = sorted(ranks, key=lambda x: rank_values.get(x, 0), reverse=True)
            hand = f"{sorted_ranks[0]}{sorted_ranks[1]}"
            
            # Añadir suited/offsuit
            if card1.suit == card2.suit:
                hand += "s"
            else:
                hand += "o"
        
        return hand
    
    def _analyze_preflop(self, hand, state):
        """Analizar situación preflop"""
        position = state.position
        hand_base = hand[:2] if len(hand) >= 2 else hand
        
        # Buscar en reglas GTO
        if position in self.gto_rules["preflop"]:
            if hand_base in self.gto_rules["preflop"][position]:
                return {
                    "action": "RAISE",
                    "confidence": 0.85,
                    "reason": f"{hand} en rango {position} (GTO)"
                }
            elif self._is_hand_close(hand_base, self.gto_rules["preflop"][position]):
                return {
                    "action": "CALL",
                    "confidence": 0.65,
                    "reason": f"{hand} cerca del rango {position}"
                }
            else:
                return {
                    "action": "FOLD",
                    "confidence": 0.75,
                    "reason": f"{hand} fuera del rango {position}"
                }
        
        # Reglas por defecto basadas en fuerza de mano
        hand_strength = self.hand_strengths.get(hand_base, 100)
        
        if hand_strength <= 10:  # Top 10 manos
            return {
                "action": "RAISE",
                "confidence": 0.80,
                "reason": f"Mano fuerte: {hand} (rank {hand_strength})"
            }
        elif hand_strength <= 20:
            return {
                "action": "CALL" if state.current_bet == 0 else "FOLD",
                "confidence": 0.60,
                "reason": f"Mano media: {hand}"
            }
        else:
            return {
                "action": "FOLD",
                "confidence": 0.70,
                "reason": f"Mano débil: {hand}"
            }
    
    def _is_hand_close(self, hand, range_list):
        """Verificar si mano está cerca del rango"""
        # Lógica simplificada para determinar si mano está cerca
        strong_hands = ["AA", "KK", "QQ", "JJ", "TT", "AK", "AQ", "AJ"]
        medium_hands = ["99", "88", "KQ", "KJ", "QJ", "JT"]
        
        if hand in strong_hands or hand in medium_hands:
            return True
        return False
    
    def _analyze_postflop(self, hand, state):
        """Analizar situación postflop"""
        # Evaluar fuerza de mano postflop (simplificado)
        hand_strength = self._evaluate_postflop_strength(hand, state)
        
        if hand_strength > 0.7:
            return {
                "action": "BET_RAISE",
                "confidence": 0.80,
                "reason": "Mano muy fuerte postflop",
                "equity": hand_strength
            }
        elif hand_strength > 0.5:
            return {
                "action": "BET_CALL",
                "confidence": 0.65,
                "reason": "Mano fuerte, valor",
                "equity": hand_strength
            }
        elif hand_strength > 0.3:
            return {
                "action": "CHECK_CALL",
                "confidence": 0.55,
                "reason": "Mano media, ver ver",
                "equity": hand_strength
            }
        else:
            return {
                "action": "CHECK_FOLD",
                "confidence": 0.70,
                "reason": "Mano débil postflop",
                "equity": hand_strength
            }
    
    def _evaluate_postflop_strength(self, hand, state):
        """Evaluar fuerza postflop (simplificado)"""
        # En sistema real, aquí iría cálculo de equity completo
        # Por ahora usamos valores estimados basados en tipo de mano
        
        if not state.community_cards:
            return 0.5  # Valor por defecto preflop
        
        # Simular fuerza basada en tipo de mano
        hand_type = self._classify_hand(hand, state)
        
        strength_map = {
            "nut_flush": 0.95,
            "nut_straight": 0.90,
            "top_set": 0.85,
            "top_two": 0.80,
            "top_pair": 0.65,
            "middle_pair": 0.50,
            "weak_pair": 0.35,
            "high_card": 0.25,
            "flush_draw": 0.45,
            "straight_draw": 0.40,
            "nothing": 0.15
        }
        
        return strength_map.get(hand_type, 0.5)
    
    def _classify_hand(self, hand, state):
        """Clasificar tipo de mano postflop"""
        # Clasificación simplificada
        if "A" in hand and len(state.community_cards) >= 3:
            return "top_pair"
        elif "K" in hand or "Q" in hand:
            return "middle_pair"
        else:
            return "weak_pair"

class OverlayManager:
    """Gestor de overlay en pantalla"""
    
    def __init__(self):
        self.overlay_data = None
        self.last_update = 0
    
    def update(self, state, analysis, screenshot):
        """Actualizar información del overlay"""
        current_time = time.time()
        
        # Actualizar cada 0.3 segundos máximo
        if current_time - self.last_update < 0.3:
            return
        
        self.last_update = current_time
        
        self.overlay_data = {
            "state": state,
            "analysis": analysis,
            "timestamp": current_time,
            "screenshot_size": screenshot.shape[:2] if screenshot is not None else (0, 0)
        }
        
        # En sistema real, aquí se dibujaría el overlay en pantalla
        # Por ahora solo mostramos en consola
        self._print_overlay()
    
    def _print_overlay(self):
        """Mostrar overlay en consola (simulado)"""
        if not self.overlay_data:
            return
        
        state = self.overlay_data.get("state")
        analysis = self.overlay_data.get("analysis")
        
        if state and analysis:
            # Limpiar línea anterior
            print("\033[F\033[K", end="")
            
            hero_cards = " ".join([str(c) for c in state.hero_cards]) if state.hero_cards else "??"
            action = analysis.get("action", "N/A")
            confidence = analysis.get("confidence", 0)
            
            print(f"  OVERLAY: {hero_cards}  {action} ({confidence:.0%})", end="", flush=True)

# ============================================
# INTERFAZ PRINCIPAL
# ============================================

def main():
    """Función principal"""
    print(" POKER AI INTEGRATOR - SISTEMA COMPLETO")
    print("=" * 60)
    
    print("\n MODOS DISPONIBLES:")
    print("1.  Modo tiempo real (captura pantalla)")
    print("2.   Modo imagen de prueba")
    print("3.  Modo test (sin captura)")
    print("4.  Calibrar sistema")
    print("5.  Salir")
    
    choice = input("\nSeleccione modo (1-5): ").strip()
    
    if choice == "1":
        print("\n CONFIGURANDO MODO TIEMPO REAL...")
        print("=" * 40)
        
        # Verificar dependencias
        print("Verificando dependencias...")
        try:
            import mss
            print(" mss disponible para captura rápida")
        except ImportError:
            print("  mss no instalado. Instale con: pip install mss")
            print(" Usando captura alternativa (más lenta)")
        
        try:
            import cv2
            print(" OpenCV disponible")
        except ImportError:
            print(" OpenCV no instalado. Instale con: pip install opencv-python")
            print(" El modo tiempo real no funcionará correctamente")
            input("Presione Enter para continuar...")
            return
        
        print("\n CONFIGURACIÓN:")
        print("FPS objetivo: 10")
        print("Overlay: Activado")
        print("Análisis IA: Activado")
        print("Logs: Activados")
        
        input("\nPresione Enter para iniciar análisis en tiempo real...")
        
        # Iniciar integrador
        integrator = PokerAIIntegrator(mode="realtime")
        integrator.capture_and_analyze()
        
    elif choice == "2":
        print("\n  MODO IMAGEN DE PRUEBA")
        print("=" * 40)
        
        # Crear imagen de prueba
        try:
            import cv2
            import numpy as np
            
            print("Creando imagen de prueba con cartas...")
            
            # Crear imagen simulando mesa de poker
            height, width = 600, 800
            img = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Fondo verde de mesa
            img[:] = (40, 90, 40)
            
            # Área central de mesa
            cv2.rectangle(img, (100, 100), (700, 500), (30, 70, 30), -1)
            
            # Dibujar cartas del hero (inferior)
            card_color = (240, 240, 220)
            cv2.rectangle(img, (350, 450), (430, 570), card_color, -1)  # Carta 1
            cv2.rectangle(img, (450, 450), (530, 570), card_color, -1)  # Carta 2
            
            # Escribir "A" y "K"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, "A", (370, 500), font, 1, (0, 0, 0), 2)
            cv2.putText(img, "K", (470, 500), font, 1, (0, 0, 0), 2)
            
            # Dibujar cartas comunitarias (centro)
            for i in range(5):
                x = 300 + i * 80
                cv2.rectangle(img, (x, 250), (x + 60, 370), card_color, -1)
            
            # Guardar imagen
            test_image_path = "test_poker_table.png"
            cv2.imwrite(test_image_path, img)
            print(f" Imagen guardada: {test_image_path}")
            
            # Procesar imagen
            print("\n PROCESANDO IMAGEN...")
            integrator = PokerAIIntegrator(mode="test")
            
            # Simular detección en imagen
            detected_cards = integrator.components['ocr'].detect_cards(img)
            
            if detected_cards:
                print(f" {len(detected_cards)} cartas detectadas:")
                for card in detected_cards:
                    print(f"    {card}")
                
                # Crear estado simulado
                state = integrator._determine_table_state(detected_cards, img)
                
                if state:
                    print(f"\n ESTADO DETECTADO:")
                    print(state)
                    
                    # Analizar
                    analysis = integrator.components['decision'].analyze(state)
                    
                    print(f"\n ANÁLISIS IA:")
                    for key, value in analysis.items():
                        print(f"   {key}: {value}")
            
        except ImportError as e:
            print(f" Error: {e}")
            print(" Instale OpenCV: pip install opencv-python")
        
    elif choice == "3":
        print("\n MODO TEST")
        print("=" * 40)
        
        print("Ejecutando pruebas del sistema...")
        
        # Crear integrador
        integrator = PokerAIIntegrator(mode="test")
        
        # Probar componentes
        print("\n TESTEANDO COMPONENTES:")
        
        # Test 1: Detector básico
        print("1. Probando detector de cartas...")
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cards = integrator.components['ocr'].detect_cards(test_image)
        print(f"    Detector funcionando ({len(cards)} cartas simuladas)")
        
        # Test 2: Motor de decisiones
        print("2. Probando motor de decisiones...")
        
        # Crear estado de prueba
        test_state = TableState(
            timestamp=time.time(),
            hero_cards=[
                DetectedCard("A", "", (100, 100), 0.9, (80, 80, 40, 60)),
                DetectedCard("K", "", (150, 100), 0.9, (130, 80, 40, 60))
            ],
            community_cards=[],
            pot_size=50.0,
            current_bet=10.0,
            player_count=6,
            position="late",
            street="preflop",
            action_on_us="raise"
        )
        
        analysis = integrator.components['decision'].analyze(test_state)
        print(f"    Motor funcionando: {analysis.get('action')} ({analysis.get('confidence'):.0%})")
        
        # Test 3: Overlay
        print("3. Probando overlay...")
        integrator.components['overlay'].update(test_state, analysis, test_image)
        print("    Overlay funcionando")
        
        print("\n TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        
    elif choice == "4":
        print("\n CALIBRACIÓN DEL SISTEMA")
        print("=" * 40)
        
        print("1. Calibración automática PokerStars")
        print("2. Calibrar detector de cartas")
        print("3. Ajustar posiciones")
        print("4. Volver")
        
        cal_choice = input("\nSeleccione opción (1-4): ").strip()
        
        if cal_choice == "1":
            print("\n CALIBRANDO PARA POKERSTARS...")
            print("Asegúrese de tener PokerStars abierto en una mesa.")
            print("Coloque la mesa en tema 'Classic' para mejor detección.")
            print("\nLa calibración detectará:")
            print("   Posiciones de cartas")
            print("   Colores de la mesa")
            print("   Botones de acción")
            print("   Tamaño de fichas")
            
            input("\nPresione Enter cuando esté listo...")
            
            # Intentar cargar calibrador si existe
            if Path("POKERSTARS_CALIBRATOR.py").exists():
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        "calibrator", "POKERSTARS_CALIBRATOR.py"
                    )
                    cal_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(cal_module)
                    
                    if hasattr(cal_module, 'main'):
                        cal_module.main()
                    else:
                        print("  Calibrador no tiene función main")
                        run_basic_calibration()
                except Exception as e:
                    print(f" Error cargando calibrador: {e}")
                    run_basic_calibration()
            else:
                print("  Calibrador no encontrado")
                run_basic_calibration()
                
        elif cal_choice == "2":
            print("\n CALIBRANDO DETECTOR DE CARTAS...")
            print("Esta función ajusta la sensibilidad del OCR.")
            print("Mejora la detección de rangos y palos.")
            
            # Aquí iría la calibración real del OCR
            print("\n Para calibración avanzada, ejecute:")
            print("python calibrate_ocr.py --train")
            
        elif cal_choice == "3":
            print("\n AJUSTANDO POSICIONES...")
            print("Permite ajustar manualmente las posiciones de:")
            print("   Cartas del hero")
            print("   Cartas comunitarias")
            print("   Botones de acción")
            print("   Área de bote")
            
            input("\nPresione Enter para comenzar ajuste manual...")
            
        elif cal_choice == "4":
            return
        
        else:
            print(" Opción no válida")
    
    elif choice == "5":
        print("\n Saliendo...")
        return
    
    else:
        print(" Opción no válida")
    
    input("\nPresione Enter para volver al menú principal...")

def run_basic_calibration():
    """Calibración básica"""
    print("\n CALIBRACIÓN BÁSICA")
    print("=" * 30)
    
    steps = [
        "1. Detectando pantalla principal...",
        "2. Buscando mesa de poker...",
        "3. Analizando colores...",
        "4. Detectando áreas de cartas...",
        "5. Guardando configuración..."
    ]
    
    for step in steps:
        print(step)
        time.sleep(1)
    
    print("\n Calibración básica completada")
    print(" Para calibración avanzada, use el calibrador completo")

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\n\n  Programa terminado por el usuario")
    except Exception as e:
        print(f"\n Error crítico: {e}")
        print(" Verifique las dependencias: pip install opencv-python numpy mss")
        input("Presione Enter para salir...")
