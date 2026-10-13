#!/usr/bin/env python3
"""Check locale completeness, generated HTML, routes, fragments and demo assets."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlparse
import build

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.nodes=[]
        self.ids=[]
        self.h1=0
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        self.nodes.append((tag,attrs))
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='h1':self.h1+=1


def check():
    subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--check'],check=True)
    build.load_content()
    pages={build.route(lc['code'],kind):Page((ROOT/build.route(lc['code'],kind)).read_text()) for lc in build.LOCALES for kind in build.PAGES}
    for code in ('es','en'):
        for kind in ('privacy','support'):
            name=build.android_route(code,kind)
            pages[name]=Page((ROOT/name).read_text())
    references=0
    for locale in build.LOCALES:
        for kind in build.PAGES:
            name=build.route(locale['code'],kind)
            p=pages[name]
            assert p.h1==1,(name,'h1')
            assert len(p.ids)==len(set(p.ids)),(name,'duplicate IDs')
            html=next(attrs for tag,attrs in p.nodes if tag=='html')
            assert html['lang']==locale['code'] and html['dir']==locale.get('dir','ltr'),(name,'language/direction')
            canonical=[attrs['href'] for tag,attrs in p.nodes if tag=='link' and attrs.get('rel')=='canonical']
            assert canonical==[build.public_url(locale['code'],kind)],(name,'canonical')
            alternates={attrs['hreflang']:attrs['href'] for tag,attrs in p.nodes if tag=='link' and attrs.get('rel')=='alternate'}
            assert alternates=={**{lc['code']:build.public_url(lc['code'],kind) for lc in build.LOCALES},'x-default':build.public_url('es',kind)},(name,'hreflang')
            languages={attrs['hreflang']:attrs['href'] for tag,attrs in p.nodes if tag=='a' and 'hreflang' in attrs}
            assert languages=={lc['code']:build.relative(locale['code'],kind,lc['code'],kind) for lc in build.LOCALES},(name,'language menu loses page')
            for tag,attrs in p.nodes:
                assert tag not in ('script','iframe','form'),(name,'unexpected remote behavior')
                if tag=='img':assert 'alt' in attrs and 'width' in attrs and 'height' in attrs,(name,'image accessibility or layout shift')
                for key in ('href','src','srcset'):
                    if key not in attrs:continue
                    url=urlparse(attrs[key]);references+=1
                    if url.scheme or url.netloc:continue
                    target=(ROOT/name).parent / unquote(url.path) if url.path else ROOT/name
                    target=target.resolve()
                    assert target.is_relative_to(ROOT),(name,'path outside site',attrs[key])
                    if target.is_dir():target=target/'index.html'
                    assert target.exists(),(name,'missing route/asset',attrs[key])
                    if url.fragment:
                        target_name=str(target.relative_to(ROOT))
                        target_page=pages.get(target_name)
                        assert target_page and url.fragment in target_page.ids,(name,'missing anchor',attrs[key])
    for code in ('es', 'en'):
        for kind in ('privacy', 'support'):
            name=build.android_route(code,kind)
            page=pages[name]
            assert page.h1 == 1 and len(page.ids) == len(set(page.ids)),name
            canonical=[attrs['href'] for tag,attrs in page.nodes if tag=='link' and attrs.get('rel')=='canonical']
            assert canonical == [build.CONFIG['base_url']+name],name
            languages={attrs['hreflang']:attrs['href'] for tag,attrs in page.nodes if tag=='a' and 'hreflang' in attrs}
            assert languages == {other:build.android_route(other,kind) for other in ('es','en')},name
            for tag,attrs in page.nodes:
                assert tag not in ('script','iframe','form'),name
                for key in ('href','src'):
                    if key not in attrs: continue
                    url=urlparse(attrs[key]);references+=1
                    if url.scheme or url.netloc: continue
                    target=(ROOT/unquote(url.path)) if url.path else ROOT/name
                    if target.is_dir():target=target/'index.html'
                    assert target.exists(),(name,attrs[key])
                    if url.fragment:
                        assert url.fragment in pages[str(target.relative_to(ROOT))].ids,(name,attrs[key])
    manifest=json.loads((ROOT/'assets/screens/manifest.json').read_text())
    assert len(manifest['assets'])==36
    for asset in manifest['assets']:
        raw=(ROOT/asset['output']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==asset['output_sha256'],asset['output']
        assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP',asset['output']
    assert len(manifest['social_assets'])==12
    for asset in manifest['social_assets']:
        raw=(ROOT/asset['output']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==asset['output_sha256'],asset['output']
        assert raw[:2]==b'\xff\xd8',asset['output']
    print(f'Validated {len(pages)} pages, {references} references, 12 reciprocal language menus, 36 native screenshots and 12 social previews.')

if __name__=='__main__':check()
