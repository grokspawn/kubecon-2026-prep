const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');

const root = __dirname;
process.env.NODE_PATH = path.join(root, 'node_modules');
require('node:module').Module._initPaths();
process.env.PLAYWRIGHT_BROWSERS_PATH = path.join(root, 'cache', 'playwright');
const PptxGenJS = require('pptxgenjs');
const sharp = require('sharp');
const { chromium } = require('playwright');
const launchChromium = chromium.launch.bind(chromium);
// The shared converter prefers a system Chrome on macOS. Use our workspace
// Chromium instead without changing that shared converter or global config.
chromium.launch = options => {
  const local = { ...options, env: { ...process.env, ...options?.env } };
  delete local.channel;
  return launchChromium(local);
};
const html2pptx = require('/Users/jordan/.claude/skills/Utilities/Documents/Pptx/Scripts/html2pptx.js');
const data = require('./slide-data.json');
const TITLE = 'The Next Era of Kubernetes Operator Lifecycle Management';
const BASE_SLIDES = 17;
const SDK_SLIDES = 10;
const SDK_INSERT_AFTER = 15;
const SDK_SECONDS = 600;
const TOTAL_SLIDES = BASE_SLIDES + SDK_SLIDES;
const BASE_SECONDS = 1320;

const esc = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const clock = seconds => `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
const contrast = /,\s*not\b|(?:—|--)\s*(?:not|they)\b|\b(?:do|does)\s+not\b[^.\n]{0,100}\bthey\b/i;
const ownership = /\bAttila\b|\bOLM\s+[ABC]\b|\bspeaker\b|\bhandoff\b|\bthree OLM\b/i;

function checkCopy() {
  if (data[0].title !== TITLE) throw new Error('Opening title differs from confirmed title.');
  for (const [index, item] of data.entries()) {
    const visible = [item.title, item.section, item.status, item.lead, ...item.bullets, item.caption].join('\n');
    if (contrast.test(visible) || contrast.test(item.notes)) throw new Error(`Contrast wording on slide ${index + 1}`);
    if (ownership.test(visible)) throw new Error(`Visible speaker assignment on slide ${index + 1}`);
  }
}

function outputNumber(index) {
  return index + 1 + (index >= SDK_INSERT_AFTER ? SDK_SLIDES : 0);
}

function slideHtml(item, index, variant, theme, imageSize) {
  const final = variant === 'final';
  const imageFile = item.imagePath
    ? (path.isAbsolute(item.imagePath) ? item.imagePath : path.join(root, '..', item.imagePath))
    : path.join(final ? theme.assetsDir : path.join(root, 'assets'), item.image || `s${String(index + 1).padStart(2, '0')}.png`);
  const image = pathToFileURL(imageFile).href;
  const proposal = /DEVELOPMENT|FEATURE.GATE|PLANNED|REVIEW|FUTURE|PREPARE/.test(item.status);
  const number = outputNumber(index);
  const bg = final ? `#${theme.background}` : '#F5F7FA';
  const ink = final ? `#${theme.titleColor}` : '#14263D';
  const body = final ? `#${theme.bodyColor}` : '#34495E';
  const font = final ? theme.font : 'Arial';
  const footer = final ? `${number} / ${TOTAL_SLIDES}` : `${number} / ${TOTAL_SLIDES} | KUBECON NA 2026 | DRY RUN`;
  const footerCss = final ? 'left:650pt;width:42pt;text-align:right' : 'left:28pt;width:664pt';
  // Explicit images may have different aspect ratios (notably the square QR).
  // Fit them within the existing figure area without stretching their pixels.
  let imageCss = '';
  if (imageSize) {
    const box = final ? { x: 338, y: 115, w: 354, h: 236 } : { x: 312, y: 128, w: 380, h: 253.333 };
    const qr = /(?:^|[-_/])qr(?:[-_.]|$)/i.test(item.imagePath);
    const scale = Math.min((qr ? Math.min(box.w, 160) : box.w) / imageSize.width, (qr ? Math.min(box.h, 160) : box.h) / imageSize.height);
    const w = imageSize.width * scale, h = imageSize.height * scale;
    imageCss = `.figure{left:${box.x + (box.w - w) / 2}pt;top:${box.y + (box.h - h) / 2}pt;width:${w}pt;height:${h}pt}`;
  }
  if (item.team) return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html{background:${bg}}body{width:720pt;height:405pt;margin:0;display:flex;position:relative;background:${bg};font-family:${font};color:${ink}}
  h1{position:absolute;left:28pt;top:35pt;font-size:28pt;margin:0} .names{position:absolute;left:35pt;top:166pt;display:flex;gap:22pt}
  .name{width:202pt;height:96pt;display:flex;align-items:center;justify-content:center;background:#FFFFFF;border:1pt solid ${final ? '#ADC5EF' : '#CBD5E1'};border-radius:${final ? '0' : '10pt'}}
  .name p{font-size:27pt;font-weight:bold;margin:0} .footer{position:absolute;${footerCss};top:389pt;font-size:8.5pt;margin:0;color:${body}}
  </style></head><body><h1>${esc(item.title)}</h1><div class="names">${item.team.map(name => `<div class="name"><p>${esc(name)}</p></div>`).join('')}</div><p class="footer">${esc(footer)}</p></body></html>`;
  if (item.intro) return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html{background:${bg}}body{width:720pt;height:405pt;margin:0;display:flex;position:relative;background:${bg};font-family:${font};color:${ink}}
  h1{position:absolute;left:28pt;top:35pt;width:664pt;height:84pt;font-size:${final ? theme.titleFontSizePt : 30}pt;line-height:1.12;margin:0}
  img{position:absolute;left:195pt;top:127pt;width:330pt;height:220pt} .caption{position:absolute;left:155pt;top:371pt;width:480pt;font-size:10.5pt;margin:0;color:${body}}
  .footer{position:absolute;${footerCss};top:389pt;font-size:8.5pt;margin:0;color:${body}}
  </style></head><body><h1>${esc(item.title)}</h1><img src="${image}" alt="The operator lifecycle"><p class="caption">${esc(item.caption)}</p><p class="footer">${esc(footer)}</p></body></html>`;
  if (item.divider) return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html{background:${bg}}body{width:720pt;height:405pt;margin:0;display:flex;position:relative;background:${bg};font-family:${font};color:${ink}}
  h1{position:absolute;left:80pt;top:137pt;width:560pt;font-size:34pt;line-height:1.15;text-align:center;margin:0}
  p{position:absolute;${footerCss};top:389pt;font-size:8.5pt;margin:0;color:${body}}
  </style></head><body><h1>${esc(item.title)}</h1><p>${esc(footer)}</p></body></html>`;
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  html{background:#F5F7FA}body{width:720pt;height:405pt;margin:0;padding:0;display:flex;position:relative;background:#F5F7FA;font-family:Arial,sans-serif;color:#14263D}
  p,h1,ul{margin:0} .stripe{position:absolute;left:0;top:0;width:720pt;height:5pt;background:#007F86}
  .eyebrow{position:absolute;left:28pt;top:20pt;font-size:10pt;font-weight:bold;color:#007F86;line-height:1.1}
  h1{position:absolute;left:28pt;top:44pt;width:664pt;height:40pt;font-size:29pt;line-height:1.14;font-weight:bold}
  .badge{position:absolute;left:28pt;top:94pt;padding:5pt 9pt;background:${proposal ? '#FFF0D6' : '#E5EDF1'};border-radius:5pt}
  .badge p{font-size:10pt;line-height:1;color:${proposal ? '#885000' : '#425A68'};font-weight:bold}
  .copy{position:absolute;left:28pt;top:132pt;width:264pt}
  .lead{font-size:19pt;line-height:1.12;font-weight:bold;margin-bottom:11pt}
  ul{padding-left:17pt;font-size:16.5pt;line-height:1.16;color:#34495E}li{margin-bottom:8pt}
  .figure{position:absolute;left:312pt;top:128pt;width:380pt;height:253.333pt}
  .caption{position:absolute;left:28pt;top:351pt;width:267pt;height:31pt;font-size:11.5pt;line-height:1.12;font-style:italic;color:#007F86}
  .footer{position:absolute;left:28pt;top:389pt;width:664pt;font-size:8.5pt;line-height:1;color:#5D6B7B}
  .cover h1{top:42pt;height:82pt;font-size:30pt;line-height:1.11}
  .cover .badge{top:133pt}.cover .copy{top:174pt}.cover .figure{left:352pt;top:140pt;width:337.5pt;height:225pt}
  ${final ? `html,body{background:${bg};font-family:${font};color:${ink}}.stripe,.eyebrow{display:none}h1{left:${theme.titleBoundsPt.x}pt;top:${theme.titleBoundsPt.y}pt;font-size:${theme.titleFontSizePt}pt;color:${ink}}.badge{top:87pt;background:#E3F6FF;border-radius:0}.badge p{color:${ink}}.copy{top:120pt;width:286pt}.lead{font-size:18.5pt;line-height:1.1;color:${body}}ul{font-size:16pt;line-height:1.13;color:${body}}.figure{left:338pt;top:115pt;width:354pt;height:236pt}.caption{left:155pt;top:371pt;width:480pt;height:24pt;font-size:10.5pt;color:${body}}.footer{${footerCss};color:${body}}` : ''}
  ${item.imagePath?.includes('namespace-management') ? '.lead{font-size:16pt;line-height:1.12;margin-bottom:14pt}' : ''}
  ${imageCss}
  </style></head><body class="${index === 0 ? 'cover' : ''}"><div class="stripe"></div><p class="eyebrow">${esc(item.section)}</p><h1>${esc(item.title)}</h1>
  ${item.status ? `<div class="badge"><p>${esc(item.status)}</p></div>` : ''}<div class="copy"><p class="lead">${esc(item.lead).replace(/\n/g, '<br>')}</p><ul>${item.bullets.map(text => `<li>${esc(text)}</li>`).join('')}</ul></div>
  <img class="figure" src="${image}" alt="Conceptual illustration for ${esc(item.title)}">
  ${item.captionUrl ? '' : `<p class="caption">${esc(item.caption)}</p>`}<p class="footer">${esc(footer)}</p></body></html>`;
}

async function buildVariant(variant) {
  checkCopy();
  const final = variant === 'final';
  const outputDir = final ? path.join(root, '..', 'final') : root;
  const theme = final ? JSON.parse(await fs.readFile(path.join(root, 'theme', 'theme.json'), 'utf8')) : null;
  const total = data.reduce((sum, slide) => sum + slide.duration, 0);
  if (data.length !== BASE_SLIDES || total !== BASE_SECONDS) throw new Error('Base count/timing mismatch.');
  if (!data[SDK_INSERT_AFTER - 1].divider) throw new Error('SDK divider must precede the imported segment.');
  const sdkStart = data.slice(0, SDK_INSERT_AFTER).reduce((sum, slide) => sum + slide.duration, 0);
  const htmlDir = path.join(outputDir, 'html');
  const scratch = path.join(outputDir, 'cache', 'html2pptx');
  const preview = path.join(outputDir, 'preview');
  await Promise.all([htmlDir, scratch, preview].map(dir => fs.mkdir(dir, { recursive: true })));
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'KUBECON', width: 10, height: 5.625 });
  pptx.layout = 'KUBECON';
  pptx.author = final ? 'Operator Framework' : 'KubeCon 2026 working draft';
  pptx.subject = final ? 'Kubernetes operator lifecycle management and Java Operator SDK' : 'Illustrated alignment dry run; roles and claim qualifications in notes';
  pptx.title = TITLE;
  pptx.company = 'Operator Framework';
  pptx.lang = 'en-US';
  pptx.theme = { headFontFace: final ? theme.font : 'Arial', bodyFontFace: final ? theme.font : 'Arial', lang: 'en-US' };
  let elapsed = 0;
  const manifest = [];
  const notesEntries = [];
  for (const [index, item] of data.entries()) {
    if (index === SDK_INSERT_AFTER) elapsed += SDK_SECONDS;
    const number = outputNumber(index);
    const imagePath = item.imagePath && (path.isAbsolute(item.imagePath) ? item.imagePath : path.join(root, '..', item.imagePath));
    const imageSize = imagePath ? await sharp(imagePath).metadata() : null;
    const filename = path.join(htmlDir, `slide-${String(index + 1).padStart(2, '0')}.html`);
    await fs.writeFile(filename, slideHtml(item, index, variant, theme, imageSize));
    const { slide } = await html2pptx(filename, pptx, { tmpDir: scratch });
    if (item.captionUrl) {
      // Keep the current Google deck's contribution-guide link clickable.
      const captionBox = final ? { x: 155, y: 371, w: 480, h: 24, fontSize: 10.5 }
        : { x: 28, y: 351, w: 267, h: 31, fontSize: 11.5 };
      slide.addText(item.caption, {
        x: captionBox.x / 72, y: captionBox.y / 72, w: captionBox.w / 72, h: captionBox.h / 72,
        fontFace: final ? theme.font : 'Arial', fontSize: captionBox.fontSize,
        color: final ? theme.bodyColor : '007F86', italic: true, margin: 0,
        hyperlink: { url: item.captionUrl },
      });
    }
    const noteText = `SLIDE ${number}: ${item.title}\nSPEAKER: ${item.speaker}\nSTART: ${clock(elapsed)}\nDURATION: ${clock(item.duration)}\nSTATUS: ${item.status}\n\nTAKEAWAY: ${item.lead}\n\nTALK TRACK / SOURCES / CAVEATS / REVIEW:\n${item.notes}\n\nSOURCE CONTEXT ROOT: ${path.dirname(root)}\n`;
    slide.addNotes(noteText);
    notesEntries.push({ number, text: `## ${number}. ${item.title}\n\n**Speaker:** ${item.speaker}  \n**Start:** ${clock(elapsed)} · **Duration:** ${clock(item.duration)} · **Status:** ${item.status}\n\n${item.lead}\n\n${item.bullets.map(text => `- ${text}`).join('\n')}\n\n${item.notes}\n\n` });
    manifest.push({ number, kind: 'generated', baseIndex: index, speaker: item.speaker, title: item.title, duration: item.duration, start: elapsed });
    elapsed += item.duration;
    console.log(`Built base ${index + 1}/${BASE_SLIDES} (output ${number}): ${item.title}`);
  }
  const stem = final ? 'kubecon-2026-final' : 'kubecon-2026-dry-run';
  const pptxPath = path.join(outputDir, `${stem}.pptx`);
  const basePath = path.join(outputDir, 'olm-base.pptx');
  const reportPath = path.join(outputDir, 'import-report.json');
  await pptx.writeFile({ fileName: basePath });
  console.log(execFileSync('python3', [path.join(root, 'import-sdk.py'), '--base', basePath,
    '--source', '/Users/jordan/Downloads/Copy of KubeCon2026.pptx', '--out', pptxPath, '--insert-after', String(SDK_INSERT_AFTER), '--start-seconds', String(sdkStart), '--report', reportPath], { encoding: 'utf8', timeout: 30000 }));
  if (final) console.log(execFileSync('python3', [path.join(root, 'theme', 'apply-theme.py'), '--pptx', pptxPath, '--profile', path.join(root, 'theme', 'theme.json')], { encoding: 'utf8', timeout: 30000 }));
  const imported = JSON.parse(await fs.readFile(reportPath, 'utf8'));
  if (imported.source_mapping.length !== SDK_SLIDES) throw new Error('SDK slide count mismatch.');
  for (const source of imported.source_mapping) {
    const number = source.output_slide;
    const sdkTitle = source.source_visible_text.find(text => text.trim())?.trim() || `SDK source slide ${source.source_slide}`;
    const sdkDuration = SDK_SECONDS / SDK_SLIDES;
    manifest.push({ number, kind: 'authored-sdk', sourceSlide: source.source_slide, part: source.imported_part, title: sdkTitle, speaker: 'Attila', duration: sdkDuration, start: sdkStart + (number - SDK_INSERT_AFTER - 1) * sdkDuration });
    notesEntries.push({ number, text: `## ${number}. SDK source slide ${source.source_slide}\n\n**Speaker:** Attila\n\n**Start:** ${source.start} · **Duration:** 01:00\n\nOriginal authored slide XML and illustrations retained. SDK wording and release/version claims remain the author's source content. This import adds assignment/timing notes only.\n\nSource: ~/Downloads/Copy of KubeCon2026.pptx, slide ${source.source_slide}.\n\n${source.source_visible_text.join(' ')}\n\n` });
  }
  manifest.sort((a, b) => a.number - b.number);
  notesEntries.sort((a, b) => a.number - b.number);
  if (elapsed !== BASE_SECONDS + SDK_SECONDS || manifest.length !== TOTAL_SLIDES || notesEntries.length !== TOTAL_SLIDES || manifest.some((entry, index) => entry.number !== index + 1)) throw new Error('Combined count/timing mismatch.');
  await fs.writeFile(path.join(outputDir, 'deck-manifest.json'), JSON.stringify(manifest, null, 2));
  await fs.writeFile(path.join(outputDir, 'speaker-notes.md'), `# ${TITLE}\n\n## Speaker notes\n\nOLM presenters: Rashmi, Joe and Jordan; A/B/C topic assignments remain to confirm. Attila presents original SDK source slides 3–12, preserved as authored. ${TOTAL_SLIDES} displayed slides total ${clock(elapsed)} including questions and buffer.\n\n` + notesEntries.map(entry => entry.text).join(''));
  console.log(execFileSync('/Applications/LibreOffice.app/Contents/MacOS/soffice', [
    `-env:UserInstallation=${pathToFileURL(path.join(outputDir, 'lo-profile')).href}`,
    '--headless', '--convert-to', 'pdf', '--outdir', outputDir, pptxPath,
  ], { encoding: 'utf8', timeout: 90000 }));
  const pdfPath = path.join(outputDir, `${stem}.pdf`);
  execFileSync('/opt/homebrew/bin/pdftoppm', ['-scale-to', '1600', '-png', pdfPath, path.join(preview, 'slide')], { timeout: 90000 });
  const images = (await fs.readdir(preview)).filter(name => /^slide-\d+\.png$/.test(name)).sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));
  if (images.length !== TOTAL_SLIDES) throw new Error(`Expected ${TOTAL_SLIDES} rendered slides, got ${images.length}.`);
  for (let sheet = 0; sheet < Math.ceil(images.length / 10); sheet++) {
    const tiles = await Promise.all(images.slice(sheet * 10, sheet * 10 + 10).map(async (name, index) => ({
      input: await sharp(path.join(preview, name)).resize(640, 360).png().toBuffer(),
      left: (index % 2) * 660 + 10, top: Math.floor(index / 2) * 380 + 10,
    })));
    const height = Math.ceil(tiles.length / 2) * 380;
    await sharp({ create: { width: 1320, height, channels: 3, background: '#DDE5EA' } }).composite(tiles).png().toFile(path.join(outputDir, `contact-sheet-${sheet + 1}.png`));
  }
  await fs.writeFile(path.join(outputDir, 'build-report.json'), JSON.stringify({ variant, slides: TOTAL_SLIDES, totalSeconds: elapsed, notes: notesEntries.length, rendering: 'LibreOffice PPTX→PDF; pdftoppm previews', editableText: true, sdkPreservation: imported.verification, pptx: pptxPath, pdf: pdfPath }, null, 2));
  console.log(`${variant}: PPTX, PDF, notes and ${TOTAL_SLIDES} rendered previews ready.`);
}

async function main() {
  const mode = process.argv.includes('--both') ? ['dry-run', 'final'] : process.argv.includes('--final') ? ['final'] : ['dry-run'];
  for (const variant of mode) await buildVariant(variant);
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
