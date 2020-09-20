from flask import request
from flask import jsonify

from controller.class_server import *



@app.route("/api/cartola/copa", methods = ["GET"])
def user():
    return jsonify(
		{
            "partidas":[{
                "clubes": [
                    {
                        "time": "Baia de Guanabara",
                        "usuario": "Hugo Rebelo",
                        "pontuacao": 50
                    },
                    {
                        "time": "Biduzido",
                        "usuario": "Kleyton Cotta",
                        "pontuacao": 49
                    },                   
			    ],
            },
            {
                "clubes": [                    
                    {
                        "time": "Time 3",
                        "usuario": "Usuario 3",
                        "pontuacao": 30
                    },
                    {
                        "time": "Time 4",
                        "usuario": "Usuario 4",
                        "pontuacao": 20
                    }
                ]
            },
            {
                "clubes": [                    
                    {
                        "time": "Time 5",
                        "usuario": "Usuario 5",
                        "pontuacao": 30
                    },
                    {
                        "time": "Time 6",
                        "usuario": "Usuario 6",
                        "pontuacao": 20
                    }
                ]
            },
            {
                "clubes": [                    
                    {
                        "time": "Time 7",
                        "usuario": "Usuario 7",
                        "pontuacao": 30
                    },
                    {
                        "time": "Time 8",
                        "usuario": "Usuario 8",
                        "pontuacao": 20
                    }
                ]
            }
            ],			
			"tipo": "Oitavas"	
		}
	)