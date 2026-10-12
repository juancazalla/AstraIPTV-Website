# Astra IPTV — project website

Public project website for Astra IPTV, a native player in development for iPhone, iPad and Apple TV.

- Spanish: https://juancazalla.github.io/AstraIPTV-Website/
- English: https://juancazalla.github.io/AstraIPTV-Website/en.html

## Editing and publishing

Static HTML and CSS, with no build tools, JavaScript, analytics or credentials. Edit `index.html` (Spanish), `en.html` (English) and `styles.css`. Keep both languages in sync. Preview with `python3 -m http.server 8080` from this directory.

GitHub Pages publishes the root of `main` after each push. This public repository contains only the website and selected demo assets. Application source code is maintained separately in private repositories.

## Assets and project status

Screenshots were captured on 2026-09-27 from the current Apple release build (app commit `6acf104`) on iPhone and iPad simulators. They show the app's demo mode with fictional titles, not bundled streams. The Apple app is not yet available on the App Store.

The Astra brand assets and demo screenshots belong to the project. Demo photography is from Unsplash; the mountain photograph is https://images.unsplash.com/photo-1464822759023-fed622ff2c3b.

English screenshots are separate `*-demo-en.png` assets captured from app commit `c7b9f56`, with the home screen and demo content localized to English. Spanish screenshots remain unchanged.

## App support and privacy

Spanish support/privacy pages are `support.html` and `privacy.html`; English equivalents are `support-en.html` and `privacy-en.html`. These cover the standalone iPhone/iPad app and its local storage, private CloudKit synchronization, provider connections and metadata services. Contact uses the developer address already present in public Git history and public website issues. Do not publish provider credentials in support reports.

## Apple acquisition channel

The Spanish/English landing pages lead to `start.html` / `start-en.html` and an optional launch notification email composed by the visitor. No mail is sent automatically and no third party is invited. Support and privacy cover Apple TV as well as iPhone/iPad.

App sharing links carry `utm_source=astra_app&utm_medium=share&utm_campaign=v1_apple`. These labels identify the link; this static site has no analytics SDK, so they do not by themselves count visits or attribute installs.

When both Apple listings are public, replace the launch-notification action with the verified App Store URL. Generate the first campaign link in App Store Connect App Analytics and copy its actual `pt` token. The ASC provider/team IDs are not campaign tokens. Use distinct campaign names (`v1_web_es`, `v1_web_en`, `v1_app_share`, `v1_guide_es`, `v1_guide_en`), under 30 characters. Read installation/discovery reports from ASC, and compare activation in consented production installations in Firebase separately. Apple may withhold small campaign samples; unavailable data is never zero conversions. Do not launch paid traffic without an explicit budget.
