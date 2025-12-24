import os
import webbrowser
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from internet import buscar_na_web

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    dados = request.json
    pergunta = dados.get("texto", "").strip().lower()

    if pergunta == "":
        resposta = "Digite uma pergunta."
    elif "hora" in pergunta:
        resposta = f"Agora são {datetime.now().strftime('%H:%M')}."
    else:
        resposta = buscar_na_web(pergunta)
        if not resposta:
            resposta = "Não encontrei uma resposta clara sobre isso."

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)
