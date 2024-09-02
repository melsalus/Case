# -*- coding: utf-8 -*-
"""Case - Marketing

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_o8tXW8IfpGlGGhTS7WUVQx06b8c-s5b
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time


############################################
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

"""## Importação dos dados, Analise Exploratória e Tratamento de Dados"""

df_dados = pd.read_excel("ml_project1_data.xlsx")

df_dados.shape

df_dados.head()

df_dados.tail()

df_dados.info()

df_dados.isnull().sum()

df_dados.describe()

variaveis_numericas = []
for i in df_dados.columns[0:48].tolist():
        if df_dados.dtypes[i] == 'int64' or df_dados.dtypes[i] == 'float64':
            print(i, ':' , df_dados.dtypes[i])
            variaveis_numericas.append(i)

variaveis_numericas

n_vars = len(variaveis_numericas)
n_cols = 3
n_rows = int(np.ceil(n_vars / n_cols))

plt.rcParams["figure.figsize"] = [10.00, 15.00]
plt.rcParams["figure.autolayout"] = True

f, axes = plt.subplots(n_rows, n_cols)

linha = 0
coluna = 0

for i in variaveis_numericas:
    sns.boxplot(data = df_dados, y=i, ax=axes[linha, coluna])
    coluna += 1
    if coluna == n_cols:
        linha += 1
        coluna = 0

plt.show()


#variavel year-birth com outliers - não faz sentido
#avaliação boa, os dados fazem sentido

df_dados.loc[df_dados['Year_Birth'] < 1910]

df_novo = df_dados.loc[df_dados['Year_Birth'] >= 1910]
df_novo.loc[df_novo['Year_Birth'] < 1910]

df_novo.groupby(['Education']).size()

#Absurd e Yolo (me parece erro de preenchimento)
#Alone e Single = mesma classificação
df_novo.groupby(['Marital_Status']).size()

df_dados_limpos = df_novo.copy()

df_dados_limpos = df_dados_limpos[~df_dados_limpos['Marital_Status'].isin(['YOLO', 'Absurd'])]

df_dados_limpos['Marital_Status'].replace('Alone', 'Single', inplace=True)

df_dados_limpos.info()

df_dados_limpos.groupby(['Marital_Status']).size()

variaveis_categoricas = []
for i in df_dados_limpos.columns[0:48].tolist():
    if df_dados_limpos.dtypes[i].name in ['object', 'category']:
        print(i, ':' , df_dados_limpos.dtypes[i])
        variaveis_categoricas.append(i)

plt.rcParams["figure.figsize"] = [10.00, 20.00]
plt.rcParams["figure.autolayout"] = True

n_graficos = len(df_dados_limpos.columns)
n_colunas = 2
n_linhas = int(np.ceil(n_graficos / n_colunas))

f, axes = plt.subplots(n_linhas, n_colunas)

linha = 0
coluna = 0

for i in df_dados_limpos.columns:
    sns.countplot(data=df_dados_limpos, x=i, ax=axes[linha, coluna])

    coluna += 1
    if coluna == n_colunas:
        linha += 1
        coluna = 0

plt.tight_layout()
plt.show()


#achei bem ok a distribuição

#vou usar essa variavel como target
df_dados_limpos['Score'] = df_dados_limpos['AcceptedCmp1'] + df_dados_limpos['AcceptedCmp2'] + df_dados_limpos['AcceptedCmp3'] + df_dados_limpos['AcceptedCmp4'] + df_dados_limpos ['AcceptedCmp5'] + df_dados_limpos ['Response']

df_dados_limpos.info()

df_dados_limpos.groupby('Score').size()

"""## Pré Processamento dos Dados"""

lb = LabelEncoder()

df_dados_limpos['Education'] = lb.fit_transform(df_dados_limpos['Education'])
df_dados_limpos['Marital_Status'] = lb.fit_transform(df_dados_limpos['Marital_Status'])


df_dados.dropna(inplace = True)

df_dados_limpos.head()

df_dados_limpos.info()

target = df_dados_limpos.iloc[:,29]

target.value_counts()

preditoras = df_dados_limpos.copy()

del preditoras['Score']
del preditoras['ID']
del preditoras ['Dt_Customer']
del preditoras['Z_CostContact']
del preditoras['Z_Revenue']

preditoras.head()

X_treino, X_teste, y_treino, y_teste = train_test_split(preditoras, target, test_size = 0.3, random_state = 40)

# normalização em treino e teste
# Padronização
sc = MinMaxScaler()
X_treino_normalizados = sc.fit_transform(X_treino)
X_teste_normalizados = sc.transform(X_teste)

clf = RandomForestClassifier()

clf.get_params()

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import time


from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')

X_treino_normalizados = imputer. fit_transform(X_treino_normalizados)

n_estimators = np.array([100,150,200,250,300])
max_depth = np.array([10,20])
criterion = np.array(["gini"])
max_features = np.array(["sqrt", "log2", None])
min_samples_split = np.array([2, 5])
min_samples_leaf = np.array([1,2,3])
bootstrap = np.array([True,False])

grid_parametros = dict(n_estimators=n_estimators,
                       max_depth=max_depth,
                       criterion=criterion,
                       max_features=max_features,
                       min_samples_split=min_samples_split,
                       min_samples_leaf=min_samples_leaf,
                       bootstrap=bootstrap)

clf = RandomForestClassifier()

clf = GridSearchCV(clf, grid_parametros, cv = 3, n_jobs = 8)

inicio = time.time()
clf.fit(X_treino_normalizados, y_treino)
fim = time.time()

treinos = pd.DataFrame(clf.cv_results_)

print(f"Acurácia: {clf.best_score_ :.2%}")
print("")
print(f"Hiperparâmetros Ideais: {clf.best_params_}")
print("")
print("Tempo de Treinamento do Modelo: ", round(fim - inicio,2))
print("")
print("Numero de treinamentos realizados: ", treinos.shape[0])

treinos.head()

clf = RandomForestClassifier(n_estimators  = 300, criterion = 'gini', max_depth = 20, max_features = None,
                              min_samples_leaf = 1, min_samples_split = 5, bootstrap = True)

# Construção do modelo
clf = clf.fit(X_treino_normalizados, y_treino)

scores = clf.score(X_treino_normalizados,y_treino)
scores

# faz sentido?
plt.rcParams["figure.figsize"] = [10.00, 10.00]
plt.rcParams["figure.autolayout"] = True

importances = pd.Series(data=clf.feature_importances_, index=preditoras.columns)
importances = importances.sort_values(ascending = False)
sns.barplot(x=importances, y=importances.index, orient='h').set_title('Importância de cada variável')
plt.show()

importances.sort_values(ascending = False)

from sklearn.tree import export_graphviz
import graphviz
from IPython.display import Image, display


dot_data = export_graphviz(clf_tree.best_estimator_, out_file=None)

feature_names = ['Year_Birth', 'Education', 'Marital_Status', 'Income',
                 'Kidhome', 'Teenhome', 'Recency', 'MntFruits',
                 'MntWines', 'MntMeatProducts', 'MntFishProducts',
                 'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
                 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
                 'NumWebVisitsMonth', 'AcceptedCmp3', 'AcceptedCmp4',
                 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2',
                 'Complain', 'Response']

dot_data = export_graphviz(clf_tree.best_estimator_,
                           out_file=None,
                           feature_names=feature_names,
                           class_names=['0', '1', '2', '3', '4', '5', '6'],
                           filled=True,
                           rounded=True,
                           special_characters=True,
                           max_depth=3)


graph = graphviz.Source(dot_data)
display(graph)

#teste modelo 1
imputer = SimpleImputer(strategy='mean') # or other strategy like 'median'
X_treino = imputer.fit_transform(X_treino)

clf.fit(X_treino, y_treino)

Year_Birth =  1980
Education = 3
Marital_Status = 1
Income =  36640
Kidhome =  0
Teenhome =  0
Recency =  23
MntFruits =  11
MntWines =  80
MntMeatProducts = 15
MntFishProducts = 45
MntSweetProducts = 11
MntGoldProds =  7
NumDealsPurchases = 2
NumWebPurchases =  5
NumCatalogPurchases = 20
NumStorePurchases = 1
NumWebVisitsMonth =  4
AcceptedCmp3 =  0
AcceptedCmp4 =  1
AcceptedCmp5 =  1
AcceptedCmp1 =  0
AcceptedCmp2 =  0
Complain =  1
Response =  1

novos_dados =[Year_Birth ,
Education ,
Marital_Status ,
Income ,
Kidhome ,
Teenhome ,
Recency ,
MntFruits ,
MntWines ,
MntMeatProducts ,
MntFishProducts ,
MntSweetProducts ,
MntGoldProds ,
NumDealsPurchases ,
NumWebPurchases ,
NumCatalogPurchases ,
NumStorePurchases ,
NumWebVisitsMonth ,
AcceptedCmp3 ,
AcceptedCmp4 ,
AcceptedCmp5 ,
AcceptedCmp1 ,
AcceptedCmp2 ,
Complain ,
Response
]

x =np.array(novos_dados).reshape(1,-1)
x = sc.transform(x)


print("Cliente possibilidade:", clf.predict(x))