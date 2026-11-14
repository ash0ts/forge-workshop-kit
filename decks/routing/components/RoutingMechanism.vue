<script setup>
import {computed,ref} from 'vue'
import evidence from '../data/concept-evidence.json'
import feature from '../data/feature-example.json'
const props=defineProps({kind:String,step:{type:Number,default:1}})
const threshold=ref(.5), example=evidence.review[3], review=evidence.review[0]
const accepted=computed(()=>evidence.policy_predictions.filter(r=>r.confidence>=threshold.value))
const bins=computed(()=>Array.from({length:20},(_,i)=>({left:i/20,n:evidence.policy_predictions.filter(r=>r.confidence>=i/20&&r.confidence<(i+1)/20).length})))
const weights=feature.tfidf
const code={vocabulary:['tokens = vectorizer.build_analyzer()(text)','row = vectorizer.transform([text])','# IDF fitted on training text only.','# Then normalize each row to length 1.'],vector:['X = cached_minilm_vectors','# Fixed encoder; 384 values per request.','head = make_classifier()','head.fit(X_train, y_train)'],fit:['head = make_classifier()','head.fit(X_train, y_train)','p = head.predict_proba(X_new)','intent = head.classes_[p.argmax(axis=1)]'],metrics:['tp, fp, fn = 34, 3, 6','precision = tp / (tp + fp)','recall = tp / (tp + fn)','f1 = 2*tp / (2*tp + fp + fn)','macro_f1 = mean(all_77_intent_f1s)'],policy:['confidence = probabilities.max()','needs_review = confidence < threshold','margin = largest - second_largest','# Margin ranks cases for labeling.'],review:['save_review(','    case_id=case_id,','    proposed_label=prediction,','    accepted_label=reviewer_choice,','    label_source="human_review",','    verified=True,',')'],judge:['response = ask_judge(', '    request, proposed_intent',')','validated = validate_judge(response)','# Only afterward: compare against review.','# Missing response stays None.'],freeze:['save(model, preprocessing, intent_order)','save(review_policy, training_ids, source)','# Reload the exact version.','predict(the_same_case_ids)'],rollback:['previous = load_exact(previous_artifact)','selected_version = previous','actual = predict(frozen_batch)','assert actual == saved_predictions']}
</script>
<template>
<div class="rm-layout">
<div class="rm-visual">
<svg v-if="kind==='vocabulary'" viewBox="0 0 660 440" role="img" aria-label="Actual request token weights from the 8,463-row training vocabulary; nine nonzero TF–IDF values occupy a 21,527-column sparse row.">
 <text x="10" y="28" class="heading">“My card isn't here yet.”</text>
 <text x="10" y="62" class="small">Actual training vocabulary · 21,527 columns</text>
 <g v-for="(item,i) in weights" :key="item.token">
  <text x="12" :y="103+i*31" class="mono">{{item.token}}</text>
  <rect x="180" :y="85+i*31" :width="item.weight*660" height="22" class="teal"/>
  <text :x="190+item.weight*660" :y="103+i*31" class="small">{{item.weight.toFixed(3)}}</text>
 </g>
 <text x="10" y="406" class="small">Length-normalized weights; all other columns are zero.</text>
 <text x="10" y="432" class="small">Rare terms get more IDF weight. This is not word importance to the model.</text>
</svg>
<svg v-else-if="kind==='vector'" viewBox="0 0 660 440" role="img" aria-label="Actual 384 cached MiniLM embedding coordinates shown in coordinate order; the encoder is fixed while a classifier on top is fitted.">
 <text x="12" y="28" class="heading">Same request, a dense representation</text>
 <text x="12" y="62" class="small">384 actual MiniLM coordinates · row-major order</text>
 <rect v-for="(v,i) in feature.embedding" :key="i" :x="12+i%24*20" :y="85+Math.floor(i/24)*13" width="18" height="11" :fill="v>=0?'#237a6c':'#c17b40'" :opacity=".15+Math.min(Math.abs(v)/.16,1)*.85"/>
 <text x="510" y="115" class="small">positive</text><rect x="510" y="130" width="105" height="17" fill="#237a6c"/>
 <text x="510" y="195" class="small">negative</text><rect x="510" y="210" width="105" height="17" fill="#c17b40"/><text x="510" y="268" class="small">clip at ±.16</text>
 <path d="M250 305V332H445V305" class="arrow"/>
 <text x="12" y="369" class="heading">Frozen encoder → trained classifier → 77 intents</text>
 <text x="12" y="406" class="small">A coordinate has no assigned word meaning.</text>
 <text x="12" y="432" class="small">Coordinates are shown in saved order, without projection.</text>
</svg>
<svg v-else-if="kind==='fit'" viewBox="0 0 660 440" role="img" aria-label="The classifier transforms a 384-value input using a 77 by 384 coefficient matrix and a 77-value intercept, producing 77 scores and probabilities. Training changes the coefficient matrix, not the frozen encoder.">
 <text x="12" y="28" class="heading">One input row</text><text x="12" y="59" class="small">384 values</text>
 <g v-for="i in 12" :key="i"><rect x="20" :y="78+i*15" width="70" height="11" :class="i%3?'teal':'pale'"/></g>
 <path d="M110 179H155" class="arrow"/><text x="190" y="58" class="heading">Classifier weights</text>
 <g v-for="i in 96" :key="i"><rect :x="178+i%12*17" :y="86+Math.floor(i/12)*22" width="14" height="18" :class="step>=2?(i%3?'teal':'gold'):'pale'"/></g>
 <text x="178" y="293" class="small">77 × 384 + 77 intercepts</text>
 <path d="M402 179H455" class="arrow"/>
 <g :opacity="step===3?1:.25"><text x="476" y="59" class="heading">Probabilities</text><rect v-for="(v,i) in [.71,.16,.08,.05]" :key="i" x="480" :y="96+i*47" :width="v*210" height="25" class="blue"/><text x="480" y="293" class="small">77 values sum to 1</text></g>
 <path v-if="step>=2" d="M90 327H350V280" class="training"/><text x="12" y="366" class="heading">{{step===1?'1 · Construct an unfitted estimator':step===2?'2 · Labeled rows update these weights':'3 · Predict using the learned weights'}}</text>
 <text x="12" y="405" class="small">Matrix cells and probability bars are schematic, not measured values.</text>
 <text x="12" y="432" class="small">8,463 labeled training rows · encoder weights remain fixed</text>
</svg>
<svg v-else-if="kind==='metrics'" viewBox="0 0 660 440" role="img" aria-label="For card arrival, 40 actual requests split into 34 correct routes and 6 misses. Three requests from other intents were wrongly sent here. Precision is 34 over 37, recall 34 over 40, and F1 68 over 77.">
 <text x="12" y="27" class="heading">Recorded card_arrival test predictions</text>
 <text x="12" y="69" class="small">40 requests really belong here</text>
 <g v-for="i in 40" :key="i"><rect :x="15+(i-1)%10*30" :y="87+Math.floor((i-1)/10)*30" width="23" height="23" :class="i<=34?'teal':'orange'"/></g>
 <text x="352" y="112" class="heading">34 correct routes</text><text x="352" y="147" class="small">TP · reached this queue</text><text x="352" y="185" class="heading">6 sent elsewhere</text><text x="352" y="220" class="small">FN · missed this queue</text>
 <g v-for="i in 3" :key="i"><rect :x="15+(i-1)*30" y="242" width="23" height="23" class="blue"/></g><text x="125" y="261" class="small">3 wrong arrivals from other intents · FP</text>
 <g v-if="step>1"><text x="12" y="310" class="heading">Precision 34 / 37 = .919</text><text x="352" y="310" class="heading">Recall 34 / 40 = .850</text><text x="12" y="353" class="heading">F1 = 68 / 77 = .883</text>
 <rect v-for="(v,i) in evidence.intent_f1s" :key="i" :x="12+i*8" :y="404-v*43" width="6" :height="v*43" class="teal"/><text x="12" y="430" class="small">F1 scale 0–1 · 77 intents · mean {{evidence.macro_f1.toFixed(6)}}</text></g>
 <text v-else x="12" y="331" class="small">One misroute is a false negative for its true intent</text><text v-if="step===1" x="12" y="360" class="small">and a false positive for its predicted intent.</text>
</svg>
<template v-else-if="kind==='policy'">
 <svg viewBox="0 0 660 330" role="img" aria-label="Actual saved classifier confidence scores and the top-two margin for one review case. A histogram of 770 validation confidences shows what a threshold accepts and defers.">
 <text x="12" y="26" class="heading">“{{example.text}}”</text>
 <text x="12" y="65" class="small">card_arrival</text><rect x="225" y="45" :width="example.confidence*600" height="27" class="teal"/><text x="544" y="66" class="small">{{example.confidence.toFixed(3)}}</text>
 <text x="12" y="111" class="small">card_delivery_estimate</text><rect x="225" y="91" :width="(example.confidence-example.margin)*600" height="27" class="blue"/>
 <path v-if="step>1" :d="`M${225+(example.confidence-example.margin)*600} 132V149H${225+example.confidence*600}V132`" class="training"/>
 <text v-if="step>1" x="278" y="181" class="small">Margin {{example.margin.toFixed(3)}} → rank labeling candidates</text>
 <text x="12" y="215" class="small">770 validation confidences · left of cutoff goes to review</text>
 <rect v-for="(b,i) in bins" :key="i" :x="15+i*30" :y="296-b.n/2.7" width="26" :height="b.n/2.7" :class="b.left>=threshold?'teal':'pale'"/>
 <path :d="`M${15+threshold*600} 222V307`" class="training"/><text x="12" y="321" class="small">0</text><text x="600" y="321" class="small">1.0</text>
 </svg>
 <label class="rm-slider">Automatic-routing cutoff {{threshold.toFixed(2)}}<input aria-label="Routing confidence cutoff" type="range" min="0" max="1" step=".05" v-model.number="threshold"/></label>
 <p class="rm-caption">{{accepted.length}} / 770 routed automatically ({{(accepted.length/770*100).toFixed(1)}}%). Moving this control sends no model request.</p>
</template>
<svg v-else-if="kind==='review'" viewBox="0 0 660 440" role="img" aria-label="The recorded card-linking example retains its model proposal, published reference, and separate human decision. Only a verified accepted decision can enter the additional training rows.">
 <text x="12" y="28" class="heading">“{{review.text}}”</text><text x="12" y="59" class="small">{{review.case_id}} · saved review-pool example</text>
 <path d="M48 82V225H90M48 140H90" class="arrow"/>
 <text x="105" y="111" class="small">Classifier proposal</text><text x="105" y="143" class="heading">activate_my_card</text><text x="105" y="198" class="small">Published dataset reference</text><text x="105" y="230" class="heading">card_linking</text>
 <path d="M355 135H400V270M355 219H400" class="arrow"/><rect x="376" y="278" width="253" height="63" class="paper"/><text x="392" y="305" class="small">Participant decision</text><text x="392" y="329" class="small">still requires your review</text>
 <g v-if="step>1"><path d="M376 310H300V368" class="training"/><rect x="13" y="371" width="621" height="40" class="teal"/><text x="30" y="399" class="small">8,463 existing rows + explicitly accepted review rows</text></g>
 <text x="12" y="436" class="small">Keep proposal, label source, reviewer, and accepted label separately.</text>
</svg>
<svg v-else-if="kind==='judge'" viewBox="0 0 660 440" role="img" aria-label="A judge sees the request and proposed intent but not the accepted label. The response passes a schema gate, then is compared with the human review. Missing responses remain unavailable.">
 <text x="12" y="29" class="heading">Request + proposed route</text><path d="M148 45V82" class="arrow"/>
 <rect x="40" y="87" width="220" height="69" class="teal"/><text x="65" y="130" class="heading">Judge model</text>
 <text x="350" y="107" class="small">Accepted human label</text><path d="M360 120V320H390" class="training"/><text x="383" y="160" class="small">withheld from prompt</text>
 <path d="M147 164V199" class="arrow"/><polygon points="147,205 263,249 147,293 31,249" class="paper"/><text x="89" y="246" class="small">Valid JSON</text><text x="86" y="271" class="small">and schema?</text>
 <g :opacity="step>1?1:.25"><path d="M263 249H490V286" class="arrow"/><text x="280" y="235" class="small">yes</text><rect x="390" y="291" width="250" height="64" class="teal"/><text x="407" y="320" class="small">Compare with review</text><text x="407" y="344" class="small">can still disagree</text>
 <path d="M147 299V343" class="arrow"/><text x="165" y="329" class="small">no</text><text x="29" y="374" class="heading">Invalid response</text><text x="29" y="408" class="small">No response → unavailable</text><text x="390" y="408" class="small">Valid ≠ correct</text></g>
</svg>
<svg v-else-if="kind==='freeze'||kind==='rollback'" viewBox="0 0 660 440" role="img" aria-label="Reproduction loads the selected artifact's classifier, feature recipe, class order, and review policy together. Rollback switches the selected artifact to the previous version, then checks the same request IDs.">
 <text x="12" y="28" class="heading">One version must contain the whole predictor</text>
 <g v-for="(label,i) in ['Feature recipe','Classifier weights','Intent order','Review policy']" :key="label"><path :d="`M${38+i*151} 77h128v118h-128z`" class="paper"/><path :d="`M${55+i*151} 105h91M${55+i*151} 125h91M${55+i*151} 145h65`" class="arrow"/><text :x="42+i*151" y="220" class="small">{{label}}</text></g>
 <path d="M100 235V256H560V235M330 256V286" class="arrow"/>
 <rect x="170" y="291" width="320" height="57" class="teal"/><text x="192" y="327" class="heading">{{kind==='rollback'?'Previous artifact version':'Selected artifact version'}}</text>
 <g v-if="step>1||kind==='rollback'"><path d="M330 355V380" class="arrow"/><text x="70" y="412" class="heading">Same case IDs → compare restored predictions</text></g>
 <text v-else x="12" y="412" class="small">Save training IDs, source, and selection reason alongside these files.</text>
</svg>
</div>
<div class="rm-code"><div class="rm-label">Code behind the figure</div><pre><span v-for="(line,i) in code[kind]" :key="i" :class="{active:i===Math.min(step-1,code[kind].length-1)}">{{line}}</span></pre><p class="rm-caption">{{['vocabulary','vector','policy','metrics','review'].includes(kind)?'Recorded inputs and saved results.':'Mechanism diagram; this does not run an experiment.'}}</p></div>
</div>
</template>
<style scoped>
.rm-layout{display:grid;grid-template-columns:1.45fr 1fr;gap:26px;align-items:start}.rm-visual{min-width:0}.rm-visual svg{width:100%;height:auto;display:block}.rm-visual text{font:22px 'IBM Plex Sans';fill:#163c43}.rm-visual .heading{font-size:24px;font-weight:500}.rm-visual .small{font-size:18px}.rm-visual .mono{font:18px 'IBM Plex Mono'}.teal{fill:#6aaa97}.blue{fill:#85b0c8}.orange{fill:#d9a16f}.gold{fill:#e9c36a}.pale{fill:#dfe5d9}.paper{fill:#fffaf0;stroke:#829e8e;stroke-width:1.5}.arrow{stroke:#617c6d;stroke-width:2;fill:none}.training{stroke:#b36e35;stroke-width:3;fill:none;stroke-dasharray:6 4}.rm-code{background:#e7ecdf;border-left:3px solid #237a6c;padding:18px 14px;min-width:0}.rm-label{font:15px 'IBM Plex Mono';color:#536d65;margin-bottom:16px}.rm-code pre{font-size:16px!important;background:none!important;margin:0!important;padding:0!important;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.65!important}.rm-code pre span{display:block;padding:4px 0}.rm-code .active{background:#c5dccb}.rm-caption{font-size:17px!important;line-height:1.35!important;color:#526d65;margin-top:20px!important}.rm-slider{display:block;font-size:18px;margin-top:13px}.rm-slider input{display:block;width:100%;accent-color:#237a6c}.rm-slider input:focus-visible{outline:3px solid #b36e35;outline-offset:3px}
</style>
