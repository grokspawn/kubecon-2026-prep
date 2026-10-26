#!/usr/bin/env python3
"""Derive the SDK slide-3 theme and recolor local SVGs; no network access."""
import argparse
import hashlib
import json
import posixpath as pp
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/jordan/Downloads/Copy of KubeCon2026.pptx')
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def derive(source):
    with zipfile.ZipFile(source) as z:
        def root(part):
            return ET.fromstring(z.read(part))

        def related(part, kind):
            rels = root(pp.join(pp.dirname(part), '_rels', pp.basename(part) + '.rels'))
            rel = next(r for r in rels if r.get('Type').endswith('/' + kind))
            return pp.normpath(pp.join(pp.dirname(part), rel.get('Target')))

        slide_part = 'ppt/slides/slide3.xml'
        layout_part = related(slide_part, 'slideLayout')
        master_part = related(layout_part, 'slideMaster')
        theme_part = related(master_part, 'theme')
        slide, layout, master, theme = map(root, (slide_part, layout_part, master_part, theme_part))
        scheme = theme.find('.//' + A + 'clrScheme')
        colors = {n.tag.split('}')[-1]: list(n)[0].get('val', list(n)[0].get('lastClr')) for n in scheme}
        cmap = master.find(P + 'clrMap').attrib

        def color(fill):
            c = list(fill)[0]
            key = c.get('val')
            if c.tag == A + 'schemeClr':
                return colors[cmap.get(key, key)].upper()
            return (c.get('lastClr') if c.tag == A + 'sysClr' else key).upper()

        def placeholder(tree, kind):
            return next(s for s in tree.findall('.//' + P + 'sp')
                        if any(p.get('type', 'obj') == kind for p in s.iter(P + 'ph')))

        def bounds(s):
            x = s.find('./' + P + 'spPr/' + A + 'xfrm')
            off, ext = x.find(A + 'off'), x.find(A + 'ext')
            return dict(zip(('x', 'y', 'width', 'height'),
                            [round(int(v) / 12700, 6) for v in
                             (off.get('x'), off.get('y'), ext.get('cx'), ext.get('cy'))]))

        def effective(kind):
            style = {}
            for tree in (master, layout, slide):
                shape = placeholder(tree, kind)
                nodes = shape.findall('./' + P + 'txBody/' + A + 'lstStyle/' + A + 'lvl1pPr/' + A + 'defRPr')
                if tree is slide:
                    paragraph = shape.find('./' + P + 'txBody/' + A + 'p')
                    nodes += paragraph.findall('./' + A + 'pPr/' + A + 'defRPr')
                    run = paragraph.find(A + 'r')
                    if run is not None:
                        nodes += run.findall(A + 'rPr')
                for n in nodes:
                    if 'sz' in n.attrib:
                        style['size'] = int(n.get('sz')) / 100
                    if 'b' in n.attrib:
                        style['bold'] = n.get('b') == '1'
                    latin = n.find(A + 'latin')
                    if latin is not None:
                        style['font'] = latin.get('typeface')
                    fill = n.find(A + 'solidFill')
                    if fill is not None:
                        style['color'] = color(fill)
            return style

        title, body = effective('title'), effective('body')
        bg = next(t.find('./' + P + 'cSld/' + P + 'bg/' + P + 'bgPr/' + A + 'solidFill')
                  for t in (slide, layout, master)
                  if t.find('./' + P + 'cSld/' + P + 'bg/' + P + 'bgPr/' + A + 'solidFill') is not None)
        branding = []
        for part, tree in ((layout_part, layout), (master_part, master)):
            for pic in tree.findall('./' + P + 'cSld/' + P + 'spTree/' + P + 'pic'):
                box = bounds(pic)
                if box['y'] >= 405 / 2:
                    relid = pic.find('.//' + A + 'blip').get(R + 'embed')
                    rels = root(pp.join(pp.dirname(part), '_rels', pp.basename(part) + '.rels'))
                    rel = next(r for r in rels if r.get('Id') == relid)
                    branding.append({'part': part, 'mediaPart': pp.normpath(pp.join(pp.dirname(part), rel.get('Target'))), **box})
        assert branding, 'No inherited footer branding found'
        palette = {'background': color(bg), 'ink': colors['dk1'], 'navy': title['color'],
                   'flow': colors['lt2'], 'highlight': colors['accent1'],
                   'muted': colors['dk2'], 'line': colors['hlink'],
                   'flowFill': colors['accent6'], 'highlightFill': colors['accent2'],
                   'white': colors['lt1']}
        return {'font': title['font'], 'titleColor': title['color'], 'bodyColor': body['color'],
                'background': color(bg), 'sourceLayoutPart': layout_part,
                'brandingFooterTopPt': min(b['y'] for b in branding), 'diagramColors': palette,
                'assetsDir': str(HERE / 'assets'), 'titleFont': title['font'], 'bodyFont': body['font'],
                'titleFontSizePt': title['size'], 'bodyFontSizePt': body['size'], 'titleBold': title['bold'],
                'titleBoundsPt': bounds(placeholder(slide, 'title')),
                'bodyBoundsPt': bounds(placeholder(slide, 'body')),
                'brandingBoundsPt': branding, 'sourceMasterPart': master_part, 'sourceThemePart': theme_part,
                'themeColors': colors, 'source': str(source.resolve()),
                'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'canvasPt': [720, 405],
                'recommendedContentBottomPt': min(b['y'] for b in branding) - 10,
                'notesPlacement': 'Keep speaker assignments, timing and sources in notesSlide parts, outside the slide canvas.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    args = parser.parse_args()
    profile = derive(args.source)
    target = HERE / 'theme.json'
    assert not target.exists(), 'Refusing to overwrite existing theme.json'
    assets = HERE / 'assets'
    assets.mkdir(exist_ok=True)
    p = profile['diagramColors']
    mapping = {'F5F7FA': p['background'], '14263D': p['ink'], 'FFFFFF': p['white'],
               '007F86': p['flow'], 'B66A00': p['highlight'], '5D6B7B': p['muted'],
               'CBD5E1': p['line'], 'FFF2DF': p['highlightFill'], 'E4F2F2': p['flowFill']}
    count = 0
    for i in range(1, 21):
        name = f's{i:02d}.svg'
        original = (HERE.parent / 'assets' / name).read_text()
        unknown = set(re.findall(r'#([0-9A-Fa-f]{6})\b', original)) - set(mapping)
        assert not unknown, f'Unmapped colors: {unknown}'
        themed = re.sub(r'#([0-9A-Fa-f]{6})\b', lambda m: '#' + mapping[m[1].upper()], original)
        # Prove only colors changed: texts, path geometry and all other markup match.
        assert re.sub(r'#[0-9A-Fa-f]{6}\b', '#COLOR', original) == re.sub(r'#[0-9A-Fa-f]{6}\b', '#COLOR', themed)
        out = assets / name
        assert not out.exists(), f'Refusing to overwrite {out}'
        out.write_text(themed)
        count += 1
    target.write_text(json.dumps(profile, indent=2) + '\n')
    subprocess.run(['node', str(HERE / 'rasterize-assets.cjs'), str(target)], check=True)
    print(json.dumps({'profile': str(target), 'recolored': count, **profile}, indent=2))


if __name__ == '__main__':
    main()
