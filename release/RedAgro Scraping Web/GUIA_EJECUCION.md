# 🚀 GUÍA DE EJECUCIÓN - PASO A PASO

## ✅ CHECKLIST PREVIO

Antes de empezar, asegúrate de tener:
- [ ] Python 3.8 o superior instalado
- [ ] Google Chrome instalado
- [ ] Acceso a internet
- [ ] La carpeta "Scraping Python" descargada

---

## 📝 PASO 1: PREPARAR EL ENTORNO

### 1.1 Abre esta carpeta en el Explorador
- Abre tu carpeta: `C:\Users\Sistemas\Scraping Python`
- Verifica que estén estos archivos:
  ```
  ✓ PetshopRed.py
  ✓ requirements.txt
  ✓ README.md
  ✓ GUIA_EJECUCION.md (este archivo)
  ✓ instalar_dependencias.bat
  ```

### 1.2 Opción A: Instalación AUTOMÁTICA (Recomendado)

1. **En la carpeta, haz doble clic en:** `instalar_dependencias.bat`
2. Se abrirá una ventana negra (terminal)
3. Espera a que termine (verás ✓ al final)
4. Presiona una tecla cuando pida
5. ¡Listo! Salta al PASO 2

### 1.3 Opción B: Instalación MANUAL

Si la opción anterior no funciona, haz esto:

1. **Abre Terminal en esta carpeta:**
   - En Windows: `Ctrl + Shift + Clic derecho` → "Abrir PowerShell aquí"

2. **Ejecuta este comando:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Espera a que termine** (verde ✓ al final)

4. **Verifica la instalación:**
   ```powershell
   python -c "import selenium; print('✓ Selenium instalado')"
   ```

---

## 🎯 PASO 2: PERSONALIZAR LA BÚSQUEDA (Opcional)

Si quieres cambiar la ubicación de búsqueda:

1. **Abre Google Maps:** https://maps.google.com
2. **Busca:** `petshop` en tu ciudad
3. **Copia la URL** de la barra de direcciones
4. **Abre:** `PetshopRed.py` con un editor de texto
5. **Encuentra esta línea:**
   ```python
   URL_MAPS = "https://www.google.com/maps/search/..."
   ```
6. **Reemplaza con tu URL**
7. **Guarda** el archivo

---

## ▶️ PASO 3: EJECUTAR EL SCRAPER

### Opción A: Desde Terminal (Recomendado)

1. **Abre Terminal en la carpeta:**
   - Windows: `Ctrl + Shift + Clic derecho` → "Abrir PowerShell aquí"

2. **Ejecuta:**
   ```powershell
   python PetshopRed.py
   ```

3. **Resultado esperado:**
   ```
   ======================================================================
   SCRAPER DE PETSHOPS - GOOGLE MAPS
   ======================================================================
   Iniciando proceso de extracción...
   
   [INICIO] Scraper iniciado a las 2026-04-13 10:30:01
   Iniciando Selenium WebDriver...
   ✓ WebDriver iniciado correctamente
   Accediendo a Google Maps...
   ...
   ```

### Opción B: Desde VS Code

1. **Abre el archivo** `PetshopRed.py`
2. **Haz clic en** el botón ▶️ (Play) en la esquina superior derecha
3. Se abrirá la terminal integrada
4. Mira la salida del programa

### Opción C: Hacer doble clic al archivo

⚠️ No recomendado (la ventana se cierra rápidamente)

---

## ⏳ PASO 4: ESPERAR LA EJECUCIÓN

### Lo que pasará:

**Segundo 1-5:**
- Se abre automáticamente una ventana de Chrome
- ✓ En la terminal verás: "WebDriver iniciado correctamente"

**Segundo 5-10:**
- Chrome navega a Google Maps
- Se ve la búsqueda de petshops
- ✓ En la terminal: "Página cargada correctamente"

**Segundo 10-30:**
- Comienza a extraer datos
- Ve scrolls automáticos en Chrome
- ✓ En la terminal: "Extrayendo petshops..."

**Segundo 30+:**
- Se procesa la información
- Se guardan los archivos
- Chrome se cierra automáticamente
- ✓ En la terminal: "Proceso completado exitosamente"

### Tiempo total estimado:
⏱️ **2-5 minutos** según cantidad de resultados

---

## 📊 PASO 5: REVISAR RESULTADOS

### Se crearán 3 archivos automáticamente:

#### 📄 Opción 1: `petshops_resultados.csv`
**Mejor para:** Excel, Google Sheets

1. Abre el archivo directamente (se abre en Excel)
2. O clic derecho → "Abrir con" → Excel
3. Verás una tabla como esta:

| Nombre | Dirección | Teléfono | Latitud | Longitud |
|--------|-----------|----------|---------|----------|
| Petshop 1 | Carrera 1 #1 | +57 1234 | 5.057 | -75.488 |
| Petshop 2 | Calle 2 #2 | +57 5678 | 5.058 | -75.489 |

#### 📋 Opción 2: `petshops_resultados.json`
**Mejor para:** Procesamiento automático

Abre con cualquier editor de texto (VS Code, Notepad)

```json
[
  {
    "nombre": "Petshop 1",
    "direccion": "Carrera 1 #1",
    "telefono": "+57 1234",
    "latitud": "5.057",
    "longitud": "-75.488",
    "hora_extraccion": "2026-04-13 10:30:45"
  }
]
```

#### 📝 Opción 3: `scraper_log.txt`
**Mejor para:** Debugging (si algo falla)

Contiene todos los eventos y tiempos:
```
[2026-04-13 10:30:01] [INICIO] Scraper iniciado...
[2026-04-13 10:30:05] Iniciando Selenium WebDriver...
[2026-04-13 10:30:10] ✓ WebDriver iniciado correctamente
...
```

---

## 🔧 PASO 6: USAR LOS DATOS

### En Excel:
1. Abre `petshops_resultados.csv` en Excel
2. Puedes:
   - ✓ Ordenar por nombre
   - ✓ Filtrar por ubicación
   - ✓ Crear gráficos
   - ✓ Importar a base de datos

### En Google Sheets:
1. Abre Google Drive
2. Nuevo → Hoja de cálculo
3. Archivo → Importar
4. Carga el archivo CSV

### En Python:
```python
import json
import csv

# Leer JSON
with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    
for petshop in datos:
    print(f"{petshop['nombre']}: {petshop['telefono']}")

# O usar pandas
import pandas as pd
df = pd.read_csv('petshops_resultados.csv')
print(df.head())
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Problem 1: "Chrome se abre y se cierra inmediatamente"
**Causa:** Chrome no está instalado en ubicación estándar
**Solución:**
1. Instala Chrome desde https://www.google.com/chrome
2. Reinicia la computadora
3. Intenta de nuevo

### Problema 2: "ModuleNotFoundError: No module named 'selenium'"
**Causa:** Las dependencias no se instalaron
**Solución:**
```powershell
pip install selenium webdriver-manager
```

### Problema 3: "Pocos datos extraídos"
**Causa:** Google Maps limita resultados
**Solución:** 
- Aumenta scrolls en `PetshopRed.py`:
  ```python
  for intento in range(10):  # Cambiar de 5 a 10
  ```

### Problema 4: "El terminal dice 'Acceso denegado'"
**Causa:** Permisos del sistema
**Solución:**
1. Clic derecho en `PowerShell` → "Ejecutar como administrador"
2. Intenta de nuevo

### Problema 5: No aparecen direcciones/teléfonos
**Causa:** Google Maps no las muestra públicamente
**Solución:** Abre Google Maps directamente para verificar

---

## 🎓 APRENDER MÁS

### Antes de ejecutar:
- Lee el archivo `README.md` para entender qué hace cada parte

### Mientras ejecuta:
- Mira cómo Chrome interactúa automáticamente
- Lee los mensajes en la terminal para seguir el progreso

### Después de ejecutar:
- Revisa los datos extraídos
- Prueba usar los datos en Excel o Python

---

## 💡 CONSEJOS ÚTILES

✅ **Ejecutar múltiples búsquedas:**
```python
URL_MAPS = "https://www.google.com/maps/search/veterinario/@5.0572936,-75.4881471,16z/"
```
Solo cambia la palabra "petshop" por lo que quieras buscar

✅ **Aumentar velocidad:**
Disminuye tiempos de espera:
```python
ESPERA_PAGINA = 5  # Cambiar de 10 a 5
TIEMPO_SCROLL = 1  # Cambiar de 2 a 1
```

✅ **Obtener más resultados:**
Aumenta número de scrolls:
```python
for intento in range(10):  # Más scrolls = más datos
```

✅ **Ejecutar sin ver Chrome:**
Agrega esta línea en el código:
```python
opciones_chrome.add_argument('--headless')
```

---

## 📞 SI AÚN NO FUNCIONA

1. **Verifica TU conexión a internet** (abre Google Maps manualmente)
2. **Abre el archivo `scraper_log.txt`** para ver dónde falla
3. **Copia el mensaje de error** en Google Search
4. **Contacta** con soporte técnico

---

## 🎉 ¡ÉXITO!

Si llegaste hasta aquí, ¡el scraper está funcionando!

**Próximos pasos:**
- ✅ Analiza los datos en Excel
- ✅ Crea visualizaciones
- ✅ Exporta a tu base de datos
- ✅ Completa con más scraping

---

**Última actualización:** 2026-04-13  
**Versión:** 1.0  
**Estado:** ✅ Probado y funcional
