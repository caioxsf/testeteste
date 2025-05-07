import matplotlib.pyplot as plt
import seaborn as sns
import os

class GraphicsData:
    def __init__(self, output_dir="visualizacoes"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set(style="whitegrid")

    def grafico_populacao_por_sexo(self, pop_total_por_sexo):
        plt.figure(figsize=(8, 6))
        sns.barplot(x=pop_total_por_sexo.index, y=pop_total_por_sexo.values, palette="pastel")
        plt.title("População Total por Sexo")
        plt.ylabel("População")
        plt.xlabel("Sexo")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/populacao_por_sexo.png")
        plt.close()

    def grafico_populacao_quinquenal_por_local(self, pop_quinquenal_total):
        top_10 = pop_quinquenal_total.sort_values(ascending=False).head(10)
        plt.figure(figsize=(10, 6))
        sns.barplot(y=top_10.index, x=top_10.values, palette="viridis")
        plt.title("Top 10 Locais com Maior População (Quinquenal)")
        plt.xlabel("População")
        plt.ylabel("Local")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/populacao_quinquenal_por_local.png")
        plt.close()

    def grafico_medias_etarias(self, medias_etarias):
        grupos = list(medias_etarias.keys())
        valores = list(medias_etarias.values())

        plt.figure(figsize=(10, 6))
        sns.barplot(x=grupos, y=valores, palette="Set2")
        plt.title("Média da População por Grupo Etário")
        plt.ylabel("População Média")
        plt.xlabel("Grupo Etário")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/media_populacao_etaria.png")
        plt.close()
