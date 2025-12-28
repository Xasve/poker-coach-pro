# create_session_info.py - Crear/verificar session_info.json
import os
import json
from datetime import datetime

def create_session_info(session_id):
    """Crear archivo session_info.json para una sesión"""
    session_path = f"data/card_templates/auto_captured/{session_id}"
    
    if not os.path.exists(session_path):
        print(f" Sesión no existe: {session_path}")
        return False
    
    # Verificar si ya existe
    info_path = os.path.join(session_path, "session_info.json")
    if os.path.exists(info_path):
        print(f" session_info.json ya existe: {info_path}")
        return True
    
    # Crear información de sesión
    session_info = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "session_type": "auto_capture",
        "version": "2.0",
        "folders": ["raw_captures", "reports"],
        "notes": "Sesión creada automáticamente por Poker Coach Pro"
    }
    
    # Guardar archivo
    with open(info_path, 'w') as f:
        json.dump(session_info, f, indent=2)
    
    print(f" session_info.json creado: {info_path}")
    return True

def fix_all_sessions():
    """Crear session_info.json para todas las sesiones que no lo tengan"""
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(f" Carpeta no existe: {base_path}")
        return
    
    sessions = [d for d in os.listdir(base_path) 
               if os.path.isdir(os.path.join(base_path, d))]
    
    if not sessions:
        print(" No hay sesiones")
        return
    
    print(f" Reparando {len(sessions)} sesiones...")
    
    fixed = 0
    for session_id in sessions:
        session_path = os.path.join(base_path, session_id)
        info_path = os.path.join(session_path, "session_info.json")
        
        if not os.path.exists(info_path):
            if create_session_info(session_id):
                fixed += 1
    
    print(f"\n {fixed}/{len(sessions)} sesiones reparadas")

def main():
    """Función principal"""
    print(" HERRAMIENTA DE REPARACIÓN DE SESIONES")
    print("=" * 60)
    
    print("Esta herramienta crea archivos session_info.json")
    print("para que el clasificador pueda encontrar las sesiones.")
    
    print("\n OPCIONES:")
    print("   1. Reparar todas las sesiones")
    print("   2. Reparar sesión específica")
    print("   3. Ver sesiones existentes")
    
    try:
        choice = input("\n Selecciona opción (1-3): ")
        
        if choice == '1':
            fix_all_sessions()
        elif choice == '2':
            session_id = input("ID de sesión (ej: 20251219_095143): ")
            create_session_info(session_id.strip())
        elif choice == '3':
            base_path = "data/card_templates/auto_captured"
            if os.path.exists(base_path):
                sessions = sorted([d for d in os.listdir(base_path) 
                                 if os.path.isdir(os.path.join(base_path, d))], 
                                 reverse=True)
                print(f"\n Sesiones disponibles ({len(sessions)}):")
                for s in sessions[:10]:
                    print(f"    {s}")
                if len(sessions) > 10:
                    print(f"   ... y {len(sessions) - 10} más")
            else:
                print(" No hay sesiones")
        else:
            print(" Opción no válida")
    
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
