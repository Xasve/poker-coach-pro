# card_classifier.py - Clasificador automático de cartas
import cv2
import numpy as np
import os
import json
import shutil
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class CardClassifier:
    """Clasificador automático de cartas usando machine learning"""
    
    def __init__(self, data_path="data/card_templates/auto_captured"):
        self.data_path = data_path
        self.sessions = self.find_sessions()
        
        # Mapeo de palos por color
        self.suit_colors = {
            'hearts': 'red',     # Corazones - rojo
            'diamonds': 'red',   # Diamantes - rojo  
            'clubs': 'black',    # Tréboles - negro
            'spades': 'black'    # Picas - negro
        }
        
        # Valores de cartas
        self.card_values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    
    def find_sessions(self):
        """Encontrar todas las sesiones de captura"""
        sessions = []
        if os.path.exists(self.data_path):
            for item in os.listdir(self.data_path):
                session_path = os.path.join(self.data_path, item)
                if os.path.isdir(session_path):
                    sessions.append({
                        "id": item,
                        "path": session_path,
                        "raw_captures": os.path.join(session_path, "raw_captures")
                    })
        
        print(f" Sesiones encontradas: {len(sessions)}")
        return sessions
    
    def load_captured_cards(self, session_path):
        """Cargar cartas capturadas de una sesión"""
        cards = []
        raw_path = os.path.join(session_path, "raw_captures")
        
        if not os.path.exists(raw_path):
            print(f" No hay capturas en: {raw_path}")
            return cards
        
        for file in os.listdir(raw_path):
            if file.endswith('.png'):
                img_path = os.path.join(raw_path, file)
                json_path = img_path.replace('.png', '.json')
                
                img = cv2.imread(img_path)
                metadata = {}
                
                if os.path.exists(json_path):
                    with open(json_path, 'r') as f:
                        metadata = json.load(f)
                
                if img is not None:
                    cards.append({
                        "image": img,
                        "path": img_path,
                        "metadata": metadata,
                        "filename": file
                    })
        
        print(f"    Cartas cargadas: {len(cards)}")
        return cards
    
    def extract_color_features(self, image):
        """Extraer características de color para clasificar palos"""
        if image is None or image.size == 0:
            return None
        
        # Convertir a diferentes espacios de color
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Definir rangos para rojo (dos rangos por la naturaleza circular de HSV)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Máscaras para rojo
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        # Contar píxeles rojos
        red_pixels = cv2.countNonZero(mask_red)
        total_pixels = image.shape[0] * image.shape[1]
        red_ratio = red_pixels / total_pixels if total_pixels > 0 else 0
        
        # Características de color
        mean_color = np.mean(image, axis=(0, 1))
        std_color = np.std(image, axis=(0, 1))
        
        features = {
            "red_ratio": float(red_ratio),
            "mean_b": float(mean_color[0]),
            "mean_g": float(mean_color[1]),
            "mean_r": float(mean_color[2]),
            "std_b": float(std_color[0]),
            "std_g": float(std_color[1]),
            "std_r": float(std_color[2]),
            "is_red_suit": red_ratio > 0.05  # Umbral para considerar rojo
        }
        
        return features
    
    def extract_shape_features(self, image):
        """Extraer características de forma para clasificar valores"""
        if image is None:
            return None
        
        # Convertir a escala de grises y binarizar
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Tomar el contorno más grande
        main_contour = max(contours, key=cv2.contourArea)
        
        # Momentos de Hu (invariantes a escala, rotación, traslación)
        moments = cv2.moments(main_contour)
        hu_moments = cv2.HuMoments(moments).flatten()
        
        # Otras características geométricas
        area = cv2.contourArea(main_contour)
        perimeter = cv2.arcLength(main_contour, True)
        x, y, w, h = cv2.boundingRect(main_contour)
        
        features = {
            "area": float(area),
            "perimeter": float(perimeter),
            "aspect_ratio": float(w / h) if h > 0 else 0,
            "compactness": (perimeter ** 2) / (4 * np.pi * area) if area > 0 else 0,
            "hu_moments": [float(m) for m in hu_moments]
        }
        
        return features
    
    def classify_suit_by_color(self, image):
        """Clasificar palo basado en color"""
        color_features = self.extract_color_features(image)
        
        if color_features is None:
            return "unknown"
        
        if color_features["is_red_suit"]:
            # Diferenciar entre corazones y diamantes
            # Los corazones suelen tener más variación en el canal rojo
            red_std = color_features["std_r"]
            if red_std > 30:
                return "hearts"
            else:
                return "diamonds"
        else:
            # Diferenciar entre tréboles y picas
            # Los tréboles suelen ser más claros
            mean_brightness = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
            if mean_brightness > 100:
                return "clubs"
            else:
                return "spades"
    
    def auto_classify_session(self, session_id):
        """Clasificar automáticamente todas las cartas de una sesión"""
        session = next((s for s in self.sessions if s["id"] == session_id), None)
        
        if not session:
            print(f"❌ Sesión no encontrada: {session_id}")
            return
        
        print(f"\n🎯 CLASIFICANDO SESIÓN: {session_id}")
        
        # Cargar cartas
        cards = self.load_captured_cards(session["path"])
        
        if not cards:
            print("❌ No hay cartas para clasificar")
            return
        
        # Clasificar cada carta
        classification_results = []
        
        for i, card in enumerate(cards):
            print(f"   Procesando carta {i+1}/{len(cards)}...", end='\r')
            
            # Clasificar palo
            suit = self.classify_suit_by_color(card["image"])
            
            # Por ahora, valor desconocido (requeriría OCR)
            value = "unknown"
            
            # Crear estructura de clasificación
            classification = {
                "filename": card["filename"],
                "suit": suit,
                "value": value,
                "confidence": 0.7,  # Confianza aproximada
                "features": {
                    "color": self.extract_color_features(card["image"]),
                    "shape": self.extract_shape_features(card["image"])
                }
            }
            
            classification_results.append(classification)
            
            # Mover a carpeta correspondiente
            self.move_to_classified_folder(card, suit, value, session["path"])
        
        print(f"\n✅ Clasificación completada: {len(classification_results)} cartas")
        
        # Guardar resultados
        self.save_classification_results(classification_results, session["path"])
        
        return classification_results
    
    def move_to_classified_folder(self, card, suit, value, session_path):
        """Mover carta clasificada a carpeta correspondiente"""
        # Carpeta destino
        if value != "unknown":
            dest_folder = os.path.join("data/card_templates/pokerstars_real", 
                                      suit, value)
        else:
            dest_folder = os.path.join("data/card_templates/pokerstars_real", 
                                      suit, "unknown")
        
        os.makedirs(dest_folder, exist_ok=True)
        
        # Nuevo nombre de archivo
        new_filename = f"{value}_{suit}_{card['filename']}"
        dest_path = os.path.join(dest_folder, new_filename)
        
        # Copiar archivo
        shutil.copy2(card["path"], dest_path)
        
        # Copiar metadata si existe
        metadata_src = card["path"].replace('.png', '.json')
        metadata_dest = dest_path.replace('.png', '.json')
        
        if os.path.exists(metadata_src):
            shutil.copy2(metadata_src, metadata_dest)
    
    def save_classification_results(self, results, session_path):
        """Guardar resultados de clasificación"""
        output_path = os.path.join(session_path, "classification_results.json")
        
        with open(output_path, 'w') as f:
            json.dump({
                "total_cards": len(results),
                "classification_date": str(datetime.now()),
                "cards": results
            }, f, indent=2)
        
        print(f" Resultados guardados en: {output_path}")
        return output_path
    
    def generate_clustering_report(self, session_id):
        """Generar reporte visual de clustering de cartas"""
        session = next((s for s in self.sessions if s["id"] == session_id), None)
        
        if not session:
            return
        
        cards = self.load_captured_cards(session["path"])
        
        if len(cards) < 10:
            print(" No hay suficientes cartas para clustering")
            return
        
        # Extraer características
        features = []
        for card in cards:
            color_feat = self.extract_color_features(card["image"])
            if color_feat:
                features.append([
                    color_feat["red_ratio"],
                    color_feat["mean_r"],
                    color_feat["mean_g"],
                    color_feat["mean_b"]
                ])
        
        if len(features) < 10:
            return
        
        # Aplicar PCA para visualización
        pca = PCA(n_components=2)
        features_pca = pca.fit_transform(features)
        
        # Aplicar K-Means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(features)
        
        # Visualizar
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(features_pca[:, 0], features_pca[:, 1], 
                            c=clusters, cmap='viridis', s=100, alpha=0.7)
        
        plt.title(f'Clustering de Cartas - Sesión {session_id}')
        plt.xlabel('Componente Principal 1')
        plt.ylabel('Componente Principal 2')
        plt.colorbar(scatter, label='Cluster')
        
        # Guardar gráfico
        plot_path = os.path.join(session["path"], "clustering_plot.png")
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f" Gráfico de clustering guardado: {plot_path}")
        
        return plot_path

# Función principal
def main():
    """Función principal del clasificador"""
    print(" CLASIFICADOR AUTOMÁTICO DE CARTAS")
    print("=" * 60)
    
    classifier = CardClassifier()
    
    if not classifier.sessions:
        print(" No hay sesiones de captura disponibles")
        print("   Ejecuta primero el capturador automático")
        return
    
    print(" Sesiones disponibles:")
    for i, session in enumerate(classifier.sessions):
        print(f"   {i+1}. {session['id']}")
    
    try:
        choice = int(input("\nSelecciona una sesión (número): "))
        if 1 <= choice <= len(classifier.sessions):
            session_id = classifier.sessions[choice-1]["id"]
            classifier.auto_classify_session(session_id)
            classifier.generate_clustering_report(session_id)
        else:
            print(" Selección inválida")
    except ValueError:
        print(" Entrada inválida")

if __name__ == "__main__":
    main()
