#!/usr/bin/env python3
"""
Test CORREGIDO del sistema de validación de calidad
Versión que SÍ funciona
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_decision_validation():
    """Probar el sistema de validación CORREGIDO"""
    
    print("🎴 POKER COACH PRO - TEST DE CALIDAD (CORREGIDO)")
    print("="*60)
    
    try:
        # Importar versión corregida
        from quality.decision_validator_fixed import SimpleDecisionValidator
        
        # Crear validador
        validator = SimpleDecisionValidator(platform="ggpoker")
        
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
        
        if validation1.get('strengths'):
            print("✅ Fortalezas:")
            for strength in validation1['strengths']:
                print(f"  • {strength}")
        
        if validation1.get('weaknesses'):
            print("⚠️  Debilidades:")
            for weakness in validation1['weaknesses']:
                print(f"  • {weakness}")
        
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
        
        if validation2.get('weaknesses'):
            print("⚠️  Debilidades:")
            for weakness in validation2['weaknesses']:
                print(f"  • {weakness}")
        
        # Caso de prueba 3: Postflop
        print("\n" + "="*60)
        print("Caso 3: Postflop (C-bet en flop)")
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
            'reason': 'C-bet estándar en flop',
            'alternatives': ['CHECK']
        }
        
        validation3 = validator.validate_decision(game_state3, decision3)
        print(f"Calidad: {validation3['quality']}")
        print(f"Puntuación: {validation3['score']}/100")
        
        # Caso de prueba 4: Call con malas odds
        print("\n" + "="*60)
        print("Caso 4: Call con malas pot odds")
        print("="*60)
        
        game_state4 = {
            'platform': 'ggpoker',
            'street': 'flop',
            'position': 'BB',
            'hero_cards': ['8h', '9h'],
            'board_cards': ['2h', '7d', 'Ts'],
            'pot_size': 10.0,
            'bet_to_call': 8.0,  # Malas odds: 8/(10+8) = 44%
            'stack_bb': 50,
            'action_to_us': True
        }
        
        decision4 = {
            'action': 'CALL',
            'size': '8.0',
            'confidence': 50,
            'reason': 'Tengo flush draw',
            'alternatives': ['FOLD']
        }
        
        validation4 = validator.validate_decision(game_state4, decision4)
        print(f"Calidad: {validation4['quality']}")
        print(f"Puntuación: {validation4['score']}/100")
        
        # Generar reporte
        print("\n" + "="*60)
        print("📊 REPORTE DE CALIDAD FINAL")
        print("="*60)
        
        report = validator.generate_quality_report()
        print(report)
        
        print("\n✅ Test completado exitosamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("\n📦 Asegúrate de que el archivo existe en:")
        print("   src/quality/decision_validator_fixed.py")
        return False
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_test():
    """Test interactivo CORREGIDO"""
    
    print("🎴 TEST INTERACTIVO DE DECISIONES (CORREGIDO)")
    print("="*60)
    
    try:
        from quality.decision_validator_fixed import SimpleDecisionValidator
        
        validator = SimpleDecisionValidator()
        
        while True:
            print("\n" + "="*60)
            print("Ingresa los detalles de la situación:")
            print("="*60)
            
            # Entrada de datos simple
            street = input("Calle (preflop/flop/turn/river): ").strip().lower() or "preflop"
            position = input("Posición (UTG/MP/CO/BTN/SB/BB): ").strip().upper() or "BTN"
            
            print("\nEjemplos de cartas: Ah Ks (As de corazones, Rey de picas)")
            hero_cards_input = input("Tus cartas (ej: Ah Ks): ").strip() or "Ah Ks"
            hero_cards = hero_cards_input.split()
            
            action = input("\nAcción (FOLD/CHECK/CALL/BET/RAISE/ALL-IN): ").strip().upper() or "FOLD"
            
            size = ""
            if action in ['BET', 'RAISE']:
                size = input("Tamaño (ej: 2.2BB, 33% pot): ").strip()
            
            print("\n" + "="*60)
            print("Analizando decisión...")
            print("="*60)
            
            # Crear estado del juego
            game_state = {
                'platform': 'ggpoker',
                'street': street,
                'position': position,
                'hero_cards': hero_cards,
                'board_cards': [],
                'pot_size': 5.0,
                'bet_to_call': 0 if street == 'preflop' else 2.0,
                'stack_bb': 100,
                'action_to_us': True
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
            
            print("\n📊 RESULTADO DE LA VALIDACIÓN")
            print("="*60)
            
            # Color según calidad
            colors = {
                'EXCELENTE': '\033[92m',  # Verde
                'BUENA': '\033[94m',      # Azul
                'ACEPTABLE': '\033[93m',  # Amarillo
                'CUESTIONABLE': '\033[91m', # Rojo claro
                'MALA': '\033[91m'        # Rojo
            }
            reset = '\033[0m'
            
            quality_color = colors.get(validation['quality'], '')
            print(f"Calidad: {quality_color}{validation['quality']}{reset}")
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
        import traceback
        traceback.print_exc()

def quick_validation_examples():
    """Ejemplos rápidos de validación"""
    
    print("🎴 EJEMPLOS RÁPIDOS DE VALIDACIÓN")
    print("="*60)
    
    examples = [
        {
            "name": "1. RAISE con AA desde UTG",
            "game_state": {
                'street': 'preflop',
                'position': 'UTG',
                'hero_cards': ['Ah', 'Ad'],
                'pot_size': 1.5,
                'bet_to_call': 0
            },
            "decision": {
                'action': 'RAISE',
                'size': '2.2BB',
                'reason': 'Mano premium'
            },
            "expected_quality": "EXCELENTE"
        },
        {
            "name": "2. FOLD con 72o desde UTG",
            "game_state": {
                'street': 'preflop',
                'position': 'UTG',
                'hero_cards': ['7h', '2d'],
                'pot_size': 1.5,
                'bet_to_call': 0
            },
            "decision": {
                'action': 'FOLD',
                'size': '',
                'reason': 'Mano muy débil'
            },
            "expected_quality": "EXCELENTE"
        },
        {
            "name": "3. CALL con mano débil desde EP",
            "game_state": {
                'street': 'preflop',
                'position': 'UTG',
                'hero_cards': ['7h', '2d'],
                'pot_size': 1.5,
                'bet_to_call': 0
            },
            "decision": {
                'action': 'CALL',
                'size': '1BB',
                'reason': 'Quiero ver flop'
            },
            "expected_quality": "MALA"
        },
        {
            "name": "4. C-bet estándar en flop seco",
            "game_state": {
                'street': 'flop',
                'position': 'BTN',
                'hero_cards': ['Ah', 'Ks'],
                'board_cards': ['2h', '7d', 'Ts'],
                'pot_size': 5.0,
                'bet_to_call': 0
            },
            "decision": {
                'action': 'BET',
                'size': '33% pot',
                'reason': 'C-bet estándar'
            },
            "expected_quality": "BUENA"
        }
    ]
    
    try:
        from quality.decision_validator_fixed import SimpleDecisionValidator
        validator = SimpleDecisionValidator()
        
        for example in examples:
            print(f"\n{example['name']}")
            print("-" * 40)
            
            # Completar game_state
            game_state = example['game_state']
            game_state.update({
                'platform': 'ggpoker',
                'stack_bb': 100,
                'action_to_us': True
            })
            
            validation = validator.validate_decision(game_state, example['decision'])
            
            print(f"Decisión: {example['decision']['action']} {example['decision'].get('size', '')}")
            print(f"Calidad: {validation['quality']} (esperado: {example['expected_quality']})")
            print(f"Puntuación: {validation['score']}/100")
            
            if validation['quality'] == example['expected_quality']:
                print("✅ Resultado CORRECTO")
            else:
                print("⚠️  Resultado diferente al esperado")
            
            # Mostrar análisis breve
            if validation.get('strengths'):
                print(f"  Fortalezas: {', '.join(validation['strengths'][:1])}")
            if validation.get('weaknesses'):
                print(f"  Debilidades: {', '.join(validation['weaknesses'][:1])}")
        
        print("\n" + "="*60)
        print("🎯 RESUMEN DE EJEMPLOS")
        print("="*60)
        
        report = validator.generate_quality_report()
        print(report)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Función principal CORREGIDA"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║  SISTEMA DE VALIDACIÓN DE CALIDAD    ║
    ║      Poker Coach Pro - CORREGIDO     ║
    ╚══════════════════════════════════════╝
    """)
    
    print("Selecciona el modo de test (CORREGIDO):")
    print("1. Test automático (casos predefinidos)")
    print("2. Test interactivo (tú proporcionas los datos)")
    print("3. Ejemplos rápidos de validación")
    print("4. Salir")
    
    choice = input("\nOpción (1-4): ").strip() or "1"
    
    if choice == '1':
        success = test_decision_validation()
        if not success:
            print("\n⚠️  Para solucionar este error:")
            print("1. Asegúrate de que el archivo existe:")
            print("   src/quality/decision_validator_fixed.py")
            print("2. Si no existe, créalo con el código proporcionado")
            print("3. Ejecuta de nuevo el test")
    elif choice == '2':
        interactive_test()
    elif choice == '3':
        quick_validation_examples()
    else:
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()