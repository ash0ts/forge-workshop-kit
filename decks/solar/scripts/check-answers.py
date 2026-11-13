"""Exercise the worked-answer snippets against public, deterministic examples."""
from pathlib import Path
import json,re
import numpy as np
import torch
from types import SimpleNamespace
root=Path(__file__).resolve().parents[1]
slides=json.loads((root/'notes/slide-map.json').read_text())['slides']
by={s['key']:s for s in slides}
ns={'np':np}
for key in ('answer-persistence','answer-flux','answer-images','answer-evidence'):
    block=re.search(r'```python\n(.*?)\n```',by[key]['body'],re.S).group(1)
    exec(compile(block,key,'exec'),ns)
x=np.array([[2.],[4.]])
y=ns['persistence_forecast']({'persistence':x,'y':np.array([[999.],[999.]])})
assert np.array_equal(y,x)
y[0,0]=0
assert x[0,0]==2
assert ns['my_flux_mae'](np.array([-2.,2.]),np.zeros(2))==2
mask=np.array([[[[1.,1.],[0.,0.]]],[[[1.,1.],[1.,1.]]]])
target=np.zeros_like(mask)
assert ns['my_image_mae'](np.ones_like(mask),target,mask)==1
outside=1-mask
assert ns['my_image_mae'](outside,target,mask)==0
# Each image has equal weight despite different valid-pixel counts.
prediction=np.stack([np.full((1,2,2),2.),np.full((1,2,2),4.)])
assert ns['my_image_mae'](prediction,target,mask)==3
assert 'final_error' not in ns['select_validation_evidence']({'split':'validation','config':{},'final_error':1})
try:
    ns['select_validation_evidence']({'split':'test','metrics':{'error':0}})
except ValueError:
    pass
else:
    raise AssertionError('Test evidence was accepted')
tensor = torch.tensor([1., 3.], requires_grad=True)
loss = ns['training_loss'](tensor, torch.zeros(2), torch.tensor([1., 0.]))
assert float(loss.detach()) == 1.0
loss.backward()
assert torch.equal(tensor.grad, torch.tensor([2., 0.]))
residual = re.search(r'```python\n(.*?)\n```', by['answer-residual']['body'], re.S).group(1)
exec(compile(residual,'answer-residual','exec'), ns)
inputs = torch.randn(2,2,4,4)
model = SimpleNamespace(net=lambda x: torch.zeros_like(x[:,1:2]))
ns['architecture']='residual'
assert torch.equal(ns['forward'](model,inputs),inputs[:,1:2])
ns['architecture']='conv'
assert torch.equal(ns['forward'](model,inputs),torch.zeros_like(inputs[:,1:2]))
result={'training_loss':'masked squared error and gradient', 'residual':'zero correction reproduces latest image', 'evidence':'allowlist and test-split rejection','persistence':'latest observation, detached result, no target use','flux':'sign, zero, constant error','image':'mask exclusion, constant error, equal example weighting','provider_calls':0,'training_runs':0}
(root/'notes/answer-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
