import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from internet import buscar_na_web

app = Flask(__name__, static_folder="static")

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.get("/manifest.webmanifest")
def manifest():
    return send_from_directory("static", "manifest.webmanifest")

@app.get("/sw.js")
def sw():
    return send_from_directory("static", "sw.js")

@app.post("/api/ask")
def ask():
    data = request.get_json(force=True)
    pergunta = (data.get("q") or "").strip()

    if not pergunta:
        return jsonify({"a": "Digite uma pergunta."})

    if "hora" in pergunta.lower():
        return jsonify({"a": f"Agora são {datetime.now().strftime('%H:%M')}."})

    resposta = buscar_na_web(pergunta) or "Ainda não sei responder isso."
    return jsonify({"a": resposta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
