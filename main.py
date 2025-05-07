from src.download import run_threads
from src.analyze_data import AnalyzeData

DOWNLOAD_DIR = r'C:\Users\Caio\Documents\Faculdade\github repositorios\testeteste\xlsx'

arquivos = {
    "simples": "projecoes_2024_tab1_idade_simples.xlsx",
    "quiquenais": "projecoes_2024_tab2_grupo_quinquenal.xlsx",
    "etarios": "projecoes_2024_tab3_grupos_etarios_especificos.xlsx"
}

def main():
    run_threads()
    analise = AnalyzeData(DOWNLOAD_DIR, arquivos)
    analise.carregar_dados()
    analise.cruzar_dados()

if __name__ == "__main__":
    main()