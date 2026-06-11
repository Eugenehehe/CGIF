const STORAGE_KEY = 'cgif-ufit-asset-scenario-v1';

const defaultCase = {
  caseId: 'UFIT-ASSET-001',
  scenario: 'Device received, deployed, but Flowtrac location may be stale',
  assetType: 'Wireless access point',
  model: 'Cisco Catalyst AP - synthetic',
  serialVendor: 'SYNAP230B018',
  serialFlowtrac: 'SYNAP230B018',
  assetTag: 'UF-SYN-230B-018',
  purchaseTicket: 'REQ-2026-SYN-104',
  quoteStatus: 'Three vendor quotes requested and attached',
  receivingSheet: true,
  flowtracExists: true,
  flowtracBin: 'SSRB Stock',
  flowtracRack: '',
  flowtracU: '',
  warehouseScan: true,
  deploymentEvidence: true,
  technicianTicket: false,
  observedBuilding: 'SSRB',
  observedRoom: '230B',
  observedRack: 'TR02',
  observedU: 'U18',
  apSourceMatch: true,
  lansweeperMatch: true,
  physicalAudit: false,
  binTransportTicket: false,
  dateReceived: '2026-05-20',
  dateDeployed: '2026-06-05',
  notes: 'Synthetic case based on the UFIT pattern: warehouse received the device and Flowtrac was created, but the technician deployment/bin transportation update may be missing.',
  reviewerDecision: 'Open',
  reviewerNotes: ''
};

let state = loadState();
let activeTab = 'overview';

function loadState(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { case: defaultCase }; }
  catch { return { case: defaultCase }; }
}
function saveState(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function str(id){ return document.getElementById(id).value; }
function bool(id){ return document.getElementById(id).checked; }
function pill(text, tone='neutral'){ return `<span class="pill ${tone}">${text}</span>`; }
function riskTone(r){ return r === 'High' ? 'danger' : r === 'Medium' ? 'warn' : 'success'; }
function list(items){ return items.length ? `<ul>${items.map(x=>`<li>${x}</li>`).join('')}</ul>` : '<div class="empty">No items flagged.</div>'; }

function calc(c){
  const known = [];
  if(c.receivingSheet) known.push(`Receiving sheet shows ${c.model} was received for purchase/request ${c.purchaseTicket}.`);
  if(c.warehouseScan) known.push(`Warehouse scan / receiving spreadsheet captured serial ${c.serialVendor}.`);
  if(c.flowtracExists) known.push(`Flowtrac record exists for serial ${c.serialFlowtrac}.`);
  if(c.deploymentEvidence) known.push(`Deployment evidence suggests the device was installed in ${c.observedBuilding} ${c.observedRoom}, ${c.observedRack} ${c.observedU}.`);
  if(c.apSourceMatch) known.push('AP source confirms the same serial is active or observed in the wireless inventory source.');
  if(c.lansweeperMatch) known.push('Lansweeper source confirms the same serial or device identity appears in endpoint/network inventory.');
  if(c.physicalAudit) known.push('Physical audit confirms the observed room/rack/U location.');

  const missing = [];
  if(!c.receivingSheet) missing.push({ owner:'Warehouse / DCL', item:'Receiving spreadsheet or scan record', reason:'Need proof that the asset entered inventory.' });
  if(!c.flowtracExists) missing.push({ owner:'DCL Inventory', item:'Flowtrac asset record', reason:'Flowtrac is the working inventory system and needs a record to update.' });
  if(c.serialVendor && c.serialFlowtrac && c.serialVendor !== c.serialFlowtrac) missing.push({ owner:'DCL Inventory', item:'Serial mismatch review', reason:'Vendor/scan serial and Flowtrac serial do not match exactly.' });
  if(!c.technicianTicket) missing.push({ owner:'Technician / Deployment Team', item:'Deployment or bin transportation ticket', reason:'Physical movement may have happened without the ticket that normally triggers bin update.' });
  if(!c.binTransportTicket) missing.push({ owner:'DCL / Technician', item:'Bin transportation confirmation', reason:'Flowtrac bin may stay stale if bin change ticket was not submitted.' });
  if(!c.physicalAudit) missing.push({ owner:'DCL Student Ops / Inventory Audit', item:'Physical room/rack/U verification', reason:'Need final evidence before changing Flowtrac location with confidence.' });
  if(!c.apSourceMatch) missing.push({ owner:'Network / AP Source Owner', item:'AP source verification', reason:'Need device-source evidence to support the deployed location.' });
  if(!c.lansweeperMatch) missing.push({ owner:'Endpoint / Lansweeper Owner', item:'Lansweeper verification', reason:'Need second inventory source before closing discrepancy.' });

  const flowtracLooksStock = String(c.flowtracBin).toLowerCase().includes('stock') || String(c.flowtracBin).toLowerCase().includes('warehouse') || String(c.flowtracBin).toLowerCase().includes('spare');
  const hasObservedLocation = Boolean(c.observedBuilding && c.observedRoom && c.observedRack && c.observedU);
  const deployedButFlowtracStock = c.deploymentEvidence && hasObservedLocation && flowtracLooksStock;
  const serialMismatch = c.serialVendor && c.serialFlowtrac && c.serialVendor !== c.serialFlowtrac;

  const supportPoints = [];
  if(!serialMismatch) supportPoints.push('Vendor/scan serial and Flowtrac serial match, so the issue is likely location status rather than identity.');
  if(c.receivingSheet && c.warehouseScan) supportPoints.push('Receiving evidence supports that the asset entered inventory before deployment.');
  if(c.apSourceMatch || c.lansweeperMatch) supportPoints.push('External inventory source gives supporting evidence beyond Flowtrac.');
  if(deployedButFlowtracStock) supportPoints.push('Deployment evidence conflicts with Flowtrac stock/bin status, suggesting Flowtrac may be stale.');

  const riskSignals = [];
  if(serialMismatch) riskSignals.push('Serial mismatch could indicate scanner error, wrong device, or record-mapping issue.');
  if(deployedButFlowtracStock) riskSignals.push('Flowtrac still shows stock/spare while deployment evidence shows a room/rack/U location.');
  if(!c.technicianTicket || !c.binTransportTicket) riskSignals.push('Missing technician/bin transportation ticket means the normal update trigger may be absent.');
  if(!c.physicalAudit) riskSignals.push('No physical audit confirmation yet, so final location should not be written as certain.');

  const checks = [
    c.receivingSheet,
    c.warehouseScan,
    c.flowtracExists,
    !serialMismatch,
    c.deploymentEvidence,
    c.technicianTicket,
    c.binTransportTicket,
    c.apSourceMatch,
    c.lansweeperMatch,
    c.physicalAudit
  ];
  const readiness = Math.round((checks.filter(Boolean).length / checks.length) * 100);
  let risk = 'Medium';
  let riskScore = 55;
  let finding = 'Possible stale Flowtrac location';
  if(serialMismatch){ risk='High'; riskScore=86; finding='Serial mismatch / identity review needed'; }
  else if(deployedButFlowtracStock && (!c.binTransportTicket || !c.physicalAudit)){ risk='High'; riskScore=78; finding='Likely stale Flowtrac bin; evidence incomplete'; }
  else if(readiness >= 80){ risk='Low'; riskScore=25; finding='Ready for Flowtrac update review'; }

  const doNotConclude = [
    'Do not conclude Flowtrac is wrong without supporting source or physical evidence.',
    'Do not conclude the device is still in stock only because Flowtrac bin says stock/spare.',
    'Do not update rack/U as final if physical audit or trusted deployment evidence is missing.',
    'Do not treat a serial mismatch as a simple typo until scanner, vendor, and Flowtrac records are reviewed.',
    'Do not blame the technician automatically; missing ticket means the process evidence is incomplete, not proof of fault.'
  ];

  let recommendation = 'Route to DCL Inventory Review and request missing bin/deployment evidence before final Flowtrac update.';
  if(serialMismatch) recommendation = 'Route to Serial Identity Review before any location update.';
  if(risk === 'Low') recommendation = 'Evidence is strong enough for DCL to review and update Flowtrac bin/rack/U.';

  return { known, missing, supportPoints, riskSignals, readiness, risk, riskScore, finding, doNotConclude, recommendation, deployedButFlowtracStock, serialMismatch };
}

function receipt(){
  const c = state.case;
  const r = calc(c);
  return {
    receipt_id: `${c.caseId}-${Date.now()}`,
    generated_at: new Date().toISOString(),
    product_boundary: 'Evidence routing and inventory workpaper control only. Synthetic UFIT-inspired scenario. Not real UF data.',
    case: {
      case_id: c.caseId,
      scenario: c.scenario,
      asset_type: c.assetType,
      model: c.model,
      asset_tag: c.assetTag,
      vendor_scan_serial: c.serialVendor,
      flowtrac_serial: c.serialFlowtrac,
      flowtrac_bin: c.flowtracBin,
      observed_location: `${c.observedBuilding} ${c.observedRoom} ${c.observedRack} ${c.observedU}`,
      date_received: c.dateReceived,
      date_deployed: c.dateDeployed
    },
    readiness: { evidence_readiness_score: r.readiness, finding: r.finding, risk: r.risk, risk_score: r.riskScore, recommendation: r.recommendation },
    known_evidence: r.known,
    support_points: r.supportPoints,
    risk_signals: r.riskSignals,
    missing_evidence: r.missing,
    do_not_conclude: r.doNotConclude,
    reviewer: { decision: c.reviewerDecision, notes: c.reviewerNotes }
  };
}

function download(filename, data, mime='application/json'){
  const blob = new Blob([mime === 'application/json' ? JSON.stringify(data, null, 2) : data], {type:mime});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; a.click(); URL.revokeObjectURL(url);
}

function setTab(tab){ activeTab = tab; render(); }
function resetDemo(){ state = { case: { ...defaultCase } }; saveState(); render(); }

function updateFromForm(){
  const c = state.case;
  c.assetType = str('assetType'); c.model = str('model'); c.assetTag = str('assetTag');
  c.serialVendor = str('serialVendor'); c.serialFlowtrac = str('serialFlowtrac');
  c.purchaseTicket = str('purchaseTicket'); c.quoteStatus = str('quoteStatus');
  c.flowtracBin = str('flowtracBin'); c.flowtracRack = str('flowtracRack'); c.flowtracU = str('flowtracU');
  c.observedBuilding = str('observedBuilding'); c.observedRoom = str('observedRoom'); c.observedRack = str('observedRack'); c.observedU = str('observedU');
  c.dateReceived = str('dateReceived'); c.dateDeployed = str('dateDeployed'); c.notes = str('notes');
  c.receivingSheet = bool('receivingSheet'); c.flowtracExists = bool('flowtracExists'); c.warehouseScan = bool('warehouseScan');
  c.deploymentEvidence = bool('deploymentEvidence'); c.technicianTicket = bool('technicianTicket'); c.binTransportTicket = bool('binTransportTicket');
  c.apSourceMatch = bool('apSourceMatch'); c.lansweeperMatch = bool('lansweeperMatch'); c.physicalAudit = bool('physicalAudit');
  saveState(); render();
}
function saveReviewer(){ state.case.reviewerDecision = str('reviewerDecision'); state.case.reviewerNotes = str('reviewerNotes'); saveState(); render(); }
function evidenceCheckbox(id, label, checked){ return `<label class="check"><input id="${id}" type="checkbox" ${checked ? 'checked' : ''} onchange="updateFromForm()"/> <span>${label}</span></label>`; }
function missingTable(items){ return items.length ? `<table><thead><tr><th>Owner</th><th>Missing evidence</th><th>Why it matters</th></tr></thead><tbody>${items.map(x=>`<tr><td>${x.owner}</td><td><b>${x.item}</b></td><td>${x.reason}</td></tr>`).join('')}</tbody></table>` : '<div class="empty">No missing evidence flagged.</div>'; }

function renderOverview(c, r){
  return `
    <section class="panel heroPanel">
      <div>
        <span class="eyebrow">UFIT-inspired narrow scenario · Synthetic data only</span>
        <h2>${r.finding}</h2>
        <p>This scenario is based on your UFIT experience: device receiving, Flowtrac inventory, warehouse scan records, deployment evidence, bin transportation tickets, and physical/rack/U audit.</p>
        <div class="heroActions"><button onclick="setTab('intake')">Edit asset evidence</button><button class="secondary" onclick="download('ufit_asset_evidence_receipt.json', receipt())">Export evidence receipt</button></div>
      </div>
      <div class="caseCard"><b>${c.caseId}</b><span>${c.assetType}</span><div class="bigNumber">${r.readiness}%</div><small>Evidence readiness</small></div>
    </section>
    <div class="metrics">
      <div class="metric"><span>Risk</span><b>${r.risk}</b><small>Score ${r.riskScore}</small></div>
      <div class="metric"><span>Flowtrac bin</span><b>${c.flowtracBin || 'Missing'}</b><small>Current system record</small></div>
      <div class="metric"><span>Observed room</span><b>${c.observedRoom || 'Unknown'}</b><small>${c.observedBuilding}</small></div>
      <div class="metric"><span>Rack/U</span><b>${c.observedRack} ${c.observedU}</b><small>Observed evidence</small></div>
      <div class="metric"><span>Serial match</span><b>${r.serialMismatch ? 'No' : 'Yes'}</b><small>Vendor vs Flowtrac</small></div>
    </div>
    <section class="panel"><div class="split"><div><h3>Recommended next action</h3><p class="finding ${r.risk.toLowerCase()}">${r.recommendation}</p><h3>Support points</h3>${list(r.supportPoints)}</div><div><h3>Risk signals</h3>${list(r.riskSignals)}<h3>Product boundary</h3><div class="boundary">This demo does not use real UF data. It shows how CGIF could structure an inventory evidence review workflow.</div></div></div></section>
  `;
}

function renderIntake(c){
  return `
    <section class="panel">
      <div class="panelHead"><div><span class="eyebrow">Asset evidence intake</span><h2>Device lifecycle facts</h2></div><button class="secondary" onclick="resetDemo()">Reset demo</button></div>
      <div class="formGrid">
        <label>Asset type<input id="assetType" value="${c.assetType}" onchange="updateFromForm()"/></label>
        <label>Model<input id="model" value="${c.model}" onchange="updateFromForm()"/></label>
        <label>Asset tag<input id="assetTag" value="${c.assetTag}" onchange="updateFromForm()"/></label>
        <label>Vendor/scan serial<input id="serialVendor" value="${c.serialVendor}" onchange="updateFromForm()"/></label>
        <label>Flowtrac serial<input id="serialFlowtrac" value="${c.serialFlowtrac}" onchange="updateFromForm()"/></label>
        <label>Request / quote ticket<input id="purchaseTicket" value="${c.purchaseTicket}" onchange="updateFromForm()"/></label>
        <label>Quote status<input id="quoteStatus" value="${c.quoteStatus}" onchange="updateFromForm()"/></label>
        <label>Flowtrac bin<input id="flowtracBin" value="${c.flowtracBin}" onchange="updateFromForm()"/></label>
        <label>Flowtrac rack<input id="flowtracRack" value="${c.flowtracRack}" onchange="updateFromForm()"/></label>
        <label>Flowtrac U<input id="flowtracU" value="${c.flowtracU}" onchange="updateFromForm()"/></label>
        <label>Observed building<input id="observedBuilding" value="${c.observedBuilding}" onchange="updateFromForm()"/></label>
        <label>Observed room<input id="observedRoom" value="${c.observedRoom}" onchange="updateFromForm()"/></label>
        <label>Observed rack<input id="observedRack" value="${c.observedRack}" onchange="updateFromForm()"/></label>
        <label>Observed U<input id="observedU" value="${c.observedU}" onchange="updateFromForm()"/></label>
        <label>Date received<input id="dateReceived" type="date" value="${c.dateReceived}" onchange="updateFromForm()"/></label>
        <label>Date deployed<input id="dateDeployed" type="date" value="${c.dateDeployed}" onchange="updateFromForm()"/></label>
      </div>
      <label class="wideLabel">Notes<textarea id="notes" onchange="updateFromForm()">${c.notes}</textarea></label>
      <h3>Evidence checklist</h3>
      <div class="checkGrid">
        ${evidenceCheckbox('receivingSheet','Receiving sheet / scan spreadsheet available',c.receivingSheet)}
        ${evidenceCheckbox('warehouseScan','Warehouse scan captured serial',c.warehouseScan)}
        ${evidenceCheckbox('flowtracExists','Flowtrac record exists',c.flowtracExists)}
        ${evidenceCheckbox('deploymentEvidence','Deployment evidence observed',c.deploymentEvidence)}
        ${evidenceCheckbox('technicianTicket','Technician deployment ticket exists',c.technicianTicket)}
        ${evidenceCheckbox('binTransportTicket','Bin transportation ticket exists',c.binTransportTicket)}
        ${evidenceCheckbox('apSourceMatch','AP source confirms serial/location',c.apSourceMatch)}
        ${evidenceCheckbox('lansweeperMatch','Lansweeper confirms serial/device identity',c.lansweeperMatch)}
        ${evidenceCheckbox('physicalAudit','Physical audit confirms rack/U',c.physicalAudit)}
      </div>
    </section>
  `;
}

function renderEvidence(c,r){ return `<section class="panel"><span class="eyebrow">Evidence review</span><h2>What is known</h2>${list(r.known)}</section><section class="panel"><span class="eyebrow">Missing support</span><h2>Owner requests</h2>${missingTable(r.missing)}</section>`; }
function renderGuardrails(r){ return `<section class="panel"><span class="eyebrow">Evidence boundary</span><h2>Do not conclude</h2><p>These guardrails prevent the tool from overclaiming what the evidence can prove.</p>${list(r.doNotConclude)}</section><section class="panel"><span class="eyebrow">Routing</span><h2>Who should review next?</h2><div class="routeBox"><div>${pill('Primary reviewer','blue')} <b>DCL Inventory Review</b><span>Review Flowtrac record, serial match, and whether bin/rack/U should be updated.</span></div><div>${pill('Evidence owner','purple')} <b>Technician / Warehouse / Network source owner</b><span>Confirm deployment ticket, scan record, AP source, and Lansweeper evidence.</span></div><div>${pill('Final check','neutral')} <b>Physical Audit</b><span>Confirm actual room/rack/U before final close if evidence is incomplete.</span></div></div></section>`; }
function renderReceipt(c,r){ return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">Audit-ready output</span><h2>Evidence receipt</h2></div><button onclick="download('ufit_asset_evidence_receipt.json', receipt())">Export JSON</button></div><p>This receipt shows what CGIF would preserve: facts, source evidence, missing evidence, guardrails, and next owner.</p><pre>${JSON.stringify(receipt(), null, 2)}</pre></section><section class="panel"><span class="eyebrow">Reviewer note</span><h2>Internal review update</h2><div class="formGrid two"><label>Decision status<select id="reviewerDecision"><option ${c.reviewerDecision === 'Open' ? 'selected' : ''}>Open</option><option ${c.reviewerDecision === 'Needs documents' ? 'selected' : ''}>Needs documents</option><option ${c.reviewerDecision === 'Ready for Flowtrac update' ? 'selected' : ''}>Ready for Flowtrac update</option><option ${c.reviewerDecision === 'Closed' ? 'selected' : ''}>Closed</option></select></label><label>Reviewer notes<textarea id="reviewerNotes">${c.reviewerNotes}</textarea></label></div><button onclick="saveReviewer()">Save reviewer update</button></section>`; }

function render(){
  const c = state.case; const r = calc(c);
  const tabs = [['overview','Overview'],['intake','Asset Intake'],['evidence','Evidence & Missing Docs'],['guardrails','Guardrails & Routing'],['receipt','Evidence Receipt']];
  let body = activeTab === 'overview' ? renderOverview(c,r) : activeTab === 'intake' ? renderIntake(c) : activeTab === 'evidence' ? renderEvidence(c,r) : activeTab === 'guardrails' ? renderGuardrails(r) : renderReceipt(c,r);
  document.getElementById('app').innerHTML = `<aside><div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>UFIT Asset Scenario</span></div></div><nav>${tabs.map(([id,label])=>`<button class="${activeTab===id?'active':''}" onclick="setTab('${id}')">${label}</button>`).join('')}</nav><div class="sideNote"><b>Synthetic data only</b><span>Do not upload or enter real UFIT asset records. This is a public GitHub Pages demo.</span></div></aside><main><header><div><span class="eyebrow">CGIF · UFIT-inspired scenario</span><h1>Asset Location Evidence Readiness</h1><p>Turn receiving, scan, Flowtrac, AP/Lansweeper, ticket, and physical audit evidence into a structured review case.</p></div><div class="headerPills">${pill(r.risk + ' risk', riskTone(r.risk))}${pill(r.readiness + '% ready','blue')}</div></header>${body}</main>`;
}

window.setTab=setTab; window.updateFromForm=updateFromForm; window.resetDemo=resetDemo; window.download=download; window.receipt=receipt; window.saveReviewer=saveReviewer;
render();
