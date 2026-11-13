import {createServer} from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {chromium} from 'playwright';
import {existsSync} from 'node:fs';
const systemChrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const executablePath=process.env.CHROME_PATH||(existsSync(systemChrome)?systemChrome:undefined);
const prefix='/forge-workshop-kit/solar/';
const root=path.resolve('dist-pages');
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2','.json':'application/json'};
const server=createServer(async(req,res)=>{
 try{
  const url=new URL(req.url,'http://localhost');
  if(!url.pathname.startsWith(prefix)){res.writeHead(404);res.end();return}
  let file=path.resolve(root,url.pathname.slice(prefix.length));
  if(!file.startsWith(root+'/')&&file!==root){res.writeHead(403);res.end();return}
  if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
  const data=await fs.readFile(file);res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');res.end(data);
 }catch{res.writeHead(404);res.end()}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}${prefix}`;
const map=JSON.parse(await fs.readFile('notes/slide-map.json','utf8'));
const browser=await chromium.launch({headless:true,executablePath});
try{
 const page=await browser.newPage();
 await page.addInitScript(()=>{
  window.__wakeLockRequests=0;
  Object.defineProperty(navigator,'wakeLock',{value:{request(){
   window.__wakeLockRequests++;
   return Promise.reject(new Error('Wake Lock denied in deployment check'));
  }}});
 });
 const {routes}=JSON.parse(await fs.readFile(path.join(root,'static-routes.json'),'utf8'));
 for(const route of routes){
  const response=await fetch(base+route);
  if(response.status!==200)throw new Error(`Known route ${route}: HTTP ${response.status}`);
 }
 if((await fetch(base+'unknown-slide')).status!==404)throw new Error('Unknown route must return 404');
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const network=[];page.on('response',r=>{if(r.status()>=400)network.push([r.status(),r.url()])});
 for(const key of ['cover','native-lens','persistence-image']){
  await page.goto(base+map.slides.find(s=>s.key===key).number,{waitUntil:'networkidle'});
  const missing=await page.locator('.slidev-page img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src));
  if(missing.length)throw new Error('Missing images '+JSON.stringify(missing));
 }
 const exercise=map.slides.find(s=>s.answer);await page.goto(base+exercise.number);
 await page.locator('a.answer-link:visible').click();await page.waitForTimeout(150);
 if(!page.url().startsWith(base))throw new Error('Answer left deployment prefix');
 await page.reload({waitUntil:'networkidle'});
 await page.locator('.source-link a:visible').click();await page.waitForTimeout(150);
 if(page.url()!==base+exercise.number)throw new Error('Return link mismatch: '+page.url());
 await page.goto(base+'presenter/1',{waitUntil:'networkidle'});
 if(await page.evaluate(()=>window.__wakeLockRequests)!==0)throw new Error('Wake Lock was requested');
 if(errors.length||network.length)throw new Error(JSON.stringify({errors,network}));
 const result={base_path:prefix,images:'passed',answer_navigation:'passed',deep_link_reload:'passed',known_routes_http_200:routes.length,unknown_route_http_404:true,wake_lock_requests:0,page_errors:errors,failed_responses:network};
 await fs.writeFile('notes/pages-checks.json',JSON.stringify(result,null,2)+'\n');console.log(result);
}finally{await browser.close();server.close()}
