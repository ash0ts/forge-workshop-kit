from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from forge_workshop_kit import media, solar, solar_teaching


def image_split():
    target = np.array([[[[0., 1.], [2., 3.]]], [[[1., 2.], [3., 4.]]]], dtype=np.float32)
    return {'y': target, 'x': np.concatenate([target - 2, target - 1], axis=1),
            'mask': np.array([[[[0, 1], [1, 1]]]] * 2, dtype=bool),
            'persistence': target - 1,
            'ids': np.array(['2014-02-13T01:00', '2014-02-13T01:12'])}


def test_typed_forecasts_preserve_scores_and_share_display_scales(tmp_path):
    split = image_split()
    predictions = {'persistence': split['persistence'], 'candidate': split['y'].copy()}
    # A large off-disk error is visible in the prediction, but excluded from MAE.
    predictions['candidate'][:, 0, 0, 0] = 12
    old = {name: solar.evaluation_rows(values, split, evidence={'stage': name})
           for name, values in predictions.items()}
    rows = solar_teaching.image_comparison_rows(predictions, split, media_dir=tmp_path / 'media',
                                                media_root=tmp_path, saved_rows=old)
    for name, values in rows.items():
        for i, row in enumerate(values):
            assert row['error'] == old[name][i]['error']
            assert row['evidence'] == old[name][i]['evidence']
            assert row['prediction']['mean'] == old[name][i]['prediction']['mean']
            for receipt in (row['input']['current_image'], row['input']['one_hour_ago'],
                            row['prediction']['image'], row['prediction']['absolute_error'],
                            row['target']['image'], row['target']['disk_mask']):
                assert media.is_image(receipt)
                assert not Path(receipt['path']).is_absolute()
                assert receipt['width'] == receipt['height'] == 2
                media.checked_image(media.bind_root(receipt, tmp_path))
    assert [r['error'] for r in rows['candidate']] == [0., 0.]
    for baseline, candidate in zip(rows['persistence'], rows['candidate']):
        assert baseline['input'] == candidate['input']
        assert baseline['target'] == candidate['target']
        assert baseline['prediction']['display_scale'] == candidate['prediction']['display_scale']
    # Matplotlib shows the low-index row at the bottom; native media must agree.
    from matplotlib import colormaps
    row = rows['candidate'][0]
    scale = row['prediction']['display_scale']
    normalized = (predictions['candidate'][0, 0] - scale['intensity_min']) / (scale['intensity_max'] - scale['intensity_min'])
    with Image.open(tmp_path / row['prediction']['image']['path']) as image:
        np.testing.assert_array_equal(np.asarray(image), colormaps['magma'](np.flipud(normalized), bytes=True))


def test_media_regeneration_reuses_files_and_rejects_mismatched_saved_results(tmp_path):
    split = image_split()
    predictions = {'candidate': split['y'].copy()}
    old = {'candidate': solar.evaluation_rows(predictions['candidate'], split)}
    first = solar_teaching.image_comparison_rows(predictions, split, media_dir=tmp_path / 'media',
                                                media_root=tmp_path, saved_rows=old)
    files = {path: path.stat().st_mtime_ns for path in (tmp_path / 'media').iterdir()}
    second = solar_teaching.image_comparison_rows(predictions, split, media_dir=tmp_path / 'media',
                                                 media_root=tmp_path, saved_rows=old)
    assert first == second
    assert files == {path: path.stat().st_mtime_ns for path in (tmp_path / 'media').iterdir()}
    old['candidate'][0]['case_id'] = 'a different timestamp'
    with pytest.raises(ValueError, match='timestamps'):
        solar_teaching.image_comparison_rows(predictions, split, media_dir=tmp_path / 'media',
                                             media_root=tmp_path, saved_rows=old)


def test_measurement_and_legacy_image_rows_remain_compatible():
    image = image_split()
    legacy = solar.evaluation_rows(image['persistence'], image)
    assert legacy[0]['prediction'] == {'mean': 0.5, 'file_index': 0}
    assert legacy[0]['input'] == {'forecast_origin': '2014-02-13T01:00'}
    split = {'y': np.array([[1.], [3.]]), 'mask': np.ones((2, 1)),
             'ids': np.array(['one', 'two']), 'persistence': np.array([[2.], [2.]])}
    rows = solar.evaluation_rows(split['persistence'], split)
    assert rows[0] == {'case_id': 'one', 'input': {'forecast_origin': 'one'},
                        'prediction': [2.], 'target': [1.], 'error': 1., 'evidence': {}}
