# Localization source

`config.json` defines the 12 fully supported Apple app localizations and their native screenshot locales. The set was checked against the app’s Xcode regions and complete string-catalog coverage on 2026-10-12.

Each `locales/<code>.json` contains the same 120 text units for the four page types. `structure.json` defines the order of guide, support and privacy sections and preserves the published external policy/contact destinations. The generator localizes internal destinations and uses service names for external link labels.

Spanish support/privacy wording was preserved from the published website. New locale drafts were translated from the equivalent English text with Google Translate’s public text interface on 2026-10-12, then reviewed for completeness and the technical privacy disclosures. Headlines, key actions, device descriptions, email behavior and native app button labels were edited separately. Spanish (Latin America) uses the Spanish text with regional wording; Portuguese (Brazil) and Portuguese (Portugal) have separate text. No visitor content is sent to a translation service.

For future changes, preserve explicit consent, data exclusions, retention periods, deletion limits and the distinction between requesting a rating and actually receiving one. Do not publish credentials, private source URLs or real customer content.
