# auto_continue.py - Continuación automática del desarrollo
import os
import sys
import json
from datetime import datetime

def analyze_project_state():
    """Analizar estado actual del proyecto"""
    print(" ANÁLISIS DEL PROYECTO")
    print("=" * 50)
    
    state = {
        "timestamp": datetime.now().isoformat(),
        "dependencies": {},
        "files": {},
        "directories": {},
        "recommendations": []
    }
    
    # Verificar dependencias
    print("\n DEPENDENCIAS:")
    deps_to_check = ["numpy", "cv2", "pyautogui", "PIL", "pytesseract"]
    
    for dep in deps_to_check:
        try:
            if dep == "cv2":
                import cv2
                version = cv2.__version__
            elif dep == "numpy":
                import numpy
                version = numpy.__version__
            elif dep == "PIL":
                from PIL import Image
                import PIL
                version = PIL.__version__
            else:
                __import__(dep)
                version = "OK"
            
            print(f"    {dep}")
            state["dependencies"][dep] = version
        except ImportError:
            print(f"    {dep}")
            state["dependencies"][dep] = "MISSING"
            state["recommendations"].append(f"Instalar {dep}: pip install {dep}")
    
    # Verificar archivos clave
    print("\n ARCHIVOS CLAVE:")
    key_files = [
        ("color_optimizer.py", "Optimizador de color"),
        ("detect_coords.py", "Configurador PokerStars"),
        ("smart_capture_fixed_v2.py", "Captura de dataset"),
        ("poker_coach_simple.py", "Sistema simplificado")
    ]
    
    for file_name, description in key_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"    {description} ({size/1024:.1f} KB)")
            state["files"][file_name] = {"size": size, "exists": True}
        else:
            print(f"    {description}")
            state["files"][file_name] = {"exists": False}
            state["recommendations"].append(f"Crear/recuperar {file_name}")
    
    # Verificar directorios de datos
    print("\n DIRECTORIOS DE DATOS:")
    data_dirs = ["data/templates", "data/calibration_samples", "config", "logs"]
    
    for dir_path in data_dirs:
        if os.path.exists(dir_path):
            items = len(os.listdir(dir_path)) if os.path.isdir(dir_path) else 1
            print(f"    {dir_path} ({items} items)")
            state["directories"][dir_path] = {"exists": True, "items": items}
        else:
            print(f"    {dir_path}")
            state["directories"][dir_path] = {"exists": False}
    
    print("\n" + "=" * 50)
    return state

def generate_next_steps(state):
    """Generar próximos pasos basados en el estado"""
    print("\n PRÓXIMOS PASOS RECOMENDADOS:")
    
    steps = []
    
    # Paso 1: Verificar dependencias
    missing_deps = [d for d, v in state["dependencies"].items() if v == "MISSING"]
    if missing_deps:
        steps.append(("1", "Instalar dependencias faltantes", f"pip install {' '.join(missing_deps)}"))
    
    # Paso 2: Configurar PokerStars si no hay configuración
    if not state["files"].get("detect_coords.py", {}).get("exists", False):
        steps.append(("2", "Configurar PokerStars", "python detect_coords.py (si existe)"))
    
    # Paso 3: Calibrar color
    if state["files"].get("color_optimizer.py", {}).get("exists", False):
        steps.append(("3", "Calibrar detección de color", "python color_optimizer.py"))
    
    # Paso 4: Capturar dataset
    if state["files"].get("smart_capture_fixed_v2.py", {}).get("exists", False):
        steps.append(("4", "Capturar dataset inicial", "python smart_capture_fixed_v2.py --limit 50"))
    
    # Paso 5: Probar sistema
    if state["files"].get("poker_coach_simple.py", {}).get("exists", False):
        steps.append(("5", "Probar sistema completo", "python poker_coach_simple.py"))
    
    # Si no hay pasos, sugerir revisión
    if not steps:
        steps.append(("", "Revisar estructura del proyecto", "Revisar archivos README.md y documentación"))
    
    # Mostrar pasos
    for number, description, command in steps:
        print(f"{number} {description}")
        print(f"    {command}")
    
    return steps

def save_state_report(state):
    """Guardar reporte del estado"""
    report_dir = "logs/project_state"
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"state_{timestamp}.json")
    
    with open(report_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print(f"\n Reporte guardado en: {report_file}")
    return report_file

def main():
    """Función principal"""
    print(" CONTINUACIÓN AUTOMÁTICA - POKER COACH PRO")
    print("=" * 60)
    
    # Analizar estado
    state = analyze_project_state()
    
    # Generar próximos pasos
    steps = generate_next_steps(state)
    
    # Guardar reporte
    report_file = save_state_report(state)
    
    print("\n" + "=" * 60)
    print(" Para continuar, ejecuta uno de los comandos sugeridos arriba")
    print(f" Estado detallado en: {report_file}")
    
    if steps:
        print("\n Recomendación principal: " + steps[0][2])

if __name__ == "__main__":
    main()
