"""Replace abstract cards with mechanisms. No workshop execution or new slide count."""

def illustrate(slides):
    by_title = {slide['title']: slide for slide in slides}
    def visual(title, mode, caption, *, stage=0, clicks=None):
        slide = by_title[title]
        value = '$clicks' if clicks is not None else str(stage)
        slide['body'] = f'<TransitMechanism mode="{mode}" :stage="{value}"/><p class="caption">{caption}</p>'
        slide['clicks'] = clicks
        slide['notes'] += ' Visual revision: follow the same named record across the reveal; all illustrative source edits are labeled. Read the caption before opening the matching notebook exercise.'
    visual('The inputs are public transit records', 'joins',
           'Follow trip_id to the service rule, then convert its departure time. 10 platforms, 1,252 trips and 6,260 stop times in this teaching subset.', clicks=2)
    visual('Start with the row for the platform', 'joins',
           'The stop-time row identifies the trip and platform. It does not contain the date on which that trip runs.', stage=0)
    visual('Join the trip to its service calendar', 'joins',
           'The shared trip_id identifies ThanksgivingDay service. Its calendar exception adds service on November 28.', stage=2)
    visual('The last train can belong to yesterday’s service', 'service-day',
           'The rider boards on November 29. The train still belongs to November 28 service. Reducing 24 modulo 24 loses that link.', stage=2)
    visual('One worker still needs a complete loop', 'worker',
           'Each tool returns an observation. That returned value goes into the next request; the worker cannot learn from a result it never receives.', clicks=3)
    visual('Choose work that can happen independently', 'tasks',
           'The query and presentation tasks can start independently. The combined check waits for both reviewed outputs.', clicks=1)
    visual('Separate working copies protect unfinished changes', 'copies',
           'Ownership limits which file each worker can edit. The shared return schema still needs a combined application test.', clicks=2)
    visual('Review a patch before it enters the product', 'copies',
           'Read the actual diff, check its base hash, then apply it. A hash check prevents stale replacement; it cannot prove the two modules agree.', stage=2)
    visual('Shared memory needs something worth sharing', 'records',
           'Store coordination, interfaces and experience separately. A task status does not establish that a general lesson is true.')
    visual('The factory has two kinds of state', 'records',
           'Task records resume the current build. Contracts and checked lessons inform future work. None requires one giant shared chat.')
    visual('Find the last direct train between two stops', 'matched',
           'Both teams receive the identical follow-up feature. Freeze the selected lesson before running either condition.', stage=0)
    visual('The faster build missed two final cases', 'outcomes',
           'Both first builds passed development checks. The reserved UTC cases exposed a wrong train in the team output. Follow-up results appear separately below.')
    visual('A timezone assumption selected the wrong train', 'timezone',
           'Follow the request, selected GTFS row and rendered board. These are two failed checks of one timezone bug, not two independent defects.', clicks=2)
    visual('Neither follow-up completed the query change', 'matched',
           'Open both failed requests in Agent Lens. Neither branch reached query testing, so this pair cannot establish a memory benefit.', stage=2)
    # Same historical failure evidence as before. The spatial clock example is not a scaled elapsed-time chart.
    for title in ['Interpret the request as one instant','The team used the caller’s clock for service time','The renderer carried the same wrong trip into the board']:
        by_title[title]['notes'] += ' The paired clock positions show matching instants, with nonuniform spacing for legibility. The third position is five hours after the expected departure.'
    return slides
