// Reuse the visual skill's locked QR dependency; no provider or network calls.
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import fs from 'node:fs/promises';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(path.join(root, 'skills/teenage-engineering-visualizations/package.json'));
const QRCode = require('qrcode');
if (require('qrcode/package.json').version !== '1.5.4') {
  throw new Error('Install the visual skill dependencies from its lockfile: qrcode 1.5.4 is required');
}
const escape = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('"', '&quot;');
let input = '';
for await (const chunk of process.stdin) input += chunk;
for (const item of JSON.parse(input)) {
  if (new URL(item.url).protocol !== 'https:') throw new Error('QR destinations must use HTTPS');
  const options = {errorCorrectionLevel: 'M', margin: 4, color: {dark: '#242522', light: '#ffffff'}};
  const svg = (await QRCode.toString(item.url, {...options, type: 'svg'})).replace(
    /(<svg[^>]*>)/,
    `$1<title>${escape(item.title)}</title><desc>Scan or follow ${escape(item.url)}</desc>`,
  );
  await fs.mkdir(path.dirname(item.svg), {recursive: true});
  await fs.writeFile(item.svg, svg);
  if (item.png) {
    await fs.mkdir(path.dirname(item.png), {recursive: true});
    await QRCode.toFile(item.png, item.url, {...options, type: 'png', width: 1024});
  }
}
