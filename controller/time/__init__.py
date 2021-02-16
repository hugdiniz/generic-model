from flask import request
from flask_restplus import Api, Resource, fields,reqparse

from controller.class_server import *
from model.time import *

descricao = "Cartola - Times"
classify_ns = api.namespace('api/cemig/menu_inteligente', description=descricao)

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('id_cartola', type=int, required=True,default=5)

@classify_ns.route('/api/cartola/time')
class Time(Resource):

    @api.expect(pagination_arguments, validate=True)
    def get(self):
        try:
            if("id_cartola" in request.args):
                id_cartola = int(request.args["id_cartola"])
            else:
                print("id_cartola is missing")
                return app.response_class(
                response="id_cartola is missing",
                status=400,
                mimetype='application/json'
            )

        except Exception as e:
            print(e)
            return app.response_class(
                response="id_cartola wrong formatted",
                status=400,
                mimetype='application/json'
            )
        try:
            time = Time.objects(id_cartola=id_cartola)[0]

        except Exception as e:
            print(e)
            return app.response_class(
                response="id_cartola not found in database",
                status=400,
                mimetype='application/json'
            )


        return mongo_to_dict(time)




@classify_ns.route('/api/cartola/times')
class Time(Resource):   
    def get(self):
        times = Time.objects()
        return {"times": mongo_to_dict(times)}