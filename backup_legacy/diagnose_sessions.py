# diagnose_sessions.py - Diagnóstico de sesiones de captura
import os
import json
from pathlib import Path

def print_section(title):
    """Imprimir sección con título"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def diagnose_sessions():
    """Diagnosticar todas las sesiones de captura"""
    print_section("DIAGNÓSTICO DE SESIONES DE CAPTURA")
    
    base_path = "data/card_templates/auto_captured"
    
    if not os.path.exists(base_path):
        print(" No existe la carpeta base:", base_path)
        print("\n Ejecuta primero el capturador automático")
        return
    
    print(f" Carpeta base: {base_path}")
    
    # Listar todas las carpetas
    all_items = os.listdir(base_path)
    print(f"\n Total items en carpeta: {len(all_items)}")
    
    # Separar carpetas y archivos
    folders = []
    files = []
    
    for item in all_items:
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
        else:
            files.append(item)
    
    print(f" Carpetas (sesiones): {len(folders)}")
    print(f" Archivos sueltos: {len(files)}")
    
    if files:
        print("\n  Archivos sueltos (no deberían estar aquí):")
        for f in files[:5]:
            print(f"    {f}")
        if len(files) > 5:
            print(f"   ... y {len(files) - 5} más")
    
    if not folders:
        print("\n No hay carpetas de sesiones")
        return
    
    print_section("ANÁLISIS DE SESIONES")
    
    # Analizar cada carpeta
    for i, folder in enumerate(sorted(folders, reverse=True)[:10], 1):  # Últimas 10
        folder_path = os.path.join(base_path, folder)
        
        print(f"\n{i}.  {folder}")
        print(f"    Ruta: {folder_path}")
        
        # Verificar estructura
        subfolders = []
        subfiles = []
        
        for item in os.listdir(folder_path):
            item_full = os.path.join(folder_path, item)
            if os.path.isdir(item_full):
                subfolders.append(item)
            else:
                subfiles.append(item)
        
        print(f"    Subcarpetas: {len(subfolders)}")
        if subfolders:
            for sf in subfolders:
                print(f"       {sf}")
        
        print(f"    Archivos: {len(subfiles)}")
        
        # Buscar archivos importantes
        has_session_info = "session_info.json" in subfiles
        has_raw_captures = "raw_captures" in subfolders
        
        print(f"    session_info.json: {'SÍ' if has_session_info else 'NO'}")
        print(f"    raw_captures: {'SÍ' if has_raw_captures else 'NO'}")
        
        # Contar imágenes en raw_captures
        if has_raw_captures:
            raw_path = os.path.join(folder_path, "raw_captures")
            if os.path.exists(raw_path):
                png_files = [f for f in os.listdir(raw_path) if f.endswith('.png')]
                jpg_files = [f for f in os.listdir(raw_path) if f.endswith(('.jpg', '.jpeg'))]
                
                print(f"    PNG: {len(png_files)} imágenes")
                print(f"    JPG: {len(jpg_files)} imágenes")
                
                # Verificar si hay JSONs correspondientes
                json_files = [f for f in os.listdir(raw_path) if f.endswith('.json')]
                print(f"    JSON: {len(json_files)} metadatos")
                
                # Mostrar primeras imágenes
                if png_files:
                    print(f"     Ejemplos: {', '.join(png_files[:3])}")
        
        # Verificar session_info.json
        if has_session_info:
            info_path = os.path.join(folder_path, "session_info.json")
            try:
                with open(info_path, 'r') as f:
                    info = json.load(f)
                print(f"    ID sesión: {info.get('session_id', 'NO')}")
                print(f"    Creada: {info.get('created_at', 'NO')}")
            except Exception as e:
                print(f"    Error leyendo session_info: {e}")
    
    if len(folders) > 10:
        print(f"\n ... y {len(folders) - 10} sesiones más")
    
    print_section("RECOMENDACIONES")
    
    # Verificar estructura esperada
    expected_folders = ["raw_captures", "reports"]
    
    print(" ESTRUCTURA ESPERADA por sesión:")
    for ef in expected_folders:
        print(f"    {ef}/")
    
    print("\n SESIONES VÁLIDAS (para clasificación):")
    valid_count = 0
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        raw_path = os.path.join(folder_path, "raw_captures")
        
        if os.path.exists(raw_path):
            png_files = [f for f in os.listdir(raw_path) if f.endswith('.png')]
            if png_files:
                valid_count += 1
                print(f"    {folder}: {len(png_files)} imágenes")
    
    if valid_count == 0:
        print("    No hay sesiones válidas")
        print("\n Ejecuta el capturador y asegúrate de que PokerStars esté visible")
    else:
        print(f"\n Total sesiones válidas: {valid_count}/{len(folders)}")
        print(f" Para clasificar, usa el ID de sesión (ej: {folders[0]})")

def check_pokerstars_real():
    """Verificar estructura de pokerstars_real"""
    print_section("VERIFICANDO TEMPLATES ORGANIZADOS")
    
    base_path = "data/card_templates/pokerstars_real"
    
    if not os.path.exists(base_path):
        print(" No existe la carpeta:", base_path)
        print("\n El clasificador creará esta estructura automáticamente")
        return
    
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    total_files = 0
    
    print(" Templates por palo:")
    for suit in suits:
        suit_path = os.path.join(base_path, suit)
        if os.path.exists(suit_path):
            files = [f for f in os.listdir(suit_path) 
                    if f.endswith(('.png', '.jpg', '.jpeg'))]
            count = len(files)
            print(f"   {suit.upper():10} {count:3} templates")
            
            if files and count <= 5:
                print(f"      Ejemplos: {', '.join(files[:3])}")
            
            total_files += count
        else:
            print(f"   {suit.upper():10} 0   (carpeta no existe)")
    
    print(f"\n TOTAL templates: {total_files}")
    
    if total_files == 0:
        print("\n No hay templates organizados aún")
        print("   Ejecuta el clasificador después de capturar cartas")
    elif total_files < 20:
        print("\n  Pocos templates para reconocimiento confiable")
        print("   Se recomienda capturar y clasificar más cartas")
    else:
        print("\n Base de templates suficiente para reconocimiento básico")

def main():
    """Función principal de diagnóstico"""
    print(" POKER COACH PRO - DIAGNÓSTICO DE SESIONES")
    print("=" * 70)
    
    print("Este script analiza la estructura de sesiones de captura")
    print("y verifica que todo esté funcionando correctamente.")
    
    diagnose_sessions()
    check_pokerstars_real()
    
    print("\n" + "=" * 70)
    print(" RESUMEN DE COMANDOS ÚTILES:")
    print("=" * 70)
    
    print("\n PARA CAPTURAR:")
    print("   python src/auto_template_capturer.py")
    print("   python start_auto_capture.py (opción 1)")
    
    print("\n PARA CLASIFICAR:")
    print("   python src/card_classifier.py")
    print("   python start_auto_capture.py (opción 4 o 5)")
    
    print("\n PARA SOLUCIONAR PROBLEMAS:")
    print("    Asegúrate de que PokerStars esté ABIERTO y VISIBLE")
    print("   • Verifica config/pokerstars_coords.json existe")
    print("   • Ejecuta este diagnóstico periódicamente")
    
    print("\n📁 ESTRUCTURA ESPERADA:")
    print("   data/card_templates/auto_captured/YYYYMMDD_HHMMSS/")
    print("   ├── raw_captures/      # Imágenes capturadas")
    print("   ├── reports/           # Reportes de sesión")
    print("   └── session_info.json  # Información de sesión")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...")
