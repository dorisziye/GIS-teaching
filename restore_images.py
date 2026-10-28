import re
import base64
from pathlib import Path

src_rmd = Path(r'c:\Users\ziye\Documents\GitHub\GIS-teaching\ENVS609 Practical 3.Rmd')
html = Path(r'c:\Users\ziye\Documents\GitHub\GIS-teaching\docs\ENVS609-Practical-3.html')
outdir = Path(r'c:\Users\ziye\Documents\GitHub\GIS-teaching\images')
outdir.mkdir(exist_ok=True)

md = src_rmd.read_text(encoding='utf-8', errors='ignore')
rel = re.findall(r'!\[\]\(images/([^)]+\.png)\)', md)
page = html.read_text(encoding='utf-8', errors='ignore')
data_urls = re.findall(r'src="(data:image/png;base64,[A-Za-z0-9+/=]+)"', page)

if len(data_urls) < len(rel):
    raise RuntimeError(f'Not enough embedded images: {len(data_urls)} < {len(rel)}')

for name, d in zip(rel, data_urls[: len(rel)]):
    payload = d.split(',', 1)[1]
    (outdir / name).write_bytes(base64.b64decode(payload))

print(f'restored {len(rel)} files to {outdir}')
print('\n'.join(sorted(p.name for p in outdir.iterdir())))
