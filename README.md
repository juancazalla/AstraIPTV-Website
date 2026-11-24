# Astra IPTV — project website

The public website for Astra IPTV on iPhone, iPad and Apple TV. The app is available on the App Store for iOS/iPadOS and tvOS. Astra is a free player for the visitor’s own authorized sources; it does not provide streams, channels or subscriptions.

https://juancazalla.github.io/AstraIPTV-Website/

## Design and languages

The site uses Astra’s purple mark, lavender accent (`#A391FF`) and dark neutral surfaces. The home page presents the released 1.1.0 features, including Multiview, per-profile Home customization and the Apple TV redesign. Native iPhone and Apple TV captures appear in the hero, with a two-channel iPad Multiview capture in the device showcase. It always uses the dark theme, regardless of the system’s color scheme, and works without JavaScript, external fonts, analytics, forms or first-party cookies. GitHub Pages hosts the site under its own privacy statement.

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

Python 3’s standard library renders 64 static HTML pages, including twelve Televizo alternative pages and four Android documents. The deployed site needs no runtime or translation service.

1. Edit the matching text in `content/locales/*.json`. Keep keys and factual disclosures consistent across languages.
2. Edit shared layout in `templates/base.html` and `scripts/build.py`; edit appearance in `styles.css`.
3. Run `python3 scripts/build.py` to regenerate HTML, `sitemap.xml` and `robots.txt`.
4. Run `python3 scripts/validate.py` to check generated files, translation coverage, page-preserving language links, routes, anchors, image accessibility and screenshot hashes.
5. Preview with `python3 -m http.server 8080` and check desktop, mobile, Arabic and the fixed dark appearance.

Do not hand-edit generated HTML. CSS URLs include a content hash to refresh cached styles. The new mark uses `assets/astra-mark.png` so previous visitors do not reuse the old green icon.

GitHub Pages publishes the root of `main` after each push. This public repository contains website text and selected demo assets. Application source and credentials stay in their separate repositories. Download actions open the verified universal App Store link for `com.astra.iptv` (`6816906088`).

## Real app assets

`assets/screens/<locale>/` contains actual localized simulator screenshots of iPhone, iPad and Apple TV using Astra’s fictional demo catalogue. The home pages use the 1.1.0 campaign captured on 18 November 2026. The Televizo alternative pages use the Apple TV guide from the same campaign. The captures were resized proportionally and encoded for the web. WebP is used for page images and JPEG for social previews. All website images are served locally.

`assets/screens/manifest.json` records the capture date, app source commit, original paths and input and output hashes. The importer verifies each native capture against the App Store campaign report before encoding any images. It reads the published website version from `content/config.json`.

To reproduce this capture set, retain the native campaign files in the private app checkout and use `cwebp` and macOS `sips`.

```sh
python3 scripts/import-assets.py --app-root ../AstraIPTV --native-root output/store-110/raw --capture-date 2026-11-18
python3 scripts/build.py
python3 scripts/validate.py
```

## Apple acquisition channel

The landing pages link directly to the App Store and to their localized connection guide. App sharing links carry `utm_source=astra_app&utm_medium=share&utm_campaign=v1_apple`. These labels identify the link; this static website does not count visits or attribute installs.

The iOS/iPadOS and tvOS 1.0.0 listings were verified as downloadable through ASC CLI, with public Spanish and US listings, on 2026-10-16. The store URL is configured in `content/config.json`. Generate the first campaign link in App Store Connect App Analytics and use its actual `pt` token; ASC provider/team IDs are not campaign tokens. The draft configuration remains in `acquisition/apple-campaigns.json`. Add distinct short campaign names for the new locale routes when configuring Apple campaign links. Read acquisition reports in ASC and compare activation in consented production installations in Firebase separately. Unavailable campaign data is not zero conversions. Paid traffic requires an explicit budget.

### Televizo searches

The `televizo-ios.html` page, `televizo-ios-en.html` and `<locale>/televizo-ios.html` routes explain Astra as an independent alternative for Apple devices. They cover all twelve site languages and the fifteen researched storefronts without duplicating pages for countries sharing a language. `content/televizo.json` holds the copy. Every localized page has a download action, source reconnection instructions, a current reference to Televizo’s own website, a clear independence notice and a real localized Astra channel-guide screenshot. Footer links, reciprocal language menus and the sitemap make the pages discoverable. Publishing these pages does not prove indexing, web ranking or App Store ranking gains.

The campaign names in `acquisition/apple-campaigns.json` are preparation for App Analytics links. The provider token is still unset; the pages deliberately use the working universal App Store link and do not claim attributed installs. A separate live-TV product page is being prepared in App Store Connect; do not link visitors to its `ppid` until its approved, available state has been checked. Advertising and organic rankings must be measured separately.

## Android review documents

`content/android.json` contains separate Android and Android TV support and privacy disclosures in Spanish and English. `scripts/build.py` generates `privacy-android.html`, `privacy-android-en.html`, `support-android.html` and `support-android-en.html`, retaining the existing Apple disclosures. These pages describe Android Keystore/local storage, source connections and optional Firebase collection, and are included in the sitemap and validation.
