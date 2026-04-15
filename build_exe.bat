@echo off
setlocal
cd /d "%~dp0"

set "APP_NAME=RedAgroScrapingWeb"
set "RELEASE_DIR=release\RedAgro Scraping Web"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: No se encontro la virtualenv local.
    echo Ejecuta primero instalar_dependencias.bat
    exit /b 1
)

echo Instalando herramientas de empaquetado...
".venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 exit /b 1

echo Construyendo ejecutable...
".venv\Scripts\pyinstaller.exe" ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name %APP_NAME% ^
  --icon "assets\redagro.ico" ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  --collect-all waitress ^
  launcher.py

if errorlevel 1 exit /b 1

if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"
copy /y "dist\%APP_NAME%.exe" "%RELEASE_DIR%\%APP_NAME%.exe" >nul
copy /y "assets\redagro.ico" "%RELEASE_DIR%\redagro.ico" >nul
copy /y "GUIA_EJECUCION.md" "%RELEASE_DIR%\GUIA_EJECUCION.md" >nul
copy /y "README_ENTREGA.txt" "%RELEASE_DIR%\README_ENTREGA.txt" >nul

echo.
echo Ejecutable creado en: dist\%APP_NAME%.exe
echo Carpeta final lista en: %RELEASE_DIR%
