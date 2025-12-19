# fix_all_menus.py - Reparar todos los menús del sistema
import os
import re

def fix_file_encoding(filepath):
    """Corregir encoding y caracteres problemáticos"""
    print(f"\n REPARANDO: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"    Archivo no existe")
        return False
    
    try:
        # Leer con diferentes encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"    Leído con encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            print(f"    No se pudo leer el archivo")
            return False
        
        # Reemplazar caracteres problemáticos
        replacements = [
            ('', '[ELIMINAR]'),
            ('', '[POKER]'),
            ('', '[OBJETIVO]'),
            ('', '[ESTADISTICAS]'),
            ('', '[CARPETA]'),
            ('', '[BUSCAR]'),
            ('', '[ADVERTENCIA]'),
            ('', '[OK]'),
            ('', '[ERROR]'),
            ('', '[MENU]'),
            ('', '[INICIAR]'),
            ('', '[LIMPIAR]'),
            ('', '[DISCO]'),
            ('', '[LISTA]'),
            ('', '[CAPTURA]'),
            ('', '[TIEMPO]'),
            ('', '[CAMARA]'),
            ('', '[HERRAMIENTA]'),
            ('', '[ADIOS]'),
            ('', '[SELECCION]'),
            ('', '[CONSEJO]'),
        ]
        
        original_content = content
        for old, new in replacements:
            content = content.replace(old, new)
        
        # También reemplazar otros caracteres Unicode problemáticos
        content = re.sub(r'[^\x00-\x7F]+', ' ', content)
        
        # Simplificar menús específicamente
        if 'start_auto_capture.py' in filepath:
            # Encontrar y simplificar show_menu
            pattern = r'def show_menu\(\):.*?return choice'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                menu_text = match.group(0)
                # Reemplazar líneas de opciones
                lines = menu_text.split('\n')
                new_lines = []
                option_num = 1
                for line in lines:
                    if 'print("' in line and any(str(i) in line for i in range(1, 10)):
                        # Es una línea de opción, simplificarla
                        new_line = f'    print("{option_num}. " + line.split(".", 1)[1].split(")", 1)[0].strip() + ")")'
                        new_lines.append(new_line)
                        option_num += 1
                    else:
                        new_lines.append(line)
                
                new_menu = '\n'.join(new_lines)
                content = content.replace(menu_text, new_menu)
        
        # Guardar de nuevo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    Archivo reparado y guardado")
        return True
        
    except Exception as e:
        print(f"    Error reparando archivo: {e}")
        return False

def create_backup(filepath):
    """Crear backup del archivo"""
    backup_path = filepath + '.backup'
    try:
        import shutil
        shutil.copy2(filepath, backup_path)
        print(f"    Backup creado: {backup_path}")
        return True
    except Exception as e:
        print(f"    Error creando backup: {e}")
        return False

def main():
    """Función principal"""
    print(" REPARADOR DE MENÚS - POKER COACH PRO")
    print("=" * 70)
    print("Este script repara problemas con caracteres especiales")
    print("y emojis que pueden causar errores en los menús.")
    
    files_to_fix = [
        "start_auto_capture.py",
        "manage_sessions.py", 
        "src/auto_capture_system.py",
        "src/session_manager.py"
    ]
    
    print(f"\n ARCHIVOS A REPARAR ({len(files_to_fix)}):")
    for file in files_to_fix:
        print(f"    {file}")
    
    confirm = input("\nContinuar con la reparación? (s/n): ")
    
    if confirm.lower() != 's':
        print("\n Reparación cancelada")
        return
    
    print("\n" + "=" * 70)
    print(" INICIANDO REPARACIÓN...")
    print("=" * 70)
    
    success_count = 0
    for file in files_to_fix:
        if os.path.exists(file):
            # Crear backup primero
            create_backup(file)
            # Reparar archivo
            if fix_file_encoding(file):
                success_count += 1
        else:
            print(f"\n  Archivo no encontrado: {file}")
    
    print("\n" + "=" * 70)
    print(" RESULTADO DE LA REPARACIÓN:")
    print(f"    Archivos reparados: {success_count}/{len(files_to_fix)}")
    
    if success_count == len(files_to_fix):
        print("\n Todos los archivos reparados exitosamente!")
        print("\n PARA PROBAR:")
        print("   python start_auto_capture.py")
        print("   (La opción 5 debería funcionar ahora)")
    else:
        print("\n  Algunos archivos no pudieron ser reparados")
        print(" Usa la versión simplificada:")
        print("   python start_auto_simple.py")
    
    print("\n CONSEJOS:")
    print("    Los backups están guardados como .backup")
    print("    Puedes restaurar: copia .backup sobre el original")
    print("    Reporta problemas si persisten")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Reparación interrumpida")
