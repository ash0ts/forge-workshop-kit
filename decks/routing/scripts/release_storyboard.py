"""Release-and-recovery capstone. The label-order fault is an explicit teaching drill."""
SOURCE = 'src/forge_workshop_kit/routing_release.py'
NOTEBOOK = 'scripts/routing_cells.py'
SESSION_MINUTES = 330


def extend(slides):
    added = []
    def row(key, title, body, minute, notes, kind='', exercise=None, answer=None):
        added.append(dict(name=key, key=key, title=title, body=body, time=f'{minute//60}:{minute%60:02d}' if minute is not None else '',
            start_minute=minute, notes=notes, kind=kind, answer=answer, exercise=exercise,
            concept=title, source=[SOURCE, NOTEBOOK], evidence=[]))
    def task(key, title, minute, steps, button, check, function=None, free=None, answer=None):
        link=f'<a class="answer-link" href="/{answer}">Worked answer ↗</a>' if answer else ''
        body=link+'\n\n<p class="where">Notebook → Release and recover</p><ol>'+''.join('<li>'+s+'</li>' for s in steps)+'</ol><div class="done"><strong>Run:</strong> '+button+'<br><strong>Check:</strong> '+check+'</div>'
        row(key,title,body,minute,'Give learners time to make the change before showing a worked answer. This release drill reuses the selected classifier. It sends no inference request and does not train again. Find the exact saved stage and native evidence links in the result.',
            'exercise', {'step':'Release and recover','function':function,'check':free,'run':button},answer)

    row('release-break','Take ten minutes. Return at 4:05.',
        '<p class="sub">Your classifier is selected. After the break, we will load its saved files and check that it still routes requests the same way.</p><p class="aside">The support team has asked whether “saved somewhere” counts as released.</p>',235,
        'Break from 3:55 to 4:05. Existing official-test results are complete; do not tune against them during the release lab.')
    row('release-request','The classifier works. Can another process use it?',
        '<div class="quote">“Please put the chosen version into the batch router. The queues are already there.”</div><div class="flow"><div>Selected experiment<small>Known predictions</small></div><b class="arrow">→</b><div>Saved release<small>Exact files and metadata</small></div><b class="arrow">→</b><div>Reloaded predictor<small>Do the destinations still match?</small></div></div><p class="caption">We will introduce a loader defect deliberately. This is a release drill, not a newly discovered model failure.</p>',245,
        'The scenario changes from model selection to delivery. The model weights stay fixed. Participants will see how an integration defect can invalidate an otherwise useful model. Explain the fault in advance; do not stage it as an organic discovery.')
    row('release-bundle','Save what the predictor needs, then reload it', '<ReleaseWalk kind="bundle" />',248,
        'The artifact contains classifier, feature representation identity, intent order, review policy, source, checks, and fixed case IDs. The source sequence is abbreviated. An exact artifact version permits reproduction; a mutable latest alias does not identify what ran. Never unpickle arbitrary downloaded models; use the artifact just created in the participant project.')
    task('release-prepare-exercise','Load your selected version from its artifact',251,
        ['Click <b>Prepare the selected router for release</b>. Inspect the files it saves.',
         'Click <b>Publish and reload the exact release artifact</b>. Copy its exact version into your notes.',
         'Compare the reloaded predictions with the intact saved release.'],
        'Prepare the selected router for release → Publish and reload the exact release artifact',
        'Prediction parity passes without fitting another classifier.')
    row('release-cohort','Choose the regression cases before predicting',
        '<svg class="diagram" viewBox="0 0 1120 290" role="img" aria-label="The existing 770-example review pool supplies one case per intent. Lexically first case IDs define 77 fixed regression cases. The official test set is unchanged."><rect x="0" y="45" width="300" height="115" fill="#e5e9dc"/><text x="22" y="86" style="font-size:28px">770 review requests</text><text x="22" y="128" style="font-size:21px">Training-derived pool</text><path d="M315 105H390" stroke="#718a7c" stroke-width="3"/><rect x="405" y="45" width="300" height="115" fill="#d3e6dc"/><text x="427" y="86" style="font-size:28px">One per intent</text><text x="427" y="128" style="font-size:21px">First case ID, sorted</text><path d="M720 105H795" stroke="#718a7c" stroke-width="3"/><rect x="810" y="45" width="300" height="115" fill="#d3e6dc"/><text x="832" y="86" style="font-size:28px">77 fixed cases</text><text x="832" y="128" style="font-size:21px">Same batch, each release</text><text x="0" y="230" style="font-size:24px">Regression and reproduction check: not a new independent test set.</text></svg>',257,
        'The cohort is selected and saved before predictions, using the lexical first review-pool case per intent. Some reviewed cases may have been accepted into training. This batch tests release behavior, not generalization. The original 3,080 official test predictions remain unchanged.')
    row('release-columns','A probability belongs to a specific intent', '<ReleaseWalk kind="mapping" :step="1" />',260,
        'Illustrative three-column values; the real model has 77 intent columns. Trace column 1 from 0.84 to card_not_working using model.classes_. The message and probabilities are explanatory, not a recorded participant output.')
    row('release-fault','Rotated labels send column 1 to another queue', '<ReleaseWalk kind="mapping" :step="2" />',262,
        'The deliberately faulty loader rotates the names by one position. Column1 still contains 0.84 but now names cash_withdrawal_not_recognised. Valid output and high confidence do not establish a correct destination. Participants inspect actual 77-class predictions in the next exercise.')
    task('release-incident-exercise','Find one request sent to the wrong queue',266,
        ['Run the faulty loader on the fixed batch.',
         'Open its Agent Lens operation and compare the loaded label order with the saved model classes.',
         'Choose a changed route. Record its case, proposed intent, accepted label, and your reason.'],
        'Run the deliberately faulty release', 'The weights and confidence are unchanged; the returned intent moves.')
    row('release-set-check','Checking the label set misses this defect', '<ReleaseWalk kind="checks" :step="1" />',273,
        'All expected names are still present. A set comparison discards order, precisely the part that links probability columns to intents. Ask learners which extra check would detect the fault.')
    row('release-order-check','Check order before accepting the loaded model', '<ReleaseWalk kind="checks" :step="2" />',275,
        'Implement both exact order and set checks. Do not sort labels as the repair: a classifier may use another class order. The free fixture intentionally uses a nonalphabetical order.')
    task('release-repair-exercise','Repair the loader and write its regression check',280,
        ['Complete <code>label_names(model_classes)</code> by preserving the supplied order.',
         'Complete <code>check_release(model_classes, loaded_labels)</code>. Check the label set and exact order.',
         'Run the free check, then execute your repaired loader on the same 77 requests.'],
        'Check my release and repair code → Run my repaired loader on the same requests',
        'Order and prediction parity pass. Existing classifier mistakes may remain.',
        'label_names; check_release', 'Check my release and repair code', 'release-repair-answer')
    row('release-parity','A repaired loader should reproduce the intact release', '<ReleaseWalk kind="checks" :step="3" />',290,
        'Compare the healthy, faulty and repaired outputs by case ID. Parity with the intact release establishes recovery from this drill. Macro-F1 still measures agreement with labels. A model can reproduce its own mistakes perfectly. Keep those two claims separate.')
    row('release-investigate','Compare three versions of the same request',
        '<table class="clean-table small-table"><thead><tr><th>Version</th><th>What to inspect</th><th>Question</th></tr></thead><tbody><tr><td>Intact release</td><td>Saved intent + confidence</td><td>What did the selected version return?</td></tr><tr><td>Faulty loader</td><td>Same probabilities, rotated names</td><td>Which destination changed?</td></tr><tr><td>Your repair</td><td>Restored mapping + regression check</td><td>Did the prediction return to its original value?</td></tr></tbody></table><p class="release-evidence">Open the notebook’s saved comparison in EvalTables. Then follow one changed case to its batch trace and exact artifact.</p><p class="caption">No fabricated result is shown here. Use your actual saved rows; publication status is separate from execution.</p>',296,
        'This is an investigation guide rather than a product screenshot. Use native links from the release result. If publication is unavailable, inspect the notebook comparison and retry publication only. Do not rerun the batch to fix an export error.')
    task('release-decision-exercise','Decide whether this release passes its checks',300,
        ['Review label order, set membership, and prediction parity.',
         'Select release or reject and explain the choice. A failed check cannot be approved as a passing release.',
         'Save the exact artifact and comparison alongside your decision.'],
        'Save my release decision', 'The decision names the tested artifact and its checks.')
    row('release-rollback','Rollback reloads a version; it does not undo training',
        '<div class="flow"><div>Previous intact artifact<small>Exact version remains available</small></div><b class="arrow">→</b><div>Fresh restore folder<small>Load saved model and metadata</small></div><b class="arrow">→</b><div>Same request batch<small>Verify the original predictions</small></div></div><p>You are switching the batch predictor’s selected files. No new fit and no model-weight reversal are needed.</p><p class="caption">Registry can organize approved versions. It does not deploy this Python predictor automatically.</p>',308,
        'Require an explicit rollback action. Preserve the faulty release and its evidence for diagnosis rather than deleting it. The required path uses Artifacts in the participant project; Registry permissions are optional.')
    task('release-rollback-exercise','Restore the previous version and verify it',312,
        ['Click the restore control. Confirm it loads the previously recorded exact artifact.',
         'Run its fixed batch and check parity with the intact release.',
         'Explain which defect the rollback removed and which classifier errors it cannot fix.'],
        'Restore the previous release and verify its predictions', 'Restored predictions match the saved intact version.')
    row('release-conclusion','Separate the model gain from the release repair',
        '<div class="two-col"><div><h2>Model comparison</h2><p>Did a different representation or accepted training data improve routing on the official test set?</p></div><div><h2>Release drill</h2><p>Did the repaired loader reproduce the selected model’s destinations on the fixed regression batch?</p></div></div><p class="caption">The first measures a classifier change. The second verifies recovery from a known implementation defect.</p>',320,
        'Have participants explain both results without merging denominators or calling the drill a new benchmark. Preserve original 3,080-test predictions; the 77-case capstone cohort is reused and may overlap reviewed training additions. Keep remaining genuine classifier errors in the conclusion.')
    row('release-repair-answer','Worked answer: preserve the probability-column order',
        '```python\ndef label_names(model_classes):\n    return list(model_classes)\n\ndef check_release(model_classes, loaded_labels):\n    expected = list(model_classes)\n    loaded = list(loaded_labels)\n    return {\n        "label_set": set(loaded) == set(expected),\n        "label_order": loaded == expected,\n    }\n```\n\n<p class="answer-nav source-link"><a href="/release-repair-exercise">Return to the release repair exercise ↩</a></p>',None,
        'This checks the metadata contract; the subsequent saved batch checks prediction parity independently. Passing both checks does not prove every route is correct. Give the worked answer after an attempt or explicit request.', 'answer')

    main=[s for s in added if s['start_minute'] is not None]
    answers=[s for s in added if s['start_minute'] is None]
    output=[]
    for s in slides:
        if s['key']=='cover':
            s['body']=s['body'].replace('Four hours', '5½ hours').replace('test a revised version using public banking requests.', 'test a revised version, then release and recover it using public banking requests.')
        if s['key']=='report-exercise':
            output.extend(main)
            s['start_minute']=325;s['time']='5:25'
            s['body']=s['body'].replace('State whether the revised classifier helped on the declared measure.', 'Separate the official-test classifier result from the controlled release repair.').replace('Describe one request that still needs a person.', 'Describe a remaining routing mistake and the regression check you added.')
            s['notes']='Final five minutes: explain the classifier comparison and the release drill separately. Include the tested artifact, decision, rollback evidence, and remaining errors. Publication reuses saved work.'
        if s['key']=='release':
            s['start_minute']=328;s['time']='5:28';s['title']='Optional: organize approved versions in Registry'
            s['body']='<p>Link the exact evaluated artifact to Registry if your project has permission. Keep the checks, previous version, and release decision alongside it.</p><p>ARIA can investigate the saved incident where access permits. Verify its cited event before accepting a proposed next test.</p><p class="caption">These are optional. Your batch predictor and Artifact-based rollback already work without Registry or ARIA.</p>'
            s['notes']='Registry manages versions, not automatic deployment. ARIA access and usage are separate; it cannot approve a repair automatically. The core capstone contains no new inference calls or training. Specialist fine-tuning remains a separately qualified future lesson.'
        if s['key']=='close':s['start_minute']=329;s['time']='5:29'
        if s['key']=='sources':output.extend(answers)
        output.append(s)
    timed=[s for s in output if s['start_minute'] is not None]
    for i,s in enumerate(timed):
        end=timed[i+1]['start_minute'] if i+1<len(timed) else SESSION_MINUTES
        if end<s['start_minute']:raise ValueError(f"Invalid timing for {s['key']}")
        section='release-and-recovery' if 235<=s['start_minute']<325 else s.get('timing',{}).get('section','conclusion')
        s['timing']={'section':section,'start':s['start_minute'],'duration':end-s['start_minute']}
    for s in answers:s['timing']={'section':'reference','start':None,'duration':0}
    return output
