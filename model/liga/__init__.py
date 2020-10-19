from mongoengine import *
from model.rodada import *
import numpy as np
import pandas as pd

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

    def to_dict(self):
        resultados = self.get_resultados()
        resultados["Colocacao"] = list(range(1,resultados.shape[0]+1))
        return {
            "resultados" : resultados.apply(lambda x: self.__resultado_to_dict__(x),axis=1).values.tolist(),
            "nome": self.nome
        } 
        
        
class Campeonato(Liga,Document):
    rodada_final = IntField()   
    
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
    