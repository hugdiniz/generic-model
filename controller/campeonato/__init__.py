from flask import request
from flask_restplus import Api, Resource, fields,reqparse
from controller.class_server import *
from model.liga import *
from model.rodada import *
import traceback


@namespace_cartola.route('/campeonatos')
class CampeonatosController(Resource):    
    def get(self):
        try:
            campeonatos = Campeonato.objects()
            rodada_atual = campeonatos[0].rodadas.__len__()
        except Exception as e:
            print(e)
            traceback.print_exc()
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
