#!/usr/bin/env python3
"""Render the localized Apple pages and Android support/privacy pages. Python standard library; no visitor-side code."""
import argparse
import html
import hashlib
import json
import posixpath
from pathlib import Path
from string import Template
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'content/config.json').read_text())
LOCALES = CONFIG['locales']
STRUCTURE = json.loads((ROOT / 'content/structure.json').read_text())
TEMPLATE = Template((ROOT / 'templates/base.html').read_text())
PAGES = ('home', 'guide', 'support', 'privacy')


def esc(text):
    return html.escape(text, quote=True)


def route(code, page):
    stem = {'home': 'index', 'guide': 'start', 'support': 'support', 'privacy': 'privacy'}[page]
    if code == 'es':
        return f'{stem}.html'
    if code == 'en':
        return 'en.html' if page == 'home' else f'{stem}-en.html'
    return f'{code}/{stem}.html'


def public_url(code, page):
    path = route(code, page)
    if path.endswith('index.html'):
        path = path[:-10]
    return CONFIG['base_url'] + path


def relative(code, page, target_code, target_page):
    path = posixpath.relpath(route(target_code, target_page), posixpath.dirname(route(code, page)) or '.')
    return './' if path == 'index.html' else path


def icon(name, size=24):
    paths = {
        'lock': '<rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
        'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18M12 3c-5 5-5 13 0 18"/>',
        'list': '<rect x="3" y="6" width="18" height="15" rx="3"/><path d="M6 3h12M7 11h10M7 16h6"/>',
        'live': '<circle cx="12" cy="12" r="2"/><path d="M7 7a7 7 0 0 0 0 10M17 7a7 7 0 0 1 0 10M4 4a11 11 0 0 0 0 16M20 4a11 11 0 0 1 0 16"/>',
        'play': '<path d="m9 6 9 6-9 6z"/><circle cx="12" cy="12" r="10"/>',
        'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def brand(prefix, home_url):
    return f'''<a class="brand" href="{home_url}" aria-label="Astra IPTV">
        <img src="{prefix}assets/astra-mark.png" width="42" height="42" alt="">
        <span class="wordmark" dir="ltr">astra<span class="brand-suffix">IPTV</span></span>
      </a>'''


def load_content():
    content = {}
    keys = None
    for locale in LOCALES:
        code = locale['code']
        data = json.loads((ROOT / f'content/locales/{code}.json').read_text())
        if keys is None:
            keys = set(data)
        if set(data) != keys or any(not isinstance(value, str) or not value.strip() for value in data.values()):
            raise ValueError(f'{code}: incomplete localization')
        content[code] = data
    return content


def home(data, prefix, urls, code):
    t = lambda key: esc(data[key])
    app_store_url = esc(CONFIG['app_store_url'])
    source = f'{prefix}assets/screens/{code}/'
    def screen(device):
        digest = hashlib.sha256((ROOT / f'assets/screens/{code}/{device}.webp').read_bytes()).hexdigest()[:12]
        return f'{source}{device}.webp?v={digest}'
    features = '\n'.join(f'''<article class="feature-card">
          <span class="feature-icon">{icon(symbol, 28)}</span>
          <h3>{t(f'feature_{i}_title')}</h3><p>{t(f'feature_{i}_body')}</p>
        </article>''' for i, symbol in enumerate(('list', 'live', 'play'), 1))
    faq = '\n'.join(f'''<details class="faq-item"><summary>{t(f'faq_{i}_q')}<span class="plus" aria-hidden="true"></span></summary><p>{t(f'faq_{i}_a')}</p></details>''' for i in range(1, 5))
    return f'''  <main id="main">
    <section class="hero wrap" aria-labelledby="hero-title">
      <div class="hero-copy">
        <p class="eyebrow"><span class="spark" aria-hidden="true">✦</span><bdi>iPhone · iPad · Apple TV</bdi></p>
        <h1 id="hero-title">{t('hero_title')} <span>{t('hero_emphasis')}</span></h1>
        <p class="hero-lead">{t('hero_lead')}</p>
        <div class="actions"><a class="button primary" href="{app_store_url}">{t('download')}{icon('arrow', 20)}</a><a class="button secondary" href="{urls['guide']}">{t('prepare')}</a></div>
        <ul class="facts"><li>{t('free')}</li><li>{t('own_content')}</li><li><bdi>iPhone · iPad · Apple TV</bdi></li></ul>
      </div>
    </section>
    <figure class="hero-visual wrap">
      <div class="tv-frame"><img src="{screen('tv')}" width="1600" height="900" alt="{t('tv_alt')}" fetchpriority="high"></div>
      <figcaption><span class="screen-label"><span aria-hidden="true">✦</span> Astra <span aria-hidden="true">/</span> <bdi>Apple TV</bdi></span><span>{t('demo_caption')}</span></figcaption>
    </figure>
    <section class="experience wrap" id="experience">
      <div class="section-heading"><p class="eyebrow">{t('experience')}</p><h2>{t('feature_title')}</h2></div>
      <div class="feature-grid">{features}</div>
    </section>
    <section class="devices wrap" id="devices">
      <div class="section-heading"><p class="eyebrow"><bdi>iPhone · iPad · Apple TV</bdi></p><h2>{t('devices_title')}</h2><p>{t('devices_body')}</p></div>
      <div class="device-grid">
        <figure class="tablet-showcase"><figcaption class="device-caption"><bdi>iPad</bdi><span>{t('tablet_tagline')}</span></figcaption><div class="tablet-frame"><img src="{screen('ipad')}" width="1080" height="1440" alt="{t('tablet_alt')}" loading="lazy"></div></figure>
        <figure class="phone-showcase"><figcaption class="device-caption"><bdi>iPhone</bdi><span>{t('phone_tagline')}</span></figcaption><div class="phone-frame"><img src="{screen('iphone')}" width="864" height="1878" alt="{t('phone_alt')}" loading="lazy"></div></figure>
      </div>
      <p class="device-note">{t('devices_note')}</p>
    </section>
    <section class="privacy-story wrap"><span class="privacy-symbol" aria-hidden="true">{icon('lock',36)}</span><p class="eyebrow">{t('privacy')}</p><h2>{t('privacy_headline')}</h2><p>{t('faq_3_a')}</p><a href="{urls['privacy']}">{t('privacy_title')}{icon('arrow',18)}</a></section>
    <section class="faq wrap" id="faq"><div class="section-heading"><p class="eyebrow">FAQ</p><h2>{t('faq_title')}</h2></div><div>{faq}</div></section>
    <section class="closing wrap"><img src="{prefix}assets/astra-mark.png" width="72" height="72" alt=""><h2>{t('closing_title')}</h2><p>{t('closing_body')}</p><a class="button primary" href="{app_store_url}">{t('download')}{icon('arrow',20)}</a><p class="closing-note">{t('availability')}</p></section>
    <section class="contact wrap"><div><h2>{t('contact_title')}</h2><p>{t('contact_body')}</p></div><a class="button secondary" href="mailto:{CONFIG['email']}">{t('contact_cta')}{icon('arrow',20)}</a></section>
  </main>'''


def document(data, page, urls):
    t = lambda key: esc(data[key])
    parts, toc = [], []
    for i, section in enumerate(STRUCTURE[page]):
        heading = t(section['heading'])
        anchor = f'section-{i + 1}'
        toc.append(f'<li><a href="#{anchor}">{heading}</a></li>')
        steps = '<ol>' + ''.join(f'<li>{t(key)}</li>' for key in section['steps']) + '</ol>' if section['steps'] else ''
        paras = ''.join(f'<p>{t(key)}</p>' for key in section['paragraphs'])
        links = []
        for link in section['links']:
            href, label = link['href'], link['label']
            if href == 'app-store':
                href, label = CONFIG['app_store_url'], data['download']
            elif href == 'privacy-en.html':
                href, label = urls['privacy'], data['privacy']
            elif href == 'start-en.html':
                href, label = urls['guide'], data['guide']
            elif href.startswith('mailto:'):
                label = CONFIG['email']
            else:
                domain = urlparse(href).netloc
                label = {'www.apple.com':'Apple', 'firebase.google.com':'Firebase', 'policies.google.com':'Google', 'docs.github.com':'GitHub', 'github.com':'GitHub', 'www.themoviedb.org':'TMDB', 'mdblist.com':'MDBList', 'unsplash.com':'Unsplash'}.get(domain, label)
            links.append(f'<a href="{esc(href)}"><bdi>{esc(label)}</bdi></a>')
        related = '<div class="document-links">' + ' · '.join(links) + '</div>' if links else ''
        parts.append(f'<section id="{anchor}"><h2>{heading}</h2>{steps}{paras}{related}</section>')
    return f'''  <main id="main" class="document wrap">
    <div class="document-header"><a class="back-link" href="{urls['home']}">{t('back')}</a><h1>{t(f'{page}_title')}</h1><p class="document-lead">{t(f'{page}_lead')}</p><p class="updated">{t('updated')}</p></div>
    <div class="document-layout"><aside class="contents"><nav aria-label="{t(page)}"><ul>{''.join(toc)}</ul></nav></aside><article class="document-body">{''.join(parts)}</article></div>
    <div class="document-end"><a class="button primary" href="{urls['home']}">{t('back')}{icon('arrow',20)}</a></div>
  </main>'''


def android_route(code, page):
    return f'{page}-android' + ('-en' if code == 'en' else '') + '.html'


def android_documents(content):
    """Android disclosures are separate from Apple CloudKit behavior."""
    android = json.loads((ROOT / 'content/android.json').read_text())
    assert set(android) == {'es', 'en'}
    outputs = {}
    names = {'es': 'Español', 'en': 'English'}
    policies = [('Firebase', 'https://firebase.google.com/support/privacy'),
                ('Google', 'https://policies.google.com/privacy'),
                ('TMDB', 'https://www.themoviedb.org/privacy-policy'),
                ('MDBList', 'https://mdblist.com/privacy/'),
                ('GitHub', 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement')]
    for code, documents in android.items():
        assert set(documents) == {'privacy', 'support'}
        data = content[code]
        for page, doc in documents.items():
            toc, sections = [], []
            for index, (heading, paragraphs) in enumerate(doc['sections'], 1):
                anchor = f'section-{index}'
                toc.append(f'<li><a href="#{anchor}">{esc(heading)}</a></li>')
                text = ''.join(f'<p>{esc(value)}</p>' for value in paragraphs)
                sections.append(f'<section id="{anchor}"><h2>{esc(heading)}</h2>{text}</section>')
            links = ' · '.join(f'<a href="{href}">{label}</a>' for label, href in policies)
            if page == 'privacy':
                sections.append(f'<div class="document-links">{links}</div>')
            support, privacy = android_route(code, 'support'), android_route(code, 'privacy')
            updated = ('Última actualización: 13 de octubre de 2026.' if code == 'es' else 'Last updated: 13 October 2026.')
            body = f'<main id="main" class="document wrap"><div class="document-header"><h1>{esc(doc["title"])}</h1><p class="document-lead">{esc(doc["lead"])}</p><p class="updated">{updated}</p></div><div class="document-layout"><aside class="contents"><nav aria-label="{esc(data[page])}"><ul>{"".join(toc)}</ul></nav></aside><article class="document-body">{"".join(sections)}</article></div></main>'
            values = {key: esc(value) for key, value in data.items()}
            canonical = CONFIG['base_url'] + android_route(code, page)
            alternates = '\n'.join(f'  <link rel="alternate" hreflang="{other}" href="{CONFIG["base_url"]}{android_route(other, page)}">' for other in names)
            alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{CONFIG["base_url"]}{android_route("es", page)}">'
            language_links = '\n'.join(f'<a href="{android_route(other, page)}" lang="{other}" hreflang="{other}"'+(' aria-current="true"' if other == code else '')+f'>{name}</a>' for other, name in names.items())
            values.update(lang=code, direction='ltr', title=esc(doc['title']), description=esc(doc['lead']), canonical=canonical,
                alternates=alternates, prefix='', locale_name=names[code], brand=brand('', './' if code == 'es' else 'en.html'), globe=icon('globe',18),
                navigation=f'<a href="{support}">{esc(data["support"])}</a><a href="{privacy}">{esc(data["privacy"])}</a>',
                language_links=language_links, guide_url=support+'#section-2', support_url=support, privacy_url=privacy,
                css_version=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:12],
                og_image=CONFIG['base_url']+'assets/astra-mark.png', tv_alt='Astra IPTV', main=body,
                footer=('Astra no incluye contenido audiovisual.' if code == 'es' else 'Astra does not supply audiovisual content.'))
            outputs[android_route(code, page)] = TEMPLATE.substitute(values)
    return outputs


def render(content):
    outputs = {}
    for locale in LOCALES:
        code, data = locale['code'], content[locale['code']]
        for page in PAGES:
            prefix = '' if code in ('es', 'en') else '../'
            urls = {target: relative(code, page, code, target) for target in PAGES}
            title = 'Astra IPTV — ' + (data['hero_title'] + ' ' + data['hero_emphasis'] if page == 'home' else data[page])
            navigation = ''.join(f'<a href="{urls[target]}"'+(' aria-current="page"' if page == target else '')+f'>{esc(data[target])}</a>' for target in ('guide','support'))
            if page == 'home':
                navigation = f'<a href="#experience">{esc(data["experience"])}</a>' + navigation
            language_links = '\n'.join(f'          <a href="{relative(code, page, other["code"], page)}" lang="{other["code"]}" hreflang="{other["code"]}"'+(' aria-current="true"' if other['code']==code else '')+f'><bdi>{esc(other["name"])}</bdi>'+(' <span aria-hidden="true">✓</span>' if other['code']==code else '')+'</a>' for other in LOCALES)
            alternates = '\n'.join(f'  <link rel="alternate" hreflang="{other["code"]}" href="{public_url(other["code"],page)}">' for other in LOCALES)
            alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{public_url("es",page)}">'
            values = {key:esc(value) for key,value in data.items()}
            values.update(lang=code, direction=locale.get('dir','ltr'), title=esc(title), description=esc(data['hero_lead'] if page=='home' else data[f'{page}_lead']), canonical=public_url(code,page), alternates=alternates, prefix=prefix, locale_name=esc(locale['name']), brand=brand(prefix,urls['home']), globe=icon('globe',18), navigation=navigation, language_links=language_links, guide_url=urls['guide'], support_url=urls['support'], privacy_url=urls['privacy'], css_version=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:12], og_image=CONFIG['base_url']+f'assets/screens/{code}/tv.jpg?v='+hashlib.sha256((ROOT/f'assets/screens/{code}/tv.jpg').read_bytes()).hexdigest()[:12], main=home(data,prefix,urls,code) if page=='home' else document(data,page,urls))
            outputs[route(code,page)] = TEMPLATE.substitute(values)
    outputs.update(android_documents(content))
    namespace='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',namespace)
    sitemap = ET.Element(f'{{{namespace}}}urlset')
    for locale in LOCALES:
        for page in PAGES:
            url = ET.SubElement(sitemap,f'{{{namespace}}}url')
            ET.SubElement(url,f'{{{namespace}}}loc').text=public_url(locale['code'],page)
    for code in ('es', 'en'):
        for page in ('privacy', 'support'):
            url = ET.SubElement(sitemap, f'{{{namespace}}}url')
            ET.SubElement(url, f'{{{namespace}}}loc').text = CONFIG['base_url'] + android_route(code, page)
    ET.indent(sitemap)
    outputs['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(sitemap,encoding='unicode') + '\n'
    outputs['robots.txt'] = 'User-agent: *\nAllow: /\nSitemap: '+CONFIG['base_url']+'sitemap.xml\n'
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated files are stale; do not write.')
    args=parser.parse_args()
    outputs=render(load_content())
    stale=[]
    for name, text in outputs.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=text:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text)
    if stale:
        raise SystemExit('Regenerate with python3 scripts/build.py: '+', '.join(stale))
    print(f'{"Checked" if args.check else "Generated"} {len(LOCALES)} locales × {len(PAGES)} pages plus four Android documents, sitemap and robots.txt.')


if __name__=='__main__':
    main()
