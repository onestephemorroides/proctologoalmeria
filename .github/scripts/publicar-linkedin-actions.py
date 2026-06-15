#!/usr/bin/env python3
import requests
import os
import sys
from bs4 import BeautifulSoup

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
MAKE_WEBHOOK_URL  = "https://hook.eu1.make.com/5zum9uznus0g9wmdivcrfrzyd18jggl6"
BASE_URL          = "https://www.proctologoalmeria.com"

def extraer_contenido_articulo(url):
    print(f"Leyendo articulo: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    titulo = soup.find("h1")
    titulo = titulo.get_text(strip=True) if titulo else "Articulo del blog"

    # Buscar imagen principal del articulo
    imagen_url = ""
    # Buscar cualquier img que no sea la foto del doctor
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src or "foto-doctor" in src or "logo" in src.lower():
            continue
        if src.startswith("http"):
            imagen_url = src
        else:
            imagen_url = f"{BASE_URL}/{src.lstrip('/')}"
        break
    print(f"Imagen encontrada: {imagen_url}" if imagen_url else "Sin imagen detectada")

    parrafos = soup.find_all("p")
    texto = " ".join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)[:3000]
    print(f"Articulo leido: {titulo}")
    return titulo, texto, imagen_url

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

def enviar_a_make(post_texto, url_articulo, imagen_url):
    print("Enviando a Make para publicar en LinkedIn...")
    payload = {
        "post": post_texto,
        "url": url_articulo,
        "imagen_url": imagen_url
    }
    r = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=30)
    print(f"Status Make: {r.status_code}")
    if r.status_code == 200:
        print("Enviado correctamente a Make!")
    else:
        print(f"Error Make: {r.text}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Falta la URL del articulo")
        sys.exit(1)

    url = sys.argv[1]
    titulo, texto, imagen_url = extraer_contenido_articulo(url)
    post = generar_post_linkedin(titulo, texto, url)

    print("\n--- POST QUE SE PUBLICARA ---")
    print(post)
    print("-----------------------------\n")

    enviar_a_make(post, url, imagen_url)

if __name__ == "__main__":
    main()
