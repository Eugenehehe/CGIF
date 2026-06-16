const STORE_KEY = 'cgif-enterprise-tax-product-v2';

const text = {
  en: {
    brand:'Enterprise Tax Workbench', title:'Enterprise Tax Evidence Workbench', subtitle:'Interactive product prototype: manage tax cases, evidence gaps, review tasks, and export review-ready packages.',
    lang:'Language', boundary:'Prototype only. Synthetic data. Not tax, accounting, legal, or transfer pricing advice.',
    nav:{queue:'Work Queue', case:'Case Intake', evidence:'Evidence Checklist', tasks:'Task Board', receipt:'Review Package', settings:'Settings'},
    create:'Create case', export:'Export package', reset:'Reset demo data', open:'Open', save:'Save', status:'Status', owner:'Owner', missing:'Missing evidence', why:'Why it matters',
    metrics:{cases:'Cases', open:'Open work', high:'High risk', avg:'Avg readiness'},
    fields:'Case fields', checklist:'Evidence checklist', known:'Known support', risk:'Risk signals', guard:'Do not conclude', recommendation:'Recommended next action',
    type:{tp:'Transfer Pricing · Product Sale', rd:'R&D Tax Credit', wht:'Withholding Tax'},
    risk:{High:'High', Medium:'Medium', Low:'Low'},
    statuses:['Open','Needs documents','Ready for specialist review','Ready for manager sign-off','Closed'],
    newCaseName:'New case', noMissing:'No missing evidence. Ready for review.',
    tasksIntro:'Tasks are generated from missing evidence across all open cases.',
    guardrails:{
      common:['Do not treat this tool as the final tax conclusion.','Do not present missing evidence as proof of wrongdoing.','Do not skip human tax/accounting review for judgment-heavy items.'],
      tp:['Do not conclude the transfer price is arm’s length only because management says it is reasonable.','Do not use a raw third-party quote without adjusting for volume, freight, warranty, payment terms, and risk allocation.','Do not pretend this MVP covers all TP methods such as TNMM, Berry Ratio, or profit split.'],
      rd:['Do not claim an R&D credit without project, activity, cost, and technical uncertainty support.','Do not treat all engineering work as qualified research automatically.'],
      wht:['Do not apply a reduced treaty rate without residency and beneficial-owner support.','Do not classify cross-border payments without contract and payment-purpose evidence.']
    }
  },
  zhCN: {
    brand:'企业税工作台', title:'企业税证据工作台', subtitle:'真正的产品原型：管理税务 case、证据缺口、review 任务，并导出可审查的证据包。',
    lang:'语言', boundary:'原型演示。全部为合成数据，不提供税务、会计、法律或移转定价建议。',
    nav:{queue:'工作队列', case:'Case 录入', evidence:'证据清单', tasks:'任务板', receipt:'审查包', settings:'设置'},
    create:'新增 case', export:'导出证据包', reset:'重置 demo 数据', open:'打开', save:'保存', status:'状态', owner:'负责人', missing:'缺失证据', why:'为什么重要',
    metrics:{cases:'Cases', open:'未关闭', high:'高风险', avg:'平均准备度'},
    fields:'Case 字段', checklist:'证据清单', known:'支持点', risk:'风险信号', guard:'现在不能直接下的结论', recommendation:'建议下一步',
    type:{tp:'移转定价 · 产品交易', rd:'研发税收抵免', wht:'预提税'},
    risk:{High:'高', Medium:'中', Low:'低'},
    statuses:['待处理','需要补文件','可交给专家复核','可给经理签核','已关闭'],
    newCaseName:'新 case', noMissing:'没有缺失证据，可进入 review。',
    tasksIntro:'任务会根据所有未关闭 case 的缺失证据自动生成。',
    guardrails:{
      common:['不要把这个工具当成最终税务结论。','不要把缺失证据直接当成违规证据。','高判断税务事项必须保留人工税务 / 会计 review。'],
      tp:['不要因为管理层说价格合理，就直接认定符合独立交易原则。','不要直接使用原始第三方报价；需要考虑数量、运费、保修、付款条件和风险承担差异。','不要把这个 MVP 包装成覆盖所有 TP 方法的系统，例如 TNMM、Berry Ratio 或利润分割法。'],
      rd:['没有项目、活动、成本和技术不确定性证据时，不要主张研发税收抵免。','不要自动把所有工程活动都当成合格研发。'],
      wht:['没有税收居民证明和受益所有人支持时，不要直接套用优惠税率。','没有合同和付款性质证据时，不要草率分类跨境付款。']
    }
  },
  zhTW: {
    brand:'企業稅工作台', title:'企業稅證據工作台', subtitle:'真正的產品原型：管理稅務 case、證據缺口、review 任務，並匯出可審查的證據包。',
    lang:'語言', boundary:'原型演示。全部為合成資料，不提供稅務、會計、法律或移轉訂價建議。',
    nav:{queue:'工作隊列', case:'Case 錄入', evidence:'證據清單', tasks:'任務板', receipt:'審查包', settings:'設定'},
    create:'新增 case', export:'匯出證據包', reset:'重置 demo 資料', open:'打開', save:'儲存', status:'狀態', owner:'負責人', missing:'缺失證據', why:'為什麼重要',
    metrics:{cases:'Cases', open:'未關閉', high:'高風險', avg:'平均準備度'},
    fields:'Case 欄位', checklist:'證據清單', known:'支持點', risk:'風險信號', guard:'現在不能直接下的結論', recommendation:'建議下一步',
    type:{tp:'移轉訂價 · 產品交易', rd:'研發稅收抵免', wht:'預提稅'},
    risk:{High:'高', Medium:'中', Low:'低'},
    statuses:['待處理','需要補文件','可交給專家複核','可給經理簽核','已關閉'],
    newCaseName:'新 case', noMissing:'沒有缺失證據，可進入 review。',
    tasksIntro:'任務會根據所有未關閉 case 的缺失證據自動生成。',
    guardrails:{
      common:['不要把這個工具當成最終稅務結論。','不要把缺失證據直接當成違規證據。','高判斷稅務事項必須保留人工稅務 / 會計 review。'],
      tp:['不要因為管理層說價格合理，就直接認定符合獨立交易原則。','不要直接使用原始第三方報價；需要考慮數量、運費、保固、付款條件和風險承擔差異。','不要把這個 MVP 包裝成覆蓋所有 TP 方法的系統，例如 TNMM、Berry Ratio 或利潤分割法。'],
      rd:['沒有專案、活動、成本和技術不確定性證據時，不要主張研發稅收抵免。','不要自動把所有工程活動都當成合格研發。'],
      wht:['沒有稅收居民證明和受益所有人支持時，不要直接套用優惠稅率。','沒有合約和付款性質證據時，不要草率分類跨境付款。']
    }
  }
};

const schemas = {
  tp: {
    fields: [
      ['seller','Seller / 卖方','text'], ['buyer','Buyer / 买方','text'], ['product','Product / 产品','text'], ['qty','Quantity / 数量','number'],
      ['price','Transfer price / 转让价格','number'], ['cost','Seller cost / 卖方成本','number'], ['markup','Policy markup % / 政策加成率','number'], ['quote','Third-party quote / 第三方报价','number'],
      ['method','Method / 方法','text'], ['agreementDate','Agreement date / 合约日期','date'], ['notes','Management rationale / 管理层解释','textarea']
    ],
    evidence: [
      ['invoice','Accounting','Invoice / 发票','Proves the transaction occurred.'],
      ['costSheet','Manufacturing Finance','Updated cost sheet / 最新成本表','Needed for cost-plus calculation.'],
      ['agreement','Legal / Tax','Intercompany agreement / 关联企业合约','Supports pricing policy and risk allocation.'],
      ['benchmark','Tax / TP Specialist','Benchmarking support / 基准分析','Needed to compare with market or comparable companies.'],
      ['methodMemo','Tax Manager','Method selection memo / 方法选择备忘录','Explains why Cost Plus, TNMM, Berry Ratio, etc. is appropriate.'],
      ['volume','Sales Ops','Volume discount support / 大量采购折扣依据','Explains why high-volume related-party price may be lower.'],
      ['freight','Operations','Freight adjustment / 运费调整','Raw quote may include different freight terms.'],
      ['warranty','Customer Service','Warranty responsibility / 保修责任','Risk allocation affects price comparability.'],
      ['approval','Controller','Management approval memo / 管理层批准备忘录','Documents business rationale.']
    ]
  },
  rd: {
    fields: [
      ['project','Project / 项目','text'], ['entity','Entity / 公司主体','text'], ['year','Tax year / 税务年度','number'], ['cost','Claimed cost / 主张费用','number'],
      ['team','Team / 团队','text'], ['uncertainty','Technical uncertainty / 技术不确定性','textarea'], ['notes','Reviewer notes / 备注','textarea']
    ],
    evidence: [
      ['projectDocs','Engineering','Project description / 项目说明','Shows what was attempted.'],
      ['uncertainty','Engineering Lead','Technical uncertainty memo / 技术不确定性说明','Supports qualified research nature.'],
      ['experiments','Product / Engineering','Experiment records / 实验记录','Shows iterative testing or development.'],
      ['time','HR / Finance','Employee time support / 员工工时','Connects labor cost to qualified activity.'],
      ['costs','Finance','Cost detail / 费用明细','Supports claimed amount.'],
      ['managerReview','Tax Manager','Tax manager review / 税务经理复核','Human review before claim package.']
    ]
  },
  wht: {
    fields: [
      ['payer','Payer / 付款方','text'], ['payee','Payee / 收款方','text'], ['country','Payee country / 收款方国家','text'], ['paymentType','Payment type / 付款性质','text'],
      ['amount','Payment amount / 付款金额','number'], ['statutoryRate','Statutory rate % / 法定税率','number'], ['treatyRate','Treaty rate % / 协定税率','number'], ['notes','Payment rationale / 付款说明','textarea']
    ],
    evidence: [
      ['contract','Legal','Contract / 合同','Supports payment nature.'],
      ['invoice','Accounting','Invoice / 发票','Supports amount and payee.'],
      ['residency','Payee / Tax','Tax residency certificate / 税收居民证明','Needed for treaty support.'],
      ['beneficialOwner','Tax','Beneficial owner support / 受益所有人证明','Needed before reduced treaty rate.'],
      ['withholdingCalc','Tax','Withholding calculation / 预提税计算','Documents rate and amount.'],
      ['approval','Tax Manager','Manager approval / 经理审批','Human review before filing or payment.']
    ]
  }
};

const seedCases = [
  { id:'TP-001', type:'tp', name:'Taiwan Co. → US Co. sensor module', status:'Needs documents', owner:'Tax Manager', data:{seller:'Taiwan Parts Co.', buyer:'US Device Co.', product:'Sensor Module A', qty:100000, price:5.00, cost:4.20, markup:20, quote:5.80, method:'Cost Plus', agreementDate:'2023-04-01', notes:'High volume; buyer pays freight and handles warranty.'}, evidence:{invoice:true,costSheet:true,agreement:true,benchmark:false,methodMemo:false,volume:false,freight:false,warranty:false,approval:false}, reviewNotes:'' },
  { id:'RD-001', type:'rd', name:'AI routing prototype R&D support', status:'Open', owner:'Tax Analyst', data:{project:'AI routing prototype', entity:'US Device Co.', year:2026, cost:180000, team:'Engineering / Data', uncertainty:'System performance and evidence routing logic were uncertain.', notes:''}, evidence:{projectDocs:true,uncertainty:false,experiments:false,time:true,costs:true,managerReview:false}, reviewNotes:'' },
  { id:'WHT-001', type:'wht', name:'Royalty payment to foreign affiliate', status:'Open', owner:'International Tax', data:{payer:'US Device Co.', payee:'SG IP Co.', country:'Singapore', paymentType:'Royalty', amount:250000, statutoryRate:30, treatyRate:10, notes:'Need treaty and beneficial owner support before applying lower rate.'}, evidence:{contract:true,invoice:true,residency:false,beneficialOwner:false,withholdingCalc:false,approval:false}, reviewNotes:'' }
];

function initialState(){ return { lang:'zhTW', page:'queue', activeId:'TP-001', cases: JSON.parse(JSON.stringify(seedCases)) }; }
let state = load();
function load(){ try { return JSON.parse(localStorage.getItem(STORE_KEY)) || initialState(); } catch { return initialState(); } }
function save(){ localStorage.setItem(STORE_KEY, JSON.stringify(state)); }
function L(){ return text[state.lang] || text.zhTW; }
function trType(type){ return L().type[type]; }
function byId(id){ return state.cases.find(c => c.id === id) || state.cases[0]; }
function active(){ return byId(state.activeId); }
function money(n){ return `$${Number(n || 0).toLocaleString(undefined,{maximumFractionDigits:2})}`; }
function pct(n){ return `${Number(n || 0).toFixed(1)}%`; }
function pill(v,tone='neutral'){ return `<span class="pill ${tone}">${v}</span>`; }
function toneRisk(r){ return r === 'High' ? 'danger' : r === 'Medium' ? 'warn' : 'success'; }
function riskLabel(r){ return L().risk[r] || r; }
function esc(v){ return String(v ?? '').replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s])); }

function evaluate(c){
  const schema = schemas[c.type];
  const missing = schema.evidence.filter(e => !c.evidence[e[0]]).map(e => ({key:e[0], owner:e[1], item:e[2], reason:e[3]}));
  const ready = Math.round(((schema.evidence.length - missing.length) / schema.evidence.length) * 100);
  const known = schema.evidence.filter(e => c.evidence[e[0]]).map(e => `${e[2]} ✓`);
  let signals = [];
  let support = [];
  let calc = {};

  if(c.type === 'tp'){
    const d = c.data;
    calc.policyPrice = Number(d.cost || 0) * (1 + Number(d.markup || 0) / 100);
    calc.actualMarkup = d.cost ? ((Number(d.price || 0) - Number(d.cost || 0)) / Number(d.cost || 1)) * 100 : 0;
    calc.quoteGap = d.quote ? ((Number(d.quote || 0) - Number(d.price || 0)) / Number(d.quote || 1)) * 100 : 0;
    support.push(`Policy price: ${money(calc.policyPrice)}; actual price: ${money(d.price)}.`);
    support.push(`Actual markup: ${pct(calc.actualMarkup)}.`);
    if(Math.abs(calc.policyPrice - Number(d.price || 0)) <= Math.max(0.1, calc.policyPrice * 0.03)) support.push('Price is close to cost-plus policy.');
    if(calc.quoteGap > 10) signals.push(`Related-party price is ${pct(calc.quoteGap)} below raw third-party quote.`);
    if(!c.evidence.benchmark) signals.push('Benchmarking support is missing.');
    if(!c.evidence.methodMemo) signals.push('Method selection memo is missing.');
  }
  if(c.type === 'rd'){
    support.push(`Claimed cost: ${money(c.data.cost)} for tax year ${c.data.year}.`);
    if(!c.evidence.uncertainty) signals.push('Technical uncertainty memo is missing.');
    if(!c.evidence.experiments) signals.push('Experiment / iteration records are missing.');
    if(c.evidence.time && c.evidence.costs) support.push('Time and cost support are partially available.');
  }
  if(c.type === 'wht'){
    const statutory = Number(c.data.amount || 0) * Number(c.data.statutoryRate || 0) / 100;
    const treaty = Number(c.data.amount || 0) * Number(c.data.treatyRate || 0) / 100;
    calc.taxDelta = statutory - treaty;
    support.push(`Potential rate difference: statutory ${money(statutory)} vs treaty ${money(treaty)}.`);
    if(!c.evidence.residency) signals.push('Tax residency certificate is missing.');
    if(!c.evidence.beneficialOwner) signals.push('Beneficial-owner support is missing.');
    if(calc.taxDelta > 0) signals.push(`Reduced treaty rate would lower withholding by ${money(calc.taxDelta)}, so support must be strong.`);
  }

  let risk = 'Medium';
  if(ready < 45 || signals.length >= 3) risk = 'High';
  if(ready >= 80 && signals.length <= 1) risk = 'Low';
  const recommendation = risk === 'High' ? 'Resolve missing evidence before specialist review.' : risk === 'Medium' ? 'Ready for tax manager triage, but not final sign-off.' : 'Ready for manager sign-off / advisor review.';
  const guards = [...L().guardrails.common, ...L().guardrails[c.type]];
  return { ready, missing, known, support, signals, risk, recommendation, guards, calc };
}

function setLang(x){ state.lang=x; save(); render(); }
function setPage(x){ state.page=x; save(); render(); }
function openCase(id){ state.activeId=id; state.page='case'; save(); render(); }
function setStatus(v){ active().status=v; save(); render(); }
function setOwner(v){ active().owner=v; save(); render(); }
function setReviewNotes(v){ active().reviewNotes=v; save(); render(); }
function setField(k,v){ const c=active(); c.data[k] = isFinite(v) && v !== '' && !String(v).startsWith('0') ? Number(v) : v; save(); render(); }
function toggleEvidence(k){ const c=active(); c.evidence[k]=!c.evidence[k]; save(); render(); }
function createCase(type){
  const prefix = type === 'tp' ? 'TP' : type === 'rd' ? 'RD' : 'WHT';
  const id = `${prefix}-${String(state.cases.filter(c=>c.type===type).length + 1).padStart(3,'0')}`;
  const schema = schemas[type];
  const data = {};
  schema.fields.forEach(f => data[f[0]] = f[2] === 'number' ? 0 : '');
  const evidence = {}; schema.evidence.forEach(e => evidence[e[0]] = false);
  state.cases.unshift({id,type,name:`${L().newCaseName} ${id}`,status:'Open',owner:'Unassigned',data,evidence,reviewNotes:''});
  state.activeId=id; state.page='case'; save(); render();
}
function resetDemo(){ state = initialState(); save(); render(); }
function exportPackage(){
  const c = active(); const e = evaluate(c);
  const receipt = {generated_at:new Date().toISOString(), language:state.lang, boundary:L().boundary, case:c, evaluation:e};
  const blob = new Blob([JSON.stringify(receipt,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=`${c.id}_review_package.json`; a.click(); URL.revokeObjectURL(url);
}
function exportQueue(){
  const rows = state.cases.map(c => { const e=evaluate(c); return {id:c.id,type:trType(c.type),name:c.name,status:c.status,owner:c.owner,readiness:e.ready,risk:e.risk,missing:e.missing.length}; });
  const blob = new Blob([JSON.stringify(rows,null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='enterprise_tax_work_queue.json'; a.click(); URL.revokeObjectURL(url);
}

function nav(){ const n=L().nav; return Object.entries(n).map(([k,v])=>`<button class="${state.page===k?'active':''}" onclick="setPage('${k}')">${v}</button>`).join(''); }
function header(){ return `<header><div><span class="eyebrow">CGIF · Product Workbench</span><h1>${L().title}</h1><p>${L().subtitle}</p></div><div class="headerPills"><span class="pill neutral">${L().lang}</span><button class="secondary" onclick="setLang('en')">English</button><button class="secondary" onclick="setLang('zhCN')">简体中文</button><button class="secondary" onclick="setLang('zhTW')">繁體中文</button></div></header>`; }
function metrics(){ const evals=state.cases.map(evaluate); const open=state.cases.filter(c=>c.status!=='Closed'&&c.status!=='已关闭'&&c.status!=='已關閉').length; const high=evals.filter(e=>e.risk==='High').length; const avg=Math.round(evals.reduce((s,e)=>s+e.ready,0)/Math.max(evals.length,1)); return `<div class="metrics"><div class="metric"><span>${L().metrics.cases}</span><b>${state.cases.length}</b><small>localStorage</small></div><div class="metric"><span>${L().metrics.open}</span><b>${open}</b><small>active workflow</small></div><div class="metric"><span>${L().metrics.high}</span><b>${high}</b><small>needs attention</small></div><div class="metric"><span>${L().metrics.avg}</span><b>${avg}%</b><small>evidence readiness</small></div></div>`; }
function queuePage(){ return `${metrics()}<section class="panel"><div class="panelHead"><div><span class="eyebrow">Product workspace</span><h2>${L().nav.queue}</h2></div><div class="heroActions"><button onclick="createCase('tp')">${L().create}: TP</button><button class="secondary" onclick="createCase('rd')">${L().create}: R&D</button><button class="secondary" onclick="createCase('wht')">${L().create}: WHT</button><button class="secondary" onclick="exportQueue()">Export queue</button></div></div><table><thead><tr><th>Case</th><th>Type</th><th>${L().status}</th><th>${L().owner}</th><th>Readiness</th><th>Risk</th><th>Missing</th><th></th></tr></thead><tbody>${state.cases.map(c=>{const e=evaluate(c);return `<tr><td><b>${esc(c.id)}</b><br/><small>${esc(c.name)}</small></td><td>${trType(c.type)}</td><td>${esc(c.status)}</td><td>${esc(c.owner)}</td><td>${e.ready}%</td><td>${pill(riskLabel(e.risk),toneRisk(e.risk))}</td><td>${e.missing.length}</td><td><button onclick="openCase('${c.id}')">${L().open}</button></td></tr>`}).join('')}</tbody></table></section>`; }
function fieldInput(f,c){ const [k,label,type]=f; const v=c.data[k] ?? ''; if(type==='textarea') return `<label class="wideLabel">${label}<textarea onchange="setField('${k}',this.value)">${esc(v)}</textarea></label>`; return `<label>${label}<input type="${type}" value="${esc(v)}" onchange="setField('${k}',this.value)"/></label>`; }
function casePage(){ const c=active(); const e=evaluate(c); return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">${trType(c.type)}</span><h2>${esc(c.id)} · ${esc(c.name)}</h2></div><div>${pill(riskLabel(e.risk),toneRisk(e.risk))}${pill(e.ready+'% ready','blue')}</div></div><div class="formGrid two"><label>${L().status}<select onchange="setStatus(this.value)">${L().statuses.map(s=>`<option ${c.status===s?'selected':''}>${s}</option>`).join('')}<option ${c.status==='Open'?'selected':''}>Open</option><option ${c.status==='Needs documents'?'selected':''}>Needs documents</option><option ${c.status==='Closed'?'selected':''}>Closed</option></select></label><label>${L().owner}<input value="${esc(c.owner)}" onchange="setOwner(this.value)"/></label></div><h3>${L().fields}</h3><div class="formGrid">${schemas[c.type].fields.filter(f=>f[2]!=='textarea').map(f=>fieldInput(f,c)).join('')}</div>${schemas[c.type].fields.filter(f=>f[2]==='textarea').map(f=>fieldInput(f,c)).join('')}<div class="boundary"><b>${L().recommendation}:</b> ${e.recommendation}</div></section>`; }
function evidencePage(){ const c=active(); const e=evaluate(c); return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">${esc(c.id)}</span><h2>${L().checklist}</h2></div><div>${pill(e.ready+'%','blue')}</div></div><div class="checkGrid">${schemas[c.type].evidence.map(x=>`<label class="check"><input type="checkbox" ${c.evidence[x[0]]?'checked':''} onchange="toggleEvidence('${x[0]}')"/> <span><b>${x[2]}</b><br/><small>${x[1]} · ${x[3]}</small></span></label>`).join('')}</div></section><section class="panel"><div class="split"><div><h3>${L().known}</h3>${e.known.length?`<ul>${e.known.map(x=>`<li>${x}</li>`).join('')}</ul>`:'<div class="empty">No known evidence yet.</div>'}<h3>${L().support}</h3><ul>${e.support.map(x=>`<li>${x}</li>`).join('')}</ul></div><div><h3>${L().risk}</h3>${e.signals.length?`<ul>${e.signals.map(x=>`<li>${x}</li>`).join('')}</ul>`:'<div class="empty">No risk signals.</div>'}<h3>${L().missing}</h3>${missingTable(e.missing)}</div></div></section>`; }
function missingTable(items){ return items.length ? `<table><thead><tr><th>${L().owner}</th><th>${L().missing}</th><th>${L().why}</th></tr></thead><tbody>${items.map(m=>`<tr><td>${m.owner}</td><td><b>${m.item}</b></td><td>${m.reason}</td></tr>`).join('')}</tbody></table>` : `<div class="empty">${L().noMissing}</div>`; }
function tasksPage(){ const tasks=[]; state.cases.forEach(c=>evaluate(c).missing.forEach(m=>tasks.push({caseId:c.id,caseName:c.name,type:c.type,...m}))); return `<section class="panel"><span class="eyebrow">Generated workflow</span><h2>${L().nav.tasks}</h2><p>${L().tasksIntro}</p>${tasks.length?`<table><thead><tr><th>Case</th><th>Type</th><th>${L().owner}</th><th>${L().missing}</th><th>${L().why}</th></tr></thead><tbody>${tasks.map(t=>`<tr><td><b>${t.caseId}</b><br/><small>${esc(t.caseName)}</small></td><td>${trType(t.type)}</td><td>${t.owner}</td><td><b>${t.item}</b></td><td>${t.reason}</td></tr>`).join('')}</tbody></table>`:`<div class="empty">${L().noMissing}</div>`}</section>`; }
function receiptPage(){ const c=active(); const e=evaluate(c); const data={generated_at:new Date().toISOString(), boundary:L().boundary, case:c, evaluation:e}; return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">${esc(c.id)}</span><h2>${L().nav.receipt}</h2></div><button onclick="exportPackage()">${L().export}</button></div><label class="wideLabel">Reviewer notes<textarea onchange="setReviewNotes(this.value)">${esc(c.reviewNotes)}</textarea></label><pre>${JSON.stringify(data,null,2)}</pre></section>`; }
function settingsPage(){ return `<section class="panel"><h2>${L().nav.settings}</h2><p>${L().boundary}</p><div class="heroActions"><button class="secondary" onclick="resetDemo()">${L().reset}</button></div></section>`; }
function pageBody(){ return state.page==='queue'?queuePage():state.page==='case'?casePage():state.page==='evidence'?evidencePage():state.page==='tasks'?tasksPage():state.page==='receipt'?receiptPage():settingsPage(); }
function render(){ document.documentElement.lang = state.lang==='en'?'en':state.lang==='zhCN'?'zh-CN':'zh-TW'; document.getElementById('app').innerHTML = `<aside><div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>${L().brand}</span></div></div><nav>${nav()}</nav><div class="sideNote"><b>Product boundary</b><span>${L().boundary}</span></div></aside><main>${header()}${pageBody()}</main>`; }
window.setLang=setLang; window.setPage=setPage; window.openCase=openCase; window.setStatus=setStatus; window.setOwner=setOwner; window.setReviewNotes=setReviewNotes; window.setField=setField; window.toggleEvidence=toggleEvidence; window.createCase=createCase; window.resetDemo=resetDemo; window.exportPackage=exportPackage; window.exportQueue=exportQueue; render();
