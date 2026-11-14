// Validate the delivered static build, including every slide and worked-answer return.
import {createServer} from 'node:http';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
import {existsSync} from 'node:fs';
import fs from 'node:fs/promises';
import path from 'node:path';

const [deckArg, siteArg, prefix] = process.argv.slice(2);
if (!prefix) throw new Error('Usage: node scripts/validate_deck.mjs DECK SITE /deployment/prefix/');
const deck = path.resolve(deckArg), site = path.resolve(siteArg);
const require = createRequire(path.join(deck, 'package.json'));
const {chromium} = require('playwright');
const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const executablePath = process.env.CHROME_PATH || (existsSync(chrome) ? chrome : undefined);
const layout = JSON.parse(await fs.readFile(path.join(deck, 'notes/slide-map.json'), 'utf8'));
const sourceSha256 = createHash('sha256').update(await fs.readFile(path.join(deck, 'slides.md'))).digest('hex');
const output = path.join(deck, '.screenshots');
await fs.mkdir(output, {recursive: true});
const types = {'.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.png':'image/png', '.svg':'image/svg+xml', '.woff2':'font/woff2', '.json':'application/json'};
const server = createServer(async (req, res) => {
  try {
    const pathname = new URL(req.url, 'http://localhost').pathname;
    if (!pathname.startsWith(prefix)) throw new Error('Unknown prefix');
    let file = path.resolve(site, pathname.slice(prefix.length));
    if (file !== site && !file.startsWith(site + path.sep)) throw new Error('Invalid path');
    if ((await fs.stat(file)).isDirectory()) file = path.join(file, 'index.html');
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    res.end(await fs.readFile(file));
  } catch {res.writeHead(404); res.end();}
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}${prefix}`;
const browser = await chromium.launch({headless:true, executablePath});
const issues = [], pageErrors = [], networkErrors = [], answers = [], titles = [], clickStates = [];
try {
  const page = await browser.newPage({viewport:{width:1280,height:720}, reducedMotion:'reduce'});
  // Slidev's display wake lock is optional and unavailable in headless CI.
  // Use its normal preference instead of ignoring permission errors globally.
  await page.addInitScript(() => localStorage.setItem('slidev-wake-lock', 'false'));
  page.on('pageerror', error => pageErrors.push(error.message));
  page.on('response', response => {if(response.status() >= 400) networkErrors.push({status:response.status(), url:response.url()});});
  const {routes} = JSON.parse(await fs.readFile(path.join(site, 'static-routes.json'), 'utf8'));
  for (const route of routes) {
    if ((await fetch(base + route)).status !== 200) issues.push({route, error:'Known route did not return HTTP 200'});
  }
  for (const slide of layout.slides) {
    await page.goto(base + slide.number, {waitUntil:'networkidle'});
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(title => {
      const normalize = text => text.replace(/\s+/g, ' ').trim();
      const template = document.createElement('div'); template.innerHTML = title.replace(/<br\s*\/?\s*>/gi, ' ');
      return [...document.querySelectorAll('.slidev-layout')].some(root => root.getBoundingClientRect().width > 0 && normalize(root.querySelector('h1')?.innerText || '') === normalize(template.textContent));
    }, slide.title);
    let currentClick = 0;
    for (;;) {
    const result = await page.evaluate(title => {
      const normalize = text => text.replace(/\s+/g, ' ').trim();
      const template = document.createElement('div'); template.innerHTML = title.replace(/<br\s*\/?\s*>/gi, ' ');
      const expected = normalize(template.textContent);
      const root = [...document.querySelectorAll('.slidev-layout')].find(element => element.getBoundingClientRect().width > 0 && normalize(element.querySelector('h1')?.innerText || '') === expected);
      const visible = element => {
        for (let node = element; node && node !== root.parentElement; node = node.parentElement) {
          const style = getComputedStyle(node);
          if (style.display === 'none' || style.visibility === 'hidden' || Number(style.opacity) === 0) return false;
        }
        return true;
      };
      const box = root.getBoundingClientRect(), overflow = [];
      for (const element of root.querySelectorAll('h1,h2,p,pre,table,.task,.done,.quote,.source-link,.bottom-note,.exercise-controls,.image-caption')) {
        const rect = element.getBoundingClientRect();
        if (visible(element) && rect.width && rect.height && (rect.bottom > box.bottom - 20 || rect.right > box.right + 1 || rect.left < box.left - 1)) overflow.push({tag:element.tagName, text:element.textContent.slice(0,100), x:rect.x, y:rect.y, width:rect.width, height:rect.height});
      }
      const diagrams = [...root.querySelectorAll('svg[role="img"]')].filter(visible).map(svg => {
        const bounds = svg.getBoundingClientRect();
        const labels = [...svg.querySelectorAll('text')].filter(text => visible(text) && text.getBoundingClientRect().width);
        const clippedLabels = labels.filter(text => {
          const label = text.getBoundingClientRect();
          return label.width && label.height && (label.left < bounds.left - 2 || label.right > bounds.right + 2 || label.top < bounds.top - 2 || label.bottom > bounds.bottom + 2);
        }).map(text => text.textContent);
        const overlappingLabels = [];
        for (let i = 0; i < labels.length; i++) {
          const a = labels[i].getBoundingClientRect();
          for (let j = i + 1; j < labels.length; j++) {
            const b = labels[j].getBoundingClientRect();
            if (Math.min(a.right,b.right) - Math.max(a.left,b.left) > 2 && Math.min(a.bottom,b.bottom) - Math.max(a.top,b.top) > 2) {
              overlappingLabels.push([labels[i].textContent,labels[j].textContent]);
            }
          }
        }
        const description = svg.getAttribute('aria-label') || svg.querySelector('title,desc')?.textContent || '';
        return {description, clippedLabels, overlappingLabels};
      });
      const textProblems = [], textOverflow = [], walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const node = walker.currentNode, parent = node.parentElement;
        if (!parent || !visible(parent) || parent.closest('script,style,pre,code')) continue;
        const range = document.createRange(); range.selectNodeContents(node);
        const lines = [...range.getClientRects()].filter(rect => rect.width && rect.height);
        if (!lines.length) continue;
        const text = node.textContent.trim();
        // Element bounds can fit while an unwrapped text line extends beyond them.
        // SVG label bounds are checked above; code has its own scroll checks.
        if (text && !parent.closest('svg')) {
          for (const rect of lines) {
            if (rect.left < box.left - 2 || rect.right > box.right + 2 || rect.top < box.top - 2 || rect.bottom > box.bottom - 12) {
              textOverflow.push({text:text.slice(0,160),x:rect.x,y:rect.y,width:rect.width,height:rect.height});
              break;
            }
            // Also detect text cropped by a nearer overflow container.
            for (let ancestor = parent; ancestor && ancestor !== root; ancestor = ancestor.parentElement) {
              const style = getComputedStyle(ancestor), clip = ancestor.getBoundingClientRect();
              const horizontal = /hidden|clip|auto|scroll/.test(style.overflowX);
              const vertical = /hidden|clip|auto|scroll/.test(style.overflowY);
              if ((horizontal && (rect.left < clip.left - 2 || rect.right > clip.right + 2)) ||
                  (vertical && (rect.top < clip.top - 2 || rect.bottom > clip.bottom + 2))) {
                textOverflow.push({text:text.slice(0,160),container:ancestor.className,error:'Text clipped by its container'});
                break;
              }
            }
          }
        }
        if (/\uFFFD|\uFFFC|`|\*\*[^*]+\*\*|\[[^\]\n]+\]\(https?:|\{\{[^}]+\}\}/.test(text)) {
          textProblems.push(text.slice(0,200));
        }
      }
      const clippedCode = [...root.querySelectorAll('pre')].filter(visible).filter(element => element.scrollWidth > element.clientWidth + 2 || element.scrollHeight > element.clientHeight + 2).map(element => element.textContent.slice(0,200));
      return {title:expected, overflow, diagrams, textProblems, textOverflow, clippedCode, missingImages:[...root.querySelectorAll('img')].filter(image => !image.complete || !image.naturalWidth).map(image => image.src)};
    }, slide.title);
    if (currentClick === 0) titles.push({number:slide.number, key:slide.key, title:result.title});
    clickStates.push({slide:slide.number, click:currentClick});
    if (result.overflow.length || result.missingImages.length || result.textProblems.length || result.textOverflow.length || result.clippedCode.length || result.diagrams.some(diagram => !diagram.description || diagram.clippedLabels.length || diagram.overlappingLabels.length)) issues.push({slide:slide.number, click:currentClick, ...result});
    const suffix = currentClick ? `-click-${currentClick}` : '';
    await page.screenshot({path:path.join(output, `${String(slide.number).padStart(3,'0')}${suffix}.png`)});
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(180);
    const next = new URL(page.url());
    if (next.pathname.replace(/\/$/,'') !== prefix + slide.number) break;
    const nextClick = Number(next.searchParams.get('clicks') || 0);
    if (slide.number === layout.total_slides && nextClick === currentClick) break;
    if (nextClick !== currentClick + 1 || nextClick > 30) {
      issues.push({slide:slide.number,error:'Click navigation did not advance predictably',currentClick,nextClick}); break;
    }
    await page.keyboard.press('ArrowLeft');
    await page.waitForTimeout(120);
    if (Number(new URL(page.url()).searchParams.get('clicks') || 0) !== currentClick) issues.push({slide:slide.number,error:'Back did not restore the previous reveal'});
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(120);
    currentClick = nextClick;
    }
    await page.goto(base + slide.number, {waitUntil:'networkidle'});
    if (slide.answer) {
      const answer = page.locator('a.answer-link:visible');
      if (await answer.count() !== 1) {issues.push({slide:slide.number,error:'Expected one worked-answer link'}); continue;}
      const destination = await answer.getAttribute('href');
      await answer.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(150);
      await page.reload({waitUntil:'networkidle'});
      const back = page.locator('.source-link a:visible').filter({hasText:/return|back/i}).first();
      if (!await back.count()) {issues.push({slide:slide.number,error:'Missing worked-answer return'}); continue;}
      await back.focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(150);
      const returned = new URL(page.url()).pathname === prefix + slide.number;
      answers.push({slide:slide.number, destination, keyboardReturn:returned});
      if (!returned) issues.push({slide:slide.number,error:'Answer did not return to exercise',url:page.url()});
    }
  }
  await page.goto(base + 'presenter/1', {waitUntil:'networkidle'});
  const presenter = (await page.locator('body').innerText()).includes(layout.slides[0].notes.slice(0,40));
  if (!presenter) issues.push({error:'Presenter notes missing'});
  const currentSourceSha256 = createHash('sha256').update(await fs.readFile(path.join(deck,'slides.md'))).digest('hex');
  if (currentSourceSha256 !== sourceSha256) issues.push({error:'Slide source changed during validation; rebuild before publishing'});
  const result = {source_sha256:sourceSha256, slides_checked:titles.length, expected_slides:layout.total_slides, titles, click_states:clickStates, issues, console_errors:pageErrors, failed_responses:networkErrors, answers, routes_checked:routes.length, presenter_notes:presenter};
  await fs.writeFile(path.join(deck, 'notes/delivery-checks.json'), JSON.stringify(result,null,2) + '\n');
  console.log(JSON.stringify({slides_checked:titles.length, click_states_checked:clickStates.length, issues, console_errors:pageErrors, failed_responses:networkErrors, answers:answers.length},null,2));
  if (issues.length || pageErrors.length || networkErrors.length) process.exitCode = 1;
} finally {await browser.close(); server.close();}
