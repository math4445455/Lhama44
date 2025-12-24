import requests

def buscar_na_web(pergunta):
    try:
        # 1. Buscar o título mais provável
        busca_url = "https://pt.wikipedia.org/w/api.php"
        busca_params = {
            "action": "query",
            "list": "search",
            "srsearch": pergunta,
            "format": "json"
        }

        busca = requests.get(busca_url, params=busca_params, timeout=10)
        dados_busca = busca.json()

        resultados = dados_busca.get("query", {}).get("search", [])
        if not resultados:
            return None

        titulo = resultados[0]["title"]

        # 2. Buscar o resumo do título encontrado
        resumo_url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo.replace(' ', '%20')}"
        resumo = requests.get(resumo_url, timeout=10)

        if resumo.status_code != 200:
            return None

        dados_resumo = resumo.json()
        texto = dados_resumo.get("extract")

        if not texto:
            return None

        if len(texto) > 350:
            texto = texto[:350] + "..."

        return texto

    except:
        return None
