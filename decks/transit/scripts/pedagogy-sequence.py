"""Put a usable one-worker app before the coordination lesson."""

def reorder(slides):
    def get(title):
        return next(item for item in slides if item['title'] == title)

    acceptance = get('Write the after-midnight acceptance check')
    slides.remove(acceptance)
    acceptance['time'] = '0:22'
    acceptance['elapsed_minutes'] = 22
    acceptance['exercise']['prerequisites'] = ['Open the notebook; no account required']
    acceptance['body'] = acceptance['body'].replace('Complete <code>check_departures(rows)</code> using the real Park Street train.', 'Click <strong>Show departures from the saved timetable</strong>. Find the real Park Street departure.').replace('Check its trip ID, November 28 service date and November 29 departure together.', 'Complete <code>check_departures(rows)</code>: check its trip ID, November 28 service date and November 29 departure together.').replace('Run the free check before asking an agent to build the feature.', 'Run the free check. It must reject a missing train and an incorrect service date.')
    acceptance['notes'] += ' Run the reference query and acceptance check before authentication. The reference output is supplied code, not an agent build. The notebook saves this draft and passing check when the participant later connects.'
    slides.insert(slides.index(get('Your project contains the experiment')), acceptance)

    # Explain the task board only after learners have inspected a solo product.
    coordination = get('Add the task board and two workers')
    slides.remove(coordination)
    coordination['time'] = '1:45'
    coordination['elapsed_minutes'] = 105
    slides.insert(slides.index(get('Choose work that can happen independently')), coordination)

    solo = dict(title='Review and run the one-builder app',
        body='<p class="where">Notebook → Run one builder</p><ol><li>Read the query and presentation patches and their development checks.</li><li>Tick <strong>I reviewed the one-builder patches and their development checks</strong>.</li><li>Test the files together, then preview the actual departures board.</li></ol><div class="done"><strong>Run:</strong> Review and test the one-builder app → Preview this saved app<br><strong>Check:</strong> Explain one returned trip, its service date, and its boarding time.</div>',
        notes='A solo worker can produce both components. This integration uses the same saved solo stage and files as the later comparison. It does not select the follow-up starting release yet: that choice waits for both integrations. Failed checks remain visible. Reviewing and previewing uses no model requests.',
        time='1:28', elapsed_minutes=88, kind='exercise', name='solo-integration-exercise', clicks=None,
        source='scripts/transit_cells.py', evidence=[], answer=None, concept='reviewed solo integration',
        exercise={'step':'worker','functions':['integrate_build'],'prerequisites':['Saved solo patches','Participant patch review'],'run':'Review and test the one-builder app','inspect':'Preview this saved app'})
    slides.insert(slides.index(get('The request has a size limit even when files are saved')), solo)
    preview = get('Use the local preview to follow a returned row')
    slides.remove(preview)
    preview['time'] = '1:32'; preview['elapsed_minutes'] = 92
    preview['body'] = preview['body'].replace('Notebook → Test the combined app', 'Notebook → Run one builder').replace('Select <strong>Two builders</strong> or <strong>One builder</strong>.', 'Select the saved <strong>One builder</strong> integration.')
    preview['notes'] += ' First preview the solo integration. Repeat this same inspection after the team integration. The dropdown contains only saved integrations.'
    preview['exercise'] = {'step':'worker','functions':['preview'],'prerequisites':['Saved solo integration'],'run':'Preview this saved app'}
    slides.insert(slides.index(get('Break until 1:45')), preview)
    team = get('Test the combined departures board')
    team['exercise']['prerequisites'] = ['Two-worker build saved', 'Review its query and presentation diffs', 'Review confirmation checkbox']
    team['notes'] += ' This button now integrates only the two-worker build. The solo integration remains saved and is reused; after both results exist, the unchanged selection rule chooses the follow-up starting source.'
    team['body'] = team['body'].replace('I reviewed both builds’ patches below and their development checks', 'I reviewed the two-builder patches and their development checks').replace("I reviewed both builds\' patches below and their development checks", 'I reviewed the two-builder patches and their development checks')
