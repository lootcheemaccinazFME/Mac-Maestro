"""Download provider-hosted MP4s beside this manifest; preserve existing files."""
import json
from pathlib import Path
from urllib.request import urlopen
import shutil

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
for clip in manifest['clips']:
    dest = root / Path(clip['filename']).name
    if dest.exists():
        print(f'Already present: {dest.name}')
        continue
    temp = dest.with_suffix('.mp4.part')
    try:
        with urlopen(clip['video_url'], timeout=120) as src, temp.open('wb') as out:
            shutil.copyfileobj(src, out)
        if temp.stat().st_size == 0:
            raise RuntimeError('Empty download')
        temp.replace(dest)
        print(f'Downloaded: {dest.name}')
    except Exception:
        temp.unlink(missing_ok=True)
        raise
