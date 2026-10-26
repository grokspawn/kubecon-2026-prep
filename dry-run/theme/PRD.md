---
task: Derive source theme assets and preserve SDK packaging
effort: standard
phase: complete
progress: 8/8
mode: interactive
---

## Context

Create source-derived theming helpers and assets only under dry-run/theme.
No voice, external calls, source edits or existing generator edits.

## Criteria

- [x] ISC-1: Profile resolves actual technical slide three title styling.
- [x] ISC-2: Profile records effective technical slide three body styling.
- [x] ISC-3: Profile records inherited layout footer branding image bounds.
- [x] ISC-4: Twenty SVG assets preserve their original non-color markup.
- [x] ISC-5: Twenty themed PNG assets use locally installed Sharp.
- [x] ISC-6: Applicator reassigns fifteen generated displayed slide layout relationships.
- [x] ISC-7: Authored SDK slides remain byte-identical to original source.
- [x] ISC-8: Applicator output passes package internal relationship integrity checks.

## Decisions

Use the original slide3 → layout5 → master1 → theme2 inheritance chain.
Record actual body navy 052243; retain theme black as diagram ink.
Test on a new layout-only package, preserving existing workspace artifacts.

## Verification

prepare-theme.py completed. check-theme.py completed against the existing
25-slide combined deck: 15 generated layouts, 10 SDK slide XML parts and 11
source media parts verified. Non-layout parts remain byte-identical. Repeat
application is idempotent. Existing PDF text extraction independently confirms
title/body colors and effective text sizes. New final-deck rendering is pending
the primary generator's integration of profile, assets and footer reserve.
