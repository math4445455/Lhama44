# Lhama44

**Lhama44** é uma IA de texto simples, implementada com FastAPI.

## Funcionalidades

* Recebe um prompt de texto
* Gera continuações usando modelo de linguagem
* Fornece uma API REST para integração com qualquer sistema

---

## Como usar no PC

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/lhama44.git
cd lhama44
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Rode a API

```bash
uvicorn lhama44_api:app --reload
```

### 4. Acesse no navegador

* Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

##  Deploy (Render ou outro)

* Use `uvicorn lhama44_api:app --host 0.0.0.0 --port 8000` como comando de start
* Configure a porta como 8000
* Inclua o `requirements.txt`

---

##  Exemplo de requisição

POST `/gerar/`

```json
{
  "texto": "História da revolução russa",
  "max_tokens": 100
}
```

### Resposta:

```json
{
  "resposta": "A revolução russa ocorreu..."
}
```

---

##  Licença

Este projeto é de uso livre, porém para outros fins além de uso do cotidiano, é necessária a minha aprovação.
