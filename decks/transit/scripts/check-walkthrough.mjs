import {createRequire} from 'node:module';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const deck=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const {chromium}=createRequire(path.join(deck,'package.json'))('playwright');
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try {
 const page=await browser.newPage({viewport:{width:1280,height:900}});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 await page.goto(pathToFileURL(path.join(deck,'public/walkthrough/index.html')).href);
 const results=[];
 for(const id of ['walkthrough','recorded-video']) {
  const video=page.locator('#'+id);
  await video.evaluate(video=>new Promise(resolve=>{if(video.readyState>=1)resolve();else video.addEventListener('loadedmetadata',resolve,{once:true});}));
  const selector=id==='walkthrough'?'button[data-time]:not([data-video])':`button[data-video="${id}"]`;
  const chapters=page.locator(selector);const count=await chapters.count();
  for(let i=0;i<count;i++) {
   const button=chapters.nth(i);const target=Number(await button.getAttribute('data-time'));
   await button.click();await page.waitForTimeout(100);
   const actual=await video.evaluate(video=>video.currentTime);
   if(Math.abs(actual-target)>0.2)throw new Error('Chapter seek failed: '+id+' '+target+' -> '+actual);
  }
  results.push({id,chapters:count,...await video.evaluate(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight}))});
 }
 await page.setViewportSize({width:390,height:844});
 if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1))throw new Error('Player overflows narrow screen');
 await page.screenshot({path:path.join(deck,'.screenshots/walkthrough-player-narrow.png'),fullPage:true});
 if(errors.length)throw new Error(errors.join('\n'));
 const receipt={videos:results,page_errors:errors,narrow_width:390,caption_mode:'Burned below the unaltered recorded viewport',paid_calls:0};
 await fs.writeFile(path.join(deck,'notes/walkthrough-checks.json'),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt));
} finally {await browser.close();}
