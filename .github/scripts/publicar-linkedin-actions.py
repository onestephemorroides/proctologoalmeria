#!/usr/bin/env python3
"""
Script para GitHub Actions: lee el último artículo añadido,
genera un post con Claude y lo publica en LinkedIn.
"""

import requests
import os
import sys
import json
from bs4 import BeautifulSoup

LINKEDIN_TOKEN     = os.environ["LINKEDIN_TOKEN"]
LINKEDIN_MEMBER_ID = "1562040614"
ANTHROPIC_API_KEY  = os.environ["ANTHROPIC_API_KEY"]

def extraer_contenido_articulo(url):
    print(f"📖 Leyendo artículo: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    titulo = soup.find("h1")
    titulo = titulo.get_text(strip=True) if titulo else "Artículo del blog"
    parrafos = soup.find_all("p")
    texto = " ".join(p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 60)[:3000]
    print(f"✅ Artículo leído: {titulo}")
    return titulo, texto

def generar_post_linkedin(titulo, texto, url):
    print("🤖 Generando post con Claude...")
    prompt = f"""Eres el Dr. Jaime Jorge Cerrudo, proctólogo y cirujano colorrectal en Almería con más de 13 años de experiencia. Tu clínica ONEstep® permite diagnóstico y tratamiento en una sola visita, sin anestesia general ni hospitalización.

Escribe un post para LinkedIn basado en este artículo de tu blog. El post debe:
- Tener entre 150-250 palabras
- Empezar con una frase que enganche (pregunta, dato sorprendente o afirmación directa)
- Transmitir autoridad médica pero con lenguaje accesible
- Mencionar ONEstep® de forma natural, no forzada
- Terminar con una llamada a la acción sutil indicando el enlace al artículo
- Incluir 3-5 hashtags relevantes al final
- NO usar asteriscos ni markdown, solo texto plano con saltos de línea

Título del artículo: {titulo}
Contenido del artículo: {texto[:2000]}
URL del artículo: {url}

Escribe solo el post, sin explicaciones ni comentarios adicionales."""

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
    print("✅ Post generado")
    return post

def publicar_en_linkedin(post_texto):
    print("📤 Publicando en LinkedIn...")
    payload = {
        "author": f"urn:li:person:{LINKEDIN_MEMBER_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_texto},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    r = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        json=payload,
        timeout=15
    )
    if r.status_code == 201:
        print("✅ ¡Post publicado en LinkedIn con éxito!")
    else:
        print(f"❌ Error al publicar: {r.status_code} - {r.text}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("❌ Falta la URL del artículo")
        print("Uso: python3 publicar-linkedin-actions.py https://www.proctologoalmeria.com/articulo.html")
        sys.exit(1)

    url = sys.argv[1]
    titulo, texto = extraer_contenido_articulo(url)
    post = generar_post_linkedin(titulo, texto, url)

    print("\n--- POST QUE SE PUBLICARÁ ---")
    print(post)
    print("----------------------------\n")

    publicar_en_linkedin(post)

if __name__ == "__main__":
    main()
