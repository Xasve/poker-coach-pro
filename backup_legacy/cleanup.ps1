# cleanup.ps1 - Script de limpieza automática
param(
    [switch]$DryRun = $false,
    [switch]$KeepArchives = $false,
    [switch]$Help = $false
)

function Show-Help {
    Write-Host "🧹 CLEANUP SCRIPT - POKER COACH PRO" -ForegroundColor Cyan
    Write-Host "=" * 60
    Write-Host "Limpia archivos temporales y organiza el proyecto" -ForegroundColor White
    Write-Host ""
    Write-Host "Uso: .\cleanup.ps1 [OPCIONES]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Gray
    Write-Host "  -DryRun        Solo mostrar qué se eliminaría" -ForegroundColor Gray
    Write-Host "  -KeepArchives  Mantener archivos en archive/" -ForegroundColor Gray
    Write-Host "  -Help          Mostrar esta ayuda" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Green
    Write-Host "  .\cleanup.ps1                 # Limpieza normal" -ForegroundColor Gray
    Write-Host "  .\cleanup.ps1 -DryRun         # Ver sin eliminar" -ForegroundColor Gray
    Write-Host "  .\cleanup.ps1 -KeepArchives   # Mantener archivos legacy" -ForegroundColor Gray
    Write-Host "=" * 60
}

if ($Help) {
    Show-Help
    exit 0
}

Write-Host "🔍 Analizando proyecto..." -ForegroundColor Green

# Patrones de archivos a eliminar
$patternsToDelete = @(
    # Archivos Python temporales
    "*.pyc",
    "*.pyo",
    "*.pyd",
    
    # Cachés
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    
    # Archivos de IDE
    ".vscode/*",
    ".idea/*",
    "*.swp",
    "*.swo",
    "*~",
    
    # Archivos de sistema
    "Thumbs.db",
    ".DS_Store",
    "desktop.ini",
    
    # Logs temporales (excepto logs organizados)
    "logs/*.log",
    "logs/*.txt",
    "!logs/sessions/",
    "!logs/decisions/",
    "!logs/errors/",
    "!logs/performance/",
    "!logs/debug/",
    
    # Backups y temporales
    "*.bak",
    "*.backup",
    "*.tmp",
    "temp_*",
    "tmp_*",
    
    # Archivos de prueba temporales
    "test_output_*",
    "debug_*",
    
    # Screenshots temporales
    "screenshot_*",
    "capture_*.png"
)

# Directorios específicos a limpiar
$directoriesToClean = @(
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "temp",
    "tmp",
    "test_output"
)

# Archivos específicos a verificar por duplicados
$potentialDuplicates = @(
    # Sistema principal (mantener solo el unificado)
    @("main_integrated.py", "final_integration.py", "integrated_system_v2.py"),
    
    # Pruebas (mantener organizadas)
    @("startup_check.py", "quick_test.py", "final_tests.py"),
    
    # Documentación (mantener organizada)
    @("README.md", "CONTINUATION_GUIDE.md", "README_FINAL.md")
)

if (-not $KeepArchives) {
    $patternsToDelete += @("archive/legacy/*.py")
}

# Función para obtener tamaño de directorio
function Get-DirectorySize($path) {
    if (Test-Path $path) {
        $size = (Get-ChildItem -Path $path -Recurse -File | Measure-Object -Property Length -Sum).Sum
        if ($size) {
            if ($size -gt 1GB) {
                return "$([math]::Round($size / 1GB, 2)) GB"
            } elseif ($size -gt 1MB) {
                return "$([math]::Round($size / 1MB, 2)) MB"
            } elseif ($size -gt 1KB) {
                return "$([math]::Round($size / 1KB, 2)) KB"
            } else {
                return "$size bytes"
            }
        }
    }
    return "0 bytes"
}

# Mostrar estadísticas antes
Write-Host "`n📊 ESTADÍSTICAS ANTES DE LIMPIAR:" -ForegroundColor Cyan

$totalFiles = (Get-ChildItem -Path . -Recurse -File).Count
$totalDirs = (Get-ChildItem -Path . -Recurse -Directory).Count
$totalSize = Get-DirectorySize "."

Write-Host "   Archivos: $totalFiles" -ForegroundColor Gray
Write-Host "   Directorios: $totalDirs" -ForegroundColor Gray
Write-Host "   Tamaño total: $totalSize" -ForegroundColor Gray

# Buscar archivos para eliminar
Write-Host "`n🔍 BUSCANDO ARCHIVOS PARA LIMPIAR..." -ForegroundColor Green

$filesToDelete = @()
$dirsToDelete = @()
$spaceToSave = 0

foreach ($pattern in $patternsToDelete) {
    $isExclusion = $pattern.StartsWith("!")
    $actualPattern = if ($isExclusion) { $pattern.Substring(1) } else { $pattern }
    
    try {
        if ($isExclusion) {
            # Para exclusiones, solo registrar
            Write-Host "   ⏭️  Excluyendo: $actualPattern" -ForegroundColor DarkGray
        } else {
            $found = Get-ChildItem -Path . -Recurse -Filter $actualPattern -ErrorAction SilentlyContinue
            
            if ($found) {
                foreach ($item in $found) {
                    if ($item.PSIsContainer) {
                        $dirsToDelete += $item.FullName
                        $dirSize = Get-DirectorySize $item.FullName
                        Write-Host "   📁 Encontrado: $($item.FullName) ($dirSize)" -ForegroundColor Gray
                    } else {
                        $filesToDelete += $item.FullName
                        $spaceToSave += $item.Length
                        Write-Host "   📄 Encontrado: $($item.FullName) ($($item.Length) bytes)" -ForegroundColor Gray
                    }
                }
            }
        }
    }
    catch {
        Write-Host "   ⚠️  Error buscando $pattern: $_" -ForegroundColor Yellow
    }
}

# Buscar directorios específicos
foreach ($dir in $directoriesToClean) {
    $foundDirs = Get-ChildItem -Path . -Recurse -Directory -Filter $dir -ErrorAction SilentlyContinue
    
    foreach ($foundDir in $foundDirs) {
        if (-not ($dirsToDelete -contains $foundDir.FullName)) {
            $dirsToDelete += $foundDir.FullName
            $dirSize = Get-DirectorySize $foundDir.FullName
            Write-Host "   📁 Encontrado: $($foundDir.FullName) ($dirSize)" -ForegroundColor Gray
        }
    }
}

# Mostrar resumen
Write-Host "`n📋 RESUMEN DE LIMPIEZA:" -ForegroundColor Cyan
Write-Host "   Archivos a eliminar: $($filesToDelete.Count)" -ForegroundColor Gray
Write-Host "   Directorios a eliminar: $($dirsToDelete.Count)" -ForegroundColor Gray

if ($spaceToSave -gt 0) {
    if ($spaceToSave -gt 1MB) {
        $spaceMB = [math]::Round($spaceToSave / 1MB, 2)
        Write-Host "   Espacio a liberar: $spaceMB MB" -ForegroundColor Gray
    } else {
        $spaceKB = [math]::Round($spaceToSave / 1KB, 2)
        Write-Host "   Espacio a liberar: $spaceKB KB" -ForegroundColor Gray
    }
}

# Preguntar confirmación (si no es DryRun)
if (-not $DryRun -and ($filesToDelete.Count -gt 0 -or $dirsToDelete.Count -gt 0)) {
    Write-Host "`n  Continuar con la limpieza? (s/n): " -ForegroundColor Yellow -NoNewline
    $confirm = Read-Host
    
    if ($confirm -ne 's') {
        Write-Host "  Limpieza cancelada" -ForegroundColor Red
        exit 0
    }
}

# Eliminar archivos
$deletedFiles = 0
$deletedDirs = 0

if (-not $DryRun) {
    Write-Host "`n  ELIMINANDO ARCHIVOS..." -ForegroundColor Green
    
    # Eliminar archivos
    foreach ($file in $filesToDelete) {
        try {
            Remove-Item -Path $file -Force -ErrorAction Stop
            Write-Host "    Eliminado: $file" -ForegroundColor Gray
            $deletedFiles++
        }
        catch {
            Write-Host "   ❌ Error eliminando $file: $_" -ForegroundColor Red
        }
    }
    
    # Eliminar directorios (en orden inverso para eliminar subdirectorios primero)
    foreach ($dir in ($dirsToDelete | Sort-Object Length -Descending)) {
        try {
            Remove-Item -Path $dir -Recurse -Force -ErrorAction Stop
            Write-Host "   ✅ Eliminado: $dir" -ForegroundColor Gray
            $deletedDirs++
        }
        catch {
            Write-Host "   ❌ Error eliminando $dir: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "`n🔍 MODO DRY RUN - No se eliminará nada" -ForegroundColor Yellow
    Write-Host "   Archivos que se eliminarían: $($filesToDelete.Count)" -ForegroundColor Gray
    Write-Host "   Directorios que se eliminarían: $($dirsToDelete.Count)" -ForegroundColor Gray
}

# Mostrar estadísticas después
Write-Host "`n📊 ESTADÍSTICAS DESPUÉS DE LIMPIAR:" -ForegroundColor Cyan

if (-not $DryRun) {
    $totalFilesAfter = (Get-ChildItem -Path . -Recurse -File).Count
    $totalDirsAfter = (Get-ChildItem -Path . -Recurse -Directory).Count
    $totalSizeAfter = Get-DirectorySize "."
    
    Write-Host "   Archivos eliminados: $deletedFiles" -ForegroundColor Gray
    Write-Host "   Directorios eliminados: $deletedDirs" -ForegroundColor Gray
    Write-Host "   Archivos restantes: $totalFilesAfter" -ForegroundColor Gray
    Write-Host "   Directorios restantes: $totalDirsAfter" -ForegroundColor Gray
    Write-Host "   Tamaño total: $totalSizeAfter" -ForegroundColor Gray
    
    # Calcular reducción
    $filesReduction = $totalFiles - $totalFilesAfter
    $sizeReduction = "N/A"  # Se necesitaría calcular el tamaño antes
    
    if ($filesReduction -gt 0) {
        Write-Host "   📉 Reducción: $filesReduction archivos menos" -ForegroundColor Green
    }
}

# Verificar estructura organizada
Write-Host "`n🔍 VERIFICANDO ESTRUCTURA ORGANIZADA..." -ForegroundColor Green

$organizedDirs = @(
    "src",
    "src/core",
    "src/ocr",
    "src/gto",
    "src/ui",
    "src/capture",
    "src/analysis",
    "src/utils",
    "data",
    "data/templates",
    "data/datasets",
    "data/models",
    "config",
    "logs",
    "docs",
    "tests",
    "scripts"
)

$missingDirs = @()
foreach ($dir in $organizedDirs) {
    if (-not (Test-Path $dir)) {
        $missingDirs += $dir
        Write-Host "   ❌ Faltante: $dir" -ForegroundColor Red
    } else {
        Write-Host "   ✅ Existe: $dir" -ForegroundColor Gray
    }
}

if ($missingDirs.Count -gt 0) {
    Write-Host "`n💡 Directorios faltantes. Creando..." -ForegroundColor Yellow
    foreach ($dir in $missingDirs) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
        Write-Host "   📁 Creado: $dir" -ForegroundColor Gray
    }
}

# Verificar archivos principales
Write-Host "`n🔍 VERIFICANDO ARCHIVOS PRINCIPALES..." -ForegroundColor Green

$essentialFiles = @(
    "poker_coach_pro.py",
    "src/core/main_system.py",
    "src/analysis/color_optimizer.py",
    "src/analysis/ocr_enhancer.py",
    "config/system_config.example.yaml"
)

$missingFiles = @()
foreach ($file in $essentialFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
        Write-Host "   ❌ Faltante: $file" -ForegroundColor Red
    } else {
        Write-Host "   ✅ Existe: $file" -ForegroundColor Gray
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "`n⚠️  Algunos archivos esenciales faltan" -ForegroundColor Yellow
}

# Resumen final
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🎉 LIMPIEZA COMPLETADA" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "📋 MODO DRY RUN - Revisa lo que se eliminaría" -ForegroundColor Yellow
    Write-Host "💡 Ejecuta sin -DryRun para limpiar realmente" -ForegroundColor Gray
} else {
    Write-Host "✅ Proyecto limpiado y organizado" -ForegroundColor Green
    Write-Host "📁 Estructura organizada verificada" -ForegroundColor Gray
    Write-Host "🚀 Listo para usar: python poker_coach_pro.py" -ForegroundColor Green
}

Write-Host "`n💡 COMANDOS ÚTILES:" -ForegroundColor Cyan
Write-Host "   • python poker_coach_pro.py          # Sistema principal" -ForegroundColor Gray
Write-Host "   .\cleanup.ps1 -DryRun               # Ver limpieza sin hacer" -ForegroundColor Gray
Write-Host "   .\scripts\setup\install.ps1         # Instalar dependencias" -ForegroundColor Gray

Write-Host "`n" + "=" * 60
