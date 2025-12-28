# auto_fix_indentation.py - Corrección automática de indentación
import re
import os

def fix_indentation_in_file(filename):
    """Corregir indentación en un archivo"""
    print(f" CORRIGIENDO: {filename}")
    
    if not os.path.exists(filename):
        print(f" Archivo no existe")
        return False
    
    # Crear backup
    backup_name = filename + '.backup'
    import shutil
    shutil.copy2(filename, backup_name)
    print(f" Backup creado: {backup_name}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar tabs por 4 espacios
        content = content.replace('\t', '    ')
        
        # Corregir indentación después de :
        lines = content.split('\n')
        fixed_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.lstrip(' ')
            current_indent = len(line) - len(stripped)
            
            # Ajustar a múltiplo de 4
            if stripped:  # No línea vacía
                adjusted_indent = (current_indent // 4) * 4
                fixed_line = ' ' * adjusted_indent + stripped
            else:
                fixed_line = line
            
            fixed_lines.append(fixed_line)
            
            # Actualizar nivel de indentación para próxima línea
            if stripped and stripped[-1] == ':':
                indent_level += 1
            elif stripped and indent_level > 0 and current_indent < adjusted_indent:
                # Disminuir nivel si hay dedentación
                indent_level -= 1
        
        fixed_content = '\n'.join(fixed_lines)
        
        # Guardar archivo corregido
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(" Archivo corregido")
        return True
        
    except Exception as e:
        print(f" Error corrigiendo archivo: {e}")
        return False

def main():
    """Función principal"""
    print(" CORRECTOR AUTOMÁTICO DE INDENTACIÓN")
    print("=" * 70)
    
    print("Este script corrige automáticamente problemas de indentación")
    print("en los archivos de Python del proyecto.")
    
    files_to_fix = [
        "start_auto_capture.py",
        "manage_sessions.py",
        "src/session_manager.py",
        "src/auto_capture_system.py",
        "src/card_detector.py",
        "src/auto_template_capturer.py",
        "src/card_classifier.py"
    ]
    
    print(f"\n ARCHIVOS A CORREGIR ({len(files_to_fix)}):")
    for file in files_to_fix:
        if os.path.exists(file):
            print(f"    {file}")
        else:
            print(f"    {file} (no existe)")
    
    confirm = input("\nContinuar con la corrección? (s/n): ")
    
    if confirm.lower() != 's':
        print("\n Corrección cancelada")
        return
    
    print("\n" + "=" * 70)
    print(" INICIANDO CORRECCIÓN...")
    print("=" * 70)
    
    success_count = 0
    for file in files_to_fix:
        if os.path.exists(file):
            if fix_indentation_in_file(file):
                success_count += 1
    
    print("\n" + "=" * 70)
    print(" RESULTADO DE LA CORRECCIÓN:")
    print(f"    Archivos corregidos: {success_count}/{len(files_to_fix)}")
    
    if success_count > 0:
        print("\n Corrección completada!")
        print("\n PARA PROBAR:")
        print("   python start_auto_capture.py")
        print("\n Los backups están guardados como .backup")
    else:
        print("\n No se pudieron corregir archivos")
        print(" Usa el archivo start_auto_capture_fixed.py")

if __name__ == "__main__":
    main()
