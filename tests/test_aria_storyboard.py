"""The deck uses recorded responses and keeps each stop beside its exercise."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('aria_storyboard',ROOT/'scripts/aria_storyboard.py')
storyboard=importlib.util.module_from_spec(spec)
spec.loader.exec_module(storyboard)


def test_handoff_renders_without_installed_participant_dependencies(tmp_path):
    # Match the deck CI job: no site-packages, editable installation, or cwd import.
    code = (
        "import runpy\n"
        f"storyboard = runpy.run_path({str(ROOT / 'scripts/aria_storyboard.py')!r})\n"
        "drawing = storyboard['_graphic']('pending', 'investigate', 2)\n"
        "assert '<svg' in drawing and 'Start ARIA investigation' in drawing\n"
    )
    subprocess.run([sys.executable, '-I', '-S', '-c', code], cwd=tmp_path,
                   check=True, capture_output=True, text=True)


def rows_for(deck):
    data=json.loads((ROOT/'decks'/deck/'notes/slide-map.json').read_text(encoding='utf-8'))
    rows=[]
    for row in data['slides']:
        # The maps omit authored body in some decks. Enrichment needs no execution.
        row={**row,'body':'Existing authored content','notes':row.get('notes',''),'kind':row.get('kind',''),'cls':row.get('cls','')}
        if row.get('name') and not row.get('key'):row['key']=row['name']
        rows.append(row)
    return [r for r in rows if not str(r.get('key','')).startswith('aria-')]


@pytest.mark.parametrize('deck',storyboard.SLUGS)
def test_two_stops_are_inserted_before_their_intervention_or_report(deck,tmp_path):
    rows=rows_for(deck)
    storyboard.enrich(rows,tmp_path,deck)
    for stop,anchor,_ in storyboard.PLACEMENTS[deck]:
        ids=[storyboard._key(r) for r in rows]
        assert ids.count(f'aria-{stop}')==1
        question=ids.index(f'aria-{stop}')
        assert ids[question:question+3]==[f'aria-{stop}',f'aria-{stop}-response',f'aria-{stop}-verify']
        assert storyboard._key(rows[question+3])==anchor or rows[question+3]['title']==anchor
        assert rows[question]['aria']['duration_minutes']==(8 if stop=='investigate' else 7)


def test_missing_recording_is_never_rendered_as_an_actual_response():
    result=storyboard._frame('pending','investigate',1,{'status':'unavailable','response':''},[])
    assert 'No usable recorded ARIA response' in result
    assert '<blockquote>' not in result


def test_recorded_claim_is_escaped_and_links_checked():
    pack={'status':'recorded','response':'Full actual response', 'claim_excerpt':'<script>bad</script>',
          'conversation_url':'javascript:alert(1)','citation_check':{'claim':'Claim','assessment':'unresolved','reason':'No source could establish it','record_url':'https://example.com/record'}}
    response=storyboard._frame('pending','investigate',1,pack,[])
    assert '<script>' not in response and 'javascript:' not in response
    verified=storyboard._frame('pending','investigate',2,pack,[])
    assert 'unresolved' in verified and 'https://example.com/record' in verified


def test_capture_cannot_escape_its_pack_directory(tmp_path):
    with pytest.raises(ValueError):
        storyboard._assets(tmp_path/'deck',{'captures':[{'path':'../secret.png'}]},tmp_path/'pack'/'investigate.json','investigate')


def test_annotations_keep_the_original_capture_and_explain_marked_fields():
    shot={'url':'/aria/investigate/source.png','caption':'Actual native source','annotations':[dict(x=.5,y=.4,width=.4,height=.2,label='Validation metrics')]}
    output=storyboard._capture(shot)
    assert 'href="/aria/investigate/source.png"' in output
    assert 'fill="none"' in output and 'Validation metrics' in output
    assert 'style="font-size:14px;font-weight:600"' in output


def test_annotation_coordinates_must_fit_the_original_capture():
    with pytest.raises(ValueError):
        storyboard._capture({'url':'/source.png','annotations':[dict(x=.8,y=.4,width=.4,height=.2,label='Outside')]})


def test_capture_uses_the_shared_intrinsic_image_layout():
    output=storyboard._capture({'url':'/aria/conclusion/response.png','portrait':True})
    assert 'class="aria-screen"' in output


def test_capture_and_offline_links_follow_the_deck_deployment_prefix(monkeypatch):
    monkeypatch.setenv('DECK_BASE','/forge-workshop-kit/pending/')
    capture=storyboard._capture({'url':'/aria/investigate/source.png'})
    assert 'href="/forge-workshop-kit/pending/aria/investigate/source.png"' in capture
    assert 'src="/aria/investigate/source.png"' in capture
    pack={'status':'recorded','response':'Actual answer','transcript_paths':{'html':'investigate-transcript.html'}}
    response=storyboard._frame('pending','investigate',1,pack,[])
    assert 'href="/forge-workshop-kit/pending/aria/investigate/investigate-transcript.html"' in response


@pytest.mark.parametrize('deck',storyboard.SLUGS)
def test_recorded_frames_do_not_depend_on_windows_default_encoding(deck,monkeypatch):
    expected={}
    for stop in ('investigate','conclusion'):
        pack,_=storyboard._pack(deck,stop)
        expected[stop]=[storyboard._frame(deck,stop,phase,pack,[]) for phase in range(3)]

    original_open=Path.open
    def windows_text_open(path,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
        if 'b' not in mode and encoding in (None,'locale'):
            encoding='cp1252'
        return original_open(path,mode,buffering,encoding,errors,newline)
    monkeypatch.setattr(Path,'open',windows_text_open)

    for stop in ('investigate','conclusion'):
        pack,_=storyboard._pack(deck,stop)
        actual=[storyboard._frame(deck,stop,phase,pack,[]) for phase in range(3)]
        assert actual==expected[stop]
