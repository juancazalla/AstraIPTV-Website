#!/usr/bin/env python3
"""Encode verified native TV-guide captures for the Televizo alternative pages."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app-root', type=Path, required=True)
    args = parser.parse_args()
    app_root = args.app_root.resolve()
    config = json.loads((ROOT / 'content/config.json').read_text())
    campaign = json.loads((app_root / 'release/app-store/campaign-1.0.2-manifest.json').read_text())
    inputs = []
    # Verify every input before modifying public images. No user sources are used.
    for locale in config['locales']:
        asset = next(item for item in campaign['assets']
                     if item['file'] == f'tvos/exports/{locale["screenshot"]}/03-guide.jpg')
        capture = asset['provenance']
        source = app_root / capture['native']
        if hashlib.sha256(source.read_bytes()).hexdigest() != capture['nativeSHA256']:
            parser.error(f'Native capture does not match frozen provenance: {source.name} ({locale["code"]})')
        inputs.append((locale['code'], source, capture))
    outputs = []
    for code, source, capture in inputs:
        destination = ROOT / f'assets/screens/{code}/guide.webp'
        subprocess.run(['cwebp', '-quiet', '-q', '88', '-m', '6', '-resize', '1600', '0',
                        str(source), '-o', str(destination)], check=True)
        outputs.append({'locale': code, 'source': capture['native'],
                        'source_sha256': capture['nativeSHA256'],
                        'output': str(destination.relative_to(ROOT)),
                        'output_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                        'bytes': destination.stat().st_size})
    manifest = {'campaign': '1.0.2', 'native_capture_batch': '2026-10-27',
                'content': 'Native Astra TV guide with fictional demo channels; resize and encode only.',
                'assets': outputs}
    (ROOT / 'assets/screens/guide-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'Imported {len(outputs)} verified guide screenshots.')


if __name__ == '__main__':
    main()
