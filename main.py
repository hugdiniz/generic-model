from flask import Flask, request,abort
from flask_cors import CORS
from flask import jsonify
import os
from controller.class_server import *
from controller.cup import *
from controller import *

@app.errorhandler(401)
def denied(error):
    return "401 Acess Denied"


@app.errorhandler(500)
def internal_error(error):
    return "500 Internal Server Error"


if __name__ == "__main__":
	controller(app)

