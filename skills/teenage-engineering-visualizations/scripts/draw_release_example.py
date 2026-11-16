"""Illustrative local release mechanism, independent of Forge and Workshop Kit."""
from pathlib import Path
import json
from illustration import Illustration, COLORS as C, ROOT


def sheet(d, x, y, w, h, title, rows, *, accent=False):
    d.path(f'M{x} {y}H{x+w-20}L{x+w} {y+20}V{y+h}H{x}Z', fill=C['white'], stroke=C['accent'] if accent else C['ink'])
    d.path(f'M{x+w-20} {y}V{y+20}H{x+w}', stroke=C['line'])
    d.text(title,x+14,y+12,size=20,weight=600,width=w-30)
    d.line(x,y+44,x+w,y+44,stroke=C['line'])
    for i,row in enumerate(rows):
        d.text(row,x+14,y+55+i*29,size=16,mono=True,width=w-28)


def draw(state, index):
    d=Illustration('An exact release, then a rollback')
    d.text('LOCAL RELEASE / ILLUSTRATIVE MECHANISM',36,14,size=15,mono=True,width=920)
    d.text('The release pointer moves. The saved files do not.',36,41,size=30,weight=600,width=1100)
    d.line(36,90,1164,90,stroke=C['line'])
    d.text('01  Inspect the saved package',36,104,size=20,weight=600,width=410)
    d.text('02  Check the file identities',460,104,size=20,weight=600,width=360)
    d.text('03  Select an exact version',870,104,size=20,weight=600,width=300)
    # An opened folder and the actual structure its manifest describes.
    d.path('M44 163H134L156 183H410V445H44Z',fill=C['panel'])
    d.text('release-v4/',60,185,mono=True,size=18,width=310)
    d.path('M77 222V374M77 242H105M77 290H105M77 338H105',stroke=C['muted'])
    for n,(y,name) in enumerate([(224,'model.bin'),(272,'labels.json'),(320,'predict.py')]):
        d.rect(108,y,275,36,fill=C['white'],stroke=C['line'])
        d.text(name,122,y+7,size=17,mono=True,width=245)
    # Weights as stored bytes, and ordered labels as an array, not generic icons.
    d.text('weights',60,397,size=16,width=90)
    for i in range(12):
        d.rect(145+i*19,397,13,20,fill=C['ink'] if i in (1,4,8) else C['line'],stroke='none')
    sheet(d,475,159,337,264,'manifest.json',[
        'version: "v4"',
        'model:  92c7…ef10',
        'labels: 41a8…97b2',
        'source: 3fd0…184c',
        'checks: "passed"'],accent=state in ('check','select'))
    d.arrow(412,285,472,285,color=C['accent'] if state=='check' else C['ink'])
    d.text('hash each file',421,434,size=16,width=190)
    # A release index exposes two immutable slots; the pin is the mutable part.
    for y,version,hashvalue in [(177,'v3','b501…809a'),(307,'v4','92c7…ef10')]:
        d.rect(910,y,238,91,fill=C['white'])
        d.text(version,927,y+12,size=26,weight=600,width=62)
        d.text(hashvalue,927,y+52,size=16,mono=True,width=210)
        d.circle(892,y+44,9,fill=C['paper'])
    chosen = 351 if state=='select' else 221
    d.path(f'M852 221V351',stroke=C['line'],sw=5)
    d.circle(852,chosen,8,fill=C['accent'],stroke=C['accent'])
    d.arrow(852,chosen,882,chosen,color=C['accent'])
    d.text('current',860,425,size=18,mono=True,width=150)
    d.text('→ v4' if state=='select' else '→ v3',1010,425,size=18,mono=True,width=120)
    d.label('1','Manifest binds the three files',60,465,606,393,width=330)
    d.label('2','Only this pointer changes',805,465,852,chosen,width=305)
    d.line(36,548,1164,548,stroke=C['line'])
    code={'package':'files = [model, ordered_labels, predict_source]', 'check':'assert actual_hashes == manifest["file_hashes"]', 'select':'current.write_text("v4")  # only after the release checks', 'rollback':'current.write_text("v3")  # load its original files'}[state]
    consequence={'package':'Keep the model, ordered labels, and prediction code together.', 'check':'A matching filename is insufficient. Verify the contents before loading.', 'select':'The next batch loads v4. Both saved packages remain available.', 'rollback':'The next batch loads v3 again; no training or file reconstruction is needed.'}[state]
    d.text(code,36,562,size=17,mono=True,width=1125)
    d.text(consequence,36,605,size=20,width=1125,weight=600)
    d.text(f'{index+1:02d} / 04',1080,16,size=15,mono=True,width=90)
    d.save(ROOT/'examples/release-mechanism'/f'{state}.svg')


def main():
    names=['package','check','select','rollback']
    for i,state in enumerate(names): draw(state,i)
    spec={'schema_version':1,'id':'release-mechanism','kind':'sequence','title':'Load an exact release, then roll it back',
          'provenance':'illustrative','summary':'Illustrative local file layout. Hashes are shortened placeholders, not measured artifact identifiers.',
          'steps':[{'id':s,'title':t,'body':b} for s,t,b in zip(names,['Save the files','Verify contents','Select version four','Restore version three'],[
              'Package model weights, ordered labels, and prediction code together.',
              'Compare each file hash with the saved manifest before loading.',
              'Change the current-version pointer after release checks pass.',
              'Restore the previous exact package without retraining.'])],
          'states':[{'id':s,'label':t,'visible':names[:i+1],'focus':[s], 'artwork':f'release-mechanism/{s}.svg',
                     'caption':'Illustrative local release; abbreviated hash values.'} for i,(s,t) in enumerate(zip(names,['Saved package','Content check','Select v4','Rollback to v3']))],
          'source_links':[]}
    (ROOT/'examples/release-mechanism.json').write_text(json.dumps(spec,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
