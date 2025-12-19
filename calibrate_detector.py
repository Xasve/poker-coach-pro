# calibrate_detector.py - Calibrar detector de mesa automáticamente (CORREGIDO)
import sys
import os
import cv2
import numpy as np
import json
import time

print("🎨 CALIBRACIÓN AUTOMÁTICA DEL DETECTOR DE MESA")
print("=" * 60)

# Añadir src al path
sys.path.insert(0, 'src')

def create_histogram_image(hist_h, cal_dir):
    """Crear imagen visual del histograma"""
    # Crear imagen para histograma
    hist_image = np.zeros((300, 360, 3), dtype=np.uint8)
    hist_image[:] = (40, 40, 40)  # Fondo gris
    
    # Normalizar histograma para visualización
    hist_normalized = hist_h.copy()
    cv2.normalize(hist_h, hist_normalized, 0, hist_image.shape[0], cv2.NORM_MINMAX)
    
    # Dibujar histograma
    bin_w = 2
    for i in range(180):
        height = int(hist_normalized[i][0])  # 🔥 CORRECCIÓN: Acceder correctamente al array
        cv2.rectangle(hist_image, 
                     (i*bin_w, hist_image.shape[0]),
                     (i*bin_w + bin_w, hist_image.shape[0] - height),
                     (0, 255, 0) if 35 <= i <= 85 else (100, 100, 100),  # Verde en rango verde
                     -1)
    
    # Añadir etiquetas
    cv2.putText(hist_image, "Histograma de Colores (HUE)", (10, 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(hist_image, "Rango verde: 35-85", (10, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    
    # Guardar histograma
    hist_path = os.path.join(cal_dir, "color_histogram.png")
    cv2.imwrite(hist_path, hist_image)
    print(f"💾 Histograma guardado: {hist_path}")
    
    return hist_path

try:
    from screen_capture.table_detector import TableDetector
    from platforms.pokerstars_adapter import PokerStarsAdapter
    
    print("🔧 Inicializando componentes...")
    adapter = PokerStarsAdapter(stealth_level=1)
    detector = TableDetector()
    
    print("\n📸 Capturando pantalla de referencia...")
    print("⏳ Tomando captura en 3 segundos...")
    time.sleep(3)
    
    screenshot = adapter.capture_table()
    
    if screenshot is None:
        print("❌ No se pudo capturar pantalla")
        print("\n🔧 Solución:")
        print("1. Asegúrate de que MSS esté instalado: pip install mss")
        print("2. Verifica que tengas permisos de captura de pantalla")
        exit(1)
    
    # Guardar captura para análisis
    cal_dir = "debug/calibration"
    os.makedirs(cal_dir, exist_ok=True)
    
    capture_path = os.path.join(cal_dir, "detector_calibration.png")
    cv2.imwrite(capture_path, screenshot)
    print(f"✅ Captura guardada: {capture_path}")
    
    height, width = screenshot.shape[:2]
    print(f"📏 Resolución: {width}x{height}px")
    
    print("\n🔍 Analizando colores en la imagen...")
    
    # Convertir a HSV
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    
    # Analizar distribución de colores
    print("📊 Analizando histograma de colores...")
    
    # Calcular histograma de Hue (tono)
    hist_h = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    
    # Encontrar picos en el histograma (colores dominantes)
    peaks = []
    peak_values = []
    
    for i in range(1, 179):
        if hist_h[i] > hist_h[i-1] and hist_h[i] > hist_h[i+1]:
            if hist_h[i] > 1000:  # Umbral mínimo para considerar pico
                peaks.append(i)
                peak_values.append(float(hist_h[i][0]))  # 🔥 CORRECCIÓN: hist_h[i][0]
    
    print(f"   Picos de color encontrados: {peaks}")
    
    # Mostrar los 5 picos más altos
    if peaks:
        sorted_indices = np.argsort(peak_values)[::-1][:5]  # Índices de los 5 mayores
        top_peaks = [peaks[i] for i in sorted_indices]
        print(f"   Top 5 picos: {top_peaks}")
    
    # Buscar verdes (HUE ~35-85 en OpenCV)
    green_peaks = [p for p in peaks if 35 <= p <= 85]
    
    if green_peaks:
        print(f"   ✅ Picos verdes encontrados: {green_peaks}")
        
        # Calcular estadísticas de verde
        green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
        green_pixels = cv2.countNonZero(green_mask)
        total_pixels = height * width
        green_percent = (green_pixels / total_pixels) * 100
        
        print(f"\n📈 ESTADÍSTICAS DE VERDE:")
        print(f"   Píxeles verdes: {green_pixels:,}")
        print(f"   Total píxeles: {total_pixels:,}")
        print(f"   Porcentaje verde: {green_percent:.2f}%")
        
        # Probar detección con detector actual
        print("\n🧪 Probando detección con detector actual...")
        current_detection = detector.detect(screenshot)
        print(f"   Detección actual: {'✅' if current_detection else '❌'}")
        
        # Crear máscara visual para debug
        test_mask = green_mask.copy()
        
        # Aplicar máscara a la imagen original
        masked_img = cv2.bitwise_and(screenshot, screenshot, mask=test_mask)
        
        # Guardar imagen con máscara
        mask_path = os.path.join(cal_dir, "green_mask.png")
        cv2.imwrite(mask_path, masked_img)
        print(f"💾 Máscara de verde guardada: {mask_path}")
        
        # Crear imagen con histograma
        create_histogram_image(hist_h, cal_dir)  # 🔥 CORRECCIÓN: Sin self
        
        # Recomendación basada en porcentaje de verde
        print("\n🎯 DIAGNÓSTICO:")
        
        if green_percent < 0.5:
            print("   ❌ MUY POCO VERDE (<0.5%)")
            print("   Posibles causas:")
            print("   1. PokerStars no está visible/abierto")
            print("   2. Estás usando tema OSCURO de PokerStars")
            print("   3. La captura es del escritorio, no de PokerStars")
            print("\n   🔧 SOLUCIÓN:")
            print("   - Abre PokerStars en una mesa")
            print("   - Usa el tema CLÁSICO (verde)")
            print("   - Asegúrate de que la mesa sea visible")
            
        elif green_percent < 3.0:
            print(f"   ⚠️  POCO VERDE ({green_percent:.1f}%)")
            print("   El detector puede tener problemas.")
            print("\n   🔧 RECOMENDACIÓN:")
            print("   1. Bajar el umbral en table_detector.py")
            print("   2. Cambiar a tema más verde en PokerStars")
            print("   3. Ajustar rangos de color manualmente")
            
        elif green_percent < 10.0:
            print(f"   📊 VERDE MODERADO ({green_percent:.1f}%)")
            print("   El detector debería funcionar con ajustes.")
            print("\n   🔧 AJUSTE RECOMENDADO:")
            print("   En table_detector.py, cambiar:")
            print("   green_threshold = 0.015  →  green_threshold = 0.008")
            
        else:
            print(f"   ✅ SUFICIENTE VERDE ({green_percent:.1f}%)")
            print("   ¡El detector debería funcionar bien!")
            print("\n   Si aún no detecta, prueba:")
            print("   1. Aumentar min_green_area")
            print("   2. Ajustar rangos de color")
        
        # Crear archivo de configuración
        config = {
            "calibration_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "screen_resolution": f"{width}x{height}",
            "detected_green_percent": green_percent,
            "green_pixels": int(green_pixels),
            "total_pixels": int(total_pixels),
            "green_peaks_found": green_peaks,
            "current_threshold": 0.015,
            "recommended_threshold": max(0.005, green_percent / 2000),  # Auto-cálculo
            "notes": "Ajustar green_threshold en table_detector.py si es necesario"
        }
        
        config_path = os.path.join(cal_dir, "detector_config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n💾 Configuración guardada: {config_path}")
        
        # Mostrar ajuste automático sugerido
        rec_threshold = config["recommended_threshold"]
        print(f"\n🔧 AJUSTE AUTOMÁTICO SUGERIDO:")
        print(f"   En table_detector.py, línea ~25, cambiar:")
        print(f"   self.green_threshold = 0.015")
        print(f"   Por:")
        print(f"   self.green_threshold = {rec_threshold:.4f}  # Ajustado automáticamente")
        
    else:
        print("❌ No se encontraron picos verdes en la imagen")
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("1. PokerStars NO está visible en la captura")
        print("2. Estás usando un tema NO VERDE (oscuro/azul)")
        print("3. La captura falló o es del escritorio")
        
        # Crear imagen de la captura para diagnóstico
        print("\n📷 REVISIÓN DE CAPTURA:")
        print("   Abre: debug/calibration/detector_calibration.png")
        print("   ¿Ves PokerStars con mesa verde en la imagen?")
        
        # Verificar contenido de la imagen
        print("\n🔍 Análisis de contenido de imagen:")
        avg_color = np.mean(screenshot, axis=(0, 1))
        print(f"   Color promedio: B={avg_color[0]:.0f}, G={avg_color[1]:.0f}, R={avg_color[2]:.0f}")
        
        if avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
            print("   ✅ Predominio de verde detectado en promedio")
        else:
            print("   ❌ NO hay predominio de verde")
    
    print("\n" + "=" * 60)
    print("🎯 CALIBRACIÓN COMPLETADA")
    print("\n📝 SIGUIENTES PASOS:")
    print("1. Revisa las imágenes en debug/calibration/")
    print("2. Ajusta table_detector.py si es necesario")
    print("3. Ejecuta: python run_pokerstars_optimized.py")
    print("=" * 60)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n🔧 Verifica que tengas instalado:")
    print("   pip install opencv-python numpy")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()