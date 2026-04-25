"""
Módulo para obtener el valor del dólar desde el Banco Central de Chile.
Utiliza Selenium para web scraping desde bcentral.cl
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# URL del Banco Central de Chile
URL_BCENTRAL = "https://www.bcentral.cl/inicio"


def obtener_dolar_selenium() -> float:
    """
    Obtiene el valor del dólar usando Selenium desde bcentral.cl.
    
    Returns:
        float: Valor del dólar en pesos chilenos (CLP)
    
    Raises:
        Exception: Si no se puede obtener el valor del dólar
    """
    # Configurar opciones de Chrome para modo headless
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navegar al sitio del Banco Central
        driver.get(URL_BCENTRAL)
        
        # Esperar a que cargue la página
        time.sleep(3)
        
        # Buscar el indicador del dólar
        # El Banco Central usually shows the dollar value in a specific section
        # Try multiple selectors to find the dollar value
        
        # Método 1: Buscar por texto que contenga "dólar" o "USD"
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ', 'abcdefghijklmnñopqrstuvwxyz'), 'dólar') or contains(translate(text(), 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ', 'abcdefghijklmnñopqrstuvwxyz'), 'dollar') or contains(translate(text(), 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ', 'abcdefghijklmnñopqrstuvwxyz'), 'usd')]"))
            )
            # Buscar el valor numérico cercano
            valor = buscar_valor_cercano(driver, elemento)
            if valor:
                return valor
        except TimeoutException:
            pass
        
        # Método 2: Buscar en tablas de indicadores económicos
        try:
            tablas = driver.find_elements(By.TAG_NAME, "table")
            for tabla in tablas:
                filas = tabla.find_elements(By.TAG_NAME, "tr")
                for fila in filas:
                    texto = fila.text.lower()
                    if "dólar" in texto or "dollar" in texto or "usd" in texto:
                        celdas = fila.find_elements(By.TAG_NAME, "td")
                        for celda in celdas:
                            texto_celda = celda.text.replace(".", "").replace(",", ".")
                            try:
                                valor = float(texto_celda)
                                if valor > 500:  # Valor razonable del dólar
                                    return valor
                            except ValueError:
                                continue
        except NoSuchElementException:
            pass
        
        # Método 3: Buscar en elementos con clases específicas
        try:
            # Buscar elementos que contengan valores numéricos grandes
            elementos = driver.find_elements(By.XPATH, "//*[contains(@class, 'indicador') or contains(@class, 'valor') or contains(@class, 'precio')]")
            for elem in elementos:
                try:
                    texto = elem.text.replace(".", "").replace(",", ".").replace("$", "").strip()
                    valor = float(texto)
                    if 500 < valor < 2000:  # Rango razonable para el dólar
                        return valor
                except ValueError:
                    continue
        except NoSuchElementException:
            pass
        
        # Si ninguno funciona, intentar con la API alternativa
        raise Exception("No se pudo encontrar el valor del dólar en bcentral.cl")
        
    finally:
        driver.quit()


def buscar_valor_cercano(driver, elemento) -> float:
    """
    Busca un valor numérico cercano a un elemento.
    
    Args:
        driver: Instancia del WebDriver
        elemento: Elemento de referencia
    
    Returns:
        float: Valor encontrado o None
    """
    try:
        # Buscar en elementos hermanos
        hermanos = elemento.find_elements(By.XPATH, "./following-sibling::* | ./preceding-sibling::*")
        for hermano in hermanos:
            texto = hermano.text.replace(".", "").replace(",", ".").replace("$", "").strip()
            try:
                valor = float(texto)
                if 500 < valor < 2000:
                    return valor
            except ValueError:
                continue
        
        # Buscar en elementos hijos
        hijos = elemento.find_elements(By.XPATH, ".//*")
        for hijo in hijos:
            texto = hijo.text.replace(".", "").replace(",", ".").replace("$", "").strip()
            try:
                valor = float(texto)
                if 500 < valor < 2000:
                    return valor
            except ValueError:
                continue
                
    except Exception:
        pass
    
    return None


def obtener_dolar_bcentral() -> float:
    """
    Obtiene el valor del dólar del día.
    Intenta primero con Selenium, si falla usa método alternativo.
    
    Returns:
        float: Valor del dólar en pesos chilenos (CLP)
    """
    try:
        return obtener_dolar_selenium()
    except Exception as e:
        print(f"Warning: Selenium no pudo obtener el dólar: {e}")
        # Fallback: intentar con API alternativa
        return obtener_dolar_api_fallback()


def obtener_dolar_api_fallback() -> float:
    """
    Método alternativo usando API pública.
    
    Returns:
        float: Valor del dólar en pesos chilenos (CLP)
    """
    try:
        import requests
        response = requests.get(
            "https://mindicador.cl/api",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return float(data["dolar"]["valor"])
    except Exception as e:
        print(f"Warning: API fallback también falló: {e}")
    
    # Valor de fallback si todo falla
    return 950.0


def obtener_dolar_fecha(fecha: str = None) -> float:
    """
    Obtiene el valor del dólar para una fecha específica.
    
    Args:
        fecha: Fecha en formato 'YYYY-MM-DD'. Si es None, usa la fecha actual.
    
    Returns:
        float: Valor del dólar en pesos chilenos (CLP)
    """
    if fecha is None:
        return obtener_dolar_bcentral()
    
    # Para fechas específicas, usar API
    try:
        import requests
        response = requests.get(
            f"https://mindicador.cl/api/dolar/{fecha}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return float(data["dolar"]["valor"])
    except Exception as e:
        print(f"Warning: No se pudo obtener el dólar para {fecha}: {e}")
        return 950.0


if __name__ == "__main__":
    # Prueba del módulo
    print("Obteniendo valor del dólar desde bcentral.cl usando Selenium...")
    try:
        dolar = obtener_dolar_bcentral()
        print(f"✓ Valor actual del dólar: ${dolar:.2f} CLP")
    except Exception as e:
        print(f"✗ Error: {e}")