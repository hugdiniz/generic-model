from flask import Flask, request,abort
from flask_cors import CORS
from flask import jsonify
import os

app = Flask(__name__)
#app = Flask(__name__,static_folder="static")
cors = CORS(app)

@app.route("/")
def index():
    return "Hello World"

def login():	
	if(request.args["hash"] =="e4ec1fc3fe931e4d933e6f3492b676d7" or request.form["hash"] =="e4ec1fc3fe931e4d933e6f3492b676d7"):
		return True
	else:
		print(request.form)
		print(request.args)
		abort(401)
		return False

@app.route("/api/cartola/rodada", methods = ["GET"])
def get_model():
	#login()

	### Get Variables
	k = 5

	#try:
	#	if("k" in request.args):
	#		k = int(request.args["k"])
	#	
	#	query = request.args["query"]
	#except:
	#	return app.response_class(
      			#response="query or k wrong formatted",
      			#status=400,
      			#mimetype='application/json'
    		#)

	### Execute any model
	return jsonify(
		{
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
			],	
			"rodada": 1	
		}
	)
	



def controller(app):
	app.static_folder = 'static'
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0',ssl_context='adhoc',port=port)
	
	##init_train_model()
	##print("Training time: "+ str(time() - t0))
	
	

@app.errorhandler(401)
def denied(error):
    return "401 Acess Denied"


@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error"


if __name__ == "__main__":
	controller(app)

