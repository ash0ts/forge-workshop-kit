// One locked Slidev installation serves every workshop. No exercise is executed.
import {spawnSync} from 'node:child_process';
import {existsSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const [command, slug, ...args] = process.argv.slice(2);
if (!['dev', 'build', 'export'].includes(command) || !slug || !/^[a-z][a-z0-9_-]*$/.test(slug)) {
  console.error('Usage: npm run dev|build|export -- WORKSHOP [Slidev options]');
  process.exit(2);
}
const deck = path.join(root, slug);
if (!existsSync(path.join(deck, 'slides.md'))) {
  console.error(`No generated slides found for ${slug}. Build its storyboard first.`);
  process.exit(2);
}
const cli = path.join(root, 'node_modules/@slidev/cli/bin/slidev.mjs');
if (!existsSync(cli)) {
  console.error('Run npm ci in decks/ to install the shared toolchain.');
  process.exit(2);
}
const result = spawnSync(process.execPath, [cli, ...(command === 'dev' ? [] : [command]), ...args], {cwd:deck, stdio:'inherit'});
if (result.error) {console.error(result.error.message); process.exit(1);}
process.exit(result.status ?? 1);
