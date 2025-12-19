# manage_sessions.py - Gestión independiente de sesiones
import sys
import os

# Añadir src al path
sys.path.insert(0, "src")

def main():
    """Función principal"""
    print("  GESTOR INDEPENDIENTE DE SESIONES - POKER COACH PRO")
    print("=" * 70)
    
    try:
        from session_manager import SessionManager
        manager = SessionManager()
        manager.main()
    except ImportError as e:
        print(f" Error importando gestor de sesiones: {e}")
        print("\n Soluciones:")
        print("   1. Asegúrate que session_manager.py esté en src/")
        print("   2. Ejecuta desde el directorio correcto")
        print("   3. Usa start_auto_capture.py (opción 5)")
        
        # Gestión básica como fallback
        print("\n GESTIÓN BÁSICA:")
        base_path = "data/card_templates/auto_captured"
        
        if not os.path.exists(base_path):
            print(" No hay sesiones de captura")
            return
        
        sessions = []
        for item in sorted(os.listdir(base_path), reverse=True):
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
                    "image_count": image_count
                })
        
        if not sessions:
            print(" No hay sesiones")
            return
        
        print(f"\n SESIONES ({len(sessions)}):")
        for i, session in enumerate(sessions[:20], 1):
            print(f"{i:2}. {session['id']} - {session['image_count']} imágenes")
        
        print("\n Para eliminar sesiones, usa:")
        print("   start_auto_capture.py (opción 5)")
        print("   O elimina manualmente las carpetas en:")
        print(f"   {base_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Gestión de sesiones interrumpida")
