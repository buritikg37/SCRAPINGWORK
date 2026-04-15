# 📚 EJEMPLOS DE USO - DATOS EXTRAÍDOS

## 🎯 Cómo usar los datos después de ejecutar el scraper

Los datos se guardan en 3 formatos. Aquí hay ejemplos de cómo trabajar con cada uno.

---

## 📊 EJEMPLO 1: TRABAJAR CON CSV EN EXCEL

### Paso 1: Abrir el archivo
```
1. Haz doble clic en: petshops_resultados.csv
2. Se abrirá automáticamente en Excel
```

### Paso 2: Formato de tabla
```
| #  | Nombre              | Dirección                  | Teléfono      | Latitud  | Longitud    |
|----|---------------------|----------------------------|---------------|----------|-------------|
| 1  | Petshop La Mascota  | Carrera 1 #123, Medellín   | +57 4 123456  | 5.067    | -75.487     |
| 2  | Pet Store Elite     | Calle 2 #456, Medellín     | +57 4 789012  | 5.068    | -75.486     |
| 3  | Tienda de Mascotas  | Diagonal 3 #789, Medellín  | +57 4 345678  | 5.069    | -75.485     |
```

### Paso 3: Acciones en Excel
```
✓ Ordenar por nombre
✓ Filtrar por dirección
✓ Buscar teléfono específico
✓ Crear gráfico de ubicaciones
✓ Hacer gráficos de densidad
```

### Ejemplo: Filtrar por nombre
```
1. Haz clic en: Datos → Filtro automático
2. Haz clic en la flecha del encabezado "Nombre"
3. Selecciona solo los que quieras
4. Presiona OK
```

---

## 📋 EJEMPLO 2: TRABAJAR CON JSON EN PYTHON

### Cargar datos
```python
import json

# Abrir el archivo JSON
with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Ver cantidad de resultados
print(f"Total de petshops: {len(petshops)}")
```

**Resultado:**
```
Total de petshops: 15
```

### Imprimir todos los datos
```python
import json

with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

for petshop in petshops:
    print(f"\n{'='*50}")
    print(f"📱 {petshop['nombre']}")
    print(f"📍 {petshop['direccion']}")
    print(f"☎️  {petshop['telefono']}")
    print(f"🗺️  ({petshop['latitud']}, {petshop['longitud']})")
    print(f"🕐 Extraído: {petshop['hora_extraccion']}")
```

**Resultado:**
```
==================================================
📱 Petshop La Mascota
📍 Carrera 1 #123, Medellín
☎️  +57 4 123456
🗺️  (5.067, -75.487)
🕐 Extraído: 2026-04-13 10:30:45

==================================================
📱 Pet Store Elite
📍 Calle 2 #456, Medellín
☎️  +57 4 789012
🗺️  (5.068, -75.486)
🕐 Extraído: 2026-04-13 10:31:12
```

### Buscar un petshop específico
```python
import json

with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Buscar por nombre
nombre_buscar = "La Mascota"

for petshop in petshops:
    if nombre_buscar.lower() in petshop['nombre'].lower():
        print(f"✓ Encontrado: {petshop['nombre']}")
        print(f"  Teléfono: {petshop['telefono']}")
        print(f"  Dirección: {petshop['direccion']}")
        break
else:
    print(f"✗ No se encontró '{nombre_buscar}'")
```

**Resultado:**
```
✓ Encontrado: Petshop La Mascota
  Teléfono: +57 4 123456
  Dirección: Carrera 1 #123, Medellín
```

### Extraer solo teléfonos
```python
import json

with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

telefonos = [p['telefono'] for p in petshops if p['telefono'] != "No disponible"]

print("Teléfonos disponibles:")
for i, tel in enumerate(telefonos, 1):
    print(f"{i}. {tel}")
```

**Resultado:**
```
Teléfonos disponibles:
1. +57 4 123456
2. +57 4 789012
3. +57 4 345678
```

### Crear nuevo archivo filtrado
```python
import json

with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Filtrar solo con teléfono disponible
con_telefono = [p for p in petshops if p['telefono'] != "No disponible"]

# Guardar filtrado
with open('petshops_con_telefono.json', 'w', encoding='utf-8') as f:
    json.dump(con_telefono, f, ensure_ascii=False, indent=4)

print(f"Se guardaron {len(con_telefono)} petshops con teléfono")
```

**Resultado:**
```
Se guardaron 12 petshops con teléfono
```

---

## 🐼 EJEMPLO 3: TRABAJAR CON PANDAS (RECOMENDADO)

### Instalación
```bash
pip install pandas
```

### Cargar datos desde CSV
```python
import pandas as pd

# Cargar CSV
df = pd.read_csv('petshops_resultados.csv')

# Ver primeros 5 registros
print(df.head())

# Ver información general
print(df.info())

# Ver estadísticas
print(df.describe())
```

**Resultado:**
```
                    nombre                     direccion         telefono latitud  longitud
0     Petshop La Mascota  Carrera 1 #123, Medellín   +57 4 123456   5.067  -75.487
1       Pet Store Elite   Calle 2 #456, Medellín    +57 4 789012   5.068  -75.486
...

Info:
Total de registros: 15
Columnas: nombre, direccion, telefono, latitud, longitud, url_actual, hora_extraccion
```

### Filtrar y ordenar
```python
import pandas as pd

df = pd.read_csv('petshops_resultados.csv')

# Solo registros sin "No disponible"
df_con_datos = df[df['telefono'] != 'No disponible']
print(f"Registros completos: {len(df_con_datos)}")

# Ordenar por nombre
df_ordenado = df.sort_values('nombre')
print(df_ordenado)

# Solo nombre y teléfono
df_reducido = df[['nombre', 'telefono']]
print(df_reducido)
```

### Guardar datos filtrados
```python
import pandas as pd

df = pd.read_csv('petshops_resultados.csv')

# Filtrar
con_telefono = df[df['telefono'] != 'No disponible']

# Guardar como nuevo CSV
con_telefono.to_csv('petshops_con_telefono_filtered.csv', index=False)

# Guardar como Excel
con_telefono.to_excel('petshops_con_telefono.xlsx', index=False)

print(f"✓ Guardado: {len(con_telefono)} registros")
```

### Crear estadísticas
```python
import pandas as pd

df = pd.read_csv('petshops_resultados.csv')

print("=== ESTADÍSTICAS ===")
print(f"Total de petshops: {len(df)}")
print(f"Con teléfono: {len(df[df['telefono'] != 'No disponible'])}")
print(f"Sin teléfono: {len(df[df['telefono'] == 'No disponible'])}")
print(f"Con dirección: {len(df[df['direccion'] != 'No disponible'])}")
print(f"Sin dirección: {len(df[df['direccion'] == 'No disponible'])}")
```

**Resultado:**
```
=== ESTADÍSTICAS ===
Total de petshops: 15
Con teléfono: 12
Sin teléfono: 3
Con dirección: 14
Sin dirección: 1
```

---

## 🗺️ EJEMPLO 4: CREAR MAPA CON UBICACIONES

### Opción A: Google MyMaps (FÁCIL)

```
1. Abre: https://mymaps.google.com
2. Clic en: "+ Crear un mapa"
3. Nombre: "Petshops Medellín"
4. Para cada petshop:
   - Haz clic en: "+ Agregar marcador"
   - Ingresa la dirección o coordenadas
   - Título: nombre del petshop
   - Descripción: teléfono
5. Guarda
```

### Opción B: Python + Folium (CODE)

```bash
pip install folium
```

```python
import json
import folium

# Cargar datos
with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Crear mapa centrado en la primera ubicación
mapa = folium.Map(
    location=[float(petshops[0]['latitud']), float(petshops[0]['longitud'])],
    zoom_start=15
)

# Agregar marcador para cada petshop
for petshop in petshops:
    try:
        lat = float(petshop['latitud'])
        lon = float(petshop['longitud'])
        
        folium.Marker(
            location=[lat, lon],
            popup=petshop['nombre'],
            tooltip=f"{petshop['nombre']}: {petshop['telefono']}"
        ).add_to(mapa)
    except:
        pass

# Guardar mapa
mapa.save('petshops_mapa.html')
print("✓ Mapa guardado en: petshops_mapa.html")
```

Luego abre en Chrome: `petshops_mapa.html`

---

## 📧 EJEMPLO 5: ENVIAR CORREOS

```python
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cargar datos
with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Crear mensaje
mensaje = "PETSHOPS ENCONTRADOS:\n\n"
for petshop in petshops[:5]:  # Primeros 5
    mensaje += f"• {petshop['nombre']}\n"
    mensaje += f"  Teléfono: {petshop['telefono']}\n"
    mensaje += f"  Dirección: {petshop['direccion']}\n\n"

print(mensaje)
# Aquí iría código para enviar por email (requiere configuración)
```

---

## 💾 EJEMPLO 6: GUARDAR EN BASE DE DATOS

```python
import json
import sqlite3

# Crear base de datos
conexion = sqlite3.connect('petshops.db')
cursor = conexion.cursor()

# Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS petshops (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT,
        latitud REAL,
        longitud REAL,
        fecha TEXT
    )
''')

# Cargar datos
with open('petshops_resultados.json', 'r', encoding='utf-8') as f:
    petshops = json.load(f)

# Insertar datos
for petshop in petshops:
    cursor.execute('''
        INSERT INTO petshops 
        (nombre, direccion, telefono, latitud, longitud, fecha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        petshop['nombre'],
        petshop['direccion'],
        petshop['telefono'],
        petshop['latitud'],
        petshop['longitud'],
        petshop['hora_extraccion']
    ))

conexion.commit()
print(f"✓ {len(petshops)} registros guardados en base de datos")

# Consultar datos
cursor.execute('SELECT COUNT(*) FROM petshops')
total = cursor.fetchone()[0]
print(f"Total en base de datos: {total}")

conexion.close()
```

---

## 🔄 EJEMPLO 7: AUTOMATIZAR SCRAPING PERIÓDICO

```python
import schedule
import time
from datetime import datetime
import subprocess

def ejecutar_scraper():
    """Ejecutar scraper y guardar con fecha"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"[{timestamp}] Ejecutando scraper...")
    subprocess.run(['python', 'PetshopRed.py'])
    print(f"[{timestamp}] Scraper completado")

# Ejecutar cada día a las 10 AM
schedule.every().day.at("10:00").do(ejecutar_scraper)

# Ejecutar cada 6 horas
schedule.every(6).hours.do(ejecutar_scraper)

# Mantener en ejecución
print("Scheduler activo. Presiona Ctrl+C para detener")
while True:
    schedule.run_pending()
    time.sleep(60)
```

```bash
pip install schedule
```

---

## 📊 RESUMEN DE OPCIONES

| Tarea | Herramienta | Dificultad |
|-------|------------|-----------|
| Ver datos | Excel | ⭐ Fácil |
| Filtrar | Excel o Pandas | ⭐ Fácil |
| Crear mapa | Google MyMaps | ⭐ Fácil |
| Análisis avanzado | Pandas + Python | ⭐⭐ Medio |
| Base de datos | SQLite | ⭐⭐ Medio |
| Automatizar | Schedule | ⭐⭐⭐ Avanzado |

---

**Última actualización:** 2026-04-13  
**Versión:** 1.0
