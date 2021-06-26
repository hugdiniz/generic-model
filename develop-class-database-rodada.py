#!/usr/bin/env python
# coding: utf-8

# # Desenvolvendo Classes e recuperando dados das rodadas.
# 
# <h4> Notebook destinado ao desenvolvimento das classes para as rodadas e recuperação dos dados da tabela encontrada no grupo salvando a no banco.</h4>

# ## Import do Python

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

from IPython.display import display, Markdown, Latex,HTML
from urllib.request import urlopen

import sys
sys.path.append("../../../")

import pandas as pd
pd.options.display.max_columns = None
import numpy as np
from dateutil.parser import parse
import datetime
import json

from mongoengine import *

html = open("../custom_files/style.css", "r")
display(HTML("<style>\n" + "".join(html.readlines()) + "</style>"))
display(HTML("<style src='https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'></style>"))
display(HTML("<script src='https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'></script>"))
#display(HTML("<style src='https://cdnjs.cloudflare.com/ajax/libs/open-iconic/1.1.1/font/css/open-iconic-bootstrap.css'></style>"))
display(HTML("<style src='https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'></style>"))


# ## Carregando os dados da tabela

# In[2]:


dados = pd.read_csv("/home/hugdiniz/Work/workspace/generic-model/data/OpenBar - 2021 - BD.csv")


# ### Exemplificação dos dados

# ## Iniciando o Acesso ao MongoDB

# In[3]:


credentials = json.load(open("../../data/keys/mongo.json",))


# In[4]:


connect(    
    host='mongodb+srv://'+credentials["user"]+':'+credentials["pwd"]+'@cartola-data.6zndg.gcp.mongodb.net/?retryWrites=true&w=majority'
)


# # Definindo a Classe

# In[5]:


class Resultado(EmbeddedDocument):
    id_cartola = IntField()
    colocacao = IntField()
    pontos = FloatField() 
    pontos_capitao = FloatField() 
    patrimonio = FloatField() 
    gols = IntField()
    atletas_gol = IntField()
    cartaos = IntField() 
    
class Rodada(Document):
    numero = IntField() 
    mes = StringField()
    resultados = ListField(EmbeddedDocumentField(Resultado))

def importar_dados(line):
    t = Rodada()
    t.numero = line["Rodada"]
    t.mes = line["Mês"]
    t.resultados = recuperar_resultados(dados,t.numero)
    t.save()
    return t

def recuperar_resultados(df,numero):
    resultados_rodada = dados[dados["Rodada"] == numero]
    resultados = [r for r in resultados_rodada.apply(apply_resultados,axis=1).values]
    return resultados

def apply_resultados(line):
    r = Resultado()
    r.id_cartola = line["time_id"]
    r.colocacao = line["Colocação"]
    r.pontos = line["pts_rodada"]
    r.pontos_capitao = line["pts_capitao"]
    r.patrimonio = line["Patrimônio"]
    r.gols = line["qtd_gol"]
    r.atletas_gol = line["qtd_atleta_gol"]
    r.cartaos = line["qtd_cartao"]
    return r


# In[6]:


rodadas = Rodada.objects()


# In[8]:


rodadas_numero_banco = [rodada.numero for rodada in rodadas]


# In[16]:


dados = dados[dados["Rodada"].map(lambda numero: numero not in rodadas_numero_banco)]
resultados = dados.apply(apply_resultados,axis=1).values


# ## Importando os dados no Banco

# In[14]:


df_rodadas = dados.groupby(["Rodada","Mês"]).size().reset_index()
saida = df_rodadas.apply(importar_dados,axis=1)


# In[18]:


print("Rodadas importadas:")
print(dados["Rodada"].unique())


# ## Teste de Sucesso da Importação

# In[11]:


#TODO

