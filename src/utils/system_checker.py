# check_system.py - Verificación completa del sistema
import os
import sys
import json
import platform

def print_header(text):
    """Imprimir encabezado"""
    print("\n" + "=" * 70)
    print(f"🔍 {text}")
    print("=" * 70)

def check_python():
    """Verificar Python"""
    print_header("VERIFICANDO PYTHON")
    
    version = sys.version_info
    print(f"   Versión: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 11:
        print("   ✅ Versión compatible (3.11+)")
        return True
    else:
        print("   ⚠️  Se recomienda Python 3.11 o superior")
        return False

def check_dependencies():
    """Verificar dependencias"""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    deps = [
        ("cv2", "OpenCV", True),
        ("numpy", "NumPy", True),
        ("mss", "MSS", True),
        ("PIL", "Pillow", True),
        ("sklearn", "scikit-learn", False),
        ("matplotlib", "Matplotlib", False),
        ("pandas", "Pandas", False)
    ]
    
    results = []
    for module_name, display_name, required in deps:
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "OK")
            
            if required:
                print(f"   ✅ {display_name:15} {version}")
                results.append(True)
            else:
                print(f"   📦 {display_name:15} {version} (opcional)")
                results.append(True)
        except ImportError:
            if required:
                print(f"   ❌ {display_name:15} FALTANTE")
                results.append(False)
            else:
                print(f"   ⚠️  {display_name:15} No instalado (opcional)")
                results.append(True)
    
    return all(results)

def check_structure():
    """Verificar estructura de directorios"""
    print_header("VERIFICANDO ESTRUCTURA")
    
    required = [
        ("src/", True),
        ("src/card_detector.py", True),
        ("src/auto_template_capturer.py", True),
        ("data/card_templates/", True),
        ("config/", True),
        ("logs/", False),
        ("debug/", False)
    ]
    
    all_ok = True
    for path, required_flag in required:
        exists = os.path.exists(path)
        
        if required_flag:
            status = "✅" if exists else "❌"
            if not exists:
                all_ok = False
        else:
            status = "📁" if exists else "⚠️ "
        
        print(f"   {status} {path}")
    
    return all_ok

def check_configuration():
    """Verificar configuración"""
    print_header("VERIFICANDO CONFIGURACIÓN")
    
    config_file = "config/pokerstars_coords.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print("✅ Configuración encontrada:")
            print(f"   Resolución: {config.get('screen_resolution', 'Desconocida')}")
            
            regions = config.get("pokerstars_regions", {})
            print(f"   Regiones: {len(regions)} configuradas")
            
            # Verificar regiones esenciales
            essential = ["mesa", "cartas_hero", "cartas_comunitarias"]
            missing = [r for r in essential if r not in regions]
            
            if missing:
                print(f"   ⚠️  Faltan regiones: {missing}")
                return False
            else:
                print("   ✅ Todas las regiones esenciales configuradas")
                return True
                
        except Exception as e:
            print(f"❌ Error leyendo configuración: {e}")
            return False
    else:
        print("❌ No hay configuración")
        print("\n💡 Para configurar:")
        print("   1. Abre PokerStars en una mesa")
        print("   2. Ejecuta: python detect_coords.py")
        return False

def check_templates():
    """Verificar templates existentes"""
    print_header("VERIFICANDO TEMPLATES")
    
    base_path = "data/card_templates/pokerstars_real"
    
    if not os.path.exists(base_path):
        print("📭 No hay carpeta de templates")
        return 0
    
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    total = 0
    
    print("🎴 Templates por palo:")
    for suit in suits:
        suit_path = os.path.join(base_path, suit)
        if os.path.exists(suit_path):
            count = len([f for f in os.listdir(suit_path) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))])
            print(f"   {suit.upper():10} {count:3}")
            total += count
        else:
            print(f"   {suit.upper():10} 0  (carpeta faltante)")
    
    print(f"\n   TOTAL:      {total:3}")
    
    # Evaluación
    if total == 0:
        print("\n📭 No hay templates")
        print("💡 Ejecuta el sistema de captura para comenzar")
    elif total < 20:
        print("\n⚠️  Pocos templates")
        print("💡 Se recomienda capturar más cartas")
    elif total < 100:
        print("\n📊 Templates suficientes")
        print("💡 Podría mejorar con más variedad")
    else:
        print("\n✅ Excelente base de datos")
        print("🎯 El sistema debería funcionar bien")
    
    return total

def check_sessions():
    """Verificar sesiones de captura"""
    print_header("VERIFICANDO SESIONES")
    
    capture_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(capture_path):
        print("�� No hay sesiones de captura")
        return 0
    
    sessions = []
    for item in os.listdir(capture_path):
        session_path = os.path.join(capture_path, item)
        if os.path.isdir(session_path):
            # Contar cartas
            raw_path = os.path.join(session_path, "raw_captures")
            card_count = 0
            if os.path.exists(raw_path):
                card_count = len([f for f in os.listdir(raw_path) 
                                if f.endswith('.png')])
            
            sessions.append({
                "id": item,
                "cards": card_count
            })
    
    if not sessions:
        print("📭 No hay sesiones")
        return 0
    
    print(f"📁 Sesiones encontradas: {len(sessions)}")
    
    # Mostrar últimas 5 sesiones
    print("\n📋 Últimas sesiones:")
    for session in sessions[-5:]:
        print(f"   {session['id']} - {session['cards']} cartas")
    
    total_cards = sum(s["cards"] for s in sessions)
    print(f"\n�� Total cartas capturadas: {total_cards}")
    
    return len(sessions)

def system_summary():
    """Resumen del sistema"""
    print_header("RESUMEN DEL SISTEMA")
    
    # Información del sistema
    print("💻 INFORMACIÓN:")
    print(f"   Sistema: {platform.system()} {platform.release()}")
    print(f"   Procesador: {platform.processor()}")
    print(f"   Arquitectura: {platform.architecture()[0]}")
    
    # Estado de componentes
    print("\n🎯 COMPONENTES:")
    
    # Verificar imports básicos
    components = [
        ("OpenCV", "cv2"),
        ("NumPy", "numpy"),
        ("MSS", "mss"),
        ("scikit-learn", "sklearn"),
        ("Matplotlib", "matplotlib")
    ]
    
    for name, module in components:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except:
            print(f"   ❌ {name}")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    
    # Verificar si está configurado
    if not os.path.exists("config/pokerstars_coords.json"):
        print("   1. ⚙️  Configurar PokerStars (ejecuta detect_coords.py)")
    
    # Verificar templates
    templates_path = "data/card_templates/pokerstars_real"
    if os.path.exists(templates_path):
        total = sum(len([f for f in os.listdir(os.path.join(templates_path, d)) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]) 
                   for d in os.listdir(templates_path) 
                   if os.path.isdir(os.path.join(templates_path, d)))
        
        if total < 20:
            print(f"   2. 📸 Capturar más cartas (tienes {total})")
    else:
        print("   2. 📸 Comenzar a capturar cartas")
    
    print("   3. 🎯 Usar start_auto_capture.py para el sistema completo")

def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🎴 POKER COACH PRO - VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("=" * 70)
    
    # Ejecutar todas las verificaciones
    checks = [
        ("Python", check_python),
        ("Dependencias", check_dependencies),
        ("Estructura", check_structure),
        ("Configuración", check_configuration),
        ("Templates", check_templates),
        ("Sesiones", check_sessions)
    ]
    
    results = []
    for name, func in checks:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    system_summary()
    
    # Conclusión
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)
    
    passed = sum(1 for name, result in results if result is not False)
    total = len(results)
    
    for name, result in results:
        if result is False:
            print(f"   ❌ {name}")
        elif result is True:
            print(f"   ✅ {name}")
        else:
            print(f"   📊 {name}: {result}")
    
    print(f"\n🎯 {passed}/{total} verificaciones exitosas")
    
    if passed == total:
        print("\n✨ ¡Sistema listo para usar!")
        print("🚀 Ejecuta: python start_auto_capture.py")
    else:
        print("\n⚠️  Algunas verificaciones fallaron")
        print("💡 Revisa las recomendaciones anteriores")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificación interrumpida")
        sys.exit(1)
