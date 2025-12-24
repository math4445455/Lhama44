import requests

HEADERS = {"User-Agent": "Lhama44/1.0 (https://github.com/)"}

def buscar_na_web(pergunta: str) -> str | None:
    termo = (pergunta or "").strip()
    if not termo:
        return None

    # Usa a API de busca da Wikipédia (pt)
    url_busca = "https://pt.wikipedia.org/w/api.php"
    params_busca = {
        "action": "query",
        "list": "search",
        "srsearch": termo,
        "format": "json",
    }

    try:
        r = requests.get(url_busca, params=params_busca, headers=HEADERS, timeout=8)
        r.raise_for_status()
        data = r.json()
        resultados = data.get("query", {}).get("search", [])
        if not resultados:
            return None

        titulo = resultados[0]["title"]

        # Pega o resumo do artigo encontrado
        url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(titulo)}"
        r2 = requests.get(url_resumo, headers=HEADERS, timeout=8)
        r2.raise_for_status()
        data2 = r2.json()

        resumo = data2.get("extract")
        return resumo if resumo else None

    except Exception:
        return None
