const STORAGE_KEY = 'cgif-enterprise-tax-multilingual-v1';
let lang = localStorage.getItem(STORAGE_KEY) || 'zhTW';
let tab = 'overview';

const caseData = {
  seller: 'Taiwan Parts Co.', buyer: 'US Device Co.', product: 'Sensor Module A', qty: 100000,
  price: 5.00, cost: 4.20, markup: 20, quote: 5.80, quoteQty: 20000
};

const i18n = {
  en: {
    langLabel:'Language', title:'Enterprise Tax Evidence Readiness', subtitle:'Small wedge: transfer pricing product transaction. Larger direction: scalable enterprise tax evidence, gap, risk, and review-package workflow.', brand:'Enterprise Tax MVP', boundary:'Synthetic demo only. Not tax, accounting, legal, or transfer pricing advice.',
    tabs:['Overview','TP Wedge','Evidence Gaps','Guardrails','Expansion','Receipt'],
    eyebrow:'Based on Jiayi feedback · narrow wedge, broader platform', heroTitle:'CGIF is not a full TP engine', heroText:'This MVP uses one simple transfer pricing product sale to validate an evidence readiness workflow for enterprise tax teams.',
    mvp:'MVP wedge', platform:'Platform direction', risk:'Risk', ready:'Readiness', policy:'Policy price', actual:'Actual markup', mvpValue:'TP product sale', platformValue:'Enterprise tax',
    validates:'What this MVP validates', notValidate:'What it does not validate',
    valItems:['Can tax teams organize source documents, calculations, comparisons, missing files, and reviewer notes in one case?','Can readiness score help decide what is not ready for review?','Can a review-ready package reduce repeated context rebuilding?'],
    notItems:['It does not cover all TP methods.','It does not decide whether a price is legally compliant.','It does not replace tax managers, TP specialists, auditors, or external advisors.'],
    wedgeTitle:'Use case 1: related-party product sale', facts:'Case facts', calc:'Calculation', support:'Support points',
    factItems:['Seller sells 100,000 units to related US buyer at $5.00/unit.','Seller cost is $4.20/unit. Policy says cost plus 20%.','One third-party quote is $5.80/unit for 20,000 units.','Buyer pays freight, handles warranty, and assumes inventory risk.'],
    evidenceTitle:'Evidence gaps and owners', guardTitle:'Do not conclude', expansionTitle:'Scalable direction: enterprise tax evidence platform', receiptTitle:'Exportable evidence receipt', export:'Export JSON',
    gaps:[['Tax / TP specialist','Benchmarking database support','Real TP work often needs comparable company or transaction benchmarking, not just one quote.'],['Tax manager','Method selection memo','Different transactions may use Cost Plus, TNMM, Berry Ratio, or other methods.'],['Operations / Logistics','Shipping adjustment support','The raw third-party quote may include different shipping terms.'],['Sales / Customer Service','Warranty responsibility support','Lower price may be supportable only if buyer truly assumes warranty risk.'],['Controller / Tax manager','Management approval memo','Need a documented business rationale, not only verbal explanation.']],
    guards:['Do not conclude $5 is arm’s length only because management says it is reasonable.','Do not conclude $5 is improper only because one quote is $5.80.','Do not use raw comparable price without adjusting for volume, freight, warranty, payment terms, and risk allocation.','Do not present this MVP as a complete TP system; it only covers the simplest product sale case.','Do not let TP define the ceiling of the product; TP is the first use case, not the whole company.'],
    modules:[['R&D Tax Credit','Future module','Project records, employee time, technical uncertainty, and cost evidence.'],['Withholding Tax','Future module','Cross-border payment contracts, tax residency, beneficial owner, and rate support.'],['VAT / GST Invoice Evidence','Future module','Invoice, order, ship-to/service location, customer data, and tax rate support.'],['Intercompany Service Fee','Future module','Service agreement, cost pool, allocation method, and benefit evidence.']],
    receiptPos:'Narrow beachhead: TP product sale. Broader platform: enterprise tax evidence readiness.'
  },
  zhCN: {
    langLabel:'语言', title:'企业税证据准备度', subtitle:'小切口：移转定价产品交易。大方向：可扩展的企业税证据、缺口、风险和审查包 workflow。', brand:'企业税证据 MVP', boundary:'全部为合成数据，不提供税务、会计、法律或移转定价建议。',
    tabs:['总览','TP 小切口','证据缺口','边界','扩展方向','证据包'],
    eyebrow:'根据 Jiayi 反馈更新 · 小切口，大方向', heroTitle:'CGIF 不是完整 TP 判断系统', heroText:'这个 MVP 用一个最简单的移转定价产品交易，验证企业税团队是否需要 evidence readiness workflow。',
    mvp:'MVP 切入点', platform:'平台方向', risk:'风险', ready:'准备度', policy:'政策价格', actual:'实际加成率', mvpValue:'TP 产品交易', platformValue:'企业税',
    validates:'现在验证什么？', notValidate:'现在不验证什么？',
    valItems:['企业税务团队是否需要把原始凭证、计算、对比、缺失文件和 reviewer notes 放进同一个 case。','证据准备度分数能不能帮助判断哪些项目还没准备好。','review-ready package 能不能减少每年重复重建 context。'],
    notItems:['不覆盖所有 TP 方法。','不判断价格是否合法。','不取代 tax manager、TP specialist、auditor 或外部顾问。'],
    wedgeTitle:'Use case 1：关联方产品销售', facts:'案例事实', calc:'计算结果', support:'支持点',
    factItems:['卖方向美国关联买方销售 100,000 个单位，单价 $5.00。','卖方成本为 $4.20 / 单位。政策写的是成本加成 20%。','一份第三方报价是 $5.80 / 单位，数量为 20,000。','买方承担运费、保修和库存风险。'],
    evidenceTitle:'证据缺口和负责人', guardTitle:'现在不能直接下的结论', expansionTitle:'可扩展方向：企业税证据准备度平台', receiptTitle:'可导出的证据包', export:'导出 JSON',
    gaps:[['税务 / TP 专家','benchmarking 数据库支持','真实 TP 项目通常需要可比公司或可比交易 benchmarking，而不是只看一份报价。'],['税务经理','方法选择备忘录','不同交易可能使用 Cost Plus、TNMM、Berry Ratio 或其他方法。'],['运营 / 物流','运费差异调整依据','第三方报价和关联方交易的运费条款可能不同。'],['销售 / 客服','保修责任证明','只有买方真实承担保修风险时，较低价格才更有解释空间。'],['Controller / 税务经理','管理层批准备忘录','需要正式商业理由，而不是口头解释。']],
    guards:['不要因为管理层说 $5 合理，就直接认定它符合独立交易原则。','不要只因为一份第三方报价是 $5.80，就直接认定 $5 有问题。','不要直接使用原始第三方价格；需要考虑数量、运费、保修、付款条件和风险承担差异。','不要把这个 MVP 包装成完整 TP 系统；它只覆盖最简单的产品交易场景。','不要把 TP 当成产品天花板；TP 是第一个 use case，不是整个公司。'],
    modules:[['R&D Tax Credit 研发税收抵免','未来模块','项目记录、员工工时、技术不确定性和费用证据。'],['Withholding Tax 预提税','未来模块','跨境付款合同、税收居民证明、受益所有人和适用税率支持。'],['VAT / GST 发票证据','未来模块','发票、订单、发货/服务地点、客户信息和税率支持。'],['Intercompany Service Fee 关联服务费','未来模块','服务协议、成本池、分摊方法和受益证据。']],
    receiptPos:'小切口：TP 产品交易。大方向：企业税证据准备度。'
  },
  zhTW: {
    langLabel:'語言', title:'企業稅證據準備度', subtitle:'小切口：移轉訂價產品交易。大方向：可擴展的企業稅證據、缺口、風險和審查包 workflow。', brand:'企業稅證據 MVP', boundary:'全部為合成資料，不提供稅務、會計、法律或移轉訂價建議。',
    tabs:['總覽','TP 小切口','證據缺口','邊界','擴展方向','證據包'],
    eyebrow:'根據 Jiayi feedback 更新 · 小切口，大方向', heroTitle:'CGIF 不是完整 TP 判斷系統', heroText:'這個 MVP 用一個最簡單的移轉訂價產品交易，驗證企業稅團隊是否需要 evidence readiness workflow。',
    mvp:'MVP 切入點', platform:'平台方向', risk:'風險', ready:'準備度', policy:'政策價格', actual:'實際加成率', mvpValue:'TP 產品交易', platformValue:'企業稅',
    validates:'現在驗證什麼？', notValidate:'現在不驗證什麼？',
    valItems:['企業稅務團隊是否需要把原始憑證、計算、對比、缺失文件和 reviewer notes 放進同一個 case。','證據準備度分數能不能幫助判斷哪些項目還沒準備好。','review-ready package 能不能減少每年重複重建 context。'],
    notItems:['不覆蓋所有 TP 方法。','不判斷價格是否合法。','不取代 tax manager、TP specialist、auditor 或外部顧問。'],
    wedgeTitle:'Use case 1：關係企業產品銷售', facts:'案例事實', calc:'計算結果', support:'支持點',
    factItems:['賣方向美國關係企業買方銷售 100,000 個單位，單價 $5.00。','賣方成本為 $4.20 / 單位。政策寫的是成本加成 20%。','一份第三方報價是 $5.80 / 單位，數量為 20,000。','買方承擔運費、保固和庫存風險。'],
    evidenceTitle:'證據缺口和負責人', guardTitle:'現在不能直接下的結論', expansionTitle:'可擴展方向：企業稅證據準備度平台', receiptTitle:'可匯出的證據包', export:'匯出 JSON',
    gaps:[['稅務 / TP 專家','benchmarking 資料庫支持','真實 TP 專案通常需要可比公司或可比交易 benchmarking，而不是只看一份報價。'],['稅務經理','方法選擇備忘錄','不同交易可能使用 Cost Plus、TNMM、Berry Ratio 或其他方法。'],['營運 / 物流','運費差異調整依據','第三方報價和關係企業交易的運費條款可能不同。'],['銷售 / 客服','保固責任證明','只有買方真實承擔保固風險時，較低價格才更有解釋空間。'],['Controller / 稅務經理','管理層核准備忘錄','需要正式商業理由，而不是口頭解釋。']],
    guards:['不要因為管理層說 $5 合理，就直接認定它符合獨立交易原則。','不要只因為一份第三方報價是 $5.80，就直接認定 $5 有問題。','不要直接使用原始第三方價格；需要考慮數量、運費、保固、付款條件和風險承擔差異。','不要把這個 MVP 包裝成完整 TP 系統；它只覆蓋最簡單的產品交易場景。','不要把 TP 當成產品天花板；TP 是第一個 use case，不是整個公司。'],
    modules:[['R&D Tax Credit 研發稅收抵免','未來模組','專案紀錄、員工工時、技術不確定性和費用證據。'],['Withholding Tax 預提稅','未來模組','跨境付款合約、稅收居民證明、受益所有人和適用稅率支持。'],['VAT / GST 發票證據','未來模組','發票、訂單、發貨/服務地點、客戶資訊和稅率支持。'],['Intercompany Service Fee 關係企業服務費','未來模組','服務協議、成本池、分攤方法和受益證據。']],
    receiptPos:'小切口：TP 產品交易。大方向：企業稅證據準備度。'
  }
};

function t(){ return i18n[lang]; }
function money(n){ return `$${Number(n).toFixed(2)}`; }
function pct(n){ return `${Number(n).toFixed(1)}%`; }
function pill(text,tone='neutral'){ return `<span class="pill ${tone}">${text}</span>`; }
function list(items){ return `<ul>${items.map(x=>`<li>${x}</li>`).join('')}</ul>`; }
function setLang(x){ lang=x; localStorage.setItem(STORAGE_KEY, x); render(); }
function setTab(x){ tab=x; render(); }
function calc(){ const d=caseData; const policy=d.cost*(1+d.markup/100); const actual=(d.price-d.cost)/d.cost*100; const gap=(d.quote-d.price)/d.quote*100; return {policy,actual,gap,ready:42,risk: lang==='en'?'Medium':lang==='zhCN'?'中':'中'}; }
function riskTone(){ return 'warn'; }
function receipt(){ const c=calc(), L=t(); return { generated_at:new Date().toISOString(), language:lang, product_positioning:L.receiptPos, boundary:L.boundary, case:caseData, calculations:{policy_price: Number(c.policy.toFixed(2)), actual_markup_percent:Number(c.actual.toFixed(2)), raw_quote_gap_percent:Number(c.gap.toFixed(2))}, evidence_gaps:L.gaps, guardrails:L.guards, future_modules:L.modules }; }
function download(){ const blob=new Blob([JSON.stringify(receipt(),null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='enterprise_tax_evidence_receipt.json'; a.click(); URL.revokeObjectURL(url); }
function languageSelector(){ return `<div class="headerPills"><span class="pill neutral">${t().langLabel}</span><button class="secondary" onclick="setLang('en')">English</button><button class="secondary" onclick="setLang('zhCN')">简体中文</button><button class="secondary" onclick="setLang('zhTW')">繁體中文</button></div>`; }
function tabs(){ const ids=['overview','wedge','gaps','guard','expand','receipt']; return ids.map((id,i)=>`<button class="${tab===id?'active':''}" onclick="setTab('${id}')">${t().tabs[i]}</button>`).join(''); }
function metrics(c){ const L=t(); return `<div class="metrics"><div class="metric"><span>${L.mvp}</span><b>${L.mvpValue}</b><small>Narrow beachhead</small></div><div class="metric"><span>${L.platform}</span><b>${L.platformValue}</b><small>Broad potential</small></div><div class="metric"><span>${L.risk}</span><b>${c.risk}</b><small>Demo score</small></div><div class="metric"><span>${L.policy}</span><b>${money(c.policy)}</b><small>Cost plus ${pct(caseData.markup)}</small></div><div class="metric"><span>${L.actual}</span><b>${pct(c.actual)}</b><small>Gross markup</small></div></div>`; }
function overview(){ const L=t(), c=calc(); return `<section class="panel heroPanel"><div><span class="eyebrow">${L.eyebrow}</span><h2>${L.heroTitle}</h2><p>${L.heroText}</p><div class="heroActions"><button onclick="setTab('wedge')">${L.tabs[1]}</button><button class="secondary" onclick="setTab('expand')">${L.tabs[4]}</button></div></div><div class="caseCard"><b>CGIF</b><span>${L.brand}</span><div class="bigNumber">${c.ready}%</div><small>${L.ready}</small></div></section>${metrics(c)}<section class="panel"><div class="split"><div><h3>${L.validates}</h3>${list(L.valItems)}</div><div><h3>${L.notValidate}</h3>${list(L.notItems)}</div></div></section>`; }
function wedge(){ const L=t(), c=calc(); return `<section class="panel"><span class="eyebrow">${L.mvpValue}</span><h2>${L.wedgeTitle}</h2><div class="split"><div><h3>${L.facts}</h3>${list(L.factItems)}</div><div><h3>${L.calc}</h3>${list([`${L.policy}: ${money(c.policy)}`, `${L.actual}: ${pct(c.actual)}`, `Raw quote gap: ${pct(c.gap)}`])}<h3>${L.support}</h3>${list([`$5.00 is close to ${money(c.policy)} under cost-plus logic.`, `Buyer-side freight/warranty/inventory risk may explain part of the raw quote gap if documented.`])}</div></div></section>`; }
function gaps(){ const L=t(); return `<section class="panel"><span class="eyebrow">Evidence workflow</span><h2>${L.evidenceTitle}</h2><table><thead><tr><th>Owner</th><th>Gap</th><th>Why it matters</th></tr></thead><tbody>${L.gaps.map(g=>`<tr><td>${g[0]}</td><td><b>${g[1]}</b></td><td>${g[2]}</td></tr>`).join('')}</tbody></table></section>`; }
function guard(){ const L=t(); return `<section class="panel"><span class="eyebrow">Evidence boundary</span><h2>${L.guardTitle}</h2>${list(L.guards)}</section>`; }
function expand(){ const L=t(); return `<section class="panel"><span class="eyebrow">Scalable direction</span><h2>${L.expansionTitle}</h2><div class="metrics">${L.modules.map(m=>`<div class="metric"><span>${m[1]}</span><b>${m[0]}</b><small>${m[2]}</small></div>`).join('')}</div></section>`; }
function receiptView(){ const L=t(); return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">Review package</span><h2>${L.receiptTitle}</h2></div><button onclick="download()">${L.export}</button></div><pre>${JSON.stringify(receipt(), null, 2)}</pre></section>`; }
function body(){ return tab==='overview'?overview():tab==='wedge'?wedge():tab==='gaps'?gaps():tab==='guard'?guard():tab==='expand'?expand():receiptView(); }
function render(){ const L=t(), c=calc(); document.documentElement.lang = lang==='en'?'en':lang==='zhCN'?'zh-CN':'zh-TW'; document.getElementById('app').innerHTML = `<aside><div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>${L.brand}</span></div></div><nav>${tabs()}</nav><div class="sideNote"><b>MVP Boundary</b><span>${L.boundary}</span></div></aside><main><header><div><span class="eyebrow">CGIF · Enterprise Tax Evidence Readiness</span><h1>${L.title}</h1><p>${L.subtitle}</p></div>${languageSelector()}</header>${body()}</main>`; }
window.setLang=setLang; window.setTab=setTab; window.download=download; render();
