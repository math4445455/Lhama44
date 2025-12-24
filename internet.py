import requests
from bs4 import BeautifulSoup
import urllib.parse

# Use um User-Agent de um navegador real
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def buscar_na_web(pergunta):
    try:
        # 1) Busca no DuckDuckGo (usando a versão lite ou html)
        query = urllib.parse.quote(pergunta)
        busca_url = f"https://html.duckduckgo.com/html/?q={query}"
        
        # É importante manter uma sessão para lidar com cookies básicos se necessário
        session = requests.Session()
        busca = session.get(busca_url, headers=HEADERS, timeout=10)
        
        soup = BeautifulSoup(busca.text, "html.parser")

        # Seleciona o link do resultado
        resultado = soup.find("a", class_="result__a")
        if not resultado:
            return "Nenhum resultado encontrado na busca."

        link = resultado["href"]
        
        # Correção: DuckDuckGo às vezes usa links relativos ou redirecionamentos
        if link.startswith("//"):
            link = "https:" + link
        if "/l/?" in link: # Limpa redirecionamentos internos
            parsed_link = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
            link = parsed_link.get("uddg", [link])[0]

        # 2) Entra na página encontrada
        pagina = session.get(link, headers=HEADERS, timeout=10)
        # Forçar encoding correto para evitar caracteres estranhos
        pagina.encoding = pagina.apparent_encoding 
        
        soup_pagina = BeautifulSoup(pagina.text, "html.parser")

        # 3) Tenta padrão Wikipédia
        conteudo = soup_pagina.find("div", class_="mw-parser-output")
        if conteudo:
            for p in conteudo.find_all("p", recursive=False): # recursive=False evita pegar tabelas internas
                texto = p.get_text().strip()
                if len(texto) > 80:
                    return texto

        # 4) Fallback: busca parágrafos significativos
        todos_p = soup_pagina.find_all("p")
        for p in todos_p:
            texto = p.get_text().strip()
            if len(texto) > 100: # Aumentei um pouco para evitar menus ou avisos de cookies
                return texto

        return "Conteúdo relevante não encontrado na página."

    except Exception as e:
        return f"Erro durante a execução: {e}"

# Teste
print(buscar_na_web("Quem foi Alan Turing?"))