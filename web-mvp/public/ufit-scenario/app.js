const STORAGE_KEY = 'cgif-ufit-asset-scenario-v2';

const defaultCase = {
  caseId: 'UFIT-ASSET-001',
  scenario: 'Cross-system asset evidence reconciliation',
  assetType: 'Wireless access point',
  model: 'Cisco Catalyst AP - synthetic',
  assetTag: 'UF-SYN-230B-018',
  purchaseTicket: 'REQ-2026-SYN-104',
  quoteStatus: 'Three vendor quotes requested and attached',

  vendorSerial: 'SYNAP230B018',
  apSerial: 'SYNAP230B018',
  lansweeperSerial: 'SYNAP230B018',
  flowtracSerial: 'YNAP230B018',

  flowtracDns: '',
  apDns: 'ssrb-ap-230b-018.ufl.edu',
  lansweeperDns: 'ssrb-ap-230b-018.ufl.edu',
  flowtracIp: '',
  apIp: '10.24.18.55',
  lansweeperIp: '10.24.18.55',
  flowtracMac: '',
  apMac: 'AA:BB:CC:11:22:33',
  lansweeperMac: 'AA:BB:CC:11:22:33',

  receivingSheet: true,
  warehouseScan: true,
  flowtracExists: true,
  flowtracBin: 'SSRB Stock',
  flowtracRack: '',
  flowtracU: '',
  deploymentEvidence: true,
  technicianTicket: false,
  binTransportTicket: false,
  physicalAudit: false,
  observedBuilding: 'SSRB',
  observedRoom: '230B',
  observedRack: 'TR02',
  observedU: 'U18',
  apSourceAvailable: true,
  lansweeperAvailable: true,
  dateReceived: '2026-05-20',
  dateDeployed: '2026-06-05',
  notes: 'Synthetic case based on your UFIT work: AP/Lansweeper exports provide DNS/IP/MAC evidence, while Flowtrac has missing technical fields and may still show the asset in stock because the bin transportation ticket is missing.',
  reviewerDecision: 'Open',
  reviewerNotes: ''
};

let state = loadState();
let activeTab = 'overview';

function loadState(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || { case: {...defaultCase} }; }
  catch { return { case: {...defaultCase} }; }
}
function saveState(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
function str(id){ return document.getElementById(id).value; }
function bool(id){ return document.getElementById(id).checked; }
function pill(text, tone='neutral'){ return `<span class="pill ${tone}">${text}</span>`; }
function riskTone(r){ return r === 'High' ? 'danger' : r === 'Medium' ? 'warn' : 'success'; }
function list(items){ return items.length ? `<ul>${items.map(x=>`<li>${x}</li>`).join('')}</ul>` : '<div class="empty">No items flagged.</div>'; }
function clean(v){ return String(v || '').trim().toUpperCase().replace(/\s+/g,''); }
function stripLeadingS(v){ const x = clean(v); return x.startsWith('S') ? x.slice(1) : x; }
function same(a,b){ return clean(a) && clean(a) === clean(b); }
function blank(v){ return !String(v || '').trim(); }

function serialMatchType(c){
  const ap = clean(c.apSerial || c.vendorSerial || c.lansweeperSerial);
  const ft = clean(c.flowtracSerial);
  if(!ft) return 'Not Found in Flowtrac';
  if(ap && ap === ft) return 'Exact Match';
  if(ap && stripLeadingS(ap) === stripLeadingS(ft)) return 'Leading S Match';
  return 'Serial Conflict';
}

function fieldCandidate(label, flowtracValue, apValue, lansweeperValue, matchType){
  const ap = String(apValue || '').trim();
  const ls = String(lansweeperValue || '').trim();
  const ft = String(flowtracValue || '').trim();
  let candidate = '';
  let confidence = 'Low';
  let status = 'No update candidate';
  let reason = '';

  if(!['Exact Match','Leading S Match'].includes(matchType)){
    return { label, flowtracValue: ft, apValue: ap, lansweeperValue: ls, candidate:'', confidence:'Blocked', status:'Blocked', reason:'Serial identity is not safe enough for technical field update.' };
  }

  if(ap && ls && clean(ap) === clean(ls)){
    candidate = ap;
    confidence = 'High';
    status = ft && clean(ft) === clean(candidate) ? 'Already aligned' : 'Ready to update';
    reason = 'AP and Lansweeper agree on the same value.';
  } else if(ap || ls){
    candidate = ap || ls;
    confidence = 'Medium';
    status = ft && clean(ft) === clean(candidate) ? 'Already aligned' : 'Review before update';
    reason = 'Only one technical source is available or sources do not fully agree.';
  } else {
    reason = 'No AP/Lansweeper value available.';
  }

  return { label, flowtracValue: ft, apValue: ap, lansweeperValue: ls, candidate, confidence, status, reason };
}

function calc(c){
  const matchType = serialMatchType(c);
  const technicalFields = [
    fieldCandidate('DNS', c.flowtracDns, c.apDns, c.lansweeperDns, matchType),
    fieldCandidate('IP', c.flowtracIp, c.apIp, c.lansweeperIp, matchType),
    fieldCandidate('MAC', c.flowtracMac, c.apMac, c.lansweeperMac, matchType)
  ];
  const readyFields = technicalFields.filter(f => f.status === 'Ready to update').length;
  const reviewFields = technicalFields.filter(f => f.status === 'Review before update').length;
  const blockedFields = technicalFields.filter(f => f.status === 'Blocked').length;

  const flowtracLooksStock = String(c.flowtracBin).toLowerCase().includes('stock') || String(c.flowtracBin).toLowerCase().includes('warehouse') || String(c.flowtracBin).toLowerCase().includes('spare');
  const hasObservedLocation = Boolean(c.observedBuilding && c.observedRoom && c.observedRack && c.observedU);
  const deployedButFlowtracStock = c.deploymentEvidence && hasObservedLocation && flowtracLooksStock;

  const known = [];
  if(c.receivingSheet) known.push(`Receiving sheet shows ${c.model} was received for purchase/request ${c.purchaseTicket}.`);
  if(c.warehouseScan) known.push(`Warehouse scan / receiving spreadsheet captured vendor/scan serial ${c.vendorSerial}.`);
  if(c.flowtracExists) known.push(`Flowtrac record exists for serial ${c.flowtracSerial}.`);
  if(c.apSourceAvailable) known.push(`AP export provides serial ${c.apSerial}, DNS ${c.apDns}, IP ${c.apIp}, MAC ${c.apMac}.`);
  if(c.lansweeperAvailable) known.push(`Lansweeper provides serial ${c.lansweeperSerial}, DNS ${c.lansweeperDns}, IP ${c.lansweeperIp}, MAC ${c.lansweeperMac}.`);
  known.push(`Serial comparison result: ${matchType}.`);
  if(c.deploymentEvidence) known.push(`Deployment evidence suggests installed location: ${c.observedBuilding} ${c.observedRoom}, ${c.observedRack} ${c.observedU}.`);
  if(c.physicalAudit) known.push('Physical audit confirms the observed room/rack/U location.');

  const missing = [];
  if(!c.receivingSheet) missing.push({ owner:'Warehouse / DCL', item:'Receiving spreadsheet or scan record', reason:'Need proof that the asset entered inventory.' });
  if(!c.flowtracExists) missing.push({ owner:'DCL Inventory', item:'Flowtrac asset record', reason:'Flowtrac is the working inventory system and needs a record to update.' });
  if(matchType === 'Serial Conflict') missing.push({ owner:'DCL Inventory', item:'Serial identity review', reason:'AP/vendor/Lansweeper serial does not safely match Flowtrac serial.' });
  if(matchType === 'Leading S Match') missing.push({ owner:'DCL Inventory', item:'Leading S match review', reason:'Likely same device, but serial format difference should be documented before serial overwrite.' });
  if(!c.apSourceAvailable) missing.push({ owner:'Network / AP Source Owner', item:'AP export', reason:'Need AP source for wireless technical fields such as DNS/IP/MAC.' });
  if(!c.lansweeperAvailable) missing.push({ owner:'Lansweeper / IT Discovery Owner', item:'Lansweeper export', reason:'Need second technical source to validate DNS/IP/MAC values.' });
  if(!c.technicianTicket) missing.push({ owner:'Technician / Deployment Team', item:'Deployment or bin transportation ticket', reason:'Physical movement may have happened without the ticket that normally triggers bin update.' });
  if(!c.binTransportTicket) missing.push({ owner:'DCL / Technician', item:'Bin transportation confirmation', reason:'Flowtrac bin may stay stale if bin change ticket was not submitted.' });
  if(!c.physicalAudit) missing.push({ owner:'DCL Student Ops / Inventory Audit', item:'Physical room/rack/U verification', reason:'Need final evidence before changing Flowtrac location with confidence.' });
  technicalFields.filter(f => f.status === 'Review before update').forEach(f => missing.push({ owner:'DCL Inventory / Source Owner', item:`${f.label} source agreement review`, reason:f.reason }));

  const supportPoints = [];
  if(matchType === 'Exact Match') supportPoints.push('Serial is an exact match, so DNS/IP/MAC updates can be considered if source evidence supports them.');
  if(matchType === 'Leading S Match') supportPoints.push('Serial differs only by leading S, matching the Excel audit pattern you used before; candidate update is possible but should be documented.');
  if(readyFields > 0) supportPoints.push(`${readyFields} technical field(s) are ready to update because AP and Lansweeper agree.`);
  if(c.receivingSheet && c.warehouseScan) supportPoints.push('Receiving and warehouse scan evidence support that the asset entered inventory before deployment.');
  if(deployedButFlowtracStock) supportPoints.push('Deployment evidence conflicts with Flowtrac stock/bin status, suggesting Flowtrac may be stale.');

  const riskSignals = [];
  if(matchType === 'Serial Conflict') riskSignals.push('Serial conflict could mean scanner error, wrong device, duplicate record, or incorrect mapping.');
  if(matchType === 'Not Found in Flowtrac') riskSignals.push('Asset appears in technical source but not Flowtrac, so creating/updating Flowtrac requires review.');
  if(reviewFields > 0) riskSignals.push(`${reviewFields} technical field(s) need source agreement review before update.`);
  if(blockedFields > 0) riskSignals.push('Technical field updates are blocked until serial identity is resolved.');
  if(deployedButFlowtracStock) riskSignals.push('Flowtrac still shows stock/spare while deployment evidence shows a room/rack/U location.');
  if(!c.technicianTicket || !c.binTransportTicket) riskSignals.push('Missing technician/bin transportation ticket means the normal update trigger may be absent.');
  if(!c.physicalAudit) riskSignals.push('No physical audit confirmation yet, so final location should not be written as certain.');

  const checks = [
    c.receivingSheet,
    c.warehouseScan,
    c.flowtracExists,
    ['Exact Match','Leading S Match'].includes(matchType),
    readyFields >= 2,
    c.deploymentEvidence,
    c.technicianTicket,
    c.binTransportTicket,
    c.apSourceAvailable,
    c.lansweeperAvailable,
    c.physicalAudit
  ];
  const readiness = Math.round((checks.filter(Boolean).length / checks.length) * 100);

  let risk = 'Medium';
  let riskScore = 55;
  let finding = 'Cross-system reconciliation needed';
  if(matchType === 'Serial Conflict' || matchType === 'Not Found in Flowtrac') { risk='High'; riskScore=88; finding='Serial identity review needed'; }
  else if(deployedButFlowtracStock && (!c.binTransportTicket || !c.physicalAudit)) { risk='High'; riskScore=80; finding='Likely stale Flowtrac bin; evidence incomplete'; }
  else if(readyFields > 0 && readiness >= 70) { risk='Medium'; riskScore=48; finding='Technical fields ready for Flowtrac update review'; }
  if(readiness >= 85 && riskSignals.length <= 1){ risk='Low'; riskScore=24; finding='Ready for Flowtrac update review'; }

  const doNotConclude = [
    'Do not create a new Flowtrac asset just because AP serial has a leading S difference.',
    'Do not overwrite the Flowtrac serial automatically; document Exact Match or Leading S Match first.',
    'Do not update DNS/IP/MAC unless serial identity is Exact Match or Leading S Match and source evidence supports it.',
    'Do not update rack/U from DNS/IP/MAC alone; physical/deployment evidence is needed for location.',
    'Do not conclude Flowtrac is wrong without supporting source or physical evidence.',
    'Do not blame the technician automatically; missing ticket means the process evidence is incomplete, not proof of fault.'
  ];

  let recommendation = 'Route to DCL Inventory Review and request missing source evidence before Flowtrac update.';
  if(matchType === 'Serial Conflict' || matchType === 'Not Found in Flowtrac') recommendation = 'Resolve serial identity before updating DNS/IP/MAC or location.';
  else if(readyFields > 0 && deployedButFlowtracStock) recommendation = 'DNS/IP/MAC can be reviewed for update, but bin/rack/U still needs ticket or physical audit evidence.';
  else if(readyFields > 0) recommendation = 'Prepare Flowtrac DNS/IP/MAC update candidate list for DCL review.';
  if(risk === 'Low') recommendation = 'Evidence is strong enough for DCL to review and update Flowtrac technical fields and location.';

  return { matchType, technicalFields, readyFields, reviewFields, blockedFields, deployedButFlowtracStock, known, missing, supportPoints, riskSignals, readiness, risk, riskScore, finding, doNotConclude, recommendation };
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
      vendor_scan_serial: c.vendorSerial,
      ap_serial: c.apSerial,
      lansweeper_serial: c.lansweeperSerial,
      flowtrac_serial: c.flowtracSerial,
      serial_match_type: r.matchType,
      flowtrac_bin: c.flowtracBin,
      observed_location: `${c.observedBuilding} ${c.observedRoom} ${c.observedRack} ${c.observedU}`,
      date_received: c.dateReceived,
      date_deployed: c.dateDeployed
    },
    technical_field_candidates: r.technicalFields,
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
function resetDemo(){ state = { case: {...defaultCase} }; saveState(); render(); }
function updateFromForm(){
  const c = state.case;
  c.assetType=str('assetType'); c.model=str('model'); c.assetTag=str('assetTag');
  c.vendorSerial=str('vendorSerial'); c.apSerial=str('apSerial'); c.lansweeperSerial=str('lansweeperSerial'); c.flowtracSerial=str('flowtracSerial');
  c.purchaseTicket=str('purchaseTicket'); c.quoteStatus=str('quoteStatus');
  c.flowtracDns=str('flowtracDns'); c.apDns=str('apDns'); c.lansweeperDns=str('lansweeperDns');
  c.flowtracIp=str('flowtracIp'); c.apIp=str('apIp'); c.lansweeperIp=str('lansweeperIp');
  c.flowtracMac=str('flowtracMac'); c.apMac=str('apMac'); c.lansweeperMac=str('lansweeperMac');
  c.flowtracBin=str('flowtracBin'); c.flowtracRack=str('flowtracRack'); c.flowtracU=str('flowtracU');
  c.observedBuilding=str('observedBuilding'); c.observedRoom=str('observedRoom'); c.observedRack=str('observedRack'); c.observedU=str('observedU');
  c.dateReceived=str('dateReceived'); c.dateDeployed=str('dateDeployed'); c.notes=str('notes');
  c.receivingSheet=bool('receivingSheet'); c.warehouseScan=bool('warehouseScan'); c.flowtracExists=bool('flowtracExists');
  c.deploymentEvidence=bool('deploymentEvidence'); c.technicianTicket=bool('technicianTicket'); c.binTransportTicket=bool('binTransportTicket'); c.physicalAudit=bool('physicalAudit');
  c.apSourceAvailable=bool('apSourceAvailable'); c.lansweeperAvailable=bool('lansweeperAvailable');
  saveState(); render();
}
function saveReviewer(){ state.case.reviewerDecision=str('reviewerDecision'); state.case.reviewerNotes=str('reviewerNotes'); saveState(); render(); }
function evidenceCheckbox(id,label,checked){ return `<label class="check"><input id="${id}" type="checkbox" ${checked?'checked':''} onchange="updateFromForm()"/> <span>${label}</span></label>`; }
function missingTable(items){ return items.length ? `<table><thead><tr><th>Owner</th><th>Missing evidence</th><th>Why it matters</th></tr></thead><tbody>${items.map(x=>`<tr><td>${x.owner}</td><td><b>${x.item}</b></td><td>${x.reason}</td></tr>`).join('')}</tbody></table>` : '<div class="empty">No missing evidence flagged.</div>'; }
function techTable(fields){ return `<table><thead><tr><th>Field</th><th>Flowtrac</th><th>AP source</th><th>Lansweeper</th><th>Candidate</th><th>Status</th></tr></thead><tbody>${fields.map(f=>`<tr><td><b>${f.label}</b></td><td>${f.flowtracValue || '<span class="muted">blank</span>'}</td><td>${f.apValue || '<span class="muted">blank</span>'}</td><td>${f.lansweeperValue || '<span class="muted">blank</span>'}</td><td>${f.candidate || '-'}</td><td>${pill(f.status, f.status==='Ready to update'?'success':f.status==='Blocked'?'danger':f.status==='Review before update'?'warn':'neutral')}<br/><small>${f.reason}</small></td></tr>`).join('')}</tbody></table>`; }

function renderOverview(c,r){
  return `<section class="panel heroPanel"><div><span class="eyebrow">UFIT-inspired scenario · Synthetic data only</span><h2>${r.finding}</h2><p>This updated scenario now includes the Excel-formula audit pattern you used before: comparing AP and Lansweeper DNS/IP/MAC against Flowtrac, classifying Exact Match / Leading S Match / Not Found, and deciding what can be updated.</p><div class="heroActions"><button onclick="setTab('technical')">Open DNS/IP/MAC reconciliation</button><button class="secondary" onclick="download('ufit_asset_evidence_receipt.json', receipt())">Export evidence receipt</button></div></div><div class="caseCard"><b>${c.caseId}</b><span>${c.assetType}</span><div class="bigNumber">${r.matchType}</div><small>Serial match type</small></div></section>
  <div class="metrics"><div class="metric"><span>Evidence readiness</span><b>${r.readiness}%</b><small>Cross-source support</small></div><div class="metric"><span>Risk</span><b>${r.risk}</b><small>Score ${r.riskScore}</small></div><div class="metric"><span>DNS/IP/MAC ready</span><b>${r.readyFields}</b><small>Fields ready to update</small></div><div class="metric"><span>Flowtrac bin</span><b>${c.flowtracBin || 'Missing'}</b><small>Current system record</small></div><div class="metric"><span>Observed location</span><b>${c.observedRoom} ${c.observedRack} ${c.observedU}</b><small>${c.observedBuilding}</small></div></div>
  <section class="panel"><div class="split"><div><h3>Recommended next action</h3><p class="finding ${r.risk.toLowerCase()}">${r.recommendation}</p><h3>Support points</h3>${list(r.supportPoints)}</div><div><h3>Risk signals</h3>${list(r.riskSignals)}<h3>Product boundary</h3><div class="boundary">Do not upload real UFIT data. This public demo uses synthetic records to show the workflow pattern.</div></div></div></section>`;
}

function renderIntake(c){
  return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">Asset intake</span><h2>Device identity and location facts</h2></div><button class="secondary" onclick="resetDemo()">Reset demo</button></div><div class="formGrid">
  <label>Asset type<input id="assetType" value="${c.assetType}" onchange="updateFromForm()"/></label><label>Model<input id="model" value="${c.model}" onchange="updateFromForm()"/></label><label>Asset tag<input id="assetTag" value="${c.assetTag}" onchange="updateFromForm()"/></label>
  <label>Vendor/scan serial<input id="vendorSerial" value="${c.vendorSerial}" onchange="updateFromForm()"/></label><label>AP serial<input id="apSerial" value="${c.apSerial}" onchange="updateFromForm()"/></label><label>Lansweeper serial<input id="lansweeperSerial" value="${c.lansweeperSerial}" onchange="updateFromForm()"/></label><label>Flowtrac serial<input id="flowtracSerial" value="${c.flowtracSerial}" onchange="updateFromForm()"/></label>
  <label>Request / quote ticket<input id="purchaseTicket" value="${c.purchaseTicket}" onchange="updateFromForm()"/></label><label>Quote status<input id="quoteStatus" value="${c.quoteStatus}" onchange="updateFromForm()"/></label>
  <label>Flowtrac bin<input id="flowtracBin" value="${c.flowtracBin}" onchange="updateFromForm()"/></label><label>Flowtrac rack<input id="flowtracRack" value="${c.flowtracRack}" onchange="updateFromForm()"/></label><label>Flowtrac U<input id="flowtracU" value="${c.flowtracU}" onchange="updateFromForm()"/></label>
  <label>Observed building<input id="observedBuilding" value="${c.observedBuilding}" onchange="updateFromForm()"/></label><label>Observed room<input id="observedRoom" value="${c.observedRoom}" onchange="updateFromForm()"/></label><label>Observed rack<input id="observedRack" value="${c.observedRack}" onchange="updateFromForm()"/></label><label>Observed U<input id="observedU" value="${c.observedU}" onchange="updateFromForm()"/></label>
  <label>Date received<input id="dateReceived" type="date" value="${c.dateReceived}" onchange="updateFromForm()"/></label><label>Date deployed<input id="dateDeployed" type="date" value="${c.dateDeployed}" onchange="updateFromForm()"/></label>
  </div><label class="wideLabel">Notes<textarea id="notes" onchange="updateFromForm()">${c.notes}</textarea></label><h3>Evidence checklist</h3><div class="checkGrid">${evidenceCheckbox('receivingSheet','Receiving sheet / scan spreadsheet available',c.receivingSheet)}${evidenceCheckbox('warehouseScan','Warehouse scan captured serial',c.warehouseScan)}${evidenceCheckbox('flowtracExists','Flowtrac record exists',c.flowtracExists)}${evidenceCheckbox('apSourceAvailable','AP source export available',c.apSourceAvailable)}${evidenceCheckbox('lansweeperAvailable','Lansweeper export available',c.lansweeperAvailable)}${evidenceCheckbox('deploymentEvidence','Deployment evidence observed',c.deploymentEvidence)}${evidenceCheckbox('technicianTicket','Technician deployment ticket exists',c.technicianTicket)}${evidenceCheckbox('binTransportTicket','Bin transportation ticket exists',c.binTransportTicket)}${evidenceCheckbox('physicalAudit','Physical audit confirms rack/U',c.physicalAudit)}</div></section>`;
}

function renderTechnical(c,r){
  return `<section class="panel"><span class="eyebrow">Technical identity reconciliation</span><h2>AP + Lansweeper vs Flowtrac</h2><p>This is the workflow you used Excel formulas for: normalize serials, classify match type, then compare DNS/IP/MAC update candidates.</p><div class="metrics"><div class="metric"><span>Match type</span><b>${r.matchType}</b><small>Serial comparison</small></div><div class="metric"><span>Ready fields</span><b>${r.readyFields}</b><small>AP and Lansweeper agree</small></div><div class="metric"><span>Review fields</span><b>${r.reviewFields}</b><small>Source conflict / one source only</small></div><div class="metric"><span>Blocked fields</span><b>${r.blockedFields}</b><small>Serial unsafe</small></div></div>${techTable(r.technicalFields)}</section>
  <section class="panel"><span class="eyebrow">Edit technical fields</span><h2>DNS / IP / MAC source values</h2><div class="formGrid"><label>Flowtrac DNS<input id="flowtracDns" value="${c.flowtracDns}" onchange="updateFromForm()"/></label><label>AP DNS<input id="apDns" value="${c.apDns}" onchange="updateFromForm()"/></label><label>Lansweeper DNS<input id="lansweeperDns" value="${c.lansweeperDns}" onchange="updateFromForm()"/></label><label>Flowtrac IP<input id="flowtracIp" value="${c.flowtracIp}" onchange="updateFromForm()"/></label><label>AP IP<input id="apIp" value="${c.apIp}" onchange="updateFromForm()"/></label><label>Lansweeper IP<input id="lansweeperIp" value="${c.lansweeperIp}" onchange="updateFromForm()"/></label><label>Flowtrac MAC<input id="flowtracMac" value="${c.flowtracMac}" onchange="updateFromForm()"/></label><label>AP MAC<input id="apMac" value="${c.apMac}" onchange="updateFromForm()"/></label><label>Lansweeper MAC<input id="lansweeperMac" value="${c.lansweeperMac}" onchange="updateFromForm()"/></label></div></section>`;
}

function renderEvidence(c,r){ return `<section class="panel"><span class="eyebrow">Evidence review</span><h2>What is known</h2>${list(r.known)}</section><section class="panel"><span class="eyebrow">Missing support</span><h2>Owner requests</h2>${missingTable(r.missing)}</section>`; }
function renderGuardrails(r){ return `<section class="panel"><span class="eyebrow">Evidence boundary</span><h2>Do not conclude</h2><p>These guardrails prevent the tool from overclaiming what the evidence can prove.</p>${list(r.doNotConclude)}</section><section class="panel"><span class="eyebrow">Routing</span><h2>Who should review next?</h2><div class="routeBox"><div>${pill('Primary reviewer','blue')} <b>DCL Inventory Review</b><span>Review Flowtrac record, serial match, DNS/IP/MAC candidates, and whether bin/rack/U should be updated.</span></div><div>${pill('Technical source owner','purple')} <b>Network / AP source / Lansweeper owner</b><span>Confirm AP and Lansweeper exports and resolve source disagreement.</span></div><div>${pill('Final location check','neutral')} <b>Physical Audit / Technician Ticket</b><span>Confirm actual room/rack/U before final location update if evidence is incomplete.</span></div></div></section>`; }
function renderReceipt(c,r){ return `<section class="panel"><div class="panelHead"><div><span class="eyebrow">Audit-ready output</span><h2>Evidence receipt</h2></div><button onclick="download('ufit_asset_evidence_receipt.json', receipt())">Export JSON</button></div><p>This receipt preserves the full reconciliation result: serial match type, DNS/IP/MAC candidates, source evidence, missing evidence, guardrails, and next owner.</p><pre>${JSON.stringify(receipt(), null, 2)}</pre></section><section class="panel"><span class="eyebrow">Reviewer note</span><h2>Internal review update</h2><div class="formGrid two"><label>Decision status<select id="reviewerDecision"><option ${c.reviewerDecision==='Open'?'selected':''}>Open</option><option ${c.reviewerDecision==='Needs documents'?'selected':''}>Needs documents</option><option ${c.reviewerDecision==='Ready for DNS/IP/MAC update'?'selected':''}>Ready for DNS/IP/MAC update</option><option ${c.reviewerDecision==='Ready for Flowtrac location update'?'selected':''}>Ready for Flowtrac location update</option><option ${c.reviewerDecision==='Closed'?'selected':''}>Closed</option></select></label><label>Reviewer notes<textarea id="reviewerNotes">${c.reviewerNotes}</textarea></label></div><button onclick="saveReviewer()">Save reviewer update</button></section>`; }

function render(){
  const c = state.case; const r = calc(c);
  const tabs = [['overview','Overview'],['intake','Asset Intake'],['technical','AP/Lansweeper Reconciliation'],['evidence','Evidence & Missing Docs'],['guardrails','Guardrails & Routing'],['receipt','Evidence Receipt']];
  let body = activeTab==='overview'?renderOverview(c,r):activeTab==='intake'?renderIntake(c):activeTab==='technical'?renderTechnical(c,r):activeTab==='evidence'?renderEvidence(c,r):activeTab==='guardrails'?renderGuardrails(r):renderReceipt(c,r);
  document.getElementById('app').innerHTML = `<aside><div class="brand"><div class="logo">CG</div><div><b>CGIF</b><span>UFIT Asset Scenario</span></div></div><nav>${tabs.map(([id,label])=>`<button class="${activeTab===id?'active':''}" onclick="setTab('${id}')">${label}</button>`).join('')}</nav><div class="sideNote"><b>Synthetic data only</b><span>Do not upload or enter real UFIT asset records. This is a public GitHub Pages demo.</span></div></aside><main><header><div><span class="eyebrow">CGIF · UFIT cross-system reconciliation</span><h1>Asset Evidence Reconciliation</h1><p>Turn AP, Lansweeper, Flowtrac, warehouse scan, ticket, and physical audit evidence into a structured review case.</p></div><div class="headerPills">${pill(r.risk + ' risk', riskTone(r.risk))}${pill(r.matchType,'blue')}${pill(r.readyFields + ' field(s) ready','success')}</div></header>${body}</main>`;
}

window.setTab=setTab; window.updateFromForm=updateFromForm; window.resetDemo=resetDemo; window.download=download; window.receipt=receipt; window.saveReviewer=saveReviewer;
render();
