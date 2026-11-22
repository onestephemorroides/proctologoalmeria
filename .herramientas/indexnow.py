#!/usr/bin/env python3
"""Avisa a Bing/IndexNow de URLs nuevas o actualizadas de proctologoalmeria.com.
Uso:
  python3 .herramientas/indexnow.py https://www.proctologoalmeria.com/pagina.html [...]
  python3 .herramientas/indexnow.py --todo     (todas las URLs del sitemap.xml)
Ejecutar DESPUÉS de que GitHub Pages haya publicado los cambios (1-2 min tras el push)."""
import sys, re, json, os, urllib.request
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
KEY = '3a2188f55119efac928270e149867d56'
HOST = 'www.proctologoalmeria.com'
urls = sys.argv[1:]
if urls == ['--todo']:
    urls = re.findall(r'<loc>([^<]+)</loc>', open('sitemap.xml', encoding='utf-8').read())
if not urls:
    sys.exit(__doc__)
body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': f'https://{HOST}/{KEY}.txt', 'urlList': urls}).encode()
req = urllib.request.Request('https://api.indexnow.org/indexnow', data=body,
                             headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    r = urllib.request.urlopen(req, timeout=30)
    print('IndexNow', r.status, '-', len(urls), 'URLs enviadas')
except urllib.error.HTTPError as e:
    print('IndexNow ERROR', e.code, e.read().decode()[:300]); sys.exit(1)
