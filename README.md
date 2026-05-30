# CGIF

CGIF is a P2D-style compliance and decision-intelligence project focused on turning policies, evidence, exceptions, reviewer rationale, and operational next steps into structured, auditable workflows.

## Current Product Direction

CGIF is positioned as an **evidence review and routing workbench** for policy-sensitive healthcare cases.

The core lesson from the meeting with Dr. Jacobs was:

> CGIF should not assume why a patient did not receive a service unless the available data supports that conclusion.

The current healthcare workflow therefore focuses on:

1. What the available data actually supports
2. What evidence is missing
3. What should not be concluded from current data
4. Which team should review the case next
5. What human reviewer decided
6. What audit-ready evidence receipt should be preserved

The stronger product framing is not:

> AI explains why care did not happen.

The stronger framing is:

> CGIF turns claims and workflow evidence into an audit-ready review queue by showing what the data supports, what it does not support, and who should review next.

## Current Main App: CGIF v4 Reviewer Workbench

The newest page is:

- `pages/2_CGIF_v4_Reviewer_Workbench.py`

This page is designed to feel closer to a real operational product than a one-off demo dashboard.

It includes:

- Operational dashboard
- Work queue table
- Simulated role-based queue filtering
- Case review page
- Human reviewer decision capture
- Reviewer rationale capture
- Audit receipt page
- Policy pack page
- Admin / readiness checklist
- CSV / JSON case upload
- Sample case export
- Work queue CSV export
- Audit receipt JSON export
- Audit event log in session state

## Primary Users

The realistic early users are not front-line physicians. The more likely early users are:

- Revenue cycle analysts
- Coding audit teams
- Compliance reviewers
- Prior authorization teams
- Chart review teams
- Patient navigation / care coordination teams
- Quality improvement teams
- Health services researchers

## Streamlit Demo Pages

The Streamlit app supports multiple CGIF scenarios:

1. PDM / Engineering Change Governance
2. Travel Expense Reimbursement
3. Healthcare Referral Readiness / LDCT Screening Readiness
4. CGIF Evidence Review & Routing Engine
5. CGIF v4 Reviewer Workbench

The upgraded healthcare workbench demonstrates a Medicare Fee-for-Service / LDCT-inspired review workflow with:

- Batch case review
- Work queue summary
- Evidence coverage score
- Priority and risk scoring
- Recommended owner / team routing
- Claims-observable evidence separation
- EHR-required evidence separation
- Workflow and care-coordination evidence gaps
- Indeterminate conclusions when current data is insufficient
- Do-not-conclude guardrails
- Human reviewer decision logging
- Audit-ready evidence receipts
- JSON and CSV export

## Example Routing Logic

| CGIF Output | Recommended Queue | Owner |
|---|---|---|
| Service not observed; reason indeterminate | Chart review intake | EHR / chart review team |
| Possible coding / payer support issue | Coding and revenue cycle review | Coding / revenue cycle analyst |
| Payer / prior authorization friction | Prior authorization review | Payer operations team |
| Access barrier supported by non-claims evidence | Patient navigation / care coordination | Care coordinator / navigator |
| Documentation gap; EHR evidence required | Clinical documentation review | Chart reviewer / documentation specialist |
| Conflicting evidence; human review required | Manual compliance review | Compliance reviewer |

## Core Concept

Policy-heavy workflows should not rely on black-box automation. CGIF structures the decision process so that every output can be explained, reviewed, routed, and audited.

Typical workflow layers:

1. Evidence intake and extraction
2. Policy matching
3. Evidence observability assessment
4. Responsible inference boundary check
5. Review routing and owner assignment
6. Human review for ambiguous or unsupported conclusions
7. Reviewer decision and rationale capture
8. Audit logging / decision receipt

## Documentation

- [CGIF Industry Readiness Roadmap](docs/industry-readiness-roadmap.md)
- [CGIF v4 Product Requirements](docs/product-requirements-cgif-v4.md)
- [CGIF v4 Data Schema](docs/data-schema-cgif-v4.md)

## Positioning

CGIF does not replace human reviewers, clinicians, EHRs, claims systems, or payer systems.

CGIF helps users see:

- what evidence is present
- what evidence is missing
- what can be responsibly inferred
- what requires additional evidence
- what should remain indeterminate
- what should not be concluded
- which team should review next
- what human reviewer decided
- what audit trail was preserved

The principle is:

> We do not guess. We show what the evidence can and cannot support, then route the case to the right reviewer.

## Prototype Boundary

This repository is now an **industry-facing prototype**, not a production healthcare deployment.

A production healthcare deployment would still require:

- security review
- PHI-safe infrastructure
- authentication
- role-based access control
- database persistence
- immutable audit logs
- encryption
- real integration contracts
- policy governance
- expert-labeled validation
- compliance approval

Do not use this prototype for final clinical, legal, coverage, fraud, or reimbursement decisions.
