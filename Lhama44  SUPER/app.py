import os
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from internet import buscar_na_web

from openai import OpenAI

app = Flask(__name__, static_folder="static")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Memória simples (por usuário/IP). Em produção, o ideal é banco.
MEM = {}

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

    # Hora local do servidor (Render geralmente UTC)
    if "hora" in pergunta.lower():
        return jsonify({"a": f"Agora são {datetime.now().strftime('%H:%M')}."})

    # Busca na web como contexto (opcional, mas melhora MUITO)
    contexto = buscar_na_web(pergunta)
    if not contexto:
        contexto = ""

    # Memória por IP
    user_id = request.headers.get("X-Forwarded-For", request.remote_addr) or "anon"
    history = MEM.get(user_id, [])

    system_prompt = (
        "Você é a Lhama44, um assistente inteligente em português. "
        "Responda de forma clara, direta e útil. "
        "Se houver 'Contexto da web', use para responder melhor. "
        "Se não souber, explique o que faltou e sugira como obter a info."
    )

    messages = [{"role": "system", "content": system_prompt}]

    # adiciona histórico curto
    messages += history[-6:]

    # adiciona contexto web
    if contexto:
        messages.append({"role": "system", "content": f"Contexto da web (pode estar incompleto):\n{contexto}"})

    messages.append({"role": "user", "content": pergunta})

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6
        )
        resposta = resp.choices[0].message.content.strip()

        # salva na memória
        history.append({"role": "user", "content": pergunta})
        history.append({"role": "assistant", "content": resposta})
        MEM[user_id] = history[-12:]  # limita memória

        return jsonify({"a": resposta})

    except Exception:
        return jsonify({"a": "Deu erro ao falar com o modelo. Verifique a chave da API e os logs."}), 500