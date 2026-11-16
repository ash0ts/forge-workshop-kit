// Local rendering only. No network request, inference or publication is allowed.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const directory = path.resolve(process.argv[2]);
const formats = new Set((process.argv[3] || '').split(','));
const manifestPath = path.join(directory, 'index.json');
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
const browser = await chromium.launch({headless:true});
const page = await browser.newPage({viewport:{width:manifest.width,height:manifest.height},deviceScaleFactor:1});
await page.route('**/*', route => {
  const protocol = new URL(route.request().url()).protocol;
  return ['file:','data:','about:'].includes(protocol) ? route.continue() : route.abort();
});
const receipts = [];
try {
  await page.goto(pathToFileURL(path.join(directory,manifest.html)).href);
  for (const [index,state] of manifest.states.entries()) {
    await page.selectOption('#state',String(index));
    await page.evaluate(() => document.fonts.ready);
    const bounds = await page.evaluate(() => {
      const failures = [];
      for (const node of document.querySelectorAll('.frame[aria-hidden="false"] text[data-box]')) {
        if (node.closest('[aria-hidden="true"]')) continue;
        const [x,y,w,h] = node.getAttribute('data-box').split(' ').map(Number);
        const b = node.getBBox();
        if (b.x < x-1 || b.y < y-3 || b.x+b.width > x+w+1 || b.y+b.height > y+h+3)
          failures.push({text:node.textContent,expected:[x,y,w,h],actual:[b.x,b.y,b.width,b.height]});
      }
      // Authored drawings are inlined, so check every actual text line, including
      // labels without an assigned box. CSS containers alone miss clipped prose.
      const svg = document.querySelector('.frame[aria-hidden="false"] > svg');
      const canvas = svg.getBoundingClientRect();
      for (const node of svg.querySelectorAll('text')) {
        if (node.closest('[aria-hidden="true"]')) continue;
        const b = node.getBoundingClientRect();
        if (b.width && b.height && (b.left < canvas.left - 1 || b.top < canvas.top - 1 || b.right > canvas.right + 1 || b.bottom > canvas.bottom + 1))
          failures.push({text:node.textContent,kind:'canvas',expected:[canvas.x,canvas.y,canvas.width,canvas.height],actual:[b.x,b.y,b.width,b.height]});
      }
      return {failures, textCount:document.querySelectorAll('.frame[aria-hidden="false"] text').length, fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))};
    });
    receipts.push({state:state.id,...bounds});
    if (formats.has('png')) {
      state.png = state.svg.replace(/\.svg$/, '.png');
      await page.screenshot({path:path.join(directory,state.png),clip:{x:0,y:0,width:manifest.width,height:manifest.height},animations:'disabled'});
    }
  }
  if (formats.has('pdf')) {
    await page.goto(pathToFileURL(path.join(directory,manifest.html)).href);
    await page.evaluate(() => document.fonts.ready);
    await page.emulateMedia({media:'print'});
    await page.addStyleTag({content:`@page{size:${manifest.layout==='print'?'420mm 594mm':`${manifest.width}px ${manifest.height}px`};margin:0}html,body,main{margin:0!important;padding:0!important;width:100%!important}.frame{margin:0!important;line-height:0}.frame svg{width:100%;height:auto;display:block}`});
    manifest.pdf = 'print.pdf';
    await page.pdf({path:path.join(directory,manifest.pdf),printBackground:true,preferCSSPageSize:true});
  }
  manifest.png = manifest.states.flatMap(s=>s.png?[s.png]:[]);
  await fs.writeFile(manifestPath,JSON.stringify(manifest,null,2)+'\n');
  await fs.writeFile(path.join(directory,'browser-validation.json'),JSON.stringify({renderer:'playwright-1.64.1',network:'blocked',states:receipts,passed:receipts.every(r=>r.failures.length===0)},null,2)+'\n');
  const failures = receipts.flatMap(r=>r.failures.map(f=>({state:r.state,...f})));
  if (failures.length) {
    console.error(JSON.stringify(failures.slice(0,12),null,2));
    throw new Error(`${failures.length} text lines exceed their assigned bounds. See browser-validation.json`);
  }
} finally { await browser.close(); }
