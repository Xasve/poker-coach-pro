#!/usr/bin/env python3
"""
REPARADOR DE ERROR: 'PokerStarsAdapter' object has no attribute 'platform'
"""
import os
import sys

def main():
    print("=" * 60)
    print("🔧 REPARANDO ERROR: No attribute 'platform'")
    print("=" * 60)
    
    # 1. Reparar pokerstars_adapter.py
    adapter_file = "src/platforms/pokerstars_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"❌ Archivo no encontrado: {adapter_file}")
        return False
    
    print("📄 Leyendo archivo...")
    
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hacer backup
    backup_file = adapter_file + ".backup"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Backup creado: {backup_file}")
    
    # Buscar y reparar
    lines = content.split('\n')
    fixed_lines = []
    changes_made = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Buscar clase PokerStarsAdapter
        if 'class PokerStarsAdapter' in line:
            print("✅ Encontrada clase PokerStarsAdapter")
            
            # Buscar el __init__ dentro de esta clase
            j = i + 1
            while j < len(lines):
                # Si encontramos otro método o fin de clase, parar
                if lines[j].strip().startswith('def ') and '__init__' not in lines[j]:
                    break
                if lines[j].strip() == '' and j > i + 10:  # Línea vacía después de varias líneas
                    break
                    
                # Buscar __init__
                if 'def __init__' in lines[j]:
                    print(f"✅ Encontrado constructor en línea {j+1}")
                    
                    # Encontrar indentación
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    
                    # Buscar dónde insertar self.platform (después de super().__init__ si existe, o al inicio del cuerpo)
                    k = j + 1
                    inserted = False
                    
                    while k < len(lines) and len(lines[k]) - len(lines[k].lstrip()) > indent:
                        # Insertar después de la primera línea no vacía del cuerpo
                        if lines[k].strip() and not inserted:
                            # Añadir self.platform
                            platform_line = ' ' * (indent + 4) + 'self.platform = "pokerstars"'
                            fixed_lines.append(platform_line)
                            print(f"✅ Añadido: {platform_line}")
                            changes_made = True
                            inserted = True
                        
                        fixed_lines.append(lines[k])
                        k += 1
                    
                    # Si no se insertó, insertar al final del __init__
                    if not inserted and k < len(lines):
                        platform_line = ' ' * (indent + 4) + 'self.platform = "pokerstars"'
                        fixed_lines.append(platform_line)
                        print(f"✅ Añadido al final: {platform_line}")
                        changes_made = True
                    
                    # Saltar las líneas que ya procesamos
                    i = k - 1
                    break
                    
                j += 1
        
        i += 1
    
    # También verificar y arreglar usos de self.platform
    print("\n🔍 Verificando usos de self.platform...")
    
    for i, line in enumerate(fixed_lines):
        # Si hay CardRecognizer que use self.platform pero puede que no exista
        if 'CardRecognizer(' in line and 'platform=' in line:
            # Reemplazar self.platform por "pokerstars" directo
            if 'self.platform' in line:
                new_line = line.replace('self.platform', '"pokerstars"')
                fixed_lines[i] = new_line
                print(f"✅ Línea {i+1}: Reemplazado self.platform por 'pokerstars'")
                changes_made = True
    
    # Si no hubo cambios, añadir platform en otra ubicación
    if not changes_made:
        print("⚠️  No se pudo encontrar dónde insertar, añadiendo al inicio de la clase...")
        
        # Buscar después de class PokerStarsAdapter:
        for i, line in enumerate(fixed_lines):
            if 'class PokerStarsAdapter' in line:
                # Añadir después de la definición de clase
                indent = len(line) - len(line.lstrip())
                platform_line = ' ' * (indent + 4) + 'def __init__(self, stealth_level="MEDIUM"):'
                platform_line2 = ' ' * (indent + 8) + 'self.platform = "pokerstars"'
                platform_line3 = ' ' * (indent + 8) + 'self.stealth_level = stealth_level'
                
                # Insertar después de la línea actual
                fixed_lines.insert(i + 1, platform_line)
                fixed_lines.insert(i + 2, platform_line2)
                fixed_lines.insert(i + 3, platform_line3)
                print("✅ Añadido constructor básico con platform")
                changes_made = True
                break
    
    # Guardar cambios
    if changes_made:
        fixed_content = '\n'.join(fixed_lines)
        with open(adapter_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print("\n💾 Archivo actualizado exitosamente")
    else:
        print("\n⚠️  No se hicieron cambios (puede que ya esté corregido)")
    
    # 2. Crear verificador
    print("\n🧪 Creando verificador...")
    
    verifier = '''#!/usr/bin/env python3
"""
VERIFICADOR - PokerStars Adapter
"""
import sys
import os

sys.path.insert(0, 'src')

print("=" * 60)
print("🔍 VERIFICANDO POKERSTARS ADAPTER")
print("=" * 60)

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    print("✅ Importación exitosa")
    
    try:
        # Crear instancia
        adapter = PokerStarsAdapter()
        print("✅ Adaptador creado exitosamente")
        
        # Verificar atributos
        if hasattr(adapter, 'platform'):
            print(f"✅ Atributo 'platform' existe: {adapter.platform}")
        else:
            print("❌ Atributo 'platform' NO existe")
        
        if hasattr(adapter, 'stealth_level'):
            print(f"✅ Atributo 'stealth_level' existe: {adapter.stealth_level}")
        
        # Verificar componentes
        if hasattr(adapter, 'capture_system') and adapter.capture_system:
            print("✅ capture_system inicializado")
        
        if hasattr(adapter, 'table_detector') and adapter.table_detector:
            print("✅ table_detector inicializado")
        
        if hasattr(adapter, 'card_recognizer') and adapter.card_recognizer:
            print("✅ card_recognizer inicializado")
        
        if hasattr(adapter, 'text_ocr') and adapter.text_ocr:
            print("✅ text_ocr inicializado")
        
        print("\n🎉 ¡ADAPTADOR FUNCIONAL!")
        print("\n🚀 Próximo paso: python test_pokerstars.py")
        
    except TypeError as e:
        print(f"❌ Error de tipo en constructor: {e}")
        print("\n💡 Posible problema con parámetros de algún componente")
        import traceback
        traceback.print_exc()
        
    except AttributeError as e:
        print(f"❌ Error de atributo: {e}")
        print("\n💡 Falta definir algún atributo en __init__")
        
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
'''

    with open("verify_adapter.py", 'w', encoding='utf-8') as f:
        f.write(verifier)
    
    print("✅ Verificador creado: verify_adapter.py")
    
    # 3. Instrucciones
    print("\n" + "=" * 60)
    print("🎯 INSTRUCCIONES")
    print("=" * 60)
    
    print("\n1. Verifica la reparación:")
    print("   python verify_adapter.py")
    
    print("\n2. Si funciona, prueba el sistema completo:")
    print("   python test_pokerstars.py")
    
    print("\n3. Si hay errores, revisa manualmente:")
    print("   - Abre src/platforms/pokerstars_adapter.py")
    print("   - Busca la clase PokerStarsAdapter")
    print("   - Asegúrate que en __init__ haya:")
    print("     self.platform = \"pokerstars\"")
    
    print("\n🔧 SOLUCIÓN MANUAL SI PERSISTE:")
    print("   Abre el archivo y añade esta línea en __init__:")
    print("   self.platform = \"pokerstars\"")
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()