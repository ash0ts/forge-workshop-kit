# Visual rules

The bundled token file defines the shared colors, font families, and baseline stroke values. The renderer owns composition geometry, spacing, and type sizes. The standalone HTML stylesheet uses CSS variables generated from the same color tokens. Use these sources together; do not create a separate theme for each figure.

## Drawing

Use pale neutral paper, charcoal headings, gray component surfaces, and restrained orange emphasis. Scientific images and screenshots retain their original meaningful colors. Existing branch colors can identify alternatives, with a written legend. Color never implies correctness.

Original line drawings identify files, records, inputs, outputs, clocks, and state. Do not turn software into an ornamental synthesizer or add controls without a function. A rectangle represents a component only when its label explains that component's responsibility.

Use solid labeled connections for data or execution. Use dashed connections for observations, references, and reviewed evidence. Put a decision in its own labeled element; selecting a version is not an execution.

Keep component positions stable through a sequence. Dim future context rather than rearranging the whole drawing. Reveal the next operation or value, not fragments of an otherwise unreadable sentence.

## Type and copy

Use bundled IBM Plex Sans for explanations and IBM Plex Mono for code, identifiers, and compact numeric labels. Use sentence case and readable weights. Keep units beside values and dimensions beside tensors.

Use a short functional title, then enough context to understand the operation. A caption should explain what changed or what to inspect. Avoid slogans, invented terminology, and repeated claims that the system is powerful or important.

## Close-ups and captures

Show the overall object before enlarging its relevant detail. Use a numbered callout to connect the detail, code, and native product field. Keep originals unchanged and overlays editable. Record source URL, capture date when known, and whether the capture shows a learner result or a recorded example.

## Comparisons

Keep the same case, axes, scale, and ordering. Label changed conditions. Show ties and regressions as clearly as improvements. A successful API response does not establish a correct task outcome; fewer alerts do not establish better monitoring.

For an illustrative calculation, say so in the visible caption. Do not interpolate a learning curve, invent a screenshot, or attach a plausible result to code that was never run.

## Surfaces

- Slides use a large diagram and a small number of readable annotations. Code belongs beside the transformation it performs.
- Notebook views retain complete editable code and use local display controls. The standalone guide scales its drawing on narrow screens and provides a readable text alternative below it.
- Digital posters lead with the situation and central drawing. Links work without scanning a QR code.
- Print posters keep the same hierarchy with larger type and a readable short URL beside the QR.
- A static frame must remain understandable when motion or JavaScript is unavailable.
