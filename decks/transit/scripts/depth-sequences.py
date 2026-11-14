"""Six-hour teaching sequence. Called by build-storyboard.py; no experiments run."""

SCHEDULE = [
    ('00:00', '00:30', 'Understand the rider, source data and service day'),
    ('00:30', '00:50', 'Connect to Forge and write an acceptance scenario'),
    ('00:50', '01:35', 'Build and inspect the single-worker loop'),
    ('01:35', '01:45', 'Break'),
    ('01:45', '02:25', 'Implement task readiness, claims and isolated copies'),
    ('02:25', '03:00', 'Run two workers and test their patches together'),
    ('03:00', '03:20', 'Break'),
    ('03:20', '04:00', 'Review a project lesson and implement retrieval'),
    ('04:00', '04:45', 'Run and inspect the matched follow-up builds'),
    ('04:45', '04:55', 'Break'),
    ('04:55', '05:30', 'Evaluate frozen builds and diagnose the UTC defect'),
    ('05:30', '06:00', 'Reproduce a result and publish the release decision'),
]

TIMES = {
 'Build a transit app<br>with a team of coding agents':'0:00',
 'Your team needs a departures board':'0:02','Here is the application we want to deliver':'0:05',
 'The inputs are public transit records':'0:08','The last train can belong to yesterday’s service':'0:17',
 'Turn the brief into checks':'0:24','A software factory needs a way to finish work':'0:26',
 'Add the task board and two workers':'0:28','Your project contains the experiment':'0:30',
 'Connect and inspect the source data':'0:33','Write the after-midnight acceptance check':'0:42',
 'One worker still needs a complete loop':'0:50','Give the worker the task it is allowed to solve':'0:53',
 'Return the tool result to the worker':'1:05','Run one worker before adding a team':'1:13',
 'A trace should answer what changed and why':'1:23','Inspect the worker’s test in Agent Lens':'1:27',
 'Choose work that can happen independently':'1:45','Ready means its prerequisites passed':'1:50',
 'Make dependencies control the workers':'2:05','Separate working copies protect unfinished changes':'2:15',
 'Run the ready tasks with two workers':'2:25','Read the timeline as work and waiting':'2:35',
 'Save the checkpoint before the break':'2:40','Review a patch before it enters the product':'2:42',
 'Test the combined departures board':'2:45','An integration error can cross a correct boundary':'2:53',
 'Shared memory needs something worth sharing':'3:20','Check the lesson before another agent relies on it':'3:23',
 'Write a rule with a test attached':'3:26','Save a lesson supported by an execution':'3:40',
 'Inspect the memory read, then its effect':'3:50','Find the last direct train between two stops':'4:00',
 'Run both versions of the follow-up feature':'4:10','The factory has two kinds of state':'4:27',
 'Evaluate the product and the process separately':'4:55','A scenario is an input and an expected behavior':'4:58',
 'Compare the frozen builds on matching cases':'5:03','Read one comparison row before the average':'5:08',
 'Compare the same departures in Forge':'5:10','The faster build missed two final cases':'5:13',
 'A timezone assumption selected the wrong train':'5:16','More workers can still produce more waiting':'5:25',
 'Choose a release using the saved checks':'5:30','Publish the version you can reproduce':'5:35',
 'Explain one result to another participant':'5:48','Take the coordination code to your own project':'5:58',
}

SRC = {
 'data':'src/forge_workshop_kit/assets/transit/manifest.json; src/forge_workshop_kit/transit.py',
 'worker':'src/forge_workshop_kit/factory.py:run_worker; src/forge_workshop_kit/factory_teaching.py:EXERCISES.worker',
 'tasks':'src/forge_workshop_kit/factory.py:TaskBoard.claim; src/forge_workshop_kit/transit.py:qualify_coordination_repair',
 'memory':'src/forge_workshop_kit/transit_workshop.py:accept_lesson; src/forge_workshop_kit/factory.py:TaskBoard.memories',
 'eval':'src/forge_workshop_kit/transit.py:evaluate; src/forge_workshop_kit/transit_workshop.py:evaluate_builds',
 'ui':'scripts/transit_cells.py',
}


def deepen(slides):
    def node(title, body, notes, time, *, name='', kind='', concept='', exercise=None, source=None, evidence=None):
        return dict(title=title,body=body,notes=notes,time=time,kind=kind,name=name,clicks=None,
                    concept=concept or title,exercise=exercise,source=source or SRC['ui'],evidence=evidence or [])
    def sequence(title, mode, stage, caption, notes, time, source, evidence=None):
        return node(title,f'<TransitMechanism mode="{mode}" :stage="{stage}"/><p class="caption">{caption}</p>',
                    notes,time,source=source,evidence=evidence)
    def code(title, snippet, explanation, notes, time, *, source, name=''):
        return node(title,'```python\n'+snippet+'\n```\n<p class="caption">'+explanation+'</p>',notes,time,source=source,name=name)
    def insert_after(title, additions):
        index=next(i for i,item in enumerate(slides) if item['title']==title)
        slides[index+1:index+1]=additions
    def get(title):
        return next(item for item in slides if item['title']==title)
    for item in slides:
        item['time']=TIMES.get(item['title'],item['time'])
        item.setdefault('concept',item['title'].replace('<br>',' '))
        item.setdefault('source',SRC['ui'])
        item.setdefault('evidence',[])
        item.setdefault('exercise',None)
    slides[0]['body']=slides[0]['body'].replace('Four hours','Six hours')
    slides[0]['notes']+=' The single session includes three breaks. The extra time is for tracing one concrete input through the implementation, writing the coordinator and explaining the recorded failures.'

    get('One worker still needs a complete loop')['body']=get('One worker still needs a complete loop')['body'].replace('The worker stops with a patch and test evidence.','A completed worker submits a patch and test evidence.')
    get('Connect and inspect the source data')['exercise']={'step':'setup','functions':['instrument_tool'],'prerequisites':['Own writable Forge project'],'run':'Connect and restore my work','inspect':'Send my first Agent Lens trace'}
    get('Run the ready tasks with two workers')['exercise']={'step':'team','functions':['ready_tasks','claim_task'],'prerequisites':['Check my after-midnight scenario','Check my build_worker_request code','Check my ready_tasks code'],'run':'Run the ready tasks with two workers'}
    insert_after('Add the task board and two workers',[
        node('Two workers means two contexts around the same model',
            '<div class="two-col"><div class="ticket"><small>Query worker</small>Task: return departure records<p>Own conversation, assigned file and checks.</p></div><div class="ticket"><small>Presentation worker</small>Task: render those records<p>Own conversation, assigned file and checks.</p></div></div><p>The model weights stay fixed. The coordinator changes which task and evidence each request receives.</p>',
            'The worker is a Python loop plus model requests and allowed tools. Two workers do not mean training two new models. Model settings match across the sequential and parallel builds. The comparison asks what the coordination design changes for this task.', '0:29',source=SRC['worker']),
    ])
    insert_after('The inputs are public transit records',[
        sequence('Start with the row for the platform', 'service-day',0,
            'The stop-time row identifies the trip and platform. It does not contain the date on which that trip runs.',
            'Keep the same trip visible through the next three slides. Read the actual identifiers aloud once. The product uses these joins, not an LLM guess about the next train. Ask which table must tell us whether this trip runs on Thanksgiving. Timeline spacing is illustrative; timestamps are actual.', '0:10',SRC['data'],['MBTA archive 20241128: trip 63926435, stop 70076']),
        sequence('Join the trip to its service calendar', 'service-day',1,
            'Trip 63926435 refers to ThanksgivingDay service. The date under consideration is November 28.',
            'The service ID is a join key. The active dates come from the calendar and exception records. Explain that calendar_dates overrides the weekly rule. This is a historical snapshot and fixed test date, not today’s schedule.', '0:13',SRC['data'],['GTFS service_id and calendar_dates']),
        sequence('Keep the service date and boarding date', 'service-day',2,
            'This train belongs to November 28 service and departs on November 29. The result needs both facts.',
            'Ask the room to name the two different dates before revealing the timestamp. The train is eight minutes after the next midnight. Explain why hour modulo 24 without carrying the day loses information.', '0:15',SRC['data'],['2024-11-29T00:08:00-05:00']),
    ])
    insert_after('The last train can belong to yesterday’s service',[
        code('Convert elapsed service time into a timestamp',
            'from datetime import datetime, timedelta\nfrom zoneinfo import ZoneInfo\n\norigin = datetime(2024, 11, 28, tzinfo=ZoneInfo("America/New_York"))\ndeparture = origin + timedelta(hours=24, minutes=8)\nassert departure.isoformat() == "2024-11-29T00:08:00-05:00"',
            'Walkthrough for this retained record. Keep service_date="2024-11-28" beside the converted timestamp.',
            'Explain the datetime origin, timezone and timedelta separately. This example has no daylight-saving transition; it does not replace the full GTFS time specification. The learners write the acceptance check, while the coding worker implements the general query.', '0:20',source=SRC['data']),
        node('Check the joined behavior, not just the parser',
            '<div class="three-checks"><div><b>Input</b><p>Park Street<br>Nov 29 at 00:05 Eastern</p></div><div><b>Required row</b><p>Trip 63926435<br>Departs 00:08 Eastern</p></div><div><b>Required dates</b><p>Service: Nov 28<br>Boarding: Nov 29</p></div></div><p>Now remove that train, or change its service date. Your check should reject either result.</p>',
            'These deliberate mutations test the participant’s assertion. They are local examples, not recorded agent mistakes. Explain why a checker that always returns True would pass the first example and fail to teach anything.', '0:23',source=SRC['data']),
    ])
    insert_after('Connect and inspect the source data',[
        code('Record the operation that you just ran',
            'task_id = observation.get(\n    "task_id", observation.get("arguments", {}).get("task_id", "setup")\n)\nwith tracing.Tool(\n    name=observation["name"], arguments=observation["arguments"],\n    result=observation["result"], tool_call_id=observation["id"],\n    started_at=stamp(observation["started_at"]),\n    ended_at=stamp(observation["ended_at"]),\n) as span:\n    span.set_attributes({"factory.task_id": task_id})',
            'Excerpt from instrument_tool(). The same function exports later worker tools. Copy the recorded times; export time is different.',
            'Identify the name, inputs, actual result and time boundaries. Participants add or edit the attribute in the full notebook function and find it in their own setup span. This operation reads the teaching dataset, so it does not spend inference allowance.', '0:38',source=SRC['ui']),
    ])
    insert_after('Give the worker the task it is allowed to solve',[
        sequence('The first action reads the assigned file','worker',0,
            'read_file returns the current text and its SHA256. The next edit must refer to that hash.',
            'This is an explanatory sequence using the implemented tool contract, not an additional live execution. Keep model, Python tool and observation separate. A model choosing read_file is not the same thing as Python executing it.', '0:56',SRC['worker']),
        sequence('The edit includes the version it was based on','worker',1,
            'write_file rejects a path the task does not own, or a file that changed since the read.',
            'Explain optimistic conflict detection: before_sha256 identifies the old file, while the returned hash identifies the new one. A rejected write should produce an observation that the next request can inspect.', '0:59',SRC['worker']),
        sequence('Run the checks against the changed files','worker',2,
            'A passing test for an earlier file does not authorize completion after another edit.',
            'The board clears the old test receipt when a file changes. The current files are what run in a child Python process. That process has restricted imports, a timeout and no inherited Forge credentials; it is reviewed code execution, not a security sandbox.', '1:02',SRC['worker']),
    ])
    insert_after('Return the tool result to the worker',[
        code('Append the actual observation to the next request',
            'result = dispatch_action(action, tools)\nmessages.append({\n    "role": "user",\n    "content": json.dumps({\n        "observation": result,\n        "messages": inbox,\n        "remaining_actions": max_steps - number - 1,\n    }),\n})',
            'Runtime excerpt. The notebook function chooses one allowed tool and must return that tool’s actual result.',
            'The agent action has already been appended as an assistant message. The following user message supplies the observation, any directed messages and remaining action count. The runtime records actual tool execution independently of the learner’s return value. Do not add a second model call here.', '1:07',source=SRC['worker']),
        sequence('Finish submits a patch for review','worker',3,
            'finish requires passing development checks for the current source. It does not release the app.',
            'Point out the status change to review. Human review and integration remain separate. If a worker reaches its action limit without this tested completion, the unfinished file is retained as evidence, not silently merged.', '1:09',SRC['worker']),
    ])
    get('Run one worker before adding a team')['body']=get('Run one worker before adding a team')['body'].replace('Run the first feature and open its model and tool spans.','Click <strong>Check my build_worker_request code</strong>. It also checks your dispatcher. Then run the first feature.').replace('Follow the task request to a real file edit and test result in Agent Lens.','The free check passes; then the actual model request, file edit and test are visible in Agent Lens.')
    get('Run one worker before adding a team')['exercise']={'step':'worker','functions':['build_worker_request','dispatch_action'],'prerequisites':['Check my after-midnight scenario','Check my build_worker_request code'],'run':'Run one worker on the first feature'}
    insert_after('Inspect the worker’s test in Agent Lens',[
        node('The request has a size limit even when files are saved',
            '<div class="context-strip"><span>Task + contract</span><span>Current source</span><span>Lessons</span><span>Observations</span></div><p>The coordinator keeps current source once and replaces superseded copies with hashes. Complete files and raw histories remain saved.</p><p class="caption">Input: serialized messages + 4096 bytes of overhead must fit 32768 bytes. Output: at most 32768 tokens. These are different units.</p>',
            'Explain why storing a complete file is different from resending it with every action. R5 still hit a bound after a long write, so this policy is not a guarantee that any generated module will fit. Do not imply that a higher output allowance fixes an oversized input.', '1:31',source=SRC['worker']),
        node('Break until 1:45','<p class="sub">Keep the saved source, task record and trace. When we return, we’ll decide which tasks can run at the same time.</p><p>Browsing and reopening the notebook do not restart workers.</p>',
            'Ten-minute break, 1:35–1:45. Use the read-only monitor to find participants who requested help. Do not treat missing progress as failure.', '1:35',kind='break'),
    ])
    insert_after('Ready means its prerequisites passed',[
        sequence('Both workers can see a pending task','claim',0,
            'Two separate reads can return pending before either worker writes its name.',
            'Use the local two-thread fixture, not a theoretical timing claim. Ask learners what changes if both read at the same time. A polite prompt does not make two Python operations atomic.', '1:53',SRC['tasks']),
        sequence('A separate check and write permits two owners','claim',1,
            'The free exercise forces both reads before either assignment. Both callers think they claimed the task.',
            'The controlled race uses a barrier to reproduce the condition. This two-owner outcome measures coordination code, not model intelligence. Show the broken if-pending then set-owner snippet in the notebook.', '1:56',SRC['tasks']),
        sequence('One short transaction assigns one owner','claim',2,
            'board.claim checks readiness and assigns the owner while holding the lock. Model work happens after the lock is released.',
            'The same two local threads now have one successful claim. The other gets a not-ready or already-claimed error. Holding the lock for the entire model call would serialize the work and block other claims.', '2:00',SRC['tasks']),
        code('Keep the model call outside the claim transaction',
            'def claim_task(board, task_id, worker_id):\n    return board.claim(task_id, worker_id)\n\n# Inside the supplied board, simplified:\nwith board.transaction() as state:\n    assert task_id in ready_tasks(state["tasks"])\n    state["tasks"][task_id]["status"] = "running"\n    state["tasks"][task_id]["worker_id"] = worker_id',
            'The participant calls the supplied atomic operation. The lower excerpt explains its critical section.',
            'This is simplified teaching code; the actual store raises FactoryStop and also records dispatch identity, source and timing. Do not instruct participants to replace the store with this excerpt. The required code change is claim_task in the notebook.', '2:03',source=SRC['tasks']),
    ])
    get('Make dependencies control the workers')['exercise']={'step':'tasks','functions':['ready_tasks','claim_task'],'prerequisites':['Connect and restore my work'],'run':'Check my ready_tasks code'}
    insert_after('Separate working copies protect unfinished changes',[
        sequence('Each worker starts from the same source','copies',0,
            'Separate directories let both workers inspect the initial interface without overwriting one another.',
            'Separate working files do not imply separate authority to change every file. Keep the common starting version visible. This is diagrammatic code flow, not a claim that all future tasks are independent.', '2:16',SRC['worker']),
        sequence('Each task can edit only its assigned module','copies',1,
            'The query task owns query.py. The presentation task owns presentation.py. Neither can change the trusted grader.',
            'Point out which files are readable and which are editable. Both task contracts name the same return schema. The worker cannot repair a failing test by changing the evaluator.', '2:19',SRC['worker']),
        sequence('Integration checks the patches against their base','copies',2,
            'If a file changed after a patch was prepared, integration reports a conflict instead of silently replacing it.',
            'Explain why different files still need a combined test: both modules can disagree about a field or timezone. The hash guards against stale file replacement; it does not prove the interface is correct.', '2:22',SRC['worker']),
    ])
    checkpoint=get('Save the checkpoint before the break')
    checkpoint.update(title='Find both submitted patches before integration',
        body='<p>In the saved task board, open each task’s diff and development-check result.</p><p>Confirm the task owner, changed file and tested source belong to the same attempt. A failed worker remains visible beside a successful one.</p>',
        notes='This is a checkpoint at 2:40, not a break. Integration starts at 2:45. If one worker is unfinished, keep that outcome and inspect the available record rather than inventing a completed patch.')
    integration=get('Test the combined departures board')
    integration['body']=integration['body'].replace('Accept or reject each patch with a reason.','Check <strong>I reviewed both builds’ patches below and their development checks</strong>.').replace('Run the combined checks and inspect one displayed departure.','Run the combined checks. Then click <strong>Preview this saved app</strong> to inspect a departure.')
    integration['exercise']={'step':'integrate','functions':['check_departures'],'prerequisites':['Both initial builds saved','Review both actual diffs','Review confirmation checkbox'],'run':'Test the combined departures board','inspect':'Preview this saved app'}
    insert_after('An integration error can cross a correct boundary',[
        node('Use the local preview to follow a returned row',
            '<p class="where">Notebook → Test the combined app</p><ol><li>Select <strong>Two builders</strong> or <strong>One builder</strong>.</li><li>Choose Park Street and <code>2024-11-29T00:05:00-05:00</code>.</li><li>Click <strong>Preview this saved app</strong> and find trip 63926435.</li></ol><p class="caption">This executes the reviewed app locally. It makes no model calls.</p>',
            'If a live build is wrong, keep the output visible and name the failed requirement. The prepared reference continuation appears only if neither initial build passes development integration; it is labeled and never replaces live results.', '2:56',source=SRC['ui']),
        node('Break until 3:20','<p class="sub">Save the reviewed builds and their checks. After the break, we’ll decide what a future worker should remember from them.</p>',
            'Twenty-minute break, 3:00–3:20. Resume the same project. Do not change source or model settings to make the live result match the prepared example.', '3:00',kind='break'),
    ])
    insert_after('Write a rule with a test attached',[
        sequence('A saved note is not automatically accepted','memory',0,
            'These four illustrative notes are candidates for the next transit task. Read the status, scope, version and tags.',
            'The examples are illustrative records matching the retrieval schema, not four observations from R5. Ask which one a fresh worker should receive and which fields justify that choice.', '3:29',SRC['memory']),
        sequence('First exclude the unchecked interpretation','memory',1,
            'Only status="accepted" passes the review filter. Saving a proposal does not approve it.',
            'The agent can propose a lesson. The participant checks its evidence and writes the accepted rule. This gate reduces propagation of guesses; it cannot guarantee the rule is correct in every context.', '3:31',SRC['memory']),
        sequence('Then check the applicable contract version','memory',2,
            'version identifies the contract where the rule applies. source_revision identifies the source that supplied its evidence.',
            'Do not compare source_revision to the current code fingerprint. A lesson may be relevant to new code while citing an earlier version. The accepted contract version is the applicability check.', '3:33',SRC['memory']),
        sequence('Finally match the task’s scope and tags','memory',3,
            'The transit service-day task receives the reviewed transit rule. The billing rule remains stored but is not supplied.',
            'select_memories performs these checks. No vector database is needed for this small project record. Let a participant explain why status alone would retrieve too much.', '3:35',SRC['memory']),
    ])
    memory=get('Save a lesson supported by an execution')
    memory['body']=memory['body'].replace('Choose a test or tool event that establishes a project rule.','Click <strong>Check my select_memories code</strong>, then optionally <strong>Ask the agent to propose a lesson</strong>.').replace('Write the rule, its scope and what would invalidate it.','Choose a <strong>Supporting development result</strong>. Write the rule and its limits.').replace('Complete <code>select_memories()</code> so only relevant approved lessons reach the worker.','Click <strong>Save a checked lesson</strong>. Inspect the saved source and evidence.')
    memory['exercise']={'step':'memory','functions':['select_memories'],'prerequisites':['Passing integrated starting build','Check my select_memories code'],'run':'Save a checked lesson','optional':'Ask the agent to propose a lesson'}
    insert_after('Find the last direct train between two stops',[
        sequence('Start both follow-ups from the same release','matched',0,
            'Both teams add last_departure and render_journey. Only one receives the accepted project lesson.',
            'Each build has two workers. The coordinator invokes the two builds in order, while each build may run its two workers concurrently. Do not describe the two conditions as synchronized or simultaneous. Compare saved initial fingerprints.', '4:02',SRC['worker']),
        sequence('Keep both sets of patches and checks','matched',1,
            'Review both outcomes before running the independent comparison. An unsuccessful branch remains part of the result.',
            'The specification, starting code, fixed research model, limits and tool implementation are held the same. The lesson cannot be edited after inspecting the first outcome and still count as a matched pair.', '4:05',SRC['memory']),
        code('The follow-up returns a journey, not a list of guesses',
            'journey = last_departure(\n    tables, origin_id, destination_id, service_date\n)\n# Return one direct trip with departure and arrival timestamps.\n# Return None when no direct service exists in the retained feed.\nhtml = render_journey(journey, title="Last direct train")',
            'Contract excerpt. A valid arrival may occur after midnight. The itinerary download must preserve the returned journey.',
            'Explain the function inputs and two valid output shapes. The retained dataset is small, so None concerns this schedule subset. It is not a statement that no real-world route exists. The renderer cannot invent a trip when the query returns None.', '4:07',source=SRC['data']),
    ])
    follow=get('Run both versions of the follow-up feature')
    follow['exercise']={'step':'followup','functions':['build_worker_request','dispatch_action','ready_tasks','claim_task','select_memories'],'prerequisites':['Checked starting build','Saved accepted lesson','Check my select_memories code'],'run':'Run both versions of the follow-up feature','review':'I reviewed the no-lesson and shared-lesson patches','integrate':'Integrate the reviewed follow-up patches'}
    follow['body']=follow['body'].replace('Run both branches, review their diffs, and inspect their tests.','Run both branches. Read their diffs and check <strong>I reviewed the no-lesson and shared-lesson patches</strong> before integrating.')
    insert_after('The factory has two kinds of state',[
        node('Find where the lesson entered the request',
            '<p>In Agent Lens, open the follow-up query worker. Find its memory-read result, then inspect the next model request.</p><div class="three-checks"><div><b>Retrieved</b><p>Which accepted rule?</p></div><div><b>Supplied</b><p>Which text reached the model?</p></div><div><b>Executed</b><p>Which edit and check followed?</p></div></div><p class="caption">A recorded read establishes consultation. The matched outputs determine what happened to the product.</p>',
            'If no explicit read_memory action is present, distinguish the initial read_shared_memory selection from an agent-initiated read. Do not claim peer messaging unless the saved events contain it. The R5 workers were coordinated through task records and supplied lessons.', '4:32',source=SRC['worker']),
        node('Keep a stopped worker’s files and error',
            '<p>Open the failed task. Inspect the last successful operation, saved source and failed request.</p><p>Retrying publication only exports saved work. Retrying execution is a separate action and can incur cost.</p><p class="caption">After freezing the comparison, preserve its failure. A changed coordinator or limit belongs in a new workspace.</p>',
            'Use Recover stopped work only after confirming the earlier execution stopped. A request with an uncertain outcome remains conservatively charged. A bound error is not fixed merely by clicking again. The six-hour schedule includes time to interpret an incomplete build, not unlimited retries.', '4:38',source=SRC['worker']),
        node('Break until 4:55','<p class="sub">Keep both follow-up outcomes. We will freeze the available versions and compare their actual outputs when we return.</p>',
            'Ten-minute break, 4:45–4:55. Stop adding features. The final comparison must include failed or incomplete branches.', '4:45',kind='break'),
    ])
    get('Evaluate the product and the process separately')['body']=get('Evaluate the product and the process separately')['body'].replace('Duplicate work and blocked time','Repeated task claims and blocked time')
    get('Evaluate the product and the process separately')['notes']+=' Repeated task claims include explicit recovery; overlapping reasoning and semantically duplicated code are not measured. Coverage is separate from passed-case rate.'
    compare=get('Compare the frozen builds on matching cases')
    compare['body']=compare['body'].replace('Complete the development <code>score_scenario()</code> and run its free checks.','Complete <code>score_scenario()</code>. Click <strong>Check my score_scenario code</strong>.')
    compare['exercise']={'step':'evaluate','functions':['score_scenario'],'prerequisites':['All four integrations recorded','Check my score_scenario code'],'run':'Compare the frozen builds','recovery':'Retry saved Forge publications'}
    insert_after('The faster build missed two final cases',[
        node('Open the two failing rows in the final comparison',
            '<div class="native-wide"><a href="https://forge.coreweave.com/wandb/wandb/forge-workshop-kit?nw=dg2ogm6wp3z"><img src="/images/native-comparison-r5-detail.png" alt="R5 native comparison showing one-builder pass rate 1, two-builder 0.8, and the UTC-input rows with different trip IDs"/></a><span class="eval-native-pin" style="left:36%;top:14%">1</span><span class="eval-native-pin" style="left:2%;top:88%">2</span><span class="eval-native-pin" style="left:35%;top:88%">3</span></div><p class="eval-native-caption"><b>1.</b> 10/10 versus 8/10. <b>2.</b> The two UTC-input cases. <b>3.</b> The selected trip differs. Recorded R5, separate from the R4 comparison.</p>',
            'Use the actual saved native view. The bottom two rows show the query and integrated application cases. Both select 63919613 in the solo output and 63919759 in the team output. The screenshot is preserved; numbered annotations sit beside the relevant fields. Capture provenance is in notes/r5-capture-receipt.json.',
            '5:15',source='decks/transit/notes/r5-capture-receipt.json',evidence=['R5 verified native comparison: dg2ogm6wp3z']),
    ])
    insert_after('A timezone assumption selected the wrong train',[
        sequence('Interpret the request as one instant','timezone',0,
            'The R5 final case sends 23:00 UTC. The next departure is 18:03 in the feed’s Eastern timezone.',
            'Recorded R5 case: departures/utc-input. This is a same-instant conversion. The feed clock defines the origin of GTFS elapsed service time; the caller is allowed to express the request using another offset.', '5:18',SRC['eval'],['R5 departures/utc-input: expectedtrip 63919613']),
        sequence('The team used the caller’s clock for service time','timezone',1,
            'The code selected trip 63919759 from service-clock 23:03. It should have selected trip 63919613 at 18:03 Eastern.',
            'Recorded behavior, not a hypothesized defect. The team anchored service-day midnight to the request timezone. This changed the chosen record, not only its formatted text. Inspect the source and actual prediction beside the expected row.', '5:20',SRC['eval'],['R5 expected63919613; actual63919759']),
        sequence('The renderer carried the same wrong trip into the board','timezone',2,
            'departures/utc-input and integrated/departures/utc-input failed for the same reason. Count two failed scenarios and one observed bug.',
            'The independent suite checks both the query and the complete application. Avoid describing these correlated cases as two independent coding errors. Learners should propose a public UTC-input regression case for a future experiment, after retaining the current outcome.', '5:22',SRC['eval'],['R5 two-worker 8/10 final scenarios']),
        sequence('Neither follow-up completed the query change','matched',2,
            'Recorded R5: both scored 12/18. Different request-limit failures prevent a conclusion about a memory benefit.',
            'Without memory: oversized input after a saved write. With memory: output allowance exhausted before a complete first action. Both query tasks stopped before testing. The existing query remained; these outcomes do not establish that shared memory caused either failure.', '5:24',SRC['eval'],['R5 with-memory and without-memory 12/18']),
    ])
    release=get('Publish the version you can reproduce')
    release['body']=release['body'].replace('Complete <code>release_decision()</code> using the required check results.','Complete <code>release_decision()</code> and click <strong>Check my release_decision code</strong>.')
    release['exercise']={'step':'release','functions':['release_decision'],'prerequisites':['Frozen evaluations saved','Check my release_decision code','Written conclusion'],'run':'Publish this release and its evidence'}
    release['notes']='Use the last half-hour for reproduction, release and a short explanation. R5 supports releasing the one-worker departures board. Failed required checks block the follow-up. The output is an artifact and Report, not automatic production deployment.'
    insert_after('Publish the version you can reproduce',[
        node('Reload the selected app and repeat one case',
            '<ol><li>Open the released artifact and identify its source and dataset versions.</li><li>Extract the app bundle and run <code>uv run --with marimo marimo edit app.py</code>.</li><li>Choose the same stop and timestamp. Compare the returned trip ID and dates with the saved case.</li></ol><p class="caption">Use the app from your selected release. The separately labeled reference download is instructor-authored.</p>',
            'This is a local inference-free reproduction. It shows that the delivered source and data yield the saved behavior. It is not a rerun of the stochastic coding agents. Verify one row, not merely that the app opens.', '5:44',source=SRC['ui']),
    ])
    # The worked answers keep symbolic IDs; build-storyboard resolves links after insertion.
    answers=[
      code('Worked answer: check the after-midnight departure',
           'def check_departures(rows):\n    return any(\n        row["trip_id"] == "63926435"\n        and row["service_date"] == "2024-11-28"\n        and row["departure_time"] == "2024-11-29T00:08:00-05:00"\n        for row in rows\n    )',
           '<a href="/acceptance-exercise">Return to the acceptance exercise ↩</a>',
           'Reveal only after an attempt or requested hint. This checks one public scenario; it does not replace the independent final scorer.', '',source=SRC['data'],name='acceptance-answer'),
      code('Worked answer: dispatch one allowed tool',
           'def dispatch_action(action, tools):\n    name = action["action"]\n    if name not in tools:\n        raise ValueError("Unknown builder operation: " + name)\n    return tools[name](action)',
           '<a href="/worker-exercise">Return to the worker exercise ↩</a>',
           'Read action["action"], select the provided callable, invoke it exactly once and return the observation unchanged. The free check rejects an unavailable shell action.', '',source=SRC['worker'],name='worker-answer'),
    ]
    answers.append(code('Worked answer: check the departure order',
        'def score_scenario(actual, expected):\n    return actual == expected\n\nassert score_scenario(["trip-1", "trip-2"], ["trip-1", "trip-2"])\nassert not score_scenario(["trip-2", "trip-1"], ["trip-1", "trip-2"])',
        '<a href="/evaluate-exercise">Return to the comparison exercise ↩</a>',
        'This participant development check tests exact ordered trip IDs. The independent final scorer also checks the other required fields. A missing judgment is not False.', '',source=SRC['eval'],name='evaluate-answer'))
    for answer in answers:
        answer['kind']='answer'
        answer['body']=answer['body'].replace('class="caption"','class="caption source-link"')
    slides.extend(answers)
    acceptance=get('Write the after-midnight acceptance check')
    acceptance.update(name='acceptance-exercise',answer='acceptance-answer',exercise={'step':'setup','functions':['check_departures'],'prerequisites':['Connect and restore my work'],'run':'Check my after-midnight scenario'})
    worker=get('Run one worker before adding a team')
    worker.update(name='worker-exercise',answer='worker-answer')
    compare.update(name='evaluate-exercise',answer='evaluate-answer')
    for item in (acceptance,worker,compare):
        item['body']=f'<a class="answer-link" href="/{item["answer"]}">Worked answer ↗</a>\n'+item['body']
    for item in slides:
        if item['time']:
            hour,minute=map(int,item['time'].split(':'))
            item['elapsed_minutes']=hour*60+minute
        else:
            item['elapsed_minutes']=None
        item['source']=item.get('source') or SRC['ui']
        if not item.get('exercise') and item['kind']=='exercise':
            item['exercise']={'step':'setup' if 'Connect' in item['title'] else 'team','controls':'See exact labels on slide and in authored notebook'}
        if item['title'] in ('The faster build missed two final cases','A timezone assumption selected the wrong train'):
            item['evidence']=['Recorded R5; .workshop/transit-v060-live-r5/journal.json; no new runs']
        if 'R3' in item['notes']: item['evidence'].append('Recorded R3; notes/capture-receipts.json')
        if 'R4' in item['notes']: item['evidence'].append('Recorded R4; notes/capture-receipts.json')
    return SCHEDULE
