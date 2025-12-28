#!/usr/bin/env python3
"""
Limpieza de archivos duplicados en Poker Coach Pro
Mantiene solo los esenciales
"""
import os
import shutil

def main():
    print("=" * 60)
    print("🧹 LIMPIEZA DE ARCHIVOS DUPLICADOS")
    print("=" * 60)
    
    # Archivos a MANTENER (esenciales)
    keep_files = {
        "poker_coach_pro.py",      # NUEVO script principal
        "requirements.txt",
        "README.md",
        "test_pokerstars.py",
        "test_ggpoker_simple.py",
        "test_capture.py",
        "test_components.py",
        "check.py",
        "cleanup.py",              # Este archivo
        "setup_folders.py"
    }
    
    # Archivos a ELIMINAR (duplicados/confusos)
    remove_files = [
        # Versiones antiguas/duplicadas del coach
        "definitive_poker_coach.py",
        "definitive_poker_coach_fixed.py",
        "emergency_coach.py",
        "final_poker_coach.py",
        "hybrid_coach.py",
        "minimal_coach.py",
        "poker_coach.py",
        "poker_coach_complete.py",
        "poker_coach_simple.py",
        "poker_coach_simple_quality.py",
        "poker_coach_with_quality.py",
        "pokerstars_coach.py",
        "pokerstars_pro_coach.py",
        "pokerstars_pro_coach_fixed.py",
        "stable_poker_coach.py",
        "start_coach.py",
        "start_coach_pro.py",
        "start_full_coach.py",
        "start_pokerstars.py",
        "run_coach.py",
        "run_simple_coach.py",
        
        # Fixers duplicados
        "apply_patches.py",
        "fix_all.py",
        "fix_all_problems.py",
        "fix_imports.py",
        "ultimate_fix.py",
        
        # Tests duplicados
        "test_adaptive.py",
        "test_pokerstars_fixed.py",
        "test_quality.py",
        "test_quality_fixed.py",
        "quick_quality_check.py",
        
        # Otros
        "install_pokerstars.py",
        "verify_structure.py",
        "main.py",
        "list_files.py",
        "create_system.py"
    ]
    
    print("\n📁 Archivos a ELIMINAR (duplicados):")
    deleted_count = 0
    skipped_count = 0
    
    for filename in remove_files:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"✅ Eliminado: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {filename}: {e}")
                skipped_count += 1
        else:
            skipped_count += 1
    
    print("\n📁 Archivos a MANTENER (esenciales):")
    for filename in sorted(keep_files):
        if os.path.exists(filename):
            print(f"✅ Mantenido: {filename}")
        else:
            print(f"⚠️  No existe: {filename}")
    
    # Crear instrucciones
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES ACTUALIZADAS")
    print("=" * 60)
    
    print("\n🎯 SCRIPT PRINCIPAL: poker_coach_pro.py")
    print("\n🚀 PARA USAR EL SISTEMA:")
    print("   1. Abre una terminal en esta carpeta")
    print("   2. Ejecuta: python poker_coach_pro.py")
    print("   3. Selecciona una opción del menú")
    
    print("\n🔧 TESTS DISPONIBLES:")
    print("   • test_pokerstars.py - Probar PokerStars")
    print("   • test_ggpoker_simple.py - Probar GG Poker")
    print("   • test_capture.py - Probar captura de pantalla")
    
    print(f"\n📊 RESUMEN:")
    print(f"   • Archivos eliminados: {deleted_count}")
    print(f"   • Archivos saltados: {skipped_count}")
    print(f"   • Archivos mantenidos: {len(keep_files)}")
    
    print("\n✅ Limpieza completada")
    print("=" * 60)

if __name__ == "__main__":
    main()