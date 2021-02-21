from flask import request
from flask_restplus import Api, Resource, fields,reqparse
from controller.class_server import *
from model.liga import *
from model.rodada import *


@namespace_cartola.route('/campeonatos')
class CampeonatosController(Resource):    
    def get(self):
        try:
            campeonatos = Campeonato.objects()
            rodada_atual = campeonatos[0].rodadas.__len__()
        except Exception as e:
            print(e)
            return app.response_class(
                response="campeonatos not found in database",
                status=400,
                mimetype='application/json'
            )
        
        saida = {
            "campeonatos": [ campeonato.to_dict() for campeonato in campeonatos],
            "rodada_atual": rodada_atual
        }
        
        return saida


def campeonato_to_dict(campeonato):
    resultados = campeonato.get_resultados()
    return {
        "Nome": campeonato.nome,
        "Time": resultados["Time"].values.tolist(),
        "Pontos": resultados["Pontos"].values.tolist(),
        "PontosCapitao": resultados["PontosCapitao"].values.tolist(),
        "Patriomonio": resultados["Patriomonio"].values.tolist(),
        "Gols": resultados["Gols"].values.tolist(),
        "AtletasGol": resultados["AtletasGol"].values.tolist(),
        "Cartaos": resultados["Cartaos"].values.tolist(),
    }
