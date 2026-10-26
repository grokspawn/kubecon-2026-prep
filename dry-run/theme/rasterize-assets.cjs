// Local installed Sharp only. SVG pixels retain the original 720x480 geometry.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('../node_modules/sharp');
async function main() {
  const profile = JSON.parse(await fs.readFile(process.argv[2], 'utf8'));
  for (let i = 1; i <= 20; i++) {
    const stem = path.join(profile.assetsDir, `s${String(i).padStart(2, '0')}`);
    const png = await sharp(`${stem}.svg`).png().toBuffer();
    await fs.writeFile(`${stem}.png`, png, { flag: 'wx' });
  }
  console.log('Rasterized 20 themed PNGs with local Sharp.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });
