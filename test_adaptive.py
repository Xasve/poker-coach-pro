"""
test_adaptive.py - Probar el sistema de aprendizaje adaptativo
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from screen_capture.adaptive_recognizer import AdaptiveCardRecognizer
    
    print("🤖 SISTEMA DE APRENDIZAJE ADAPTATIVO")
    print("=" * 50)
    
    # Crear reconocedor
    recognizer = AdaptiveCardRecognizer(platform="ggpoker", stealth_level="MINIMUM")
    
    # Mostrar estadísticas
    stats = recognizer.get_learning_stats()
    
    print(f"\n📊 ESTADO DEL SISTEMA:")
    print(f"   Cartas aprendidas: {stats['total_learned_cards']}")
    print(f"   Confianza promedio: {stats['average_confidence']:.3f}")
    
    if stats['known_cards']:
        print(f"\n🃏 CARTAS CONOCIDAS ({len(stats['known_cards'])}):")
        # Mostrar en grupos
        cards = stats['known_cards']
        for i in range(0, len(cards), 8):
            print(f"   {', '.join(cards[i:i+8])}")
    
    print("\n🎯 INSTRUCCIONES:")
    print("1. Abre GG Poker o PokerStars")
    print("2. Juega normalmente")
    print("3. El sistema aprenderá automáticamente")
    print("4. Mejorará con cada mano que juegues")
    
    print("\n✅ ¡No necesitas capturar cartas manualmente!")
    print("   El sistema descargó cartas iniciales de internet")
    print("   y aprenderá las específicas de tu plataforma.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()