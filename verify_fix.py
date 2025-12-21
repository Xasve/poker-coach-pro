# verify_fix.py - Verificar que la reparación funcionó
import os
import sys

def check_structure():
    """Verificar estructura del proyecto"""
    print(" VERIFICANDO ESTRUCTURA...")
    
    required_items = [
        ("src/core/main_system.py", "Módulo principal"),
        ("poker_coach_pro.py", "Sistema principal"),
        ("config/system_config.yaml", "Configuración"),
        ("requirements.txt", "Dependencias")
    ]
    
    all_ok = True
    for path, description in required_items:
        if os.path.exists(path):
            print(f"    {description}")
        else:
            print(f"    {description}")
            all_ok = False
    
    return all_ok

def test_import():
    """Probar importación del módulo principal"""
    print("\n PROBANDO IMPORTACIÓN...")
    
    try:
        # Añadir src al path
        sys.path.insert(0, "src")
        
        # Intentar importar
        from core.main_system import PokerCoachProV2
        
        print("    Importación exitosa")
        
        # Probar instanciación
        system = PokerCoachProV2()
        print("    Instanciación exitosa")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🎴 VERIFICACIÓN DE REPARACIÓN - POKER COACH PRO")
    print("=" * 60)
    
    structure_ok = check_structure()
    import_ok = test_import()
    
    print("\n" + "=" * 60)
    print(" RESULTADOS:")
    
    if structure_ok and import_ok:
        print(" REPARACIÓN EXITOSA!")
        print("\n Ahora puedes ejecutar:")
        print("   python poker_coach_pro.py")
    else:
        print(" Reparación incompleta")
        
        if not structure_ok:
            print("    Faltan archivos en la estructura")
        
        if not import_ok:
            print("    Error en la importación del módulo")
        
        print("\n Soluciones:")
        print("   1. Verifica que todos los archivos se crearon")
        print("   2. Ejecuta el script de reparación nuevamente")
        print("   3. Revisa los permisos de escritura")

if __name__ == "__main__":
    main()
