from flask import Flask, request, render_template

app = Flask(__name__)

databases = []
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


if __name__ == '__main__':
    app.run(debug=True)