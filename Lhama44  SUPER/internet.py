import re
import requests

HEADERS = {"User-Agent": "Lhama44/1.0 (https://github.com/)"}

BAN_WORDS = [
    "álbum", "album", "música", "musica", "single", "ep", "banda sonora",
    "trilha sonora", "canção", "cancao", "disco", "song", "track"
]

GOOD_HINTS = [
    "instrumento", "ferramenta", "dispositivo", "animal", "planta",
    "cidade", "país", "pais", "objeto", "conceito", "ciência", "ciência",
]

def _limpar_pergunta(pergunta: str) -> str:
    p = (pergunta or "").strip().lower()
    # remove frases comuns do tipo "o que é", "oq é", etc.
    p = re.sub(r"^(o que é|oque é|oq é|oqe|que é|quem é|defina|definição de)\s+", "", p)
    # tira pontuação extra
    p = re.sub(r"[?!.]+$", "", p).strip()
    return p

def _pontuar_titulo(titulo: str, pergunta_original: str) -> int:
    t = titulo.lower()
    score = 0

    # penaliza coisas que costumam ser resultado errado
    for w in BAN_WORDS:
        if w in t:
            score -= 8

    # bônus se tiver dicas boas no título
    for w in GOOD_HINTS:
        if w in t:
            score += 4

    # bônus se indicar desambiguação útil
    if "(" in t and ")" in t:
        score += 3

    # bônus se o título bate bem com o termo (sem “o que é”)
    termo = _limpar_pergunta(pergunta_original)
    if termo and termo in t:
        score += 5

    return score

def buscar_na_web(pergunta: str) -> str | None:
    termo = _limpar_pergunta(pergunta)
    if not termo:
        return None

    url_busca = "https://pt.wikipedia.org/w/api.php"
    params_busca = {
        "action": "query",
        "list": "search",
        "srsearch": termo,
        "format": "json",
        "srlimit": 6  # pega vários pra escolher melhor
    }

    try:
        r = requests.get(url_busca, params=params_busca, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        resultados = data.get("query", {}).get("search", [])
        if not resultados:
            return None

        # rankeia por pontuação (em vez de pegar o primeiro)
        candidatos = [x["title"] for x in resultados if "title" in x]
        candidatos.sort(key=lambda t: _pontuar_titulo(t, pergunta), reverse=True)

        # tenta pegar resumo de até 3 candidatos (fallback automático)
        for titulo in candidatos[:3]:
            url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(titulo)}"
            r2 = requests.get(url_resumo, headers=HEADERS, timeout=10)
            if r2.status_code != 200:
                continue

            info = r2.json()
            resumo = info.get("extract")
            if not resumo:
                continue

            # filtro extra: se o resumo começa falando de álbum/música, tenta o próximo
            resumo_l = resumo.lower()
            if any(w in resumo_l for w in BAN_WORDS):
                continue

            return resumo

        # se tudo falhar, devolve o melhor candidato mesmo
        titulo = candidatos[0]
        url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(titulo)}"
        r3 = requests.get(url_resumo, headers=HEADERS, timeout=10)
        if r3.status_code == 200:
            return (r3.json().get("extract") or None)

        return None

    except Exception:
        return None