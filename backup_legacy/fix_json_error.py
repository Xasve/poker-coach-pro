# Script para reparar la serialización JSON con tipos NumPy
import json
import numpy as np
from datetime import datetime

class NumpyJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para manejar tipos NumPy en JSON"""
    
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64,
                           np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.complexfloating):
            return {'real': obj.real, 'imag': obj.imag}
        elif hasattr(obj, '__dict__'):
            return self._clean_dict(obj.__dict__)
        elif isinstance(obj, dict):
            return self._clean_dict(obj)
        elif isinstance(obj, (list, tuple, set)):
            return [self.default(item) for item in obj]
        else:
            return super().default(obj)
    
    def _clean_dict(self, d):
        """Limpiar diccionario recursivamente"""
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._clean_dict(value)
            elif isinstance(value, (list, tuple, set)):
                result[key] = [self.default(item) for item in value]
            else:
                result[key] = self.default(value)
        return result

def apply_fix_to_complete_system():
    """Aplicar el fix al archivo complete_poker_learning_system.py"""
    
    target_file = "complete_poker_learning_system.py"
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Encontrar el método save_complete_state
        if 'def save_complete_state(self):' in content:
            print(f" Encontrado método save_complete_state en {target_file}")
            
            # Reemplazar la línea problemática
            old_line = 'json.dump(complete_state, f, indent=2, ensure_ascii=False)'
            new_line = 'json.dump(complete_state, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)'
            
            if old_line in content:
                content = content.replace(old_line, new_line)
                
                # Añadir la definición del encoder si no está presente
                if 'class NumpyJSONEncoder' not in content:
                    # Insertar después de los imports
                    imports_end = content.find('\n\n', content.find('import json'))
                    if imports_end != -1:
                        encoder_def = '''
class NumpyJSONEncoder(json.JSONEncoder):
    """Encoder personalizado para manejar tipos NumPy en JSON"""
    
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64,
                           np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.complexfloating):
            return {'real': obj.real, 'imag': obj.imag}
        elif hasattr(obj, '__dict__'):
            return self._clean_dict(obj.__dict__)
        elif isinstance(obj, dict):
            return self._clean_dict(obj)
        elif isinstance(obj, (list, tuple, set)):
            return [self.default(item) for item in obj]
        else:
            return super().default(obj)
    
    def _clean_dict(self, d):
        """Limpiar diccionario recursivamente"""
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._clean_dict(value)
            elif isinstance(value, (list, tuple, set)):
                result[key] = [self.default(item) for item in value]
            else:
                result[key] = self.default(value)
        return result
'''
                        content = content[:imports_end] + encoder_def + content[imports_end:]
                
                # Guardar el archivo reparado
                backup_file = target_file + '.backup'
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f" Backup creado: {backup_file}")
                
                # Ahora guardar los cambios
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f" Fix aplicado a {target_file}")
                print("   Se añadió NumpyJSONEncoder para manejar tipos NumPy")
                
                return True
            else:
                print(f" No se encontró la línea problemática en {target_file}")
                return False
        else:
            print(f" Método save_complete_state no encontrado en {target_file}")
            return False
            
    except Exception as e:
        print(f" Error aplicando fix: {e}")
        return False

def create_standalone_fix():
    """Crear un script standalone para reparar el error"""
    
    fix_code = '''
import json
import numpy as np
from datetime import datetime

def numpy_to_python(obj):
    """Convertir objetos NumPy a tipos nativos de Python"""
    if isinstance(obj, dict):
        return {k: numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [numpy_to_python(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj

def save_state_fixed(state_data, filename):
    """Guardar estado con fix aplicado"""
    # Convertir todos los objetos NumPy a tipos Python
    cleaned_data = numpy_to_python(state_data)
    
    # Guardar en JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    print(f" Estado guardado: {filename}")
    return True

if __name__ == "__main__":
    # Ejemplo de uso
    test_data = {
        'int_numpy': np.int64(42),
        'float_numpy': np.float64(3.14159),
        'array_numpy': np.array([1, 2, 3]),
        'regular_int': 100,
        'regular_float': 2.71828,
        'timestamp': datetime.now().isoformat()
    }
    
    save_state_fixed(test_data, 'test_state_fixed.json')
    print(" Fix verificado correctamente")
'''
    
    with open('json_fix_standalone.py', 'w', encoding='utf-8') as f:
        f.write(fix_code)
    
    print(" Script standalone creado: json_fix_standalone.py")
    return 'json_fix_standalone.py'

def test_fix():
    """Probar que el fix funciona"""
    import numpy as np
    
    test_data = {
        'numpy_int64': np.int64(100),
        'numpy_float64': np.float64(3.14159),
        'numpy_array': np.array([1, 2, 3]),
        'regular_data': {
            'int': 42,
            'float': 2.71828,
            'list': [1, 'two', 3.0]
        }
    }
    
    # Probar con encoder personalizado
    encoder = NumpyJSONEncoder()
    try:
        result = encoder.encode(test_data)
        print(" Test de encoder exitoso")
        return True
    except Exception as e:
        print(f" Error en test: {e}")
        return False

def main():
    """Función principal"""
    print(" APLICANDO FIX PARA ERROR DE SERIALIZACIÓN JSON")
    print("=" * 50)
    
    # Aplicar fix al archivo principal
    print("\n1 Aplicando fix a complete_poker_learning_system.py...")
    if apply_fix_to_complete_system():
        print("    Fix aplicado exitosamente")
    else:
        print("    No se pudo aplicar el fix automáticamente")
        print("    Creando solución alternativa...")
    
    # Crear script standalone
    print("\n2 Creando script standalone de reparación...")
    standalone_file = create_standalone_fix()
    
    # Probar el fix
    print("\n3 Probando la solución...")
    if test_fix():
        print("    Test completado exitosamente")
    else:
        print("    El test encontró problemas")
    
    print("\n" + "=" * 50)
    print(" FIX APLICADO COMPLETAMENTE")
    print("\n Para aplicar manualmente el fix:")
    print("   1. En complete_poker_learning_system.py, busca:")
    print("      json.dump(complete_state, f, indent=2, ensure_ascii=False)")
    print("   2. Reemplázalo con:")
    print("      json.dump(complete_state, f, indent=2, ensure_ascii=False, cls=NumpyJSONEncoder)")
    print("\n Ahora ejecuta:")
    print("   python quick_start.py")

if __name__ == "__main__":
    main()
