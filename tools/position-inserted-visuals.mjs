// Arrange images inserted through the Slides editor from private Drive files.
import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
const root='/Users/jordan/devel/mcp-googledocs-server';
const work='/Users/jordan/devel/breadcrumbs/2026-kubecon-wip';
const presentationId='1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8';
const req=createRequire(`${root}/package.json`);
const {google}=req('googleapis');const {authorize}=await import(`${root}/dist/auth.js`);
const slides=google.slides({version:'v1',auth:await authorize()});
const before=JSON.parse(await readFile(`${work}/current-visuals-before.json`,'utf8'));
const {data:deck}=await slides.presentations.get({presentationId});
if(deck.slides.length!==27 || !deck.revisionId) throw Error('Unexpected deck state');
const getText=e=>(e?.shape?.text?.textElements??[]).map(t=>t.textRun?.content??'').join('');
const body5='h2e53265e7e1a2617_1_2',body6='h17c27b4e15e0645b_0_2',oldImage='h17c27b4e15e0645b_3_198',caption='h17c27b4e15e0645b_3_199',notesId='h17c27b4e15e0645b_3_191';
const added=[];
for(const n of [5,6,14]) {
  const existing=new Set(before.slides[n-1].pageElements.map(e=>e.objectId));
  const next=deck.slides[n-1];
  if(next.objectId!==before.slides[n-1].objectId)throw Error(`Slide ${n} moved or changed`);
  const images=next.pageElements.filter(e=>e.image && !existing.has(e.objectId));
  if(images.length!==1)throw Error(`Expected one newly inserted image on slide ${n}, got ${images.length}`);
  added.push(images[0]);
}
const notesPage=deck.slides[13].slideProperties.notesPage;
const notes=getText(notesPage.pageElements.find(e=>e.objectId===notesId));
const deferred=' A QR code remains deferred until the visual update.';
const noteStart=notes.indexOf(deferred);
if(noteStart<0)throw Error('Contribution speaker note changed');
if(!deck.slides[13].pageElements.some(e=>e.objectId===oldImage && e.image))throw Error('Old contribution image changed');

const requests=[];
function body(objectId, value) {
  requests.push({deleteText:{objectId,textRange:{type:'ALL'}}},{insertText:{objectId,insertionIndex:0,text:value}});
  requests.push({updateTextStyle:{objectId,textRange:{type:'ALL'},style:{fontFamily:'Arial',fontSize:{magnitude:17,unit:'PT'}},fields:'fontFamily,fontSize'}});
  requests.push({updatePageElementTransform:{objectId,applyMode:'ABSOLUTE',transform:{scaleX:1.27,scaleY:1.1058,translateX:24.54,translateY:90.75,unit:'PT'}}});
}
function place(element,x,y,w,h,title,description) {
  if(element.size.width.unit!=='EMU' || element.size.height.unit!=='EMU') throw Error('Unexpected image size unit');
  requests.push({updatePageElementTransform:{objectId:element.objectId,applyMode:'ABSOLUTE',transform:{scaleX:w*12700/element.size.width.magnitude,scaleY:h*12700/element.size.height.magnitude,translateX:x,translateY:y,unit:'PT'}}});
  requests.push({updatePageElementAltText:{objectId:element.objectId,title,description}});
}
body(body5,'Standard channel since v1.11.0\n\n• spec.serviceAccount is optional and ignored.\n\n• The controller uses its own service account.\n\n• Restrict ClusterExtension access with RBAC and admission policy.');
body(body6,'Experimental channel since v1.12.0\nControlled by feature gate\n\n• Set spec.namespace: use an existing user-managed namespace.\n\n• Omit it: OLM manages a derived namespace.\n\n• Deletion removes that namespace and its contents.');
place(added[0],344,120,345,230,'ClusterExtension installation','A ClusterExtension is reconciled by the controller using its service account, with access governed by RBAC and admission policy.');
place(added[1],344,120,345,230,'Install namespace choices','An explicitly set namespace remains user-managed. When omitted, OLM derives and manages it; deletion removes the managed namespace and its contents.');
requests.push({deleteObject:{objectId:oldImage}});
place(added[2],451,128,175,175,'Operator controller contributing guide QR code','Scan to open github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md.');
requests.push({updateTextStyle:{objectId:caption,textRange:{type:'ALL'},style:{link:{url:'https://github.com/operator-framework/operator-controller/blob/main/CONTRIBUTING.md'}},fields:'link'}});
requests.push({deleteText:{objectId:notesId,textRange:{type:'FIXED_RANGE',startIndex:noteStart,endIndex:noteStart+deferred.length}}});
await writeFile(`${work}/current-visuals/slide-api-before-positioning.json`,JSON.stringify(deck,null,2));
try {
  const {data}=await slides.presentations.batchUpdate({presentationId,requestBody:{requests,writeControl:{requiredRevisionId:deck.revisionId}}});
  console.log(`Positioned three visuals; applied ${data.replies?.length??0} requests.`);
} catch(e) { console.error(`Positioning failed: ${e.response?.data?.error?.message??e.message}`);process.exitCode=1; }
