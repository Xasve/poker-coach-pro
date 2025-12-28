# card_classifier.py - VERSIÓN MEJORADA PARA ENCONTRAR SESIONES
import cv2
import numpy as np
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Importar condicionalmente
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class CardClassifier:
    """Clasificador automático de cartas - VERSIÓN MEJORADA"""
    
    def __init__(self, data_path="data/card_templates/auto_captured"):
        self.data_path = data_path
        self.sessions = self.find_sessions_improved()
        
        # Mapeo de palos
        self.suit_colors = {
            'hearts': 'red',
            'diamonds': 'red',  
            'clubs': 'black',
            'spades': 'black'
        }
        
        print(f" Clasificador inicializado: {len(self.sessions)} sesiones encontradas")
    
    def find_sessions_improved(self):
        """Encontrar sesiones - VERSIÓN MEJORADA"""
        sessions = []
        
        if not os.path.exists(self.data_path):
            print(f"  Carpeta no existe: {self.data_path}")
            return sessions
        
        # Buscar todas las carpetas que parezcan sesiones (formato YYYYMMDD_HHMMSS)
        for item in sorted(os.listdir(self.data_path), reverse=True):  # Más recientes primero
            session_path = os.path.join(self.data_path, item)
            
            if os.path.isdir(session_path):
                # Verificar si tiene la estructura esperada
                has_raw_captures = os.path.exists(os.path.join(session_path, "raw_captures"))
                has_session_info = os.path.exists(os.path.join(session_path, "session_info.json"))
                
                # Contar imágenes
                raw_path = os.path.join(session_path, "raw_captures")
                card_count = 0
                if os.path.exists(raw_path):
                    card_count = len([f for f in os.listdir(raw_path) 
                                    if f.endswith('.png')])
                
                # Solo considerar si tiene imágenes
                if card_count > 0 or has_session_info:
                    sessions.append({
                        "id": item,
                        "path": session_path,
                        "raw_captures": raw_path,
                        "card_count": card_count,
                        "has_session_info": has_session_info,
                        "is_valid": card_count > 0
                    })
        
        return sessions
    
    def get_session_by_id(self, session_id):
        """Obtener sesión por ID - MÉTODO MEJORADO"""
        for session in self.sessions:
            if session["id"] == session_id:
                return session
        
        # Intentar buscar directamente en disco
        session_path = os.path.join(self.data_path, session_id)
        if os.path.exists(session_path):
            # Contar imágenes
            raw_path = os.path.join(session_path, "raw_captures")
            card_count = 0
            if os.path.exists(raw_path):
                card_count = len([f for f in os.listdir(raw_path) 
                                if f.endswith('.png')])
            
            session_info = {
                "id": session_id,
                "path": session_path,
                "raw_captures": raw_path,
                "card_count": card_count,
                "has_session_info": os.path.exists(os.path.join(session_path, "session_info.json")),
                "is_valid": card_count > 0
            }
            
            # Agregar a la lista
            self.sessions.append(session_info)
            self.sessions.sort(key=lambda x: x["id"], reverse=True)  # Ordenar
        
            return session_info
        
        return None
    
    def load_captured_cards(self, session_path):
        """Cargar cartas capturadas de una sesión"""
        cards = []
        raw_path = os.path.join(session_path, "raw_captures")
        
        if not os.path.exists(raw_path):
            print(f"❌ No hay carpeta raw_captures en: {session_path}")
            return cards
        
        # Obtener lista de archivos PNG
        png_files = [f for f in os.listdir(raw_path) if f.endswith('.png')]
        
        if not png_files:
            print(f"📭 No hay imágenes PNG en: {raw_path}")
            return cards
        
        print(f" Cargando {len(png_files)} imágenes...")
        
        for i, filename in enumerate(png_files[:100]):  # Limitar a 100 imágenes para performance
            if i % 10 == 0:
                print(f"   Cargando... {i}/{min(len(png_files), 100)}", end='\r')
            
            img_path = os.path.join(raw_path, filename)
            json_path = img_path.replace('.png', '.json')
            
            # Cargar imagen
            img = cv2.imread(img_path)
            if img is None:
                continue
            
            # Cargar metadatos si existen
            metadata = {}
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r') as f:
                        metadata = json.load(f)
                except:
                    metadata = {"filename": filename}
            else:
                metadata = {"filename": filename}
            
            cards.append({
                "image": img,
                "path": img_path,
                "metadata": metadata,
                "filename": filename
            })
        
        print(f"\n {len(cards)} imágenes cargadas correctamente")
        return cards
    
    def extract_color_features(self, image):
        """Extraer características de color simplificadas"""
        if image is None or image.size == 0:
            return None
        
        # Convertir a diferentes espacios de color
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detectar rojo (dos rangos)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Contar píxeles
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = image.shape[0] * image.shape[1]
        red_ratio = red_pixels / total_pixels if total_pixels > 0 else 0
        
        # Características básicas
        mean_color = np.mean(image, axis=(0, 1))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        
        return {
            "red_ratio": float(red_ratio),
            "brightness": float(brightness),
            "mean_r": float(mean_color[2]),
            "mean_g": float(mean_color[1]),
            "mean_b": float(mean_color[0]),
            "is_red_suit": red_ratio > 0.05
        }
    
    def classify_suit_simple(self, image):
        """Clasificación simple de palo"""
        features = self.extract_color_features(image)
        
        if features is None:
            return "unknown", 0.5
        
        if features["is_red_suit"]:
            # Diferenciar corazones vs diamantes
            if features["brightness"] > 120:
                return "hearts", min(0.8, features["red_ratio"] * 2)
            else:
                return "diamonds", min(0.8, features["red_ratio"] * 2)
        else:
            # Tréboles vs picas
            if features["brightness"] > 100:
                return "clubs", 0.7
            else:
                return "spades", 0.7
    
    def auto_classify_session(self, session_id):
        """Clasificar automáticamente una sesión - VERSIÓN MEJORADA"""
        print(f"\n CLASIFICANDO SESIÓN: {session_id}")
        
        # Buscar sesión
        session = self.get_session_by_id(session_id)
        
        if not session:
            print(f" Sesión no encontrada: {session_id}")
            print(f" Buscando en: {self.data_path}")
            
            # Listar sesiones disponibles
            print("\n SESIONES DISPONIBLES:")
            available = self.find_sessions_improved()
            for s in available[:5]:  # Mostrar primeras 5
                print(f"    {s['id']} ({s['card_count']} imágenes)")
            
            if len(available) > 5:
                print(f"   ... y {len(available) - 5} más")
            
            return None
        
        if session["card_count"] == 0:
            print(f" Sesión vacía: {session_id}")
            return None
        
        print(f" Cargando {session['card_count']} imágenes...")
        
        # Cargar cartas
        cards = self.load_captured_cards(session["path"])
        
        if not cards:
            print(" No se pudieron cargar imágenes")
            return None
        
        print(f"\n Procesando {len(cards)} cartas...")
        
        # Clasificar cada carta
        results = []
        suits_count = {
            "hearts": 0,
            "diamonds": 0,
            "clubs": 0,
            "spades": 0,
            "unknown": 0
        }
        
        for i, card in enumerate(cards):
            if i % 5 == 0:
                print(f"   Procesando carta {i+1}/{len(cards)}...", end='\r')
            
            # Clasificar
            suit, confidence = self.classify_suit_simple(card["image"])
            
            # Actualizar contadores
            suits_count[suit] = suits_count.get(suit, 0) + 1
            
            # Crear resultado
            result = {
                "filename": card["filename"],
                "suit": suit,
                "value": "unknown",  # Por ahora
                "confidence": confidence,
                "features": self.extract_color_features(card["image"])
            }
            
            results.append(result)
            
            # Mover a carpeta correspondiente
            self.move_to_classified_folder(card, suit, session_id)
        
        print(f"\n Clasificación completada: {len(results)} cartas procesadas")
        
        # Mostrar estadísticas
        print("\n DISTRIBUCIÓN DE PALOS:")
        total = len(results)
        for suit, count in suits_count.items():
            if count > 0:
                percentage = (count / total) * 100
                print(f"   {suit.upper():10} {count:3} ({percentage:.1f}%)")
        
        # Guardar resultados
        self.save_classification_results(results, session["path"])
        
        return results
    
    def move_to_classified_folder(self, card, suit, session_id):
        """Mover carta clasificada a carpeta correspondiente"""
        try:
            # Carpeta destino en pokerstars_real
            dest_base = "data/card_templates/pokerstars_real"
            dest_folder = os.path.join(dest_base, suit)
            
            # Crear carpeta si no existe
            os.makedirs(dest_folder, exist_ok=True)
            
            # Nuevo nombre con sesión
            new_filename = f"{session_id}_{suit}_{card['filename']}"
            dest_path = os.path.join(dest_folder, new_filename)
            
            # Copiar archivo (no mover, por si acaso)
            shutil.copy2(card["path"], dest_path)
            
            # También copiar metadata si existe
            metadata_src = card["path"].replace('.png', '.json')
            metadata_dest = dest_path.replace('.png', '.json')
            
            if os.path.exists(metadata_src):
                shutil.copy2(metadata_src, metadata_dest)
            
            return True
            
        except Exception as e:
            print(f"  Error moviendo {card['filename']}: {e}")
            return False
    
    def save_classification_results(self, results, session_path):
        """Guardar resultados de clasificación"""
        output_path = os.path.join(session_path, "classification_results.json")
        
        # Resumen estadístico
        suits_summary = {}
        for result in results:
            suit = result["suit"]
            suits_summary[suit] = suits_summary.get(suit, 0) + 1
        
        summary = {
            "session_path": session_path,
            "classification_date": datetime.now().isoformat(),
            "total_cards": len(results),
            "suits_distribution": suits_summary,
            "sample_cards": results[:10]  # Solo guardar muestra
        }
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f" Resultados guardados: {output_path}")
        
        return output_path
    
    def get_latest_session(self):
        """Obtener la sesión más reciente"""
        if not self.sessions:
            return None
        
        # Ordenar por ID (el más reciente primero)
        valid_sessions = [s for s in self.sessions if s["card_count"] > 0]
        if not valid_sessions:
            return None
        
        return valid_sessions[0]

# Función principal mejorada
def main():
    """Función principal del clasificador"""
    print(" CLASIFICADOR DE CARTAS - VERSIÓN MEJORADA")
    print("=" * 70)
    
    classifier = CardClassifier()
    
    if not classifier.sessions:
        print(" No hay sesiones de captura disponibles")
        print(f" Busca en: {classifier.data_path}")
        print("\n Primero ejecuta el capturador automático")
        return
    
    print(f" Sesiones encontradas: {len(classifier.sessions)}")
    
    # Mostrar sesiones con imágenes
    valid_sessions = [s for s in classifier.sessions if s["card_count"] > 0]
    
    if not valid_sessions:
        print(" No hay sesiones con imágenes para clasificar")
        return
    
    print(f"\n SESIONES CON IMÁGENES ({len(valid_sessions)}):")
    for i, session in enumerate(valid_sessions[:10], 1):
        print(f"   {i}. {session['id']} - {session['card_count']} imágenes")
    
    if len(valid_sessions) > 10:
        print(f"   ... y {len(valid_sessions) - 10} más")
    
    try:
        choice = input("\n Número de sesión, 'ultima', o 'todas': ")
        
        if choice.lower() == 'ultima':
            latest = classifier.get_latest_session()
            if latest:
                classifier.auto_classify_session(latest["id"])
            else:
                print(" No hay sesiones válidas")
        
        elif choice.lower() == 'todas':
            for session in valid_sessions:
                print(f"\n{'='*50}")
                classifier.auto_classify_session(session["id"])
        
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(valid_sessions):
                session_id = valid_sessions[idx]["id"]
                classifier.auto_classify_session(session_id)
            else:
                print(" Número fuera de rango")
        
        else:
            print(" Opción no válida")
    
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    main()
