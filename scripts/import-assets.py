#!/usr/bin/env python3
"""Import real Apple demo screenshots, resizing and encoding only (requires cwebp)."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--app-root',type=Path,required=True)
parser.add_argument('--native-root',type=Path,help='New native captures: <locale>/<iphone|ipad|tv>.png. Defaults to the archived fictional release captures.')
parser.add_argument('--capture-date',default='2026-10-09')
parser.add_argument('--capture-metadata',type=Path,help='Capture provenance JSON for a new native capture batch.')
args=parser.parse_args()
if args.native_root and not args.capture_metadata:
    parser.error('--native-root requires --capture-metadata to preserve screenshot provenance')
config=json.loads((ROOT/'content/config.json').read_text())
assets=[]
social_assets=[]
for locale in config['locales']:
    code, native=locale['code'],locale['screenshot']
    for device,width in [('iphone',864),('ipad',1080 if args.native_root else 960),('tv',1600 if args.native_root else 1280)]:
        source=(str((args.native_root/code/f'{device}.png').resolve().relative_to(args.app_root.resolve())) if args.native_root else
                f'release/app-store/tvos/raw/{native}/01-library.png' if device=='tv' else f'release/app-store/raw/{native}/{device}/01-library.png')
        path=args.app_root/source
        destination=f'assets/screens/{code}/{device}.webp'
        target=ROOT/destination
        target.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['cwebp','-quiet','-q','88','-m','6','-resize',str(width),'0',str(path),'-o',str(target)],check=True)
        assets.append({'locale':code,'device':device,'source':source,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'output':destination,'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'bytes':target.stat().st_size})

        if device=='tv':
            social=target.with_suffix('.jpg')
            subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','88','-Z','1280',str(path),'--out',str(social)],stdout=subprocess.DEVNULL,check=True)
            social_assets.append({'locale':code,'source':source,'output':str(social.relative_to(ROOT)),'output_sha256':hashlib.sha256(social.read_bytes()).hexdigest()})
shutil.copyfile(args.app_root/'Astra/Resources/Assets.xcassets/BrandMark.imageset/brand-mark.png', ROOT/'assets/astra-mark.png')
manifest={'description':'Actual simulator screenshots of Astra demo mode. Encoding and proportional resize only; no interface reconstruction or content edits. Fictional titles, no playable streams.','ios_capture_date':'2026-10-09','ios_source_commit':'72bc4e4e0a85c583728657179b9d47a9658a9311','assets':assets,'social_assets':social_assets}
if args.native_root:
    metadata=json.loads(args.capture_metadata.read_text())
    manifest={**metadata,'capture_date':args.capture_date,'assets':assets,'social_assets':social_assets}
(ROOT/'assets/screens/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'Imported {len(assets)} screenshots: {sum(a["bytes"] for a in assets)/1024/1024:.2f} MiB total.')
