# ============================================================================
# SISTEMA DE MONITOREO PROFESIONAL EN TIEMPO REAL
# ============================================================================

import time
from datetime import datetime
from collections import deque
import threading

class ProfessionalMonitor:
    """Monitor profesional que verifica decisiones en tiempo real"""
    
    def __init__(self):
        self.decision_history = deque(maxlen=1000)
        self.performance_metrics = {
            'professional_decisions': 0,
            'suboptimal_decisions': 0,
            'learning_opportunities': 0,
            'average_decision_quality': 0.0
        }
        
        self.professional_standards = {
            'preflop': {
                'vpip_range': (18, 24),
                'pfr_range': (16, 22),
                '3bet_range': (8, 12)
            },
            'postflop': {
                'cbet_frequency': (65, 75),
                'turn_continuation': (40, 60),
                'river_aggression': (30, 50)
            },
            'psychological': {
                'adjustment_frequency': 'every_100_hands',
                'image_awareness': 'high',
                'tilt_resistance': 'excellent'
            }
        }
    
    def monitor_decision(self, decision, context):
        """Monitorear cada decisión en tiempo real"""
        
        start_time = time.time()
        
        # Evaluar calidad profesional
        quality_score = self._evaluate_professional_quality(decision, context)
        
        # Verificar contra estándares profesionales
        standards_check = self._check_against_standards(decision, context)
        
        # Identificar oportunidades de aprendizaje
        learning_ops = self._identify_learning_opportunities(decision, context)
        
        # Actualizar métricas
        self._update_metrics(quality_score, standards_check)
        
        monitoring_time = time.time() - start_time
        
        return {
            'monitoring_timestamp': datetime.now().isoformat(),
            'decision_quality_score': quality_score,
            'professional_standards_met': standards_check['met'],
            'learning_opportunities': learning_ops,
            'monitoring_time_ms': monitoring_time * 1000,
            'professional_rating': self._assign_professional_rating(quality_score),
            'recommendations': self._generate_recommendations(standards_check)
        }
    
    def _evaluate_professional_quality(self, decision, context):
        """Evaluar calidad profesional de una decisión"""
        
        factors = {
            'mathematical_correctness': self._evaluate_math(decision, context),
            'strategic_soundness': self._evaluate_strategy(decision, context),
            'exploitative_effectiveness': self._evaluate_exploitation(decision, context),
            'psychological_appropriateness': self._evaluate_psychology(decision, context)
        }
        
        # Ponderar factores
        weights = {
            'mathematical_correctness': 0.30,
            'strategic_soundness': 0.25,
            'exploitative_effectiveness': 0.25,
            'psychological_appropriateness': 0.20
        }
        
        weighted_score = sum(factors[k] * weights[k] for k in factors)
        
        return weighted_score
    
    def _check_against_standards(self, decision, context):
        """Verificar contra estándares profesionales"""
        
        street = context.get('street', 'preflop')
        standards = self.professional_standards.get(street, {})
        
        met_standards = []
        missed_standards = []
        
        for standard, value_range in standards.items():
            if isinstance(value_range, tuple):
                # Rango numérico
                decision_value = decision.get(standard, 0)
                if value_range[0] <= decision_value <= value_range[1]:
                    met_standards.append(standard)
                else:
                    missed_standards.append({
                        'standard': standard,
                        'expected': value_range,
                        'actual': decision_value
                    })
        
        return {
            'met': met_standards,
            'missed': missed_standards,
            'compliance_rate': len(met_standards) / (len(met_standards) + len(missed_standards))
        }
    
    def _assign_professional_rating(self, score):
        """Asignar calificación profesional"""
        
        if score >= 0.95:
            return "WORLD CLASS"
        elif score >= 0.90:
            return "ELITE"
        elif score >= 0.85:
            return "ADVANCED"
        elif score >= 0.80:
            return "PROFESSIONAL"
        elif score >= 0.75:
            return "SEMI-PRO"
        else:
            return "NEEDS IMPROVEMENT"
    
    def generate_performance_report(self):
        """Generar reporte de rendimiento"""
        
        report = {
            'report_date': datetime.now().isoformat(),
            'decisions_monitored': len(self.decision_history),
            'professional_decisions': self.performance_metrics['professional_decisions'],
            'professional_decision_rate': (
                self.performance_metrics['professional_decisions'] / 
                max(len(self.decision_history), 1)
            ),
            'average_decision_quality': self.performance_metrics['average_decision_quality'],
            'top_strengths': self._identify_top_strengths(),
            'improvement_areas': self._identify_improvement_areas(),
            'learning_progress': self._calculate_learning_progress()
        }
        
        return report

def real_time_monitoring_demo():
    """Demostración de monitoreo en tiempo real"""
    
    monitor = ProfessionalMonitor()
    
    print(" MONITOREO PROFESIONAL EN TIEMPO REAL")
    print("="*60)
    
    # Simular algunas decisiones
    test_decisions = [
        {
            'action': 'RAISE',
            'size': 3.0,
            'street': 'preflop',
            'position': 'BTN',
            'vpip': 22.5,
            'pfr': 20.1,
            '3bet': 9.8
        },
        {
            'action': 'CBET',
            'size': 0.75,
            'street': 'flop',
            'board': 'dry',
            'cbet_frequency': 68.2,
            'turn_continuation': 52.3
        },
        {
            'action': 'BLUFF',
            'size': 1.5,
            'street': 'river',
            'board': 'dynamic',
            'river_aggression': 42.7,
            'bluff_frequency': 31.5
        }
    ]
    
    for i, decision in enumerate(test_decisions, 1):
        print(f"\n Decisión {i}: {decision['action']} en {decision['street']}")
        
        context = {
            'street': decision['street'],
            'position': decision.get('position', 'unknown'),
            'board_texture': decision.get('board', 'unknown')
        }
        
        monitoring_result = monitor.monitor_decision(decision, context)
        
        print(f"   Calificación: {monitoring_result['professional_rating']}")
        print(f"   Puntuación: {monitoring_result['decision_quality_score']:.1%}")
        print(f"   Estándares cumplidos: {len(monitoring_result['professional_standards_met'])}")
    
    # Generar reporte final
    print("\n" + "="*60)
    print(" REPORTE FINAL DE MONITOREO")
    print("="*60)
    
    report = monitor.generate_performance_report()
    
    print(f"Decisiones monitoreadas: {report['decisions_monitored']}")
    print(f"Decisiones profesionales: {report['professional_decisions']}")
    print(f"Tasa profesional: {report['professional_decision_rate']:.1%}")
    print(f"Calidad promedio: {report['average_decision_quality']:.1%}")
    
    print("\n FORTALEZAS PRINCIPALES:")
    for strength in report['top_strengths'][:3]:
        print(f"    {strength}")
    
    print("\n ÁREAS DE MEJORA:")
    for area in report['improvement_areas'][:3]:
        print(f"    {area}")

if __name__ == "__main__":
    real_time_monitoring_demo()
