#!/usr/bin/env python3
"""Encode verified Astra simulator captures for the website."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCENES = {
    'iphone': ('iphone', 'home', 880),
    'ipad': ('ipad', 'multiview', 1080),
    'tv': ('tv', 'home', 1600),
    'guide': ('tv', 'guide', 1600),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-root', type=Path, required=True)
    parser.add_argument('--native-root', type=Path, required=True, help='Capture directory relative to app-root')
    parser.add_argument('--capture-date', required=True, help='Capture date in YYYY-MM-DD format')
    parser.add_argument('--home-capture-report', type=Path, required=True,
                        help='Verified iPhone and Apple TV Home capture report relative to app-root')
    args = parser.parse_args()
    config = json.loads((ROOT / 'content/config.json').read_text())
    app_root = args.app_root.resolve()
    native_root = (app_root / args.native_root).resolve().relative_to(app_root)
    evidence = Path('release/app-store') / f"campaign-{config['app_version']}" / 'verification/campaign.json'
    report = json.loads((app_root / evidence).read_text())
    if report['version'] != config['app_version']:
        parser.error('Campaign verification does not match the website version')
    home_evidence = (app_root / args.home_capture_report).resolve().relative_to(app_root)
    home_report = json.loads((app_root / home_evidence).read_text())
    home_captures = {(item['locale'], item['device']): item for item in home_report['captures']}
    expected_home = {(locale['code'], device) for locale in config['locales'] for device in ('iphone', 'tv')}
    if set(home_captures) != expected_home or len(home_report['captures']) != len(expected_home):
        parser.error('Home capture report must cover both devices in every website locale')
    verified = {}
    for record in report['nativeScenes']:
        _, locale, device, filename = Path(record['file']).parts
        scene = Path(filename).stem.split('-', 1)[1]
        verified[locale, device, scene] = record

    # Verify every capture before writing any public asset.
    inputs = []
    for locale in config['locales']:
        code = locale['code']
        for name, (device, scene, width) in SCENES.items():
            if name in ('iphone', 'tv'):
                capture = home_captures[code, name]
                source = home_evidence.parent / capture['source']
                source_hash = capture['source_sha256']
            else:
                native_locale = locale['screenshot']
                source = native_root / native_locale / device / f'{scene}.jpg'
                source_hash = verified[native_locale, device, scene]['nativeSHA256']
            if sha256(app_root / source) != source_hash:
                parser.error(f'Capture does not match verification: {source}')
            inputs.append((code, name, width, source, source_hash))

    assets, social_assets = [], []
    for code, name, width, source, source_hash in inputs:
        target = ROOT / 'assets/screens' / code / f'{name}.webp'
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['cwebp', '-quiet', '-q', '88', '-m', '6', '-resize', str(width), '0',
                        str(app_root / source), '-o', str(target)], check=True)
        metadata = {'locale': code, 'device': name, 'source': str(source), 'source_sha256': source_hash}
        assets.append({**metadata, 'output': str(target.relative_to(ROOT)), 'output_sha256': sha256(target),
                       'bytes': target.stat().st_size})
        if name == 'tv':
            social = target.with_suffix('.jpg')
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', '-Z', '1280',
                            str(app_root / source), '--out', str(social)], stdout=subprocess.DEVNULL, check=True)
            social_assets.append({**metadata, 'output': str(social.relative_to(ROOT)), 'output_sha256': sha256(social)})
    manifest = {
        'campaign': report['version'],
        'source_commit': report['source'],
        'source_evidence': str(evidence),
        'capture_date': args.capture_date,
        'website_home_capture': {
            'app_version': home_report['app_version'],
            'capture_date': home_report['capture_date'],
            'source_evidence': str(home_evidence),
            'source_commits': home_report['source_commits'],
        },
        'content': 'Native Home captures with TMDB artwork, alongside the original Multiview and guide demo captures. Proportional resize and encoding only.',
        'assets': assets,
        'social_assets': social_assets,
    }
    (ROOT / 'assets/screens/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'Imported {len(assets)} verified screenshots and {len(social_assets)} social previews.')


if __name__ == '__main__':
    main()
