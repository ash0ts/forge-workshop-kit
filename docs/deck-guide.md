# Workshop decks

The Solar companion is in `decks/solar/`. It keeps the original deck’s typography, colors, progressive diagrams and exact exercise instructions, with a computational research lab as its setting. Pending, Inc. keeps its office setting.

The notebook is the work surface. Keep the current exercise slide on screen while participants edit code and inspect their own evidence. Worked answers follow the main deck and link back to the exercise. Recorded results are labeled separately from participant work.

## Solar Autoresearch

The four-hour schedule is in `decks/solar/notes/facilitator-notes.md`. The editable storyboard is `decks/solar/scripts/build-storyboard.py`, which generates `slides.md`. The portable browser deck and PDF preserve each incremental diagram frame.

- Begin with the failed handoff of a promising score without reproducible source or settings. This opening is fictional.
- Build persistence, record experiments, compare six configurations, then move from measurements to image forecasts.
- Distinguish changing settings, choosing implemented architectures, and asking an agent to write new code.
- The forecasting models train weights. The research agent remains fixed.
- Review two candidates, test them, compose, test again, and retain evidence for another round.
- Freeze source and trained weights before opening reserved dates. Keep measurement and image metrics separate.

The public source and dataset are part of the same repository. Attendees copy the template into their own project and use their own Forge access. No host token or workshop gateway is involved. Hosted notebook compute is billed separately from the notebook’s inference allowance.

## Pending, Inc.

The [November 12 deck](https://github.com/ash0ts/pending-inc-workshop/releases/tag/workshop-2026-11-12) remains a historical workshop release. Its explanatory diagrams and exercise progression are the design reference. Its gateway, two-token setup, and expired access window do not apply to the Workshop Kit notebook.

For the current gateway-free Pending notebook, begin at [the new template](https://forge.coreweave.com/notebooks/Tm90ZWJvb2s6MTU3NzQ=/view), copy it into the attendee’s project, and use the notebook’s own guided steps. The kit uses local tools and actual local MCP. Do not describe those receipts as remote Sandbox execution.

### Current Pending exercise references

Keep the office scenes and technical diagrams from the earlier deck. Use the following controls when presenting the current notebook; its steps replace the old connection forms, phase dropdowns, and step/finish buttons.

| Earlier deck topic | Current notebook step and editable code | Current action |
| --- | --- | --- |
| Clock in and connect | **1 · Connect and trace**; `my_tool_span`, `my_model_span` | **Check my project and restore saved work**, then **Run this check and verify my Agent Lens trace** |
| Equipment and invoice access | **2 · Build an invoice tool**; `my_invoice_tool` | **Test my invoice lookup** |
| Employee tool loop | **3 · Pass observations to the agent**; `my_dispatch`, `my_observation` | **Test my tool-to-model handoff**, then **Freeze this executor and run the two starting tickets** |
| Stop marking your own homework | **4 · Check the work**; `my_state_check`, `my_judge_validation`, judge rubric | **Test my scorer against four known examples**, then **Judge and publish the starting development comparison** |
| Update the handbook | **5 · Edit one procedure**; selected evidence and verification skill | **Save this procedure and rerun both development tickets** |
| Automate management and repeat | **6 · Improve twice**; visible proposal, probe, composition and adoption code | Use the one current **Round N · …** control. Review the displayed diff before testing; the notebook advances from saved records. |
| Monday, again | **7 · Compare fresh tickets**; frozen versions and independent scoring | **Freeze versions and run 12 evaluations** |
| Explain the work; optional ARIA | **8 · Explain the result**; conclusion and evidence links | **Publish my conclusion with the comparison and evidence**. The optional ARIA prompt asks for analysis, not new executions. |

The invoice tool runs in local Python and onboarding uses actual local MCP. The participant's credentials publish directly to their project. Do not use the historical deck's remote Sandbox registration, gateway URL, host tokens, or renewal instructions. The editor changes the harness after the participant's executor is frozen; it cannot replace the tool loop or trusted final scorer.

The current authored cells live in `scripts/pending_cells.py`; the generated attendee notebook is `notebooks/pending_inc.py`. Those files are the source of truth for button labels and prerequisites.

## Product screens

Use the current participant’s own runs whenever possible. Captures in the deck are recorded evidence, not promises about what a new execution will do. Agent Lens shows actual model and tool activity. W&B runs and Artifacts preserve training settings and files. Weave and native EvalTables align matching cases when publication is available.

Native EvalTables returned HTTP 500 in the technical rehearsal. Use the notebook and Weave comparisons when that status persists, then retry publication without repeating training or model calls.
