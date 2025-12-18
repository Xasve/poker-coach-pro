#!/usr/bin/env python3
"""
Script para probar el sistema de validación de calidad
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_decision_validation():
    """Probar el sistema de validación"""
    
    print("🎴 POKER COACH PRO - TEST DE CALIDAD")
    print("="*60)
    
    try:
        from quality.decision_validator import DecisionValidator
        
        # Crear validador
        validator = DecisionValidator(platform="ggpoker")
        
        print("✅ Validador creado correctamente")
        
        # Caso de prueba 1: Decisión buena
        print("\n" + "="*60)
        print("Caso 1: Decisión buena (RAISE con mano premium)")
        print("="*60)
        
        game_state1 = {
            'platform': 'ggpoker',
            'street': 'preflop',
            'position': 'BTN',
            'hero_cards': ['Ah', 'Ks'],
            'board_cards': [],
            'pot_size': 1.5,
            'bet_to_call': 0,
            'stack_bb': 100,
            'action_to_us': True
        }
        
        decision1 = {
            'action': 'RAISE',
            'size': '2.2BB',
            'confidence': 85,
            'reason': 'Mano premium en posición. Open estándar.',
            'alternatives': ['FOLD']
        }
        
        validation1 = validator.validate_decision(game_state1, decision1)
        print(f"Calidad: {validation1['quality']}")
        print(f"Puntuación: {validation1['score']}/100")
        print(f"Fortalezas: {validation1.get('strengths', [])}")
        
        # Caso de prueba 2: Decisión mala
        print("\n" + "="*60)
        print("Caso 2: Decisión mala (FOLD con mano premium)")
        print("="*60)
        
        decision2 = {
            'action': 'FOLD',
            'size': '',
            'confidence': 60,
            'reason': 'Miedo a 3-bet',
            'alternatives': []
        }
        
        validation2 = validator.validate_decision(game_state1, decision2)
        print(f"Calidad: {validation2['quality']}")
        print(f"Puntuación: {validation2['score']}/100")
        print(f"Debilidades: {validation2.get('weaknesses', [])}")
        
        # Caso de prueba 3: Postflop
        print("\n" + "="*60)
        print("Caso 3: Postflop (C-bet en flop seco)")
        print("="*60)
        
        game_state3 = {
            'platform': 'ggpoker',
            'street': 'flop',
            'position': 'BTN',
            'hero_cards': ['Ah', 'Ks'],
            'board_cards': ['2h', '7d', 'Ts'],
            'pot_size': 5.0,
            'bet_to_call': 0,
            'stack_bb': 80,
            'action_to_us': True
        }
        
        decision3 = {
            'action': 'BET',
            'size': '33% pot',
            'confidence': 75,
            'reason': 'C-bet estándar en flop seco',
            'alternatives': ['CHECK']
        }
        
        validation3 = validator.validate_decision(game_state3, decision3)
        print(f"Calidad: {validation3['quality']}")
        print(f"Puntuación: {validation3['score']}/100")
        print(f"Análisis: {validation3.get('sizing_analysis', {})}")
        
        # Generar reporte
        print("\n" + "="*60)
        print("📊 REPORTE DE CALIDAD FINAL")
        print("="*60)
        
        report = validator.generate_quality_report()
        print(report)
        
        print("\n✅ Test completado exitosamente")
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("\n📦 Instala las dependencias:")
        print("pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

def interactive_test():
    """Test interactivo de decisiones"""
    
    print("🎴 TEST INTERACTIVO DE DECISIONES")
    print("="*60)
    
    try:
        from quality.decision_validator import DecisionValidator
        
        validator = DecisionValidator()
        
        while True:
            print("\n" + "="*60)
            print("Ingresa los detalles de la situación:")
            print("="*60)
            
            # Entrada de datos
            street = input("Calle (preflop/flop/turn/river): ").strip().lower()
            position = input("Posición (UTG/MP/CO/BTN/SB/BB): ").strip().upper()
            hero_cards_input = input("Tus cartas (ej: Ah Ks): ").strip()
            hero_cards = hero_cards_input.split() if hero_cards_input else []
            
            board_cards_input = input("Cartas mesa (deja vacío si preflop): ").strip()
            board_cards = board_cards_input.split() if board_cards_input else []
            
            try:
                pot_size = float(input("Tamaño del pot ($): ").strip())
                bet_to_call = float(input("Apuesta a pagar ($, 0 si no hay): ").strip())
            except:
                pot_size = 0
                bet_to_call = 0
            
            print("\n" + "="*60)
            print("Ingresa la decisión:")
            print("="*60)
            
            action = input("Acción (FOLD/CHECK/CALL/BET/RAISE/ALL-IN): ").strip().upper()
            size = input("Tamaño (ej: 2.2BB, 33% pot): ").strip() if action in ['BET', 'RAISE'] else ""
            
            # Crear estado del juego
            game_state = {
                'platform': 'ggpoker',
                'street': street,
                'position': position,
                'hero_cards': hero_cards,
                'board_cards': board_cards,
                'pot_size': pot_size,
                'bet_to_call': bet_to_call,
                'stack_bb': 100,  # Valor por defecto
                'action_to_us': bet_to_call > 0
            }
            
            # Crear decisión
            decision = {
                'action': action,
                'size': size,
                'confidence': 70,
                'reason': 'Decisión del usuario',
                'alternatives': []
            }
            
            # Validar
            validation = validator.validate_decision(game_state, decision)
            
            print("\n" + "="*60)
            print("📊 RESULTADO DE LA VALIDACIÓN")
            print("="*60)
            
            print(f"Calidad: {validation['quality']}")
            print(f"Puntuación: {validation['score']}/100")
            
            if validation.get('strengths'):
                print("\n✅ Fortalezas:")
                for strength in validation['strengths']:
                    print(f"  • {strength}")
            
            if validation.get('weaknesses'):
                print("\n⚠️  Debilidades:")
                for weakness in validation['weaknesses']:
                    print(f"  • {weakness}")
            
            if validation.get('suggestions'):
                print("\n💡 Sugerencias:")
                for suggestion in validation['suggestions']:
                    print(f"  • {suggestion}")
            
            # Preguntar si continuar
            continuar = input("\n¿Probar otra decisión? (s/n): ").strip().lower()
            if continuar != 's':
                break
        
        # Mostrar reporte final
        print("\n" + "="*60)
        print("📈 REPORTE FINAL DE LA SESIÓN")
        print("="*60)
        
        report = validator.generate_quality_report()
        print(report)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║  SISTEMA DE VALIDACIÓN DE CALIDAD    ║
    ║      Poker Coach Pro v2.0            ║
    ╚══════════════════════════════════════╝
    """)
    
    print("Selecciona el modo de test:")
    print("1. Test automático (casos predefinidos)")
    print("2. Test interactivo (tú proporcionas los datos)")
    print("3. Salir")
    
    choice = input("\nOpción (1-3): ").strip()
    
    if choice == '1':
        test_decision_validation()
    elif choice == '2':
        interactive_test()
    else:
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()