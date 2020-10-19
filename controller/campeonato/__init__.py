from flask import request

from controller.class_server import *
from model.liga import *
from model.rodada import *

@app.route("/api/cartola/campeonatos", methods = ["GET"])
def campeonatos():
    try:
        campeonatos = Campeonato.objects()

    except Exception as e:
        print(e)
        return app.response_class(
            response="id_cartola not found in database",
            status=400,
            mimetype='application/json'
    	)
    
    saida = {
        "campeonatos": [ campeonato.to_dict() for campeonato in campeonatos]
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
