<script setup>
import { computed, ref } from 'vue'
import facts from '../data/concept-evidence.json'
const props=defineProps({kind:String,step:{type:Number,default:1}})
const threshold=ref(.5)
const row=facts.review[3]
const policy=computed(()=>{
 const rows=facts.policy_predictions, accepted=rows.filter(r=>r.confidence>=threshold.value)
 return {n:accepted.length,coverage:accepted.length/rows.length,accuracy:accepted.length?accepted.filter(r=>r.correct).length/accepted.length:null}
})
const snippets={
 representation:['TfidfVectorizer(', '  ngram_range=(1, 2),', '  sublinear_tf=True', ')', '', '# Or: frozen MiniLM features', 'X.shape == (8463, 384)'],
 fit:['head = make_classifier()', 'head.fit(X_train, y_train)', 'p = head.predict_proba(X)', 'choice = head.classes_[', '    p.argmax(axis=1)', ']'],
 metrics:['tp = correct_for_this_intent', 'fp = wrong_routes_to_it', 'fn = requests_sent_elsewhere', 'precision = tp / (tp + fp)', 'recall = tp / (tp + fn)', 'f1 = 2*tp / (2*tp + fp + fn)', 'macro_f1 = mean(intent_f1s)'],
 policy:['confidence = probabilities.max()', 'margin = largest - second_largest', '', 'def needs_review(confidence, t):', '    return confidence < t', '', '# Labeling candidates:', 'sorted(rows, key=lambda r:', '    (r["margin"], r["case_id"]))'],
 judge:['# Route 8 validation requests:', 'route_messages(text, intents)', '', '# Judge reviewed classifier routes:', '{"request": text,', ' "proposed_intent": proposed,', ' "needs_review": False}', '', '# Compare after judging:', 'failed = proposed != accepted'],
 review:['review = {', '  "case_id": case_id,', '  "proposed_label": predicted,', '  "accepted_label": yours,', '  "reviewer": your_name,', '  "label_source": "human_review",', '  "verified": True', '}', '# Only accepted review-pool rows', '# may extend the training set.'],
 freeze:['saved = {', '  "model": classifier_file,', '  "policy_source": review_code,', '  "threshold": chosen_threshold,', '  "training_ids": training_ids,', '  "source": classifier_code', '}', '# Final predictions use saved files.']}
const active=computed(()=>({representation:props.step===1?[0,1,2,3]:[5,6],fit:props.step===1?[0]:props.step===2?[1]:[2,3,4,5],metrics:props.step===1?[0,1,2]:[3,4,5,6],policy:props.step===1?[0,3,4]:[1,6,7,8],judge:props.step===1?[0,1]:[3,4,5,6,8,9],review:props.step===1?[1,2]:[3,4,5,6,8,9],freeze:props.step===1?[1,2,3]:[4,5,7]}[props.kind]||[]))
</script>
<template>
<div class="walk-layout">
 <div class="walk-visual">
  <template v-if="kind==='representation'">
   <div class="walk-request">“My card isn't here yet.”</div>
   <svg viewBox="0 0 640 255" role="img" :aria-label="step===1?'The request becomes words and adjacent word pairs, then a sparse TF–IDF row.':'The same request becomes a fixed 384-value sentence vector; the classifier learns from these values.'">
    <template v-if="step===1">
     <text x="20" y="35" class="label">Words and adjacent pairs</text>
     <g v-for="(s,i) in ['my','card','isn','here','yet']" :key="s"><rect :x="20+i*121" y="55" width="109" height="47" rx="6"/><text :x="32+i*121" y="85">{{s}}</text></g>
     <text x="20" y="145">my card · card isn · isn here · here yet</text>
     <path d="M310 160V190"/><text x="20" y="230">One sparse row in the training vocabulary</text>
    </template>
    <template v-else>
     <rect x="20" y="30" width="245" height="85" rx="8"/><text x="40" y="65">Frozen MiniLM</text><text x="40" y="95" class="small">encoder weights stay fixed</text>
     <path d="M280 72H350"/><rect x="365" y="30" width="250" height="85" rx="8"/><text x="385" y="65">384 values</text><text x="385" y="95" class="small">one row per request</text>
     <g v-for="i in 24" :key="i"><rect :x="20+(i-1)*25" y="165" width="18" height="38" :class="i%3===0?'accent':'muted'"/></g>
     <text x="20" y="245" class="small">Schematic vector: these are not plotted embedding values.</text>
    </template>
   </svg>
   <p>{{step===1?'Fit vocabulary and IDF weights on training text only. Tokenization drops the one-letter t; we are showing the actual default token pattern.':'The cache saves encoding time. Only the classifier on top of these vectors is trained in this workshop.'}}</p>
  </template>
  <template v-else-if="kind==='fit'">
   <svg viewBox="0 0 640 310" role="img" aria-label="Construct an unfitted estimator, fit its weights using labeled training vectors, then predict probabilities for new inputs.">
    <g v-for="(title,i) in ['Construct the estimator','Fit its classifier weights','Predict a new request']" :key="title" :opacity="i+1<=step?1:.3">
     <rect x="20" :y="10+i*101" width="600" height="83" rx="7" :class="i+1===step?'accent':''"/>
     <text x="40" :y="43+i*101">{{i+1}} · {{title}}</text>
     <text x="40" :y="73+i*101" class="small">{{['C=10 · max_iter=1000 · random_state=17','8,463 labeled rows → learned coefficients','one input vector → 77 probabilities → one intent'][i]}}</text>
    </g>
   </svg>
   <p>{{step===1?'Returning a classifier does not train it. C controls regularization; max_iter limits the optimizer.':step===2?'The two representations use the same labeled messages and classifier settings. Their feature dimensions differ.':'The probabilities support a review policy. They are model outputs, not calibrated guarantees.'}}</p>
  </template>
  <template v-else-if="kind==='metrics'">
   <p class="walk-label">Recorded test predictions · {{facts.metric.intent}}</p>
   <div class="count-grid"><div><strong>{{facts.metric.tp}}</strong>right routes<br><small>TP</small></div><div><strong>{{facts.metric.fp}}</strong>wrong arrivals<br><small>FP</small></div><div><strong>{{facts.metric.fn}}</strong>sent elsewhere<br><small>FN</small></div></div>
   <div v-if="step>1" class="walk-values"><p>Precision: {{facts.metric.precision.toFixed(3)}} · Recall: {{facts.metric.recall.toFixed(3)}}</p><p>F1: {{facts.metric.f1.toFixed(3)}}</p><div class="mini-bars"><i v-for="(v,i) in facts.intent_f1s" :key="i" :style="{height:(v*88)+'px'}"/></div><p class="small">77 intent F1 scores → macro-F1 {{facts.macro_f1.toFixed(6)}}</p></div>
   <p v-else>Count all predictions before calculating the score. A request sent to the wrong intent creates a false positive there and a false negative for its correct intent.</p>
  </template>
  <template v-else-if="kind==='policy'">
   <div class="walk-request">“{{row.text}}”</div>
   <div class="prob-row"><span>card_arrival</span><b>{{row.confidence.toFixed(3)}}</b><i :style="{width:row.confidence*310+'px'}"/></div>
   <div class="prob-row"><span>card_delivery_estimate</span><b>{{(row.confidence-row.margin).toFixed(3)}}</b><i :style="{width:(row.confidence-row.margin)*310+'px'}"/></div>
   <template v-if="step===1"><label class="slider-label">Review threshold {{threshold.toFixed(2)}}<input aria-label="Routing review threshold" type="range" min="0" max="1" step=".05" v-model.number="threshold"/></label><p><b>{{row.confidence<threshold?'Send this request to a person':'Route this request automatically'}}</b></p><p class="small">Recorded 770 validation predictions: {{policy.n}} routed ({{(policy.coverage*100).toFixed(1)}}%); accuracy among routed {{policy.accuracy===null?'unavailable':(policy.accuracy*100).toFixed(1)+'%'}}.</p></template>
   <template v-else><p class="walk-callout">Margin = {{row.confidence.toFixed(3)}} − {{(row.confidence-row.margin).toFixed(3)}} = {{row.margin.toFixed(3)}}</p><p>Small margins identify close choices to review for labeling. This is a different rule from the automatic-routing threshold.</p></template>
   <p class="small">Saved review-pool example. Moving the slider performs no model call.</p>
  </template>
  <template v-else-if="kind==='judge'">
   <div class="lane"><b>Routing demonstration</b><p>8 validation messages → fixed model → typed routing decisions</p><small>Open an actual model request in Agent Lens.</small></div>
   <div class="lane" :class="{faded:step<2}"><b>Judge alignment exercise</b><p>Reviewed classifier proposal → judge → compare with your accepted label</p><small>The judge never sees your accepted label. These are separate cases and calls.</small></div>
   <div v-if="step>1" class="judge-outcomes"><span>Malformed<br>response validation fails</span><span>Valid but disagrees<br>inspect its reasoning</span><span>Unavailable<br>keep judgment missing</span></div>
  </template>
  <template v-else-if="kind==='review'">
   <div class="walk-request">One request, one saved review record</div>
   <div class="record-row"><span>Proposed label</span><b>Classifier output</b></div><div class="record-row"><span>Published label</span><b>Dataset annotation</b></div>
   <div class="record-row" :class="{faded:step<2}"><span>Accepted label</span><b>Your explicit decision</b></div>
   <div v-if="step>1" class="lane"><b>8,463 training rows + accepted review rows</b><p>Refit the classifier. Keep encoder weights fixed.</p><small>Validation chooses the version. Test requests stay out.</small></div>
   <p>Reference examples are available for teaching. They do not become attendee reviews merely by appearing on a slide.</p>
  </template>
  <template v-else-if="kind==='freeze'">
   <svg viewBox="0 0 640 300" role="img" aria-label="The selected release saves classifier, preprocessing, review policy and source. Matching cases are then evaluated with those files.">
    <rect x="20" y="15" width="600" height="175" rx="8"/><text x="43" y="53">Selected router</text>
    <text x="43" y="95" class="small">Weights + vectorizer or frozen encoder identity</text><text x="43" y="130" class="small">Review code + threshold</text><text x="43" y="165" class="small">Training IDs + source + selection reason</text>
    <g v-if="step>1"><path d="M320 200V225"/><text x="25" y="267">Same 3,080 test requests → aligned predictions</text></g>
   </svg>
   <p>{{step===1?'Choose using validation results. A label change, model change and review-policy change are three different interventions.':'In EvalTables, compare the same request. In the summary, separate macro-F1 from coverage and selective accuracy.'}}</p>
  </template>
 </div>
 <div class="walk-code"><span class="walk-label">Relevant implementation</span><pre><template v-for="(line,i) in snippets[kind]" :key="i"><span :class="{active:active.includes(i)}">{{line||' '}}</span></template></pre></div>
</div>
</template>
