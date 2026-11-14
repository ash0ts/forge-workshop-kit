// Record actual local notebook edits and free checks. No connection or worker-run button is clicked.
import {createRequire} from 'node:module';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const deck=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const kit=path.resolve(deck,'../..');
const require=createRequire(path.join(deck,'package.json'));
const {chromium}=require('playwright');
const output=path.join(deck,'.screenshots/walkthrough-raw');
await fs.mkdir(output,{recursive:true});
const python=process.env.WORKSHOP_PYTHON || path.join(kit,'.venv/bin/python');
const reply=spawnSync(python,['-c','import json; from forge_workshop_kit import factory_teaching as t; print(json.dumps({"acceptance":t.ACCEPTANCE_SOLUTION, **{k:v["solution"] for k,v in t.EXERCISES.items()}}))'],{cwd:kit,encoding:'utf8'});
if(reply.status)throw new Error(reply.stderr);
const answers=JSON.parse(reply.stdout);
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const context=await browser.newContext({viewport:{width:1600,height:1000},recordVideo:{dir:output,size:{width:1600,height:1000}},reducedMotion:'reduce'});
const page=await context.newPage();
const captions=[],actions=[];
const started=performance.now();
const stamp=()=>Math.round((performance.now()-started)/100)/10;
async function hold(text,seconds=5){console.log(text);const start=stamp();actions.push({at:start,caption:text,url:page.url()});await page.waitForTimeout(seconds*1000);captions.push({start,end:stamp(),text});}
async function visibleEditor(){const editors=page.locator('.cm-content[contenteditable="true"]');for(let i=0;i<await editors.count();i++){const e=editors.nth(i);if(await e.isVisible())return e;}throw new Error('No visible learner code editor');}
async function replaceCode(source){const e=await visibleEditor();await e.scrollIntoViewIfNeeded();await e.click();await page.keyboard.press(process.platform==='darwin'?'Meta+A':'Control+A');await page.keyboard.insertText(source);await page.waitForTimeout(700);}
async function step(label){await page.getByRole('button',{name:label,exact:true}).click();await page.waitForTimeout(600);}
try{
 await page.goto(process.env.NOTEBOOK_URL||'http://127.0.0.1:3092',{waitUntil:'networkidle'});
 await page.getByRole('heading',{name:'Build a transit app with a team of coding agents'}).waitFor();
 await hold('Worked example: edit the coordination code and run free checks in the actual notebook. No agents run in this segment.',6);
 await page.getByRole('heading',{name:'Read one departure before writing code'}).scrollIntoViewIfNeeded();
 await hold('The input is a real archived MBTA schedule. A 24:08 departure belongs to the previous service day.',6);
 await page.getByRole('heading',{name:'Write one acceptance scenario'}).scrollIntoViewIfNeeded();
 await (await visibleEditor()).scrollIntoViewIfNeeded();
 await hold('Start by checking the behavior the app must preserve. The starter function is deliberately incomplete.',5);
 await page.getByRole('button',{name:'Check my after-midnight scenario',exact:true}).click();
 await page.waitForTimeout(800);
 await hold('The free check reports the missing implementation. It does not make a model request.',4);
 await replaceCode(answers.acceptance);
 await hold('Require the actual trip, service date and civil departure time together. This is the worked answer.',7);
 await page.getByRole('button',{name:'Check my after-midnight scenario',exact:true}).click();
 await page.getByText('Scenario passed.',{exact:false}).waitFor();
 await page.getByText('Scenario passed.',{exact:false}).scrollIntoViewIfNeeded();
 await hold('The real row passes. A missing departure and the wrong service day fail. These are useful negative controls.',6);
 await step('2 · Run one builder');
 await replaceCode(answers.worker);
 await hold('Complete both halves of the worker loop: build its request, then dispatch only an allowed action and return the result.',8);
 await page.getByRole('button',{name:'Check my build_worker_request code',exact:true}).click();
 await page.waitForTimeout(800);
 await hold('The free check exercises those functions with stub tools. Starting the real coding worker is a separate action.',6);
 await step('3 · Divide and claim the work');
 await (await visibleEditor()).scrollIntoViewIfNeeded();
 await hold('Now write the coordinator. A task can start only after its dependencies are integrated.',5);
 await replaceCode(answers.tasks);
 await hold('The readiness check and atomic claim serve different purposes: dependencies first, then one owner.',7);
 await page.getByRole('button',{name:'Check my ready_tasks code',exact:true}).click();
 await page.waitForTimeout(800);
 await hold('Run the real dependency and competing-claim checks. The integration task must stay blocked until its inputs are ready.',6);
 await page.screenshot({path:path.join(deck,'.screenshots/walkthrough-task-check.png')});
 await step('6 · Keep a checked lesson');
 await replaceCode(answers.memory);
 await hold('Retrieve accepted lessons for this scope and interface version. Proposed notes and old rules stay out of the worker request.',7);
 await page.getByRole('button',{name:'Check my select_memories code',exact:true}).click();
 await page.waitForTimeout(800);
 await hold('A useful-looking note is not automatically evidence. The later comparison tests whether the checked lesson changes the work.',6);
 await step('8 · Compare frozen builds');
 await replaceCode(answers.evaluate);
 await page.getByRole('button',{name:'Check my score_scenario code',exact:true}).click();
 await page.waitForTimeout(800);
 await hold('Compare the actual departure IDs in order. The final evaluation also checks the full output with an independent scorer.',6);
 await page.goto(process.env.APP_URL||'http://127.0.0.1:3091',{waitUntil:'networkidle'});
 await page.getByRole('heading',{name:'The last train is still on yesterday’s timetable'}).waitFor();
 await hold('This is the reference app running locally, not an agent result. The rider chooses a platform and a historical time.',7);
 await page.getByText('2024-11-29T00:08:00-05:00',{exact:true}).first().scrollIntoViewIfNeeded();
 await hold('At Park Street after midnight, the board includes the 00:08 train from the previous service day.',6);
 await page.getByRole('heading',{name:'Last direct train on this service date'}).scrollIntoViewIfNeeded();
 await hold('The follow-up feature finds a direct journey and preserves an arrival after midnight. It does not plan transfers.',6);
 await page.getByText('Download this itinerary',{exact:true}).scrollIntoViewIfNeeded();
 await hold('The itinerary is an actual output file. Worker builds must reproduce the required behavior before release.',6);
 await page.screenshot({path:path.join(deck,'.screenshots/walkthrough-reference-app.png')});
}catch(error){actions.push({at:stamp(),error:error.message});throw error;}
finally{
 await fs.writeFile(path.join(output,'local-segment-captions.json'),JSON.stringify(captions,null,2)+'\n');
 await fs.writeFile(path.join(output,'local-segment-actions.json'),JSON.stringify({kind:'Actual browser recording of worked example and reference app',paid_calls:0,actions},null,2)+'\n');
 const video=page.video();await context.close();
 if(video)await video.saveAs(path.join(output,'local-segment.webm'));
 await browser.close();
}
console.log(JSON.stringify({seconds:stamp(),captions:captions.length,output}));
