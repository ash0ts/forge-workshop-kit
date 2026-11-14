"""Six-hour teaching sequence; presentation only, with no experiment execution."""
from pathlib import Path
import json

SCHEDULE = [
    ('setup','Connect and trace an operation',0,25,'cover'),
    ('data','Read observations and implement persistence',25,65,'goes-window'),
    ('tracking','Explain loss and save a training run',65,95,'number'),
    ('break-one','Break',95,110,'break-one'),
    ('search','Inspect model shapes and compare configurations',110,155,'search-levels'),
    ('images','Implement image prediction and scoring',155,200,'images-window'),
    ('meal','Meal break',200,230,'meal-break'),
    ('agent','Build the research-agent request',230,260,'agent-need'),
    ('rounds','Review and test two rounds of changes',260,310,'propose'),
    ('break-two','Break',310,320,'break-two'),
    ('evaluation','Freeze and compare on reserved dates',320,345,'freeze'),
    ('conclusion','Reproduce and explain the result',345,360,'reproduce'),
]


def expand(slides, root):
    index=lambda key: next(i for i,s in enumerate(slides) if s['key']==key)
    find=lambda key: slides[index(key)]
    def slide(key,title,body,notes,concept,clicks=0,source=None):
        return dict(key=key,title=title,body=body,notes=notes,kind='',time='',answer=None,
                    concept=concept,clicks=clicks,source=source or ['src/forge_workshop_kit/solar.py'],
                    evidence={'type':'explanation','records':[]})
    def insert(after,rows):
        at=index(after)+1; slides[at:at]=rows
    def graphic(mode,stages=3):
        return f'<SolarConcept mode="{mode}" :reveal="Math.min($clicks + 1, {stages})" />'
    def code(text,highlight='all'):
        return '```python {'+highlight+'}\n'+text+'\n```\n\n'
    def note(text): return '<div class="bottom-note">'+text+'</div>'
    window=json.loads((root/'data/teaching-window.json').read_text())

    # One actual object links the opening, transformations, baseline and metric.
    find('goes-window').update(body=graphic('window'), clicks=2,
        notes='Set the clock to 01:00 UTC on February 1. Reveal the 01:30 target, then persistence. All numerical values are from the immutable teaching dataset, extracted without training. Ask which number a forecasting program is allowed to use at 01:00. The answer is the observation, not the later target.')
    find('goes-actual-window').update(title='Read the arrays for that same forecast', body=code(
        'example = splits["train"]\ni = 1  # Forecast origin: 2014-02-01T01:00 UTC\nx = example["x"][i]          # shape (2, 60)\ny = example["y"][i]          # shape (1,)\nlatest = example["persistence"][i]  # shape (1,)', '1-2|3|4-5|all')+note('The dictionary keeps the inputs, target, timestamp and persistence forecast aligned.'),
        notes='A NumPy array stores numbers with named positions, not timestamp metadata in every entry. The shared index identifies the same forecast across x, y, ids and persistence. Channel zero is XRSA; channel one is XRSB. The final axis runs from the oldest to the latest minute. The persistence array preserves log-flux units before input standardization. This is a read-only excerpt; use the notebook window selector to inspect it.')
    insert('chronology',[slide('window-validity','Keep the whole example inside one date split',graphic('validity'),
        'Reveal one invalid cross-boundary window and then one gap. load_goes checks every one-minute interval from the first history sample through the target, including the forecast horizon. It rejects windows crossing a date partition. Randomly shuffling overlapping windows across train and test would let nearly identical histories occur on both sides. The workshop uses chronological partitions, but adjacent accepted windows still overlap within a partition.',
        'Forecast-window eligibility and chronological leakage',2)])
    # Fold the old standalone gaps statement into the concrete boundary explanation.
    slides.remove(find('gaps'))
    for key,mode,stages in [('goes-normalization','normalization',4),('goes-mlp','mlp',4),('goes-cnn','cnn',4),('training-step','training',4),('loss','loss',3),('freeze','inference',4)]:
        row=find(key);row['body']=row['body'].replace(f'<SolarComputation mode="{mode}" />',f'<SolarComputation mode="{mode}" :reveal="Math.min($clicks + 1, {stages})" />');row['clicks']=stages-1
        row['notes']+=' Reveal one operation at a time. Ask what changed before advancing. Back restores the previous state.'
    find('image-score')['body'] = find('image-score')['body'].replace('<SolarMechanism mode="mask" />', '<SolarMechanism mode="mask" :reveal="Math.min($clicks + 1, 4)" />')
    find('image-score')['clicks'] = 3
    norm=code('log_flux = np.log10(raw_flux)\nmodel_input = (log_flux - training_mean) / training_std\n# Target and persistence remain in log10 XRS-B units.', '1|2|3|all')
    norm+=f'<table class="clean-table teaching-values"><tr><th>01:00 XRS-B observation</th><th>Value</th></tr><tr><td>Raw flux</td><td>{window["raw_flux"]:.6g} W/m²</td></tr><tr><td>log10 flux</td><td>{window["latest_log10"]:.6f}</td></tr><tr><td>Training mean / standard deviation</td><td>{window["mean_xrsb"]:.6f} / {window["std_xrsb"]:.6f}</td></tr><tr><td>Standardized input</td><td>{window["standardized_latest"]:.6f}</td></tr></table>'
    insert('goes-normalization',[slide('normalization-values','Calculate the value the model receives',norm,
        'These numbers come from the same 01:00 window. Subtract the XRS-B training mean and divide by the training standard deviation to obtain minus 0.233211. The different number is a change of units, not a different observation. Both channels get their own training-derived statistics. Learners should reproduce the value using the notebook table and its normalization checkbox. The baseline must return minus 5.534128, not minus 0.233211. Rounded displayed values may differ in their last digit from full-precision calculations.',
        'Input standardization versus target units',source=['src/forge_workshop_kit/solar.py:load_goes','decks/solar/data/teaching-window.json'])])
    insert('metric',[slide('actual-baseline-error','Score the forecast we just made',
        f'<div class="teaching-equation"><p>At 01:00, predict <strong>{window["latest_log10"]:.6f}</strong>.</p><p>At 01:30, the observed target is <strong>{window["target_log10"]:.6f}</strong>.</p><p class="mono">|prediction − target| = {abs(window["latest_log10"]-window["target_log10"]):.6f}</p></div>'+note('One window’s absolute error, in log10 flux units. The reported MAE averages all accepted windows.'),
        'This particular forecast misses a rise in flux. Persistence can work well on slowly changing periods and miss rapid changes. Do not infer the mean from this one example. The existing arithmetic slide shows how individual errors are averaged. A log10 error of about 0.59 corresponds to a ratio near four, not a 59 percent error.',
        'One real error versus mean error',source=['decks/solar/data/teaching-window.json','src/forge_workshop_kit/solar.py:errors'])])

    # Replace repeated storage overviews with one execution, its outputs and restore path.
    for key in ['program','source','record','image-stack']:
        slides.remove(find(key))
    find('stage')['body']=code('with session.stage(name, config=config,\n    sources={"candidate.py": source},\n    inputs={"dataset": dataset_version}) as stage:\n    if stage.needs_run:\n        result, predictions = training.train(...)\n        stage.record(result, files=output_files)', '1-3|4-5|6|all')+note('Shortened from run_training. The saved files include source, weights, predictions and losses.')
    find('stage')['notes']='Find the full editable run_training function in the notebook. The stage identifies a request to train specific source with specific settings and data. Its completed result is reused only for that matching request. training.train runs the program and returns predictions. stage.record stores its result and output files. Publication follows execution; an upload failure does not erase training or require training again. The ellipsis abbreviates arguments in this teaching excerpt; it is not a paste-ready function.'
    insert('training-step',[slide('gradient-arithmetic','Use the error to decide which way a weight should move',graphic('gradient'),
        'Use a one-weight model to explain the derivative before showing PyTorch. With x equal two and target three, loss is (2w minus three) squared. At w equal one, its derivative is minus four. A simple gradient-descent step subtracts learning rate times gradient. The displayed update uses 0.1 and gives w equal 1.4. This is arithmetic, not a logged workshop result. Our real model uses Adam, which also maintains estimates of gradient moments. Do not describe this example as an exact Adam update.',
        'Loss, gradient and parameter update',2, ['decks/solar/components/SolarConcept.vue','examples/solar/candidate.py']),
        slide('optimizer-code','Separate prediction, gradients and the optimizer step',code(
        'prediction = model(batch_x)\nloss = training_loss(prediction, batch_y, mask)\noptimizer.zero_grad()\nloss.backward()\noptimizer.step()', '1-2|3|4|5|all')+note('A forward pass returns predictions. Only the optimizer step changes model parameters.'),
        'zero_grad clears accumulated gradients; PyTorch adds new gradients unless we clear them. The forward pass creates predictions and records the operations needed for differentiation. backward computes derivatives of the loss with respect to trainable parameters. step applies the optimizer update. The workshop loops over a fixed number of optimizer steps, not a promised number of full dataset epochs. Training sample order and initialization depend on the seed. Learners edit training_loss; they can inspect the surrounding fit function.',
        'The mechanics of one optimizer step',source=['examples/solar/candidate.py']),
        slide('validation-code','Validation measures the current weights without fitting them',code(
        'model.eval()\nwith torch.no_grad():\n    prediction = model(validation_x)\nerror = fixed_score(prediction, validation_y)', '1|2-3|4|all')+note('eval() changes layer behavior; no_grad() stops gradient recording. Neither call selects a model.'),
        'eval disables training-specific behavior such as dropout if a candidate uses it. no_grad prevents autograd from retaining a differentiation graph. Our current small models do not need dropout to illustrate the distinction. The fixed parent scorer compares predictions to validation targets. Participants choose a configuration using validation; the optimizer itself never updates from these validation targets in this workshop. This is an explanatory excerpt of the scoring boundary, not the exact function signature.',
        'Training updates versus validation selection',source=['src/forge_workshop_kit/training.py'])])
    insert('tracking-turn',[slide('break-one','Take a fifteen-minute break',
        '<p>Your draft loss and metric should be saved. Check that completed results remain visible after navigating away and back.</p><p>After the break, we’ll follow a batch through the two forecasting models.</p>',
        'Use minutes 95 through 110. Do not start a new training run during the break. A pending publication can be retried from saved results later.', 'Saved work and pacing')])
    insert('search-levels',[slide('batch-shapes','Read the batch, channel and time axes',graphic('batch'),
        'B counts windows processed together. Each window has two instrument channels and sixty time positions. The target has one value per window. The training configuration uses batch size thirty-two. The notebook free shape demonstration uses batch size two and width four so learners can inspect a small forward pass; it does not train and does not change later random state. Ask learners to explain x[0,1,-1] before revealing the output shape.',
        'NumPy/PyTorch tensor axes and batch semantics',2, ['src/forge_workshop_kit/solar.py:load_goes','src/forge_workshop_kit/solar_views.py:forward_shapes']),
        slide('batch-indexing','Index one value, then keep the batch shape',code(
        'x.shape             # (B, 2, 60)\nx[0, 1, -1]         # latest XRS-B input in window 0\nx[:, 1, -1:]        # latest XRS-B input, shape (B, 1)\nmodel(x).shape      # (B, 1)', '1|2|3|4|all')+note('The values in x are standardized. This indexing exercise does not define a persistence forecast.'),
        'Explain colon as selecting every item and negative one as the final position. Using -1 removes the last axis; -1: preserves it as length one. Shape-compatible subtraction matters: (B,1) minus (B,) can broadcast to a B by B matrix and silently score the wrong pairs. Both predictions and targets should remain B by one. Ask experienced participants to demonstrate that broadcasting issue with a small local NumPy array; no training is needed.',
        'Indexing, dimensions and accidental broadcasting',source=['src/forge_workshop_kit/solar.py','src/forge_workshop_kit/solar_teaching.py:check_flux_metric'])])
    insert('goes-mlp',[slide('one-neuron','Calculate one hidden unit before adding the whole layer',graphic('neuron'),
        'The arithmetic uses three values for legibility. The real MLP flattens 120 values. A Linear layer gives every hidden unit one learned weight per input plus a bias. ReLU retains positive values and sets negative values to zero. A second Linear layer combines hidden outputs into one forecast. With no nonlinear activation between linear layers, their composition would still be one affine transformation. The example illustrates the operation; it is not a neuron from a trained checkpoint.',
        'Affine layer, bias and ReLU',2)])
    insert('goes-cnn',[slide('convolution-weights','Reuse one filter at each time position',graphic('filter'),
        'One Conv1d output channel uses a five-position filter for each of the two input channels, sums ten products and adds its bias. Slide the highlighted window once while retaining the same weights. Multiple output channels learn different filters. Padding two preserves the time dimension at sixty. Average pooling then discards the time-position axis. That is a modeling assumption, not merely a shape trick: the network summarizes local features across the hour. The MLP gives distinct weights to each time position.',
        'Convolution weight sharing and temporal pooling',2),
        slide('parameter-code','Choose settings separately from the weights being learned',code(
        'config = {"architecture": "cnn", "width": 16,\n          "learning_rate": 0.001, "steps": 60, "seed": 17}\nmodel = build_model((2, 60), config)\noptimizer = torch.optim.Adam(model.parameters(),\n                             lr=config["learning_rate"])', '1-2|3|4-5|all')+note('Width and learning rate are settings. The weights and biases inside model.parameters() are trained.'),
        'The six Sweep configurations are predefined; the required exercise is a bounded comparison, not an adaptive search algorithm. Architecture chooses an existing implementation. Width changes its number of hidden features. Learning rate scales updates. Steps fixes the update budget. Seed controls initialization and sampling. None of these is itself a learned model weight. All comparisons must record the settings because a favorable score does not tell us which choices produced it.',
        'Parameters, hyperparameters and architecture choice',source=['examples/solar/candidate.py','scripts/solar_cells.py'])])
    slides.remove(find('break'))

    insert('persistence-image',[slide('image-units','Put image inputs and targets in the same units',
        code('logged = np.log1p(pixel_rate)\nnormalized = (logged - training_center) / training_scale\n# Apply the same transform to inputs and future targets.', '1|2|3|all')+
        '<p>AIA arrays use exposure-normalized intensity. The loader fits its center and scale using training pixels inside the disk.</p>'+note('GOES targets stayed in log-flux units. Image targets are standardized along with image inputs.'),
        'This difference deserves explicit attention. The prepared AIA images are exposure-normalized rates. log1p reduces the dynamic range while accepting zero. The loader computes center and scale over on-disk training pixels, then uses the same transform for all frames and targets. Negative normalized values are possible; they do not mean negative observed light. Display colors encode intensity and are not the three input channels of an RGB model. The model receives two grayscale frames as channels.',
        'AIA intensity transformation and units',source=['scripts/prepare_solar.py','src/forge_workshop_kit/solar.py:load_aia']),
        slide('image-batch','Keep the two image times in separate channels',graphic('image'),
        'Use the same earlier and current observations already displayed. The input is B by two by sixty-four by sixty-four. The output is B by one by sixty-four by sixty-four. x[:,1:2] selects the current image while retaining the channel dimension. x[:,1] would drop it and can broadcast incorrectly. The image diagram is a shape illustration; the preceding slide supplies actual solar observations.',
        'Image tensor axes and residual addition',2)])
    insert('image-score-code',[slide('equal-image-average','Give each forecast image one score',graphic('averaging'),
        'This is the exact arithmetic of the public scorer fixture with error set to one and inside selected. The first image includes one pixel with error one. The second includes four pixels with error two, so its sum is eight but its per-image MAE is two. Average one and two to obtain 1.5. Pooling all pixels gives 1.8 and changes the weighting. In the notebook, move the error outside the mask and run Try my image scorer on these pixels; the score becomes zero. Missing predictions do not become a zero score.',
        'Masked reduction, axes and equal-image weighting',2, ['src/forge_workshop_kit/solar_views.py:scorer_fixture','src/forge_workshop_kit/solar.py:errors'])])
    insert('image-turn',[slide('meal-break','Pause for thirty minutes before the research-agent exercise',
        '<p>Keep the image comparison open at one timestamp. Save the draft you trained and the observation you want the agent to investigate.</p><p>After the break, we’ll give the agent the code and validation evidence behind that result.</p>',
        'Use minutes 200 through 230 for the meal break. Completed work should already be saved. Do not ask people to leave an unreviewed paid action running during the break.', 'Saved comparison and pacing')])
    insert('boundaries',[slide('agent-context','Give each program only the data it needs',graphic('context'),
        'Separate three programs. The language model receives selected source and validation evidence and proposes code. Reviewed training code receives training arrays and fits the forecasting network. The parent scorer receives validation predictions and targets. The research agent can inspect validation evidence, but final-test scores and dates stay outside its improvement request. File access is scoped by the workshop; reviewed subprocess execution is not a security sandbox. These arrows describe data flow, not a guarantee that an arbitrary untrusted program is safe.',
        'Research-agent context versus training and scoring data',2, ['src/forge_workshop_kit/research.py','scripts/solar_cells.py','src/forge_workshop_kit/training.py']),
        slide('research-tool-result','Gather validation evidence before requesting a proposal',code(
        '_, observed = event("read_validation_evidence",\n                    {"execution": evidence["stage_id"]},\n                    read_validation)\nprompt = {"mission": "Propose two competing code changes...",\n          "source": source, "evidence": allowed}\n# validated_json sends this prompt in the model request.', '1-3|4-5|6|all')+note('Shortened from research.propose(). The notebook chooses and runs the evidence-read operation.'),
        'The notebook reads the selected validation execution before asking the model for proposals. read_validation returns the saved configuration, metrics and source fingerprint; event records that operation for Agent Lens. The request is built separately from the current source and the allowed evidence dictionary. It does not send prediction arrays or images, and the model does not choose this evidence-read call. Open the recorded operation to find its config and metrics, then open the model request to inspect source and evidence. A separate reviewed training action tests each proposed program.',
        'Notebook evidence gathering and the model proposal request',source=['src/forge_workshop_kit/research.py:propose','scripts/solar_cells.py'])])
    insert('native-diff',[slide('loss-change-effect','The loss edit changes which errors receive larger gradients',
        '<table class="clean-table"><tr><th>Illustrative absolute error</th><th>Squared loss</th><th>Absolute loss</th></tr><tr><td>0.1</td><td>0.01</td><td>0.1</td></tr><tr><td>1.0</td><td>1.0</td><td>1.0</td></tr><tr><td>3.0</td><td>9.0</td><td>3.0</td></tr></table>'+note('The evaluation metric stays masked absolute error. Only the training objective changes.'),
        'Squared error grows quadratically, and its gradient magnitude grows with the error. Absolute error grows linearly and has constant magnitude away from zero. Matching the objective to the final metric is a plausible hypothesis, not a guarantee of better generalization. The model may trade large localized errors against smaller widespread errors. Inspect the actual validation forecasts after testing. These three arithmetic values are illustrations, not measured solar residuals.',
        'Training-objective consequences and a testable hypothesis')])
    insert('test-composed',[slide('composition-versus-adoption','Test the recommendation before carrying it forward',graphic('selection'),
        'The agent chooses or combines source changes after reviewing probes. That is one decision. The notebook trains that proposed source and applies the strict validation-error rule. That is another decision. Equal, worse or failed results keep the earlier version. A KEEP composition may train unchanged source again; it is an additional execution without an invented code change. The branch panel should expose the actual source and execution attached to each node.',
        'Proposal, tested composition and deterministic adoption',2)])
    # Bring the actual second edit into the main explanation instead of leaving its mechanism in an appendix.
    for key in ['recorded-code','zero-head']:
        row=find(key);slides.remove(row);slides.insert(index('repeat'),row)
    insert('zero-head',[slide('zero-head-gradients','Zeroing the last layer still allows learning',
        code('features = earlier_layers(x)\ncorrection = output_layer(features)  # starts at zero\nforecast = current_image + correction\n# First update: output-layer weights can change.\n# Later updates: gradients also reach earlier layers.', '1-3|4|5|all')+note('Earlier layers retain their normal initialization. The recorded edit does not zero every parameter.'),
        'At initialization the final layer weights are zero, so its output correction is zero. The output weights still receive gradients because their derivative depends on the preceding features. For the first backward pass the zero output weights block gradients to preceding layers; after the output weights move, gradients can flow farther back. This explains why a zero residual head is compatible with learning. Do not teach zero initialization of every hidden layer as an equivalent change.',
        'Residual initialization and gradient flow',source=['decks/solar/public/recorded-study.json'])])
    insert('branch-inspect',[slide('break-two','Take ten minutes before opening the final dates',
        '<p>Finish the current action and save the selected version. Do not make another code choice from the final comparison.</p><p>We’ll load the saved weights when we return.</p>',
        'Use minutes 310 through 320. If a run is still incomplete, keep its status visible. Use the labeled recorded case for discussion rather than assigning its outcome to the learner edit.', 'Freeze and pacing')])
    insert('qualified-images',[slide('repeatability','Separate repeated forecasts from repeated experiments',
        '<div class="teaching-equation"><p><strong>199 windows</strong> reuse observations across two dates.</p><p><strong>Three seeds</strong> repeat fixed training recipes with different initialization and sampling.</p><p><strong>One agent discovery</strong> produced the edits we repeated.</p></div>'+note('Neither count establishes performance across different solar periods or independent research-agent searches.'),
        'Overlapping windows are not independent solar events. The three-seed qualification tests fixed source, not three agents independently discovering the same edit. Seed seventeen and twenty-nine improve, while seed forty-three slightly regresses. The mean improvement and that regression both belong in the conclusion. A next study could predeclare different dates, more training seeds and independent agent adaptations, but this workshop does not run that study.',
        'Units of repetition and the limit of the measured improvement',source=['docs/solar-qualification.md','decks/solar/public/qualification-summary.json'])])
    # Replace prose/arithmetic-only explanations with the intermediate values drawn
    # beside the two source lines responsible. These views never execute training.
    worked = {
        'normalization-values': ('normalize',
            'logged = np.log10(raw_flux)\nmodel_input = (logged - training_mean) / training_std',
            'The target and persistence prediction stay in log-flux units.'),
        'actual-baseline-error': ('error',
            'prediction = split["persistence"]\nabsolute_errors = np.abs(prediction - split["y"])',
            'This is one real window. Average all accepted windows to report MAE.'),
        'batch-indexing': ('alignment',
            'assert prediction.shape == target.shape == (batch_size, 1)\nabsolute_errors = np.abs(prediction - target)',
            'Illustrative values. Preserve the last axis with x[:, 1, -1:].'),
        'validation-code': ('validation',
            'model.eval()\nwith torch.no_grad(): prediction = model(validation_x)',
            'No optimizer step. Validation measures the weights produced by training.'),
        'loss-change-effect': ('loss',
            'squared_loss = ((prediction - target).square() * mask).sum() / mask.sum()\nabsolute_loss = ((prediction - target).abs() * mask).sum() / mask.sum()',
            'The recorded edit changes the masked training objective; the fixed scorer does not change.'),
        'zero-head-gradients': ('zero',
            'nn.init.zeros_(self.net[-1].weight)\nnn.init.zeros_(self.net[-1].bias)',
            'The earlier layers keep their normal initialization. Do not zero the entire network.'),
        'repeatability': ('repetition', '',
            '199 overlapping windows on the same two dates; three seeds repeat fixed recipes, not agent discovery.'),
        'configs': ('search', '',
            'The 60-update comparison is a short teaching run, not a claim about the best architecture.'),
    }
    for key, (mode, excerpt, caption) in worked.items():
        row = find(key)
        row['body'] = f'<SolarWorked mode="{mode}" :reveal="Math.min($clicks + 1, 3)" />\n\n'
        if excerpt:
            row['body'] += code(excerpt)
        row['body'] += note(caption)
        row['clicks'] = 2
        row['kind'] = 'worked-visual'
        row['notes'] += ' Keep the graphic visible while reading the two-line excerpt. Advance to reveal the next quantity; Back restores the earlier explanation. Diagrams are explanatory and do not execute code.'
        row.setdefault('source', []).append('decks/solar/components/SolarWorked.vue')
    find('batch-indexing')['title'] = 'Keep each prediction paired with its own target'
    find('repeatability')['title'] = 'The same image edit helped two seeds and hurt one'
    find('schedule').update(title='Six-hour session with three breaks',body='<table class="clean-table schedule"><tr><th>Minutes</th><th>Work</th></tr>'+''.join(f'<tr><td>{a}–{b}</td><td>{title}</td></tr>' for _,title,a,b,_ in SCHEDULE)+'</table>',notes='One six-hour session for a mixed room. The schedule includes fifty-five minutes of breaks. Keep introductory arithmetic beside implementation; experienced participants use the shape, broadcasting and metric checks to inspect assumptions. No extra training or paid research round has been added.')
    find('schedule')['kind']='schedule-reference'

    # Metadata is owned by the authored sequence, rather than inferred from rendered screenshots.
    exercise={
        'setup-turn':('setup','instrument_tool','Check my tracing code','Send my first Agent Lens trace'),
        'data-turn':('data','load_goes / load_aia','','Load the solar dataset'),
        'persistence-turn':('baseline','persistence_forecast','Check my persistence function','Run my persistence baseline'),
        'tracking-turn':('search','training_loss / my_flux_mae','Check my measurement code',''),
        'search-turn':('search','build_model / run_training','Run one forward pass and show tensor shapes','Run six tracked configurations'),
        'goes-repair-turn':('search','FluxPredictor.forward / fit','Check the GOES repair code','Train the worked GOES repair'),
        'image-turn':('images','ImagePredictor.forward / training_loss / my_image_mae','Check my image code','Compare convolutional and residual predictors'),
        'evidence-turn':('research','select_validation_evidence','Check my evidence selection','Round 1: Propose two code changes'),
        'round1-turn':('research','next_research_action / choose_adoption','','Round 1: current action'),
        'round2-turn':('research','next_research_action / choose_adoption','','Round 2: current action'),
        'final-turn':('final','research.freeze / training.train(weights=...)','','Freeze versions and evaluate reserved dates'),
        'conclusion-turn':('final','publish_report','','Publish my conclusion'),
    }
    section_starts={key:(section,title,start,end) for section,title,start,end,key in SCHEDULE}
    section=None; main=[]
    for row in slides:
        if row['key']=='reference': break
        if row['key'] in section_starts: section=section_starts[row['key']]
        row['_section']=section;main.append(row)
    for section_id,title,start,end,_ in SCHEDULE:
        members=[r for r in main if r['_section'][0]==section_id]
        weights=[6 if r['kind']=='exercise' else 1 for r in members]
        total=sum(weights); elapsed=float(start)
        for row,weight in zip(members,weights):
            duration=(end-start)*weight/total
            row['timing']={'section':section_id,'section_title':title,'start_minute':round(elapsed,2),'duration_minutes':round(duration,2),'section_start':start,'section_end':end}
            row['time']=f'{start//60}:{start%60:02}–{end//60}:{end%60:02}'
            row['notes']+=' Session block: '+title+f' (minutes {start}–{end}).'
            elapsed+=duration
    for row in slides:
        row.pop('_section',None)
        row.setdefault('concept',row['title'].replace('<br>',' '))
        row.setdefault('source',['scripts/solar_cells.py','src/forge_workshop_kit/solar.py'])
        if 'recorded' in row['key'] or 'qualified' in row['key'] or row['key'] in ['native-lens','native-diff','native-training','native-forecast','zero-head','repeatability']:
            row.setdefault('evidence',{'type':'recorded','records':['decks/solar/public/recorded-study.json','docs/solar-qualification.md']})
        else:
            row.setdefault('evidence',{'type':'exercise' if row['kind']=='exercise' else 'explanation','records':[]})
        if row['key'] in exercise:
            step,function,check,run=exercise[row['key']]
            row['exercise']={'step':step,'function':function,'check':check,'run':run}
        else: row.setdefault('exercise',None)
        row.setdefault('timing',{'section':'reference','start_minute':None,'duration_minutes':0})
        row.setdefault('clicks',0)
    return slides,len(main)
