import collections
import json
import re
import zipfile
import xml.etree.ElementTree as E
from pathlib import Path
import posixpath as pp

P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
with zipfile.ZipFile('/Users/jordan/Downloads/Copy of KubeCon2026.pptx') as z:
    part = 'ppt/slides/slide3.xml'
    for level in range(4):
        root = E.fromstring(z.read(part))
        print('\nPART', part, root.attrib)
        if root.tag == A + 'theme':
            print(E.tostring(root.find('.//' + A + 'clrScheme'), encoding='unicode'))
            print(E.tostring(root.find('.//' + A + 'fontScheme'), encoding='unicode'))
        for s in root.findall('.//' + P + 'spTree/*'):
            print('SHAPE', s.tag.split('}')[-1], 'TEXT', [t.text for t in s.iter(A+'t')], 'PH', [n.attrib for n in s.iter(P+'ph')], 'STYLE REF', [E.tostring(n, encoding='unicode') for n in s.findall(P+'style')])
        for tag in ('bg', 'clrMap'):
            for n in root.findall('.//' + P + tag):
                print(tag, E.tostring(n, encoding='unicode'))
        relpart = pp.join(pp.dirname(part), '_rels', pp.basename(part) + '.rels')
        if relpart not in z.namelist():
            break
        rs = E.fromstring(z.read(relpart))
        kind = ('slideLayout', 'slideMaster', 'theme', 'none')[level]
        r = next((r for r in rs if r.get('Type').endswith('/' + kind)), None)
        if r is None:
            break
        part = pp.normpath(pp.join(pp.dirname(part), r.get('Target')))
c = collections.Counter()
for f in (Path(__file__).parent.parent / 'assets').glob('s*.svg'):
    c.update(re.findall(r'#[0-9a-fA-F]{3,8}\b', f.read_text()))
print('SVG COLORS', json.dumps(c))
