"""Candidate subprocess. Receives training labels and prediction inputs, never test labels."""
import importlib.util
import json
import sys
from pathlib import Path
import numpy as np
import torch


def main():
    request=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    torch.set_num_threads(2)
    torch.manual_seed(request['config'].get('seed',17))
    spec=importlib.util.spec_from_file_location('learner_candidate',request['source'])
    code=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(code)
    data=np.load(request['data'],allow_pickle=False)
    model=code.build_model(data['predict_x'].shape[1:],request['config'])
    if request.get('weights'):
        model.load_state_dict(torch.load(request['weights'],map_location='cpu',weights_only=True))
        losses=[]
    else:
        losses=code.fit(model,*[torch.tensor(data[k],dtype=torch.float32)
                               for k in ['train_x','train_y','train_mask']],request['config'])
    model.eval()
    with torch.no_grad():
        predictions=np.concatenate([model(torch.tensor(data['predict_x'][i:i+16],dtype=torch.float32)).numpy()
                                    for i in range(0,len(data['predict_x']),16)])
    np.save(request['prediction'],predictions)
    torch.save(model.state_dict(),request['output_weights'])
    Path(request['losses']).write_text(json.dumps(losses,allow_nan=False), encoding="utf-8", newline="\n")

if __name__=='__main__':
    main()
