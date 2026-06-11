const STORAGE_KEY = 'cgif-transfer-pricing-demo-v1';

const defaultCase = {
  caseId: 'TP-001',
  transactionType: 'Related-party product sale',
  seller: 'Taiwan Parts Co.',
  buyer: 'US Device Co.',
  relationship: 'Common ownership / controlled group',
  product: 'Sensor Module A',
  quantity: 100000,
  transferPrice: 5.00,
  sellerCost: 4.20,
  policyMarkup: 20,
  thirdPartyQuote: 5.80,
  thirdPartyQuantity: 20000,
  agreementDate: '2023-04-01',
  agreementStatus: 'Available but needs current-year confirmation',
  pricingPolicy: 'Cost plus 20%',
  shipping: 'Buyer pays freight',
  warranty: 'Buyer handles end-customer warranty',
  inventoryRisk: 'Buyer assumes inventory risk after shipment',
  paymentTerms: 'Net 15',
  priorYearRationale: false,
  managementApproval: false,
  volumeDiscountSupport: false,
  shippingAdjustment: false,
  warrantySupport: false,
  inventoryRiskSupport: false,
  comparableSupport: false,
  costSheetUpdated: true,
  invoiceAvailable: true,
  agreementAvailable: true,
  notes: 'Client says the lower price is due to high volume and buyer-assumed risks, but support is not fully documented yet.',
  reviewerDecision: 'Open',
  reviewerNotes: ''
};

let state = loadState();
let activeTab = 'overview';

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return saved || { case: defaultCase };
  } catch {
    return { case: defaultCase };
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function money(n) {
  return `$${Number(n || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function pct(n) {
  return `${Number(n || 0).toFixed(1)}%`;
}

function num(id) {
  return Number(document.getElementById(id).value || 0);
}

function str(id) {
  return document.getElementById(id).value;
}

function bool(id) {
  return document.getElementById(id).checked;
}

function calc(c) {
  const costPlusPrice = c.sellerCost * (1 + c.policyMarkup / 100);
  const actualMarkup = c.sellerCost ? ((c.transferPrice - c.sellerCost) / c.sellerCost) * 100 : 0;
  const quoteGap = c.thirdPartyQuote ? ((c.thirdPartyQuote - c.transferPrice) / c.thirdPartyQuote) * 100 : 0;

  const known = [];
  if (c.invoiceAvailable) known.push(`Invoice shows ${c.seller} sold ${Number(c.quantity).toLocaleString()} units to ${c.buyer} at ${money(c.transferPrice)} per unit.`);
  if (c.costSheetUpdated) known.push(`Updated cost sheet shows seller cost of ${money(c.sellerCost)} per unit.`);
  if (c.agreementAvailable) known.push(`Intercompany agreement is available and states ${c.pricingPolicy}.`);
  known.push(`Actual markup on cost is ${pct(actualMarkup)}.`);
  known.push(`Policy price under cost-plus logic would be approximately ${money(costPlusPrice)}.`);
  if (c.thirdPartyQuote) known.push(`One third-party quote is ${money(c.thirdPartyQuote)} per unit for ${Number(c.thirdPartyQuantity).toLocaleString()} units.`);
  known.push(`Transaction terms: ${c.shipping}; ${c.warranty}; ${c.inventoryRisk}; payment term ${c.paymentTerms}.`);

  const missing = [];
  if (!c.invoiceAvailable) missing.push({ owner: 'Accounting', item: 'Invoice or transaction listing', reason: 'Need basic proof that the transaction occurred.' });
  if (!c.costSheetUpdated) missing.push({ owner: 'Manufacturing Finance', item: 'Updated cost sheet', reason: 'Cost-plus support cannot be checked without current cost data.' });
  if (!c.agreementAvailable) missing.push({ owner: 'Legal / Tax', item: 'Intercompany agreement', reason: 'Pricing policy and risk allocation need written support.' });
  if (!c.volumeDiscountSupport) missing.push({ owner: 'Procurement / Sales Ops', item: 'Volume discount support', reason: 'The related-party order is larger than the third-party quote; the discount needs evidence.' });
  if (!c.shippingAdjustment) missing.push({ owner: 'Operations / Logistics', item: 'Shipping term adjustment', reason: 'Third-party quote may include seller-paid freight while related party buyer pays freight.' });
  if (!c.warrantySupport) missing.push({ owner: 'Sales / Customer Service', item: 'Warranty responsibility support', reason: 'Lower price may be supportable only if buyer truly handles warranty risk.' });
  if (!c.inventoryRiskSupport) missing.push({ owner: 'Operations / Finance', item: 'Inventory risk documentation', reason: 'Risk allocation affects pricing comparability.' });
  if (!c.comparableSupport) missing.push({ owner: 'Tax / External Advisor', item: 'Comparable adjustment or benchmark support', reason: 'Raw third-party quote cannot be used without adjustment analysis.' });
  if (!c.priorYearRationale) missing.push({ owner: 'Tax', item: 'Prior-year pricing rationale', reason: 'Need continuity and explanation of any year-over-year changes.' });
  if (!c.managementApproval) missing.push({ owner: 'Controller / Tax Manager', item: 'Management approval memo', reason: 'Need documented business rationale, not just verbal explanation.' });

  const supportPoints = [];
  const policyDelta = Math.abs(c.transferPrice - costPlusPrice);
  if (policyDelta <= Math.max(0.1, costPlusPrice * 0.03)) supportPoints.push(`Transfer price ${money(c.transferPrice)} is close to policy price ${money(costPlusPrice)} under ${c.pricingPolicy}.`);
  if (actualMarkup > 0) supportPoints.push(`Seller earns a positive gross markup of ${pct(actualMarkup)} on current cost data.`);
  if (String(c.shipping).toLowerCase().includes('buyer')) supportPoints.push('Buyer-paid freight may explain part of the gap versus a seller-paid third-party quote.');
  if (String(c.warranty).toLowerCase().includes('buyer')) supportPoints.push('Buyer-handled warranty may support a lower product price if documented.');
  if (String(c.inventoryRisk).toLowerCase().includes('buyer')) supportPoints.push('Buyer-assumed inventory risk may support comparability adjustment if documented.');

  const riskSignals = [];
  if (quoteGap > 10) riskSignals.push(`Related-party price is ${pct(quoteGap)} below the raw third-party quote.`);
  if (actualMarkup < c.policyMarkup - 5) riskSignals.push(`Actual markup ${pct(actualMarkup)} is materially below stated policy markup ${pct(c.policyMarkup)}.`);
  if (missing.length >= 6) riskSignals.push('Several core support documents are missing or unconfirmed.');
  if (String(c.agreementStatus).toLowerCase().includes('needs') || String(c.agreementStatus).toLowerCase().includes('expired')) riskSignals.push('Agreement status is not fully current-year confirmed.');

  const evidenceChecks = [
    c.invoiceAvailable,
    c.costSheetUpdated,
    c.agreementAvailable,
    c.volumeDiscountSupport,
    c.shippingAdjustment,
    c.warrantySupport,
    c.inventoryRiskSupport,
    c.comparableSupport,
    c.priorYearRationale,
    c.managementApproval
  ];
  const readiness = Math.round((evidenceChecks.filter(Boolean).length / evidenceChecks.length) * 100);

  let risk = 'Medium';
  let riskScore = 55;
  if (readiness < 45 || riskSignals.length >= 4 || quoteGap > 20) { risk = 'High'; riskScore = 82; }
  else if (readiness >= 75 && riskSignals.length <= 1) { risk = 'Low'; riskScore = 28; }
  else if (readiness >= 60 && riskSignals.length <= 2) { risk = 'Medium'; riskScore = 50; }

  const nextOwners = missing.slice(0, 5);
  const doNotConclude = [
    `Do not conclude ${money(c.transferPrice)} is arm's length only because management says it is reasonable.`,
    `Do not conclude ${money(c.transferPrice)} is improper solely because one third-party quote is ${money(c.thirdPartyQuote)}.`,
    'Do not use the raw comparable quote without adjusting for volume, shipping, warranty, payment terms, and risk allocation.',
    'Do not rely on an older agreement without confirming it still applies to the current year.',
    'Do not present one fixed answer if the evidence only supports a defensible range.'
  ];

  let recommendation = 'Tax manager should review the evidence package before external advisor or auditor use.';
  if (risk === 'High') recommendation = 'Escalate to transfer pricing specialist / external advisor after internal owners fill missing documents.';
  if (risk === 'Low') recommendation = 'Ready for tax manager sign-off and advisor/auditor package export, subject to professional review.';

  return { costPlusPrice, actualMarkup, quoteGap, known, missing, supportPoints, riskSignals, readiness, risk, riskScore, nextOwners, doNotConclude, recommendation };
}

function receipt() {
  const c = state.case;
  const r = calc(c);
  return {
    receipt_id: `${c.caseId}-${Date.now()}`,
    generated_at: new Date().toISOString(),
    product_boundary: 'Evidence readiness and workpaper control only. Not tax, accounting, legal, or transfer pricing advice.',
    case: {
      case_id: c.caseId,
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
    readiness: {
      evidence_readiness_score: r.readiness,
      risk: r.risk,
      risk_score: r.riskScore,
      recommendation: r.recommendation
    },
    known_evidence: r.known,
    support_points: r.supportPoints,
    risk_signals: r.riskSignals,
    missing_evidence: r.missing,
    do_not_conclude: r.doNotConclude,
    reviewer: {
      decision: c.reviewerDecision,
      notes: c.reviewerNotes
    }
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

function setTab(tab) {
  activeTab = tab;
  render();
}

function updateFromForm() {
  const c = state.case;
  c.seller = str('seller');
  c.buyer = str('buyer');
  c.product = str('product');
  c.quantity = num('quantity');
  c.transferPrice = num('transferPrice');
  c.sellerCost = num('sellerCost');
  c.policyMarkup = num('policyMarkup');
  c.thirdPartyQuote = num('thirdPartyQuote');
  c.thirdPartyQuantity = num('thirdPartyQuantity');
  c.agreementDate = str('agreementDate');
  c.agreementStatus = str('agreementStatus');
  c.shipping = str('shipping');
  c.warranty = str('warranty');
  c.inventoryRisk = str('inventoryRisk');
  c.paymentTerms = str('paymentTerms');
  c.notes = str('notes');
  c.invoiceAvailable = bool('invoiceAvailable');
  c.costSheetUpdated = bool('costSheetUpdated');
  c.agreementAvailable = bool('agreementAvailable');
  c.volumeDiscountSupport = bool('volumeDiscountSupport');
  c.shippingAdjustment = bool('shippingAdjustment');
  c.warrantySupport = bool('warrantySupport');
  c.inventoryRiskSupport = bool('inventoryRiskSupport');
  c.comparableSupport = bool('comparableSupport');
  c.priorYearRationale = bool('priorYearRationale');
  c.managementApproval = bool('managementApproval');
  saveState();
  render();
}

function saveReviewer() {
  state.case.reviewerDecision = str('reviewerDecision');
  state.case.reviewerNotes = str('reviewerNotes');
  saveState();
  render();
}

function resetDemo() {
  state = { case: { ...defaultCase } };
  saveState();
  render();
}

function pill(text, tone = 'neutral') {
  return `<span class="pill ${tone}">${text}</span>`;
}

function list(items) {
  if (!items.length) return '<div class="empty">No items flagged.</div>';
  return `<ul>${items.map(x => `<li>${x}</li>`).join('')}</ul>`;
}

function missingTable(items) {
  if (!items.length) return '<div class="empty">No missing evidence flagged.</div>';
  return `<table><thead><tr><th>Owner</th><th>Missing evidence</th><th>Why it matters</th></tr></thead><tbody>${items.map(x => `<tr><td>${x.owner}</td><td><b>${x.item}</b></td><td>${x.reason}</td></tr>`).join('')}</tbody></table>`;
}

function evidenceCheckbox(id, label, checked) {
  return `<label class="check"><input id="${id}" type="checkbox" ${checked ? 'checked' : ''} onchange="updateFromForm()"/> <span>${label}</span></label>`;
}

function renderOverview(c, r) {
  return `
    <section class="panel heroPanel">
      <div>
        <span class="eyebrow">Phase 1 narrow demo · Related-party product sale only</span>
        <h2>${c.seller} → ${c.buyer}</h2>
        <p>This demo does not decide whether the transfer price is compliant. It organizes evidence, missing support, owner requests, and an advisor-ready receipt.</p>
        <div class="heroActions">
          <button onclick="setTab('intake')">Edit transaction facts</button>
          <button class="secondary" onclick="download('tp_advisor_ready_receipt.json', receipt())">Export advisor-ready receipt</button>
        </div>
      </div>
      <div class="caseCard">
        <b>${c.caseId}</b>
        <span>${c.transactionType}</span>
        <div class="bigNumber">${money(c.transferPrice)}</div>
        <small>Transfer price per unit</small>
      </div>
    </section>
    <div class="metrics">
      <div class="metric"><span>Evidence readiness</span><b>${r.readiness}%</b><small>10 support checks</small></div>
      <div class="metric"><span>Risk</span><b>${r.risk}</b><small>Score ${r.riskScore}</small></div>
      <div class="metric"><span>Policy price</span><b>${money(r.costPlusPrice)}</b><small>Cost plus ${pct(c.policyMarkup)}</small></div>
      <div class="metric"><span>Actual markup</span><b>${pct(r.actualMarkup)}</b><small>Seller gross markup</small></div>
      <div class="metric"><span>Quote gap</span><b>${pct(r.quoteGap)}</b><small>Below raw third-party quote</small></div>
    </div>
    <section class="panel">
      <div class="split">
        <div>
          <h3>Current system finding</h3>
          <p class="finding ${r.risk.toLowerCase()}">${r.recommendation}</p>
          <h3>Support points</h3>
          ${list(r.supportPoints)}
        </div>
        <div>
          <h3>Risk signals</h3>
          ${list(r.riskSignals)}
          <h3>Product boundary</h3>
          <div class="boundary">Evidence readiness only. No final tax, accounting, legal, or transfer pricing conclusion.</div>
        </div>
      </div>
    </section>
  `;
}

function renderIntake(c) {
  return `
    <section class="panel">
      <div class="panelHead"><div><span class="eyebrow">Transaction intake</span><h2>Related-party product sale facts</h2></div><button class="secondary" onclick="resetDemo()">Reset demo</button></div>
      <div class="formGrid">
        <label>Seller entity<input id="seller" value="${c.seller}" onchange="updateFromForm()"/></label>
        <label>Buyer entity<input id="buyer" value="${c.buyer}" onchange="updateFromForm()"/></label>
        <label>Product<input id="product" value="${c.product}" onchange="updateFromForm()"/></label>
        <label>Quantity<input id="quantity" type="number" value="${c.quantity}" onchange="updateFromForm()"/></label>
        <label>Transfer price / unit<input id="transferPrice" type="number" step="0.01" value="${c.transferPrice}" onchange="updateFromForm()"/></label>
        <label>Seller cost / unit<input id="sellerCost" type="number" step="0.01" value="${c.sellerCost}" onchange="updateFromForm()"/></label>
        <label>Policy markup %<input id="policyMarkup" type="number" step="0.1" value="${c.policyMarkup}" onchange="updateFromForm()"/></label>
        <label>Third-party quote / unit<input id="thirdPartyQuote" type="number" step="0.01" value="${c.thirdPartyQuote}" onchange="updateFromForm()"/></label>
        <label>Third-party quote quantity<input id="thirdPartyQuantity" type="number" value="${c.thirdPartyQuantity}" onchange="updateFromForm()"/></label>
        <label>Agreement date<input id="agreementDate" type="date" value="${c.agreementDate}" onchange="updateFromForm()"/></label>
        <label>Agreement status<input id="agreementStatus" value="${c.agreementStatus}" onchange="updateFromForm()"/></label>
        <label>Payment terms<input id="paymentTerms" value="${c.paymentTerms}" onchange="updateFromForm()"/></label>
        <label>Shipping terms<input id="shipping" value="${c.shipping}" onchange="updateFromForm()"/></label>
        <label>Warranty responsibility<input id="warranty" value="${c.warranty}" onchange="updateFromForm()"/></label>
        <label>Inventory risk<input id="inventoryRisk" value="${c.inventoryRisk}" onchange="updateFromForm()"/></label>
      </div>
      <label class="wideLabel">Management explanation / notes<textarea id="notes" onchange="updateFromForm()">${c.notes}</textarea></label>
      <h3>Evidence checklist</h3>
      <div class="checkGrid">
        ${evidenceCheckbox('invoiceAvailable', 'Invoice available', c.invoiceAvailable)}
        ${evidenceCheckbox('costSheetUpdated', 'Updated cost sheet available', c.costSheetUpdated)}
        ${evidenceCheckbox('agreementAvailable', 'Intercompany agreement available', c.agreementAvailable)}
        ${evidenceCheckbox('volumeDiscountSupport', 'Volume discount support attached', c.volumeDiscountSupport)}
        ${evidenceCheckbox('shippingAdjustment', 'Shipping adjustment documented', c.shippingAdjustment)}
        ${evidenceCheckbox('warrantySupport', 'Warranty responsibility documented', c.warrantySupport)}
        ${evidenceCheckbox('inventoryRiskSupport', 'Inventory risk documented', c.inventoryRiskSupport)}
        ${evidenceCheckbox('comparableSupport', 'Comparable / benchmark support attached', c.comparableSupport)}
        ${evidenceCheckbox('priorYearRationale', 'Prior-year rationale available', c.priorYearRationale)}
        ${evidenceCheckbox('managementApproval', 'Management approval memo available', c.managementApproval)}
      </div>
    </section>
  `;
}

function renderEvidence(c, r) {
  return `
    <section class="panel">
      <span class="eyebrow">Evidence review</span>
      <h2>What is known</h2>
      ${list(r.known)}
    </section>
    <section class="panel">
      <span class="eyebrow">Missing support</span>
      <h2>Document owner requests</h2>
      ${missingTable(r.missing)}
    </section>
  `;
}

function renderGuardrails(r) {
  return `
    <section class="panel">
      <span class="eyebrow">Judgment boundary</span>
      <h2>Do not conclude</h2>
      <p>These guardrails preserve professional judgment space. The tool should not write the tax conclusion for the company.</p>
      ${list(r.doNotConclude)}
    </section>
    <section class="panel">
      <span class="eyebrow">Reviewer routing</span>
      <h2>Who should review next?</h2>
      <div class="routeBox">
        <div>${pill('Primary reviewer', 'blue')} <b>Internal Tax Manager</b><span>Review evidence readiness, owner requests, and management rationale.</span></div>
        <div>${pill('Secondary reviewer', 'purple')} <b>Transfer Pricing Specialist / External Advisor</b><span>Evaluate method selection, comparability adjustments, and final documentation.</span></div>
        <div>${pill('Document owners', 'neutral')} <b>Legal, Operations, Sales, Procurement, Finance</b><span>Fill missing support before final review.</span></div>
      </div>
    </section>
  `;
}

function renderReceipt(c, r) {
  const data = receipt();
  return `
    <section class="panel">
      <div class="panelHead"><div><span class="eyebrow">Advisor-ready package</span><h2>Evidence receipt</h2></div><button onclick="download('tp_advisor_ready_receipt.json', receipt())">Export JSON</button></div>
      <p>This is the output you would show Jiayi: not a legal/tax answer, but a structured workpaper showing facts, evidence gaps, risk, and next owners.</p>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    </section>
    <section class="panel">
      <span class="eyebrow">Reviewer note</span>
      <h2>Internal review update</h2>
      <div class="formGrid two">
        <label>Decision status<select id="reviewerDecision"><option ${c.reviewerDecision === 'Open' ? 'selected' : ''}>Open</option><option ${c.reviewerDecision === 'Needs documents' ? 'selected' : ''}>Needs documents</option><option ${c.reviewerDecision === 'Ready for specialist review' ? 'selected' : ''}>Ready for specialist review</option><option ${c.reviewerDecision === 'Closed' ? 'selected' : ''}>Closed</option></select></label>
        <label>Reviewer notes<textarea id="reviewerNotes">${c.reviewerNotes}</textarea></label>
      </div>
      <button onclick="saveReviewer()">Save reviewer update</button>
    </section>
  `;
}

function render() {
  const c = state.case;
  const r = calc(c);
  const tabs = [
    ['overview', 'Overview'],
    ['intake', 'Transaction Intake'],
    ['evidence', 'Evidence & Missing Docs'],
    ['guardrails', 'Guardrails & Routing'],
    ['receipt', 'Advisor Package']
  ];
  let body = '';
  if (activeTab === 'overview') body = renderOverview(c, r);
  if (activeTab === 'intake') body = renderIntake(c);
  if (activeTab === 'evidence') body = renderEvidence(c, r);
  if (activeTab === 'guardrails') body = renderGuardrails(r);
  if (activeTab === 'receipt') body = renderReceipt(c, r);

  document.getElementById('app').innerHTML = `
    <aside>
      <div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>Transfer Pricing MVP</span></div></div>
      <nav>${tabs.map(([id, label]) => `<button class="${activeTab === id ? 'active' : ''}" onclick="setTab('${id}')">${label}</button>`).join('')}</nav>
      <div class="sideNote">
        <b>Demo boundary</b>
        <span>Only one case type: related-party product sale. Synthetic data only.</span>
      </div>
    </aside>
    <main>
      <header>
        <div>
          <span class="eyebrow">CGIF Phase 1 MVP</span>
          <h1>Transfer Pricing Evidence Readiness</h1>
          <p>Make the company ready to explain a related-party product sale before final tax or advisor review.</p>
        </div>
        <div class="headerPills">${pill(r.risk + ' risk', r.risk === 'High' ? 'danger' : r.risk === 'Medium' ? 'warn' : 'success')}${pill(r.readiness + '% ready', 'blue')}</div>
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
