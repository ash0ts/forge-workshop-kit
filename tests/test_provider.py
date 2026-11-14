import concurrent.futures

import httpx
import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.provider import MODEL, Provider, ProviderStop


def provider(tmp_path, monkeypatch, response, budget=8):
    monkeypatch.setattr('forge_workshop_kit.provider.credentials',lambda:'test-credential')
    session=WorkshopSession('person/lab','test',state_dir=tmp_path,budget_usd=budget)
    return Provider(session,transport=httpx.MockTransport(response),sleeper=lambda _:None)


def test_missing_usage_retains_reservation_and_reuses_response(tmp_path,monkeypatch):
    calls=[]
    def response(request):
        calls.append(request)
        return httpx.Response(200,json={'model':MODEL,'choices':[{'message':{'content':'{}'}}]})
    p=provider(tmp_path,monkeypatch,response)
    first=p.complete('one',[{'role':'user','content':'hello'}])
    assert first['observed_usd'] is None and first['unknown_usd']>0
    assert p.complete('one',[{'role':'user','content':'hello'}])==first
    assert len(calls)==1
    assert calls[0].headers['OpenAI-Project']=='person/lab'


def test_retry_limit_and_circuit_breaker(tmp_path,monkeypatch):
    calls=[]
    def failure(request):
        calls.append(request)
        return httpx.Response(500,json={'error':'unavailable'})
    p=provider(tmp_path,monkeypatch,failure)
    with pytest.raises(ProviderStop): p.complete('one',[])
    assert len(calls)==3
    with pytest.raises(ProviderStop,match='cooling'): p.complete('two',[])
    assert len(calls)==3
    assert p.summary()['bounded_unknown_usd']>0


def test_model_mismatch_stops_future_calls(tmp_path,monkeypatch):
    p=provider(tmp_path,monkeypatch,lambda _:httpx.Response(200,json={'model':'other','choices':[{}]}))
    with pytest.raises(ProviderStop,match='model'): p.complete('one',[])
    with pytest.raises(ProviderStop,match='model'): p.complete('two',[])


def test_concurrent_reservations_cannot_exceed_allowance(tmp_path,monkeypatch):
    p=provider(tmp_path,monkeypatch,lambda _:httpx.Response(200,json={'model':MODEL,'choices':[{}]}),budget=.005)
    def call(i):
        try: return p.complete(str(i),[])
        except ProviderStop: return None
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(call,range(4)))
    assert sum(r is not None for r in rows)==1
    assert sum(p.summary().values())<=.005


def test_32k_output_is_reserved_and_larger_requests_are_rejected(tmp_path,monkeypatch):
    calls=[]
    def response(request):
        calls.append(request)
        return httpx.Response(200,json={'model':MODEL,'choices':[{'message':{'content':'{}'}}]})
    p=provider(tmp_path,monkeypatch,response)
    record=p.complete('large',[],max_tokens=32768)
    assert record['request']['max_tokens']==32768
    assert record['reserved_usd']==pytest.approx((4098*.12 + 32768*.38)/1e6)
    assert record['unknown_usd']==record['reserved_usd']
    with pytest.raises(ValueError,match='32768'):
        p.complete('too-large',[],max_tokens=32769)
    assert len(calls)==1
