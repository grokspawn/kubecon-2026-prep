import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { access } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

const root = '/Users/jordan/devel/mcp-googledocs-server';
const require = createRequire(`${root}/package.json`);
const presentationId = '1_WK8mNw3pERO6U96ptlW3pKiQDvZdBpk12kRN5orIqk';

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

if (process.argv.includes('--server')) {
  const { FastMCP } = await import(`${root}/node_modules/fastmcp/dist/FastMCP.js`);
  const { z } = require('zod');
  const { google } = require('googleapis');
  const { authorize } = await import(`${root}/dist/auth.js`);
  const server = new FastMCP({ name: 'Temporary read-only prior-slide adapter', version: '1.0.0' });
  server.addTool({
    name: 'readPriorPresentation',
    description: 'Read only the authorized 2025 KubeCon presentation, preserving slide order and speaker notes.',
    parameters: z.object({ presentationId: z.literal(presentationId) }),
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: true },
    execute: async () => {
      try {
        // Refuse any new/service-account authorization flow. The module internally
        // uses existing saved credentials; credentials are never emitted.
        if (process.env.SERVICE_ACCOUNT_PATH) return JSON.stringify({ error: 'Existing OAuth path required; authentication unchanged.' });
        await access(`${root}/token.json`);
        await access(`${root}/credentials.json`);
        const auth = await authorize();
        const slidesApi = google.slides({ version: 'v1', auth });
        try {
          const { data } = await slidesApi.presentations.get({ presentationId }, { timeout: 20000 });
          const slides = (data.slides ?? []).map((slide, index) => ({
            number: index + 1,
            objectId: slide.objectId,
            ...extract(slide.pageElements),
            notes: extract(slide.slideProperties?.notesPage?.pageElements).text,
            skipped: slide.slideProperties?.isSkipped ?? false,
          }));
          return JSON.stringify({ retrievalMethod: 'Slides API through temporary MCP tool', presentationId: data.presentationId, title: data.title, slideCount: slides.length, slides });
        } catch (slidesError) {
          const drive = google.drive({ version: 'v3', auth });
          const metadata = await drive.files.get({ fileId: presentationId, fields: 'id,name,mimeType,modifiedTime' }, { timeout: 20000 });
          const exported = await drive.files.export({ fileId: presentationId, mimeType: 'application/vnd.openxmlformats-officedocument.presentationml.presentation' }, { responseType: 'arraybuffer', timeout: 20000 });
          const parsed = spawnSync('python3', [fileURLToPath(new URL('./parse-slide-export.py', import.meta.url))], { input: Buffer.from(exported.data), encoding: 'utf8', maxBuffer: 4 * 1024 * 1024, timeout: 5000 });
          if (parsed.status !== 0) return JSON.stringify({ error: 'Export received; structured extraction failed.' });
          return JSON.stringify({ retrievalMethod: 'Drive PPTX export through temporary MCP tool', presentationId: metadata.data.id, title: metadata.data.name, sourceMimeType: metadata.data.mimeType, modifiedTime: metadata.data.modifiedTime, slidesApiFailure: { code: slidesError.code ?? slidesError.response?.status, reasons: slidesError.response?.data?.error?.errors?.map(item => item.reason) ?? [] }, ...JSON.parse(parsed.stdout) });
        }
      } catch (error) {
        // No raw API error/config objects: these may contain credentials.
        return JSON.stringify({ error: 'Read-only retrieval failed', code: error.code ?? error.response?.status ?? 'unknown' });
      }
    },
  });
  await server.start({ transportType: 'stdio' });
} else {
  const { Client } = await import(require.resolve('@modelcontextprotocol/sdk/client/index.js'));
  const { StdioClientTransport } = await import(require.resolve('@modelcontextprotocol/sdk/client/stdio.js'));
  const transport = new StdioClientTransport({ command: process.execPath, args: [fileURLToPath(import.meta.url), '--server'], stderr: 'pipe' });
  const client = new Client({ name: 'KubeCon prior-deck assessor', version: '1.0.0' });
  try {
    await client.connect(transport);
    const listed = await client.listTools();
    console.log(JSON.stringify({ protocol: 'MCP stdio', tools: listed.tools.map(tool => tool.name) }));
    const result = await client.callTool({ name: 'readPriorPresentation', arguments: { presentationId } }, undefined, { timeout: 30000 });
    for (const item of result.content ?? []) if (item.type === 'text') console.log(JSON.stringify(JSON.parse(item.text), null, 2));
  } catch {
    console.log(JSON.stringify({ error: 'MCP initialization or tool call failed; authentication details withheld.' }));
    process.exitCode = 1;
  } finally {
    await client.close();
  }
}
