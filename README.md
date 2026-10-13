# Astra IPTV — project website

The public website for Astra IPTV on iPhone, iPad and Apple TV. The public App Store launch is still being prepared. Astra is a free player for the visitor’s own authorized sources; it does not provide streams, channels or subscriptions.

https://juancazalla.github.io/AstraIPTV-Website/

## Design and languages

The site follows the current Apple app: the purple Astra mark, indigo accent (`#8A76FF`), dark neutral surfaces and rounded cards. It always uses the dark theme, regardless of the system’s color scheme, and works without JavaScript, external fonts, analytics, forms or first-party cookies. GitHub Pages hosts the site under its own privacy statement.

Home, connection guide, support and privacy are available in all 12 complete iOS localizations. Arabic uses right-to-left layout. The language menu keeps the current page; every page has reciprocal `hreflang` links and a canonical URL.

| Language | Home | Guide / support / privacy |
| --- | --- | --- |
| Español | `/` | `start.html`, `support.html`, `privacy.html` |
| Español (Latinoamérica) | `es-419/` | `es-419/start.html`, `support.html`, `privacy.html` in that directory |
| English | `en.html` | `start-en.html`, `support-en.html`, `privacy-en.html` |
| Français | `fr/` | `start.html`, `support.html`, `privacy.html` in the locale directory |
| Italiano | `it/` | Same page names in the locale directory |
| Deutsch | `de/` | Same page names in the locale directory |
| Nederlands | `nl/` | Same page names in the locale directory |
| العربية | `ar/` | Same page names in the locale directory |
| Bahasa Indonesia | `id/` | Same page names in the locale directory |
| Türkçe | `tr/` | Same page names in the locale directory |
| Português (Brasil) | `pt-BR/` | Same page names in the locale directory |
| Português (Portugal) | `pt-PT/` | Same page names in the locale directory |

The original Spanish and English URLs remain valid for existing App Store links. Japanese and Korean are not advertised: their three generic catalog entries do not constitute complete app localizations.

## Editing and publishing

Python 3’s standard library renders 48 static HTML pages. The deployed site needs no runtime or translation service.

1. Edit the matching text in `content/locales/*.json`. Keep keys and factual disclosures consistent across languages.
2. Edit shared layout in `templates/base.html` and `scripts/build.py`; edit appearance in `styles.css`.
3. Run `python3 scripts/build.py` to regenerate HTML, `sitemap.xml` and `robots.txt`.
4. Run `python3 scripts/validate.py` to check generated files, translation coverage, page-preserving language links, routes, anchors, image accessibility and screenshot hashes.
5. Preview with `python3 -m http.server 8080` and check desktop, mobile, Arabic and the fixed dark appearance.

Do not hand-edit generated HTML. CSS URLs include a content hash to refresh cached styles. The new mark uses `assets/astra-mark.png` so previous visitors do not reuse the old green icon.

GitHub Pages publishes the root of `main` after each push. This public repository contains website text and selected demo assets. Application source and credentials stay in their separate repositories. Launch-notification links only compose an email; the visitor chooses whether to send it.

## Real app assets

`assets/screens/<locale>/` contains actual localized simulator screenshots of iPhone, iPad and Apple TV. They display fictional demo titles, with no bundled streams. Images are proportionally resized and encoded for the web; the app interface is not reconstructed. WebP is used in the page and JPEG in social preview metadata.

The iPhone/iPad captures are from 2026-10-09, app commit `72bc4e4e0a85c583728657179b9d47a9658a9311`. Apple TV uses the verified native captures in the app release assets. `assets/screens/manifest.json` records original paths, original screenshot hashes and output hashes. The mark is copied from the app’s BrandMark asset. Demo imagery belongs to the app’s release demo assets.

To refresh assets from the local Apple checkout, install `cwebp` and use macOS `sips`, then run:

```sh
python3 scripts/import-assets.py --app-root ../AstraIPTV
python3 scripts/build.py
python3 scripts/validate.py
```

## Apple acquisition channel

The landing pages lead to their localized connection guide and an optional launch notification email. App sharing links carry `utm_source=astra_app&utm_medium=share&utm_campaign=v1_apple`. These labels identify the link; this static website does not count visits or attribute installs.

When the Apple listings are public, replace the launch-notification action with the verified App Store URL. Generate the first campaign link in App Store Connect App Analytics and use its actual `pt` token; ASC provider/team IDs are not campaign tokens. The draft configuration remains in `acquisition/apple-campaigns.json`. Add distinct short campaign names for the new locale routes when configuring Apple campaign links. Read acquisition reports in ASC and compare activation in consented production installations in Firebase separately. Unavailable campaign data is not zero conversions. Paid traffic requires an explicit budget.

## Android review documents

`content/android.json` contains separate Android and Android TV support and privacy disclosures in Spanish and English. `scripts/build.py` generates `privacy-android.html`, `privacy-android-en.html`, `support-android.html` and `support-android-en.html`, retaining the existing Apple disclosures. These pages describe Android Keystore/local storage, source connections and optional Firebase collection, and are included in the sitemap and validation.
