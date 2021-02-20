from flask import request
from flask_restplus import Api, Resource, fields,reqparse
from controller.class_server import *
from model.liga import *
from model.rodada import *
import jsonpickle
import traceback

@namespace_cartola.route('/copa')
class CopaController(Resource):    
    def get(self):
        try:
            copas = []
            rodadas = Rodada.objects()
            for numero in config_vars["rodadas_seletiva"]:
                if(numero <= rodadas.__len__()):
                    rodada_seletiva = rodadas[numero-1]
                    rodadas_copa = rodadas[rodada_seletiva.numero:rodada_seletiva.numero+4]
                    copa = Copa(rodada_seletiva,rodadas_copa,config_vars)        
                    copas.append(copa)
                else:
                    break
        except Exception as e:
            print(e)    
            traceback.print_exc()
            return app.response_class(
                response="error creating copa",
                status=500,
                mimetype='application/json'
            )
        
        
        return app.response_class(
        response=jsonpickle.dumps(copas,unpicklable=False),
        status=200,
        mimetype='application/json'
    )
