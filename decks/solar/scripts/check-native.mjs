import {chromium} from 'playwright';
import fs from 'node:fs/promises';
const base=process.env.DECK_URL||'http://127.0.0.1:3058';
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const page=await browser.newPage({viewport:{width:1280,height:720}});
const map=JSON.parse(await fs.readFile('notes/slide-map.json','utf8'));
const results=[],errors=[];page.on('pageerror',e=>errors.push(e.message));
for(const s of map.slides.filter(s=>['native-lens','result-meaning','reproduce','close','links'].includes(s.key)||s.key.startsWith('pending-'))){
 await page.goto(`${base}/${s.number}`,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
 await page.waitForFunction(title=>{
  const normalize=s=>s.replace(/\s+/g,' ').trim();const template=document.createElement('div');template.innerHTML=title.replace(/<br\s*\/?\s*>/gi,' ');const expected=normalize(template.textContent);
  return [...document.querySelectorAll('.slidev-layout')].some(e=>e.getBoundingClientRect().width>0&&normalize(e.querySelector('h1')?.innerText||'')===expected);
 },s.title);
 await page.waitForTimeout(150);
 const result=await page.evaluate(title=>{
  const normalize=s=>s.replace(/\s+/g,' ').trim();const template=document.createElement('div');template.innerHTML=title.replace(/<br\s*\/?\s*>/gi,' ');const expected=normalize(template.textContent);
  const root=[...document.querySelectorAll('.slidev-layout')].find(e=>e.getBoundingClientRect().width>0&&normalize(e.querySelector('h1')?.innerText||'')===expected),b=root.getBoundingClientRect();
  const clipped=[...root.querySelectorAll('h1,p,.product-caption,.image-caption,.appendix-return')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&(r.right>b.right||r.bottom>b.bottom-10||r.left<b.left)}).map(e=>e.textContent);
  return {title:normalize(root.querySelector('h1').innerText),expected,title_matches:normalize(root.querySelector('h1').innerText)===expected,clipped,missing:[...root.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),links:[...root.querySelectorAll('a')].map(a=>({text:a.textContent||a.getAttribute('aria-label'),href:a.href}))};
 },s.title);
 await page.screenshot({path:`.screenshots/native-v023-${s.number}.png`});results.push({slide:s.number,key:s.key,...result});
 if(s.key.startsWith('pending-')){await page.locator('.appendix-return a:visible').click();await page.waitForTimeout(100);if(!page.url().endsWith('/6'))throw Error('Appendix return failed: '+page.url());}
}
await browser.close();const output={slides:results,errors};await fs.writeFile('notes/native-v023-render-checks.json',JSON.stringify(output,null,2));console.log(JSON.stringify(output,null,2));if(errors.length||results.some(r=>r.clipped.length||r.missing.length))process.exitCode=1;
