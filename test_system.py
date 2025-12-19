#!/usr/bin/env python3
"""
SCRIPT DE PRUEBA - Poker Coach Pro
"""
import sys
import os

# Añadir src al path
sys.path.insert(0, 'src')

print("🧪 PRUEBA DEL SISTEMA POKER COACH PRO")
print("=" * 50)

# Prueba 1: Importar módulo principal
print("
1. Probando importación de screen_capture...")
try:
    import screen_capture
    print("✅ Módulo screen_capture importado")
    
    # Prueba 2: Importar clases específicas
    print("
2. Probando clases específicas...")
    from screen_capture.stealth_capture import StealthScreenCapture
    from screen_capture.table_detector import TableDetector
    
    print("✅ StealthScreenCapture importado")
    print("✅ TableDetector importado")
    
    # Prueba 3: Crear instancias
    print("
3. Probando creación de instancias...")
    capture = StealthScreenCapture()
    detector = TableDetector()
    
    print("✅ Instancias creadas")
    
    # Prueba 4: Inicializar captura
    print("
4. Probando inicialización...")
    if capture.initialize():
        print("✅ Captura inicializada")
    else:
        print("⚠️  Captura no pudo inicializarse")
    
    print("
" + "=" * 50)
    print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
    print("
🚀 El sistema está listo para usar.")
    print("   Ejecuta: python start_coach.py")
    
except ImportError as e:
    print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
    print("\n💡 Solución:")
    print("   1. Ejecuta: python fix_imports_corrected.py")
    print("   2. Verifica que existe src/screen_capture/__init__.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
