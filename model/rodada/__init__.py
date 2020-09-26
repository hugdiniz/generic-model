from mongoengine import *
    
class Resultado(EmbeddedDocument):
    id_cartola = IntField()
    colocacao = IntField()
    pontos = FloatField() 
    pontos_capitao = FloatField() 
    patrimonio = FloatField() 
    gols = IntField()
    atletas_gol = IntField()
    cartaos = IntField() 
    
class Rodada(Document):
    numero = IntField() 
    mes = StringField()
    resultados = ListField(EmbeddedDocumentField(Resultado))