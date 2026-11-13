"""Package validated static slides and editable deck source. Makes no remote calls."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
layout=json.loads((root/'notes/slide-map.json').read_text())
render=json.loads((root/'notes/render-checks.json').read_text())
pdf=json.loads((root/'notes/pdf-checks.json').read_text())
assert render['slides_checked']==layout['total_slides']
assert not render['issues'] and not render['console_errors']
assert pdf['pages']==layout['total_slides'] and pdf['empty_pages']==0
assert (root/'dist/serve.py').exists()
assert json.loads((root/'notes/exercise-contract-checks.json').read_text())['status']=='passed'
assert json.loads((root/'notes/recorded-evidence-checks.json').read_text())['status']=='passed'
assert json.loads((root/'notes/answer-checks.json').read_text())['provider_calls']==0
stages=json.loads((root/'public/recorded-study.json').read_text())['stages']
for name in ('images/final-comparison','goes/final-comparison','images/round-2/adopt'):
    assert any(row['name']==name and row['status']=='complete' for row in stages),name
source_roots=['README.md','package.json','package-lock.json','slides.md','style.css',
              'global-bottom.vue','components','data','public','scripts','notes']
def archive(filename,files,prefix,relative_root):
    with zipfile.ZipFile(root/filename,'w',compression=zipfile.ZIP_DEFLATED) as out:
        for file in sorted(files):
            if file.is_file() and file.name!='release-files.json' and '__pycache__' not in file.parts:
                out.write(file,str(Path(prefix)/file.relative_to(relative_root)))
    return root/filename
browser=archive('solar-autoresearch-browser.zip',(root/'dist').rglob('*'),'solar-autoresearch-browser',root/'dist')
files=[]
for item in source_roots:
    item=root/item;files.extend(item.rglob('*') if item.is_dir() else [item])
source=archive('solar-autoresearch-deck-source.zip',files,'solar-autoresearch-deck-source',root)
release={'main_frames':layout['main_slides'],'total_frames':layout['total_slides'],
         'files':[{'file':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                  for path in (browser,source,root/'solar-autoresearch.pdf')],
         'assets':[{'file':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                   for path in sorted((root/'public').rglob('*')) if path.is_file()]}
(root/'notes/release-files.json').write_text(json.dumps(release,indent=2)+'\n')
print(json.dumps({k:v for k,v in release.items() if k!='assets'},indent=2))
