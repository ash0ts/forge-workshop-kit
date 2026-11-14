# Visual Inspection companion deck

Edit `scripts/build-storyboard.py`, then run the shared deck build. The deck uses the same controls and function names as `scripts/inspection_cells.py`. The deck includes native Agent Lens and Evaluation Tables Preview captures from saved executions. Its standalone photographs and masks are actual VisA examples. On the comparison detail slide, the next click reveals the reference defect mask: white pixels mark the supplied annotation, not model localization.

The failed first recipe and the explicitly labeled teaching retest both appear. Local images retain VisA attribution and the source link. Opening the deck does not run training or inference.

The four-hour teaching sequence includes two ten-minute breaks. Progressive diagrams connect the editable function to its inputs and outputs; adjacent slides preserve the same objects for backward navigation and PDF export. Edit `scripts/depth_storyboard.py` for these sequences and timing, then run `scripts/build-storyboard.py`. Symbolic exercise/answer names resolve during generation. `notes/slide-map.json` records the concept, source, evidence, exercise control and timing for each slide.
