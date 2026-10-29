// Upload generated visuals to a new private Drive folder for insertion via
// the Google Slides editor. This does not change sharing permissions.
import { createReadStream } from 'node:fs';
import { writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
const root='/Users/jordan/devel/mcp-googledocs-server';
const work='/Users/jordan/devel/breadcrumbs/2026-kubecon-wip/current-visuals';
const require=createRequire(`${root}/package.json`);
const {google}=require('googleapis');
const {authorize}=await import(`${root}/dist/auth.js`);
const drive=google.drive({version:'v3',auth:await authorize()});
const created=[];
try {
  const {data:folder}=await drive.files.create({requestBody:{name:'KubeCon 2026 slide visuals',mimeType:'application/vnd.google-apps.folder'},fields:'id,name,webViewLink'});
  created.push(folder.id);
  const files=[];
  for(const [name,path] of [
    ['KubeCon installation illustration.png','streamlined-installation.png'],
    ['KubeCon namespace illustration.png','namespace-management.png'],
    ['KubeCon contribution guide QR.png','contributing-qr.png'],
  ]) {
    const {data}=await drive.files.create({requestBody:{name,parents:[folder.id]},media:{mimeType:'image/png',body:createReadStream(`${work}/${path}`)},fields:'id,name,webViewLink'});
    created.push(data.id); files.push(data);
    console.log(`Uploaded ${data.name}`);
  }
  await writeFile(`${work}/private-drive-uploads.json`, JSON.stringify({folder,files},null,2));
} catch(e) {
  console.error(`Private upload failed: ${e.message}`);
  for(const fileId of created.reverse()) try { await drive.files.delete({fileId}); } catch { console.error(`Could not delete temporary file ${fileId}`); }
  process.exitCode=1;
}
