#!/usr/bin/env python3
"""
ANÁLISIS PARA BOT PROFESIONAL - Poker Coach Pro
Ejecutar: python analyze_for_bot.py
"""

import ast
import os
import json
from pathlib import Path

print("🔍 ANÁLISIS PROFUNDO DE MÓDULOS PARA BOT PROFESIONAL")
print("=" * 70)

# Módulos a analizar
MODULES_TO_ANALYZE = [
    ("core/card_recognizer.py", ["PokerStarsCardDetector", "GTOAnalyzer", "Card"]),
    ("core/learning_system.py", ["PokerCoachProCompleteSystem"]),
    ("integration/pokerstars_assistant.py", []),
    ("integration/pokerstars_calibrator_fixed.py", ["PokerStarsCalibratorSimple"]),
]

def analyze_file(filepath, expected_classes):
    """Analiza un archivo Python en profundidad."""
    print(f"\n📄 {filepath}:")
    
    if not os.path.exists(filepath):
        print("   ❌ NO EXISTE")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Analizar estructura AST
        tree = ast.parse(content)
        
        # Encontrar todas las clases y métodos
        classes_info = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                methods = []
                
                for subnode in node.body:
                    if isinstance(subnode, ast.FunctionDef):
                        methods.append(subnode.name)
                
                classes_info.append({
                    "name": class_name,
                    "methods": methods,
                    "line": node.lineno
                })
        
        if classes_info:
            print(f"   📦 CLASES ENCONTRADAS ({len(classes_info)}):")
            for cls in classes_info:
                print(f"      • {cls['name']} (línea {cls['line']})")
                if cls["methods"]:
                    print(f"        Métodos: {', '.join(cls['methods'][:4])}")
                    if len(cls["methods"]) > 4:
                        print(f"          ... y {len(cls['methods']) - 4} más")
        else:
            print("   ⚠️  No se encontraron clases definidas")
        
        # Verificar clases esperadas
        found_classes = [cls["name"] for cls in classes_info]
        for expected in expected_classes:
            if expected in found_classes:
                print(f"   ✅ {expected} DISPONIBLE")
            else:
                print(f"   ❌ {expected} NO ENCONTRADO")
        
        # Encontrar funciones importantes
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not isinstance(node.parent, ast.ClassDef):
                functions.append({
                    "name": node.name,
                    "line": node.lineno
                })
        
        if functions:
            print(f"   🔧 FUNCIONES ({len(functions)}):")
            for func in functions[:6]:
                print(f"      • {func['name']}() (línea {func['line']})")
            if len(functions) > 6:
                print(f"        ... y {len(functions) - 6} más")
        
        # Mostrar líneas clave
        lines = content.split('\n')
        print(f"   📊 ESTADÍSTICAS:")
        print(f"      Líneas totales: {len(lines)}")
        
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        print(f"      Líneas de código: {len(code_lines)}")
        
        # Buscar imports importantes
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(f"from {node.module}")
        
        if imports:
            print(f"   📦 IMPORTS:")
            for imp in imports[:8]:
                print(f"      • {imp}")
            if len(imports) > 8:
                print(f"        ... y {len(imports) - 8} más")
        
        return {
            "file": filepath,
            "classes": classes_info,
            "functions": functions,
            "imports": imports,
            "lines": len(lines)
        }
        
    except SyntaxError as e:
        print(f"   ❌ ERROR DE SINTAXIS en línea {e.lineno}")
        
        # Mostrar contexto del error
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
        
        start = max(0, e.lineno - 3)
        end = min(len(all_lines), e.lineno + 2)
        
        print(f"      Contexto (líneas {start+1}-{end}):")
        for i in range(start, end):
            print(f"      {i+1}: {all_lines[i].rstrip()}")
        
        return {"file": filepath, "error": f"SyntaxError línea {e.lineno}"}
    
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)[:80]}")
        return {"file": filepath, "error": str(e)}

def main():
    """Función principal."""
    results = {}
    
    for filepath, expected_classes in MODULES_TO_ANALYZE:
        result = analyze_file(filepath, expected_classes)
        if result:
            results[filepath] = result
    
    # Resumen general
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL ANÁLISIS")
    print("=" * 70)
    
    total_classes = 0
    total_methods = 0
    working_files = 0
    
    for filepath, result in results.items():
        if "error" not in result and "classes" in result:
            working_files += 1
            total_classes += len(result["classes"])
            for cls in result["classes"]:
                total_methods += len(cls["methods"])
    
    print(f"✅ Archivos analizados: {len(MODULES_TO_ANALYZE)}")
    print(f"✅ Archivos sin errores: {working_files}")
    print(f"✅ Clases encontradas: {total_classes}")
    print(f"✅ Métodos totales: {total_methods}")
    
    # Recomendaciones para el bot
    print("\n🎯 RECOMENDACIONES PARA EL BOT PROFESIONAL:")
    
    if "core/card_recognizer.py" in results and "classes" in results["core/card_recognizer.py"]:
        card_classes = [c["name"] for c in results["core/card_recognizer.py"]["classes"]]
        print("  1. ✅ Módulo de reconocimiento de cartas disponible")
        print(f"     Clases: {', '.join(card_classes)}")
    
    if "core/learning_system.py" in results and "classes" in results["core/learning_system.py"]:
        learning_classes = [c["name"] for c in results["core/learning_system.py"]["classes"]]
        print("  2. ✅ Sistema de aprendizaje disponible")
        print(f"     Clases: {', '.join(learning_classes)}")
    
    # Guardar resultados en JSON
    output_path = Path("bot_analysis_report.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte guardado en: {output_path}")
    
    # Siguientes pasos
    print("\n" + "=" * 70)
    print("🚀 SIGUIENTES PASOS PARA EL BOT PROFESIONAL")
    print("=" * 70)
    
    print("1. Crear motor de decisiones basado en GTO avanzado")
    print("2. Integrar reconocimiento de cartas con PokerStars")
    print("3. Implementar estrategias por fase (preflop, flop, turn, river)")
    print("4. Añadir perfil de jugador con 20+ años experiencia")
    print("5. Crear sistema de ejecución automática de acciones")
    
    print("\n📋 EJECUTAR:")
    print("   python create_professional_bot.py")

if __name__ == "__main__":
    main()