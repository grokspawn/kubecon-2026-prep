# Source-derived SDK theme

All artifacts in this directory are new. The source deck, dry-run generator,
slide-data JSON, import helper and existing dry-run outputs were preserved.

## Prepared artifacts

- `theme.json`: effective slide-3 typography, colors, geometry and provenance.
- `assets/s01.svg` through `s20.svg`: palette-only changes, with unchanged SVG text and geometry.
- `assets/s01.png` through `s20.png`: local Sharp rasterizations at original dimensions.
- `apply-theme.py`: relationship-only SDK master/layout application.
- `layout-integration-test.pptx`: **layout-only integration test**, not the visually finished final deck.
- `applytheme-report.json`: test-package preservation and relationship results.

## Profile contract

Colors are six-digit RGB without `#`. Bounds are points on a 720 × 405 pt canvas.

```json
{
  "font": "Arial",
  "titleColor": "00144C",
  "bodyColor": "052243",
  "background": "FFFFFF",
  "sourceLayoutPart": "ppt/slideLayouts/slideLayout5.xml",
  "brandingFooterTopPt": 361.528819,
  "diagramColors": {
    "background": "FFFFFF",
    "ink": "000000",
    "navy": "00144C",
    "flow": "113E82",
    "highlight": "D62293",
    "muted": "052243",
    "line": "ADC5EF",
    "flowFill": "E3F6FF",
    "highlightFill": "FFEE88",
    "white": "FFFFFF"
  },
  "assetsDir": "/Users/jordan/Documents/devel/breadcrumbs/2026-kubecon-wip/dry-run/theme/assets"
}
```

The `devel` workspace resolves to `Documents/devel` on this machine; both paths
identify the same directory. The profile uses the resolved absolute path.

Slide 3 uses Arial **28 pt bold** for the title and **12 pt** for first-level
body text. Its body color is `052243`, not black: the layout inherits the master
body placeholder's `dk2`. The existing dry-run PDF independently confirms
`00144C` titles and `052243` body text. Diagram ink is theme `dk1` (`000000`).
The linked theme is `ppt/theme/theme2.xml`; taking theme1 or accent1 as the title
color would give an incorrect result.

## Footer and content placement

The inherited branding image is `ppt/media/image8.png`, supplied by layout5.
Slide 3 itself contains no pictures. The master supplies inherited typography;
the layout supplies this footer logo image.

| Element | x | y | width | height |
|---|---:|---:|---:|---:|
| Title | 24.543307 | 35.041339 | 670.913386 | 45.094488 |
| Body | 24.543307 | 90.746063 | 670.913386 | 261.212598 |
| Branding | 24.543307 | 361.528819 | 87.590551 | 36.813465 |

Branding ends at **398.342284 pt**. Reserve the full-width band from
**361.528819 to 405 pt**. Recommended generated content bottom:
**351.528819 pt**, leaving 10 pt clearance. Caption and diagram boxes must end
at or above that boundary. At the old diagram top of 128 pt, the maximum height
is 223.528819 pt; preserve its 3:2 ratio when resizing. The old 351 pt caption
and 389 pt dry-run footer conflict with the branding reserve and need new
positions in the final generator. Keep speaker assignments, timing, sources and
handoff details in speaker notes, outside the slide canvas.

## Integration

The final-deck generator should consume profile colors/fonts, use these themed
assets, and reserve the footer before importing the SDK slides. After running
the existing SDK importer on that generated output:

```sh
python3 -B /Users/jordan/devel/breadcrumbs/2026-kubecon-wip/dry-run/theme/apply-theme.py \
  --pptx /PATH/TO/GENERATED-FINAL.pptx \
  --profile /Users/jordan/devel/breadcrumbs/2026-kubecon-wip/dry-run/theme/theme.json
```

The applicator writes `applytheme-report.json` beside the supplied PPTX. It
preserves the existing layout relationship ID, changes its target to
`../../sdk/ppt/slideLayouts/slideLayout5.xml`, and verifies that the SDK master is
already registered. Content, notes, media and every `sdk/` part remain
byte-identical to the input package. Only generated displayed-slide relationship
parts can change. The original source deck is rejected as an output target.

`prepare-theme.py` was run successfully. It is a create-only producer: a repeat
run in this populated directory deliberately refuses existing outputs.

## Checks completed

- 20 SVGs: exact non-color markup comparison, including geometry and text.
- 20 PNGs: generated using installed local Sharp; valid PNG signatures.
- 15 generated displayed slides: reassigned to SDK layout5.
- All 10 authored SDK slide XML parts: byte-identical to original source slides 3–12.
- All 11 source media parts: byte-identical to original source.
- Every SDK part, generated slide XML, notes part and unrelated part: unchanged against test input.
- Internal relationships: valid before and after ZIP round trip.
- Display order: unchanged; 25 displayed slides.
- Repeat in-memory application: byte-idempotent.
- Package without imported SDK parts: rejected.
- Source SHA-256: `dac21407ed62d03b404155a3bf6cbde10a22412d407c90485534eb3a28cba92c`.

## Limits

Layout application preserves explicit shape formatting and image pixels, so it
does not restyle an already-built dry-run deck. The supplied integration test
therefore retains its old generated colors and placement. A final generator must
use the profile and assets. Opaque generated shapes or `showMasterSp="0"` can
hide inherited branding. A visually finished final deck still requires rendered
review after integration; no new final-deck render was performed here.
