"""
================================================================================
SCRAPER DE PETSHOPS - GOOGLE MAPS
================================================================================
Proyecto: Extracción de datos de petshops desde Google Maps
Objetivo: Obtener nombre, dirección, teléfono y ubicación de petshops
Autor: Sistema de Scraping
Fecha: 2026-04-13
================================================================================

DESCRIPCIÓN:
Este script automatiza la extracción de información de petshops desde Google Maps
usando Selenium para navegar la página y obtener los datos dinámicos.

DATOS A EXTRAER:
- Nombre del negocio
- Dirección completa
- Número de teléfono
- Coordenadas de ubicación (latitud, longitud)

REQUISITOS:
- selenium
- webdriver-manager
- pandas (para guardar en CSV)
- python 3.8+
================================================================================
"""

# ============================================================================
# PASO 1: IMPORTAR LIBRERÍAS NECESARIAS
# ============================================================================
import time
import json
import csv
import re
import os
import sys
from urllib.parse import quote
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import random

# ============================================================================
# PASO 2: CONFIGURACIÓN INICIAL
# ============================================================================

DEFAULT_SEARCH_TERM = "petshop"
DEFAULT_CITY = "Manizales, Caldas"

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("WDM_LOCAL", "0")

# Configuración de tiempo
ESPERA_PAGINA = 10  # segundos para esperar carga de elementos
TIEMPO_SCROLL = 2   # segundos entre scrolls
DELAY_PETICIONES = 2  # segundos entre peticiones (para no sobrecargar)
SCROLLS_RESULTADOS = 8

# Rutas de salida
ARCHIVO_JSON = BASE_DIR / "petshops_resultados.json"
ARCHIVO_CSV = BASE_DIR / "petshops_resultados.csv"
ARCHIVO_LOG = BASE_DIR / "scraper_log.txt"
DIRECTORIO_BUSQUEDAS = BASE_DIR / "busquedas"
DIRECTORIO_WDM = BASE_DIR / ".wdm"

SIMBOLOS_LOG = {
    "✓": "[OK]",
    "✗": "[ERROR]",
    "⚠": "[WARN]",
    "📍": "-",
    "☎️": "-",
    "🗺️": "-",
}


def construir_url_maps(termino_busqueda, ciudad=DEFAULT_CITY):
    partes = [(termino_busqueda or DEFAULT_SEARCH_TERM).strip()]
    if ciudad and ciudad.strip():
        partes.append(ciudad.strip())
    consulta = quote(" ".join(partes))
    return f"https://www.google.com/maps/search/{consulta}?entry=ttu"


def normalizar_nombre_busqueda(termino_busqueda, ciudad=DEFAULT_CITY):
    base = (termino_busqueda or DEFAULT_SEARCH_TERM).strip()
    if ciudad and ciudad.strip():
        base = f"{base} {ciudad.strip()}"
    texto = base.lower()
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE)
    texto = re.sub(r"[-\s]+", "_", texto, flags=re.UNICODE).strip("_")
    return texto or DEFAULT_SEARCH_TERM

# ============================================================================
# PASO 3: CREAR CLASE PARA MANEJAR EL SCRAPER
# ============================================================================

class ScraperPetshops:
    """
    Clase para gestionar el scraping de petshops desde Google Maps
    
    Métodos:
    - __init__: Inicializa el driver de Selenium
    - iniciar_driver: Abre el navegador Chrome
    - registrar_log: Guarda eventos en archivo de log
    - extraer_petshops: Realiza el scraping de petshops
    - procesar_datos: Limpia y organiza los datos extraídos
    - guardar_resultados: Guarda datos en JSON y CSV
    - cerrar_driver: Cierra el navegador
    """
    
    def __init__(self, termino_busqueda=DEFAULT_SEARCH_TERM, ciudad=DEFAULT_CITY):
        """Inicializa el scraper con variables vacías"""
        self.driver = None
        self.petshops = []
        self.termino_busqueda = (termino_busqueda or DEFAULT_SEARCH_TERM).strip()
        self.ciudad = (ciudad or DEFAULT_CITY).strip()
        self.slug_busqueda = normalizar_nombre_busqueda(self.termino_busqueda, self.ciudad)
        self.url_maps = construir_url_maps(self.termino_busqueda, self.ciudad)
        self.directorio_busqueda = DIRECTORIO_BUSQUEDAS / self.slug_busqueda
        self.archivo_json_busqueda = self.directorio_busqueda / "resultados.json"
        self.archivo_csv_busqueda = self.directorio_busqueda / "resultados.csv"
        self.marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.registrar_log(f"[INICIO] Scraper iniciado a las {self.marca_tiempo}")
        self.registrar_log(f"[BUSQUEDA] Termino: {self.termino_busqueda}")
        self.registrar_log(f"[CIUDAD] Ciudad: {self.ciudad}")
    
    def registrar_log(self, mensaje):
        """
        PASO 3.1: Registrar eventos en archivo de log
        
        Argumentos:
            mensaje (str): Mensaje a registrar
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_mensaje = f"[{timestamp}] {mensaje}"
        print(self._texto_consola(log_mensaje))
        
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
            f.write(log_mensaje + "\n")

    def _texto_consola(self, texto):
        """Convierte la salida a ASCII seguro para terminales Windows."""
        for origen, reemplazo in SIMBOLOS_LOG.items():
            texto = texto.replace(origen, reemplazo)
        return texto.encode("cp1252", errors="replace").decode("cp1252")

    def _resolver_chromedriver(self, ruta_instalada):
        """Asegura que Selenium reciba el ejecutable real de ChromeDriver."""
        ruta = Path(ruta_instalada)
        if ruta.name.lower() == "chromedriver.exe":
            return str(ruta)

        candidatos = sorted(ruta.parent.rglob("chromedriver.exe"))
        if candidatos:
            return str(candidatos[0])

        return str(ruta_instalada)

    def _obtener_texto_elemento(self, xpath):
        try:
            elemento = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            return ""

        texto = (elemento.text or "").strip()
        if texto:
            return texto

        for atributo in ("aria-label", "data-item-id", "content", "value"):
            valor = (elemento.get_attribute(atributo) or "").strip()
            if valor:
                return valor
        return ""

    def _limpiar_campo(self, valor, prefijos):
        texto = (valor or "").replace("\ue0c8", " ").replace("\n", " ").strip()
        if not texto:
            return "No disponible"

        for prefijo in prefijos:
            if texto.lower().startswith(prefijo.lower()):
                texto = texto[len(prefijo):].strip(" :")
        texto = re.sub(r"\s{2,}", " ", texto).strip(" -:")
        return texto or "No disponible"

    def _extraer_telefono_real(self):
        candidatos = []

        for xpath in [
            "//a[starts-with(@href, 'tel:')]",
            "//button[contains(@data-item-id, 'phone')]",
            "//button[contains(@aria-label, 'teléfono')]",
            "//button[contains(@aria-label, 'telefono')]",
            "//button[contains(@aria-label, 'phone')]",
        ]:
            texto = self._obtener_texto_elemento(xpath)
            if texto:
                candidatos.append(texto)

        try:
            panel_texto = self.driver.find_element(By.TAG_NAME, "body").text
            if panel_texto:
                candidatos.extend(panel_texto.splitlines())
        except Exception:
            pass

        patrones = [
            r"(\+?57[\s().-]*\d[\d\s().-]{7,}\d)",
            r"((?:\(?606\)?[\s().-]*)\d[\d\s().-]{5,}\d)",
            r"((?:3\d{2}|6\d{1,2})[\s().-]*\d[\d\s().-]{5,}\d)",
        ]

        for candidato in candidatos:
            texto = (candidato or "").strip()
            if not texto:
                continue

            texto_lower = texto.lower()
            if "enviar al teléfono" in texto_lower or "send to phone" in texto_lower:
                continue

            for patron in patrones:
                match = re.search(patron, texto)
                if match:
                    return match.group(1).strip()

        return ""

    def _extraer_desde_panel(self, item_id, terminos_aria):
        xpaths = [
            f"//button[contains(@data-item-id, '{item_id}')]",
            f"//button[@data-item-id='{item_id}']",
        ]
        for termino in terminos_aria:
            xpaths.append(
                "//*[@aria-label and contains("
                "translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ', 'abcdefghijklmnopqrstuvwxyzáéíóú'), "
                f"'{termino.lower()}')]"
            )

        for xpath in xpaths:
            texto = self._obtener_texto_elemento(xpath)
            if texto:
                return texto
        return ""

    def _esperar_panel_detalle(self, nombre, url_anterior=""):
        try:
            WebDriverWait(self.driver, ESPERA_PAGINA).until(
                lambda d: (
                    d.current_url != url_anterior
                    or nombre.lower() in (d.title or "").lower()
                    or nombre.lower() in self._obtener_texto_elemento("//h1")
                )
            )
        except Exception:
            time.sleep(1)

    def _extraer_coordenadas(self, url_actual):
        if "@" not in url_actual:
            return "No disponible", "No disponible"

        coords_str = url_actual.split("@", 1)[1].split(",")
        if len(coords_str) < 2:
            return "No disponible", "No disponible"

        latitud = coords_str[0].strip()
        longitud = coords_str[1].split("/")[0].strip()
        return latitud, longitud

    def _guardar_archivos_busqueda(self):
        self.directorio_busqueda.mkdir(parents=True, exist_ok=True)

        with open(self.archivo_json_busqueda, "w", encoding="utf-8") as f:
            json.dump(self.petshops, f, ensure_ascii=False, indent=4)

        if self.petshops:
            with open(self.archivo_csv_busqueda, "w", newline="", encoding="utf-8") as f:
                escritor = csv.DictWriter(f, fieldnames=self.petshops[0].keys())
                escritor.writeheader()
                escritor.writerows(self.petshops)
    
    def iniciar_driver(self):
        """
        PASO 3.2: Inicializar Selenium WebDriver
        
        - Descarga automáticamente ChromeDriver compatible
        - Configura opciones del navegador
        - Abre navegador Chrome
        """
        try:
            self.registrar_log("Iniciando Selenium WebDriver...")
            
            opciones_chrome = webdriver.ChromeOptions()
            # Opciones para mejorar compatibilidad y velocidad
            opciones_chrome.add_argument('--start-maximized')
            opciones_chrome.add_argument('--disable-blink-features=AutomationControlled')
            opciones_chrome.add_experimental_option("excludeSwitches", ["enable-automation"])
            opciones_chrome.add_experimental_option('useAutomationExtension', False)
            
            # Descargar e instalar ChromeDriver automáticamente
            DIRECTORIO_WDM.mkdir(parents=True, exist_ok=True)
            cache_manager = DriverCacheManager(root_dir=str(DIRECTORIO_WDM))
            driver_path = self._resolver_chromedriver(
                ChromeDriverManager(cache_manager=cache_manager).install()
            )
            servicio = Service(driver_path)
            self.driver = webdriver.Chrome(service=servicio, options=opciones_chrome)
            
            self.registrar_log("✓ WebDriver iniciado correctamente")
            
        except Exception as e:
            self.registrar_log(f"✗ Error al iniciar WebDriver: {str(e)}")
            raise
    
    def extraer_petshops(self):
        """
        PASO 4: EXTRAER INFORMACIÓN DE PETSHOPS
        
        Proceso:
        1. Acceder a la URL de Google Maps
        2. Esperar a que carguen los resultados
        3. Extraer cada resultado visible
        4. Hacer scroll para cargar más resultados
        5. Repetir hasta obtener todos los datos
        """
        try:
            self.registrar_log(f"Accediendo a Google Maps: {self.url_maps}")
            self.driver.get(self.url_maps)
            time.sleep(3)
            
            # Aceptar cualquier popup de cookies
            try:
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Acepto')]").click()
                time.sleep(1)
            except:
                pass
            
            self.registrar_log("✓ Página cargada correctamente")
            
            # Hacer scroll en el panel de resultados para cargar más elementos
            self.registrar_log("Extrayendo petshops...")
            petshops_extraidos = set()
            
            for intento in range(SCROLLS_RESULTADOS):
                self.registrar_log(f"  Scroll {intento + 1}/{SCROLLS_RESULTADOS}...")
                
                try:
                    # Obtener todos los items de resultados
                    # Google Maps usa divs con role="button" para los resultados
                    items = self.driver.find_elements(By.XPATH, "//div[@role='button' and contains(@class, 'result')]")
                    
                    if not items:
                        # Intenta selectores alternativos
                        items = self.driver.find_elements(By.XPATH, "//a[@href and contains(@href, '/maps/place')]/..")
                    
                    if not items:
                        # Otro selector más genérico
                        items = self.driver.find_elements(By.XPATH, "//div[@data-item-id]")
                    
                    self.registrar_log(f"    Encontrados {len(items)} elementos")
                    
                    for item in items:
                        try:
                            # Extraer texto del item
                            texto_completo = item.text
                            if not texto_completo or texto_completo in petshops_extraidos:
                                continue
                            
                            # Dividir nombre y detalles
                            lineas = texto_completo.split('\n')
                            nombre = lineas[0].strip() if lineas else ""
                            
                            if nombre and nombre not in petshops_extraidos:
                                petshops_extraidos.add(nombre)
                                
                                # Hacer click para obtener más detalles
                                url_antes = self.driver.current_url
                                try:
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                                    time.sleep(0.3)
                                    item.click()
                                    self._esperar_panel_detalle(nombre, url_antes)
                                except Exception:
                                    try:
                                        self.driver.execute_script("arguments[0].click();", item)
                                        self._esperar_panel_detalle(nombre, url_antes)
                                    except Exception:
                                        pass
                                
                                # Extraer información del panel de detalles
                                info_petshop = self.extraer_detalles_petshop(nombre)
                                if info_petshop:
                                    self.petshops.append(info_petshop)
                                    self.registrar_log(f"    ✓ {nombre}")
                        
                        except Exception as e:
                            pass
                    
                    # Scroll en el panel de resultados
                    try:
                        panel = self.driver.find_element(By.XPATH, "//div[@role='feed']")
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", panel)
                    except:
                        self.driver.execute_script("window.scrollBy(0, 500);")
                    
                    time.sleep(1)
                
                except Exception as e:
                    self.registrar_log(f"    Error en scroll {intento}: {str(e)}")
                    pass
            
            self.registrar_log(f"✓ Extracción completada: {len(self.petshops)} petshops encontrados")
            
        except Exception as e:
            self.registrar_log(f"✗ Error durante extracción: {str(e)}")
            # No relanzar excepción para continuar con guardado
    
    def extraer_detalles_petshop(self, nombre):
        """
        PASO 5: EXTRAER DETALLES ESPECÍFICOS DE CADA PETSHOP
        
        Extrae:
        - Nombre
        - Dirección
        - Teléfono
        - Ubicación (coordenadas)
        
        Argumentos:
            nombre (str): Nombre del petshop
            
        Retorna:
            dict: Diccionario con información del petshop
        """
        try:
            info = {
                "nombre": nombre,
                "busqueda": self.termino_busqueda,
                "ciudad": self.ciudad,
                "direccion": "No disponible",
                "telefono": "No disponible",
                "latitud": "No disponible",
                "longitud": "No disponible",
                "url_actual": self.driver.current_url,
                "hora_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            nombre_visible = self._obtener_texto_elemento("//h1")
            if nombre_visible and nombre_visible.strip().lower() not in {"resultados", "results"}:
                info["nombre"] = self._limpiar_campo(nombre_visible, [])

            direccion = self._extraer_desde_panel("address", ["dirección", "address"])
            if not direccion:
                direccion = self._obtener_texto_elemento("//button[contains(@aria-label, 'Dirección')]")
            if not direccion:
                direccion = self._obtener_texto_elemento("//button[contains(@aria-label, 'Address')]")
            info["direccion"] = self._limpiar_campo(direccion, ["Dirección", "Address"])

            telefono = self._extraer_desde_panel("phone", ["teléfono", "telefono", "phone"])
            if not telefono:
                telefono = self._obtener_texto_elemento("//a[starts-with(@href, 'tel:')]")
            if telefono:
                match = re.search(r"(\+?\d[\d\s().-]{6,}\d)", telefono)
                if match:
                    telefono = match.group(1).strip()
            info["telefono"] = self._limpiar_campo(telefono, ["Teléfono", "Telefono", "Phone", "Llamar al", "Call"])

            if "enviar al tel" in str(info["telefono"]).lower():
                telefono_real = self._extraer_telefono_real()
                if telefono_real:
                    info["telefono"] = telefono_real
                else:
                    info["telefono"] = "No disponible"

            latitud, longitud = self._extraer_coordenadas(info["url_actual"])
            info["latitud"] = latitud
            info["longitud"] = longitud
            
            return info
        
        except Exception as e:
            self.registrar_log(f"Error al extraer detalles: {str(e)}")
            return None
    
    def procesar_datos(self):
        """
        PASO 6: PROCESAR Y LIMPIAR DATOS
        
        - Eliminar duplicados
        - Validar información
        - Ordenar resultados
        """
        self.registrar_log("Procesando y limpiando datos...")
        
        # Eliminar duplicados basados en nombre
        petshops_unicos = {}
        for petshop in self.petshops:
            if petshop["nombre"] not in petshops_unicos:
                petshops_unicos[petshop["nombre"]] = petshop
        
        self.petshops = list(petshops_unicos.values())
        self.registrar_log(f"✓ Datos procesados: {len(self.petshops)} registros únicos")
    
    def guardar_resultados(self):
        """
        PASO 7: GUARDAR RESULTADOS EN ARCHIVOS
        
        Formato 1: JSON (estructura completa)
        Formato 2: CSV (formato tabular para hojas de cálculo)
        """
        try:
            self.registrar_log("Guardando resultados...")
            
            # Guardar en JSON
            with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
                json.dump(self.petshops, f, ensure_ascii=False, indent=4)
            self.registrar_log(f"✓ Archivo JSON guardado: {ARCHIVO_JSON}")
            
            # Guardar en CSV
            if self.petshops:
                with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
                    escritor = csv.DictWriter(f, fieldnames=self.petshops[0].keys())
                    escritor.writeheader()
                    escritor.writerows(self.petshops)
                self.registrar_log(f"✓ Archivo CSV guardado: {ARCHIVO_CSV}")

            self._guardar_archivos_busqueda()
            self.registrar_log(f"✓ Carpeta de búsqueda guardada: {self.directorio_busqueda}")
            
            # Mostrar resumen
            self.mostrar_resumen()
        
        except Exception as e:
            self.registrar_log(f"✗ Error al guardar resultados: {str(e)}")
    
    def mostrar_resumen(self):
        """
        PASO 8: MOSTRAR RESUMEN DE RESULTADOS
        """
        self.registrar_log("\n" + "="*70)
        self.registrar_log("RESUMEN DE EXTRACCIÓN")
        self.registrar_log("="*70)
        self.registrar_log(f"Total de petshops: {len(self.petshops)}")
        
        for i, petshop in enumerate(self.petshops, 1):
            self.registrar_log(f"\n{i}. {petshop['nombre']}")
            self.registrar_log(f"   📍 Dirección: {petshop['direccion']}")
            self.registrar_log(f"   ☎️  Teléfono: {petshop['telefono']}")
            self.registrar_log(f"   🗺️  Ubicación: ({petshop['latitud']}, {petshop['longitud']})")
        
        self.registrar_log("="*70 + "\n")
    
    def cerrar_driver(self):
        """
        PASO 9: CERRAR NAVEGADOR Y LIBERAR RECURSOS
        """
        if self.driver:
            self.driver.quit()
            self.registrar_log("✓ Navegador cerrado correctamente")
    
    def ejecutar(self):
        """
        PASO 10: ORQUESTAR TODO EL PROCESO
        
        Orden de ejecución:
        1. Iniciar WebDriver
        2. Extraer petshops
        3. Procesar datos
        4. Guardar resultados
        5. Cerrar navegador
        """
        try:
            self.iniciar_driver()
            self.extraer_petshops()
            self.procesar_datos()
            self.guardar_resultados()
        
        except Exception as e:
            self.registrar_log(f"✗ Error crítico: {str(e)}")
        
        finally:
            self.cerrar_driver()
            self.registrar_log("[FIN] Scraper finalizado\n")


# ============================================================================
# PASO 11: PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Execución principal del programa
    """
    print("\n" + "="*70)
    print("SCRAPER DE PETSHOPS - GOOGLE MAPS")
    print("="*70)
    print("Iniciando proceso de extraccion...\n")
    
    try:
        # Crear instancia del scraper
        scraper = ScraperPetshops()
        
        # Ejecutar el proceso completo
        scraper.ejecutar()
        
        print("\n[OK] Proceso completado exitosamente")
        print(f"Revisa los archivos: {ARCHIVO_JSON} y {ARCHIVO_CSV}")
        
    except KeyboardInterrupt:
        print("\n[WARN] Proceso interrumpido por el usuario")
    
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
