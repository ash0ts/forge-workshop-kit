"""Rebuild teaching values from frozen public data; no classifier fitting or paid calls."""
import json, hashlib, shutil
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[3]
from sklearn.feature_extraction.text import TfidfVectorizer
cases=json.loads((R/"data/banking77-v1/cases.json").read_text())
train=[r for r in cases if r['split']=='train']; row=next(r for r in cases if r['id']=='official-train/00023'); v=TfidfVectorizer(ngram_range=(1,2),sublinear_tf=True);v.fit([r['text'] for r in train]);a=v.transform([row['text']]); names=v.get_feature_names_out(); ix=a.indices
emb=np.load(R/'data/banking77-v1/embeddings.npy'); pos=cases.index(row)
f={'source':'data/banking77-v1/cases.json','source_sha256':hashlib.sha256((R/'data/banking77-v1/cases.json').read_bytes()).hexdigest(),'case_id':row['id'],'text':row['text'],'training_rows':len(train),'vocabulary_size':len(names),'tfidf':[{'token':str(names[i]),'idf':float(v.idf_[i]),'weight':float(a[0,i])} for i in ix],'embedding':[float(x) for x in emb[pos]],'embedding_source':'data/banking77-v1/embeddings.npy','embedding_source_sha256':hashlib.sha256((R/'data/banking77-v1/embeddings.npy').read_bytes()).hexdigest(),'embedding_note':'Actual cached all-MiniLM-L6-v2 output; coordinate index is not a word or category.'}
(R/'decks/routing/data/feature-example.json').write_text(json.dumps(f,indent=2)+'\n')
