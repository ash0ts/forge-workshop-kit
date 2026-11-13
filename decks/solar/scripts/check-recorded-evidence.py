"""Reconcile the displayed rehearsal results with saved source and metrics."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
study = json.loads((root / 'public/recorded-study.json').read_text())
by = {row['name']: row for row in study['stages']}
slides = (root / 'slides.md').read_text()
assert (root / 'data/recorded-runs.json').read_bytes() == (root / 'public/recorded-runs.json').read_bytes()
source_matches = []
for number in (1, 2):
    base = f'images/round-{number}'
    candidates = by[base + '/propose']['result']['candidates']
    for index, candidate in enumerate(candidates):
        probe = by[f'{base}/probe-{index}']
        assert candidate['source'] == probe['sources']['candidate.py']
        assert probe['trace']['verified']
        source_matches.append({'round': number, 'candidate': index, 'probe': probe['id'], 'source_matches': True})
    composition = by[base + '/compose']['result']['decision']
    assert composition['source'] == by[base + '/composition-test']['sources']['candidate.py']
assert by['images/round-1/propose']['result']['candidates'][0]['source'] == by['images/round-1/compose']['result']['decision']['source']
keep = by['images/round-1/propose']['result']['candidates'][1]
assert keep['decision'] == 'KEEP'
assert keep['source'] == by['images/manual-residual']['sources']['candidate.py']
assert by['images/round-2/propose']['result']['candidates'][0]['source'] == by['images/round-2/compose']['result']['decision']['source']

images = by['images/final-comparison']['result']['metrics_by_version']
measurement = by['goes/final-comparison']['result']['metrics_by_version']
for version in ('persistence', 'manual', 'agent'):
    assert f"{images[version]['error']:.6f}" in slides
    assert images[version]['examples'] == 199
for version in ('persistence', 'selected-model'):
    assert f"{measurement[version]['error']:.3f}" in slides
    assert measurement[version]['examples'] == 2694
assert '0.120769' not in slides
result = {
    'status': 'passed', 'source_matches': source_matches,
    'round_1_composition_selected_tested_a': True,
    'round_1_keep_source_unchanged': True,
    'round_2_composition_selected_tested_a': True,
    'workspace': study['workspace'],
    'image_errors': {name: row['error'] for name, row in images.items()},
    'image_skill_vs_persistence': {name: row['skill_vs_persistence'] for name, row in images.items()},
    'agent_relative_error_reduction_vs_manual': 1 - images['agent']['error'] / images['manual']['error'],
    'measurement_errors': {name: row['error'] for name, row in measurement.items()},
    'image_windows': 199, 'measurement_windows': 2694,
    'independent_trials': 1, 'provider_calls': 0, 'training_runs': 0,
}
(root / 'notes/recorded-evidence-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
