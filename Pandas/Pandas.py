import pandas as pd

dados = pd.read_csv("https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv", delimiter=";")

dados.head()

dados.tail()

type(dados)

dados.shape
# linhas 32960
# colunas 9

dados.columns

dados.info()

# Series (indices e valores)
dados['Tipo']

dados[['Quartos', 'Valor']]

#Quais os valores médios de aluguel por tipo de imóvel?
dados['Valor'].mean()
#mean(numeric_only=True) para pegar somente colunas de numeros
df_preco_tipo = dados.groupby('Tipo')[['Valor']].mean().sort_values('Valor')

df_preco_tipo.plot(kind='barh', figsize=(14,10), color='purple')

#analisar Tipos unicos - lista todos os tipos de imóveis
dados.Tipo.unique()

imoveis_comerciais = ['Conjunto Comercial/Sala', 
                      'Prédio Inteiro', 'Loja/Salão', 
                      'Galpão/Depósito/Armazém', 
                      'Casa Comercial', 'Terreno Padrão',
                      'Loja Shopping/ Ct Comercial',
                      'Box/Garagem', 'Chácara',
                      'Loteamento/Condomínio', 'Sítio',
                      'Pousada/Chalé', 'Hotel', 'Indústria']

#filtrar os dados e tirar os imoveis comerciais                                            
df_residenciais = dados.query('@imoveis_comerciais not in Tipo')

df_residenciais.Tipo.unique()

df_preco_tipo = df_residenciais.groupby('Tipo')[['Valor']].mean().sort_values('Valor')

df_preco_tipo.plot(kind='barh', figsize=(14,10), color='purple')

# df_residenciais.query('Suites >= 1')

#Qual o percentual de cada tipo de imóvel na nossa base de dados?
# percentual_tipo = df_residenciais.groupby('Tipo')['Tipo'].count() / df_residenciais['Tipo'].count() * 100
df_percentual_tipo = dados.Tipo.value_counts(normalize=True).to_frame().sort_values('proportion')
# Alterando o nome da coluna "Proportion" para "Percentuais"
dados.rename(columns={'proportion': 'Percentual'}, inplace=True)

# Visualizando o DataFrame
df_percentual_tipo

df_percentual_tipo.plot(kind='bar', figsize=(14,10), color='green', xlabel="Tipos", ylabel="Percentual")

#como é desproporcional o valor entre casas e apartamentos, vamos filtrar somente apartamentos
df_apartamentos_only = df_residenciais.query('Tipo == "Apartamento"')

# #média de quartos 2.48
# df_apartamentos_only['Quartos'].mean()

# #Conferir quantos bairros únicos existem na nossa base de dados
# dados['Bairro'].nunique()
# len(dados['Bairro'].unique())

# top_cinco_valor_bairro = dados.groupby("Bairro")[['Valor']].mean().sort_values("Valor", ascending=False).head(5)

# top_cinco_valor_bairro.plot(kind='barh', figsize=(14,10), color='green', xlabel="Tipos", ylabel="Percentual")

#Verificar valores nulos
df_apartamentos_only.isnull().sum()

#Tratar valores nulos, como todos as colunas são númericas, iremos apenas substituir o nulo por 0
df_apartamentos_only = df_apartamentos_only.fillna(0)
df_apartamentos_only.isnull().sum()

#Remover apartamentos com valor igual a 0
#Remover apartamentos com condomínio igual a 0
valor_igual_zero = df_apartamentos_only.query("Valor == 0 | Condominio == 0")

#pegar o indice das linhas que desejamos remover
valor_igual_zero.index

#remover as linhas com os indices, axis= 0 remover linhas, inplace => alterações sejam aplicadas diretamente no Dataframe
df_apartamentos_only.drop(valor_igual_zero.index, axis=0, inplace=True)
#verificar
df_apartamentos_only.query("Valor == 0 | Condominio == 0")

df_apartamentos_only.Tipo.unique()

#remover coluna apartamento
df_apartamentos_only.drop("Tipo", axis=1, inplace=True)

#Aplicar os filtros necessários
# 1. Apartamentos que possuem 1 quarto e aluguel menor que R$ 1200;
# item_1 = df_apartamentos_only.query("Quartos == 1 & Valor < 1200")

quarto_1 = df_apartamentos_only["Quartos"] == 1
aluguel_1200 = df_apartamentos_only["Valor"] < 1200

item_1 = df_apartamentos_only[quarto_1 & aluguel_1200]

# 2. Apartamentos que possuem pelo menos 2 quartos, aluguel menor que R$ 3000 e área maior que 70 m².
condicao2 = (df_apartamentos_only['Quartos'] >= 2) & (df_apartamentos_only['Valor'] < 3000) & (df_apartamentos_only["Area"] > 70)

item_2 = df_apartamentos_only[condicao2]

#Salvar o dataframe completo após todas as modificações
df_apartamentos_only.to_csv("dados_apartamentos.csv", index=False, sep=";")

#Gerou uma coluna de index Unnamed:0, para evitar isso precisa adicionar index=False
new_data = pd.read_csv(
  "D:\OneDrive\CURSOS\PROJETOS\Dados\PythonDataScience\Pandas\dados_apartamentos.csv",
  sep=";")


item_1.to_csv("dados_apartamentos_item_1.csv", index=False, sep=";")
item_2.to_csv("dados_apartamentos_item_2.csv", index=False, sep=";")

new_data_item_1 = pd.read_csv(
  "D:\OneDrive\CURSOS\PROJETOS\Dados\PythonDataScience\Pandas\dados_apartamentos_item_1.csv",
  sep=";")

new_data_item_2 = pd.read_csv(
  "D:\OneDrive\CURSOS\PROJETOS\Dados\PythonDataScience\Pandas\dados_apartamentos_item_2.csv",
  sep=";")


# Criar coluna valor_por_mes
dados.info()
dados['valor_por_mes'] = dados['Valor'] + dados['Condominio']
# Criar coluna valor_por_ano
dados['valor_por_ano'] = (dados['valor_por_mes'] * 12) + dados["IPTU"]
dados.head()

#Criar a coluna de descrição
dados['descricao'] = dados['Tipo'] + ' em ' + dados['Bairro'] + ' com ' + \
                     dados['Quartos'].astype(str) + ' quarto(s) ' + \
                     " e " + dados['Vagas'].astype(str) + ' vaga(s) de garagem.'


#Criar a coluna possui_suite, o x é cada linha da coluna suites
dados['possui_suite'] = dados['Suites'].apply(lambda x: "Sim" if x > 0 else "Não")
dados.tail()

dados.to_csv("dados_completos_dev.csv", index=False, sep=';')

new_dados = pd.read_csv("dados_completos_dev.csv", sep=';')