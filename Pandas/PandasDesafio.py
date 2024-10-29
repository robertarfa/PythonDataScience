import pandas as pd

url = "https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/desafios/alunos.csv"

dados = pd.read_csv(url)

dados.head(7)

dados.tail(5)

dados.shape

dados.columns

dados.info()

dados.describe()

dados.dtypes

#Verificar dados nulo
dados.isnull().sum()
#preencher com 0
dados = dados.fillna(0)
#remover Alice e Carlos
dados = dados.query("Nome != 'Alice' & Nome != 'Carlos'")
#filtrar apenas aprovados
aprovados = dados[dados["Aprovado"] == True]

aprovados.to_csv("alunos_aprovados.csv", index=False)

aprovados_new = pd.read_csv("alunos_aprovados.csv")

#substituir as notas 7 por 8
aprovados = aprovados.replace(7.0, 8.0)

aprovados