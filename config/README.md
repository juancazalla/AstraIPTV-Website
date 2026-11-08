# Apple playback engine experiment

`apple-player-experiment.json` is a public, non-sensitive feature flag consumed by future Astra Apple releases. It contains only rollout controls; never add credentials, installation identifiers, provider URLs or personal data here.

As of 2026-11-04 the experiment is paused (`enabled=false`). Builds through 72 use VLC as their ordinary default; newer builds use the operational policy below, with an Aether baseline. The stored 50/50 split is inactive while the flag is disabled. Manual player choices remain effective.

- `schemaVersion`: keep at 1 for this client schema.
- `experimentVersion`: integer 1–10000. Increase it when intentionally starting a new allocation/analysis period.
- `enabled`: false restores the app baseline when no operational default applies, on the next player opening after clients refresh. Manual player choices always win.
- `aetherPercent`: integer 0–100, used for new allocations only. Existing installations retain their allocation within the same experiment version. The initial split is 50/50.

The app reads this asynchronously only for consenting eligible releases without a valid manual engine preference. A channel never waits for the download. Refresh is throttled to 15 minutes within a process; cached policies expire after 24 hours. Offline/invalid/expired experiment policy means the app baseline, labeled separately in analytics; the newer operational policy can independently override that default. A rollout change does not switch an already open player. Consent withdrawal clears local experiment state while retaining manual preferences.

Publishing this file does not distribute an app build or change existing released clients that do not read this flag. The Apple source, telemetry definitions and experiment analysis guide are maintained in `juancazalla/Astra-iOS`, release/1.1.0. Recheck the deployed JSON after GitHub Pages has published a change.

## Playback safety controls

`apple-playback-policy.json` is the operational policy for Apple app builds that include `PlaybackFeatureFlags` (after build 72). Older app builds do not consume this endpoint. These controls are independent of analytics consent and the allocation experiment above. They never contain customer/provider data and the app does not append identifiers to its request.

The initial policy uses Aether as the default, disables VLC live rewind pending physical Apple TV stability validation, and keeps Aether live rewind enabled. Existing manual player choices remain effective. Disabling rewind prevents the VLC capture/manifest observer or Aether DVR from being enabled; it does not merely hide the timeline. Ordinary live playback and audio-track controls remain available.

- `schemaVersion`: 1.
- `revision`: integer 1–1000000. Increment for every change, including restoring a previous setting. Older revisions and changed contents with the same revision are ignored.
- `defaultEngine`: `"astra"` (VLC), `"aether"`, or `null`. A non-null value supplies the default for users without a saved manual preference. `null` delegates to the separate consented allocation experiment; its inactive/offline fallback is the app's Aether baseline.
- `liveRewind.astra`, `liveRewind.aether`: booleans enabling history independently for each engine, including users who selected that engine manually.

The app fetches asynchronously on launch/foreground and when playback controls are consulted, at most once every 15 minutes within a process. Playback never waits for the request. The last valid policy is retained offline and is not re-enabled by an arbitrary cache expiry. With no valid policy the safe defaults are Aether, VLC rewind off, Aether rewind on. An existing input keeps its captured controls; changes take effect when a subsequent input opens after refresh. Seeking within the same retained capture does not start a new policy lifetime. Test-only overrides require a Debug app launched with `--ui-testing`; they are absent from Release builds.

To change a switch, edit the policy, increment `revision`, validate with `python3 scripts/validate.py`, commit and push `main`, then wait for GitHub Pages and verify the deployed JSON. This updates supported installed app builds without another binary upload. Do not change `apple-player-experiment.json` as a substitute for these operational controls: that legacy endpoint cannot disable rewind and is intentionally consent-gated.
