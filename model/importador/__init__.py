
import pandas as pd
pd.options.display.max_columns = None
import numpy as np
from dateutil.parser import parse
import datetime
import json

from mongoengine import *

from model.rodada import *
from model.api_cartola import *
from time import time

tempo_verificacao = 0
___rodada_parcial = None

def get_rodada_parcial():
    return ___rodada_parcial

def verifica_api(tempo_cache_min = 60):
    global tempo_verificacao
    time_atual = time()
    if ((time_atual - tempo_verificacao)/60)  > tempo_cache_min:
        tempo_verificacao = time_atual
        executar_importacao()


def executar_importacao():
    global ___rodada_parcial
    dados,e_parcial = importar_api_cartola()

    rodadas = Rodada.objects()
    rodadas_numero_banco = [rodada.numero for rodada in rodadas]
    dados = dados[dados["Rodada"].map(lambda numero: numero not in rodadas_numero_banco)]
    resultados = dados.apply(apply_resultados,axis=1).values
    df_rodadas = dados.groupby(["Rodada","Mês"]).size().reset_index()

    if e_parcial:    
        saida = df_rodadas.apply(lambda x: criar_rodada_sem_importar(x,dados),axis=1)
        ___rodada_parcial = saida[0]
        print("Parcial importada:")
        print(___rodada_parcial.numero)
    else: 
        ___rodada_parcial = None
        saida = df_rodadas.apply(lambda x: importar_dados(x,dados),axis=1)  
        print("Rodadas importadas:")
        print(dados["Rodada"].unique())


def criar_rodada_sem_importar(line,dados):
    t = Rodada()
    t.numero = line["Rodada"]
    t.mes = line["Mês"]
    t.resultados = recuperar_resultados(dados,t.numero,dados)
    return t


def importar_dados(line,dados):
    t = Rodada()
    t.numero = line["Rodada"]
    t.mes = line["Mês"]
    t.resultados = recuperar_resultados(dados,t.numero,dados)
    t.save()
    return t

def recuperar_resultados(df,numero,dados):
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