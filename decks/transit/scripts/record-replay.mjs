// Navigate saved R4 work. No execution, retry or publication control is used.
import {createRequire} from 'node:module';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const deck=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(path.join(deck,'package.json'));
const {chromium}=require('playwright');
const output=path.join(deck,'.screenshots/replay-raw');
await fs.mkdir(output,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const context=await browser.newContext({viewport:{width:1600,height:1000},recordVideo:{dir:output,size:{width:1600,height:1000}},reducedMotion:'reduce'});
const page=await context.newPage();
const captions=[],actions=[];const started=performance.now();const stamp=()=>Math.round((performance.now()-started)/100)/10;
async function hold(text,seconds=6){console.log(text);const start=stamp();actions.push({at:start,caption:text,url:page.url()});await page.waitForTimeout(seconds*1000);captions.push({start,end:stamp(),text});}
const summary=text=>page.locator('summary').filter({hasText:new RegExp('^'+text.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$')}).first();
try{
 await page.goto(process.env.REPLAY_URL||'http://127.0.0.1:2776',{waitUntil:'networkidle'});
 await page.waitForTimeout(2000);await page.mouse.move(1100,800);await page.mouse.wheel(0,1300);await page.waitForTimeout(900);
 await page.getByRole('heading',{name:'Two builders',exact:true}).scrollIntoViewIfNeeded();
 await hold('Recorded rehearsal R4. These are saved agent executions, restored in the notebook. Opening this view starts no new build.',7);
 await hold('The query and presentation tasks each have one owner. Both patches were integrated into the first-release app.',6);
 const task=summary('Query scheduled departures: files, checks, and decision');await task.click();await task.scrollIntoViewIfNeeded();
 await hold('Open the query task to read the worker’s stated decision and the files it changed.',4);
 const taskDetails=task.locator('..');
 await taskDetails.locator('pre').first().scrollIntoViewIfNeeded();
 await hold('This is the saved query.py diff. The added code converts service-day times and filters scheduled departures.',7);
const conversation=taskDetails.getByRole('link',{name:'Builder conversation',exact:true});
 const conversationUrl=await conversation.getAttribute('href');
 if(!conversationUrl?.includes('b12ffc8bc8427644cef616c34265ad7f'))throw new Error('The displayed query task links to the wrong conversation');
 actions.push({at:stamp(),verified_query_conversation:conversationUrl});await task.click();
 const event=summary('run_tests · builder-1');await event.click();await event.scrollIntoViewIfNeeded();
 const eventDetails=event.locator('..');await eventDetails.locator('summary').filter({hasText:/^Returned result$/}).click();
 const span=eventDetails.locator('a[href*="0aed8384a1436468"]');await span.waitFor();actions.push({at:stamp(),verified_query_test_span:await span.getAttribute('href')});
 await hold('The saved run_tests event includes the returned check and an exact native span link for this worker and build.',7);
 await page.goto(pathToFileURL(path.join(deck,'public/walkthrough/r4-span.html')).href);
 await hold('This is the authenticated Agent Lens capture of that same R4 span. The query component passed; integration is checked separately.',8);
 await page.goto(process.env.REPLAY_URL||'http://127.0.0.1:2776',{waitUntil:'networkidle'});
 await page.getByRole('button',{name:'8 · Compare frozen builds',exact:true}).click();await page.waitForTimeout(6000);await page.mouse.move(1100,800);await page.mouse.wheel(0,1300);await page.waitForTimeout(900);
 await hold('R4 preserved all outcomes. Both first releases passed 10/10. Both follow-up builds scored 14/18 after query workers hit an input bound.',8);
 await page.goto('https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=5lkijosxo9y',{waitUntil:'domcontentloaded'});
 await page.getByText('Aggregated scores',{exact:true}).waitFor();
 const cookieClose=page.getByRole('button',{name:'Close',exact:true});if(await cookieClose.isVisible())await cookieClose.click();
 await page.getByRole('button',{name:'Hide runs sidebar',exact:true}).click();await page.mouse.move(1500,100);await page.waitForTimeout(1000);
 await hold('The actual public EvalTables comparison aligns the same first-release scenarios. The single-worker build is the reference.',7);
 const row=page.getByRole('row').filter({has:page.getByText('departures/other-direction',{exact:true})});
 await row.getByRole('gridcell').nth(4).hover();await page.waitForTimeout(1500);
 const full=page.getByText('Click to view full content',{exact:true});if(await full.isVisible())await full.click();
 await hold('Inspect the returned departures, including service date and civil timestamp. Both builds pass this case; that is a tie in product quality.',8);
 await page.screenshot({path:path.join(deck,'.screenshots/replay-evaltable.png')});
 await page.goto(process.env.REPLAY_APP_URL||'http://127.0.0.1:3094',{waitUntil:'networkidle'});
 await page.getByRole('heading',{name:'The last train is still on yesterday’s timetable'}).waitFor();
 await hold('This is the actual R4 team app, exported from its frozen source. It is not the instructor-authored reference application.',7);
 const date=page.getByRole('textbox',{name:'Historical date and time, including UTC offset',exact:true});await date.fill('2024-11-29T00:10:00-05:00');await date.press('Enter');await page.waitForTimeout(1000);
 await hold('Change the requested time and read the recomputed schedule. The saved app runs locally; this interaction makes no model call.',7);
 await page.screenshot({path:path.join(deck,'.screenshots/replay-actual-app.png')});
}catch(error){actions.push({at:stamp(),error:error.message});throw error;}
finally{
 await fs.writeFile(path.join(output,'local-segment-captions.json'),JSON.stringify(captions,null,2)+'\n');
 await fs.writeFile(path.join(output,'local-segment-actions.json'),JSON.stringify({kind:'Actual browser replay of saved R4 executions',paid_calls:0,actions},null,2)+'\n');
 const video=page.video();await context.close();if(video)await video.saveAs(path.join(output,'local-segment.webm'));await browser.close();
}
console.log(JSON.stringify({seconds:stamp(),captions:captions.length,output}));
