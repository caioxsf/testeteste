from src.graphics import GraphicsData
import pandas as pd
import os 
import concurrent.futures

graphics_data = GraphicsData()


class AnalyzeData:
    def __init__(self, download_dir, arquivos):
        self.download_dir = download_dir
        self.arquivos = arquivos
        self.dataframes = {} 
    
    def carregar_dados(self):
        
        def read_files(nome, caminho):
            print(f"[{nome}] Carregando dados...")

            if nome in ["simples", "quiquenais"]:
                df = pd.read_excel(caminho, skiprows=5, engine="openpyxl")
            elif nome in ["etarios"]:
                df = pd.read_excel(caminho, skiprows=6, engine="openpyxl")
            else:
                df = pd.read_excel(caminho, engine="openpyxl")

            print(f"[{nome}] Linhas carregadas: {len(df)}")
            return nome, df

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for nome, arquivo in self.arquivos.items():
                caminho = os.path.join(self.download_dir, arquivo)
                futures.append(executor.submit(read_files, nome, caminho))

            for future in concurrent.futures.as_completed(futures):
                nome, df = future.result()
                self.dataframes[nome] = df

    def cruzar_dados(self):
        print("[CRUZAMENTO] Iniciando merge entre DataFrames...")

        df_simples = self.dataframes.get("simples")
        df_quinquenal = self.dataframes.get("quiquenais")
        df_etarios = self.dataframes.get("etarios")
        print(df_etarios.columns.tolist())
        
        df_simples_2024 = df_simples[["IDADE", "SEXO", "LOCAL", 2024]]
        df_quinquenal_2024 = df_quinquenal[["GRUPO ETÁRIO", "SEXO", "LOCAL", 2024]]

        df_simples_2024 = df_simples_2024.rename(columns={2024: "POP_SIMPLES"})
        df_quinquenal_2024 = df_quinquenal_2024.rename(columns={2024: "POP_QUINQUENAL"})

        df_merged = pd.merge(df_simples_2024, df_quinquenal_2024, on=["SEXO", "LOCAL"])

        pop_total_por_sexo = df_simples_2024.groupby("SEXO")["POP_SIMPLES"].sum()
        pop_quinquenal_total = df_quinquenal_2024.groupby("LOCAL")["POP_QUINQUENAL"].sum()
        media_masculina = df_simples_2024[df_simples_2024["SEXO"] == "Homens"]["POP_SIMPLES"].mean()

        df_etarios = self.dataframes.get("etarios")

        colunas_grupos = ["0-14_T", "15-59_T", "60+_T", "65+_T", "80+_T"]
        df_etarios[colunas_grupos] = df_etarios[colunas_grupos].apply(pd.to_numeric, errors="coerce")

        media_criancas_jovens = df_etarios["0-14_T"].mean()
        media_adultos = df_etarios["15-59_T"].mean()
        media_idosos_60 = df_etarios["60+_T"].mean()
        media_idosos_65 = df_etarios["65+_T"].mean()
        media_idosos_80 = df_etarios["80+_T"].mean()

        print("\n[MÉDIA POPULAÇÃO POR GRUPO ETÁRIO]")
        print(f"Crianças e Jovens (0-14): {media_criancas_jovens:.2f}")
        print(f"Adolescentes e Adultos (15-59): {media_adultos:.2f}")
        print(f"Idosos 60+: {media_idosos_60:.2f}")
        print(f"Idosos 65+: {media_idosos_65:.2f}")
        print(f"Idosos 80+: {media_idosos_80:.2f}")

        print("\n[POPULAÇÃO TOTAL POR SEXO]")
        print(pop_total_por_sexo)

        print("\n[POPULAÇÃO TOTAL POR LOCAL (QUINQUENAL)]")
        print(pop_quinquenal_total)

        print(f"\n[MÉDIA POPULAÇÃO MASCULINA - IDADE SIMPLES]: {media_masculina:.2f}")

        print("\n[MÉDIA POPULAÇÃO POR GRUPO ETÁRIO]")
        print(f"Crianças e Jovens (0-14): {media_criancas_jovens:.2f}")
        print(f"Adolescentes e Adultos (15-59): {media_adultos:.2f}")
        print(f"Idosos 60+: {media_idosos_60:.2f}")
        print(f"Idosos 65+: {media_idosos_65:.2f}")
        print(f"Idosos 80+: {media_idosos_80:.2f}")

        medias_etarias = {
            "0-14 (Crianças e Jovens)": media_criancas_jovens,
            "15-59 (Adultos)": media_adultos,
            "60+": media_idosos_60,
            "65+": media_idosos_65,
            "80+": media_idosos_80,
        }

        graphics_data.grafico_populacao_por_sexo(pop_total_por_sexo)
        graphics_data.grafico_populacao_quinquenal_por_local(pop_quinquenal_total)
        graphics_data.grafico_medias_etarias(medias_etarias)

        print(f"\n[✓] Gráficos salvos em: {graphics_data.output_dir}")




        