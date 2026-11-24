#!/usr/bin/env python3
"""Encode the verified fictional demo captures from Astra's App Store campaign."""
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
    args = parser.parse_args()
    config = json.loads((ROOT / 'content/config.json').read_text())
    app_root = args.app_root.resolve()
    native_root = (app_root / args.native_root).resolve().relative_to(app_root)
    evidence = Path('release/app-store') / f"campaign-{config['app_version']}" / 'verification/campaign.json'
    report = json.loads((app_root / evidence).read_text())
    if report['version'] != config['app_version']:
        parser.error('Campaign verification does not match the website version')
    verified = {}
    for record in report['nativeScenes']:
        _, locale, device, filename = Path(record['file']).parts
        scene = Path(filename).stem.split('-', 1)[1]
        verified[locale, device, scene] = record

    # Wait until all input hashes match the reviewed campaign before writing any public asset.
    inputs = []
    for locale in config['locales']:
        for name, (device, scene, width) in SCENES.items():
            native_locale = locale['screenshot']
            record = verified[native_locale, device, scene]
            source = native_root / native_locale / device / f'{scene}.jpg'
            if sha256(app_root / source) != record['nativeSHA256']:
                parser.error(f'Capture does not match campaign verification: {source}')
            inputs.append((locale['code'], name, width, source, record['nativeSHA256']))

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
        'content': 'Native simulator captures of the fictional Astra demo catalogue. Proportional resize and encoding only.',
        'assets': assets,
        'social_assets': social_assets,
    }
    (ROOT / 'assets/screens/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'Imported {len(assets)} verified screenshots and {len(social_assets)} social previews.')


if __name__ == '__main__':
    main()
