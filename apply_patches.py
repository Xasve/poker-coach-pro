"""
Patch para arreglar stealth_capture.py
"""
import os

def fix_stealth_capture():
    """Corregir errores en stealth_capture.py"""
    file_path = "src/screen_capture/stealth_capture.py"
    
    if not os.path.exists(file_path):
        print(f" Archivo no encontrado: {file_path}")
        return False
    
    print(" Aplicando patch a stealth_capture.py...")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Reemplazar líneas problemáticas
    fixes = [
        # Fix para error de uint8
        ("np.array(sct_img)[:, :, :3]", "np.array(sct_img, dtype=np.uint8)[:, :, :3]"),
        # Asegurar que la imagen sea uint8
        ("image = np.array(sct_img)", "image = np.array(sct_img, dtype=np.uint8)"),
    ]
    
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f" Reemplazado: {old[:50]}...")
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(" Patch aplicado")
    return True

def fix_table_detector():
    """Añadir método detect_table si falta"""
    file_path = "src/screen_capture/table_detector.py"
    
    if not os.path.exists(file_path):
        print(f" Archivo no encontrado: {file_path}")
        return False
    
    print(" Verificando table_detector.py...")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Verificar si tiene método detect_table
    if "def detect_table" not in content:
        print("  Añadiendo método detect_table...")
        
        # Buscar donde insertar (después de __init__)
        if "def __init__" in content:
            # Añadir método simple
            method = '''
    def detect_table(self, screenshot):
        """Detectar mesa en screenshot (placeholder)"""
        # Por ahora, devolver información básica
        # En producción, implementar detección real con OpenCV
        import random
        
        # Simular detección
        return {
            "found": random.random() > 0.5,
            "position": (100, 100, 800, 600),
            "confidence": 0.8
        }
'''
            
            # Insertar después de __init__
            lines = content.split('\n')
            new_lines = []
            method_added = False
            
            for line in lines:
                new_lines.append(line)
                if "def __init__" in line and not method_added:
                    # Encontrar fin del método __init__
                    indent = len(line) - len(line.lstrip())
                    new_lines.append('\n' + ' ' * indent + method.strip())
                    method_added = True
            
            content = '\n'.join(new_lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(" Método detect_table añadido")
        else:
            print(" No se pudo encontrar __init__ para insertar método")
            return False
    else:
        print(" detect_table ya existe")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print(" APLICANDO PATCHES DE EMERGENCIA")
    print("=" * 60)
    
    success = True
    success = fix_stealth_capture() and success
    success = fix_table_detector() and success
    
    if success:
        print("\n Todos los patches aplicados correctamente")
        print("\n Ahora ejecuta: python pokerstars_coach.py")
    else:
        print("\n Algunos patches fallaron")
    
    print("=" * 60)
