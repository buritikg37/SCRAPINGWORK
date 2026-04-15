@echo off
setlocal
REM ============================================================================
REM SCRIPT DE CONFIGURACION - SCRAPER DE PETSHOPS
REM ============================================================================
REM Este script crea una virtualenv local e instala las dependencias necesarias.
REM Ejecutar: instalar_dependencias.bat
REM ============================================================================

echo.
echo ============================================================================
echo         CONFIGURACION AUTOMATICA - SCRAPER DE PETSHOPS
echo ============================================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

REM Verificar Python instalado
echo [PASO 1] Verificando instalacion de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python no esta instalado o no esta en PATH
    echo Por favor, descarga Python desde https://www.python.org
    echo E instala con la opcion "Agregar Python a PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do echo ✓ %%i encontrado

REM Crear entorno virtual local
echo.
echo [PASO 2] Preparando entorno virtual local...
if exist ".venv\Scripts\python.exe" (
    echo ✓ Se reutilizara la virtualenv local existente
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear la virtualenv local
        pause
        exit /b 1
    )
    echo ✓ Virtualenv creada en %PROJECT_DIR%.venv
)

REM Verificar pip en el entorno virtual
echo.
echo [PASO 3] Verificando gestor de paquetes (pip)...
".venv\Scripts\python.exe" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no esta disponible dentro de la virtualenv
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('".venv\Scripts\python.exe" -m pip --version') do echo ✓ %%i

REM Actualizar pip
echo.
echo [PASO 4] Actualizando pip a la ultima version...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: No se pudo actualizar pip
    pause
    exit /b 1
)
echo ✓ pip actualizado

REM Instalar dependencias
echo.
echo [PASO 5] Instalando dependencias del proyecto...
echo Esto puede tomar varios minutos, espera...
echo.
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema instalando las dependencias
    echo Intenta ejecutar manualmente:
    echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)
echo.
echo ✓ Todas las dependencias instaladas correctamente

REM Verificar Chrome
echo.
echo [PASO 6] Verificando instalacion de Google Chrome...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version >nul 2>&1
if errorlevel 1 (
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ADVERTENCIA: Chrome no se encontro en ubicaciones estandar
        echo La carpeta puede estar en otra ubicacion
        echo Por favor descarga Chrome desde https://www.google.com/chrome
        echo.
    ) else (
        echo ✓ Google Chrome encontrado
    )
) else (
    echo ✓ Google Chrome encontrado
)

REM Finalizar
echo.
echo ============================================================================
echo                       CONFIGURACION COMPLETADA
echo ============================================================================
echo.
echo PROXIMOS PASOS:
echo 1. Abre Terminal/PowerShell en esta carpeta
echo 2. Ejecuta: .venv\Scripts\python.exe PetshopRed.py
echo.
echo Para mas informacion, consulta el archivo README.md
echo.
pause
