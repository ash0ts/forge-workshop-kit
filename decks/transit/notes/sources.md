# Transit deck sources

The deck distinguishes actual source records, explanatory diagrams and participant results. The recorded R3 presentation-worker component check is labeled separately from final application quality. The reference-app screenshot displays actual historical schedule rows and is labeled separately from agent results.

- Data archive: https://cdn.mbtace.com/archive/20241128.zip
- Archive SHA256: `a034da05b7d71d9ce8977b9c59bee831cec52c4bf4a560ae3ad09e3064c27bcd`
- MBTA feed definition: https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs.md
- GTFS service-day semantics: https://gtfs.org/documentation/schedule/reference/
- Actual illustrated row: trip `63926435`, stop `70076`, departure `24:08:00`, service `ThanksgivingDay`, headsign `Alewife`, stop sequence `150`.
- Prepared subset: 10 platforms at five stations, 1,252 trips and 6,260 stop-time rows. Verify against the packaged data manifest when rebuilding.

## Coordination and memory references

- https://factory.strongdm.ai/
- https://www.anthropic.com/research/building-c-compiler
- https://code.claude.com/docs/en/agent-teams
- https://github.com/gastownhall/gastown
- https://github.com/gastownhall/beads
- https://www.anthropic.com/research/components-of-agent-memory
- https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/

The sources motivate task ownership, working-copy isolation, verification, durable records and checked memory. Their performance results are not forecasts for this workshop.

## Native capture requirements

The reference-app capture is recorded in `capture-receipts.json`, including its original screenshot, crop and source hashes. Native Forge capture slides are generated only after the matching transit records exist and readback has passed. Use preserved 1920×1080 native screenshots at an 850×478 presentation size, with adjacent numbered explanations.

1. Agent Lens: the R3 presentation-worker test capture has been added after “A trace should answer what changed and why.” Its conversation, test span and verified readback are in `capture-receipts.json`. A passing component test is not an integrated-app result.
2. Native Evaluation Tables Preview: one identical scenario input aligned across frozen builds, with the actual outputs and score fields. Add after “Read one comparison row before the average.”

Store the exact source URL, selected record, capture date and any crop or redaction in a separate capture receipt. Never redraw a product screenshot or label a diagram as a recorded execution.
