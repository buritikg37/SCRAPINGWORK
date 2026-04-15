print("Scraping environment is ready!")

#correr la terminal python scraper.py

#Para comprobar si se instaló correctamente, prueba lo siguiente

import requests
print(requests.__version__)

#Para nuestra primera solicitud, comprobaremos el código de estado HTTP de una página.

import requests

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)

print("Status Code:", response.status_code)

#Así pues, vamos a imprimir los primeros 500 caracteres del código fuente de la página para asegurarnos de que hemos obtenido el contenido correctamente.

import requests

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)

print("Page HTML Preview:", response.text[:500])

#Para verificar la instalación,importar la biblioteca y mostrar su versión.

#Para instalar BeautifulSoup y sus dependencias, ejecute:

from bs4 import BeautifulSoup
print(BeautifulSoup)

#extraer la <h1>etiqueta de la página
#soup = BeautifulSoup(response.text, "html.parser")convierte el HTML sin procesar en un objeto estructurado
#.find("h1")busca la primera <h1>etiqueta
#.get_text()extrae el contenido legible, eliminando las etiquetas HTML
#Y nos queda el título de la página.

import requests
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

h1_tag = soup.find("h1")
print("Page Title:", h1_tag.get_text())



#Extracción de nombres y capitales de países
#.find_all("div", class_="country")obtiene todos los bloques de países
#.find("h3", class_="country-name")encuentra el nombre del país
#.find("span", class_="country-capital")obtiene el capital
#.get_text(strip=True)garantiza una salida limpia, eliminando espacios adicionales
#Lo que estamos imprimiendo son los nombres y las capitales de todos los países en este sitio web de demostración.

countries = soup.find_all("div", class_="country")

for c in countries:
    name = c.find("h3", class_="country-name").get_text(strip=True)
    capital = c.find("span", class_="country-capital").get_text(strip=True)
    print("Country-name:", name, "| Capital:", capital)
    
    
#Exportación de datos a CSV
#CSV (valores separados por comas) es un formato común para hojas de cálculo y bases de datos.
#El módulo integrado de Python csvfacilita la escritura de datos estructurados en un archivo.
#Vamos a tomar la lista de nombres de países y capitales y guardarla en countries.csv:

#open("countries.csv", "w", newline="", encoding="utf-8")crea un nuevo archivo CSV
#writer.writerow(["Country", "Capital"])agrega una fila de encabezado
#El bucle extrae el nombre y la capital de cada país y luego los escribe como filas en el archivo CSV.

import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

countries = soup.find_all("div", class_="country")

# Open a new CSV file and write headers
with open("countries.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Country", "Capital"])

    # Loop through countries and write each row
    for c in countries:
        name = c.find("h3", class_="country-name").get_text(strip=True)
        capital = c.find("span", class_="country-capital").get_text(strip=True)
        writer.writerow([name, capital])

print("Data saved to countries.csv")



#Exportación de datos a JSON
#Después de CSV, el formato de exportación de datos más utilizado es JSON .
#JSON (JavaScript Object Notation) se utiliza ampliamente para API y para almacenar datos estructurados.
#Una vez más, el módulo de Python jsonsimplifica la tarea de escribir los datos recopilados en un .jsonarchivo.

#data.append({"country": name, "capital": capital})crea un diccionario para cada país
#json.dump(data, f, indent=4, ensure_ascii=False)lo escribe countries.jsonen un formato legible

import json
import requests
from bs4 import BeautifulSoup

url = "https://www.scrapethissite.com/pages/simple/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

countries = soup.find_all("div", class_="country")

# Create a list to store country data
data = []

for c in countries:
    name = c.find("h3", class_="country-name").get_text(strip=True)
    capital = c.find("span", class_="country-capital").get_text(strip=True)

    # Append dictionary to list
    data.append({"country": name, "capital": capital})

# Save data to a JSON file
with open("countries.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Data saved to countries.json")



#Carga de una página con un navegador sin interfaz gráfica
#Empecemos por lo sencillo: cargaremos una página web usando Playwright y comprobaremos que funciona.
#Este script abre un navegador en segundo plano, visita la página y la cierra. A diferencia de otros requests.get(), este sí renderiza la página como lo haría Chrome o Firefox.

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/simple/")
    print("Page loaded successfully")
    browser.close()
    
    
    
#Extracción de datos tras la ejecución de JavaScript
#Un navegador sin interfaz gráfica resulta realmente útil cuando un sitio web carga el contenido de forma dinámica.
#Para mostrar esto en acción, usemos Playwright para extraer el título de la página después de que JavaScript se haya ejecutado por completo .


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/simple/")

    # Wait for an element to be present before extracting content
    page.wait_for_selector("h1")

    # Get the page’s fully rendered HTML
    html_content = page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    h1_tag = soup.find("h1")
    print("Page Title:", h1_tag.get_text())

    browser.close()
    
    
    
    
    #Extracción de datos de una página renderizada con JavaScript
    #Algunos sitios web no cargan los datos inmediatamente, sino que los obtienen dinámicamente mediante AJAX.
    #Si intentáramos extraerlos con una solicitud normal, solo obtendríamos una respuesta parcial.
    #Para mostrar cómo los navegadores sin interfaz gráfica ayudan en situaciones en las que necesitamosextraer datos de una página renderizada con JavaScript, extraeremos datos deEsta lista de películas ganadoras del Oscar en 2015que carga contenido dinámicamente con JavaScript.    
    
    
    
    #Primero, intentemos obtener los datos de la tabla usando solo requests:
    
    import requests

url = "https://www.scrapethissite.com/pages/ajax-javascript/#2015"
response = requests.get(url)

print(response.text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.scrapethissite.com/pages/ajax-javascript/#2015")

    # Wait 3 seconds for JavaScript to load the content
    page.wait_for_Timeout(3000)

    # Get the fully rendered HTML
    html_content = page.content()
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the data
    print("Extracted Content:", soup.prettify())

    browser.close()