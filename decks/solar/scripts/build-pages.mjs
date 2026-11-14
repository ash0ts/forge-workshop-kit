// Compatibility entry point. The shared builder owns routes, links, and packages.
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const result = spawnSync(process.env.PYTHON || 'python3', [path.join(root, 'scripts/build_decks.py'), '--only', 'solar'], {cwd:root, stdio:'inherit'});
if (result.error) {console.error(result.error.message); process.exit(1);}
process.exit(result.status ?? 1);
