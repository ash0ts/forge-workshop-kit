import {chromium} from 'playwright';
import {existsSync} from 'node:fs';
const systemChrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const executablePath=process.env.CHROME_PATH||(existsSync(systemChrome)?systemChrome:undefined);
import fs from 'node:fs/promises';
const base=process.env.DECK_URL||'http://127.0.0.1:3058';
const map=JSON.parse(await fs.readFile('notes/slide-map.json','utf8'));
await fs.mkdir('.screenshots',{recursive:true});
const browser=await chromium.launch({headless:true,executablePath});
const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
const issues=[],consoleErrors=[];
page.on('pageerror',e=>consoleErrors.push(e.message));
for(const slide of map.slides){
 await page.goto(`${base}/${slide.number}`,{waitUntil:'networkidle'});
 await page.evaluate(()=>document.fonts.ready);
 await page.waitForTimeout(100);
 const info=await page.evaluate(()=>{
  const root=document.querySelector('.slidev-page')||document.querySelector('.slidev-layout');
  const boundary=document.querySelector('.slidev-layout').getBoundingClientRect();
  const bad=[];
  for(const e of root.querySelectorAll('h1,h2,p,pre,table,.task,.done,.quote,.source-link,.bottom-note,.exercise-controls,.image-caption')){
   const b=e.getBoundingClientRect();
   if(b.width&&b.height&&(b.bottom>boundary.bottom-30||b.right>boundary.right+1||b.left<boundary.left-1))bad.push({element:e.tagName,text:e.textContent.slice(0,95),box:{x:b.x,y:b.y,width:b.width,height:b.height}})
  }
  const missing=[...root.querySelectorAll('img')].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src);
  return {bad,missing,title:root.querySelector('h1')?.innerText};
 });
 if(info.bad.length||info.missing.length)issues.push({slide:slide.number,...info});
 await page.screenshot({path:`.screenshots/${String(slide.number).padStart(2,'0')}.png`});
}
await fs.writeFile('notes/render-checks.json',JSON.stringify({slides_checked:map.total_slides,issues,console_errors:consoleErrors},null,2));
await page.goto(`${base}/${map.slides.find(s=>s.key==='branch-inspect').number}`);
await page.getByRole('button',{name:'Candidate A',exact:true}).click();
const branchClick=await page.locator('.branch-detail').innerText();
await page.getByRole('button',{name:'Candidate B',exact:true}).focus();await page.keyboard.press('Enter');
const branchKeyboard=await page.locator('.branch-detail').innerText();
await page.goto(`${base}/${map.slides.find(s=>s.key==='run-inspector').number}`);
await page.getByRole('button',{name:'Show active settings',exact:true}).click();
const runInspector=await page.locator('.run-inspector:visible').innerText();
if(!runInspector.includes('learning rate 0.001')||!runInspector.includes('learning rate 0.003'))throw new Error('Run inspector did not reveal actual configurations');
await page.getByRole('button',{name:'Hide settings',exact:true}).focus();await page.keyboard.press('Enter');
const inspectorKeyboard=await page.getByRole('button',{name:'Show active settings',exact:true}).getAttribute('aria-expanded');
if(inspectorKeyboard!=='false')throw new Error('Run inspector keyboard toggle failed');
const exercise=map.slides.find(s=>s.answer);await page.goto(`${base}/${exercise.number}`);
await page.locator('a.answer-link').click();await page.waitForTimeout(200);const answerNavigation=page.url();
await page.locator('.source-link a:visible').click();await page.waitForTimeout(200);const answerReturn=page.url();
await page.goto(`${base}/presenter/${map.slides.find(s=>s.key==='setup-turn').number}`,{waitUntil:'networkidle'});
const presenterNotes=(await page.locator('body').innerText()).includes('Allow 7 minutes.');
if(!presenterNotes)throw new Error('Presenter notes were not visible');
await browser.close();
const result={slides_checked:map.total_slides,issues,console_errors:consoleErrors,branchClick,branchKeyboard,runInspector,inspectorKeyboard,answerNavigation,answerReturn,presenterNotes};
await fs.writeFile('notes/render-checks.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
