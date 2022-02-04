# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mlj9hkHyPX7AiYvmwCotn0UeSJNAImuL

<h1> Doenças Coronárias </h1>

#Import
"""

# Bibliotecas de manipulação de dados
import pandas as pd
import numpy as np 
# Gráficos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 
import matplotlib.gridspec as gridspec
# Machine Learning
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier 
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier, train
from sklearn.neural_network import MLPClassifier
# Métricas de avaliação dos modelos
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, classification_report, plot_confusion_matrix
from sklearn.model_selection import GridSearchCV

"""Importando os dados"""

df = pd.read_csv("heart.csv")
df.head()

df.tail()

df.shape

df.columns

df.info()

df.describe(percentiles=[0.1, 0.25, 0.75, 0.9])

"""# Análise Exploratória dos Dados

Entender cada coluna no conjunto de dados e verificar cada variável. 

No conjunto de dados, checar se contém:
*   Valores Nulos;
*   Valores Duplicados;
*   Outliers.
"""

# Nulos
df.isnull().sum()

# Duplicados
df.duplicated().sum()

df = df.drop_duplicates()

"""Qual variável é discreta? Qual variável é contínua?"""

df.nunique()

"""*   Discreta: cp, fbs, restecg, thal, slope, ca
*   Continua: age, trestbps, chol, thalach, olpeak
*   categórica: sex, exang  

Responder essa pergunta é importante para saber qual o melhor tipo de gráafico para cada coluna.

**Transformar as variávies continuas  in categorica and Discreta.**
"""

for i in df.columns:
    sns.histplot(x=i,data=df, hue='target',kde=True, element="step")  
    plt.figure()

# Verificando os quartis de distribuição. 
Q1=df[["age", "trestbps", "chol", "thalach", "oldpeak"]].quantile(0.25)
Q3=df[["age", "trestbps", "chol", "thalach", "oldpeak"]].quantile(0.75)
IQR=Q3-Q1
print("Q1", Q1)
print("Q3", Q3)
print("IQR", IQR)
lower_bound = Q1-1.5*IQR
upper_bound = Q3+1.5*IQR
print("Normal Range", lower_bound, "-", upper_bound)

# Checar os outliers  nas variávies contínuas  
#age, trestbps, chol, thalach, olpeak

def draw_boxplots(df, selected_features):
  n = len(selected_features)
  fig = plt.figure(constrained_layout=True, figsize=(10, 20))
  gs = gridspec.GridSpec(int(n/5) + 1, 5, figure=fig)
  for i in range(n):
    k = int(i / 5)
    j = i % 5
    col = selected_features[i]
    ax = fig.add_subplot(gs[k, j])
    ax.set_title(col)
    ax.boxplot(df[col])

draw_boxplots(df, ["age", "trestbps","chol",  "thalach", "oldpeak"])

"""Na coluna de Age não tem outliers, mas nas outras colunas tem! Como tratar? Melhor tratar pela mediana."""

median = np.median(df)

df["trestbps"] = df["trestbps"].mask(df["trestbps"] > 170, median)
median = df.loc[df["trestbps"]<170, "trestbps"].median()
df.loc[df.trestbps > 170, "trestbps"] = np.nan

df["chol"] = df["chol"].mask(df["chol"] > 350, median)
median = df.loc[df["chol"]<350, "chol"].median()
df.loc[df.chol > 350, "chol"] = np.nan

df["thalach"] = df["thalach"].mask(df["thalach"] < 80, median)
median = df.loc[df["thalach"]<80, "thalach"].median()
df.loc[df.thalach < 80, "thalach"] = np.nan

df["oldpeak"] = df["oldpeak"].mask(df["oldpeak"] > 4.0, median)
median = df.loc[df["oldpeak"]< 4.0, "oldpeak"].median()
df.loc[df.oldpeak > 4.0, "oldpeak"] = np.nan

for i in df.columns:
    df[df.columns].boxplot(i)
    plt.figure()

"""## Data Understanding

Entendendo os dados



*   cp = tipo de dor no peito;  
*   trestbps = pressão arterial;
*   chol = cholesterol (mg/dl);
*   fbs = Nível de açucar no sangue (diabetes);
*   restecg = eletreocardiograma resultados; 
*   thlach = heart rate archieved; 
*   exang = exercicios angina; 
*   oldpeak: Depressão de ST induzida por exercício em relação ao repouso;
*   slope: Tipo de inclinação do segmento ST de pico do exercício;
*   ca: número de vasos sanguínios ressaltados (coloridos por fluoroscopia);
*   thal: Talassemia -> 3 = normal; 6 = fixed defect; 7 = reversable defect;
*   target: alvo; 1 = doente, 0 = não doente.

What features can ben created? Is better try to work with the continuous data and create an categorical data. 

*  "age", 
*  trestbps "chol", "thalach", "oldpeak"
"""

df["sex"].groupby(df["target"]).mean()

df.groupby(df["sex"]).mean()

"""### Data Construction """

df["senior"] ='standard'
df.loc[df["age"] >= 55, "senior"]  ='senior'
df.loc[df["age"] <= 55, "senior"]  ='young'

df["hchol"] ='standard'
df.loc[df["chol"] >= 200, "hchol"]  ='high'
df.loc[df["chol"] < 200, "hchol"]  ='low'

df['hbp'] = df['trestbps'].apply(lambda x: 'high' if x >= 140.0  else 'standard')
df['hbpm'] = df['thalach'].apply(lambda x: 'high' if x >= 140.0  else 'standard')

"""Now the new features have been created we must to transform this data binary type"""

df['senior']= df['senior'].map({'young':0, 'senior':1})
df['hchol']= df['hchol'].map({'low':0, 'high':1})
df['hbp']= df['hbp'].map({'standard':0, 'high':1})
df['hbpm']= df['hbpm'].map({'standard':0, 'high':1})

"""### Data Tranformation"""

df['age'] = df['age'].astype(float)
df['cp'] = df['cp'].astype(float)
df['slope'] = df['slope'].astype(float)
df['thal'] = df['thal'].astype(float)

df['trestbps'] = df['trestbps'].astype(float)
df['chol'] = df['chol'].astype(float)
df['thalach'] = df['thalach'].astype(float)

df['senior']= df['senior'].astype(float)
df['hchol']= df['hchol'].astype(float)
df['hbp']= df['hbp'].astype(float)
df['hbpm']= df['hbpm'].astype(float)

df["exang"] = df['exang'].astype(float)
df["fbs"] = df['fbs'].astype(float)
df["sex"] = df['sex'].astype(float) 
df["restecg"] = df['restecg'].astype(float)

df.dtypes

"""# Data Visualization

In this part of the code I will not create beautiful charts, but I want to check how the data in raw stage.
"""

df_corr = df.corr()
df_corr

fig, ax = plt.subplots(figsize=(20,12))
sns.heatmap(df_corr, annot = True)

sns.pairplot(df)

"""# Machine Learning

Comece por modelos simples e depois aprimore a complexidade dos modelos. Então, comece por modelos como árvore de decisão até modelos de Deep Learning.

### Modeling
"""

df = df.dropna()

#Pacient 
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=42) 


models = {'Decision Tree':     DecisionTreeClassifier(criterion="entropy"),  
          'Extra Tree':        ExtraTreesClassifier(n_estimators=200, random_state=0),  
          'Random Forest':     RandomForestClassifier(bootstrap=  False, criterion= "entropy",max_depth= 3,max_features= 'log2',min_samples_split= 3,n_estimators= 50),   
          'XGBoost':           XGBClassifier(model_learning_rate=0.001, model_max_depth=3,model_n_estimators=100), 
          'AdaBoost':          AdaBoostClassifier(n_estimators=100, random_state=0),  
          'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),  
          'Redes Neurais':     MLPClassifier(hidden_layer_sizes=(100, 50, 10), max_iter=1000)}  

for reg, modelo in zip(models.values(),models.keys()):
  regressor = reg
  regressor.fit(X_train, y_train)
  y_pred = regressor.predict(X_test)
  print(modelo)
  print(f"Acccuracy: {accuracy_score(y_test, y_pred)*100}%")
  print(f"Precision: {precision_score(y_test, y_pred)*100}%")
  print(f"Recall: {recall_score(y_test, y_pred)*100}%")
  print(f"F1: {f1_score(y_test, y_pred)*100}%")
  print('-----------------------------------')

"""Hiperparâmetros"""

# Verificando no XGBoost 
model = XGBClassifier()
param = dict(model_max_depth=[3,5,7], model_learning_rate=[0.001,0.01, 0.1], model_n_estimators=[100,500])

cv = GridSearchCV(model, param_grid=param, cv=10)
cv.fit(X_train, y_train)
test_pred = cv.predict(X_test)
cv.best_estimator_

# Verificando no Random Forest
params_grid = {'n_estimators':[100, 150, 200, 250, 500],
               'criterion':['gini', 'entropy'],
               'max_depth':[None, 1, 2, 3],
               'min_samples_split':[1, 2, 3],
               'max_features':['auto', 'sqrt', 'log2', 2, 3, 4, 5],
               'bootstrap':[True, False]}

RFC = RandomForestClassifier()

grid_search_rfc = GridSearchCV(RFC, param_grid=params_grid, cv=3, n_jobs=-1, verbose=2)

grid_search_rfc.fit(X_train, y_train)

grid_search_rfc.best_params_

clf_best_rfc = grid_search_rfc.best_estimator_
y_pred_rf = clf_best_rfc.predict(X_test)
print(round(f1_score(y_test, y_pred_rf, average='weighted')*100, 2))
print(classification_report(y_test, y_pred_rf))

plot_confusion_matrix(clf_best_rfc, X_test, y_test, values_format='d')
plt.grid(False)
plt.show()

"""# Conclusão

O trabalho de feature engeneering não ajudou muito o modelo de classificação a performar melhor. É necessário reavaliar o comportamento das variáveis em relação ao target.

\
"""
# My model
pickle_in = open('Heartbetting.pkl', 'rb') 
Heartbetting = pickle.load(pickle_in)


#-------------------------------------------------------------
#           TEMPLATE DO STREAMLIT APP
#-------------------------------------------------------------
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

# função para carregar o dataset
@st.cache(allow_output_mutation=True)
def get_data():
    return pd.read_csv('diabetes_data_upload.csv')

# função para treinar o modelo
def train_model():
    x = test_size
    data = get_data()
    # transformando os atributos em dados categóricos
    from sklearn.preprocessing import LabelEncoder 
    objectList = data.select_dtypes(include = 'object').columns
    le = LabelEncoder()
    for i in objectList:
        data[i] = le.fit_transform(data[i])

    # mapa de correlação
    corr = data.corr()['class']

    #Separando as variaveis de entrada e saída
    X = data.drop(["class"],axis=1)
    y = data["class"]
    
    # padronização da coluna Age
    from sklearn.preprocessing import MinMaxScaler
    mm = MinMaxScaler()
    X[['Age']] = mm.fit_transform(X[['Age']])
  
    #Separando os Dados de Treino e de Teste
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X ,y, test_size=x) 

    #Treinamento dos modelos
    modelos = ['SVC','Random Forest','KNeighbors','LogisticRegression','Naive_Bayes',]

    column_names = ["Modelo","Acuracia","Precisao","Recall","F1",
                        "Total_Positivos","Total_Negativos", "Falsos_Positivos", "Falsos_Negativos",
                        "Classificador"]
    results = pd.DataFrame(columns = column_names)

    for i in range(0,len(modelos)):
        
        if i == 0:
            from sklearn.svm import SVC
            classifier = SVC(kernel='linear', gamma= 1e-5, C=10,random_state=7)
         
        elif  i == 1:
            from sklearn.ensemble import RandomForestClassifier
            classifier = RandomForestClassifier(n_estimators=100)
    
        elif  i == 2:
            from sklearn.neighbors import KNeighborsClassifier
            classifier = KNeighborsClassifier(n_neighbors=30)
    
        elif  i == 3:
            from sklearn.linear_model import LogisticRegression
            start_time = time.time()
            classifier = LogisticRegression()
            time_train = time.time() - start_time
    
        elif  i == 4:
            from sklearn.naive_bayes import GaussianNB
            start_time = time.time()
            classifier = GaussianNB()
            time_train = time.time() - start_time
    
        # Treinamento
        start_time = time.time()
        classifier.fit(X_train,y_train)
        time_train = time.time() - start_time
        
        # Teste
        start_time = time.time()
        y_pred = classifier.predict(X_test)
        time_test = time.time() - start_time
    
        from sklearn import metrics
        acc = metrics.accuracy_score(y_test, y_pred)*100
        prc = metrics.precision_score(y_test, y_pred)*100
        rec = metrics.recall_score(y_test, y_pred)*100
        f1 = metrics.f1_score(y_test, y_pred)*100
    
        from sklearn.metrics import confusion_matrix, plot_confusion_matrix
        cm = confusion_matrix(y_test,y_pred)
        tn, fp, fn, tp = cm.ravel()      
        
        data = [[modelos[i],acc, prc, rec, f1, tp, tn, fp, fn, classifier,time_train,time_test]]
        column_names = ["Modelo","Acuracia","Precisao","Recall","F1",
                        "Total_Positivos","Total_Negativos", "Falsos_Positivos", "Falsos_Negativos",
                        "Classificador", "Tempo_Treino","Tempo_Teste"]
        model_results = pd.DataFrame(data = data, columns = column_names)
        results = results.append(model_results, ignore_index = True)

    return results, corr

# criando um dataframe
data = get_data()


st.sidebar.subheader("Atributos de Análise")

# mapeando dados do usuário para cada atributo
In1 =  st.sidebar.number_input("Idade", min_value=20,max_value=65,step=1)
In2 =  st.sidebar.selectbox("Gênero:", ["Masculino","Femenino"])
In3 =  st.sidebar.selectbox("Poliúria:",["Não","Sim"])
In4 =  st.sidebar.selectbox("Polidipsia:",["Não","Sim"])
In5 =  st.sidebar.selectbox("Perda repentina de peso:",["Não","Sim"])
In6 =  st.sidebar.selectbox("Fraqueza:",["Não","Sim"])
In7 =  st.sidebar.selectbox("Polifagia:",["Não","Sim"])
In8 =  st.sidebar.selectbox("Tordo genital:",["Não","Sim"])
In9 =  st.sidebar.selectbox("Embaçamento visual:",["Não","Sim"])
In10 = st.sidebar.selectbox("Coceira:",["Não","Sim"])
In11 = st.sidebar.selectbox("Irritabilidade:",["Não","Sim"])
In12 = st.sidebar.selectbox("Demora de cura:",["Não","Sim"])
In13 = st.sidebar.selectbox("Paresia parcial:",["Não","Sim"])
In14 = st.sidebar.selectbox("Rigidez muscular:",["Não","Sim"])
In15 = st.sidebar.selectbox("Alopecia:",["Não","Sim"])
In16 = st.sidebar.selectbox("Obesidade:",["Não","Sim"])

# Tamanho da base de teste
test_size = st.sidebar.slider  (label = 'Tamanho da base de teste (%):', 
                            min_value=0, 
                            max_value=100, 
                            value=20, 
                            step=1)

# salvando o resultado do treinamento no dataframe
results, corr = train_model()

# inserindo um botão na tela
btn_predict = st.sidebar.button("REALIZAR PREDIÇÃO")

st.sidebar.write('') 
st.sidebar.write('**Daniel Gleison M. Lira**')
st.sidebar.write('**Mestrado em Ciências da Computação**')
st.sidebar.write('**Universidade Estadual do Ceará**')
st.sidebar.write('mailto:daniel.gleison@aluno.uece.br')
st.sidebar.markdown('https://github.com/danielgleison')

# título
#image = Image.open('Logo.png')
#st.image(image, use_column_width=True, use_column_height=True)
st.title("Sistema de Classificação Preditiva de Diabetes")

# subtítulo
st.write ('Aplicação acadêmica para classificação preditiva de diabetes ' +
        'utilizando técnicas de Machine Learning (Aprendizado de Máquina). ' +
        'Considerando a relevância dos falsos negativos em aplicações de predição de patologias. ' +
        'utilizaremos a métrica estatística Recall (Sensibilidade) para avaliação do melhor modelo. '
        'A Inteligência Artificial na área de Saúde tem por objetivo prover ' +
        'análises preditivas e auxiliar a tomada de decisão, não devendo ser utilizada ' +
        'em substituição ao diagnóstico de profissional qualificado. ' +
        'Para cada predição, será realizado novos treinamentos e avaliação dos modelos. '
        'Preencha o perfil de análise na barra lateral e clique no botão Realizar Predição para a visualização dos resultados.')
st.markdown("Dataset: https://www.kaggle.com/ishandutta/early-stage-diabetes-risk-prediction-dataset")

st.subheader("Resultados")
# verifica se o botão foi acionado
if btn_predict:

    values = [In1,In2,In3,In4,In5,In6,In7,In8,In9,In10,In11,In12,In13,In14,In15,In16]
    column_names = ["Idade","Genero","Poliuria","Polidipsia","Perda_Peso","Fraqueza","Polifagia","Tordo_genital",\
                    "Embacamento_visual","Coceira","Irritabilidade",\
                    "Demora_cura","Paresia_parcial","Rigidez_muscular","Alopecia","Obesidade"]
    df = pd.DataFrame(values, column_names)

    if  df[0][1] == 'Masculino': df[0][1] = 1 
    elif df[0][1]  == 'Femenino': df[0][1] = 0
            
    for x in range(2,16):
        if   df[0][x] == 'Sim': df[0][x] = 1 
        elif df[0][x]  == 'Não':df[0][x] = 0


    # padronização do input Idade
    df[0][0] = (df[0][0] - 16) / 74
        
    # resultado da predição
        
    pred = [list(df[0])]

    classifier_best = results['Classificador'][results['Recall'] == results['Recall'].max()].values
    classifier = classifier_best[0]

    model_best = results['Modelo'][results['Recall'] == results['Recall'].max()].values
    model = model_best[0]

    result = classifier.predict(pred)
    #prob =  classifier.predict_proba(pred)
    result = result[0]
    #prob = prob[0].max()

    if result == 0: st.write("Predição de Diagnóstico: **NEGATIVO**")
    if result == 1: st.write("Predição de Diagnóstico: **POSITIVO**")
    st.write("Modelo: ", model)
    st.write("Divisão do Dataset: Treino - ", 100 - test_size,'% / ''Teste -',test_size,'%')

    st.subheader("Métricas de Avaliação (%)")
    st.table(results[["Modelo","Recall","Acuracia","Precisao","F1"]].sort_values(by="Recall", ascending=False))
    
    st.subheader("Quantidade de Acertos e Erros")
    st.table(results[["Modelo","Total_Positivos","Total_Negativos", "Falsos_Positivos", "Falsos_Negativos"]].sort_values(by="Falsos_Negativos", ascending=True))
    
    st.subheader("Tempos de Treinamento e Teste (s)")
    st.table(results[["Modelo","Tempo_Treino","Tempo_Teste"]].sort_values(by="Tempo_Treino", ascending=True))

    
    
    #st.table(corr)

    st.subheader("Matriz de Correlação do Dataset")
    
    fig, ax = plt.subplots()
    ax = corr.plot.bar  (figsize = (20,10), 
                        fontsize = 15, 
                        rot = 90, 
                        grid = True)
    st.pyplot(fig)


      
    st.subheader("Distribuição das Classes")
    freq = data['class'].value_counts()
    fig, ax = plt.subplots()
    ax = freq.plot  (kind='bar',
                    figsize = (10,5),
                    rot = 0, 
                    grid = False)
    st.pyplot(fig)
