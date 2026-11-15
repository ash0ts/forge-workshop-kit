"""Render sourced diagrams for the Transit and Airline learning Reports.

No service calls, training, or inference. PNGs are for native Reports; SVGs retain
editable text. Screenshots remain their original files and are never redrawn.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'workshop-report-mpl'))
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'reports/assets'
BG, INK, MUTED = '#f8f5ee', '#183f3e', '#546563'
TEAL, BLUE, ORANGE, GRAY = '#147d79', '#3478ad', '#bc6d35', '#8b9593'
PALE, BLUE_PALE, ORANGE_PALE = '#e4efeb', '#e6eff6', '#f4e8db'
plt.rcParams.update({'svg.fonttype': 'none', 'svg.hashsalt': 'workshop-report-transit-airline-v1', 'font.size': 17, 'text.color': INK})


def fonts():
    # Matplotlib's bundled face keeps local regeneration independent of font downloads.
    plt.rcParams['font.family'] = 'DejaVu Sans'


def canvas(title, subtitle, height=7.5):
    fig, ax = plt.subplots(figsize=(12, height), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set(xlim=(0, 12), ylim=(0, height))
    ax.axis('off')
    fig.subplots_adjust(0, 0, 1, 1)
    text(ax, .55, height-.62, title, 26, weight='bold')
    text(ax, .55, height-1.12, subtitle, 15, color=MUTED)
    return fig, ax


def text(ax, x, y, label, size=18, color=INK, weight='normal', ha='left', **kw):
    return ax.text(x, y, label, fontsize=size, color=color, weight=weight,
                   ha=ha, va='center', linespacing=1.35, **kw)


def box(ax, x, y, w, h, label, *, color=TEAL, fill=PALE, size=18):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.10',
                               facecolor=fill, edgecolor=color, linewidth=1.5))
    text(ax, x+w/2, y+h/2, label, size, ha='center')


def arrow(ax, start, end, color=INK, dashed=False):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=16,
                               linewidth=1.6, color=color, linestyle='--' if dashed else '-'))


def save(fig, slug, name):
    fig.canvas.draw()
    bounds = fig.bbox
    for ax in fig.axes:
        for label in ax.texts:
            extent = label.get_window_extent(fig.canvas.get_renderer())
            if extent.x0 < 0 or extent.y0 < 0 or extent.x1 > bounds.width or extent.y1 > bounds.height:
                raise ValueError(f'Clipped text in {slug}/{name}: {label.get_text()}')
    folder = ASSETS / slug
    folder.mkdir(parents=True, exist_ok=True)
    for suffix in ('svg', 'png'):
        fig.savefig(folder / f'{name}.{suffix}', facecolor=BG,
                    **({'metadata': {'Date': None}} if suffix == 'svg' else {}))
        if suffix == 'svg':
            path = folder / f'{name}.{suffix}'
            path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
    plt.close(fig)


def transit():
    fig, ax = canvas('The train after midnight still has a service day',
                     'Real MBTA record · Park Street · trip 63926435 · historical schedule')
    box(ax, .6, 4.5, 4.3, 1.35, 'Service date: Nov 28, 2024\nGTFS departure: 24:08:00', color=GRAY, fill='#eeece6')
    box(ax, 6.2, 4.5, 5.2, 1.35, 'Passenger clock: Nov 29\n00:08 Eastern', color=TEAL)
    arrow(ax, (5,5.18),(6.1,5.18))
    text(ax, 6, 3.8, 'Nov 28 midnight + 24 hours + 8 minutes', 21, ha='center')
    ax.plot([1,11],[2.6,2.6],color=GRAY,lw=3)
    for x,top,bottom,color in [(1.5,'Nov 28','23:55',GRAY),(4.5,'Nov 29','00:00',GRAY),(7.5,'Query','00:05',BLUE),(9.3,'Departure','00:08',TEAL)]:
        ax.plot([x,x],[2.47,2.73],color=color,lw=3)
        text(ax,x,3.1,top,16,ha='center',color=color)
        text(ax,x,2.14,bottom,20,ha='center',color=color,weight='bold')
    text(ax,6,1.25,'At 00:05, include the 00:08 train from the previous service day.',19,ha='center')
    text(ax,.6,.5,'Source: retained stop_times and calendar records; not a live arrival prediction.',13,color=MUTED)
    save(fig,'transit','service-day')

    fig, ax = canvas('Separate work becomes one checked application',
                     'Implemented coordination flow · workers edit app code; participants review patches',8.3)
    box(ax,3.8,5.9,4.4,1.05,'Shared starting files + contracts',color=GRAY,fill='#eeece6',size=19)
    box(ax,.7,3.6,4.65,1.5,'Query worker\nOwns query.py\nread → edit → development test',color=BLUE,fill=BLUE_PALE,size=18)
    box(ax,6.65,3.6,4.65,1.5,'Presentation worker\nOwns presentation.py\nread → edit → development test',color=ORANGE,fill=ORANGE_PALE,size=18)
    arrow(ax,(4.4,5.85),(3,5.15));arrow(ax,(7.6,5.85),(9,5.15))
    box(ax,3.8,1.85,4.4,1.05,'Review + integrate patches',color=TEAL,size=19)
    arrow(ax,(3,3.55),(4.8,2.95));arrow(ax,(9,3.55),(7.2,2.95))
    text(ax,.7,2.48,'Conflicting changes?\nStop and inspect.',16,color=MUTED)
    box(ax,3.8,.35,4.4,.85,'Check the combined app',color=INK,fill=BG,size=19)
    arrow(ax,(6,1.8),(6,1.25))
    text(ax,8.55,.8,'Submitted ≠ integrated\nIntegrated ≠ correct',15,color=MUTED)
    save(fig,'transit','worker-integration')

    summary=json.loads((ROOT/'evidence/transit-v060-rehearsal-summary.json').read_text())
    r5=next(r for r in summary['rehearsals'] if r['identity']=='transit-v060-live-r5')
    scores=[r5['evaluations'][k]['passed_count'] for k in ('solo','team')]
    assert scores==[10,8]
    fig, ax=canvas('The faster build returned the wrong train',
                   'Recorded R5 comparison · same first work order · one run per condition',7.2)
    for y,label,color,passed,seconds,cost in [(4.6,'One worker',BLUE,scores[0],124.78,.01107),(2.8,'Two workers',ORANGE,scores[1],94.91,.01221)]:
        text(ax,.65,y+.45,label,22,color=color,weight='bold')
        for i in range(10):
            ax.add_patch(Rectangle((3+i*.38,y+.18),.28,.46,facecolor=color if i<passed else BG,
                                   edgecolor=color,lw=1.7,hatch=None if i<passed else '//'))
        text(ax,7.1,y+.42,f'{passed}/10',23,weight='bold')
        text(ax,8.7,y+.42,f'{seconds:.2f} s',22)
        text(ax,8.7,y-.15,f'${cost:.5f}',17,color=MUTED)
    text(ax,3,5.65,'Final checks passed',16,color=MUTED)
    text(ax,8.7,5.65,'Builder time / model cost',15,color=MUTED)
    text(ax,.65,1.65,'The two failed checks cover the query and rendered board for one UTC bug.',17)
    text(ax,.65,1.05,'Time excludes participant review and integration. Both builds passed 5/5 development checks.',15,color=MUTED)
    text(ax,.65,.45,'Source: R5 saved evaluations. Filled / hatched marks mean passed / failed checks.',13,color=MUTED)
    save(fig,'transit','build-comparison')

    fig, ax=canvas('Carry a reviewed lesson into the next work order',
                   'Same starting release, specification, contracts, model, and request limits',7.8)
    box(ax,.65,4.3,4.2,1.3,'Proposed note\nEvidence + scope\nContract version',color=GRAY,fill='#eeece6',size=17)
    box(ax,6.2,4.3,5.1,1.3,'Participant reviews the note\nAccept, reject, or revise',size=19)
    arrow(ax,(4.9,4.95),(6.1,4.95),dashed=True)
    box(ax,.65,1.7,4.75,1.35,'Team without lessons\nNo experience notes in context',color=BLUE,fill=BLUE_PALE,size=19)
    box(ax,6.6,1.7,4.75,1.35,'Team with accepted lessons\nOnly applicable notes in context',color=ORANGE,fill=ORANGE_PALE,size=18)
    arrow(ax,(8.9,4.25),(8.9,3.1),dashed=True)
    text(ax,3,.88,'R5: 12/18 final checks passed',19,ha='center',color=BLUE)
    text(ax,9,.88,'R5: 12/18 final checks passed',19,ha='center',color=ORANGE)
    text(ax,.65,.3,'Both query workers stopped before testing. Neither follow-up was releasable.',14,color=MUTED)
    save(fig,'transit','memory-comparison')


def airline():
    cases=json.loads((ROOT/'src/forge_workshop_kit/assets/airline/cases.json').read_text())
    case=next(c for c in cases if c['id']=='airline-discovery-02')
    booking=case['initial']['reservation']
    assert booking['reservation_id']=='59XX6W'
    assert [r['flight_number'] for r in booking['flights']]==['HAT007','HAT174']
    assert case['passenger']['replacement'][0]['flight_number']=='HAT061'
    fig,ax=canvas('Change the outward flight; keep the journey home',
                  'Simulated reservation 59XX6W · replace segment [0:1] · complete-itinerary API',8)
    text(ax,.65,5.95,'Original booking',18,weight='bold')
    box(ax,3.1,5.2,3.6,1.35,'HAT007 · May 19\nLAS → ATL',color=GRAY,fill='#eeece6',size=20)
    box(ax,7.3,5.2,4.1,1.35,'HAT174 · May 29\nATL → LAS',color=TEAL,size=20)
    text(ax,.65,3.9,'Required result',18,weight='bold')
    box(ax,3.1,3.15,3.6,1.35,'HAT061 · May 19\nLAS → ATL',color=BLUE,fill=BLUE_PALE,size=20)
    box(ax,7.3,3.15,4.1,1.35,'HAT174 · May 29\nATL → LAS',color=TEAL,size=20)
    arrow(ax,(4.9,5.15),(4.9,4.55),BLUE);arrow(ax,(9.35,5.15),(9.35,4.55),TEAL)
    text(ax,4.9,2.65,'Replace this flight',17,ha='center',color=BLUE)
    text(ax,9.35,2.65,'Preserve this flight',17,ha='center',color=TEAL)
    box(ax,.65,.7,10.75,1.15,'Send [HAT061, HAT174] after fare quote and confirmation.\nSending only [HAT061] replaces the booking with one flight.',size=19,color=ORANGE,fill=ORANGE_PALE)
    save(fig,'airline','itinerary-change')

    fig,ax=canvas('Three checks ask different questions',
                  'One request can contain a failed tool call and still finish correctly',7.7)
    rows=[(4.9,'Tool execution','Did this call return?','Error, arguments, timing',BLUE,BLUE_PALE),
          (3.15,'Booking correctness','Did the requested change happen?','Flights, passengers, policy, confirmation',TEAL,PALE),
          (1.4,'Explanation judgment','Does the reply match the work?','Claims, unresolved issues, available context',ORANGE,ORANGE_PALE)]
    for y,title,q,evidence,color,fill in rows:
        box(ax,.65,y,3.4,1.35,title,color=color,fill=fill,size=19)
        text(ax,4.45,y+.92,q,21,weight='bold')
        text(ax,4.45,y+.38,evidence,16,color=MUTED)
    text(ax,.65,.55,'Recorded qualification: 10 tool errors; all 40 final bookings passed independent checks.',15,color=MUTED)
    save(fig,'airline','different-checks')

    fig,ax=canvas('Unprocessed turns have no prediction yet',
                  'Metric definitions · no invented predictions from the unavailable native judge',8)
    box(ax,.65,5.45,10.7,1,'Eligible turns in the frozen workshop batch',color=GRAY,fill='#eeece6',size=21)
    box(ax,.65,3.3,6.3,1.25,'Completed boolean predictions\nOnly these can be positive or negative',color=TEAL,size=19)
    box(ax,7.5,3.3,3.85,1.25,'Unprocessed / unavailable\nNo prediction yet',color=GRAY,fill='#eeece6',size=18)
    arrow(ax,(3.8,5.4),(3.8,4.6));arrow(ax,(9.4,5.4),(9.4,4.6),GRAY)
    text(ax,.65,2.55,'Coverage = completed predictions / eligible turns',21,weight='bold')
    text(ax,.65,1.65,'Then keep the completed predictions with reviewed human labels:',17)
    text(ax,.65,1.02,'Precision = TP / (TP + FP)       Recall = TP / (TP + FN)',21)
    text(ax,.65,.42,'TP = correctly flagged issue; FP = false alarm; FN = missed reviewed issue. Empty denominators stay missing.',13,color=MUTED)
    save(fig,'airline','monitor-denominators')

    fig,ax=canvas('Replay the reviewed request from its original booking',
                  'Controlled local regression · no model calls · confirmation remains enforced',8.4)
    box(ax,2.1,5.85,7.8,1,'Saved request + original [HAT007, HAT174]',color=GRAY,fill='#eeece6',size=21)
    box(ax,.65,3.65,4.9,1.4,'Omission adapter\nProposes [HAT061]',color=ORANGE,fill=ORANGE_PALE,size=21)
    box(ax,6.45,3.65,4.9,1.4,'Itinerary builder\nProposes [HAT061, HAT174]',color=BLUE,fill=BLUE_PALE,size=20)
    arrow(ax,(4.3,5.8),(3.1,5.1));arrow(ax,(7.7,5.8),(8.9,5.1))
    text(ax,3.1,2.95,'Passenger refuses',21,ha='center',weight='bold')
    text(ax,8.9,2.95,'Passenger confirms',21,ha='center',weight='bold')
    arrow(ax,(3.1,3.6),(3.1,3.25));arrow(ax,(8.9,3.6),(8.9,3.25))
    box(ax,.65,1,4.9,1.3,'Booking stays [HAT007, HAT174]\nRequested change: incomplete',color=ORANGE,fill=BG,size=17)
    box(ax,6.45,1,4.9,1.3,'Booking becomes [HAT061, HAT174]\nBooking checks: pass',color=BLUE,fill=BG,size=17)
    arrow(ax,(3.1,2.65),(3.1,2.35));arrow(ax,(8.9,2.65),(8.9,2.35))
    text(ax,.65,.4,'The separate calibration incident deliberately bypassed refusal and removed the return flight.',14,color=MUTED)
    save(fig,'airline','regression-replay')


if __name__=='__main__':
    fonts()
    transit()
    airline()
