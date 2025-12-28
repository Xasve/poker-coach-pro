# pokerstars_assistant.py - Asistente paso a paso
import os
import sys
import time
import json

def print_step(number, title, description):
    """Imprimir paso con formato"""
    print(f"\n{'='*60}")
    print(f"🎯 PASO {number}: {title}")
    print(f"{'='*60}")
    print(description)
    input("\n👉 Presiona Enter para continuar...")

def check_pokerstars_open():
    """Verificar si PokerStars está abierto"""
    print("\n VERIFICANDO POKERSTARS...")
    print("-" * 50)
    
    print("1. Por favor, ABRE PokerStars en tu computadora")
    print("2. Asegúrate de que esté ejecutándose")
    print("3. Si no lo tienes instalado, instálalo primero")
    
    input("\n👉 Cuando PokerStars esté abierto, presiona Enter...")

def guide_table_selection():
    """Guía para seleccionar mesa correcta"""
    print_step(1, "SELECCIONAR MESA CORRECTA", 
        """ MESAS CORRECTAS (con cartas rojas):
            Busca 'NL Hold'em Classic'
            O 'PL Omaha Classic'
           • O cualquier mesa que diga 'Classic'
           
           ❌ MESAS INCORRECTAS (solo cartas negras):
            CUALQUIER mesa con 'Dark'
            CUALQUIER mesa con 'Stealth'
            CUALQUIER mesa con 'Night'
           
           � CONSEJO:
           - Elige mesas con fondo CLARO/AMARILLO
           - Evita mesas con fondo OSCURO/NEGRO""")

def guide_visual_verification():
    """Guía para verificación visual"""
    print_step(2, "VERIFICACIÓN VISUAL", 
        """ VERIFICA CON TUS PROPIOS OJOS:
           
           1. Únete a una mesa 'Classic'
           2. Espera a que repartan cartas
           3. MIRA las cartas en la pantalla
           
           ❓ ¿Ves cartas ROJAS? (♥️♦️)
           - Si NO ves rojas: SAL de esa mesa
           - Busca OTRA mesa 'Classic'
           
            Esto es CRÍTICO:
           El sistema NO funcionará sin cartas rojas""")

def run_detection():
    """Ejecutar detección de coordenadas"""
    print_step(3, "CONFIGURAR CAPTURA", 
        """🎮 AHORA CONFIGURAREMOS LA CAPTURA:
           
           El script detect_coords.py te pedirá:
           1. Haz clic en tu PRIMERA carta (hero card 1)
           2. Haz clic en tu SEGUNDA carta (hero card 2)
           3. Haz clic en las cartas COMUNITARIAS
           
            INSTRUCCIONES:
           - Usa el MOUSE para hacer clic
           - Sigue las instrucciones en pantalla
           - No cierres PokerStars durante el proceso""")
    
    print("\n EJECUTANDO CONFIGURACIÓN...")
    os.system("python detect_coords.py")

def run_balanced_capture():
    """Ejecutar captura balanceada"""
    print_step(4, "CAPTURAR DATASET BALANCEADO", 
        """ AHORA CAPTURAREMOS CARTAS:
           
           El script capturará automáticamente:
            Al menos 100 cartas
            Balanceando rojas y negras
            Con pausas automáticas
           
            DURACIÓN: 2-3 minutos
            OBJETIVO: 30-40% cartas rojas
           
            Durante la captura:
           - NO muevas la ventana de PokerStars
           - Deja que el script trabaje
           - Puedes presionar Ctrl+C para detener""")
    
    print("\n CONFIGURANDO CAPTURA...")
    
    try:
        target = input("Cuántas cartas capturar? (default: 100): ").strip()
        target_count = int(target) if target.isdigit() else 100
    except:
        target_count = 100
    
    print(f"\n CAPTURANDO {target_count} CARTAS...")
    os.system(f'python smart_capture_fixed.py')

def verify_results():
    """Verificar resultados"""
    print_step(5, "VERIFICAR RESULTADOS", 
        """ VERIFICAREMOS EL DATASET:
           
           El script analizará:
            Total de cartas capturadas
            Porcentaje de cartas rojas
            Distribución por palo
           
            RESULTADO ESPERADO:
            Mínimo 30% cartas rojas
            Distribución balanceada
           
            SI FALLA:
            Volver al PASO 1
            Cambiar de mesa PokerStars""")
    
    print("\n ANALIZANDO RESULTADOS...")
    os.system("python verify_balance.py")

def final_instructions():
    """Instrucciones finales"""
    print_step(6, "SISTEMA LISTO", 
        """ FELICIDADES!
           
           Si llegaste hasta aquí:
            PokerStars configurado correctamente
            Dataset balanceado capturado
            Sistema listo para usar
           
            AHORA PUEDES:
           1. Ejecutar sistema completo: python main_integrated.py
           2. Gestionar sesiones: python session_manager.py
           3. Probar análisis: python start_auto_simple.py
           
            RECOMENDACIÓN:
           Usa primero: python main_integrated.py
           Selecciona 'Modo interactivo'""")

def main():
    """Función principal"""
    print(" POKER COACH PRO - ASISTENTE DE CONFIGURACIÓN")
    print("=" * 70)
    print("Este asistente te guiará paso a paso para configurar")
    print("correctamente PokerStars y capturar un dataset balanceado.")
    print("=" * 70)
    
    try:
        # Ejecutar pasos
        check_pokerstars_open()
        guide_table_selection()
        guide_visual_verification()
        run_detection()
        run_balanced_capture()
        verify_results()
        final_instructions()
        
        print("\n" + "=" * 70)
        print(" CONFIGURACIÓN COMPLETADA CON ÉXITO!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n Error: {e}")
        print(" Intenta ejecutar los pasos manualmente:")

if __name__ == "__main__":
    main()
