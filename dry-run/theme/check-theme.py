"""Local integration check; creates a new layout-only test output in theme/."""
import importlib.util
import json
import subprocess
import sys
import xml.etree.ElementTree as E
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('apply_theme', HERE / 'apply-theme.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sdk = module.sdk
profile = json.loads((HERE / 'theme.json').read_text())
before = sdk.package(HERE.parent / 'kubecon-2026-dry-run.pptx')
target = HERE / 'layout-integration-test.pptx'
with target.open('xb') as f:
    f.write((HERE.parent / 'kubecon-2026-dry-run.pptx').read_bytes())
subprocess.run([sys.executable, '-B', str(HERE / 'apply-theme.py'), '--pptx', str(target),
                '--profile', str(HERE / 'theme.json')], check=True)
after = sdk.package(target)
source = sdk.package(profile['source'])
for n in range(3, 13):
    assert source[f'ppt/slides/slide{n}.xml'] == after[f'sdk/ppt/slides/slide{n}.xml']
for name in source:
    if name.startswith('ppt/media/'):
        assert source[name] == after['sdk/' + name]
again, slides = module.apply(after, profile)
assert again == after, 'Second application must be byte-idempotent'
assert len(slides) == 15
try:
    module.apply({k: v for k, v in before.items() if not k.startswith('sdk/')}, profile)
except (ValueError, KeyError):
    pass
else:
    raise AssertionError('Missing SDK package should fail')
for i in range(1, 21):
    png = HERE / 'assets' / f's{i:02d}.png'
    assert png.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    original = E.fromstring((HERE.parent / 'assets' / f's{i:02d}.svg').read_bytes())
    themed = E.fromstring((HERE / 'assets' / f's{i:02d}.svg').read_bytes())
    assert list(original.itertext()) == list(themed.itertext())
print(json.dumps({'status': 'passed', 'generated_layouts': 15, 'sdk_slides_identical_to_source': 10,
                  'sdk_media_identical_to_source': sum(n.startswith('ppt/media/') for n in source),
                  'svg_texts_preserved': 20, 'png_assets': 20, 'idempotent': True,
                  'source_sha256': sdk.digest(Path(profile['source']).read_bytes())}, indent=2))
body = next(s for s in sdk.xml(source['ppt/slides/slide3.xml']).iter('{' + sdk.P + '}sp')
            if any(p.get('type') == 'body' for p in s.iter('{' + sdk.P + '}ph')))
for part in ('ppt/slides/slide3.xml', 'ppt/slideLayouts/slideLayout5.xml', 'ppt/slideMasters/slideMaster1.xml'):
    for s in sdk.xml(source[part]).iter('{' + sdk.P + '}sp'):
        if any(p.get('type') in ('body', 'title') for p in s.iter('{' + sdk.P + '}ph')):
            print('STYLE REF', part, [E.tostring(n, encoding='unicode') for n in s.findall('{' + sdk.P + '}style')])
