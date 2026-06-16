const STORAGE_KEY = 'cgif-enterprise-tax-demo-cn-v2';

const defaultCase = {
  caseId: 'TAX-TP-001',
  module: '移转定价 · 产品交易',
  transactionType: '关联方产品销售',
  seller: '台湾零件公司',
  buyer: '美国设备公司',
  relationship: '同一集团 / 关联企业',
  product: 'Sensor Module A 传感器模块',
  quantity: 100000,
  transferPrice: 5.00,
  sellerCost: 4.20,
  policyMarkup: 20,
  thirdPartyQuote: 5.80,
  thirdPartyQuantity: 20000,
  agreementDate: '2023-04-01',
  agreementStatus: '有合约，但需要确认 2026 年是否仍然适用',
  pricingPolicy: '成本加成 20%',
  shipping: '买方承担运费',
  warranty: '买方负责终端客户保修',
  inventoryRisk: '发货后由买方承担库存风险',
  paymentTerms: 'Net 15',
  priorYearRationale: false,
  managementApproval: false,
  volumeDiscountSupport: false,
  shippingAdjustment: false,
  warrantySupport: false,
  inventoryRiskSupport: false,
  comparableSupport: false,
  benchmarkDatabaseSupport: false,
  methodSelectionMemo: false,
  costSheetUpdated: true,
  invoiceAvailable: true,
  agreementAvailable: true,
  notes: '公司解释说，价格较低是因为采购量大，而且美国买方承担运费、保修和库存风险。但这些解释还没有被完整文件化。',
  reviewerDecision: '待处理',
  reviewerNotes: ''
};

const futureModules = [
  {
    name: 'R&D Tax Credit 研发税收抵免',
    status: '未来模块',
    problem: '研发费用、项目记录、员工工时、技术不确定性证据分散。',
    evidence: ['项目说明', '研发人员工时', '工资/费用明细', '技术实验记录', '管理层说明'],
    output: '生成研发税收抵免 evidence package 和缺失文件清单。'
  },
  {
    name: 'Withholding Tax 预提税文件',
    status: '未来模块',
    problem: '跨境付款常常缺税收协定、受益所有人、付款性质等支持文件。',
    evidence: ['付款记录', '合同', '税收居民证明', '受益所有人声明', '适用税率依据'],
    output: '提示预提税文件缺口和复核责任人。'
  },
  {
    name: 'VAT / GST 发票证据',
    status: '未来模块',
    problem: '发票、税率、供应地点、客户信息不一致时，后续审查成本很高。',
    evidence: ['发票', '订单', '发货/服务记录', '客户地点', '税率规则'],
    output: '整理发票证据、异常项和审查包。'
  },
  {
    name: 'Intercompany Service Fee 关联服务费',
    status: '未来模块',
    problem: '集团内部服务费需要证明服务真实发生、受益方是谁、分摊逻辑是什么。',
    evidence: ['服务协议', '服务清单', '成本池', '分摊方法', '受益方确认'],
    output: '生成服务费支持文件清单和风险提示。'
  }
];

let state = loadState();
let activeTab = 'overview';

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return saved || { case: { ...defaultCase } };
  } catch {
    return { case: { ...defaultCase } };
  }
}
function saveState() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function money(n) { return `$${Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`; }
function pct(n) { return `${Number(n || 0).toFixed(1)}%`; }
function num(id) { return Number(document.getElementById(id).value || 0); }
function str(id) { return document.getElementById(id).value; }
function bool(id) { return document.getElementById(id).checked; }
function pill(text, tone = 'neutral') { return `<span class="pill ${tone}">${text}</span>`; }
function riskTone(risk) { return risk === '高' ? 'danger' : risk === '中' ? 'warn' : 'success'; }
function list(items) { return items.length ? `<ul>${items.map(x => `<li>${x}</li>`).join('')}</ul>` : '<div class="empty">目前没有标记项目。</div>'; }

function calc(c) {
  const costPlusPrice = c.sellerCost * (1 + c.policyMarkup / 100);
  const actualMarkup = c.sellerCost ? ((c.transferPrice - c.sellerCost) / c.sellerCost) * 100 : 0;
  const quoteGap = c.thirdPartyQuote ? ((c.thirdPartyQuote - c.transferPrice) / c.thirdPartyQuote) * 100 : 0;

  const known = [];
  if (c.invoiceAvailable) known.push(`发票显示：${c.seller} 向 ${c.buyer} 销售 ${Number(c.quantity).toLocaleString()} 个单位，单价为 ${money(c.transferPrice)}。`);
  if (c.costSheetUpdated) known.push(`成本表显示：卖方每单位制造成本为 ${money(c.sellerCost)}。`);
  if (c.agreementAvailable) known.push(`关联企业合约存在，并写明定价政策为：${c.pricingPolicy}。`);
  known.push(`实际成本加成率为 ${pct(actualMarkup)}。`);
  known.push(`按照成本加成政策，理论价格约为 ${money(costPlusPrice)}。`);
  if (c.thirdPartyQuote) known.push(`目前找到一份第三方报价：${money(c.thirdPartyQuote)} / 单位，数量为 ${Number(c.thirdPartyQuantity).toLocaleString()} 个单位。`);
  known.push(`交易条件：${c.shipping}；${c.warranty}；${c.inventoryRisk}；付款条件 ${c.paymentTerms}。`);

  const missing = [];
  if (!c.invoiceAvailable) missing.push({ owner: '会计部门', item: '发票或交易清单', reason: '需要证明这笔交易实际发生。' });
  if (!c.costSheetUpdated) missing.push({ owner: '制造财务部门', item: '最新成本表', reason: '没有最新成本，就无法检查成本加成逻辑。' });
  if (!c.agreementAvailable) missing.push({ owner: '法务 / 税务', item: '关联企业合约', reason: '定价政策和风险分配需要书面依据。' });
  if (!c.volumeDiscountSupport) missing.push({ owner: '采购 / 销售运营', item: '大量采购折扣依据', reason: '关联方交易数量较大，价格较低可能需要用数量折扣解释。' });
  if (!c.shippingAdjustment) missing.push({ owner: '运营 / 物流', item: '运费差异调整依据', reason: '第三方报价可能包含卖方承担运费，而本交易由买方承担运费。' });
  if (!c.warrantySupport) missing.push({ owner: '销售 / 客服', item: '保修责任证明', reason: '如果买方承担保修，较低价格才可能有解释空间。' });
  if (!c.inventoryRiskSupport) missing.push({ owner: '运营 / 财务', item: '库存风险承担证明', reason: '风险由谁承担会影响价格可比性。' });
  if (!c.comparableSupport) missing.push({ owner: '税务 / 外部顾问', item: '可比交易调整或基准分析', reason: '不能直接拿原始第三方报价做结论，需要调整分析。' });
  if (!c.benchmarkDatabaseSupport) missing.push({ owner: '税务 / 外部顾问', item: 'benchmarking 数据库支持', reason: '真实项目通常需要从数据库按行业代码筛选可比公司或可比交易。' });
  if (!c.methodSelectionMemo) missing.push({ owner: '税务经理 / TP 专家', item: '方法选择备忘录', reason: '不同交易可能适用 Cost Plus、TNMM、Berry Ratio 等不同方法，不能只写死一种方法。' });
  if (!c.priorYearRationale) missing.push({ owner: '税务部门', item: '上一年度定价解释', reason: '需要保留历史解释，避免每年从零开始。' });
  if (!c.managementApproval) missing.push({ owner: 'Controller / 税务经理', item: '管理层批准备忘录', reason: '需要正式商业理由，而不是口头解释。' });

  const supportPoints = [];
  const policyDelta = Math.abs(c.transferPrice - costPlusPrice);
  if (policyDelta <= Math.max(0.1, costPlusPrice * 0.03)) supportPoints.push(`转让价格 ${money(c.transferPrice)} 接近 ${c.pricingPolicy} 下的理论价格 ${money(costPlusPrice)}。`);
  if (actualMarkup > 0) supportPoints.push(`卖方不是零利润或亏损出售，当前成本下仍有 ${pct(actualMarkup)} 的毛利加成。`);
  if (String(c.shipping).includes('买方')) supportPoints.push('买方承担运费，可能解释为什么价格低于包含运费的第三方报价。');
  if (String(c.warranty).includes('买方')) supportPoints.push('买方承担终端客户保修责任，如果有文件支持，可以解释较低售价。');
  if (String(c.inventoryRisk).includes('买方')) supportPoints.push('买方承担库存风险，如果有文件支持，可以作为可比性调整因素。');

  const riskSignals = [];
  if (quoteGap > 10) riskSignals.push(`关联方价格比原始第三方报价低 ${pct(quoteGap)}。`);
  if (actualMarkup < c.policyMarkup - 5) riskSignals.push(`实际加成率 ${pct(actualMarkup)} 明显低于政策加成率 ${pct(c.policyMarkup)}。`);
  if (missing.length >= 6) riskSignals.push('多项核心支持文件缺失或尚未确认。');
  if (String(c.agreementStatus).includes('需要') || String(c.agreementStatus).includes('过期')) riskSignals.push('合约状态尚未完成当年度确认。');

  const evidenceChecks = [
    c.invoiceAvailable,
    c.costSheetUpdated,
    c.agreementAvailable,
    c.volumeDiscountSupport,
    c.shippingAdjustment,
    c.warrantySupport,
    c.inventoryRiskSupport,
    c.comparableSupport,
    c.benchmarkDatabaseSupport,
    c.methodSelectionMemo,
    c.priorYearRationale,
    c.managementApproval
  ];
  const readiness = Math.round((evidenceChecks.filter(Boolean).length / evidenceChecks.length) * 100);

  let risk = '中';
  let riskScore = 55;
  if (readiness < 45 || riskSignals.length >= 4 || quoteGap > 20) { risk = '高'; riskScore = 82; }
  else if (readiness >= 75 && riskSignals.length <= 1) { risk = '低'; riskScore = 28; }

  const doNotConclude = [
    `不要因为管理层说 ${money(c.transferPrice)} 合理，就直接认定它符合独立交易原则。`,
    `不要只因为一份第三方报价是 ${money(c.thirdPartyQuote)}，就直接认定 ${money(c.transferPrice)} 有问题。`,
    '不要直接使用原始第三方报价；需要考虑数量、运费、保修、付款条件和风险承担差异。',
    '不要只依赖旧合约；需要确认它是否仍适用于当前年度。',
    '不要把 TP 当成整个产品天花板；它只是企业税证据准备度平台的第一个小切口。',
    '不要把这个 MVP 包装成完整 TP 专业系统；它现在只覆盖最简单的产品交易场景。'
  ];

  let recommendation = '建议由内部税务经理先审查证据包，再决定是否交给 TP 专家或外部顾问。';
  if (risk === '高') recommendation = '建议先补齐 benchmark、方法选择、可比性调整等关键资料，再进入专业复核。';
  if (risk === '低') recommendation = '证据准备度较高，可进入税务经理签核或外部顾问复核阶段，但仍不构成最终税务结论。';

  return { costPlusPrice, actualMarkup, quoteGap, known, missing, supportPoints, riskSignals, readiness, risk, riskScore, doNotConclude, recommendation };
}

function receipt() {
  const c = state.case;
  const r = calc(c);
  return {
    receipt_id: `${c.caseId}-${Date.now()}`,
    generated_at: new Date().toISOString(),
    product_positioning: 'Narrow beachhead: transfer pricing product sale. Broader platform: enterprise tax evidence readiness.',
    product_boundary: '本工具只做证据准备度和工作底稿管理，不提供税务、会计、法律或移转定价结论。',
    case: {
      case_id: c.caseId,
      module: c.module,
      transaction_type: c.transactionType,
      seller: c.seller,
      buyer: c.buyer,
      product: c.product,
      quantity: c.quantity,
      transfer_price: c.transferPrice,
      total_value: c.quantity * c.transferPrice,
      seller_cost: c.sellerCost,
      policy_markup: c.policyMarkup,
      third_party_quote: c.thirdPartyQuote
    },
    calculated_support: {
      policy_price_cost_plus: Number(r.costPlusPrice.toFixed(2)),
      actual_markup_on_cost_percent: Number(r.actualMarkup.toFixed(2)),
      raw_quote_gap_percent: Number(r.quoteGap.toFixed(2))
    },
    readiness: { evidence_readiness_score: r.readiness, risk: r.risk, risk_score: r.riskScore, recommendation: r.recommendation },
    known_evidence: r.known,
    support_points: r.supportPoints,
    risk_signals: r.riskSignals,
    missing_evidence: r.missing,
    do_not_conclude: r.doNotConclude,
    future_modules: futureModules,
    reviewer: { decision: c.reviewerDecision, notes: c.reviewerNotes }
  };
}

function download(filename, data, mime = 'application/json') {
  const blob = new Blob([mime === 'application/json' ? JSON.stringify(data, null, 2) : data], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
function setTab(tab) { activeTab = tab; render(); }
function resetDemo() { state = { case: { ...defaultCase } }; saveState(); render(); }
function updateFromForm() {
  const c = state.case;
  c.seller = str('seller'); c.buyer = str('buyer'); c.product = str('product');
  c.quantity = num('quantity'); c.transferPrice = num('transferPrice'); c.sellerCost = num('sellerCost');
  c.policyMarkup = num('policyMarkup'); c.thirdPartyQuote = num('thirdPartyQuote'); c.thirdPartyQuantity = num('thirdPartyQuantity');
  c.agreementDate = str('agreementDate'); c.agreementStatus = str('agreementStatus');
  c.shipping = str('shipping'); c.warranty = str('warranty'); c.inventoryRisk = str('inventoryRisk'); c.paymentTerms = str('paymentTerms'); c.notes = str('notes');
  c.invoiceAvailable = bool('invoiceAvailable'); c.costSheetUpdated = bool('costSheetUpdated'); c.agreementAvailable = bool('agreementAvailable');
  c.volumeDiscountSupport = bool('volumeDiscountSupport'); c.shippingAdjustment = bool('shippingAdjustment'); c.warrantySupport = bool('warrantySupport'); c.inventoryRiskSupport = bool('inventoryRiskSupport');
  c.comparableSupport = bool('comparableSupport'); c.benchmarkDatabaseSupport = bool('benchmarkDatabaseSupport'); c.methodSelectionMemo = bool('methodSelectionMemo');
  c.priorYearRationale = bool('priorYearRationale'); c.managementApproval = bool('managementApproval');
  saveState(); render();
}
function saveReviewer() { state.case.reviewerDecision = str('reviewerDecision'); state.case.reviewerNotes = str('reviewerNotes'); saveState(); render(); }
function evidenceCheckbox(id, label, checked) { return `<label class="check"><input id="${id}" type="checkbox" ${checked ? 'checked' : ''} onchange="updateFromForm()"/> <span>${label}</span></label>`; }
function missingTable(items) { return items.length ? `<table><thead><tr><th>负责人</th><th>缺失证据</th><th>为什么重要</th></tr></thead><tbody>${items.map(x => `<tr><td>${x.owner}</td><td><b>${x.item}</b></td><td>${x.reason}</td></tr>`).join('')}</tbody></table>` : '<div class="empty">目前没有缺失证据。</div>'; }
function moduleCards(){ return futureModules.map(m => `<div class="metric"><span>${m.status}</span><b>${m.name}</b><small>${m.problem}</small></div>`).join(''); }

function renderOverview(c, r) {
  return `
    <section class="panel heroPanel">
      <div>
        <span class="eyebrow">根据 Jiayi 反馈更新 · 小切口，大方向</span>
        <h2>企业税证据准备度 MVP</h2>
        <p>这个 MVP 不再把自己定位成“完整移转定价工具”。更准确的定位是：先用一个最小 TP 产品交易场景验证企业税务 evidence readiness / documentation workflow。</p>
        <div class="heroActions"><button onclick="setTab('intake')">打开 TP 小切口</button><button class="secondary" onclick="setTab('roadmap')">看扩展方向</button></div>
      </div>
      <div class="caseCard"><b>Narrow Beachhead</b><span>${c.module}</span><div class="bigNumber">${r.readiness}%</div><small>证据准备度</small></div>
    </section>
    <div class="metrics">
      <div class="metric"><span>MVP 切入点</span><b>TP 产品交易</b><small>只覆盖最简单场景</small></div>
      <div class="metric"><span>平台方向</span><b>企业税</b><small>不被 TP 锁死</small></div>
      <div class="metric"><span>风险等级</span><b>${r.risk}</b><small>风险分数 ${r.riskScore}</small></div>
      <div class="metric"><span>政策价格</span><b>${money(r.costPlusPrice)}</b><small>成本加成 ${pct(c.policyMarkup)}</small></div>
      <div class="metric"><span>实际加成率</span><b>${pct(r.actualMarkup)}</b><small>卖方毛利加成</small></div>
    </div>
    <section class="panel"><div class="split"><div><h3>现在验证什么？</h3>${list(['企业税务团队是否需要把原始凭证、计算、对比、缺失文件和风险提示整理成 case。','内部税务经理是否愿意用 evidence readiness score 来判断哪些项目还没准备好。','是否需要把 reviewer notes、do-not-conclude 和 exportable package 留下来，避免每年从零开始。'])}</div><div><h3>不验证什么？</h3>${list(['不验证完整 TP 专业方法论。','不自动决定价格是否合法。','不试图覆盖所有产品、服务、特许权使用、TNMM、Berry Ratio 等复杂场景。'])}</div></div></section>
  `;
}

function renderIntake(c) {
  return `
    <section class="panel">
      <div class="panelHead"><div><span class="eyebrow">第一个小切口</span><h2>关联方产品销售 · TP Evidence Readiness</h2></div><button class="secondary" onclick="resetDemo()">重置演示</button></div>
      <div class="formGrid">
        <label>卖方公司<input id="seller" value="${c.seller}" onchange="updateFromForm()"/></label>
        <label>买方公司<input id="buyer" value="${c.buyer}" onchange="updateFromForm()"/></label>
        <label>产品<input id="product" value="${c.product}" onchange="updateFromForm()"/></label>
        <label>数量<input id="quantity" type="number" value="${c.quantity}" onchange="updateFromForm()"/></label>
        <label>每单位转让价格<input id="transferPrice" type="number" step="0.01" value="${c.transferPrice}" onchange="updateFromForm()"/></label>
        <label>卖方每单位成本<input id="sellerCost" type="number" step="0.01" value="${c.sellerCost}" onchange="updateFromForm()"/></label>
        <label>政策加成率 %<input id="policyMarkup" type="number" step="0.1" value="${c.policyMarkup}" onchange="updateFromForm()"/></label>
        <label>第三方报价 / 单位<input id="thirdPartyQuote" type="number" step="0.01" value="${c.thirdPartyQuote}" onchange="updateFromForm()"/></label>
        <label>第三方报价数量<input id="thirdPartyQuantity" type="number" value="${c.thirdPartyQuantity}" onchange="updateFromForm()"/></label>
        <label>合约日期<input id="agreementDate" type="date" value="${c.agreementDate}" onchange="updateFromForm()"/></label>
        <label>合约状态<input id="agreementStatus" value="${c.agreementStatus}" onchange="updateFromForm()"/></label>
        <label>付款条件<input id="paymentTerms" value="${c.paymentTerms}" onchange="updateFromForm()"/></label>
        <label>运费条款<input id="shipping" value="${c.shipping}" onchange="updateFromForm()"/></label>
        <label>保修责任<input id="warranty" value="${c.warranty}" onchange="updateFromForm()"/></label>
        <label>库存风险<input id="inventoryRisk" value="${c.inventoryRisk}" onchange="updateFromForm()"/></label>
      </div>
      <label class="wideLabel">管理层解释 / 备注<textarea id="notes" onchange="updateFromForm()">${c.notes}</textarea></label>
      <h3>证据清单</h3>
      <div class="checkGrid">
        ${evidenceCheckbox('invoiceAvailable', '已有发票', c.invoiceAvailable)}
        ${evidenceCheckbox('costSheetUpdated', '已有最新成本表', c.costSheetUpdated)}
        ${evidenceCheckbox('agreementAvailable', '已有关联企业合约', c.agreementAvailable)}
        ${evidenceCheckbox('volumeDiscountSupport', '已有大量采购折扣依据', c.volumeDiscountSupport)}
        ${evidenceCheckbox('shippingAdjustment', '已有运费差异调整依据', c.shippingAdjustment)}
        ${evidenceCheckbox('warrantySupport', '已有保修责任证明', c.warrantySupport)}
        ${evidenceCheckbox('inventoryRiskSupport', '已有库存风险证明', c.inventoryRiskSupport)}
        ${evidenceCheckbox('comparableSupport', '已有可比交易调整', c.comparableSupport)}
        ${evidenceCheckbox('benchmarkDatabaseSupport', '已有 benchmarking 数据库支持', c.benchmarkDatabaseSupport)}
        ${evidenceCheckbox('methodSelectionMemo', '已有方法选择备忘录', c.methodSelectionMemo)}
        ${evidenceCheckbox('priorYearRationale', '已有上一年度定价解释', c.priorYearRationale)}
        ${evidenceCheckbox('managementApproval', '已有管理层批准备忘录', c.managementApproval)}
      </div>
    </section>
  `;
}

function renderEvidence(c, r) { return `<section class="panel"><span class="eyebrow">证据审查</span><h2>目前已知事实</h2>${list(r.known)}</section><section class="panel"><span class="eyebrow">缺失证据</span><h2>需要哪些部门补资料？</h2>${missingTable(r.missing)}</section>`; }
function renderGuardrails(r) { return `<section class="panel"><span class="eyebrow">判断边界</span><h2>现在不能直接下的结论</h2><p>这些限制是为了保留专业判断空间，也避免把 MVP 夸大成完整 TP 系统。</p>${list(r.doNotConclude)}</section><section class="panel"><span class="eyebrow">审查分流</span><h2>下一步应该给谁看？</h2><div class="routeBox"><div>${pill('主要审查人', 'blue')} <b>内部税务经理</b><span>审查证据准备度、缺失文件和管理层解释。</span></div><div>${pill('专业复核', 'purple')} <b>移转定价专家 / 外部顾问</b><span>判断方法选择、可比性调整和最终文件策略。</span></div><div>${pill('产品验证问题', 'neutral')} <b>企业税流程 owner</b><span>判断这个 evidence readiness workflow 是否能扩展到其他企业税场景。</span></div></div></section>`; }
function renderRoadmap(){ return `<section class="panel"><span class="eyebrow">Scalable direction</span><h2>不是只做 TP，而是企业税证据准备度平台</h2><p>Jiayi 的反馈是对的：TP 很专业，也偏小众。所以这个 MVP 应该用 TP 产品交易做窄切口，但未来平台能力要能迁移到更多企业税场景。</p><div class="metrics">${moduleCards()}</div></section><section class="panel"><h2>统一底层 workflow</h2>${list(['上传或录入原始凭证 / 内部数据。','系统提取或计算关键数值。','对比外部基准、规则或历史解释。','标出缺失文件、风险信号、责任人。','生成 reviewer-ready package，而不是直接给最终税务结论。'])}</section>`; }
function renderReceipt(c, r) { return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">可交付证据包</span><h2>证据准备度 Receipt</h2></div><button onclick="download('企业税证据准备度_receipt.json', receipt())">导出 JSON</button></div><p>这不是税务结论，而是一个结构化工作底稿：列出交易事实、支持点、缺口、风险、边界和未来可扩展模块。</p><pre>${JSON.stringify(receipt(), null, 2)}</pre></section><section class="panel"><span class="eyebrow">内部审查记录</span><h2>Reviewer 更新</h2><div class="formGrid two"><label>处理状态<select id="reviewerDecision"><option ${c.reviewerDecision === '待处理' ? 'selected' : ''}>待处理</option><option ${c.reviewerDecision === '需要补文件' ? 'selected' : ''}>需要补文件</option><option ${c.reviewerDecision === '可交给专家复核' ? 'selected' : ''}>可交给专家复核</option><option ${c.reviewerDecision === '已关闭' ? 'selected' : ''}>已关闭</option></select></label><label>Reviewer 备注<textarea id="reviewerNotes">${c.reviewerNotes}</textarea></label></div><button onclick="saveReviewer()">保存审查记录</button></section>`; }

function render() {
  const c = state.case;
  const r = calc(c);
  const tabs = [['overview', '总览'], ['intake', 'TP 小切口'], ['evidence', '证据与缺口'], ['guardrails', '边界与分流'], ['roadmap', '扩展方向'], ['receipt', '证据包']];
  let body = '';
  if (activeTab === 'overview') body = renderOverview(c, r);
  if (activeTab === 'intake') body = renderIntake(c);
  if (activeTab === 'evidence') body = renderEvidence(c, r);
  if (activeTab === 'guardrails') body = renderGuardrails(r);
  if (activeTab === 'roadmap') body = renderRoadmap();
  if (activeTab === 'receipt') body = renderReceipt(c, r);

  document.getElementById('app').innerHTML = `
    <aside>
      <div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>企业税证据 MVP</span></div></div>
      <nav>${tabs.map(([id, label]) => `<button class="${activeTab === id ? 'active' : ''}" onclick="setTab('${id}')">${label}</button>`).join('')}</nav>
      <div class="sideNote"><b>MVP 边界</b><span>现在只用 TP 产品交易验证流程；未来方向是企业税 evidence readiness。全部是合成数据。</span></div>
    </aside>
    <main>
      <header>
        <div><span class="eyebrow">CGIF · Enterprise Tax Evidence Readiness</span><h1>企业税证据准备度</h1><p>小切口：移转定价产品交易。大方向：可扩展的企业税证据、缺口、风险和审查包 workflow。</p></div>
        <div class="headerPills">${pill(r.risk + '风险', riskTone(r.risk))}${pill(r.readiness + '% 准备度', 'blue')}${pill('TP = 第一个 use case', 'purple')}</div>
      </header>
      ${body}
    </main>
  `;
}

window.setTab = setTab;
window.updateFromForm = updateFromForm;
window.resetDemo = resetDemo;
window.download = download;
window.receipt = receipt;
window.saveReviewer = saveReviewer;

render();
