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
            
            rodada = Rodada.objects.order_by('-numero').first()
            rodada_map = {
                "nome": "Ultima Rodada",
                "rodada_inicial": rodada.numero,
                "rodada_final": rodada.numero,
                "tipo": TipoCampeonato.RODADA.value
            }
            campeonato_ultima_rodada = Campeonato(**rodada_map)
            rodada_atual = rodada.numero

            parcial_map = {
                "nome": "Ultima Rodada",
                "rodada_inicial": rodada.numero,
                "rodada_final": rodada.numero,
                "tipo": TipoCampeonato.RODADA.value
            }

            parcial = Campeonato(**parcial_map)            
            parcial.nome = "Parcial"
            
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

        saida["campeonatos"].append(campeonato_ultima_rodada.to_dict())
        saida["campeonatos"].append(parcial.to_dict())

        rodadas = Rodada.objects()
        for rodada in rodadas:
            print("Rodada " + str(rodada.numero) + " Mês: "+ rodada.mes)           
            rodada_map = {
                "nome": "Rodada " + str(rodada.numero) ,
                "rodada_inicial": rodada.numero,
                "rodada_final": rodada.numero,
                "tipo": TipoCampeonato.RODADA.value
            }
            campeonato_ultima_rodada = Campeonato(**rodada_map)
            saida["campeonatos"].append(campeonato_ultima_rodada.to_dict())
        
        
        
        return saida
