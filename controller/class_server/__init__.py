from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask_restplus import Api
from mongoengine import *
import json
import sys
import os

from flask_restplus import Api, Resource, fields,reqparse
from model.time import *

def load_config_variables():

    ################################
    ####### DB - Variables #########
    ################################

    variables = {}
    if "LOCAL" in sys.argv:	
        mongo_credentials = json.load(open("data/keys/mongo.json",))
        variables["mongo_user"] = mongo_credentials["user"]
        variables["mongo_pwd"] = mongo_credentials["pwd"]
    else:
        variables["mongo_user"] = os.environ['mongo_user']
        variables["mongo_pwd"] = os.environ['mongo_pwd']

    #################################
    #### Configuration Variables ####
    #################################

    variables.update(json.load(open("data/config.json",'r')))
    
    return variables

class APIError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def class_to_view(obj):
    return jsonify(mongo_to_dict(obj))

def mongo_to_dict(obj,field_to_remove=["id"]):
    return_data = []
    
    if isinstance(obj, QuerySet):
        return listField_to_dict(obj)

    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in field_to_remove:
            continue

        if isinstance(obj._fields[field_name], EmbeddedDocumentField):
            data = obj._data[field_name]
            return_data.append((field_name, mongo_to_dict(data)))

        data = getattr(obj, field_name)

        if data != None:
            if isinstance(obj._fields[field_name], DateTimeField):
                return_data.append((field_name, str(data.isoformat())))
            elif isinstance(obj._fields[field_name], StringField):
                return_data.append((field_name, str(data)))
            elif isinstance(obj._fields[field_name], FloatField):
                return_data.append((field_name, float(data)))
            elif isinstance(obj._fields[field_name], IntField):
                return_data.append((field_name, int(data)))
            elif isinstance(obj._fields[field_name], ListField):
                return_data.append((field_name, listField_to_dict(data))) 
            else:
                return_data.append((field_name, data))
        else:
            return_data.append((field_name, None))
    
    return dict(return_data)
            



def mongo_to_dict_old(obj):
    return_data = []
    
    if isinstance(obj, QuerySet):
        return listField_to_dict(obj)

    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], DateTimeField):
            return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, listField_to_dict(data)))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))
        elif isinstance(obj._fields[field_name], DBRef):            
            return_data.append((field_name, mongo_to_dict(getattr(obj, field_name))))
        else:
            return_data.append((field_name, data))

    return dict(return_data)

def listField_to_dict(listdata):
    return_data = []
    for data in listdata:
        if isinstance(data, ListField):
            return_data.append(listField_to_dict(data))
        elif isinstance(data, EmbeddedDocument):           
            return_data.append(mongo_to_dict(data))
        elif isinstance(data, Document):           
            return_data.append(mongo_to_dict(data))
        else:            
            return_data.append(data)
            
    return return_data


######################
######## VARS ########
######################

app = Flask(__name__)
api = Api(app)

descricao = "Cartola - Times"
namespace_cartola = api.namespace('api/cartola/', description=descricao)

#app = Flask(__name__,static_folder="static")
cors = CORS(app)

config_vars = load_config_variables()
connect(    
    host='mongodb+srv://'+config_vars["mongo_user"]+':'+config_vars["mongo_pwd"]+'@cartola-data.6zndg.gcp.mongodb.net/?retryWrites=true&w=majority'
)



