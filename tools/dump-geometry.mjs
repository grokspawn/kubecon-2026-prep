// Dump geometry of selected slides (read-only) for update planning.
import { createRequire } from 'node:module';

const root = '/Users/jordan/devel/mcp-googledocs-server';
const require = createRequire(`${root}/package.json`);
const { google } = require('googleapis');
const { authorize } = await import(`${root}/dist/auth.js`);

const presentationId = '1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8';
const auth = await authorize();
const api = google.slides({ version: 'v1', auth });
const { data } = await api.presentations.get({ presentationId });
const PT = 12700;

for (const idx of [4, 5, 13, 0]) {
  const slide = data.slides[idx];
  console.log(`=== displayed slide ${idx + 1} objectId ${slide.objectId}`);
  for (const el of slide.pageElements) {
    const t = el.transform;
    if (el.shape) {
      const txt = (el.shape.text?.textElements ?? []).map(r => r.textRun?.content ?? '').join('').trim().slice(0, 55);
      console.log(`  shape ${el.shape.placeholder?.type ?? 'plain'} ${el.objectId} pos ${Math.round(t.translateX / PT)},${Math.round(t.translateY / PT)} size ${Math.round((el.size?.width ?? 0) / PT)}x${Math.round((el.size?.height ?? 0) / PT)} ${JSON.stringify(txt)}`);
    }
    if (el.image) console.log(`  image ${el.objectId}`);
  }
  const notes = slide.slideProperties?.notesPage;
  console.log('  --- notes page:');
  for (const el of notes?.pageElements ?? []) {
    if (el.shape && (el.shape.placeholder || (el.shape.text?.textElements ?? []).length)) {
      const txt = (el.shape.text?.textElements ?? []).map(r => r.textRun?.content ?? '').join('').trim().slice(0, 40);
      console.log(`    ${el.shape.placeholder?.type ?? 'plain'} ${el.objectId} ${JSON.stringify(txt)}`);
    }
  }
}
