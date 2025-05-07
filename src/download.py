from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures

DOWNLOAD_DIR = r'C:\Users\Caio\Documents\Faculdade\github repositorios\testeteste\xlsx'

def download_file(url, selector_button_download, name_thread):

    print(f"[{name_thread}] Iniciando...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, selector_button_download))).click()
        time.sleep(10)
        print(f"[{name_thread}] Download concluído.")

    except Exception as e:
        print(f"[{name_thread}] Erro: {e}")
    finally:
        driver.quit()

sites = [
    {
        "url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?edicao=41053",
        "selector_button_download": '//*[@id="resultados"]/ul[2]/li[1]/strong/strong[1]/a',
        "name_thread": "população_por_sexo_e_idade_simples"
    },
    {
        "url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?edicao=41053",
        "selector_button_download": '//*[@id="resultados"]/ul[2]/li[2]/strong/strong[1]/a',
        "name_thread": "população_por_sexo_e_grupo_quiquenais"
    },
    {
        "url": "https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?edicao=41053",
        "selector_button_download": '//*[@id="resultados"]/ul[2]/li[3]/strong/strong[1]/a',
        "name_thread": "população_por_sexo_e_grupos_etarios_especificos"
    }
]

def run_threads():
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sites)) as executor:
        futures = [
            executor.submit(download_file, site["url"], site["selector_button_download"], site["name_thread"])
            for site in sites
        ]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Erro em uma das threads: {e}")