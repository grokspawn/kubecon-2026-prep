// Update text and speaker notes in the current Google Slides deck.
// This script deliberately makes no image, geometry, or formatting changes.
import { createRequire } from 'node:module';
import { writeFile } from 'node:fs/promises';

const workspace = '/Users/jordan/devel/breadcrumbs/2026-kubecon-wip';
const root = '/Users/jordan/devel/mcp-googledocs-server';
const require = createRequire(`${root}/package.json`);
const { google } = require('googleapis');
const { authorize } = await import(`${root}/dist/auth.js`);
const id = '1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8';
const slides = google.slides({ version: 'v1', auth: await authorize() });
const { data: deck } = await slides.presentations.get({ presentationId: id });
if (deck.slides.length !== 27 || !deck.revisionId) throw new Error('Unexpected deck size or missing revision ID');
await writeFile(`${workspace}/current-deck-api-before.json`, JSON.stringify(deck, null, 2));

const expected = ['The Next Era of Kubernetes Operator Lifecycle Management', 'Presentation team', 'Compatibility and lifecycle foundations', 'OLM: past, current and future', 'Streamlined Installation', 'Namespace Management', 'Inspect phased resource rollouts', 'User control of extension deployments', 'OLMv0 → OLMv1 migration', 'Install a bundle directly', 'Planned Helm content support', 'Catalog performance and content types', 'Shared lifecycle logic in library-olm', 'Contribute to Operator Framework', 'Operator Framework: Java Operator SDK'];
const shapeText = e => (e.shape?.text?.textElements ?? []).map(x => x.textRun?.content ?? '').join('');
for (let i = 0; i < expected.length; i++) {
  if (!deck.slides[i].pageElements.some(e => shapeText(e).includes(expected[i]))) throw new Error(`Slide ${i + 1} changed; review before updating`);
}

// Allocations: A 7 minutes including the close; B 7 minutes; C 6 minutes;
// Attila 10 minutes; questions 2 minutes. Names for A/B/C remain unassigned.
const durations = [45,30,90,75,60,60,120,90,120,90,120,90,60,60,30,60,60,60,60,60,60,60,60,60,60,60,120];
if (durations.reduce((a,b) => a+b, 0) !== 1920) throw new Error('Schedule must total 32 minutes');
const speakers = [...Array(6).fill('OLM A — context and installation; name to confirm'), ...Array(4).fill('OLM B — lifecycle primitives and migration; name to confirm'), ...Array(5).fill('OLM C — content, catalogs and contributions; name to confirm'), ...Array(10).fill('Attila — Java Operator SDK'), 'OLM A — session host; name to confirm', 'OLM A/B/C and Attila — questions'];
const fmt = n => `${String(Math.floor(n/60)).padStart(2,'0')}:${String(n%60).padStart(2,'0')}`;
const notesText = slide => {
  const page = slide.slideProperties?.notesPage;
  const oid = page?.notesProperties?.speakerNotesObjectId;
  if (!oid) throw new Error(`Missing speaker-notes object for ${slide.objectId}`);
  const el = (page.pageElements ?? []).find(e => e.objectId === oid);
  return { oid, text: el ? shapeText(el) : '' };
};
const priorTalk = text => {
  const normalized = text.replace(/\u000b/g, '\n');
  const marker = 'TALK TRACK / SOURCES / CAVEATS / REVIEW:';
  const pos = normalized.indexOf(marker);
  return (pos < 0 ? normalized : normalized.slice(pos + marker.length)).trim().replace(/\n\nSOURCE CONTEXT ROOT:.*?(?=\n\n|$)/s, '').trim();
};

const special = {
  2: 'Introduce Rashmi, Joe and Jordan as the OLM presentation team. Introduce Attila as the fourth speaker, covering Java Operator SDK. The mapping from A/B/C to individual OLM presenters remains to be confirmed. Photos are deferred. The session uses prepared examples without live demos.',
  5: 'As of operator-controller v1.11.0, the standard installation channel no longer requires spec.serviceAccount. The controller uses its own service account; the deprecated field is ignored. ClusterExtension write access is a high-privilege operation because the controller uses cluster-admin permissions. When delegating access, combine Kubernetes RBAC with appropriate admission policy, such as ValidatingAdmissionPolicy, to constrain allowed extensions. Source: https://github.com/operator-framework/operator-controller/pull/2770 and the v1.11.0 release notes.',
  6: 'Operator-controller v1.12.0 introduced optional spec.namespace in the experimental installation channel. With the feature-gated runtime, an explicitly supplied namespace remains user-managed. When the field is omitted, OLM derives and manages an install namespace using bundle metadata and defaults. Deleting the extension also deletes its managed namespace and all remaining objects in that namespace, including objects OLM did not install. Explain namespace-transition validation and verify the selected bundle and controller version before demonstrating. Sources: https://github.com/operator-framework/operator-controller/pull/2925, https://github.com/operator-framework/operator-controller/pull/2926, https://github.com/operator-framework/operator-controller/pull/2929.',
  7: 'Explain the ClusterExtension → ClusterObjectDeployment → ClusterObjectSet ownership model. ClusterObjectDeployment manages rollout and revision history; ClusterObjectSets hold immutable revisions with ordered phases. observedPhases and other status details help identify stalled objects. Objects within a phase have no defined ordering. The API and rollout behavior are in active development and controlled by feature-gate. Standalone ClusterObjectDeployment use is in active development. A namespace-scoped ObjectDeployment is under consideration, with no committed availability. Sources: https://github.com/operator-framework/operator-controller/pull/3058 and https://github.com/operator-framework/operator-controller/pull/3072.',
  14: 'Invite contributions to the Operator Framework project: documentation, focused tests, code, and reproducible migration, chart, or schema fixtures. Start with the repository contribution guide: https://github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md. Identify an issue or discussion, provide a reproducible case, and describe the expected result.',
  15: 'C hands off to Attila for the Java Operator SDK section. OLM packaging supports operators written in any language; SDKs support controller implementation. Attila presents the ten authored SDK slides, unchanged, in approximately ten minutes.',
  26: 'Close with the Operator Framework contribution guide, the OLM documentation, and the Java Operator SDK project. Companion demos are intended for online use; no live demo is planned. Confirm resource links before publication.',
  27: 'Reserve two minutes for questions and transition overruns. A/B/C answer OLM questions; Attila answers Java Operator SDK questions. The proposed total duration is 32 minutes.',
};

const requests = [];
const records = [];
let elapsed = 0;
for (let i = 0; i < deck.slides.length; i++) {
  const slide = deck.slides[i], n = i + 1;
  const title = n <= expected.length ? expected[i] : shapeText(slide.pageElements.find(e => shapeText(e).trim()) ?? {}).trim().split('\n')[0];
  const old = notesText(slide);
  let note;
  if (n >= 16 && n <= 25) {
    // Preserve Attila's source attribution; change only schedule metadata.
    note = old.text.trim().replace(/start=\d\d:\d\d/, `start=${fmt(elapsed)}`).replace(/end=\d\d:\d\d/, `end=${fmt(elapsed + durations[i])}`);
  } else {
    let talk = special[n] ?? priorTalk(old.text);
    if (n === 4) talk = talk.replace(/A hands off to B after this overview at 04:00\./, 'A continues with installation changes.');
    if (n === 9) talk = talk.replace('The user confirms structured output that supports automated processing, including models; it has not been independently exercised in this editing task.', 'The example binaries produce structured output for automation and model consumers. The companion migration scenario exercises JSON Lines output.');
    if (n === 10) talk = talk.replace('as of the supplied check dated 2026-10-09', 'as of the 2026-10-28 check');
    if (n === 11) talk += '\n\nTransition: the direct-image source motivates future chart content support. The companion Helm experiment uses an OCI image config; standard Helm OCI config handling remains unverified.';
    if (n === 13) talk = talk.replace('B hands off to C after this slide at 12:00.', 'C connects catalog work with shared lifecycle logic.');
    note = `SLIDE ${n}: ${title}\nSPEAKER: ${speakers[i]}\nSTART: ${fmt(elapsed)}\nDURATION: ${fmt(durations[i])}\n\nTALK TRACK / SOURCES / CAVEATS:\n${talk}`;
  }
  if (!note.trim()) throw new Error(`Empty notes for slide ${n}`);
  if (old.text.trim()) requests.push({deleteText:{objectId:old.oid,textRange:{type:'ALL'}}});
  requests.push({insertText:{objectId:old.oid,insertionIndex:0,text:note}});
  records.push({number:n,title,speaker:speakers[i],start:fmt(elapsed),duration:fmt(durations[i]),notes:note});
  elapsed += durations[i];

  // Replace existing footer text only. New slides and authored SDK pages
  // without footers remain unchanged; no shapes are created.
  const footer = (slide.pageElements ?? []).map(shapeText).map(t => t.trim()).find(t => /^\d+\s*\/\s*25$/.test(t));
  if (footer) requests.push({replaceAllText:{pageObjectIds:[slide.objectId],containsText:{text:footer,matchCase:true},replaceText:`${n} / 27`}});
}
const replace = (n, find, replacement) => {
  const slide = deck.slides[n-1];
  if (!slide.pageElements.some(e => shapeText(e).includes(find))) throw new Error(`Expected text missing on slide ${n}: ${find}`);
  requests.push({replaceAllText:{pageObjectIds:[slide.objectId],containsText:{text:find,matchCase:true},replaceText:replacement}});
};
replace(5, '<upstreamRelease>', 'v1.11.0');
replace(6, '<upstreamRelease>', 'v1.12.0');
replace(7, 'Inspect revision content and ownership changes', 'Inspect ClusterObjectDeployment and revision status');
replace(14, 'Help develop the project through documentation, code and test cases.', 'Contribute to Operator Framework development.');
replace(14, 'Improve documentation and examples', 'Read the repository contribution guide');
replace(14, 'Contribute code and focused tests', 'Discuss an issue and propose a change');
replace(14, 'Add migration, chart and schema fixtures', 'Submit code, documentation or test fixtures');
replace(14, 'Start with a reproducible case and a clear expected result.', 'operator-controller: CONTRIBUTING.md');

await writeFile(`${workspace}/current-deck-run-of-show.json`, JSON.stringify({totalSeconds:elapsed,records},null,2));
await writeFile(`${workspace}/current-deck-speaker-notes.md`, '# Current Google Slides: speaker notes\n\n32 minutes total. A/B/C assignments to named OLM speakers remain open.\n\n' + records.map(r => `## ${r.number}. ${r.title}\n\n${r.notes}\n`).join('\n'));
console.log(`Prepared ${requests.length} text-only requests for ${records.length} slides; total ${fmt(elapsed)}.`);
if (process.argv.includes('--apply')) {
  const result = await slides.presentations.batchUpdate({presentationId:id,requestBody:{requests,writeControl:{requiredRevisionId:deck.revisionId}}});
  console.log(`Applied ${result.data.replies?.length ?? 0} requests atomically.`);
} else console.log('Dry run only.');
