import numpy as np
import pytest
from forge_workshop_kit import inspection, inspection_teaching as teaching


def data():
    return {'records': [{'case_id': str(i), 'partition': p, 'label': i % 2} for i, p in enumerate(['fit'] * 4 + ['review'] * 2 + ['validation'] * 2 + ['test'] * 2)],
            'whole': np.random.default_rng(4).normal(size=(10, 3)).astype('float32'),
            'patches': np.random.default_rng(5).normal(size=(10, 2, 2, 2)).astype('float32')}


def test_exercises_and_starters():
    teaching.check_features(teaching.FEATURE_SOLUTION)
    teaching.check_threshold(teaching.THRESHOLD_SOLUTION)
    teaching.check_review(teaching.REVIEW_SOLUTION)
    for check, starter in [(teaching.check_features, teaching.FEATURE_STARTER), (teaching.check_threshold, teaching.THRESHOLD_STARTER), (teaching.check_review, teaching.REVIEW_STARTER)]:
        with pytest.raises(NotImplementedError):
            check(starter)


def test_test_and_validation_never_train():
    fixture = data()
    for index in [6, 8]:
        with pytest.raises(ValueError, match='Training can only'):
            inspection.fit_classifier(fixture, [0, 1, index])
    with pytest.raises(ValueError, match='counted twice'):
        inspection.fit_classifier(fixture, [0, 1, 1])


def test_saved_classifier_reproduces_scores(tmp_path):
    fixture = data()
    fitted = inspection.fit_classifier(fixture, [0, 1, 2, 3], 'patch')
    path = tmp_path / 'model.npz'
    inspection.save_classifier(path, fitted, .3)
    loaded = inspection.load_classifier(path)
    assert loaded['threshold'] == .3
    np.testing.assert_allclose(inspection.score(fixture, [6, 7], fitted), inspection.score(fixture, [6, 7], loaded))


def test_review_has_equal_budget_and_no_duplicates():
    rows, values = np.arange(10), np.arange(10.)
    for method in ['active', 'random']:
        selected = inspection.select_review(values, rows, 3.1, 3, method, 17)
        assert len(selected) == len(set(selected)) == 3
    assert set(inspection.select_review(values, rows, 3.1, 3, 'active', 17)) == {2, 3, 4}


def test_metrics_keep_review_separate_from_detection():
    result = inspection.metrics([1, 1, 0, 0], [.9, .3, .6, .1], .5, review_margin=.21)
    assert result['misses'] == result['false_alarms'] == 1
    assert result['defect_recall'] == result['false_alarm_rate'] == .5
    assert result['review_count'] == 2
    assert result['auto_pass_misses'] == 0
    with pytest.raises(ValueError, match='finite'):
        inspection.metrics([1, 0], [float('nan'), .2], .5)


def test_nearest_patch_model_reproduces_and_does_not_match_itself(tmp_path):
    fixture = data()
    model = inspection.fit_classifier(fixture, [0, 1, 2, 3], 'nearest-patch', C=.03)
    errors = inspection.nearest_patch_errors(fixture, np.array([0]), model['reference'])
    assert np.all(errors > 0), 'A training board must not get a zero-distance self-match.'
    path = tmp_path / 'nearest.npz'
    inspection.save_classifier(path, model, -.2)
    np.testing.assert_allclose(inspection.score(fixture, [8, 9], model), inspection.score(fixture, [8, 9], inspection.load_classifier(path)))


def test_typed_media_are_copied_and_relative(tmp_path):
    import hashlib
    from PIL import Image
    fixture = data()
    source = tmp_path / 'data'
    source.mkdir()
    for i, row in enumerate(fixture['records']):
        path = source / f'{i}.png'
        Image.new('RGB', (10, 10), (i, 0, 0)).save(path)
        row.update(image=path.name, image_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), source_sha256='source-hash', mask=None, mask_sha256=None)
    fixture.update(root=source, manifest={'encoder':'test'})
    model = inspection.fit_classifier(fixture, [0, 1, 2, 3])
    output = inspection.prediction_rows(fixture, [8, 9], model, 0, destination=tmp_path / 'saved/media', root=tmp_path)
    assert output[0]['input']['path'] == 'saved/media/8.png'
    assert output[0]['input']['_workshop_type'] == 'image'
    (source / '8.png').write_bytes(b'changed')
    with pytest.raises(ValueError, match='changed'):
        inspection.prediction_rows(fixture, [8], model, 0)
