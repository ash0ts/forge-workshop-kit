# Transit product contract
This is a historical timetable explorer, not live travel advice. MassDOT/MBTA
provide the schedule data. The subset covers ten central Red Line platforms,
2024-11-28 through 2024-12-04. All times in this week use UTC-05:00.

Only query.py and presentation.py may change. Use Python's standard library.
No network calls, new processes, package imports, or reads of files outside the
workspace. Inputs are plain JSON tables with original GTFS column names and
string values. Do not hard-code trip IDs or expected answers.

query.departures(tables, stop_id, at, limit=5) returns a list of records with:
trip_id, route_id, headsign, stop_id, stop_name, service_date (YYYY-MM-DD), and
departure_time (ISO timestamp with UTC offset). Return departures at or after
the supplied aware timestamp and no more than two hours later, sorted by
(departure_time, trip_id), limited to 1..20. An empty list means none in that
window. Invalid platform/date/naive timestamp/limit raises ValueError.
Apply the weekday calendar AND calendar_dates additions/removals. GTFS hours
may exceed 23: 24:08:00 belongs to the stated service day but occurs at 00:08
on the following civil day. Check the previous service day after midnight.
Ignore stop times with pickup_type=1. Parent station IDs are not platform IDs.

query.last_departure(tables, origin_id, destination_id, service_date) returns
the latest direct trip on that service date, with trip_id, route_id, headsign,
origin_stop_id, destination_stop_id, service_date, departure_time, arrival_time.
Use stop_sequence to ensure the destination follows the origin on the SAME
trip; respect pickup_type/drop_off_type=1. Times stay absolute, including
after-midnight arrivals. Return None for no direct trip or identical stops.
Choose the maximum (departure_time, trip_id) for deterministic ties.

presentation.render_board(rows, title='Departures') returns escaped, readable
HTML with a heading, the stop name, destination and departure timestamp for
each row; show 'No scheduled departures in the next two hours' for []. Include
'Historical schedule' and 'MassDOT' attribution. Never call data real-time.
presentation.render_journey(journey, title='Last direct train') similarly shows
the origin, destination, both absolute timestamps, and service date. For None,
show 'No direct train in this timetable subset'. Escape text including title.
The presentation worker can use sample.json without waiting for query.py.
