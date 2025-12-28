# Añadir Python 3.11 al PATH (sesión actual)
$python311Dir = "python311_scripts"
if (Test-Path $python311Dir) {
    $env:Path = "$pwd\\$python311Dir;" + $env:Path
    Write-Host " Python 3.11 añadido al PATH" -ForegroundColor Green
}

# Alias para usar Python 3.11
function python311 { & "python311_scripts\python311.bat" @args }
function pip311 { & "python311_scripts\python311.bat" -m pip @args }

Write-Host "Alias disponibles: python311, pip311" -ForegroundColor Cyan
