# Apple playback engine experiment

`apple-player-experiment.json` is a public, non-sensitive feature flag consumed by future Astra Apple releases. It contains only rollout controls; never add credentials, installation identifiers, provider URLs or personal data here.

As of 2026-11-04 the experiment is paused (`enabled=false`): VLC is the default until the updated app is released and the experiment is explicitly activated. The stored 50/50 split is inactive while the flag is disabled. Manual player choices remain effective.

- `schemaVersion`: keep at 1 for this client schema.
- `experimentVersion`: integer 1–10000. Increase it when intentionally starting a new allocation/analysis period.
- `enabled`: false restores the ordinary VLC default on the next player opening after clients refresh. Manual player choices always win.
- `aetherPercent`: integer 0–100, used for new allocations only. Existing installations retain their allocation within the same experiment version. The initial split is 50/50.

The app reads this asynchronously only for consenting eligible releases without a valid manual engine preference. A channel never waits for the download. Refresh is throttled to 15 minutes within a process; cached policies expire after 24 hours. Offline/invalid/expired policy means the ordinary VLC default, labeled separately in analytics. A rollout change does not switch an already open player. Consent withdrawal clears local experiment state while retaining manual preferences.

Publishing this file does not distribute an app build or change existing released clients that do not read this flag. The Apple source, telemetry definitions and experiment analysis guide are maintained in `juancazalla/Astra-iOS`, release/1.1.0. Recheck the deployed JSON after GitHub Pages has published a change.
