# CGIF

CGIF is a P2D-style compliance and decision-intelligence project focused on turning policies, evidence, exceptions, reviewer rationale, and operational next steps into structured, auditable workflows.

## Current Product Direction

CGIF is now positioned as an **evidence review and routing engine** for policy-sensitive healthcare cases.

The core lesson from the meeting with Dr. Jacobs was:

> CGIF should not assume why a patient did not receive a service unless the available data supports that conclusion.

The current healthcare workflow therefore focuses on:

1. What the available data actually supports
2. What evidence is missing
3. What should not be concluded from current data
4. Which team should review the case next
5. What audit-ready evidence receipt should be preserved

The stronger product framing is not:

> AI explains why care did not happen.

The stronger framing is:

> CGIF turns claims and workflow evidence into an audit-ready review queue by showing what the data supports, what it does not support, and who should review next.

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

## Streamlit Demo

The Streamlit app supports multiple CGIF scenarios:

1. PDM / Engineering Change Governance
2. Travel Expense Reimbursement
3. Healthcare Referral Readiness / LDCT Screening Readiness
4. CGIF Evidence Review & Routing Engine

The upgraded healthcare page demonstrates a Medicare Fee-for-Service / LDCT-inspired review workflow with:

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
7. Audit logging / decision receipt

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

The principle is:

> We do not guess. We show what the evidence can and cannot support, then route the case to the right reviewer.

## Roadmap

See the industry-readiness roadmap:

- [CGIF Industry Readiness Roadmap](docs/industry-readiness-roadmap.md)

## Prototype Boundary

This repository is still a prototype. A production healthcare deployment would require security review, PHI-safe infrastructure, access control, real integration contracts, policy governance, human reviewer validation, and compliance approval.
