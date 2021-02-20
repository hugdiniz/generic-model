from flask import Flask, request,abort
from flask_cors import CORS
from flask import jsonify

from controller.class_server import *
import os
import sys


def controller(app):
	app.static_folder = 'static'  
	port = int(os.environ.get('PORT', 5000))
	#app.run(host='0.0.0.0',ssl_context='adhoc',port=port)
	if "LOCAL" in sys.argv:		
		app.run(host='0.0.0.0',port=port)
	else:
		app.run(host='0.0.0.0',ssl_context='adhoc',port=port)

	##init_train_model()
	##print("Training time: "+ str(time() - t0))
	
	