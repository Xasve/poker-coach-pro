# test_capture.py - Prueba rápida de captura
import os
import sys

print("🧪 PRUEBA RÁPIDA DE CAPTURA")
print("=" * 60)

def test_all_options():
    """Probar todas las opciones de captura"""
    print("\n🎯 OPCIONES DISPONIBLES:")
    print("1. Captura mejorada V2 (recomendada)")
    print("2. Captura simplificada (más confiable)")
    print("3. Verificar archivos existentes")
    print("4. Salir")
    
    choice = input("\n Selecciona opción (1-4): ").strip()
    
    if choice == "1":
        print("\n Ejecutando captura mejorada V2...")
        if os.path.exists("smart_capture_fixed_v2.py"):
            os.system("python smart_capture_fixed_v2.py")
        else:
            print("❌ Archivo no encontrado: smart_capture_fixed_v2.py")
            
    elif choice == "2":
        print("\n⚡ Ejecutando captura simplificada...")
        if os.path.exists("quick_capture.py"):
            os.system("python quick_capture.py")
        else:
            print("❌ Archivo no encontrado: quick_capture.py")
            
    elif choice == "3":
        print("\n🔍 Verificando archivos...")
        files = [
            "smart_capture_fixed_v2.py",
            "quick_capture.py",
            "smart_capture_fixed.py",
            "forced_capture.py"
        ]
        
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"✅ {file} - {size:,} bytes")
            else:
                print(f"❌ {file} - NO EXISTE")
                
    elif choice == "4":
        print("\n👋 ¡Hasta luego!")
        
    else:
        print(" Opción no válida")

def main():
    """Función principal"""
    print(" PRUEBA DE CAPTURA - ELIGE EL MÉTODO")
    print("\n Problema conocido: La detección de color falla")
    print(" Soluciones disponibles:")
    print("    V2: Detección mejorada")
    print("    Simplificada: Sin detección (más confiable)")
    
    test_all_options()

if __name__ == "__main__":
    main()
