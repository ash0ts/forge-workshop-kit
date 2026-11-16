"""Original technical-manual drawing of the notebook-to-ARIA handoff.

Identifiers are field names, not invented measurements. The same drawing is
used by the notebook and deck; a reveal adds the returned handle and source.
"""
from html import escape


def handoff(phase=2):
    if phase not in (0, 1, 2):
        raise ValueError('ARIA handoff phase must be 0, 1, or 2.')
    ink, paper, panel, orange = '#242522', '#f4f3ef', '#e8e9e3', '#ec5b28'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1110 205" role="img" aria-label="An explicit notebook action sends the question and selected records. ARIA returns a saved turn and conversation. Open that conversation, then verify its claim against the source." style="font-family:IBM Plex Sans,sans-serif;background:{paper};max-width:100%">',
        '<title>Start once, open the same conversation, check its source</title>',
        '<desc>Illustration of API fields, not a screenshot or measured response. Solid arrows send data; the dashed line follows a cited record.</desc>']
    def text(x, y, value, size=16, mono=False, fill=ink):
        family = 'IBM Plex Mono,monospace' if mono else 'IBM Plex Sans,sans-serif'
        return f'<text x="{x}" y="{y}" fill="{fill}" style="font-family:{family};font-size:{size}px">{escape(value)}</text>'
    out += [f'<rect x="8" y="8" width="320" height="183" fill="white" stroke="{ink}"/>',
        f'<path d="M8 42h320" stroke="{ink}"/>', text(22,31,'01  Notebook · your saved result',18),
        text(24,68,'Question + your explanation'),
        f'<rect x="24" y="81" width="139" height="29" fill="{panel}" stroke="{ink}"/>',
        text(34,101,'selected run',15,True),
        f'<rect x="172" y="81" width="138" height="29" fill="{panel}" stroke="{ink}"/>',
        text(180,101,'conversation',15,True),
        f'<rect x="24" y="128" width="286" height="43" fill="{orange if phase==0 else panel}" stroke="{ink}"/>',
        text(40,155,'Start ARIA investigation',17,fill='white' if phase==0 else ink),
        f'<path d="M329 100h56m-9-7 9 7-9 7" fill="none" stroke="{ink}" stroke-width="2"/>',
        text(336,84,'send',14),
        f'<rect x="393" y="8" width="330" height="183" fill="white" stroke="{ink}"/>',
        f'<path d="M393 42h330" stroke="{ink}"/>', text(407,31,'02  ARIA · the same conversation',18)]
    if phase >= 1:
        out += [text(409,67,'turn_id',16,True),text(534,67,'saved locally',16),
            text(409,93,'queued → in progress',16,True),
            f'<path d="M410 106h296" stroke="{ink}"/>',
            text(410,130,'Open ARIA conversation',17,fill=orange),
            f'<rect x="410" y="142" width="296" height="32" fill="{paper}" stroke="{ink}"/>',
            text(421,164,'Ask a follow-up in Forge',16)]
    else:
        out += [text(409,83,'The request starts here.'),text(409,114,'No request runs on opening'),text(409,138,'or restoring the notebook.')]
    out += [f'<path d="M726 100h52m-9-7 9 7-9 7" fill="none" stroke="{ink}" stroke-width="2" stroke-dasharray="5 4"/>',
        text(732,84,'cite',14),
        f'<path d="M791 8h289l22 22v161H791zM1080 8v22h22" fill="white" stroke="{ink}"/>',
        text(807,34,'03  Check the saved source',18)]
    if phase >= 2:
        out += [text(809,68,'ARIA claim → exact field',16),
            f'<rect x="809" y="80" width="271" height="32" fill="{panel}" stroke="{orange}" stroke-width="2"/>',
            text(820,102,'value / event / code line',15,True),
            text(809,140,'Supported? Disputed?'),text(809,164,'Unresolved is a valid answer.')]
    else:
        out += [text(809,85,'An answer needs a source.'),text(809,119,'This inspection comes next.')]
    return ''.join(out) + '</svg>'
