#!/usr/bin/env python3
"""Reassign generated displayed slides to the imported SDK layout, in place.

Run ONLY on a generated final output after import-sdk.py. Direct shape formatting
and images must already use theme.json; this tool preserves their XML verbatim.
"""
import argparse
import importlib.util
import io
import json
import os
import posixpath as pp
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('sdk_import', HERE.parent / 'import-sdk.py')
sdk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdk)


def apply(parts, profile):
    sdk.validate_relationships(parts)
    sdk.require(sdk.canvas(parts) == sdk.CANVAS, 'Canvas differs from SDK source')
    layout = 'sdk/' + profile['sourceLayoutPart']
    sdk.require(layout in parts, 'Run import-sdk.py first: missing ' + layout)
    masters = [sdk.resolve(layout, r.get('Target')) for r in sdk.relationships(parts, layout)
               if r.get('Type') == sdk.R + '/slideMaster']
    registered = {sdk.resolve(sdk.PRES, r.get('Target')) for r in sdk.relationships(parts, sdk.PRES)
                  if r.get('Type') == sdk.R + '/slideMaster'}
    sdk.require(len(masters) == 1 and masters[0] in registered, 'SDK master is not registered')
    pres_ids = sdk.xml(parts[sdk.PRES]).find('{' + sdk.P + '}sldMasterIdLst')
    master_ids = {n.get('{' + sdk.R + '}id') for n in pres_ids}
    sdk.require(any(r.get('Id') in master_ids and sdk.resolve(sdk.PRES, r.get('Target')) == masters[0]
                    for r in sdk.relationships(parts, sdk.PRES) if r.get('Type') == sdk.R + '/slideMaster'),
                'SDK master missing from presentation master list')
    output = dict(parts)
    changed = []
    for number, slide in enumerate(sdk.displayed(parts), 1):
        if slide.startswith('sdk/'):
            continue
        name = sdk.rels_name(slide)
        root = sdk.xml(parts[name])
        rels = [r for r in root if r.get('Type') == sdk.R + '/slideLayout']
        sdk.require(len(rels) == 1, 'Expected exactly one existing slideLayout: ' + slide)
        old = rels[0].get('Target')
        target = pp.relpath(layout, pp.dirname(slide))
        rels[0].set('Target', target)
        if old != target:
            output[name] = sdk.serialize(root, parts[name])
        changed.append({'displayedSlide': number, 'part': slide, 'relationshipId': rels[0].get('Id'),
                        'previousTarget': old, 'target': target})
    sdk.require(changed, 'No generated displayed slides found')
    verify(parts, output, {sdk.rels_name(s['part']) for s in changed})
    return output, changed


def verify(before, after, allowed):
    sdk.require(set(before) == set(after), 'Package part set changed')
    for name in before:
        if name not in allowed:
            sdk.require(before[name] == after[name], 'Protected part changed: ' + name)
    sdk.require(sdk.displayed(before) == sdk.displayed(after), 'Slide display order changed')
    sdk.validate_relationships(after)
    for name in allowed:
        old, new = sdk.xml(before[name]), sdk.xml(after[name])
        for node in old:
            if node.get('Type') == sdk.R + '/slideLayout':
                node.set('Target', next(n.get('Target') for n in new if n.get('Id') == node.get('Id')))
        sdk.require(sdk.xml(sdk.serialize(old, before[name])).tag == new.tag, 'Relationship root changed')
        sdk.require(sdk.ET.tostring(old) == sdk.ET.tostring(new), 'Non-layout relationship changed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pptx', type=Path, required=True)
    parser.add_argument('--profile', type=Path, required=True)
    args = parser.parse_args()
    profile = json.loads(args.profile.read_text())
    pptx = args.pptx.resolve()
    sdk.require(pptx != Path(profile['source']).resolve(), 'Refusing to modify source deck')
    sdk.require(pptx.suffix.lower() == '.pptx' and pptx != args.profile.resolve(), 'Expected generated PPTX')
    before = sdk.package(pptx)
    after, slides = apply(before, profile)
    buffer = io.BytesIO()
    with zipfile.ZipFile(pptx) as original, zipfile.ZipFile(buffer, 'w') as archive:
        archive.comment = original.comment
        for info in original.infolist():
            archive.writestr(info, after.get(info.filename, original.read(info.filename)))
    buffer.seek(0)
    with zipfile.ZipFile(buffer) as archive:
        sdk.require(archive.testzip() is None, 'ZIP CRC failure')
        roundtrip = {n: archive.read(n) for n in after}
    verify(before, roundtrip, {sdk.rels_name(s['part']) for s in slides})
    # Validate everything before replacing the generated output.
    temp = pptx.with_name(pptx.name + '.theme-new')
    with temp.open('xb') as f:
        f.write(buffer.getvalue())
    os.replace(temp, pptx)
    report = {'status': 'verified', 'pptx': str(pptx), 'profile': str(args.profile.resolve()),
              'sourceLayoutPart': profile['sourceLayoutPart'], 'generatedSlides': slides,
              'sdkPartsByteIdentical': True, 'sdkSlideXmlByteIdentical': True, 'sdkMediaByteIdentical': True,
              'generatedSlideXmlByteIdentical': True, 'notesByteIdentical': True,
              'onlyGeneratedLayoutRelationshipsChanged': True, 'relationshipsValid': True,
              'displayedSlides': len(sdk.displayed(after)), 'sdkPartsChecked': sum(n.startswith('sdk/') for n in before),
              'outputSha256': sdk.digest(buffer.getvalue()),
              'limitations': ['Explicit shape formatting and image pixels are preserved; generate them using theme.json.',
                              'Opaque content or showMasterSp=0 can hide inherited branding; reserve the footer before generating.',
                              'No visual rendering validation is performed by this relationship-only applicator.']}
    report_path = pptx.with_name('applytheme-report.json')
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'generatedSlides': len(slides), 'report': str(report_path)}))


if __name__ == '__main__':
    main()
