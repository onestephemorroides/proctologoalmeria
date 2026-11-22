#!/usr/bin/env python3
"""Actualiza <lastmod> de sitemap.xml con la fecha del último cambio real de cada página
(último commit que tocó el archivo, ignorando commits de solo metadatos/limpieza).
Uso: python3 .herramientas/actualizar-lastmod.py   (desde la raíz del repo)"""
import re, subprocess, os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BASE = 'https://www.proctologoalmeria.com/'
# Commits que no cuentan como cambio de contenido (mensaje que contiene alguna de estas cadenas)
IGNORAR = ['recortar meta descriptions', 'Medir clics', 'Perf:', 'lastmod', 'limpieza preview', 'temporal para publicar']

def fecha(path):
    out = subprocess.run(['git', 'log', '--format=%cs%x09%s', '--', path],
                         capture_output=True, text=True).stdout.splitlines()
    for line in out:
        d, _, msg = line.partition('\t')
        if not any(k.lower() in msg.lower() for k in IGNORAR):
            return d
    return out[0].split('\t')[0] if out else None

s = open('sitemap.xml', encoding='utf-8').read()
def repl(m):
    block = m.group(0)
    url = re.search(r'<loc>([^<]+)</loc>', block).group(1)
    rel = url[len(BASE):] or 'index.html'
    if rel.endswith('/'): rel += 'index.html'
    if not os.path.exists(rel):
        print('AVISO: no existe', rel, file=sys.stderr); return block
    d = fecha(rel)
    return re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{d}</lastmod>', block) if d else block
s2 = re.sub(r'<url>.*?</url>', repl, s, flags=re.S)
open('sitemap.xml', 'w', encoding='utf-8').write(s2)
for u, d in re.findall(r'<loc>([^<]+)</loc>\s*(?:<[^>]*>\s*)*?<lastmod>([^<]+)</lastmod>', s2):
    print(d, u[len(BASE):] or '/')
