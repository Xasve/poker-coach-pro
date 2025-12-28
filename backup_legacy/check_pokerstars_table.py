# check_pokerstars_table.py - Verificar mesa PokerStars
import os
import sys

def check_table_type():
    """Verificar tipo de mesa PokerStars"""
    print(" VERIFICADOR DE MESA POKERSTARS")
    print("=" * 60)
    
    print("\n  POR FAVOR, VERIFICA VISUALMENTE:")
    print("-" * 50)
    
    print("1. Mira la ventana de PokerStars")
    print("2. Fíjate en el NOMBRE de la mesa")
    print("3. Responde las siguientes preguntas:")
    
    print("\n PREGUNTA 1:")
    print("   El nombre de la mesa contiene 'Classic'?")
    answer1 = input("   (s/n): ").strip().lower()
    
    print("\n PREGUNTA 2:")
    print("   El fondo de la mesa es CLARO/AMARILLO?")
    answer2 = input("   (s/n): ").strip().lower()
    
    print("\n❓ PREGUNTA 3:")
    print("   ¿Ves cartas ROJAS (♥️♦️) en la pantalla?")
    answer3 = input("   (s/n): ").strip().lower()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO DE LA VERIFICACIÓN:")
    
    score = 0
    if answer1 == 's':
        print("   ✅ La mesa es 'Classic' (CORRECTO)")
        score += 1
    else:
        print("   ❌ La mesa NO es 'Classic' (INCORRECTO)")
        print("      💡 Busca una mesa que diga 'Classic'")
    
    if answer2 == 's':
        print("    Fondo claro (CORRECTO)")
        score += 1
    else:
        print("    Fondo oscuro (INCORRECTO)")
        print("       Cambia a mesa con fondo claro")
    
    if answer3 == 's':
        print("    Ves cartas rojas (CORRECTO)")
        score += 1
    else:
        print("    NO ves cartas rojas (PROBLEMA CRÍTICO)")
        print("       SAL de esta mesa inmediatamente")
        print("       Busca otra mesa 'Classic'")
    
    print("\n" + "=" * 60)
    
    if score == 3:
        print(" MESA PERFECTA! Puedes continuar.")
        print("\n Siguiente paso:")
        print("   Ejecuta: python detect_coords.py")
        return True
    elif score >= 2:
        print("⚠️  Mesa aceptable, pero podrías mejorar.")
        print("\n💡 Recomendación:")
        print("   Busca una mesa mejor o continúa así.")
        return True
    else:
        print(" MESA INCORRECTA. No continúes.")
        print("\n Acción requerida:")
        print("   1. SAL de esta mesa")
        print("   2. Busca mesa 'NL Hold'em Classic'")
        print("   3. Vuelve a ejecutar este verificador")
        return False

def quick_fix_instructions():
    """Instrucciones de solución rápida"""
    print("\n🔧 SOLUCIÓN RÁPIDA PARA MESA INCORRECTA:")
    print("-" * 50)
    
    print("1. En PokerStars, ve a 'Cash Games'")
    print("2. Filtra por 'Hold'em' -> 'No Limit'")
    print("3. Busca mesas que digan 'Classic'")
    print("4. Únete a una con fondo claro/amarillo")
    print("5. Espera a ver cartas ROJAS")
    
    print("\n MESAS RECOMENDADAS:")
    print("    'NL Hold'em Classic'")
    print("   • 'PL Omaha Classic'")
    print("   • Cualquier '... Classic'")
    
    print("\n❌ MESAS A EVITAR:")
    print("   • Cualquier '... Dark'")
    print("   • Cualquier '... Stealth'")
    print("   • Cualquier '... Night'")

def main():
    """Función principal"""
    print(" VERIFICACIÓN DE MESA POKERSTARS")
    print("=" * 70)
    print("Este script te ayuda a verificar si estás")
    print("en la mesa correcta de PokerStars.")
    print("=" * 70)
    
    if check_table_type():
        print("\n Puedes continuar con la configuración")
        print("\n Siguiente paso:")
        print("   Ejecuta: python pokerstars_assistant.py")
        print("   O directamente: python detect_coords.py")
    else:
        quick_fix_instructions()
        print("\n Vuelve a ejecutar este script después de")
        print("   cambiar a una mesa correcta.")

if __name__ == "__main__":
    main()
