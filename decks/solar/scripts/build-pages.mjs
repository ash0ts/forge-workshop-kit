import {spawnSync} from 'node:child_process';
import fs from 'node:fs/promises';
const base=process.env.DECK_BASE||'/forge-workshop-kit/solar/';
const python=process.env.PYTHON||'python3';
const run=(command,args,env=process.env)=>{
 const result=spawnSync(command,args,{stdio:'inherit',env});
 if(result.status!==0)throw new Error(`${command} exited with ${result.status}: ${result.error||''}`);
};
try{
 run(python,['scripts/build-storyboard.py'],{...process.env,DECK_BASE:base});
 run(process.execPath,['node_modules/@slidev/cli/bin/slidev.mjs','build','--base',base,'--out','dist-pages']);
 await fs.copyFile('dist-pages/index.html','dist-pages/404.html');
}finally{
 run(python,['scripts/build-storyboard.py'],{...process.env,DECK_BASE:''});
}
