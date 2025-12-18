#!/usr/bin/env python3
"""
Verificación RÁPIDA de calidad de decisiones
No requiere instalación, solo Python
"""

def quick_check(street, position, hand, action, size=""):
    """Verificación rápida de calidad"""
    
    print(f"\n🎴 Verificando: {street} | {position} | {hand}")
    print(f"Decisión: {action} {size}")
    print("-" * 40)
    
    score = 70
    feedback = []
    
    # REGLA 1: Manos premium = RAISE
    premium_hands = ['AA', 'KK', 'QQ', 'JJ', 'TT', 'AKs', 'AQs']
    if hand in premium_hands:
        if action == 'RAISE':
            score += 20
            feedback.append("✅ Mano premium, raise correcto")
        else:
            score -= 20
            feedback.append("❌ Mano premium debería raise")
    
    # REGLA 2: Manos muy débiles desde EP = FOLD
    weak_hands = ['72o', '83o', '92o', 'T2o', 'J2o', 'Q2o', 'K2o', 'A2o']
    if position == 'UTG' and hand in weak_hands:
        if action == 'FOLD':
            score += 15
            feedback.append("✅ Mano débil desde UTG, fold correcto")
        else:
            score -= 15
            feedback.append("❌ Mano muy débil desde UTG, debería fold")
    
    # REGLA 3: Tamaño preflop
    if street == 'preflop' and action == 'RAISE':
        try:
            if 'BB' in size:
                bb_size = float(size.replace('BB', ''))
                if 2.0 <= bb_size <= 2.5:
                    score += 10
                    feedback.append("✅ Tamaño de raise correcto")
                else:
                    score -= 10
                    feedback.append(f"⚠️  Tamaño {bb_size}BB, ideal 2.2BB")
        except:
            pass
    
    # Calidad final
    score = max(0, min(100, score))
    
    if score >= 90:
        quality = "EXCELENTE 🏆"
    elif score >= 75:
        quality = "BUENA 👍"
    elif score >= 60:
        quality = "ACEPTABLE ⚠️"
    elif score >= 40:
        quality = "CUESTIONABLE 🔧"
    else:
        quality = "MALA ❌"
    
    print(f"Puntuación: {score}/100")
    print(f"Calidad: {quality}")
    
    if feedback:
        print("\n📝 Análisis:")
        for item in feedback:
            print(f"  {item}")
    
    return score

def main():
    print("""
    ╔══════════════════════════════════╗
    ║  VERIFICACIÓN RÁPIDA DE CALIDAD  ║
    ╚══════════════════════════════════╝
    """)
    
    print("Ejemplos de formato:")
    print("  Mano: AA (pocket aces), AKs (Ace-King suited)")
    print("  Tamaño: 2.2BB, 33% pot")
    print()
    
    # Ejemplos predefinidos
    examples = [
        ("preflop", "BTN", "AA", "RAISE", "2.2BB"),
        ("preflop", "UTG", "72o", "FOLD", ""),
        ("preflop", "UTG", "AQo", "RAISE", "2.2BB"),
        ("preflop", "BB", "KQs", "CALL", "1BB"),
    ]
    
    total_score = 0
    
    for i, (street, position, hand, action, size) in enumerate(examples, 1):
        print(f"\n📋 Ejemplo {i}:")
        score = quick_check(street, position, hand, action, size)
        total_score += score
    
    promedio = total_score / len(examples)
    
    print(f"\n{'='*40}")
    print(f"📊 PUNTUACIÓN PROMEDIO: {promedio:.1f}/100")
    
    if promedio >= 85:
        print("🎉 ¡Excelente! Tu estrategia es sólida")
    elif promedio >= 70:
        print("👍 Buen trabajo, algunas mejoras posibles")
    else:
        print("🔧 Considera revisar tu estrategia")
    
    print("\n💡 Consejo: Juega tight desde posiciones tempranas")
    print("💡 Consejo: Defiende BB ampliamente")
    print("💡 Consejo: Fold AQo desde UTG en mesas full")

if __name__ == "__main__":
    main()