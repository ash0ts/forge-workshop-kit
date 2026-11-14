# Workshop decks

All five decks use one pinned Slidev installation in this directory. Their storyboards, diagrams, and screenshots remain separate.

```sh
cd decks
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
npm run dev -- routing
```

Per-workshop `npm run dev`, `npm run build`, and `npm run export` commands also resolve the parent installation. Do not install dependencies inside each workshop directory.

For the complete browser deck, PDF, source package, and validation:

```sh
python3 scripts/build_decks.py --only routing --install --pdf --validate
```

Run that command from the repository root. The shared build generates both GitHub Pages routes and an offline browser package. Downloaded source bundles include this toolchain and can build without the rest of the repository.

Opening or building a deck sends no model requests and runs no workshop exercises.
