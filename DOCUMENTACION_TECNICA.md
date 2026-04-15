# 🏗️ DOCUMENTACIÓN TÉCNICA - ESTRUCTURA DEL PROYECTO

## 📁 Estructura de la carpeta

```
Scraping Python/
│
├── 📄 PetshopRed.py                    ← ARCHIVO PRINCIPAL (ejecutar esto)
├── 📄 scraper.py                       ← Ejemplos básicos de scraping
│
├── 📋 requirements.txt                 ← Lista de dependencias
├── 🔧 instalar_dependencias.bat        ← Script instalación automática
│
├── 📚 README.md                        ← Guía general del proyecto
├── 🚀 GUIA_EJECUCION.md               ← Pasos para ejecutar (EMPIEZA AQUÍ)
├── 📚 EJEMPLOS_DE_USO.md              ← Cómo usar los datos extraídos
├── 📋 DOCUMENTACION_TECNICA.md         ← Este archivo
│
├── 📂 Archivos de salida (se crean automáticamente):
│   ├── petshops_resultados.json        ← Datos en formato JSON
│   ├── petshops_resultados.csv         ← Datos en formato tabla (Excel)
│   └── scraper_log.txt                 ← Log de ejecución
│
└── 📂 Datos ejemplo (opcionales):
    ├── countries.csv                   ← Archivo de ejemplo
    └── countries.json                  ← Archivo de ejemplo
```

---

## 🔄 FLUJO DEL PROGRAMA

```
┌─────────────────────────────────────────┐
│   INICIO: Ejecutar PetshopRed.py        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 1. Inicializar ScraperPetshops()        │
│    ├─ Crear lista vacía                │
│    └─ Registrar evento en log          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. iniciar_driver()                     │
│    ├─ Descargar ChromeDriver           │
│    ├─ Configurar opciones Chrome       │
│    └─ Abrir navegador                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. extraer_petshops()                   │
│    ├─ Acceder URL                      │
│    ├─ Esperar carga                    │
│    ├─ Fazer scrolls                    │
│    ├─ Encontrar elementos              │
│    └─ Para cada resultado:             │
│        └─ Llamar extraer_detalles()    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. extraer_detalles_petshop()           │
│    ├─ Extraer nombre                   │
│    ├─ Extraer dirección                │
│    ├─ Extraer teléfono                 │
│    ├─ Extraer ubicación                │
│    └─ Guardar en lista                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 5. procesar_datos()                     │
│    ├─ Eliminar duplicados              │
│    ├─ Validar información              │
│    └─ Ordenar resultados               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 6. guardar_resultados()                 │
│    ├─ Guardar JSON                     │
│    ├─ Guardar CSV                      │
│    ├─ Mostrar resumen                  │
│    └─ Registrar en log                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 7. cerrar_driver()                      │
│    └─ Cerrar navegador                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   FIN: Proceso completado               │
└─────────────────────────────────────────┘
```

---

## 📝 DESCRIPCIÓN DE ARCHIVOS

### PetshopRed.py (ARCHIVO PRINCIPAL)

**Propósito:** Extraer datos de petshops desde Google Maps

**Componentes principales:**

#### 1. Importaciones
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
```

#### 2. Configuración
```python
URL_MAPS = "..."  # URL a scrapear
ESPERA_PAGINA = 10  # Tiempos de espera
ARCHIVO_JSON = "petshops_resultados.json"  # Archivos salida
```

#### 3. Clase ScraperPetshops
```python
class ScraperPetshops:
    def __init__(self)
    def registrar_log(mensaje)
    def iniciar_driver()
    def extraer_petshops()
    def extraer_detalles_petshop(nombre)
    def procesar_datos()
    def guardar_resultados()
    def mostrar_resumen()
    def cerrar_driver()
    def ejecutar()
```

**Total de líneas:** ~450 líneas documentadas

---

### requirements.txt

**Propósito:** Definir todas las dependencias del proyecto

**Contenido:**
```
selenium==4.15.2           # WebDriver para Chrome
webdriver-manager==4.0.1   # Descargar ChromeDriver automático
pandas==2.1.4              # Análisis de datos
requests==2.31.0           # Peticiones HTTP
beautifulsoup4==4.12.2     # Parsing HTML
lxml==4.9.3                # Parser XML
python-dateutil==2.8.2     # Manejo de fechas
```

**Instalación:**
```bash
pip install -r requirements.txt
```

---

### README.md

**Propósito:** Documentación general del proyecto

**Secciones:**
- ✅ Descripción
- ✅ Requisitos
- ✅ Instalación
- ✅ Uso
- ✅ Archivos de salida
- ✅ Explicación del código
- ✅ Configuración personalizada
- ✅ Solución de problemas
- ✅ Referencias

---

### GUIA_EJECUCION.md

**Propósito:** Guía paso a paso para ejecutar el scraper

**Contenido:**
- ✅ Checklist previo
- ✅ Preparación del entorno
- ✅ Instalación (automática o manual)
- ✅ Personalización de búsqueda
- ✅ Ejecución del scraper
- ✅ Revisión de resultados
- ✅ Solución de problemas
- ✅ Consejos útiles

---

### EJEMPLOS_DE_USO.md

**Propósito:** Ejemplos prácticos de cómo usar los datos

**Ejemplos incluidos:**
- ✅ Trabajar con CSV en Excel
- ✅ Trabajar con JSON en Python
- ✅ Análisis con Pandas
- ✅ Crear mapas
- ✅ Enviar correos
- ✅ Guardar en base de datos
- ✅ Automatizar scraping periódico

---

### instalar_dependencias.bat

**Propósito:** Script para instalación automática en Windows

**Acciones:**
```
1. Verifica Python instalado
2. Verifica pip instalado
3. Actualiza pip
4. Instala dependencias desde requirements.txt
5. Verifica Chrome
```

**Uso:** Doble clic en el archivo

---

## 🔑 VARIABLES CLAVE

### Configuración Global

```python
# URL de búsqueda - MODIFICAR para cambiar ubicación
URL_MAPS = "https://www.google.com/maps/search/petshop/@5.0572936,-75.4881471,16z/..."

# Tiempos de espera (en segundos)
ESPERA_PAGINA = 10  # Espera máxima para cargar elementos
TIEMPO_SCROLL = 2   # Espera entre scrolls
DELAY_PETICIONES = 2  # Espera entre peticiones

# Archivos de salida
ARCHIVO_JSON = "petshops_resultados.json"
ARCHIVO_CSV = "petshops_resultados.csv"
ARCHIVO_LOG = "scraper_log.txt"
```

### Variables de Instancia

```python
self.driver          # Objeto WebDriver de Selenium
self.petshops        # Lista con datos extraídos
self.marca_tiempo    # Timestamp de ejecución
```

---

## 🔗 DEPENDENCIAS Y VERSIONES

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| selenium | 4.15.2 | WebDriver para navegación automática |
| webdriver-manager | 4.0.1 | Descarga ChromeDriver automático |
| pandas | 2.1.4 | Análisis y manipulación de datos |
| requests | 2.31.0 | Peticiones HTTP |
| beautifulsoup4 | 4.12.2 | Parsing de HTML |
| lxml | 4.9.3 | Parser XML |
| python-dateutil | 2.8.2 | Utiles de fecha |
| Python | 3.8+ | Lenguaje base |
| Google Chrome | Última | Navegador a automatizar |

---

## 🧪 FLUJO DE DATOS

### Entrada:
```
URL de Google Maps
    ↓
(Selenium navega)
```

### Procesamiento:
```
HTML de Google Maps
    ↓
(Parsing con Selenium/BeautifulSoup)
    ↓
Extraer: nombre, dirección, teléfono, ubicación
    ↓
(Procesar: eliminar duplicados, validar)
    ↓
Lista de petshops limpios
```

### Salida:
```
petshops_resultados.json     ← Formato JSON
petshops_resultados.csv      ← Formato tabla
scraper_log.txt              ← Eventos de ejecución
```

---

## 🛡️ MANEJO DE ERRORES

El script incluye manejo de excepciones en:

```python
# Iniciar driver
try:
    # código
except Exception as e:
    registrar_log(f"✗ Error: {str(e)}")

# Extraer datos
try:
    # código
except:
    registrar_log(f"⚠️ Error al procesar item")
    continue

# Guardar resultados
try:
    # código
except Exception as e:
    registrar_log(f"✗ Error al guardar: {str(e)}")

# Ejecución principal
try:
    scraper.ejecutar()
except KeyboardInterrupt:
    print("\n⚠ Proceso interrumpido")
finally:
    scraper.cerrar_driver()
```

---

## 📊 ESTRUCTURA DE DATOS

### Formato JSON
```json
{
  "nombre": "Petshop La Mascota",
  "direccion": "Carrera 1 #123, Medellín",
  "telefono": "+57 4 123456",
  "latitud": "5.067",
  "longitud": "-75.487",
  "url_actual": "https://www.google.com/maps/...",
  "hora_extraccion": "2026-04-13 10:30:45"
}
```

### Formato CSV
```
nombre,direccion,telefono,latitud,longitud,url_actual,hora_extraccion
"Petshop La Mascota","Carrera 1 #123, Medellín","+57 4 123456","5.067","-75.487","https://...",2026-04-13 10:30:45
```

### Estructura en Python (list of dicts)
```python
petshops = [
    {
        "nombre": str,
        "direccion": str,
        "telefono": str,
        "latitud": str,
        "longitud": str,
        "url_actual": str,
        "hora_extraccion": str
    },
    ...
]
```

---

## ⏱️ COMPLEJIDAD Y RENDIMIENTO

### Complejidad de Tiempo
- Extracción: O(n) donde n = número de petshops
- Procesamiento: O(n log n) si hay ordenamiento
- Guardado: O(n)
- **Total:** O(n log n)

### Tiempo Real Estimado
- Iniciación: 5 segundos
- Navegación: 3 segundos
- Extracción: 2-3 minutos (depende de cantidad)
- Procesamiento: 1 segundo
- Guardado: 1 segundo
- **Total:** 2-5 minutos

### Optimizaciones Posibles
```python
# Aumentar velocidad
ESPERA_PAGINA = 5        # Reducir de 10
TIEMPO_SCROLL = 0.5      # Reducir de 2
headless = True          # No mostrar navegador

# Usar ThreadPoolExecutor para paralelismo
# Usar cache de resultados
# Limitar cantidad de scrolls
```

---

## 🔐 SEGURIDAD Y BUENAS PRÁCTICAS

✅ **Implementado:**
- Identificación como bot reducida (user-agent)
- Delays entre peticiones (DELAY_PETICIONES)
- Logging detallado de todas acciones
- Manejo de excepciones robusto
- Cierre correcto de recursos

❌ **No implementado (para futura mejora):**
- Proxy rotation
- VPN integration
- Rate limiting avanzado
- Captcha solving
- Session persistence

---

## 🔄 POSIBLES MEJORAS

### Nivel 1: Básico
```python
✓ Agregar más campos (horarios, reseñas)
✓ Filtrar por calificación
✓ Exportar a Excel formateado
```

### Nivel 2: Intermedio
```python
✓ Múltiples ciudades en una ejecución
✓ Base de datos MySQL/PostgreSQL
✓ API REST para acceder a datos
✓ Dashboard con gráficos
```

### Nivel 3: Avanzado
```python
✓ Machine learning para clasificación
✓ Información histórica (tracker precios)
✓ Integración con aplicaciones externas
✓ Sistema de notificaciones
```

---

## 📞 SOPORTE TÉCNICO

### Errores comunes:

| Error | Prueba |
|-------|--------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Element not found | Aumentar `ESPERA_PAGINA` |
| Connection refused | Verificar internet |
| Chrome not found | Instalar Chrome |
| Permission denied | Ejecutar como admin |

### Debugging:
1. Leer `scraper_log.txt` completamente
2. Verificar `petshops_resultados.json` tiene datos
3. Ejecutar manualmente en Chrome
4. Usar `print()` para debugging

---

## 📚 REFERENCIAS

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [Google Maps](https://maps.google.com)

---

**Versión:** 1.0  
**Última actualización:** 2026-04-13  
**Mantenedor:** Sistema de Scraping  
**Estado:** ✅ Documentación Completa
