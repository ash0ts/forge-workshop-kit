import fs from 'node:fs/promises';
await fs.copyFile('scripts/serve-browser.py','dist/serve.py');
await fs.writeFile('dist/README.txt',`Solar Forecasting Lab — Autoresearch\n\nRun python3 serve.py (Windows: py serve.py).\nOpen the local address printed by the server.\nPresenter notes: /presenter/1\nArrow keys move through incremental diagrams.\nWorked-answer links return to the exercise.\n\nThis deck makes no inference or training calls. Product links need the reader's own Forge access.\n`);
