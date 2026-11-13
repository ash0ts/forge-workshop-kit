

def test_composition_normalizes_recorded_lessons_without_inventing_text():
    from forge_workshop_kit.research import normalize_composition
    original = {'decision': 'KEEP', 'lessons': [
        {'lesson': 'The candidate tied on validation.', 'limits': 'Only one seed was tested.'}]}
    normalized = normalize_composition(original)
    assert normalized['lesson'] == original['lessons'][0]['lesson']
    assert normalized['limits'] == original['lessons'][0]['limits']
    assert 'lesson' not in original
    assert normalized['lessons'] == original['lessons']
    assert 'no new inference' in normalized['lesson_normalization']


def test_composition_rejects_missing_or_unstructured_lessons():
    import pytest
    from forge_workshop_kit.research import normalize_composition
    for decision in ({}, {'lesson': 'It worked'}, {'lessons': ['It worked']},
                     {'lessons': [{'lesson': 'It worked', 'limits': None}]}):
        with pytest.raises(ValueError, match='lesson and its limits'):
            normalize_composition(decision)


def test_composition_rejects_test_parent_before_any_stage_or_request():
    import pytest
    from forge_workshop_kit.research import compose
    class NoExecution:
        def stage(self, *args, **kwargs):
            raise AssertionError('Rejected evidence must not start work')
    with pytest.raises(ValueError, match='Only validation'):
        compose(NoExecution(), 1, 'source', {'split': 'test'}, [{'split': 'validation'}])
