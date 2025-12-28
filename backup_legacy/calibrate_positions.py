# calibrate_detector.py - Calibrar detector de mesa automáticamente
import sys
import os
import cv2
import numpy as np
import json

print("🎨 CALIBRACIÓN AUTOMÁTICA DEL DETECTOR DE MESA")
print("=" * 60)

sys.path.insert(0, 'src')

try:
    from screen_capture.table_detector import TableDetector
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("🔧 Inicializando componentes...")
    adapter = PokerStarsAdapter(stealth_level=1)
    detector = TableDetector()
    
    print("\n📸 Capturando pantalla de referencia...")
    screenshot = adapter.capture_table()
    
    if screenshot is None:
        print("❌ No se pudo capturar pantalla")
        exit(1)
    
    # Guardar captura para análisis
    cal_dir = "debug/calibration"
    os.makedirs(cal_dir, exist_ok=True)
    
    capture_path = os.path.join(cal_dir, "detector_calibration.png")
    cv2.imwrite(capture_path, screenshot)
    print(f"💾 Captura guardada: {capture_path}")
    
    print("\n🔍 Analizando colores en la imagen...")
    
    # Convertir a HSV
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    height, width = screenshot.shape[:2]
    
    # Analizar distribución de colores
    print("📊 Analizando histograma de colores...")
    
    # Calcular histograma de Hue (tono)
    hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    
    # Encontrar picos en el histograma (colores dominantes)
    peaks = []
    for i in range(1, 179):
        if hist_h[i] > hist_h[i-1] and hist_h[i] > hist_h[i+1] and hist_h[i] > 1000:
            peaks.append(i)
    
    print(f"   Picos de color encontrados en HUE: {peaks}")
    
    # Buscar verdes (HUE ~35-85 en OpenCV)
    green_peaks = [p for p in peaks if 35 <= p <= 85]
    
    if green_peaks:
        print(f"   ✅ Picos verdes encontrados: {green_peaks}")
        
        # Calibrar rangos basados en los picos
        avg_green = np.mean(green_peaks)
        
        # Rangos recomendados
        lower_h = max(0, int(avg_green - 15))
        upper_h = min(180, int(avg_green + 15))
        
        print(f"\n🎨 RANGOS RECOMENDADOS:")
        print(f"   HUE: [{lower_h}, {upper_h}]")
        print(f"   SATURACIÓN: [40, 255]")
        print(f"   VALOR: [40, 255]")
        
        # Probar detección con nuevos rangos
        print("\n🧪 Probando detección con rangos actuales...")
        current_detection = detector.detect(screenshot)
        print(f"   Detección actual: {'✅' if current_detection else '❌'}")
        
        # Crear máscara visual para debug
        test_lower = np.array([lower_h, 40, 40])
        test_upper = np.array([upper_h, 255, 255])
        test_mask = cv2.inRange(hsv, test_lower, test_upper)
        
        # Aplicar máscara a la imagen original
        masked_img = cv2.bitwise_and(screenshot, screenshot, mask=test_mask)
        
        # Guardar imagen con máscara
        mask_path = os.path.join(cal_dir, "green_mask.png")
        cv2.imwrite(mask_path, masked_img)
        print(f"💾 Máscara de verde guardada: {mask_path}")
        
        # Calcular porcentaje de verde
        green_pixels = cv2.countNonZero(test_mask)
        total_pixels = height * width
        green_percent = (green_pixels / total_pixels) * 100
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   Píxeles verdes: {green_pixels:,}")
        print(f"   Total píxeles: {total_pixels:,}")
        print(f"   Porcentaje verde: {green_percent:.2f}%")
        
        # Recomendación
        if green_percent < 1.0:
            print("\n⚠️  ADVERTENCIA: Poco verde detectado")
            print("   Posibles causas:")
            print("   1. PokerStars no está visible")
            print("   2. Usas un tema oscuro/diferente")
            print("   3. La mesa está minimizada")
            print("\n   Solución: Abre PokerStars en una mesa verde clásica")
        elif green_percent > 30.0:
            print("\n✅ ¡Mucho verde detectado! El detector debería funcionar bien.")
        else:
            print(f"\n📊 Verde moderado detectado ({green_percent:.1f}%)")
            print("   El detector debería funcionar con ajustes menores.")
        
        # Crear archivo de configuración
        config = {
            "calibration_date": "auto-generated",
            "screen_resolution": f"{width}x{height}",
            "detected_green_percent": green_percent,
            "recommended_hue_range": [int(lower_h), int(upper_h)],
            "current_threshold": 0.015,
            "notes": "Ajustar green_threshold en table_detector.py si es necesario"
        }
        
        config_path = os.path.join(cal_dir, "detector_config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n💾 Configuración guardada: {config_path}")
        
    else:
        print("❌ No se encontraron picos verdes en la imagen")
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("1. Asegúrate de que PokerStars esté ABIERTO y VISIBLE")
        print("2. Usa el tema CLÁSICO (verde) de PokerStars")
        print("3. Si usas tema oscuro, necesitamos ajustar el detector")
        print("4. La captura está en: debug/calibration/detector_calibration.png")
        
        # Sugerir ajuste manual
        print("\n🎯 AJUSTE MANUAL REQUERIDO:")
        print("   Edita: src/screen_capture/table_detector.py")
        print("   Busca 'lower_green1' y 'upper_green1'")
        print("   Ajusta los valores según el color de tu mesa")
    
    print("\n" + "=" * 60)
    print("🎯 CALIBRACIÓN COMPLETADA")
    print("\n📝 Siguiente paso: Ejecuta 'python run_pokerstars_optimized.py'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()