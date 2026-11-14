# Build a transit product with a small software factory

A rider checks the board just after midnight. The next train is still part of
yesterday's service. Your team's product needs to show that train, explain its
destination, and later identify the last direct train between two platforms.

The workshop builds a historical timetable explorer from a real MBTA feed. It
does not provide live predictions or current travel advice. Agents implement two
files against one shared contract: `query.py` selects the trains, and
`presentation.py` renders the result. You inspect each diff and integrate the
changes before running independent acceptance checks.

## The data

The [official archived feed](https://cdn.mbtace.com/archive/20241128.zip) covers
November 28 through December 4, 2024. Its SHA-256 is
`a034da05b7d71d9ce8977b9c59bee831cec52c4bf4a560ae3ad09e3064c27bcd`.
The MBTA [archive documentation](https://github.com/mbta/gtfs-documentation/blob/02da961b963ba3d3a66042ca4d5bd19e21ce5c0a/reference/gtfs-archive.md)
explains that archive dates can be adjusted after publication to identify the
appropriate historical period.

We retain all active Red Line trips for that week, restricted to the two
platforms at Kendall/MIT, Charles/MGH, Park Street, Downtown Crossing, and South
Station. The packaged subset has 1,252 trips and 6,260 stop-time rows. The
original field names and values are unchanged. The preparation script records
the original CSV checksums, selection rule, source version, license, and output
checksums. Data selection used dates and schedule coverage before any agent ran.

For example, the actual `stop_times.txt` record for trip `63926435` at platform
`70076` has departure time `24:08:00`. Its trip uses `ThanksgivingDay` service,
which `calendar_dates.txt` adds on November 28. The train therefore departs Park
Street toward Alewife at **00:08 on November 29**, while retaining **November 28
as its service date**. That distinction follows the
[GTFS service-day definition](https://gtfs.org/documentation/schedule/reference/#term-definitions).

The dates contain no daylight-saving transition and use UTC−05:00. The exercise
does not claim to implement a general timezone-aware journey planner. Parent
stations, transfers, fares, accessibility routing, and real-time changes are
outside its contract.

Data is provided by MassDOT and the MBTA under the included Massachusetts
Department of Transportation Developers License Agreement. This independent
teaching app is not affiliated with or endorsed by either agency. The agreement
permits reuse and redistribution with attribution and other stated conditions;
it does not grant use of agency logos. Read the bundled
[license](../../src/forge_workshop_kit/assets/transit/developers-license-agreement.pdf).

## Run the free worked implementation

From a Workshop Kit checkout:

```sh
uv sync --frozen
uv run python -c "from forge_workshop_kit import transit; print(transit.evaluate(transit.worked_sources(2), order=2))"
uv run python -c "from forge_workshop_kit import transit; transit.export_app(transit.worked_sources(2), 'transit-product', order=2)"
uv run marimo edit transit-product/app.py
```

This exports the exact source and pinned data as a small editable application.
Choose a platform and historical time to inspect departures. The second view
selects two platforms and a service date, then offers the itinerary as a JSON
download. These controls use local computation and make no model calls.

The worked solution is instructor-authored. The separately labeled repair
removes and then restores the previous-service-day lookup. Its saved check
results demonstrate an implementation repair, not a measured advantage of
multiple agents or shared memory.

## Development checks and final evaluation

`transit.development_check()` supplies public checks for each independently
editable file. `transit.evaluate()` uses different case identities and also
checks the renderer against the query's actual output. It records every result,
including empty results and execution failures. Neither the reference scorer nor
reserved cases are copied into worker directories or model requests. Their
source remains inspectable by workshop participants in this public repository.

Candidate code runs with an execution deadline, an approved import list, and a
clean environment that does not inherit Forge credentials. This is reviewed
local code execution, not a security sandbox. Review changes before executing
or exporting them.

To reproduce acquisition and verify the pinned source bytes:

```sh
uv run python scripts/prepare_transit.py
```

That command downloads only the public historical archive and its license. No
inference access is needed.
