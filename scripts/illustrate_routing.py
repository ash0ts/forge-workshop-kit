"""Draw routing mechanics using messages, feature arrays and ordered label columns."""
from __future__ import annotations
import json
import math
from illustrate_airline import Drawing,ROOT,PAPER,INK,MUTED,LINE,PANEL,ORANGE,BLUE,emit,document,write_hero

MESSAGE='What is the status of my card’s delivery?'

def message(d,x,y,w=600,small=False):
    h=88 if small else 112
    d.path(f'M{x},{y}H{x+w}V{y+h-18}H{x+38}L{x+18},{y+h}V{y+h-18}H{x}Z',INK,PAPER,2)
    d.text(x+18,y+29,'official-train/00021 · card_arrival',16,mono=True,fill=MUTED)
    d.text(x+18,y+64,MESSAGE,20 if small else 24,600)

def cells(d,x,y,labels,values=None,w=120,active=None):
    for j,label in enumerate(labels):
        xx=x+j*w
        d.rect(xx,y,w,62,ORANGE if j==active else PAPER,INK,1.5)
        d.text(xx+w/2,y+37,values[j] if values else f'p{j}',22,600,anchor='middle',mono=True)
        d.text(xx+w/2,y+87,label,17,anchor='middle',mono=True)
        d.text(xx+w/2,y-11,f'[{j}]',16,anchor='middle',mono=True,fill=MUTED)

def matrix(d,x,y,cols,rows,cw=12,ch=12,pattern=True):
    # Continuous signed schematic values; no binary or measured-embedding claim.
    for r in range(rows):
        for c in range(cols):
            k=r*cols+c
            value=[0.12,-0.08,0.31][k] if k<3 else math.sin(k*0.71)*0.8
            shade=round(180-value*68) if pattern else 226
            d.rect(x+c*cw,y+r*ch,cw-2,ch-2,f"rgb({shade},{shade},{shade})",stroke='none')

def figure_overview(d,i):
    message(d,40,111,700)
    d.text(825,143,'77 possible intents',25,600)
    d.text(825,176,'One queue destination',21)
    d.path('M200,225V268H205V296',INK,sw=2,arrow=True);d.path('M200,268H620V296',INK,sw=2,arrow=True)
    d.text(40,293,'WORDS',18,600,fill=MUTED)
    for j,t in enumerate(['card','delivery','card delivery']):
        d.rect(40+j*140,312,125,39,PANEL,INK);d.text(103+j*140,338,t,16,anchor='middle',mono=True)
    d.text(40,383,'Sparse TF–IDF features',21,600)
    matrix(d,620,312,32,4,14,13)
    d.text(620,397,'384-value vector (partial view)',21,600)
    if i>=1:
        d.line(240,408,240,442,INK,2,arrow=True);d.line(835,408,835,442,INK,2,arrow=True)
        d.text(115,475,'fit classifier → scores',20,mono=True)
        d.text(710,475,'fit classifier → scores',20,mono=True)
    if i>=2:
        d.line(478,477,666,477,INK,1.5,'5 4')
        d.text(855,515,'Compare the same requests',20,anchor='middle')
    if i>=3:
        d.text(40,525,'Save model + preprocessing + intent order',18,600)
    d.code(['scores = fitted["model"].predict_proba(inputs)','labels = fitted["model"].classes_'],['Learn from reviewed mistakes.','Test release behavior on matching cases.'])

def figure_features(d,i):
    message(d,40,105,770,True)
    d.text(855,137,'Same text',22,600);d.text(855,169,'Two separate models',20)
    d.path('M425,196V214H250V224',INK,sw=2,arrow=True);d.path('M425,214H865V224',INK,sw=2,arrow=True)
    d.text(40,252,'TF–IDF',25,600,fill=BLUE)
    d.text(655,252,'FROZEN SENTENCE ENCODER',22,600,fill=ORANGE)
    # Vocabulary slots depict sparsity; term weights are symbols rather than invented measurements.
    terms=['card','delivery','card delivery','cash','pin','…']
    for j,t in enumerate(terms):
        y=293+j*32
        d.text(40,y,t,18,mono=True)
        d.rect(235,y-23,253,27,PAPER,LINE)
        width=[175,213,134,0,0,40][j]
        if width and i>=1:d.rect(235,y-23,width,27,BLUE if j<3 else PANEL,stroke='none')
        d.text(505,y,(f'w{j}' if j<3 else '0' if j<5 else '…') if i>=1 else '—',17,mono=True)
    d.text(40,516,'Terms shown; bar lengths are schematic.',18,fill=MUTED)
    matrix(d,655,280,32,12,14,14,pattern=i>=2)
    d.text(655,483,'[+0.12, −0.08, +0.31, …]',18,mono=True)
    d.text(655,516,'Schematic values; the encoder stays frozen.',18)
    if i==0:d.code(['text = request["text"]'],['Both paths receive the same request.','Reference label: card_arrival.'])
    elif i==1:d.code(['model = make_pipeline(vectorizer, head)','model.fit(texts, labels)'],['Vocabulary + weights fit on training text.','Zero means this term is absent.'])
    elif i==2:d.code(['features.shape  # (n_requests, 384)','head.fit(features, labels)'],['The encoder stays frozen.','The classification head is fitted.'])
    else:d.code(['a = predict(word_model, data, "validation")','b = predict(sentence_model, data, "validation")'],['Same request IDs, separate predictions.','Neither representation feeds the other.'])

def figure_decision(d,i):
    d.text(40,116,'Illustrative close-up: three of the model’s 77 intent columns',22,600)
    labels=['card_arrival','card_linking','activate_my_card']
    cells(d,60,190,labels,['0.72','0.18','0.10'],330,0)
    d.text(60,318,'Chosen route: card_arrival',25,600)
    d.line(60,373,1110,373,INK,2)
    for x,v in [(60,'0.0'),(585,'0.5'),(1110,'1.0')]:d.line(x,367,x,379,INK);d.text(x,409,v,18,anchor='middle',mono=True)
    # Shared probability axis shows distinct threshold and top-two margin.
    d.circle(249,373,7,PAPER,INK);d.text(249,348,'runner-up 0.18',18,anchor='middle')
    d.circle(816,373,8,ORANGE);d.text(816,348,'top 0.72',18,600,anchor='middle')
    if i>=1:
        d.line(900,333,900,448,INK,1.5,'5 4');d.text(900,481,'threshold 0.80',18,mono=True,anchor='middle')
        d.text(60,443,'0.72 < 0.80 → send to human review',22,600)
    if i>=2:
        d.path('M249,497V512H816V497',INK,sw=2);d.text(533,538,'Top-two margin = 0.72 − 0.18 = 0.54',20,anchor='middle')
    d.code(['defer = confidence < threshold','margin = top_probability - runner_up'],['Threshold controls routing coverage.','Margin describes competing predictions.'])

def figure_labels(d,i):
    message(d,40,109,730,True)
    d.text(850,140,'REVIEW POOL',18,600,fill=MUTED);d.text(850,174,'Eligible development case',19)
    d.text(40,244,'PREDICTION',18,600,fill=MUTED)
    d.text(40,282,'card_linking',27,600,fill=ORANGE)
    d.text(40,317,'Illustrative wrong route',18,fill=MUTED)
    d.line(310,278,415,278,INK,1.5,arrow=True)
    d.text(450,244,'HUMAN REVIEW',18,600,fill=MUTED)
    d.text(450,282,'card_arrival',27,600)
    d.text(450,317,'“Delivery status, not linking.”',20)
    if i>=1:
        d.line(450,336,755,336,ORANGE,2.5);d.text(450,369,'accepted label + reviewer + reason',18)
    if i>=2:
        document(d,850,221,300,'reviewed-example.json',['case_id','proposed_label','accepted_label'],True)
        d.line(770,278,830,278,INK,1.5,arrow=True)
    d.path('M40,419H190L210,400H1145V521H40Z',INK,PANEL,2)
    d.text(60,452,'dataset version',19,600)
    d.text(60,488,'request_id   original prediction   reviewer   accepted label   label_source',18,mono=True)
    d.code(['label_source = ("human_review" if verified', '                else "unverified_suggestion")'],['A proposed label remains a suggestion.','Only accepted examples enter training.'])

def figure_metrics(d,i):
    d.text(40,116,'Illustrative counts for one intent: card_arrival',23,600)
    d.text(550,152,'PREDICTED',18,600,fill=MUTED)
    d.text(515,187,'card_arrival',19,mono=True)
    d.text(790,187,'another intent',19,mono=True)
    d.text(40,273,'ACTUAL',18,600,fill=MUTED)
    d.text(205,270,'card_arrival',18,mono=True)
    d.text(205,406,'another intent',18,mono=True)
    for x,y,count,tag in [(450,208,8,'TP'),(730,208,2,'FN'),(450,344,2,'FP')]:
        d.rect(x,y,265,122,PAPER,INK)
        for j in range(count):d.circle(x+28+(j%4)*44,y+36+(j//4)*36,9,ORANGE if tag!='TP' else INK)
        d.text(x+239,y+98,f'{tag} = {count}',19,600,anchor='end',mono=True)
    d.rect(730,344,265,122,PANEL,INK);d.text(754,386,'True negatives',20);d.text(754,420,'Not in this F1 fraction',19)
    if i>=1:
        d.text(40,513,'F1 = 2TP / (2TP + FP + FN) = 16 / 20 = 0.8',25,600)

    if i>=2:
        d.text(1030,265,'× 77',27,600);d.text(1030,303,'intents',19);d.text(1030,349,'↓',28);d.text(1030,392,'mean',22,600)
    d.code(['f1_score(targets, predictions, labels=labels,','         average="macro", zero_division=0)'],['Calculate F1 separately for each intent.','Then average all 77 scores equally.'])

def figure_judge(d,i):
    d.path('M40,107H1150V180H80L60,199V180H40Z',INK,PAPER,2)
    d.text(60,134,'RECORDED REQUEST',16,600,fill=MUTED)
    d.text(60,166,'“Can I activate a card in the app?”',25,600)
    d.text(40,236,'ROUTER',18,600,fill=MUTED)
    d.text(40,271,'activate_my_card',25,600,mono=True)
    d.text(40,314,'DATASET REFERENCE',18,600,fill=MUTED)
    d.text(40,349,'card_linking',25,600,mono=True)
    d.line(572,213,572,365)
    d.text(640,236,'AUTOMATED REVIEWER',18,600,fill=MUTED)
    if i>=1:
        d.text(640,271,'{"failed": false, …}',25,mono=True)
        d.text(640,307,'Reason present; read the full native span.',20)
        d.text(640,341,'The schema is valid. Its verdict needs review.',20)
    else:d.text(640,278,'Inspect the request before the judgment.',20)
    d.line(40,380,1150,380)
    d.text(40,413,'Human review question',22,600)
    d.text(40,448,'Does “activate … in the app” mean activation or linking? The wording is ambiguous.',20)
    if i>=2:
        for x,head,val in [(40,'SCHEMA','Valid'),(385,'REVIEW','Unresolved'),(760,'IF NO RESPONSE','Unavailable — not a pass')]:
            d.text(x,487,head,17,600,fill=MUTED);d.text(x,519,val,21,600)
    d.code(['type(value["failed"]) is bool','bool(value["reason"].strip())'],['Reference disagreement calls for review.','It is not proof the judge is wrong.'])

def figure_release(d,i):
    d.text(40,116,'Probability columns keep their values. The faulty loader moves the labels.',22,600)
    d.text(40,153,'Illustrative probabilities and labels • the real drill rotates all 77 intents',18,fill=MUTED)
    # Three physical score columns remain fixed, while labels visibly move under them.
    for j,(x,h,p) in enumerate([(70,158.4,'0.72'),(390,39.6,'0.18'),(710,22,'0.10')]):
        d.rect(x,354-h,210,h,PANEL,INK,2)
        d.text(x+105,389,p,27,600,anchor='middle',mono=True)
        d.text(x+105,185,f'column {j}',18,anchor='middle',mono=True)
    d.text(40,430,'HEALTHY',18,600,fill=MUTED)
    for x,l in zip([175,495,815],['card_arrival','card_linking','activate_my_card']):d.text(x,466,l,18,anchor='middle',mono=True)
    d.text(40,505,'REPAIRED' if i>=2 else 'FAULTY' if i==1 else 'LOADER NOT RUN',18,600,fill=MUTED)
    for x,l in zip([175,495,815],['card_linking','activate_my_card','card_arrival'] if i==1 else ['card_arrival','card_linking','activate_my_card']):d.text(x,535,l if i else '—',18,600,fill=ORANGE if i==1 else INK,anchor='middle',mono=True)
    if i==1:
        d.path('M495,473Q345,492 175,511M815,473Q665,492 495,511',ORANGE,sw=2,arrow=True)
        d.path('M175,473C175,493 815,493 815,511',ORANGE,sw=1.5,arrow=True)
    d.line(960,176,960,528)
    d.text(985,217,'RECORDED DRILL',17,600,fill=MUTED)
    for y,label,val in [(269,'Healthy','71/77'),(352,'Faulty','0/77'),(435,'Repaired','71/77')]:
        d.text(985,y,label,20);d.text(985,y+33,val if i>=3 else '—',29,600,mono=True)
    d.text(985,519,'6 errors remain' if i>=3 else 'Review cohort',18)
    d.code(['healthy = list(model_classes)','faulty = labels[1:] + labels[:1]'],['Check both label membership and order.','Repair and rollback reproduce healthy.'])

if __name__=='__main__':
    emit('routing', {'overview':figure_overview,'features':figure_features,'decision':figure_decision,'labels':figure_labels,'metrics':figure_metrics,'judge':figure_judge,'release':figure_release})
    write_hero('routing',figure_overview)
