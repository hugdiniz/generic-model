from flask import request
from flask_restplus import Api, Resource, fields,reqparse
from controller.class_server import *
from model.liga import *
from model.rodada import *
import jsonpickle
import traceback

@namespace_cartola.route('/ultima_rodada')
class UltimaRodadaController(Resource):    
    def get(self):
        try:
            rodada = Rodada.objects.order_by('-numero').first()
            rodada_map = {
                "nome": "Rodada Atual",
                "rodada_inicial": rodada.numero,
                "rodada_final": rodada.numero,
                "tipo": TipoCampeonato.RODADA.value
            }
            campeonato_ultima_rodada = Campeonato(**rodada_map)

        except Exception as e:
            print(e)    
            traceback.print_exc()
            return app.response_class(
                response="error creating copa",
                status=500,
                mimetype='application/json'
            )
        
        
        return {
            "ultima_rodada": campeonato_ultima_rodada.to_dict()
        }
