#!/usr/bin/env python3
# Script de ejecución automática para Poker Coach Pro
import os
import sys
import subprocess

def main():
    print(" POKER COACH PRO - EJECUTOR AUTOMÁTICO")
    print("=" * 50)
    
    # Opciones de ejecución
    python_options = []
    
    # 1. Entorno virtual (recomendado)
    venv_python = "poker_env_311\Scripts\python.exe"
    if os.path.exists(venv_python):
        python_options.append((" Entorno virtual 3.11", venv_python))
    
    # 2. Python 3.11 directo
    python311_bat = "python311_scripts\python311.bat"
    if os.path.exists(python311_bat.replace(".bat", ".bat")):
        python_options.append((" Python 3.11 directo", python311_bat))
    
    # 3. Python del sistema (última opción)
    python_options.append((" Python del sistema", "python"))
    
    print("Selecciona el intérprete de Python:")
    for i, (name, path) in enumerate(python_options, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("\nOpción (1-3): ").strip())
        if 1 <= choice <= len(python_options):
            selected_name, selected_path = python_options[choice-1]
            print(f"\nUsando: {selected_name}")
            
            # Ejecutar quick_start.py
            cmd = f'"{selected_path}" quick_start.py'
            print(f"Comando: {cmd}")
            
            # Ejecutar en una nueva ventana de PowerShell
            ps_script = f'''
            cd "{os.getcwd()}"
            {cmd}
            pause
            '''
            
            ps_file = "temp_run.ps1"
            with open(ps_file, 'w', encoding='utf-8') as f:
                f.write(ps_script)
            
            os.system(f'start powershell -NoExit -File "{ps_file}"')
            
        else:
            print(" Opción no válida")
    except ValueError:
        print(" Entrada no válida")

if __name__ == "__main__":
    main()
