"""Four-hour PCB inspection lesson, with explicit shapes and operating decisions."""
import re
TIMES={'opening':0,'assignment':2,'real-data':4,'dataset':8,'partitions':11,'connect':16,'trace-code':23,'inspect':27,'encoder':37,'patches':47,'features':59,'cache':74,'classifier':79,'threshold':86,'threshold-exercise':98,'metrics':112,'forge':119,'forge-training':122,'break':130,'review':151,'human':162,'review-fit':173,'freeze':188,'final':210,'native-comparison':219,'native-board':222,'failure':225,'retest':227,'improved-case':229,'regression':231,'reproduce':234,'release':237,'conclusion':239}
SECTIONS=[('setup',0,27),('data',27,37),('features',37,79),('classifier',79,98),('metrics',98,130),('break',130,140),('review',140,188),('freeze',188,200),('break',200,210),('final',210,234),('reproduce',234,240)]
SOURCE='https://github.com/ash0ts/forge-workshop-kit/blob/main/'
IMPLEMENTATION='src/forge_workshop_kit/inspection.py'
NOTEBOOK='scripts/inspection_cells.py'
def label(n):return '' if n is None else f'{n//60}:{n%60:02d}'

def extend(slides):
    extra={}
    for row in slides:
        key=row['key']; minute=TIMES.get(key)
        row.update(name=key,time=label(minute) if minute is not None else 'Optional answer',start_minute=minute,
                   concept=row['title'].replace('<br>',' '),source=[IMPLEMENTATION,NOTEBOOK],evidence=[],exercise=None)
        row['body']=row['body'].replace('Three hours','Four hours').replace('three hours','four hours')
        if key in ['features','threshold-exercise','review']:
            row['exercise']={'step':{'features':'Compute image features','threshold-exercise':'Train the whole-image baseline','review':'Choose examples to review'}[key],
              'function':{'features':'build_features','threshold-exercise':'choose_threshold','review':'choose_review'}[key],
              'check':{'features':'Check my patch-feature function','threshold-exercise':'Check my threshold function','review':'Check my review selector'}[key],
              'run':{'features':None,'threshold-exercise':'Train the whole-image baseline','review':'Select 24 boards for each review method'}[key]}
        elif row['kind']=='exercise':row['exercise']={'step':key,'function':None,'check':None,'run':re.findall(r'<strong>([^<]+)</strong>',row['body'])}
        if key in ['real-data','dataset','encoder','patches']:row['evidence']=['data/inspection-v1/manifest.json','docs/inspection-workshop.md']
        if key in ['native-comparison','native-board']:row['evidence']=['decks/inspection/data/evaltables-native.json']
        if key=='forge-training':row['evidence']=['decks/inspection/public/images/agent-lens-training-original.png']
        if key in ['retest','improved-case','regression']:row['evidence']=['evidence/inspection-teaching-retest-v2/results.json','evidence/inspection-teaching-retest-v2/predictions.json']
        if key=='failure':row['evidence']=['evidence/inspection-qualification-v1/results.json']
        if key=='encoder':row['body']='<InspectionMechanism kind="encoder" :step="1" />'
        if key=='patches':
            row['title']='Compare local features at the same board position'
            row['body']='<InspectionMechanism kind="patch" :step="1" />'
            row['notes']='Use only normal fitting boards as the reference bank. At each spatial position, find the closest actual reference vector after scaling. A normal fitting board cannot match itself. The older mean-patch result is preserved beside the later recorded comparison.'
        if key=='classifier':row['body']=row['body'].replace('validation_scores = inspection.score(data, validation_rows, model)', 'validation_scores = inspection.score(\n    data, validation_rows, model,\n    build_features=build_features,\n)')
        if key=='threshold':row['body']='<InspectionMechanism kind="threshold" :step="1" />'
        if key=='break':
            row['title']='Take ten minutes. Return at 2:20.'
            row['notes']='Break from elapsed 2:10 to 2:20. Confirm both models are saved. After the break we choose where to spend 24 additional labels.'
        if key in ['improved-case','regression']:
            row['body']='<InspectionMechanism kind="outcomes" case-id="'+('pcb1-anomaly-048' if key=='improved-case' else 'pcb1-anomaly-015')+'" />'
        if key=='answer-features':
            row['body']='''```python
whole = data["whole"][rows]
if method == "whole":
    return whole
if method == "nearest-patch":
    errors = inspection.nearest_patch_errors(data, rows, reference)
else:
    errors = inspection.patch_errors(data["patches"][rows], reference)
# Compress distances, then preserve one row per board.
local = np.log1p(errors).reshape(len(rows), -1)
# Feature axis: 512 whole-image values + 196 patch values.
return np.concatenate([whole, local], axis=1)
```
<div class="bottom-note">Both branches are exercised by the free check. The live comparison uses nearest-patch.</div>'''
            row['notes']='The complete function signature is in the notebook. This body includes the historical mean-patch branch required by the free fixture. Each row remains one board; concatenation extends its feature columns.'
    def walk(after,key,title,kind,step,minute,notes,evidence=(),before=False):
        extra.setdefault((after,before),[]).append({'key':key,'name':key,'title':title,
            'body':f'<InspectionMechanism kind="{"features" if kind=="patch" and step==2 else kind}" :step="{step}" />','notes':notes,'time':label(minute),'start_minute':minute,
            'kind':'','answer':None,'concept':title,'exercise':None,'source':[IMPLEMENTATION,NOTEBOOK,'src/forge_workshop_kit/inspection_teaching.py'],'evidence':list(evidence)})
    walk('inspect','board-target','Predict a label for the whole board','data',1,32,
        'Ask participants to choose pass or inspection before advancing. The first figure hides its source label and mask. Identify the photograph as the input and the binary label as the target. A detector flags a board; it does not learn pixel labels here.', ['data/inspection-v1/records.json'])
    walk('inspect','mask-boundary','Use the mask to investigate the decision','data',2,34,
        'Now reveal pcb1-anomaly-005 from the fitting partition: source image pcb1/Data/Images/Anomaly/005.JPG, SHA-256 ec34541be729af29a287bde12d4e3955cf3f83c734baea8a9505a7b801ce54e2, VisA CC BY 4.0. Source metadata and bundled image/mask checksums are in decks/inspection/data/feature-example.json. Ask which input would leak the answer if passed to the classifier. The mask is reference evidence for human inspection; neither masks nor test labels enter feature assembly.', ['data/inspection-v1/records.json','decks/inspection/data/feature-example.json'])
    walk('encoder','patch-grid','Keep local information as well as the whole image','encoder',2,41,
        'Read the shapes out loud: N boards, 14 rows, 14 columns, 64 feature channels. The overlay shows feature positions schematically, not exact independent image crops. The whole-image representation has 512 values; the grid retains spatial differences.', ['src/forge_workshop_kit/inspection_encoder.py'])
    walk('patches','append-patches','Append 196 distances to the 512 whole-image values','patch',2,53,
        'Walk the same board through errors, log1p, reshape and concatenate. The output has 708 columns. axis=0 would add observations rather than features and fail the shape/order fixture. log1p compresses large distances; it does not turn them into probabilities.')
    walk('classifier','fit-operation','Fit on training boards; measure on validation boards','train',1,82,
        'Point to the learner build_features argument. The same function must be supplied to fit and score. We fit a small class-balanced logistic classifier, not the ResNet encoder. Saving a completed fit and exporting its trace happen afterward.')
    walk('threshold','validation-cutoff','Require 11 of the 12 validation defects to be caught','threshold',2,92,
        'The slider uses the exact existing free fixture. With three fixture defects and recall 2/3 the cutoff is 0.7. For the real validation set, ceil(.9*12)=11. Explain that the chosen cutoff constrains this validation set only.', ['src/forge_workshop_kit/inspection_teaching.py:check_threshold','docs/inspection-workshop.md'])
    walk('metrics','ranking-ap','Calculate ranking quality before choosing one cutoff','ranking',1,114,
        'Use the five public fixture scores. Defects occur at ranks 2,3,4; precision is 1/2,2/3,3/4 at those recalls. Average precision is their mean, 0.638889. This is an illustrative calculation, not a PCB1 result.', ['src/forge_workshop_kit/inspection_teaching.py:check_threshold'])
    walk('metrics','operating-errors','Count operating errors at the chosen cutoff','ranking',2,117,
        'At cutoff 0.7, the fixture has one missed defect and one false alarm. Moving the cutoff leaves the score ordering and AP unchanged. A review band sends additional cases to people and should be reported as workload, not detection improvement.')
    walk('forge-training','training-evidence','Match the tool call to the saved validation result','train',2,126,
        'Return to the code and identify the training arguments corresponding to the capture. The trace is a CPU tool operation, with no LLM provider call. A failed trace upload must not cause another fit. Find C, method, training count and validation counts in your own run.')
    walk('review','active-selection','Choose uncertain boards before opening their labels','review',1,140,
        'Predict which scores the selector will choose. The public fixture uses row IDs 10,20,30,40 with scores .8,-.1,.01,-.9. At threshold 0, the two closest rows are 20 and 30. The function receives no labels.', ['src/forge_workshop_kit/inspection_teaching.py:check_review'],before=True)
    walk('review','random-control','Give random selection the same labeling budget','review',2,146,
        'Both branches start from the same nearest-patch parent and review pool. Each gets 24 labels; overlapping selections are allowed across methods. Random selection controls for simply receiving more data. Do not promise that uncertainty sampling wins.')
    # Keep both concept builds before the exercise, ordered by elapsed time.
    extra[('review',True)] += extra.pop(('review',False))
    walk('freeze','detector-bundle','Freeze the preprocessing and reference bank too','freeze',1,194,
        'Name the pieces needed to reproduce a score: reference bank, scaling, participant feature code, coefficients and threshold. Selecting the version uses validation. The final comparison still includes all four frozen versions.')
    walk('reproduce','reload-detector','Reproduce one score from the saved detector','freeze',2,236,
        'The reload operation uses the frozen feature source rather than the current editor draft. Compare its output with the previously saved score for the same case. An artifact makes that complete version addressable; Registry is an optional release extension.')
    extra[('freeze',False)].append({'key':'break-two','name':'break-two','title':'Take ten minutes. Return at 3:30.',
       'body':'<p class="sub">Your detector and threshold are frozen. Leave the final comparison for when everyone is back.</p>',
       'notes':'Break from elapsed 3:20 to 3:30. No training runs during the break. On return, evaluate the saved versions.',
       'time':'3:20','start_minute':200,'kind':'','answer':None,'concept':'Pause after freezing the comparison','exercise':None,'source':[NOTEBOOK],'evidence':[]})
    out=[]
    for row in slides:out+=extra.get((row['key'],True),[]);out.append(row);out+=extra.get((row['key'],False),[])
    def exercise_row(key,title,body,minute,step,run,notes):
        return dict(name=key,key=key,title=title,body=body,notes=notes,kind='exercise',
                    time=label(minute),start_minute=minute,answer=None,concept=title,
                    source=[NOTEBOOK],evidence=[],exercise=dict(step=step,function=None,check=None,run=run))
    out.extend([
        exercise_row('baseline-observation','Inspect a baseline miss or false alarm',
            '<div class="task">Notebook: Train the whole-image baseline</div><ol class="exercise-controls"><li>Select a validation board. Compare the photograph, annotation, score, and cutoff.</li><li>Explain what the whole-image detector missed or flagged. What local detail might help?</li><li>Optionally click <strong>Save my baseline observation</strong>.</li></ol><p class="done"><b>Check:</b> A saved baseline decision supports your hypothesis. No patch model has run yet.</p>',
            65,'Train the whole-image baseline','Save my baseline observation',
            'Choose a saved validation error if available; do not force a failure. If the baseline gets the selected board right, describe what evidence would distinguish the next representation. The displayed score comes from the saved weights and feature source.'),
        exercise_row('one-patch-distance','Calculate the distance at one image position',
            '<div class="task">Notebook: Compute image features</div><p>Click <strong>Calculate one patch distance</strong>. Read the visible calculation at row 7, column 7 of fitting board pcb1-anomaly-005.</p><ol class="exercise-controls"><li>Scale each channel using normal fitting boards.</li><li>Compare the query vector with each normal vector at that position.</li><li>Take the smallest mean squared difference, then log1p.</li></ol><p class="done"><b>Check:</b> Your displayed minimum agrees with nearest_patch_errors.</p>',
            82,'Compute image features','Calculate one patch distance',
            'These values come from the real prepared feature cache, not the five-board threshold fixture. Only fitting boards form the reference bank. The free calculation does not fit a classifier.'),
        exercise_row('patch-experiment','Test patches against the saved baseline',
            '<div class="task">Notebook: Compare global and patch features</div><ol class="exercise-controls"><li>Keep the whole-image branch, C=0.03, and threshold rule unchanged.</li><li>Click <strong>Train the patch-feature alternative</strong>.</li><li>Compare its validation mistakes with the saved whole-image result.</li></ol><p class="done"><b>Check:</b> Both representations are saved before continuing to review selection.</p>',
            104,'Compare global and patch features','Train the patch-feature alternative',
            'The first fit remains valid while learners implement the patch branch. A changed threshold rule or changed whole-image inputs would confound this comparison and is rejected. Previously saved matching runs are reused.'),
    ])
    first=[('opening',0),('assignment',2),('real-data',4),('board-target',6),('mask-boundary',8),
           ('dataset',10),('partitions',13),('connect',17),('trace-code',23),('inspect',27),('encoder',32),
           ('classifier',37),('fit-operation',40),('threshold',44),('validation-cutoff',48),
           ('threshold-exercise',53),('baseline-observation',65),('patch-grid',72),('patches',76),
           ('one-patch-distance',82),('append-patches',87),('features',92),('cache',101),('patch-experiment',104)]
    by_key={row['key']:row for row in out}
    for key,minute in first: by_key[key].update(start_minute=minute,time=label(minute))
    chosen={key for key,_ in first}
    out=[by_key[key] for key,_ in first]+[row for row in out if row['key'] not in chosen]
    by_key['real-data']['notes']+=' The same fitting example is bundled in the notebook setup. Ask for a pass/review choice before revealing its annotation; no authentication or download is needed.'
    timed=[s for s in out if s['start_minute'] is not None]
    for i,row in enumerate(timed):
        start=row['start_minute'];end=timed[i+1]['start_minute'] if i+1<len(timed) else 240
        assert end>=start,(row['key'],start,end)
        row['timing']={'section':next(name for name,a,b in SECTIONS if a<=start<b),'start':start,'duration':end-start}
    for row in out:
        if row['start_minute'] is None:row['timing']={'section':'reference','start':None,'duration':0}
        row['notes']+='\nTeaching source: '+SOURCE+row['source'][0]+'.'
    return out
