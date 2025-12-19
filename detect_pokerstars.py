import mss
import cv2
import numpy as np
import os

print(" BUSCANDO POKERSTARS EN PANTALLA...")
print("=" * 50)

with mss.mss() as sct:
    # Capturar pantalla completa
    monitor = sct.monitors[1]
    screenshot = sct.grab(monitor)
    
    # Convertir a numpy array
    img = np.array(screenshot)
    
    print(f" Resolución capturada: {img.shape[1]}x{img.shape[0]}")
    
    # Guardar captura para análisis
    os.makedirs("debug", exist_ok=True)
    cv2.imwrite("debug/full_screen.jpg", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
    print(" Captura guardada: debug/full_screen.jpg")
    
    # Buscar colores de PokerStars (verde)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Rango de verde (mesas de poker)
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Contar píxeles verdes
    green_pixels = np.sum(mask > 0)
    total_pixels = mask.shape[0] * mask.shape[1]
    green_percentage = (green_pixels / total_pixels) * 100
    
    print(f"\n ANÁLISIS DE COLORES:")
    print(f"   Píxeles verdes: {green_pixels:,}")
    print(f"   Porcentaje verde: {green_percentage:.2f}%")
    
    if green_pixels > 10000:
        print(" COLOR VERDE DETECTADO! (Posible mesa de PokerStars)")
        
        # Encontrar contornos de áreas verdes
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Encontrar el contorno más grande
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            print(f"\n POSIBLE MESA DETECTADA:")
            print(f"   Coordenadas: X={x}, Y={y}")
            print(f"   Tamaño: {w}x{h} píxeles")
            print(f"   Área: {w*h:,} píxeles")
            
            # Dibujar rectángulo en la captura
            img_with_box = img.copy()
            cv2.rectangle(img_with_box, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.imwrite("debug/pokerstars_detected.jpg", cv2.cvtColor(img_with_box, cv2.COLOR_BGRA2BGR))
            print("    Imagen con detección: debug/pokerstars_detected.jpg")
            
            print("\n INSTRUCCIÓN: Usa estas coordenadas en tu configuración:")
            print(f"   region = [{x}, {y}, {w}, {h}]")
    else:
        print(" NO SE DETECTÓ SUFICIENTE COLOR VERDE")
        print("\n RAZONES POSIBLES:")
        print("   1. PokerStars no está abierto")
        print("   2. La mesa está en otro color (modo nocturno?)")
        print("   3. La ventana está minimizada o detrás de otras")
    
    print("\n" + "=" * 50)
    print(" PRÓXIMOS PASOS:")
    print("   1. Abre PokerStars en una mesa de poker")
    print("   2. Ejecuta este script nuevamente")
    print("   3. Si detecta verde, actualiza las coordenadas")
