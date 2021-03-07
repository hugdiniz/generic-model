from mongoengine import *
from model.rodada import *
import numpy as np
import pandas as pd
from flask import jsonify
from enum import Enum

class Liga():
    nome = StringField()
    rodada_inicial = IntField()

    def get_resultados(self):        
        return pd.DataFrame()

    def __resultado_to_dict__(self,resultado):
        return {
            "Time": resultado["Time"],
            "Pontos": resultado["Pontos"],
            "PontosCapitao": resultado["PontosCapitao"],
            "Patriomonio": resultado["Patriomonio"],
            "Gols": resultado["Gols"],
            "AtletasGol": resultado["AtletasGol"],
            "Cartaos": resultado["Cartaos"],
            "Colocacao": resultado["Colocacao"]
        }


class TipoCampeonato(Enum):
    MENSAL = "mensal"
    RODADA = "rodada"
    GERAL  = "geral"
            
        
class Campeonato(Liga,Document):
    rodada_final = IntField()   
    tipo = StringField()

    def to_dict(self):
        resultados = self.get_resultados()
        resultados["Colocacao"] = list(range(1,resultados.shape[0]+1))
        return {
            "resultados" : resultados.apply(lambda x: self.__resultado_to_dict__(x),axis=1).values.tolist(),
            "nome": self.nome,
            "rodadaInicial": self.rodada_inicial,
            "rodadaFinal": self.rodada_final,
            "tipo": self.tipo,
        } 
    
    def __init__(self, *args, **kwargs):    
        Document.__init__(self, *args, **kwargs)
        self.rodadas = Rodada.objects.filter(numero__gte=self.rodada_inicial).filter(numero__lte=self.rodada_final)    
    
    def get_resultados(self):
        resultado_time = []
        resultado_pontos = []
        resultado_pontos_capitao = []
        resultado_patrimonio = []
        resultado_gols = []
        resultado_atletas_gol = []
        resultado_cartaos = []
        for rodada in self.rodadas:            
            for resultado in rodada.resultados:
                if resultado.id_cartola not in resultado_time:
                    resultado_time = np.append(resultado_time,resultado.id_cartola)
                    resultado_pontos.append(0)
                    resultado_pontos_capitao.append(0)
                    resultado_patrimonio.append(0)
                    resultado_gols.append(0)
                    resultado_atletas_gol.append(0)
                    resultado_cartaos.append(0)

                pos = np.where(resultado_time == resultado.id_cartola)[0][0]

                resultado_pontos[pos]         = resultado_pontos[pos] + resultado.pontos
                resultado_pontos_capitao[pos] = resultado_pontos_capitao[pos] + resultado.pontos_capitao
                resultado_patrimonio[pos]     = resultado_patrimonio[pos] + resultado.patrimonio
                resultado_gols[pos]           = resultado_gols[pos] + resultado.gols
                resultado_atletas_gol[pos]    = resultado_atletas_gol[pos] + resultado.atletas_gol
                resultado_cartaos[pos]        = resultado_cartaos[pos] + resultado.cartaos


        saida = pd.DataFrame({
            "Time": resultado_time,
            "Pontos": resultado_pontos,
            "PontosCapitao": resultado_pontos_capitao,
            "Patriomonio": resultado_patrimonio,
            "Gols": resultado_gols,
            "AtletasGol": resultado_atletas_gol,
            "Cartaos": resultado_cartaos,       
        }).sort_values(by=["Cartaos"])

        saida.sort_values(by=["Pontos","PontosCapitao","Gols","Patriomonio"],inplace=True,ascending=False)

        return saida

def sort_resultado(resultado):
    return resultado.colocacao 
def sort_resultado_id(resultado):
    return resultado.id_cartola 

__numero_copa__ = 0
def gerarNomeCopa():
    global __numero_copa__
    __numero_copa__ = __numero_copa__ + 1
    return "Copa " + str(__numero_copa__)


class Copa():
    def __init__(self,rodada_seletiva,numero_ultima_rodada,rodadas, config_vars):
        total_times = pow(2,config_vars["copa_total_chaves"])
        resultados = rodada_seletiva.resultados
        resultados.sort(key=sort_resultado)
        
        classificados =  [resultado for resultado in resultados[:total_times]]

        self.nome = gerarNomeCopa()
        self.descricao = None
        self.rodada_final = numero_ultima_rodada
        self.rodada_seletiva = rodada_seletiva.numero  
        
        resultados.sort(key=sort_resultado_id)       
        self.chaves = {}
        self.chaves[0] = [None for pos in range(pow(2, config_vars["copa_total_chaves"] - 1 ))] 
        for posicao_chave,i in zip(config_vars["copa_posicao_chaves"],range(pow(2, config_vars["copa_total_chaves"] - 1 ))):
            id_time1 = classificados[i].id_cartola
            id_time2 = classificados[total_times - i - 1].id_cartola
            index_time1 = None
            index_time2 = None
            
            for j,time in zip(range(resultados.__len__()),resultados):
                if(time.id_cartola == id_time1):
                    index_time1 = j
                if(time.id_cartola == id_time2):
                    index_time2 = j
                if( index_time1 != None and index_time2 != None):
                    break
                    
            self.chaves[0][posicao_chave] = Chave(id_time1,id_time2,index_time1,index_time2)
            
        self.campeao = None
        
        ########################
        ### Execucao Rodadas ###
        ########################
        
        i = 1
        for rodada in rodadas:
            self.chaves[i] = []

            resultados = rodada.resultados
            resultados.sort(key=sort_resultado_id)

            if (self.chaves[i-1].__len__() == 1):                
                self.campeao = self.chaves[i-1][0].vencedor(resultados)[0]

            elif (self.chaves[i-1].__len__() >  1):
                for j in range(int(self.chaves[i-1].__len__() / 2)):                    
                    id_time1,index_time1 = self.chaves[i-1][2*j].vencedor(resultados)
                    id_time2,index_time2 = self.chaves[i-1][2*j + 1].vencedor(resultados) 
                    chave = Chave(id_time1,id_time2,index_time1,index_time2)
                    self.chaves[i].append(chave)        
            i = i + 1

    def to_dict(self):
        return jsonify(self)
        


            
class Chave():
    def __init__(self,id_time1,id_time2,index_time1,index_time2):
        self.id_time1 = id_time1
        self.id_time2 = id_time2
        self.index_time1 = index_time1
        self.index_time2 = index_time2

    
    def vencedor(self,resultados):
        self.pontos_time1 = resultados[self.index_time1].pontos
        self.pontos_time2 = resultados[self.index_time2].pontos

        if(resultados[self.index_time1].colocacao < resultados[self.index_time2].colocacao):            
            return self.id_time1,self.index_time1
        else:
            return self.id_time2,self.index_time2

    def to_dict(self):
        return jsonify(self)

    
        