from mongoengine import *

class Time(Document):
    id_cartola = IntField() 
    nome = StringField()
    url_escudo = StringField()
    nome_usuario = StringField()