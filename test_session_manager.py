# test_session_manager.py - Prueba del gestor de sesiones
import sys
import os

sys.path.insert(0, "src")

print(" PRUEBA DEL GESTOR DE SESIONES")
print("=" * 60)

try:
    from session_manager import SessionManager
    
    print(" Importando SessionManager...")
    manager = SessionManager()
    
    print(f" Gestor inicializado")
    print(f"   Sesiones encontradas: {len(manager.sessions)}")
    
    if manager.sessions:
        print("\n MUESTRA DE SESIONES:")
        for i, session in enumerate(manager.sessions[:3], 1):
            print(f"{i}. {session['id']} - {session['image_count']} imágenes")
        
        # Probar funciones básicas
        print("\n PROBANDO FUNCIONES:")
        
        # 1. Listar sesiones
        print("1. 📋 Listar sesiones...")
        displayed = manager.list_sessions(show_all=False, max_display=5)
        print(f"    Mostradas: {len(displayed)} sesiones")
        
        # 2. Mostrar uso de disco
        print("2.  Mostrar uso de disco...")
        manager.show_disk_usage()
        
        print("\n🎉 ¡Todas las pruebas pasaron!")
        
    else:
        print("\n📭 No hay sesiones para probar")
        print(" Ejecuta primero el capturador automático")
        
except ImportError as e:
    print(f" Error importando: {e}")
    print("\n Verifica que session_manager.py exista en src/")
    
    # Mostrar contenido de src/
    print("\n CONTENIDO DE src/:")
    try:
        files = os.listdir("src")
        for f in files:
            print(f"    {f}")
    except:
        print("    No se pudo acceder a src/")
        
except Exception as e:
    print(f" Error durante la prueba: {e}")

print("\n" + "=" * 60)
print("✅ Prueba completada")
