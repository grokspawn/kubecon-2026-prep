// One-shot read-only reader for the imported KubeCon 2026 Google Slides
// deck. Reuses the saved OAuth credentials of the local google-docs MCP
// server; performs a single presentations.get and prints slide order,
// text and notes as JSON. No writes of any kind.
import { createRequire } from 'node:module';

const root = '/Users/jordan/devel/mcp-googledocs-server';
const require = createRequire(`${root}/package.json`);
const presentationId = '1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8';

function extract(elements = []) {
  const text = [];
  const images = [];
  for (const element of elements) {
    const runs = element.shape?.text?.textElements ?? [];
    const value = runs.map(run => run.textRun?.content ?? '').join('').trim();
    if (value) text.push(value);
    for (const row of element.table?.tableRows ?? []) {
      text.push(row.tableCells.map(cell => (cell.text?.textElements ?? [])
        .map(run => run.textRun?.content ?? '').join('').trim()).join(' | '));
    }
    if (element.image) images.push({ title: element.title ?? '', description: element.description ?? '' });
    if (element.elementGroup?.children) {
      const children = extract(element.elementGroup.children);
      text.push(...children.text);
      images.push(...children.images);
    }
  }
  return { text, images };
}

const { google } = require('googleapis');
const { authorize } = await import(`${root}/dist/auth.js`);
const auth = await authorize();
const slidesApi = google.slides({ version: 'v1', auth });
const { data } = await slidesApi.presentations.get({ presentationId }, { timeout: 30000 });
const slides = (data.slides ?? []).map((slide, index) => ({
  number: index + 1,
  objectId: slide.objectId,
  ...extract(slide.pageElements),
  notes: extract(slide.slideProperties?.notesPage?.pageElements).text,
  skipped: slide.slideProperties?.isSkipped ?? false,
}));
console.log(JSON.stringify({ title: data.title, slideCount: slides.length, slides }, null, 1));
