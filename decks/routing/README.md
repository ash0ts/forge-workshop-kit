# Request-routing workshop deck

This four-hour deck follows the current `notebooks/request_routing.py`. The audience joins a fictional bank support team, uses real Banking77 requests, trains two classifiers, reviews uncertain cases, checks a judge, and evaluates a frozen version.

Edit `scripts/build-storyboard.py`, then regenerate `slides.md`. It contains exact notebook controls, editable function names, presenter notes, and optional worked answers. `RoutingCase.vue` uses recorded review-pool predictions; it does not invent attendee outcomes.

The measured worked example is a 4.0844-point macro-F1 gain from frozen MiniLM features over word TF–IDF on the official test set. Participant review/retraining is an honest live experiment and may tie or regress. Evidence and limits are in `../../docs/routing-workshop.md`.

Build with the repository's `scripts/build_decks.py --only routing`. The deck includes an actual Agent Lens judge conversation and a preserved original capture with its source link. The 12-call live rehearsal verifies requests and stored spans, not judge reliability. The native comparison slides use Weave-backed Evaluation Tables Preview in the W&B workspace. They are separate from the CES v2 publication attempt, whose HTTP 500 remains visible in the saved receipt.

The four-hour teaching sequence includes two ten-minute breaks. Progressive diagrams connect the editable function to its inputs and outputs; adjacent slides preserve the same objects for backward navigation and PDF export. Edit `scripts/depth_storyboard.py` for these sequences and timing, then run `scripts/build-storyboard.py`. Symbolic exercise/answer names resolve during generation. `notes/slide-map.json` records the concept, source, evidence, exercise control and timing for each slide.
