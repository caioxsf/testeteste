from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import zipfile
import threading
import time
import shutil
import gzip
import os

def download_file (dataset, name_file):
    print(f"[INFO] Iniciando download: {name_file}")
    response = requests.get(dataset)

    extensao = name_file.split('.')[-1]
    if extensao == 'csv':
        with zipfile(name_file, 'r') as zip:
            zip.printdir()
            zip.extractall()
    else:
         with open(name_file+'.csv', 'wb') as f:
            f.write(response.content)


def run_threads():
    datasets = [
        {
            "url": 'https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab1_idade_simples.xlsx',
            "name": 'DadosIBGE',
        },
        {
            "url": 'https://basedosdados.org/api/tables/downloadTable?p=YnJfYmRfZGlyZXRvcmlvc19icmFzaWw=&q=bXVuaWNpcGlv&d=dHJ1ZQ==&s=ZnJlZQ==',
            "name": 'DadosPrestadoresAguaEsgoto'
        }
    ]

    threads = []

    for data in datasets:
        t = threading.Thread(target=download_file, args=(data["url"], data["name"]))
        t.start()
        threads.append(t)    

    for t in threads:
        t.join()

def main():

    run_threads()

if __name__ == "__main__":
    main()
