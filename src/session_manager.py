# session_manager.py - Gestión completa de sesiones
import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class SessionManager:
    """Gestor completo de sesiones de captura"""
    
    def __init__(self, base_path="data/card_templates/auto_captured"):
        self.base_path = base_path
        self.sessions = self.load_sessions()
    
    def load_sessions(self):
        """Cargar todas las sesiones"""
        sessions = []
        
        if not os.path.exists(self.base_path):
            return sessions
        
        for item in sorted(os.listdir(self.base_path), reverse=True):
            session_path = os.path.join(self.base_path, item)
            if os.path.isdir(session_path):
                # Contar imágenes
                raw_path = os.path.join(session_path, "raw_captures")
                image_count = 0
                if os.path.exists(raw_path):
                    image_count = len([f for f in os.listdir(raw_path) 
                                     if f.endswith(('.png', '.jpg', '.jpeg'))])
                
                # Obtener información de sesión
                session_info = self.get_session_info(session_path)
                
                sessions.append({
                    "id": item,
                    "path": session_path,
                    "image_count": image_count,
                    "size_mb": self.get_folder_size(session_path),
                    "created": item[:15],  # Fecha del ID
                    "info": session_info,
                    "has_raw_captures": os.path.exists(raw_path),
                    "has_classification": os.path.exists(os.path.join(session_path, "classification_results.json"))
                })
        
        return sessions
    
    def get_session_info(self, session_path):
        """Obtener información de sesión desde session_info.json"""
        info_path = os.path.join(session_path, "session_info.json")
        if os.path.exists(info_path):
            try:
                with open(info_path, 'r') as f:
                    return json.load(f)
            except:
                return {"session_id": os.path.basename(session_path)}
        return {"session_id": os.path.basename(session_path)}
    
    def get_folder_size(self, folder_path):
        """Obtener tamaño de carpeta en MB"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        return round(total_size / (1024 * 1024), 2)  # MB
    
    def list_sessions(self, show_all=True, max_display=20):
        """Listar sesiones con información detallada"""
        if not self.sessions:
            print(" No hay sesiones de captura")
            return []
        
        sessions_to_show = self.sessions if show_all else self.sessions[:max_display]
        
        print(f"\n SESIONES DISPONIBLES ({len(self.sessions)} total):")
        print("=" * 80)
        print(f"{'#':3} {'ID':20} {'IMÁGENES':8} {'TAMAÑO':8} {'CLASIF':7} {'CREADA':16}")
        print("-" * 80)
        
        for i, session in enumerate(sessions_to_show, 1):
            classified = "" if session["has_classification"] else ""
            print(f"{i:3} {session['id']:20} {session['image_count']:8} {session['size_mb']:6} MB {classified:7} {session['created']:16}")
        
        if not show_all and len(self.sessions) > max_display:
            print(f"   ... y {len(self.sessions) - max_display} sesiones más")
        
        print("-" * 80)
        
        # Resumen
        total_images = sum(s["image_count"] for s in self.sessions)
        total_size = sum(s["size_mb"] for s in self.sessions)
        classified_count = sum(1 for s in self.sessions if s["has_classification"])
        
        print(f" RESUMEN: {total_images} imágenes | {total_size:.1f} MB | {classified_count} clasificadas")
        
        return sessions_to_show
    
    def delete_session(self, session_id, backup=True):
        """Eliminar una sesión específica"""
        session_path = os.path.join(self.base_path, session_id)
        
        if not os.path.exists(session_path):
            print(f" Sesión no encontrada: {session_id}")
            return False
        
        # Confirmación
        session_info = self.get_session_info(session_path)
        image_count = len([f for f in os.listdir(os.path.join(session_path, "raw_captures")) 
                         if f.endswith(('.png', '.jpg'))]) if os.path.exists(os.path.join(session_path, "raw_captures")) else 0
        
        print(f"\n  ELIMINAR SESIÓN:")
        print(f"   ID: {session_id}")
        print(f"   Imágenes: {image_count}")
        print(f"   Ruta: {session_path}")
        
        confirm = input("\n Estás SEGURO de eliminar esta sesión? (escribe 'ELIMINAR' para confirmar): ")
        
        if confirm != "ELIMINAR":
            print(" Eliminación cancelada")
            return False
        
        # Crear backup si se solicita
        if backup:
            backup_path = f"data/card_templates/deleted_sessions/{session_id}"
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            try:
                shutil.move(session_path, backup_path)
                print(f" Sesión movida a backup: {backup_path}")
            except Exception as e:
                print(f"  Error moviendo a backup: {e}")
                # Intentar eliminar directamente
                try:
                    shutil.rmtree(session_path)
                    print(f" Sesión eliminada: {session_id}")
                except Exception as e2:
                    print(f" Error eliminando sesión: {e2}")
                    return False
        else:
            # Eliminar directamente
            try:
                shutil.rmtree(session_path)
                print(f" Sesión eliminada: {session_id}")
            except Exception as e:
                print(f" Error eliminando sesión: {e}")
                return False
        
        # Actualizar lista de sesiones
        self.sessions = self.load_sessions()
        return True
    
    def delete_multiple_sessions(self, session_ids, backup=True):
        """Eliminar múltiples sesiones"""
        if not session_ids:
            print(" No se especificaron sesiones para eliminar")
            return False
        
        print(f"\n  ELIMINAR {len(session_ids)} SESIONES:")
        for session_id in session_ids:
            print(f"    {session_id}")
        
        confirm = input("\n Estás SEGURO de eliminar estas sesiones? (escribe 'ELIMINAR' para confirmar): ")
        
        if confirm != "ELIMINAR":
            print(" Eliminación cancelada")
            return False
        
        success_count = 0
        for session_id in session_ids:
            if self.delete_session(session_id, backup):
                success_count += 1
        
        print(f"\n {success_count}/{len(session_ids)} sesiones eliminadas")
        return success_count > 0
    
    def delete_old_sessions(self, days_old=30, backup=True):
        """Eliminar sesiones antiguas"""
        old_sessions = []
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for session in self.sessions:
            session_path = session["path"]
            if os.path.exists(session_path):
                # Usar fecha de creación de la carpeta o del ID
                try:
                    # Intentar extraer fecha del ID (YYYYMMDD_HHMMSS)
                    session_date = datetime.strptime(session["id"][:15], "%Y%m%d_%H%M%S")
                    session_timestamp = session_date.timestamp()
                except:
                    # Usar fecha de modificación de la carpeta
                    session_timestamp = os.path.getmtime(session_path)
                
                if session_timestamp < cutoff_date:
                    old_sessions.append(session["id"])
        
        if not old_sessions:
            print(f" No hay sesiones más antiguas de {days_old} días")
            return False
        
        print(f"\n  SESIONES ANTIGUAS (> {days_old} días): {len(old_sessions)}")
        for session_id in old_sessions[:10]:
            print(f"    {session_id}")
        
        if len(old_sessions) > 10:
            print(f"   ... y {len(old_sessions) - 10} más")
        
        return self.delete_multiple_sessions(old_sessions, backup)
    
    def delete_empty_sessions(self, backup=True):
        """Eliminar sesiones vacías o con pocas imágenes"""
        empty_sessions = []
        
        for session in self.sessions:
            if session["image_count"] < 5:  # Sesiones con menos de 5 imágenes
                empty_sessions.append(session["id"])
        
        if not empty_sessions:
            print(" No hay sesiones vacías (< 5 imágenes)")
            return False
        
        print(f"\n  SESIONES VACÍAS (< 5 imágenes): {len(empty_sessions)}")
        for session_id in empty_sessions[:10]:
            print(f"    {session_id}")
        
        if len(empty_sessions) > 10:
            print(f"   ... y {len(empty_sessions) - 10} más")
        
        return self.delete_multiple_sessions(empty_sessions, backup)
    
    def cleanup_system(self):
        """Limpieza completa del sistema"""
        print("\n LIMPIEZA COMPLETA DEL SISTEMA")
        print("=" * 60)
        
        print("1.   Eliminar sesiones vacías (< 5 imágenes)")
        print("2.   Eliminar sesiones antiguas (> 30 días)")
        print("3.  Ver espacio liberado")
        print("4.  Volver")
        
        try:
            choice = input("\n Selecciona opción (1-4): ")
            
            if choice == '1':
                self.delete_empty_sessions()
            elif choice == '2':
                days = input("Días de antigüedad (default 30): ")
                days = int(days) if days.isdigit() else 30
                self.delete_old_sessions(days_old=days)
            elif choice == '3':
                self.show_disk_usage()
            elif choice == '4':
                return
            else:
                print(" Opción no válida")
        except Exception as e:
            print(f" Error: {e}")
    
    def show_disk_usage(self):
        """Mostrar uso de disco"""
        print("\n USO DE DISCO - SESIONES DE CAPTURA")
        print("=" * 60)
        
        if not self.sessions:
            print(" No hay sesiones")
            return
        
        total_size = sum(s["size_mb"] for s in self.sessions)
        total_images = sum(s["image_count"] for s in self.sessions)
        session_count = len(self.sessions)
        
        print(f" Sesiones totales: {session_count}")
        print(f" Imágenes totales: {total_images}")
        print(f" Espacio usado: {total_size:.1f} MB")
        
        # Por tamaño
        small_sessions = [s for s in self.sessions if s["size_mb"] < 10]
        medium_sessions = [s for s in self.sessions if 10 <= s["size_mb"] < 50]
        large_sessions = [s for s in self.sessions if s["size_mb"] >= 50]
        
        print(f"\n DISTRIBUCIÓN POR TAMAÑO:")
        print(f"   Pequeñas (<10 MB): {len(small_sessions)} sesiones")
        print(f"   Medianas (10-50 MB): {len(medium_sessions)} sesiones")
        print(f"   Grandes (>=50 MB): {len(large_sessions)} sesiones")
        
        # Por antigüedad
        print(f"\n RECOMENDACIONES:")
        if len(small_sessions) > 5:
            print(f"    Puedes eliminar {len(small_sessions)} sesiones pequeñas")
        if total_size > 500:  # Más de 500 MB
            print(f"    Considera limpiar sesiones antiguas ({total_size:.1f} MB)")
        
        # Espacio estimado a liberar
        empty_count = len([s for s in self.sessions if s["image_count"] < 5])
        if empty_count > 0:
            empty_size = sum(s["size_mb"] for s in self.sessions if s["image_count"] < 5)
            print(f"    {empty_count} sesiones vacías ocupan {empty_size:.1f} MB")

def main():
    """Función principal del gestor de sesiones"""
    print("  GESTOR DE SESIONES - POKER COACH PRO")
    print("=" * 70)
    
    manager = SessionManager()
    
    while True:
        print("\n MENÚ GESTIÓN DE SESIONES:")
        print("1.  Listar todas las sesiones")
        print("2.   Eliminar sesión específica")
        print("3.   Eliminar sesiones vacías (< 5 imágenes)")
        print("4.   Eliminar sesiones antiguas")
        print("5.  Ver uso de disco")
        print("6.  Limpieza completa")
        print("7.  Volver al menú principal")
        
        try:
            choice = input("\n Selecciona opción (1-7): ")
            
            if choice == '1':
                manager.list_sessions(show_all=True)
            elif choice == '2':
                sessions = manager.list_sessions(show_all=False, max_display=15)
                if sessions:
                    try:
                        num = int(input("\nNúmero de sesión a eliminar (0 para cancelar): "))
                        if 1 <= num <= len(sessions):
                            manager.delete_session(sessions[num-1]["id"])
                        elif num != 0:
                            print(" Número fuera de rango")
                    except ValueError:
                        print(" Entrada no válida")
            elif choice == '3':
                manager.delete_empty_sessions()
            elif choice == '4':
                days = input("Días de antigüedad (default 30): ")
                days = int(days) if days.isdigit() else 30
                manager.delete_old_sessions(days_old=days)
            elif choice == '5':
                manager.show_disk_usage()
            elif choice == '6':
                manager.cleanup_system()
            elif choice == '7':
                print("\n Volviendo al menú principal...")
                break
            else:
                print(" Opción no válida")
            
            if choice != '7':
                input("\n Presiona Enter para continuar...")
                
        except Exception as e:
            print(f" Error: {e}")

if __name__ == "__main__":
    main()
