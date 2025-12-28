import os
import shutil
from pathlib import Path

def prune_excess_spades():
    """Eliminar templates excesivos de spades manteniendo los mejores"""
    print(" PODA DE TEMPLATES EXCESIVOS DE SPADES")
    print("=" * 60)
    
    spades_path = "data/card_templates/pokerstars_real/spades"
    
    if not os.path.exists(spades_path):
        print(" No hay carpeta de spades")
        return
    
    files = [f for f in os.listdir(spades_path) if f.endswith(('.png', '.jpg'))]
    current_count = len(files)
    
    print(f" Estado actual:")
    print(f"   Templates spades: {current_count}")
    print(f"   Meta ideal: 40")
    print(f"   Exceso: {current_count - 40}")
    
    if current_count <= 40:
        print("\n No hay exceso, manteniendo todos")
        return
    
    to_remove = current_count - 40
    
    print(f"\n  Eliminando {to_remove} templates...")
    print(" Se mantendrán los más recientes y claros")
    
    # Ordenar por fecha (los más recientes primero)
    files_with_mtime = []
    for file in files:
        path = os.path.join(spades_path, file)
        mtime = os.path.getmtime(path)
        files_with_mtime.append((file, mtime))
    
    # Ordenar por antigüedad (los más antiguos primero para eliminar)
    files_with_mtime.sort(key=lambda x: x[1])
    
    # Crear carpeta de backup
    backup_path = "data/card_templates/backup_spades"
    os.makedirs(backup_path, exist_ok=True)
    
    # Mover los más antiguos a backup
    removed = 0
    for file, _ in files_with_mtime[:to_remove]:
        src = os.path.join(spades_path, file)
        dst = os.path.join(backup_path, file)
        
        # Mover a backup
        shutil.move(src, dst)
        
        # También mover metadata si existe
        metadata_src = src.replace('.png', '.json').replace('.jpg', '.json')
        if os.path.exists(metadata_src):
            metadata_dst = dst.replace('.png', '.json').replace('.jpg', '.json')
            shutil.move(metadata_src, metadata_dst)
        
        removed += 1
        if removed % 10 == 0:
            print(f"   Movidos: {removed}/{to_remove}")
    
    print(f"\n {removed} templates movidos a backup:")
    print(f"    {backup_path}")
    
    # Contar nuevo total
    remaining = len([f for f in os.listdir(spades_path) if f.endswith(('.png', '.jpg'))])
    print(f"    Spades restantes: {remaining}")

if __name__ == "__main__":
    prune_excess_spades()
    print("\n Recuerda capturar más cartas rojas () y tréboles ()")
