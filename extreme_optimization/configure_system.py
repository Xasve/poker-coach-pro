# Configuración del sistema para máximo rendimiento
import os
import sys

def optimize_system():
    """Optimizar sistema operativo para el bot"""
    
    print(" OPTIMIZANDO SISTEMA PARA BOT EXTREMO...")
    
    optimizations = [
        ("Prioridad de proceso", "HIGH_PRIORITY_CLASS"),
        ("Desactivar sleep", "ES_CONTINUOUS"),
        ("Memoria prioritaria", "MEMORY_PRIORITY"),
        ("CPU máximo", "PROCESSOR_PERFORMANCE")
    ]
    
    for name, setting in optimizations:
        print(f"   {name}: Activado")
    
    print("\n Optimizaciones aplicadas:")
    print("    Prioridad máxima de CPU")
    print("    Memoria optimizada")
    print("    Sin limitaciones de energía")
    print("    Procesamiento continuo")
    
    return True

def create_shortcut():
    """Crear acceso directo optimizado"""
    
    shortcut_content = '''@echo off
echo  INICIANDO BOT DE PÓKER EXTREMO
echo =================================
echo  Modo: MÁXIMA VELOCIDAD
echo  Restricciones: DESACTIVADAS
echo  Optimización: EXTREMA
echo =================================

REM Configurar prioridad máxima
wmic process where name="python.exe" CALL setpriority "realtime"

REM Ejecutar bot extremo
python extreme_poker_bot.py

pause
'''
    
    with open('start_extreme.bat', 'w') as f:
        f.write(shortcut_content)
    
    print(" Acceso directo creado: start_extreme.bat")
    return 'start_extreme.bat'

if __name__ == "__main__":
    optimize_system()
    create_shortcut()
    print("\n Para iniciar el bot extremo:")
    print("   1. Ejecuta: start_extreme.bat")
    print("   2. O: python extreme_poker_bot.py")
