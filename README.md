# 📱 SCRAPER DE PETSHOPS - GOOGLE MAPS

## 📋 Descripción del Proyecto

Este proyecto automatiza la **extracción de datos de petshops desde Google Maps**. Utilizando tecnología de web scraping, extrae información detallada de cada negocio encontrado en la búsqueda.

### Datos que se extraen:
✅ **Nombre del negocio**  
✅ **Dirección completa**  
✅ **Número de teléfono**  
✅ **Coordenadas de ubicación** (Latitud y Longitud)

---

## 🛠️ REQUISITOS DEL SISTEMA

### Dependencias de Software:
- **Python 3.8** o superior
- **Google Chrome** instalado en tu computadora
- **pip** (gestor de paquetes de Python)

### Verificar la instalación:
```bash
python --version
pip --version
```

---

## 📦 INSTALACIÓN DE DEPENDENCIAS

### Paso 1: Abrir Terminal en la carpeta del proyecto

En Windows, dentro de la carpeta del proyecto (`Scraping Python`), haz clic derecho y selecciona:
- "Abrir terminal aquí" o
- "Abrir PowerShell aquí"

### Paso 2: Instalar las librerías necesarias

Ejecuta el siguiente comando en la terminal:

```bash
pip install selenium webdriver-manager pandas requests beautifulsoup4
```

#### Explicación de cada librería:

| Librería | Propósito |
|----------|-----------|
| **selenium** | Automatiza la navegación en Chrome |
| **webdriver-manager** | Descarga automáticamente ChromeDriver |
| **pandas** | Manejo de datos en DataFrames |
| **requests** | Realiza peticiones HTTP |
| **beautifulsoup4** | Parsea y extrae HTML |

### Verificar instalación:
```bash
pip list
```

Deberías ver todas las librerías instaladas con sus versiones.

---

## 🚀 CÓMO USAR EL SCRAPER

### Método 1: Ejecutar desde Terminal (RECOMENDADO)

1. **Abre Terminal/PowerShell en la carpeta del proyecto**

2. **Ejecuta el comando:**
```bash
python PetshopRed.py
```

3. **Resultado esperado:**
   - Se abrirá automáticamente una ventana de Chrome
   - Chrome navegará a Google Maps
   - Empezará a extraer datos de petshops
   - Se generarán 3 archivos automáticamente

### Método 2: Ejecutar desde VS Code

1. **Abre el archivo `PetshopRed.py`**

2. **Haz clic en el botón "Play" (▶️) en la esquina superior derecha**

3. **O presiona:** `Ctrl + Shift + D` → Selecciona "Python"

---

## 📊 ARCHIVOS DE SALIDA

El scraper genera **3 archivos automáticamente** en la misma carpeta:

### 1️⃣ `petshops_resultados.json`
Formato: **Estructura JSON completa**
```json
[
  {
    "nombre": "Petshop ejemplo",
    "direccion": "Carrera 1 #1, Medellín",
    "telefono": "+57 1 2345678",
    "latitud": "5.0572936",
    "longitud": "-75.4881471",
    "url_actual": "https://www.google.com/maps/...",
    "hora_extraccion": "2026-04-13 10:30:45"
  }
]
```

**Ventajas:** Estructura ordenada, fácil de procesar con código

### 2️⃣ `petshops_resultados.csv`
Formato: **Tabla (Excel/Hoja de Cálculo)**
```
nombre,direccion,telefono,latitud,longitud,url_actual,hora_extraccion
Petshop ejemplo,"Carrera 1 #1, Medellín",+57 1 2345678,5.0572936,-75.4881471,...,2026-04-13 10:30:45
```

**Ventajas:** Abrir con Excel, Google Sheets, importar a bases de datos

### 3️⃣ `scraper_log.txt`
Formato: **Registro de eventos**
```
[2026-04-13 10:30:01] [INICIO] Scraper iniciado a las 2026-04-13 10:30:01
[2026-04-13 10:30:05] Iniciando Selenium WebDriver...
[2026-04-13 10:30:10] ✓ WebDriver iniciado correctamente
...
```

**Ventajas:** Debuggear, ver detalles de la ejecución

---

## 🔍 EXPLICACIÓN DEL CÓDIGO (PASO A PASO)

### PASO 1: IMPORTAR LIBRERÍAS
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
```
✅ Importa Selenium para automatizar el navegador  
✅ Importa las herramientas para encontrar elementos

### PASO 2: CONFIGURACIÓN INICIAL
```python
URL_MAPS = "https://www.google.com/maps/search/petshop/@5.0572936,-75.4881471,16z/..."
ESPERA_PAGINA = 10  # segundos
```
✅ Define la URL de búsqueda en Google Maps  
✅ Configura tiempos de espera para que cargue la página

### PASO 3: CREAR CLASE SCRAPERNETSHOPS
```python
class ScraperPetshops:
    def __init__(self):
        self.petshops = []
```
✅ Crea una clase para organizar todo el código  
✅ Inicializa una lista vacía para guardar datos

### PASO 4: EXTRAER PETSHOPS
```python
def extraer_petshops(self):
    self.driver.get(URL_MAPS)  # Acceder a Google Maps
    WebDriverWait(...).until(...)  # Esperar carga
    items = self.driver.find_elements(...)  # Encontrar resultados
```
✅ Accede a Google Maps  
✅ Espera a que carguen los resultados  
✅ Encuentra todos los petshops listados

### PASO 5: EXTRAER DETALLES
```python
def extraer_detalles_petshop(self, nombre):
    direccion = self.driver.find_element(...)
    telefono = self.driver.find_element(...)
```
✅ Extrae la dirección del petshop  
✅ Extrae el número de teléfono

### PASO 6-10: PROCESAR, GUARDAR Y CERRAR
```python
def guardar_resultados(self):
    json.dump(self.petshops, f)  # Guardar JSON
    escritor.writerows(self.petshops)  # Guardar CSV
```
✅ Procesa los datos (elimina duplicados)  
✅ Guarda en archivos JSON y CSV  
✅ Cierra el navegador correctamente

---

## ⚙️ CONFIGURACIÓN PERSONALIZADA

Puedes modificar estos parámetros en `PetshopRed.py`:

```python
# URL de búsqueda (cambiar con otro lugar)
URL_MAPS = "https://www.google.com/maps/search/petshop/@5.0572936,-75.4881471,16z/..."

# Tiempos de espera (en segundos)
ESPERA_PAGINA = 10      # Tiempo máximo para cargar página
TIEMPO_SCROLL = 2       # Espera entre scrolls
DELAY_PETICIONES = 2    # Espera entre peticiones

# Nombres de archivos de salida
ARCHIVO_JSON = "petshops_resultados.json"
ARCHIVO_CSV = "petshops_resultados.csv"
ARCHIVO_LOG = "scraper_log.txt"
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "ChromeDriver not found"
**Solución:**
```bash
pip install --upgrade webdriver-manager
```

### ❌ Error: "Connection refused"
**Solución:** Asegúrate de tener internet y que Google Maps funcione normalmente

### ❌ Error: "Element not found"
**Solución:** Google Maps puede cambiar su estructura. Abre el archivo y verifica los elementos CSS

### ❌ Chrome se cierra inmediatamente
**Solución:** Comprueba que Chrome esté correctamente instalado
```bash
chrome.exe --version
```

### ❌ Poco datos extraídos
**Solución:** Aumenta el número de scrolls:
```python
for intento in range(10):  # Cambiar de 5 a 10
```

---

## 💾 OPCIONES DE USO

### Opción 1: Abrir CSV en Excel
1. Abre el archivo `petshops_resultados.csv`
2. Haz clic derecho → "Abrir con" → Excel
3. Se verá como una tabla

### Opción 2: Abrir JSON en Python
```python
import json

with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

for petshop in datos:
    print(f"{petshop['nombre']}: {petshop['telefono']}")
```

### Opción 3: Usar en Google Sheets
1. Abre Google Drive
2. Crea nueva hoja de cálculo
3. Archivo → Importar → Carga `petshops_resultados.csv`

---

## 📈 MEJORAS FUTURAS

- [ ] Extraer calificación/reseñas
- [ ] Extraer horario de atención
- [ ] Extraer sitio web
- [ ] Extraer redes sociales
- [ ] Agregar búsqueda por múltiples ciudades
- [ ] Crear interfaz gráfica (GUI)
- [ ] Guardar en base de datos SQL

---

## ⚠️ NOTAS IMPORTANTES

⚠️ **Respeta los términos de servicio de Google Maps**
- Este scraper es solo para uso educativo
- No sobrecargar los servidores con peticiones frecuentes
- Usar con responsabilidad

⚠️ **Verificar datos extraídos**
- A veces el scraper puede no encontrar toda la información
- Si falta información, significa que Google Maps no la visibiliza

⚠️ **Privacidad**
- Los datos extraídos son públicos en Google Maps
- No compartir información personal indebidamente

---

## 📞 CONTACTO Y SOPORTE

Si tienes problemas:
1. Revisa este archivo completamente
2. Verifica el archivo `scraper_log.txt` para más detalles
3. Abre un issue en el proyecto

---

## 📚 REFERENCIAS

- [Documentación de Selenium](https://selenium-python.readthedocs.io/)
- [Google Maps](https://maps.google.com)
- [Python 3 Documentation](https://docs.python.org/3/)

---

**Última actualización:** 2026-04-13  
**Versión:** 1.0  
**Estado:** ✅ Funcional
