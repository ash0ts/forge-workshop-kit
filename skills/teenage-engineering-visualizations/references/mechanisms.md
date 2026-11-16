# Illustrating a mechanism

Start with a drawing someone could point at while explaining the operation. The TE guides establish the whole object, identify the part being used, enlarge that part, then show what happens. Use that instructional structure for software and data as well as physical systems.

## Choose an object with inspectable parts

| Subject | Draw | Make the operation visible |
| --- | --- | --- |
| Tool dispatch | Action record, argument fields, selected function, returned record, appended message | Trace the same account and invoice values across the function boundary. Show the new message appended to the old history. |
| Forecasting | Timestamped observations, a selected window, tensor cells, output and target | Move the window boundary; keep the target outside it. Show flattening or convolution on the actual dimensions. |
| Classification | Message tokens, sparse or dense feature values, probability columns, queue labels | Preserve column positions while changing the label mapping. Show which destination becomes wrong. |
| Patch features | Photograph, patch grid, enlarged patch, reference patches, distances | Point from the selected image region to its feature vector and nearest reference. Do not imply that a distance is a causal explanation. |
| Parallel work | Task rows, owner cells, working-copy trees, changed lines and integration result | Show two claim attempts against one owner field, or two patches touching the same line. |
| Itinerary updates | Ordered flight segments and a replacement interval | Keep the unchanged segment visible in the complete replacement payload. Show precisely where a faulty payload drops it. |

These are examples, not a library of mandatory metaphors. Use the actual system's structure. Do not add knobs, circuit traces, or fake panels just to make software resemble a device.

## Three useful views

**Anatomy:** one assembled drawing dominates the page. Short labels point to real parts. A file can expose its key fields; a model can expose its layers. Details earn their place by answering a question.

**Operation:** show before, action, and after. Repeat the same object at the same scale. Emphasize the changed part and retain unchanged context. An action arrow ends on the part being changed, not on a generic box containing its name.

**Enlarged detail:** locate the small part on the assembled drawing, enclose it, then connect it to a larger view. The enlarged view retains the same identifiers, ordering, and values. A decorative circle around an unrelated icon is not a detail view.

## Drawing and type

Use original SVG paths, rows, grids, curves, shapes, and local photographs. Put annotations around the drawing. Keep most of the page available for the object and its operation. A code excerpt is useful when its operands can be found in the drawing.

At a 1200 × 675 slide size, use body labels around 18–22 px and code around 16–18 px. Short identifiers can be smaller only if they remain legible at projected size. Prefer fewer visible details over shrinking a dense implementation to fit. Numbered callouts connect the mechanism, code, and evidence; they do not replace the mechanism.

Original screenshots and scientific images keep their colors and provenance. An illustration of a fixture is labeled illustrative. A drawn prediction must not imply a recorded experimental result.

## Review

Inspect the rendered drawing at its intended size, not only its SVG source. Ask:

- What can the reader identify here that the previous text-only explanation could not show?
- Which specific part does each leader line point to?
- Is there an actual input, intermediate state, or output to follow?
- Do consecutive frames show the change while keeping its context stable?
- Is the largest object the thing being explained, or merely a large caption?
- Are illustrated examples distinguishable from measurements and native captures?

If the explanation would work just as well as a bullet list, it probably needs a different drawing. Keep simple lists as lists; do not dress them up as diagrams.
