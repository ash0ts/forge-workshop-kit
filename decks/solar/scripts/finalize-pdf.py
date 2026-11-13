"""Convert exported localhost slide links into internal PDF page links and inspect pages."""
from pathlib import Path
from urllib.parse import urlparse
import json
import pymupdf
root=Path(__file__).resolve().parents[1]
path=root/'solar-autoresearch.pdf'
doc=pymupdf.open(path)
expected=json.loads((root/'notes/slide-map.json').read_text())['total_slides']
assert len(doc)==expected,(len(doc),expected)
converted=0
image_links=0
for page in doc:
    for link in page.get_links():
        uri=link.get('uri','')
        parsed=urlparse(uri)
        if parsed.hostname in ('localhost','127.0.0.1'):
            destination=parsed.path.strip('/')
            if destination.isdigit() and 1<=int(destination)<=len(doc):
                area=link['from'];page.delete_link(link)
                page.insert_link({'kind':pymupdf.LINK_GOTO,'from':area,'page':int(destination)-1,'to':pymupdf.Point(0,0)})
                converted+=1
            elif destination.startswith('images/'):
                area=link['from'];page.delete_link(link)
                page.insert_link({'kind':pymupdf.LINK_URI,'from':area,'uri':'https://ash0ts.github.io/forge-workshop-kit/solar/'+destination})
                image_links+=1
            else:
                raise AssertionError('Unexpected localhost link: '+uri)
    assert page.get_text().strip(),'Empty PDF page'
if converted or image_links:
    temp=path.with_name('solar-autoresearch-linked.pdf');doc.save(temp);doc.close();temp.replace(path)
else:doc.close()
doc=pymupdf.open(path)
for i,page in enumerate(doc):
    for link in page.get_links():
        assert 'localhost' not in link.get('uri','')
    # Full-size rendering validates every exported page, not only Chromium's export return code.
    page.get_pixmap(matrix=pymupdf.Matrix(1,1)).save(root/'.screenshots'/f'pdf-{i+1:02}.png')
result={'pages':len(doc),'converted_internal_links':converted,'full_size_image_links':image_links,'all_pages_rendered':True,'empty_pages':0}
(root/'notes/pdf-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
