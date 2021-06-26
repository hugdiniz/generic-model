
import pandas as pd
pd.options.display.max_columns = None
import numpy as np
from dateutil.parser import parse
import datetime
import json

from mongoengine import *

# ## Carregando os dados da tabela

# In[2]:


dados = pd.read_csv("data/OpenBar - 2021 - BD.csv")


# ### Exemplificação dos dados

# ## Iniciando o Acesso ao MongoDB

# In[3]:


credentials = json.load(open("data/keys/mongo.json",))


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

