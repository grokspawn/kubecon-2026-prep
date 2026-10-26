#!/usr/bin/env node
'use strict';

// Original, editable concept illustrations. No external services or source-deck edits.
// Run: node make-assets.js (requires the existing local sharp dependency).
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('sharp');
const OUT = path.join(__dirname, 'assets');
const C = { bg: '#F5F7FA', white: '#FFFFFF', ink: '#14263D', teal: '#007F86', amber: '#B66A00', muted: '#5D6B7B', line: '#CBD5E1', tint: '#E4F2F2', warn: '#FFF2DF' };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
let labels = [];
function text(x, y, s, { size = 32, color = C.ink, weight = 600, width = 640 } = {}) {
  labels.push({ x, y, s, size, width });
  return `<text x="${x}" y="${y}" text-anchor="middle" font-family="Arial" font-size="${size}" font-weight="${weight}" fill="${color}">${esc(s)}</text>`;
}
function rect(x, y, w, h, { fill = C.white, stroke = C.line, dash = '', radius = 20 } = {}) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${fill}" stroke="${stroke}" stroke-width="3" ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
}
function line(x1, y1, x2, y2, color = C.teal, dash = '') {
  return `<path d="M${x1},${y1} L${x2},${y2}" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
}
function arrow(x1, y1, x2, y2, { color = C.teal, dash = '' } = {}) {
  return `<path d="M${x1},${y1} L${x2},${y2}" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" marker-end="url(#${color === C.amber ? 'amber' : color === C.muted ? 'muted' : 'teal'})" ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
}
function route(d, { color = C.teal, dash = '', end = true } = {}) {
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" ${end ? `marker-end="url(#${color === C.amber ? 'amber' : 'teal'})"` : ''} ${dash ? `stroke-dasharray="${dash}"` : ''}/>`;
}
function circle(x, y, r, fill = C.white, stroke = C.teal) {
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="4"/>`;
}
function icon(kind, x, y, scale = 1, color = C.teal) {
  const shapes = {
    box: '<path d="M-34,-20 L0,-38 L34,-20 L34,20 L0,38 L-34,20 Z M-34,-20 L0,0 L34,-20 M0,0 V38 M-17,-29 L17,-9"/>',
    doc: '<path d="M-27,-36 H12 L28,-20 V36 H-27 Z M12,-36 V-20 H28 M-14,-5 H14 M-14,9 H14 M-14,23 H5"/>',
    pod: '<path d="M-38,-24 H38 V27 H-38 Z M-25,-10 H-6 V13 H-25 Z M6,-10 H25 V13 H6 Z M-30,36 H30"/>',
    check: '<path d="M-25,0 L-7,19 L28,-22"/>',
    gear: '<circle r="25"/><circle r="9"/><path d="M0,-38 V-26 M0,26 V38 M-38,0 H-26 M26,0 H38 M-27,-27 L-18,-18 M18,18 L27,27 M27,-27 L18,-18 M-18,18 L-27,27"/>',
    up: '<path d="M-27,14 L0,-15 L27,14 M0,-15 V36 M-30,-32 H30"/>',
    gate: '<path d="M-30,35 V-35 H30 V35 M-15,-23 V24 M0,-23 V24 M15,-23 V24"/>',
    warning: '<path d="M0,-36 L39,32 H-39 Z M0,-13 V9"/><circle cx="0" cy="21" r="2"/>',
    lens: '<circle cx="-8" cy="-8" r="26"/><path d="M12,12 L37,37"/>',
    event: '<path d="M-30,-28 H30 V16 H5 L-13,32 V16 H-30 Z M-17,-13 H17 M-17,0 H8"/>',
    metric: '<path d="M-30,-33 V32 H33 M-17,19 V3 M0,19 V-10 M17,19 V-26"/>',
    cache: '<ellipse cy="-25" rx="34" ry="12"/><path d="M-34,-25 V25 C-34,42 34,42 34,25 V-25 M-34,0 C-34,17 34,17 34,0"/>',
    code: '<path d="M-15,-22 L-36,0 L-15,22 M15,-22 L36,0 L15,22 M8,-31 L-8,31"/>',
    person: '<circle cy="-20" r="13"/><path d="M-25,32 V15 C-25,-5 25,-5 25,15 V32"/>',
    test: '<path d="M-12,-35 H12 M-8,-35 V-8 L-29,27 Q-33,35 -21,35 H21 Q33,35 29,27 L8,-8 V-35 M-20,12 H20"/>',
    branch: '<circle cx="-20" cy="-25" r="7"/><circle cx="-20" cy="28" r="7"/><circle cx="25" cy="-17" r="7"/><path d="M-20,-18 V21 M-20,8 Q25,8 25,-10"/>',
    java: '<path d="M-27,0 H21 V23 Q-3,40 -27,23 Z M21,3 H32 Q44,15 21,21 M-33,39 H32 M-11,-10 Q-26,-23 -8,-36 M5,-10 Q-8,-21 11,-35"/>',
    threads: '<path d="M-32,-25 H7 Q28,-25 28,-7 H-9 Q-29,-7 -29,11 H13 Q32,11 32,29 H-32"/>',
    question: '<path d="M-17,-20 Q-13,-39 8,-32 Q32,-22 9,-4 Q0,0 0,13"/><circle cy="28" r="2"/>',
  };
  if (!shapes[kind]) throw new Error(`Unknown icon: ${kind}`);
  return `<g transform="translate(${x} ${y}) scale(${scale})" fill="none" stroke="${color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">${shapes[kind]}</g>`;
}
function card(x, y, w, h, title, kind, options = {}) {
  const cy = y + (h >= 150 ? 55 : h >= 130 ? 42 : 32);
  const scale = h >= 150 ? 0.8 : h >= 130 ? 0.7 : 0.6;
  return rect(x, y, w, h, options) + (kind ? icon(kind, x + w / 2, cy, scale, options.stroke === C.amber ? C.amber : C.teal) : '') + text(x + w / 2, kind ? y + h - 22 : y + h / 2 + 11, title, { width: w - 20, size: 30 });
}
function heading(s) { return text(360, 57, s, { size: 34 }); }
function note(s, y = 429, color = C.muted) { return text(360, y, s, { size: 30, color, weight: 400 }); }
function svg(title, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="720" height="480" viewBox="0 0 720 480" role="img" aria-labelledby="title"><title id="title">${esc(title)}</title><defs>${['teal', 'amber', 'muted'].map(k => `<marker id="${k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3" markerHeight="3" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="${C[k]}"/></marker>`).join('')}</defs><rect width="720" height="480" fill="${C.bg}"/>${body}</svg>`;
}

const slides = [
  ['Package, install, upgrade, operate', () => {
    let b = heading('The operator lifecycle');
    const nodes = [[80,105,'Package','box'],[405,105,'Install','pod'],[405,280,'Upgrade','up'],[80,280,'Operate','gear']];
    b += arrow(280,180,390,180) + arrow(505,240,505,265) + arrow(405,355,295,355) + arrow(180,280,180,255);
    return b + nodes.map(n => card(n[0],n[1],200,145,n[2],n[3])).join('');
  }],
  ['Feature timeline: past, current, work now, planned and future', () => {
    let b = heading('Feature timeline');
    b += line(80,290,640,290,C.muted);
    const stages = [
      [80,'Past','v0','FBC'], [220,'Current','v1 API','Pins'],
      [360,'Work now','Config','Install'], [500,'Planned','Helm','Schemas'],
      [640,'Future','OCI','Catalogs'],
    ];
    for (const [x,stage,first,second] of stages) {
      const planned = x >= 500;
      b += text(x,120,stage,{size:30,width:150});
      b += rect(x-68,145,136,110,{stroke:planned ? C.amber : C.teal,fill:planned ? C.warn : C.white});
      b += text(x,184,first,{size:30,width:132}) + text(x,226,second,{size:30,width:132});
      b += line(x,255,x,278,planned ? C.amber : C.teal) + circle(x,290,10,planned ? C.warn : C.teal,planned ? C.amber : C.teal);
    }
    return b + note('Feature sequence; ordering to refine',402);
  }],
  ['OLMv0 isolation assumptions: shared APIs are a legacy flaw', () => {
    let b = heading('OLMv0 isolation assumptions');
    b += rect(45,95,285,220) + rect(390,95,285,220);
    b += text(188,140,'Namespace A',{size:30,width:265}) + text(533,140,'Namespace B',{size:30,width:265});
    b += icon('doc',125,215,0.8) + icon('doc',245,215,0.8) + icon('doc',470,215,0.8) + icon('doc',590,215,0.8);
    b += text(188,292,'Own CRs',{size:30}) + text(533,292,'Own CRs',{size:30});
    b += line(188,315,188,345) + line(533,315,533,345) + line(188,345,533,345);
    return b + card(170,360,380,64,'Shared cluster CRDs',null,{stroke:C.amber,fill:C.warn}) + line(360,345,360,360) + note('Namespace-isolation assumptions',463,C.amber);
  }],
  ['Compatibility with existing content during lifecycle redesign', () => {
    let b = heading('Compatibility during redesign');
    b += rect(30,300,145,130,{fill:C.tint}) + rect(545,300,145,130,{fill:C.tint});
    b += route('M80,300 Q360,130 640,300',{end:false,color:C.muted}) + line(100,300,620,300,C.ink);
    for (const x of [190,260,460,530]) b += line(x,300,x,213 + Math.abs(x-360)*0.2,C.line);
    b += icon('box',225,235,0.75) + icon('box',470,235,0.75) + arrow(275,235,420,235);
    b += icon('warning',360,340,0.65,C.amber) + line(300,300,415,300,C.amber);
    b += text(360,155,'Existing content',{size:32,width:360});
    return b + text(360,414,'Redesign in progress',{size:30,color:C.amber});
  }],
  ['Direct bundle installation from a registry+v1 OCIImage source', () => {
    let b = heading('Direct bundle installation');
    b += rect(24,140,170,180) + icon('box',109,190,0.75);
    b += text(109,263,'Bundle',{size:30,width:150}) + text(109,301,'OCI image',{size:30,width:150});
    b += rect(225,155,270,150,{stroke:C.teal,fill:C.tint}) + icon('gear',360,203,0.75) + text(360,282,'ClusterExtension',{size:30,width:250});
    b += rect(526,140,170,180) + icon('pod',611,190,0.75);
    b += text(611,263,'Cluster',{size:30,width:150}) + text(611,301,'resources',{size:30,width:150});
    b += arrow(199,230,215,230) + arrow(500,230,516,230);
    return b + note('Direct source: OCIImage',388) + note('Content type: registry+v1',439);
  }],
  ['Ordered rollout: API, RBAC and deployment progress toward configured readiness', () => {
    let b = heading('Phase-by-phase rollout');
    b += card(30,310,135,115,'API','doc') + card(205,235,135,115,'RBAC','gate');
    b += card(380,160,135,115,'Deploy','pod') + card(555,85,135,115,'Ready','check');
    b += route('M165,367 H185 V292 H195') + route('M340,292 H360 V217 H370') + route('M515,217 H535 V142 H545');
    b += text(145,150,'Readiness',{size:30,width:240,color:C.amber}) + text(145,190,'checks',{size:30,width:240,color:C.amber});
    return b + note('Configured readiness checks',464);
  }],
  ['Operator author and user agree through config and schema; validated configuration drives Deployment', () => {
    let b = heading('Configuration contract');
    b += rect(30,100,290,100) + text(175,138,'Operator author',{size:30,width:270}) + text(175,180,'Config contract',{size:30,width:270});
    b += rect(400,100,290,100) + text(545,138,'User',{size:30,width:270}) + text(545,180,'Requirements',{size:30,width:270});
    b += rect(230,245,260,80,{stroke:C.teal,fill:C.tint}) + text(360,278,'Config / schema',{size:30,width:240}) + text(360,313,'Validated',{size:30,width:240});
    b += route('M175,200 V285 H220') + route('M230,265 H205 V210 H175');
    b += route('M545,200 V285 H500') + route('M490,265 H515 V210 H545');
    b += arrow(360,330,360,365) + card(230,375,260,60,'Deployment',null,{stroke:C.teal});
    return b;
  }],
  ['Management migration from v0 to v1 with variable workload restart requirements', () => {
    let b = heading('OLMv0 to OLMv1');
    b += card(85,110,180,125,'v0','gear') + card(455,110,180,125,'v1','gear',{stroke:C.teal});
    b += arrow(275,170,440,170) + line(175,235,175,280,C.muted,'7 7') + line(545,235,545,280,C.muted,'7 7') + line(175,280,545,280,C.muted,'7 7');
    b += rect(175,310,370,91,{stroke:C.teal}) + icon('pod',238,355,0.75) + text(407,368,'Workload',{size:32,width:210});
    b += line(360,280,360,310,C.muted,'7 7');
    return b + note('Restart requirements vary',449);
  }],
  ['Planned shared lifecycle interfaces and test fixtures for CLI, controller and UI', () => {
    let b = heading('Shared lifecycle interfaces');
    b += card(45,100,180,125,'CLI','code') + card(270,100,180,125,'Controller','gear') + card(495,100,180,125,'UI','pod');
    b += route('M135,230 V270 H360 V295',{dash:'8 8'}) + arrow(360,230,360,295,{dash:'8 8'}) + route('M585,230 V270 H360 V295',{dash:'8 8'});
    b += rect(135,310,450,110,{stroke:C.teal,fill:C.tint}) + text(360,351,'Shared contract',{size:32,width:420}) + text(360,396,'Test fixtures',{size:30,width:420});
    return b + note('Dashed = intended reuse',461);
  }],
  ['Rendering chart OCI and values into OLM objects using helm+v2 content', () => {
    let b = heading('Helm content → OLM objects');
    b += card(40,110,190,130,'Chart OCI','box') + card(40,280,190,95,'Values',null);
    b += route('M235,175 H275 V230 H305') + route('M235,328 H275 V230 H305');
    b += card(320,165,150,135,'Render','gear') + arrow(475,232,505,232);
    b += rect(525,135,155,195,{stroke:C.teal}) + icon('doc',578,186,0.7) + icon('doc',625,227,0.7) + text(602,305,'OLM',{size:32,width:130});
    return b + note('Content type: helm+v2');
  }],
  ['FBC to v2 schemas: shared metadata reduces repetition and registry+v1 and helm+v2 provide typed content', () => {
    let b = heading('Catalog schema structure');
    b += rect(205,125,310,85,{stroke:C.teal,fill:C.tint}) + text(360,180,'Shared metadata',{size:32,width:285});
    b += route('M360,215 V235 H195 V260') + route('M360,235 H525 V260');
    b += rect(45,275,300,95) + text(195,315,'registry+v1',{size:30,width:280}) + text(195,353,'Version card',{size:30,width:280});
    b += rect(375,275,300,95) + text(525,315,'helm+v2',{size:30,width:280}) + text(525,353,'Version card',{size:30,width:280});
    b += text(360,100,'Less repeated metadata',{size:30,width:620,color:C.muted});
    b += text(360,408,'Typed content',{size:30,width:620,color:C.muted});
    return b + note('FBC → v2 schemas',458);
  }],
  ['Help develop OLM: improve documentation, add tests and contribute code', () => {
    let b = heading('Help develop OLM');
    b += card(40,125,195,160,'Docs','doc') + card(263,125,195,160,'Tests','test') + card(486,125,195,160,'Code','code');
    b += route('M137,290 V330 H360 V360') + arrow(360,290,360,360) + route('M583,290 V330 H360 V360');
    return b + card(190,375,340,65,'Project development',null,{stroke:C.teal,fill:C.tint});
  }],
  ['Language-neutral OLM packaging and Java Operator SDK reconciliation', () => {
    let b = heading('Packaging and reconciliation');
    b += rect(65,100,590,132,{stroke:C.teal}) + icon('box',128,165,0.85) + text(407,154,'Packaging · OLM',{size:32,width:435}) + text(407,201,'Language-neutral',{size:30,color:C.muted,width:435});
    b += arrow(360,240,360,266);
    b += rect(65,282,590,132,{stroke:C.teal,fill:C.tint}) + icon('java',128,348,0.85) + text(407,333,'Reconciliation · SDK',{size:32,width:435}) + text(407,382,'Java focus',{size:30,color:C.muted,width:435});
    return b;
  }],
  ['Write and cache observation timeline with stale and updated cache states', () => {
    let b = heading('Write and cache observation');
    b += arrow(65,325,660,325,{color:C.muted});
    b += card(45,115,180,145,'Write','doc') + card(270,115,180,145,'Cache','cache',{stroke:C.amber,fill:C.warn}) + card(495,115,180,145,'Observe','lens');
    b += circle(135,325,12,C.teal) + circle(360,325,12,C.warn,C.amber) + circle(585,325,12,C.teal);
    b += line(135,265,135,308) + line(360,265,360,308,C.amber) + line(585,265,585,308);
    b += text(135,375,'New',{size:30,width:160}) + text(360,375,'Stale',{size:30,color:C.amber,width:160}) + text(585,375,'Caught up',{size:30,width:170});
    return b + note('Time →');
  }],
  ['Update event handling based on event source and relevance', () => {
    let b = heading('Update event handling');
    b += card(40,100,220,110,'Own write','doc') + card(40,270,220,110,'Other actor','person');
    b += route('M265,155 H300 V240 H325') + route('M265,325 H300 V240 H325');
    b += `<path d="M425,153 L512,240 L425,327 L338,240 Z" fill="${C.tint}" stroke="${C.teal}" stroke-width="4"/>` + text(425,251,'Eligible?',{size:30,width:160});
    b += arrow(514,240,555,240) + rect(575,190,100,100,{stroke:C.teal}) + icon('check',625,240,0.85);
    return b + note('Check event source and relevance');
  }],
  ['Informer sharing for compatible configurations and separate informers for incompatible configurations', () => {
    let b = heading('Informer sharing');
    b += rect(35,105,390,300) + text(230,145,'Compatible',{size:30,width:360});
    b += card(60,165,150,115,'A','gear') + card(250,165,150,115,'B','gear');
    b += route('M135,285 V306 H230 V321') + route('M325,285 V306 H230 V321');
    b += card(70,338,320,55,'Shared informer',null,{stroke:C.teal,fill:C.tint});
    b += rect(455,105,230,300,{stroke:C.amber}) + text(570,145,'Incompatible',{size:30,color:C.amber,width:210}) + card(495,165,150,115,'C','gear');
    return b + arrow(570,285,570,322,{color:C.amber}) + card(475,338,190,55,'Separate',null,{stroke:C.amber,fill:C.warn});
  }],
  ['Controller telemetry through logs, events and metrics', () => {
    let b = heading('Controller telemetry');
    b += circle(360,170,66,C.tint) + icon('gear',360,170,1.1);
    b += route('M306,216 L145,295') + arrow(360,242,360,295) + route('M414,216 L575,295');
    b += card(45,310,180,120,'Logs','doc') + card(270,310,180,120,'Events','event') + card(495,310,180,120,'Metrics','lens');
    return b;
  }],
  ['Virtual-thread tasks pass through a bounded concurrency gate', () => {
    let b = heading('Virtual thread concurrency');
    b += rect(45,130,180,230) + icon('threads',135,187,0.95) + text(135,270,'Tasks',{size:32,width:160}) + text(135,322,'Queued',{size:30,color:C.muted,width:160});
    b += arrow(235,245,290,245) + rect(310,130,150,230,{stroke:C.amber,fill:C.warn}) + icon('gate',385,207,1) + text(385,320,'Bounded',{size:30,color:C.amber,width:135});
    b += arrow(470,245,515,245) + rect(535,130,140,230,{stroke:C.teal}) + icon('pod',605,207,1) + text(605,320,'Active',{size:30,width:120});
    return b + note('Concurrency gate controls entry');
  }],
  ['Contribution routes: installation validation, issue reproduction and pull requests', () => {
    let b = heading('Contribution routes');
    b += card(40,125,195,230,'Validation','pod') + card(263,125,195,230,'Report','test') + card(486,125,195,230,'Request','branch');
    b += text(137,280,'Content',{size:30,width:175}) + text(360,280,'Issue',{size:30,width:175}) + text(583,280,'Pull',{size:30,width:175});
    return b + note('Usage, issue reports, pull requests');
  }],
  ['Discussion of OLM packaging and Java Operator SDK reconciliation', () => {
    let b = heading('Discussion');
    b += `<path d="M65,115 H295 Q315,115 315,135 V285 Q315,305 295,305 H175 L125,360 V305 H65 Q45,305 45,285 V135 Q45,115 65,115 Z" fill="${C.white}" stroke="${C.teal}" stroke-width="4"/>`;
    b += `<path d="M425,115 H655 Q675,115 675,135 V285 Q675,305 655,305 H595 V360 L545,305 H425 Q405,305 405,285 V135 Q405,115 425,115 Z" fill="${C.white}" stroke="${C.teal}" stroke-width="4"/>`;
    b += icon('question',180,185,1.1) + icon('question',540,185,1.1) + text(180,279,'OLM',{size:34,width:220}) + text(540,279,'SDK',{size:34,width:220});
    return b + note('Packaging      ↔      Reconciliation');
  }],
];

async function main() {
  // Verify the existing project directory before creating any output.
  if (!(await fs.stat(__dirname)).isDirectory()) throw new Error('Project directory missing');
  await fs.mkdir(OUT, { recursive: true });
  const generated = [];
  for (let i = 0; i < slides.length; i++) {
    labels = [];
    const [title, draw] = slides[i];
    const content = svg(title, draw());
    // Measure labels using the same local SVG renderer as the final artwork.
    // No font shrinking: a label that does not fit is a generation error.
    for (const label of labels) {
      const sample = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="100"><rect width="1200" height="100" fill="white"/><text x="20" y="65" font-family="Arial" font-size="${label.size}" font-weight="600" fill="black">${esc(label.s)}</text></svg>`;
      const { info } = await sharp(Buffer.from(sample)).trim().png().toBuffer({ resolveWithObject: true });
      if (info.width > label.width || label.x - info.width / 2 < 16 || label.x + info.width / 2 > 704 || label.y > 465 || label.y - label.size < 10) {
        throw new Error(`s${i+1}: label does not fit: ${label.s} (${info.width}px / ${label.width}px)`);
      }
    }
    const name = `s${String(i + 1).padStart(2, '0')}`;
    await fs.writeFile(path.join(OUT, `${name}.svg`), content);
    await sharp(Buffer.from(content)).resize(1440, 960).png().toFile(path.join(OUT, `${name}.png`));
    const m = await sharp(path.join(OUT, `${name}.png`)).metadata();
    if (m.width !== 1440 || m.height !== 960) throw new Error(`Bad dimensions: ${name}`);
    generated.push({ name, title });
  }
  const tiles = await Promise.all(generated.map(async ({ name }, i) => ({
    input: await sharp(path.join(OUT, `${name}.png`)).resize(360, 240).png().toBuffer(),
    left: (i % 4) * 360, top: Math.floor(i / 4) * 270 + 30,
  })));
  const captions = `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1350">${generated.map(({name},i) => `<text x="${(i%4)*360+180}" y="${Math.floor(i/4)*270+25}" text-anchor="middle" font-family="Arial" font-size="22" fill="${C.ink}">${name}</text>`).join('')}</svg>`;
  await sharp({ create: { width: 1440, height: 1350, channels: 3, background: C.bg } }).composite([...tiles, { input: Buffer.from(captions), left: 0, top: 0 }]).png().toFile(path.join(OUT, 'contact-sheet.png'));
  console.log(`Created ${generated.length} SVG + ${generated.length} PNG illustrations in ${OUT}`);
  console.log('Verified: SVG 720×480; PNG 1440×960; Arial labels ≥30px; rendered label widths fit.');
  console.log('Preview: assets/contact-sheet.png');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
