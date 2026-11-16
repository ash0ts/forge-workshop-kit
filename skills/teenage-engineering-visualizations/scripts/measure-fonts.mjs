// Maintainer utility: regenerate bundled advance widths from the bundled fonts.
import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
let css='';
for(const [file,family,weight] of [['ibm-plex-sans-latin-400-normal.woff2','IBM Plex Sans',400],['ibm-plex-sans-latin-600-normal.woff2','IBM Plex Sans',600],['ibm-plex-mono-latin-400-normal.woff2','IBM Plex Mono',400]]){
 const data=(await fs.readFile(path.join(root,'assets/fonts',file))).toString('base64');
 css+=`@font-face{font-family:'${family}';font-weight:${weight};src:url(data:font/woff2;base64,${data})}`;
}
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage();await page.setContent(`<style>${css}</style>`);
 const metrics=await page.evaluate(async()=>{
  const result={},canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
  for(const [key,font] of [['sans','400 100px "IBM Plex Sans"'],['semibold','600 100px "IBM Plex Sans"'],['mono','400 100px "IBM Plex Mono"']]){
   await document.fonts.load(font);ctx.font=font;result[key]={};
   for(let i=32;i<127;i++)result[key][String.fromCharCode(i)]=ctx.measureText(String.fromCharCode(i)).width/100;
   for(const c of '−→←×÷·—–‘’“”…≥≤±αβσμ²³Å∈')result[key][c]=ctx.measureText(c).width/100;
  }
  return result;
 });
 await fs.writeFile(path.join(root,'assets/font-metrics.json'),JSON.stringify(metrics)+'\n');
}finally{await browser.close()}
