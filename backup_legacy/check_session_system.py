# check_session_system.py - Diagnóstico completo del sistema de sesiones
import os
import sys

def print_header(text):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)

def check_files():
    """Verificar archivos necesarios"""
    print_header("VERIFICANDO ARCHIVOS")
    
    required_files = [
        ("src/session_manager.py", True),
        ("manage_sessions.py", True),
        ("start_auto_capture.py", True),
        ("data/card_templates/auto_captured/", False),
        ("data/card_templates/deleted_sessions/", False)
    ]
    
    all_ok = True
    for file_path, required in required_files:
        exists = os.path.exists(file_path)
        status = "" if exists else (" " if not required else "")
        
        if required and not exists:
            all_ok = False
        
        print(f"   {status} {file_path}")
    
    return all_ok

def check_imports():
    """Verificar que los imports funcionen"""
    print_header("VERIFICANDO IMPORTS")
    
    try:
        sys.path.insert(0, "src")
        from session_manager import SessionManager
        print(" session_manager.py: Import OK")
        
        # Probar creación de instancia
        manager = SessionManager()
        print(f" SessionManager: Inicializado ({len(manager.sessions)} sesiones)")
        
        # Probar métodos básicos
        if hasattr(manager, 'list_sessions'):
            print(" Método list_sessions: Disponible")
        if hasattr(manager, 'delete_session'):
            print(" Método delete_session: Disponible")
        if hasattr(manager, 'show_disk_usage'):
            print(" Método show_disk_usage: Disponible")
        
        return True
        
    except ImportError as e:
        print(f" Error de importación: {e}")
        return False
    except Exception as e:
        print(f" Error inicializando: {e}")
        return False

def check_sessions():
    """Verificar sesiones existentes"""
    print_header("VERIFICANDO SESIONES EXISTENTES")
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(" No hay carpeta de sesiones")
        return 0
    
    sessions = []
    for item in os.listdir(base_path):
        session_path = os.path.join(base_path, item)
        if os.path.isdir(session_path):
            # Contar imágenes
            raw_path = os.path.join(session_path, "raw_captures")
            image_count = 0
            if os.path.exists(raw_path):
                image_count = len([f for f in os.listdir(raw_path) 
                                 if f.endswith(('.png', '.jpg'))])
            
            sessions.append({
                "id": item,
                "images": image_count,
                "path": session_path
            })
    
    print(f" Sesiones encontradas: {len(sessions)}")
    
    if sessions:
        print("\n LISTA DE SESIONES:")
        for i, session in enumerate(sessions[:10], 1):
            print(f"{i:2}. {session['id']} - {session['images']} imágenes")
        
        if len(sessions) > 10:
            print(f"   ... y {len(sessions) - 10} más")
        
        total_images = sum(s["images"] for s in sessions)
        print(f"\n📊 TOTAL: {total_images} imágenes en {len(sessions)} sesiones")
    
    return len(sessions)

def show_usage_guide():
    """Mostrar guía de uso"""
    print_header("GUÍA DE USO - GESTIÓN DE SESIONES")
    
    print("\n COMANDOS DISPONIBLES:")
    print("   1. python manage_sessions.py          - Gestor independiente")
    print("   2. python start_auto_capture.py       - Menú completo (opción 5)")
    print("   3. python src/session_manager.py      - Usar directamente")
    
    print("\n FUNCIONES PRINCIPALES:")
    print("     Listar sesiones con detalles")
    print("      Eliminar sesiones específicas")
    print("      Eliminar sesiones vacías (< 5 imágenes)")
    print("     Ver espacio usado")
    print("     Limpieza automática")
    
    print("\n  PRECAUCIONES:")
    print("    Las eliminaciones requieren confirmación")
    print("    Las sesiones eliminadas van a backup")
    print("    Verifica antes de eliminar sesiones grandes")
    
    print("\n CONSEJOS:")
    print("    Mantén sesiones con > 10 imágenes")
    print("    Elimina sesiones con errores de captura")
    print("    Usa 'Ver uso de disco' para monitorear espacio")

def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🎴 DIAGNÓSTICO DEL SISTEMA DE GESTIÓN DE SESIONES")
    print("=" * 70)
    
    print("Este script verifica que todo esté funcionando correctamente")
    print("para la gestión de sesiones de captura.")
    
    # Ejecutar todas las verificaciones
    files_ok = check_files()
    imports_ok = check_imports()
    session_count = check_sessions()
    
    # Resumen
    print_header("RESUMEN DEL DIAGNÓSTICO")
    
    if files_ok and imports_ok:
        print(" Sistema de gestión de sesiones: FUNCIONAL")
        print(f" Sesiones disponibles: {session_count}")
        
        if session_count > 0:
            print("\n Puedes comenzar a gestionar tus sesiones:")
            print("   Ejecuta: python manage_sessions.py")
        else:
            print("\n No hay sesiones para gestionar")
            print("   Primero captura algunas cartas")
    else:
        print("  Sistema de gestión de sesiones: CON PROBLEMAS")
        
        if not files_ok:
            print("    Faltan archivos necesarios")
        if not imports_ok:
            print("    Hay problemas con los imports")
        
        print("\n Soluciones:")
        print("   1. Verifica que todos los archivos estén en su lugar")
        print("   2. Asegúrate de estar en el directorio correcto")
        print("   3. Ejecuta este diagnóstico nuevamente")
    
    show_usage_guide()
    
    print("\n" + "=" * 70)
    print("✅ Diagnóstico completado")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
