#!/usr/bin/env python3
import requests
import os
import sys
from bs4 import BeautifulSoup

LINKEDIN_TOKEN     = os.environ["LINKEDIN_TOKEN"]
LINKEDIN_MEMBER_ID = "1562040614"
ANTHROPIC_API_KEY  = os.environ["ANTHROPIC_API_KEY"]

def extraer_contenido_articulo(url):
    print(f"Leyendo articulo: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    titulo = soup.find("h1")
    titulo = titulo.get_text(strip=True) if titulo else "Articulo del blog"
    parrafos = soup.find_all("p")
    texto = " ".join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)[:3000]
    print(f"Articulo leido: {titulo}")
    return titulo, texto

def generar_post_linkedin(titulo, texto, url):
    print("Generando post con Claude...")
    prompt = f"""Eres el Dr. Jaime Jorge Cerrudo, proctologo y cirujano colorrectal en Almeria con mas de 13 anos de experiencia. Tu clinica ONEstep permite diagnostico y tratamiento en una sola visita, sin anestesia general ni hospitalizacion.

Escribe un post para LinkedIn basado en este articulo de tu blog. El post debe:
- Tener entre 150-250 palabras
- Empezar con una frase que enganche
- Transmitir autoridad medica pero con lenguaje accesible
- Mencionar ONEstep de forma natural
- Terminar con el enlace al articulo
- Incluir 3-5 hashtags al final
- Solo texto plano con saltos de linea, sin asteriscos ni markdown

Titulo: {titulo}
Contenido: {texto[:2000]}
URL: {url}

Escribe solo el post, sin comentarios adicionales."""

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    r.raise_for_status()
    post = r.json()["content"][0]["text"].strip()
    print("Post generado")
    return post

def publicar_en_linkedin(post_texto):
    print("Publicando en LinkedIn...")

    # Endpoint REST nuevo de LinkedIn (v202401)
    payload = {
        "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
        "commentary": post_texto,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    r = requests.post(
        "https://api.linkedin.com/rest/posts",
        headers={
            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
            "Content-Type": "application/json",
            "LinkedIn-Version": "202501",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        json=payload,
        timeout=15
    )

    print(f"Status: {r.status_code}")
    if r.status_code in [200, 201]:
        print("Post publicado en LinkedIn con exito!")
        return True
    else:
        print(f"Error al publicar: {r.status_code} - {r.text}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Falta la URL del articulo")
        sys.exit(1)

    url = sys.argv[1]
    titulo, texto = extraer_contenido_articulo(url)
    post = generar_post_linkedin(titulo, texto, url)

    print("\n--- POST QUE SE PUBLICARA ---")
    print(post)
    print("-----------------------------\n")

    publicar_en_linkedin(post)

if __name__ == "__main__":
    main()
