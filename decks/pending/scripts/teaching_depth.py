"""Worked mechanisms and four-hour pacing for the current Pending notebook."""


def enrich(slides, code):
    def item(key, title, body, notes, **metadata):
        return dict(key=key, title=title, body=body, notes=notes, cls="", **metadata)

    def before(key, rows):
        index = next(i for i, row in enumerate(slides) if row["key"] == key)
        slides[index:index] = rows

    def replace(key, rows):
        index = next(i for i, row in enumerate(slides) if row["key"] == key)
        slides[index:index + 1] = rows

    slides[:] = [row for row in slides if row["key"] not in ("harness-1", "harness-2")]
    replace("harness-0", [
        item("harness-inputs", "The harness builds the request the model receives.", '<HarnessParts :level="1" />',
             "Point to the system text, tool guide, installed skill names and customer ticket. Ask which item would change if the participant edited instructions. A skill name advertises a procedure; its contents have not yet entered the request."),
        item("harness-execution", "Python executes the action and returns its result.", '<HarnessParts :level="2" />',
             "Keep the request in place. Reveal the selected action and the Python dispatcher. The model produces JSON; the runtime decides which function to call. Follow the returning arrow to my_observation. This is the mechanism we will implement, not a provider-native function-calling example."),
        item("harness-edit-boundary", "Different edits change different parts of the agent.",
             '<table class="clean-table readable-table"><thead><tr><th>Edit</th><th>What execution receives</th></tr></thead><tbody><tr><td>System instructions</td><td>New instructions in the first request</td></tr><tr><td>Verification skill</td><td>New procedure after a read_skill call</td></tr><tr><td>my_invoice_tool</td><td>Different Python behavior or returned records</td></tr><tr><td>my_observation</td><td>Different history in the next request</td></tr><tr><td>verify_before_finish</td><td>A runtime check before accepting completion</td></tr></tbody></table><div class="bottom-note">We implement the tools first, then freeze that code while comparing harness instructions and workflow rules.</div>',
             "Use the table to distinguish behavior changes. The model is fixed; it is not retrained when instructions change. The learner develops tools and the loop before the baseline. The later editor cannot rewrite those frozen functions. Ask whether editing an unused skill can explain a changed outcome.")
    ])
    before("starting", [item("history-not-training", "A tool result changes the next request, not the weights.",
        '<ExecutionBoundaries :level="1" />',
        "Ask a participant to locate the returned payments in the saved next request. This is in-context information available to the next model call. No optimizer or weight update occurs. Reuse this distinction when we introduce the editor.")])
    before("model-span", [item("break-one", "Take ten minutes before investigating the timeout.",
        '<OfficeScene mode="employee" /><div class="bottom-note">1:10–1:20 · Save your draft. Return to the model trace and onboarding tools in step 3.</div>',
        "Save at 70 minutes. The first break occurs after the two starting cases. Leave the project and next step visible. Reopening the notebook does not execute either case again.")])
    replace("onboarding", [
        item("mcp-initialize", "The executor starts a local MCP session.", '<McpSequence :level="1" />',
             "MCP is the interface between this Python client and the onboarding service. Here the service is a local subprocess communicating over stdio. There is no gateway or remote Sandbox requirement. A new action starts a session against the saved office state."),
        item("mcp-discover", "Discovery returns tool names and input schemas.", '<McpSequence :level="2" />',
             "list_tools returns the actual schema for onboarding_status and provision_member. The discover_onboarding action exposes those records to the model. A schema describes accepted arguments; it does not grant access or execute a write."),
        item("mcp-invoke", "Call the discovered tool with the selected arguments.", '<McpSequence :level="3" />',
             "The call supplies account_id, email, role and operation_id. The MCP server calls the same office simulator used in our checks. The simulated write can commit before a timeout result comes back."),
        item("mcp-return", "Read the returned observation before deciding what to do next.", '<McpSequence :level="4" />',
             "The server returns JSON and saves office.json. The executor reloads that state and my_observation adds the result to the conversation. A timed-out result and unchanged client expectations cannot establish that the server did nothing."),
        item("mcp-code", "Discovery and execution are separate client calls.",
             code('''await client.initialize()
tools = await client.list_tools()
if name == "discover_onboarding":
    result = {"tools": [{"name": t.name, "inputSchema": t.inputSchema}
                        for t in tools.tools]}
else:
    response = await client.call_tool(name, arguments)
    result = json.loads(next(c.text for c in response.content
                             if hasattr(c, "text")))''', '1-2|3-5|6-9|all') +
             '<div class="bottom-note">Excerpt from pending/loop.py · Inspect provision_member and onboarding_status in your own Agent Lens conversation.</div>',
             "This is the exact client control flow inside mcp_action, with the surrounding context managers omitted. Ask which branch can discover tools without invoking a mutation, and which branch parses a tool response. This is explanatory code, not an additional exercise or model call.")
    ])
    before("judge", [
        item("judge-state", "The account can contradict a confident reply.", '<JudgeMeaning :level="1" />',
             "The public partial-refund fixture contains one 100-cent refund, compared with the required 4900 cents. The model's explanation cannot change that state. Read the actual integer comparison before introducing the judge."),
        item("judge-validity", "A valid judge response can still contain a wrong judgment.", '<JudgeMeaning :level="2" />',
             "Work through availability, schema and correctness separately. The validator can reject strings in boolean fields. It cannot prove complete:true is right. For this illustrative partial-refund example it would be wrong. The live judge's actual reason remains the evidence to inspect.")
    ])
    before("round-two", [
        item("between-rounds", "The next task gets the selected procedure and a checked lesson.", '<ExecutionBoundaries :level="2" />',
             "A lesson is an agent-written interpretation with a supporting run and limits. It is not a model weight update. We carry the selected harness and lesson into onboarding, while constructing a fresh account state and conversation for that case. The next execution tests whether the lesson transfers."),
        item("compose-not-test", "Choosing a combination does not test it.",
             '<div class="two-col"><div class="ticket"><div class="account">PROBED CANDIDATES</div><p>A: revised skill<br>B: completion gate</p><p class="mini">Each has its own execution.</p></div><div class="ticket"><div class="account">POSSIBLE COMPOSITION</div><p>Revised skill + gate</p><p class="mini">This combination needs its own execution.</p></div></div><div class="bottom-note">Illustrative choices. Retain this version also receives a confirming run, without inventing changed files.</div>',
             "Do not infer that a composition inherits the scores of its ingredients. The combined behavior can differ, so the controller runs it before adoption. The recorded round-one decision retained the parent instead; the previous slides show its reason and execution.")
    ])

    by_key = {row["key"]: row for row in slides}
    by_key["cover"]["body"] = by_key["cover"]["body"].replace("three-hour", "four-hour")
    by_key["schedule"]["body"] = '<div class="current-plan"><div>0:00–1:10<small>Understand the harness, trace, implement tools and handoff</small></div><div>1:20–2:15<small>MCP, timeout recovery, scoring and a manual edit</small></div><div>2:25–3:30<small>Two rounds of proposed edits and matched probes</small></div><div>3:30–4:00<small>Fresh tickets, comparison, conclusion</small></div></div><div class="bottom-note">Ten-minute breaks at 1:10 and 2:15. Leave each exercise slide visible while participants code.</div>'
    by_key["schedule"]["notes"] = "One four-hour session. The schedule includes two ten-minute breaks and hands-on coding. Foundations precede implementation; worked answers are linked for help, not additional required work. Allow final comparisons to finish from saved stages if provider latency is high. Never call a replay the attendee's execution."
    by_key["break"]["notes"] = "Second break: 135–145 minutes. Save the manual comparison and return to step 6. Do not start automatic work during the break."
    by_key["break"]["body"] = by_key["break"]["body"].replace("Resume at 6", "2:15–2:25 · Resume at 6")

    # These section anchors also feed the facilitator's runbook and slide map.
    sections = [
        ("cover", "Understand the task and harness", 0, 20, "1 · Connect and trace", "harness.py", ""),
        ("copy", "Connect and instrument", 20, 20, "1 · Connect and trace", "teaching.py", "visual-v030-pending-lookup.png"),
        ("invoice", "Implement the tool and observation handoff", 40, 30, "2–3 · Tools and observations", "loop.py", ""),
        ("break-one", "Break", 70, 10, "", "", ""),
        ("model-span", "Inspect MCP and recover from a timeout", 80, 25, "3 · Pass observations to the agent", "loop.py", "visual-v030-pending-timeout.png"),
        ("checks", "Score the work and edit one procedure", 105, 30, "4–5 · Check and edit", "teaching.py", "evidence/pending-retry-repair.json"),
        ("break", "Break", 135, 10, "", "", ""),
        ("editor", "Propose, probe and compose", 145, 40, "6 · Improve twice", "loop.py", "evidence/v030-pending-rehearsal.json"),
        ("between-rounds", "Carry a lesson into the next task", 185, 25, "6 · Improve twice", "loop.py", "evidence/v030-pending-rehearsal.json"),
        ("freeze", "Evaluate frozen harnesses", 210, 20, "7 · Compare fresh tickets", "grading.py", "evidence/v030-pending-rehearsal.json"),
        ("report", "Explain the result", 230, 10, "8 · Explain the result", "loop.py", "evidence/v030-pending-rehearsal.json"),
        ("answer-tool", "Worked answers", 240, 0, "Reference", "teaching.py", ""),
    ]
    current = sections[0]
    anchors = {row[0]: row for row in sections}
    for row in slides:
        current = anchors.get(row["key"], current)
        _, section, start, duration, step, source, evidence = current
        row["concept"] = row["title"].replace("<br>", " ").rstrip(".")
        row["timing"] = dict(section=section, start_minute=start, duration_minutes=duration)
        row["source"] = ["scripts/pending_cells.py"] + (["src/forge_workshop_kit/pending/" + source] if source else [])
        row["evidence"] = [evidence] if evidence else []
        row.setdefault("exercise", {"step": step})
    return sections
