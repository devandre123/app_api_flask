from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

databases = []

def checkapi(Function):
    if Function == 'getdatabases':
        for i in databases:
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

        for i in databases:
            ret={
                'Banco de dados': i['bd'],
                'tabela': i['tabela'],
                'audiencia': i['audiencia'],
                'midia': i['midia']
            }
        return jsonify(ret)

@app.route('/', methods=["GET", "POST"])
def page_home():

    if request.method == "POST":
        if request.form.get("bd") and request.form.get("tabela") and request.form.get("audiencia") and request.form.get("midia"):
            databases.append({"bd": request.form.get("bd"),\
                              "tabela": request.form.get("tabela"),\
                              "audiencia": request.form.get("audiencia"),\
                              "midia": request.form.get("midia")})
            print(databases)
            
    return render_template('index.html', databases=databases)


api.add_resource(GetBases, "/getdatabases")

if __name__ == '__main__':
    app.run(debug=True)