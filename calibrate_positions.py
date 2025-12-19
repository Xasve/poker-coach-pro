# calibrate_positions.py - Ajustar posiciones de cartas
import sys
import os
import cv2
import numpy as np

print("🎯 CALIBRACIÓN DE POSICIONES DE CARTAS")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    # Crear adaptador
    adapter = PokerStarsAdapter(stealth_level=1)
    
    print("📸 Capturando pantalla para calibración...")
    screenshot = adapter.capture_table()
    
    if screenshot is None:
        print("❌ No se pudo capturar pantalla")
        exit(1)
    
    height, width = screenshot.shape[:2]
    print(f"✅ Captura: {width}x{height}px")
    
    # Guardar captura original
    cal_dir = "debug/calibration"
    os.makedirs(cal_dir, exist_ok=True)
    original_path = os.path.join(cal_dir, "original.png")
    cv2.imwrite(original_path, screenshot)
    print(f"💾 Original guardado: {original_path}")
    
    # Mostrar imagen con grid para referencia
    grid_img = screenshot.copy()
    
    # Dibujar grid
    grid_size = 100
    for x in range(0, width, grid_size):
        cv2.line(grid_img, (x, 0), (x, height), (0, 255, 0), 1)
        cv2.putText(grid_img, str(x), (x, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    for y in range(0, height, grid_size):
        cv2.line(grid_img, (0, y), (width, y), (0, 255, 0), 1)
        cv2.putText(grid_img, str(y), (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    grid_path = os.path.join(cal_dir, "grid.png")
    cv2.imwrite(grid_path, grid_img)
    
    print("\n🎮 INSTRUCCIONES DE CALIBRACIÓN:")
    print("1. Abre la imagen en debug/calibration/grid.png")
    print("2. Identifica las coordenadas de las cartas:")
    print("   - Cartas propias (abajo centro)")
    print("   - Cartas comunitarias (centro)")
    print("3. Anota las coordenadas (x, y, ancho, alto)")
    
    # Posiciones por defecto (ajustar según lo que veas)
    default_positions = {
        "hole_card_1": (width//2 - 110, height - 150, 71, 96),
        "hole_card_2": (width//2 + 40, height - 150, 71, 96),
        "community_1": (width//2 - 180, height//2 - 60, 71, 96),
        "community_2": (width//2 - 90, height//2 - 60, 71, 96),
        "community_3": (width//2, height//2 - 60, 71, 96),
        "community_4": (width//2 + 90, height//2 - 60, 71, 96),
        "community_5": (width//2 + 180, height//2 - 60, 71, 96)
    }
    
    print("\n📏 POSICIONES POR DEFECTO (1080p):")
    for name, (x, y, w, h) in default_positions.items():
        print(f"   {name}: ({x}, {y}, {w}, {h})")
    
    # Crear imagen con rectángulos en posiciones por defecto
    rect_img = screenshot.copy()
    colors = {
        "hole": (0, 0, 255),      # Rojo para cartas propias
        "community": (0, 255, 0)  # Verde para comunitarias
    }
    
    # Dibujar rectángulos para cartas propias
    for name in ["hole_card_1", "hole_card_2"]:
        x, y, w, h = default_positions[name]
        cv2.rectangle(rect_img, (x, y), (x+w, y+h), colors["hole"], 2)
        cv2.putText(rect_img, name, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors["hole"], 1)
    
    # Dibujar rectángulos para cartas comunitarias
    for name in ["community_1", "community_2", "community_3", "community_4", "community_5"]:
        x, y, w, h = default_positions[name]
        cv2.rectangle(rect_img, (x, y), (x+w, y+h), colors["community"], 2)
        cv2.putText(rect_img, name, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors["community"], 1)
    
    rect_path = os.path.join(cal_dir, "default_positions.png")
    cv2.imwrite(rect_path, rect_img)
    print(f"\n💾 Imagen con posiciones guardada: {rect_path}")
    
    print("\n🔧 PARA AJUSTAR POSICIONES:")
    print("1. Si los rectángulos no coinciden con las cartas,")
    print("2. Edita el archivo: src/platforms/pokerstars_adapter.py")
    print("3. Busca las funciones recognize_hole_cards y recognize_community_cards")
    print("4. Ajusta las coordenadas en las listas card_positions")
    
    # Crear archivo de configuración de posiciones
    position_config = {
        "screen_resolution": f"{width}x{height}",
        "positions": default_positions,
        "card_size": {"width": 71, "height": 96},
        "instructions": "Ajustar coordenadas si los rectángulos no alinean con las cartas"
    }
    
    config_path = os.path.join(cal_dir, "position_config.json")
    with open(config_path, 'w') as f:
        json.dump(position_config, f, indent=2)
    
    print(f"\n📋 Configuración guardada: {config_path}")
    print("\n🎯 Siguiente: Ejecuta 'python test_real_capture.py' para probar")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()