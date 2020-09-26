from flask import request

from controller.class_server import *
from model.time import *


@app.route("/api/cartola/time", methods = ["GET"])
def time():
    try:
        if("id_cartola" in request.args):
            id_cartola = int(request.args["id_cartola"])
        else:
            return app.response_class(
            response="id_cartola is missing",
            status=400,
            mimetype='application/json'
    	)

    except:
        return app.response_class(
            response="query or k wrong formatted",
            status=400,
            mimetype='application/json'
    	)
    try:
        time = Time.objects(id_cartola=id_cartola)[0]

    except:
        return app.response_class(
            response="id_cartola not found in database",
            status=400,
            mimetype='application/json'
    	)
    
    
    return mongo_to_dict(time)