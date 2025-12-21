
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
