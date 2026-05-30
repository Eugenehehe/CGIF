# CGIF v4 Product Requirements

## Product Name

CGIF Reviewer Workbench

## Product Positioning

CGIF is an evidence review and routing workbench for policy-sensitive healthcare cases. It helps reviewers understand what the available data supports, what evidence is missing, what should not be concluded, and which team should review the case next.

CGIF is not positioned as an autonomous clinical decision system.

## Core Problem

Healthcare teams often have fragmented claims, EHR, payer, scheduling, and care-coordination data. A raw report may show that a service was not observed or that a claim was denied, but it may not explain why.

The risk is that teams over-infer causes from incomplete data.

CGIF reduces this risk by producing:

- evidence boundary assessment
- missing evidence checklist
- do-not-conclude guardrails
- recommended review queue
- reviewer decision capture
- audit-ready receipt

## Primary Users

1. Chart reviewers
2. Coding analysts
3. Revenue cycle analysts
4. Prior authorization specialists
5. Care coordinators / patient navigators
6. Compliance reviewers
7. Quality improvement analysts
8. Health services researchers

## MVP Workflow

1. Cases are loaded through sample data, CSV, or JSON.
2. CGIF normalizes and validates case data.
3. CGIF routes each case to a work queue.
4. Reviewer opens a case.
5. Reviewer reviews known facts, missing evidence, and do-not-conclude guardrails.
6. Reviewer agrees, overrides, escalates, requests evidence, excludes, or closes the case.
7. CGIF records reviewer rationale.
8. CGIF generates audit receipts and event logs.
9. Work queue and receipts can be exported.

## Functional Requirements

### FR1: Case Intake

CGIF must support:

- synthetic demo cases
- manual JSON case input through earlier prototype pages
- CSV upload
- JSON upload

### FR2: Data Validation

CGIF must check:

- case_id exists
- duplicate case_id is flagged
- service context exists or is defaulted
- boolean-like fields are normalized

### FR3: Evidence Assessment

CGIF must separate evidence into source layers:

- claims
- EHR / chart
- workflow / scheduling
- payer / prior authorization
- care coordination / SDOH

### FR4: Routing

CGIF must route cases into operational queues:

- Chart review intake
- Clinical documentation review
- Coding and revenue cycle review
- Prior authorization review
- Patient navigation / care coordination
- Manual compliance review
- No immediate exception / sampling queue

### FR5: Risk and Priority

CGIF must assign:

- priority: Low / Medium / High
- risk score: 0-100
- evidence coverage percentage

### FR6: Inference Guardrails

CGIF must show conclusions that should not be made from current data, including:

- patient refusal without documentation
- access barrier without care-coordination evidence
- provider failure without order/referral evidence
- full clinical eligibility without chart evidence
- improper claim without coding and documentation review

### FR7: Human Review

CGIF must let reviewers capture:

- case status
- reviewer decision
- assigned owner
- final queue
- reviewer rationale
- timestamp
- role that updated the case

### FR8: Audit Receipt

Each case must be exportable as a receipt containing:

- receipt ID
- generated timestamp
- app version
- policy pack ID
- role generating receipt
- case ID
- service
- source reference
- source hash
- CGIF output
- queue
- owner
- priority
- risk score
- evidence coverage
- known facts
- missing evidence
- do-not-conclude guardrails
- reviewer status and rationale
- boundary statement

### FR9: Export

CGIF must support export of:

- work queue CSV
- audit receipts JSON
- policy pack JSON
- sample cases CSV

## Non-Functional Requirements for Production

The prototype is not production-ready for PHI. A real deployment must include:

- authentication
- role-based access control
- database persistence
- immutable audit logging
- encryption at rest and in transit
- PHI minimization
- access logging
- environment separation
- security review
- backup and retention policy
- incident response procedure
- validation with expert-labeled cases
- formal compliance review

## Prototype Boundary

The v4 Streamlit app is an industry-facing prototype. It simulates the operational workflow without claiming to be production healthcare infrastructure.

It must not be used for final clinical, legal, coverage, fraud, or reimbursement decisions.

## Success Metrics for Pilot

A pilot should measure:

- percentage of cases routed to correct reviewer
- reviewer agreement rate
- average review time reduction
- percentage of cases with missing evidence correctly identified
- reduction in unsupported conclusions
- number of cases closed without escalation
- number of cases escalated appropriately
- reviewer satisfaction

## One-Sentence Pitch

CGIF turns fragmented claims and workflow evidence into an audit-ready review queue by showing what the data supports, what it cannot support, and who should review the case next.
