// One-shot read-only Drive export of the imported KubeCon 2026 deck as
// PPTX, using the google-docs MCP server's saved OAuth credentials.
// Export is a read-only operation on the Drive file.
import { createRequire } from 'node:module';
import { writeFile } from 'node:fs/promises';

const root = '/Users/jordan/devel/mcp-googledocs-server';
const require = createRequire(`${root}/package.json`);
const fileId = '1yLWsXrp2GWjLyS_ztnbnmR40OGwm29QHI4qpxGHf7A8';

const { google } = require('googleapis');
const { authorize } = await import(`${root}/dist/auth.js`);
const auth = await authorize();
const drive = google.drive({ version: 'v3', auth });
const { data } = await drive.files.export(
  { fileId, mimeType: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' },
  { responseType: 'arraybuffer', timeout: 60000 },
);
await writeFile('/tmp/imported-deck.pptx', Buffer.from(data));
console.log('exported', Buffer.from(data).length, 'bytes to /tmp/imported-deck.pptx');
