from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd



app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_andre.sqlite3"
db = SQLAlchemy(app)

databases = []


#con = sqlite3.connect("/home/andre/Documents/projetos/app_api_flask/src/app_andre.sqlite3")
con = sqlite3.connect("//home/ubuntu/projects/app_flask/app_api_flask/src/app_andre.sqlite3")

cur = con.cursor()

df = pd.read_sql_query('SELECT * FROM db_bases', con)


class dbBases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    database = db.Column(db.String(50))
    tabela = db.Column(db.String(50))
    audiencia = db.Column(db.String(50))
    midia = db.Column(db.String(50))

    def __init__(self,database,tabela,audiencia,midia):
        self.database = database
        self.tabela = tabela
        self.audiencia = audiencia
        self.midia = midia



def checkapi(Function):
    if Function == 'getdatabases':
        for i in df.iterrows():
            if i == 'null':
                return 301
            else:
                return 200

class GetBases(Resource):
    def get(__self__):

        status_code = checkapi("getdatabases")

        if (status_code != 200):
            retjson={
                'Mensagem': "Sem bases para execução",
                'Status Code': status_code
            }
            return jsonify(retjson)
        
        else:
            #for index, i in df.iterrows():
            all_qurey = [{'Banco de dados': i['database'],
                        'tabela': i['tabela'],
                        'audiencia': i['audiencia'],
                        'midia': i['midia']} for index, i in df.iterrows()]
            return jsonify(all_qurey)

@app.route('/', methods=["GET", "POST"])
def page_home():

    '''
    if request.method == "POST":
        if request.form.get("bd") and request.form.get("tabela") and request.form.get("audiencia") and request.form.get("midia"):
            databases.append({"bd": request.form.get("bd"),\
                              "tabela": request.form.get("tabela"),\
                              "audiencia": request.form.get("audiencia"),\
                              "midia": request.form.get("midia")})
            print(databases)
    '''

    banco =request.form.get("bd")
    tabeladb = request.form.get("tabela")
    audienciadb = request.form.get("audiencia")
    midiadb = request.form.get("midia")

    if request.method == "POST":

        db_base = dbBases(banco, tabeladb, audienciadb, midiadb)
        db.session.add(db_base)
        db.session.commit()

    return render_template('index.html', databases=databases)


api.add_resource(GetBases, "/getdatabases")

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)