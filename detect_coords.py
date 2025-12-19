import mss, cv2, numpy as np, os, json, time
print(" DETECTOR DE POKERSTARS - COORDENADAS REALES")
print("="*60)

with mss.mss() as sct:
    for i in range(3):
        print(f"\n Captura {i+1}/3...")
        img = np.array(sct.grab(sct.monitors[1]))
        
        # Buscar verde (mesas PokerStars)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        verde_bajo = np.array([35, 50, 50])
        verde_alto = np.array([85, 255, 255])
        mascara = cv2.inRange(hsv, verde_bajo, verde_alto)
        
        # Encontrar áreas verdes grandes
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = []
        
        for c in contornos:
            x,y,w,h = cv2.boundingRect(c)
            area = w*h
            if area > 100000:  # Áreas grandes (> 100k píxeles)
                areas.append({"x":x, "y":y, "w":w, "h":h, "area":area})
                
        if areas:
            print(f"✅ Encontradas {len(areas)} posibles mesas:")
            for idx, a in enumerate(areas, 1):
                print(f"   Mesa {idx}: Posición [{a['x']}, {a['y']}]")
                print(f"           Tamaño: {a['w']}x{a['h']} ({a['area']:,} px)")
                
            # Guardar configuración
            config = {
                "screen_resolution": f"{img.shape[1]}x{img.shape[0]}",
                "pokerstars_regions": {
                    "mesa": [areas[0]["x"], areas[0]["y"], areas[0]["w"], areas[0]["h"]],
                    "cartas_hero": [areas[0]["x"] + areas[0]["w"]//2 - 75, areas[0]["y"] + areas[0]["h"] - 100, 150, 60],
                    "cartas_comunitarias": [areas[0]["x"] + 50, areas[0]["y"] + areas[0]["h"]//2 - 40, 400, 80],
                    "pozo": [areas[0]["x"] + areas[0]["w"]//2 - 100, areas[0]["y"] + 100, 200, 40]
                },
                "detected_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open("config/pokerstars_coords.json", "w") as f:
                json.dump(config, f, indent=2)
            
            print(f"\n💾 Configuración guardada: config/pokerstars_coords.json")
            print("🎯 ¡COORDENADAS LISTAS PARA MODO REAL!")
            break
            
        time.sleep(1)
    
    if not areas:
        print("❌ No se detectaron mesas de PokerStars")
        print("\n💡 Asegúrate de:")
        print("   1. Tener PokerStars ABIERTO en una mesa")
        print("   2. La ventana debe ser VISIBLE (no minimizada)")
        print("   3. Ejecutar de nuevo con PokerStars visible")
