"""Four-hour routing lesson: one request through representation, review and release."""
import re

KEYS = ['cover','queue','manager','dataset','partitions','connect','trace','read-request','words','embeddings','classifier-exercise','macro-f1','recorded-gain','deferral','policy-exercise','review-case','review-exercise','break-one','typed-route','prompted-exercise','judge-purpose','validator-exercise','recorded-judge','review-dataset','retrain-exercise','freeze','final-exercise','native-comparison','native-row','report-exercise','release','close','classifier-answer','policy-answer','validator-answer','sources']
TIMES = [0,2,4,7,10,15,22,26,36,46,57,72,82,95,105,112,120,130,140,151,160,170,183,190,198,220,225,230,232,235,237,239,None,None,None,None]
SECTIONS = [('setup',0,26),('data',26,36),('representations',36,72),('metrics',72,95),('review',95,130),('break',130,140),('judge',140,190),('retrain',190,210),('break',210,220),('final',220,235),('conclusion',235,240)]
IMPLEMENTATION='src/forge_workshop_kit/routing.py'
NOTEBOOK='scripts/routing_cells.py'
SOURCE='https://github.com/ash0ts/forge-workshop-kit/blob/main/'

def time_label(minute): return '' if minute is None else f'{minute//60}:{minute%60:02d}'

def extend(original):
    assert len(original)==len(KEYS), 'Map new original slides before extending the lesson.'
    slides=[]
    for row,key,minute in zip(original,KEYS,TIMES):
        row.update(name=key,key=key,time=time_label(minute),start_minute=minute,
                   concept=row['title'].replace('<br>',' '),source=[IMPLEMENTATION,NOTEBOOK],evidence=[])
        row['body']=row['body'].replace('Three hours','Four hours')
        if row.get('answer'):
            row['exercise']={'step':{'classifier-exercise':'Train classifiers','policy-exercise':'Review requests','validator-exercise':'Check the judge'}[key],
               'function':{'classifier-exercise':'make_classifier','policy-exercise':'needs_review','validator-exercise':'validate_judge'}[key],
               'check':{'classifier-exercise':'Check my classifier code','policy-exercise':'Check my review rule','validator-exercise':'Check my judge validator'}[key],
               'run':{'classifier-exercise':'Train both classifiers on the same messages','policy-exercise':None,'validator-exercise':'Compare the judge with up to eight of my reviews'}[key]}
        elif row['kind']=='exercise':
            row['exercise']={'step':key,'function':None,'check':None,'run':re.sub('<.*?>','',row['body']).split('Run:')[-1].split('Check:')[0].strip()}
        else:row['exercise']=None
        if key in ['recorded-gain','macro-f1','deferral']:row['evidence']=['evidence/routing-qualification-20261114/embedding-17.json','evidence/routing-qualification-20261114/tfidf-17.json']
        if key=='review-case':row['evidence']=['examples/routing/recorded-review.json']
        if key in ['native-comparison','native-row']:row['evidence']=['decks/routing/data/evaltables-native.json']
        if key=='recorded-judge':row['evidence']=['evidence/routing-live-v050.json','decks/routing/public/images/agent-lens-judge-detail.png']
        if key=='break-one':
            row['title']='Take ten minutes. Return at 2:20.'
            row['notes']='Break from elapsed 2:10 to 2:20. Confirm the reviews and trained versions are saved. Reopening does not train or call a model.'
        if key=='judge-purpose':row['title']='Check the model-based judge against your reviews'
        if key=='classifier-answer':row['body']=row['body'].replace('This function trains the head','This function constructs the head. The later fit call trains it')
        if key=='validator-answer':
            row['body']=row['body'].replace('if set(value) !=','if not isinstance(value, dict) or set(value) !=')
            row['notes']='This uses the same type guard as the notebook. Valid JSON is only a response contract; it does not establish agreement with a reviewer.'
        slides.append(row)
    additions={}
    def walk(after,key,title,kind,step,minute,notes,evidence=(),before=False):
        row={'name':key,'key':key,'title':title,'body':f'<RoutingMechanism kind="{dict(representation="vocabulary" if step==1 else "vector").get(kind,kind)}" :step="{step}" />',
             'notes':notes,'kind':'','time':time_label(minute),'start_minute':minute,'answer':None,'exercise':None,
             'concept':title,'source':[IMPLEMENTATION,NOTEBOOK,'src/forge_workshop_kit/routing_teaching.py'],
             'evidence':list(evidence)}
        additions.setdefault((after,before),[]).append(row)
    walk('words','word-vector','Measure the words and phrases in one request','representation',1,39,
         'Read the real review-pool message aloud. The default tokenizer produces my, card, isn, here, yet; single-letter t is omitted. The nine nonzero TF–IDF weights are recalculated from the frozen 8,463 training messages and shown against the actual 21,527-column vocabulary. IDF and the vocabulary use training text only.', ['examples/routing/recorded-review.json'])
    walk('embeddings','sentence-vector','Keep one vector for each request','representation',2,49,
         'Compare the unchanged message with the different representation. Explain 384 as the encoder output size, not a count of hand-chosen keywords. The heatmap shows all 384 actual cached coordinates in index order. Color is signed magnitude, not semantic location. Encoder weights stay frozen.')
    walk('embeddings','construct-head','Construct the estimator before fitting it','fit',1,52,
         'Point to make_classifier: it returns an unfitted estimator. C is inverse regularization strength; changing it changes the training objective, not the number of output intents. max_iter limits optimization. Use the fixed recipe in the required path.')
    walk('embeddings','fit-head','Fit the head on the labeled training rows','fit',2,54,
         'The learner factory supplies the estimator in both branches. TF–IDF fits a vectorizer and head; the embedding branch fits the head on cached features. Both see the same 8,463 labels. The sparse vocabulary width and 384 embedding values are different input spaces.')
    walk('classifier-exercise','predict-probabilities','A fitted classifier returns 77 probabilities','fit',3,68,
         'After the exercise, locate predict_proba and classes_. Array position alone is not an intent label; the class order maps columns to names. Ask which files would be needed to predict after restarting.')
    walk('macro-f1','intent-counts','Count the errors for one intent','metrics',1,75,
         'These are the recorded embedding model’s official-test card_arrival predictions: 34 true positives, 3 false positives, 6 false negatives. Trace a misroute to the appropriate count. This example explains the metric; do not select a new model using these final examples.', ['decks/routing/data/concept-evidence.json'])
    walk('macro-f1','intent-average','Calculate F1, then average across intents','metrics',2,78,
         'Compute precision 34/37 and recall 34/40. F1 is 68/77=0.883117 for this intent. The bars show all 77 saved intent F1s; their mean is the existing 0.920229 result. A per-case correct flag is a different measurement.', ['decks/routing/data/concept-evidence.json'])
    walk('deferral','threshold-policy','Move the threshold without retraining','policy',1,98,
         'Use the keyboard on the slider. The request and classifier probabilities stay unchanged. Coverage and selective accuracy recompute from the 770 saved validation predictions. At zero accepted cases, show unavailable rather than claiming perfect accuracy.', ['decks/routing/data/concept-evidence.json'])
    walk('deferral','review-margin','Choose labeling candidates by their top-two margin','policy',2,102,
         'The displayed review-pool request has confidence 0.508052 and margin 0.180419. Confidence controls automatic deferral; margin ranks which examples to ask someone to label. These are distinct rules in predict and select_review.', ['examples/routing/recorded-review.json'])
    walk('review-exercise','review-provenance','Keep the proposal and accepted label separate','review',1,126,
         'Ask the participant to find all three labels for a case: model proposal, dataset reference, personal accepted label. Do not overwrite the proposal when accepting a correction. The record must preserve who made the decision and which data it belongs to.')
    walk('typed-route','two-model-tasks','The judge reviews a route in a separate call','judge',1,145,
         'The first lane routes eight fixed validation requests. The second judges classifier proposals attached to human reviews. The judge does not consume the eight prompted routes. Both use actual provider calls and native spans; neither sample ranks models on the complete final dataset.')
    walk('judge-purpose','judge-evidence','Keep the accepted label out of the judge prompt','judge',2,164,
         'Show the user message fields in the actual notebook. The accepted label is used afterward to calculate human failure labels, not supplied to the judge. Contrast a malformed response, a valid disagreement and an unavailable request. This exercise is not an automatic native Insights cluster or tag.')
    walk('review-dataset','accepted-training','Refit the head with your accepted labels','review',2,194,
         'Only unique review-pool cases with label_source=human_review and verified=true may extend training. The fixed encoder and original training rows stay. Extra labels can be useful, redundant or wrong; compare validation before selecting a version.')
    walk('freeze','freeze-files','Save the transformations with the weights','freeze',1,222,
         'Have someone name the missing component if only coefficients are saved. TF–IDF needs its fitted vectorizer; the embedding model needs the encoder identity and preprocessing. The review policy also changes what users see.')
    walk('final-exercise','aligned-requests','Compare matching requests, then the operating policy','freeze',2,228,
         'First compare intent predictions across versions on all 3,080 requests. Then compare how many were automatically routed under the chosen policy. A selected version may be the same saved embedding model. Reusing it is a keep decision, not another improvement.')
    second_break={'name':'break-two','key':'break-two','title':'Take ten minutes. Return at 3:40.',
       'body':'<p class="sub">Save the revised classifier and your validation-based choice.</p><p class="aside">No tickets will be forwarded while you are away.</p>',
       'notes':'Break from elapsed 3:30 to 3:40. Keep the final test closed. On return, freeze the version and policy you chose from validation.',
       'time':'3:30','start_minute':210,'kind':'','concept':'Pause after the reviewed-data experiment','exercise':None,'answer':None,'source':[NOTEBOOK],'evidence':[]}
    additions.setdefault(('retrain-exercise',False),[]).append(second_break)
    expanded=[]
    for row in slides:
        expanded+=additions.get((row['key'],True),[]);expanded.append(row);expanded+=additions.get((row['key'],False),[])
    timed=[s for s in expanded if s['start_minute'] is not None]
    for i,row in enumerate(timed):
        start=row['start_minute']; end=timed[i+1]['start_minute'] if i+1<len(timed) else 240
        assert end>=start,(row['key'],start,end)
        section=next(name for name,a,b in SECTIONS if a<=start<b)
        row['timing']={'section':section,'start':start,'duration':end-start}
    for row in expanded:
        if row['start_minute'] is None: row['timing']={'section':'reference','start':None,'duration':0}
        row['notes'] += '\nTeaching source: '+SOURCE+row['source'][0]+'.'
    return expanded
