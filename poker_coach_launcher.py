#!/usr/bin/env python3
"""
POKER COACH PRO - LAUNCHER SIMPLE
Versión minimalista pero funcional
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("POKER COACH PRO - MENU PRINCIPAL")
    print("=" * 60)
    
    # Scripts principales disponibles
    main_scripts = [
        ("test_pokerstars.py", "Sistema COMPLETO PokerStars"),
        ("test_ggpoker_simple.py", "Sistema COMPLETO GG Poker"),
        ("test_capture.py", "Probar captura de pantalla"),
        ("check.py", "Verificar sistema completo"),
        ("cleanup.py", "Limpiar archivos duplicados"),
        ("src/integration/pokerstars_coach.py", "Integrador avanzado")
    ]
    
    # Filtrar solo los que existen
    available_scripts = []
    for script, desc in main_scripts:
        if os.path.exists(script):
            available_scripts.append((script, desc))
    
    if not available_scripts:
        print("\n❌ No se encontraron scripts principales")
        return
    
    print("\n🎯 SCRIPTS DISPONIBLES:")
    for i, (script, desc) in enumerate(available_scripts, 1):
        print(f"\n  {i}. {script}")
        print(f"     📖 {desc}")
    
    print(f"\n  {len(available_scripts) + 1}. 🚪 Salir")
    
    try:
        choice = input(f"\n👉 Selecciona (1-{len(available_scripts) + 1}): ").strip()
        
        if choice.isdigit():
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(available_scripts):
                script_name, description = available_scripts[choice_num - 1]
                
                print(f"\n🚀 Ejecutando: {script_name}")
                print(f"📖 {description}")
                print("-" * 50)
                
                # Ejecutar script
                subprocess.run([sys.executable, script_name])
                
                print("\n" + "=" * 50)
                print("✅ Script completado")
                
            elif choice_num == len(available_scripts) + 1:
                print("\n👋 ¡Hasta pronto!")
            else:
                print("\n❌ Opción inválida")
        else:
            print("\n❌ Por favor ingresa un número")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Operación cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()