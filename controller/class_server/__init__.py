from flask import Flask
from flask_cors import CORS
from flask import jsonify
from mongoengine import *

app = Flask(__name__)
#app = Flask(__name__,static_folder="static")
cors = CORS(app)




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

def mongo_to_dict(obj):
    return_data = []

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

    return dict(return_data)

def listField_to_dict(listdata):
    return_data = []
    for data in listdata:
        if isinstance(data, ListField):
            return_data.append(listField_to_dict(data))
        elif isinstance(data, EmbeddedDocument):           
            return_data.append(mongo_to_dict(data))
        else:            
            return_data.append(data)
            
        return return_data