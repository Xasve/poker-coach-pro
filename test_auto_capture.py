# test_auto_capture.py
print(" PRUEBA DEL SISTEMA DE CAPTURA AUTOMÁTICA")
print("=" * 60)

def test_imports():
    """Probar imports de todos los módulos"""
    modules = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("mss", "MSS"),
        ("sklearn", "scikit-learn"),
        ("pandas", "Pandas")
    ]
    
    print("\n PROBANDO IMPORTS:")
    all_ok = True
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"    {display_name}")
        except ImportError:
            print(f"   ❌ {display_name}")
            all_ok = False
    
    return all_ok

def test_file_structure():
    """Probar estructura de archivos"""
    required_files = [
        ("src/card_detector.py", True),
        ("src/auto_template_capturer.py", True),
        ("src/card_classifier.py", True),
        ("src/auto_capture_system.py", True),
        ("config/pokerstars_coords.json", False),
        ("data/card_templates/auto_captured/", False)
    ]
    
    print("\n PROBANDO ESTRUCTURA:")
    all_ok = True
    
    for file_path, required in required_files:
        exists = os.path.exists(file_path)
        status = "" if exists else (" " if not required else "")
        print(f"   {status} {file_path}")
        
        if required and not exists:
            all_ok = False
    
    return all_ok

def test_configuration():
    """Probar configuración"""
    print("\n  PROBANDO CONFIGURACIÓN:")
    
    config_file = "config/pokerstars_coords.json"
    if os.path.exists(config_file):
        try:
            import json
            with open(config_file) as f:
                config = json.load(f)
            
            regions = config.get("pokerstars_regions", {})
            print(f"    Configuración cargada ({len(regions)} regiones)")
            
            # Verificar regiones esenciales
            essential_regions = ["mesa", "cartas_hero", "cartas_comunitarias"]
            for region in essential_regions:
                if region in regions:
                    print(f"   ✅ Región '{region}' configurada")
                else:
                    print(f"   ⚠️  Región '{region}' faltante")
            
            return True
        except Exception as e:
            print(f"    Error cargando configuración: {e}")
            return False
    else:
        print("     No hay configuración (ejecuta detect_coords.py)")
        return False

def quick_detection_test():
    """Prueba rápida de detección"""
    print("\n🎯 PRUEBA RÁPIDA DE DETECCIÓN:")
    
    try:
        from src.card_detector import CardDetector
        detector = CardDetector()
        print("    CardDetector inicializado")
        
        # Verificar templates cargados
        if detector.templates:
            print(f"    {len(detector.templates)} templates cargados")
        else:
            print("   ⚠️  No hay templates cargados")
        
        return True
    except Exception as e:
        print(f"    Error: {e}")
        return False

def main():
    """Función principal de prueba"""
    import os
    import sys
    
    print("Iniciando pruebas del sistema...")
    
    # Ejecutar todas las pruebas
    tests = [
        ("Imports", test_imports),
        ("Estructura", test_file_structure),
        ("Configuración", test_configuration),
        ("Detección", quick_detection_test)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f" {test_name}")
        print(f"{'='*40}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" Error ejecutando prueba: {e}")
            results.append((test_name, False))
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print(" RESUMEN DE PRUEBAS")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = " PASÓ" if result else " FALLÓ"
        print(f"   {status} {test_name}")
    
    print(f"\n Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n Sistema listo para usar!")
        print("\n Ejecuta: python start_auto_capture.py")
    else:
        print("\n  Algunas pruebas fallaron")
        print(" Ejecuta: .\install_auto_capture.ps1")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
