# CGIF Industry Readiness Roadmap

## Product Direction

CGIF is being positioned as an **evidence review and routing engine** for policy-sensitive healthcare cases.

The strongest current use case is not to claim the real reason care did not happen. The stronger use case is to help operational, compliance, coding, and research teams answer:

1. What does the available data actually support?
2. What evidence is missing?
3. What should not be concluded from the current data?
4. Which team should review the case next?
5. What audit-ready receipt should be preserved?

## Current MVP Capability

The current Streamlit prototype supports a Medicare Fee-for-Service / LDCT-inspired workflow and demonstrates:

- Batch case review
- Claims-observable evidence separation
- EHR-required evidence separation
- Workflow and care-coordination evidence gaps
- Indeterminate conclusions when the data is insufficient
- Operational queue routing
- Recommended reviewer / owner
- Priority and risk scoring
- Evidence coverage scoring
- Do-not-conclude guardrails
- Audit-ready evidence receipts
- JSON and CSV export

## Primary Users

The first realistic users are not front-line physicians.

The likely early users are:

- Revenue cycle analysts
- Coding audit teams
- Compliance reviewers
- Prior authorization teams
- Chart review teams
- Patient navigation / care coordination teams
- Quality improvement teams
- Health services researchers

## Example Work Queue Routing

| CGIF Output | Recommended Queue | Owner |
|---|---|---|
| Service not observed; reason indeterminate | Chart review intake | EHR / chart review team |
| Possible coding / payer support issue | Coding and revenue cycle review | Coding / revenue cycle analyst |
| Payer / prior authorization friction | Prior authorization review | Payer operations team |
| Access barrier supported by non-claims evidence | Patient navigation / care coordination | Care coordinator / navigator |
| Documentation gap; EHR evidence required | Clinical documentation review | Chart reviewer / documentation specialist |
| Conflicting evidence; human review required | Manual compliance review | Compliance reviewer |

## Why This Is Useful

A raw claims or workflow report may only say:

> Service not observed.

That is not operationally enough.

CGIF turns that into:

- What is known
- What is missing
- What cannot be concluded
- What team should review next
- What questions the reviewer should answer
- What receipt should be kept for auditability

This makes CGIF more useful as a review-routing system than as a black-box prediction system.

## Current Prototype Boundaries

The current version is a prototype and should not be treated as a production healthcare system.

It does not currently provide:

- PHI-safe infrastructure
- Authentication or role-based access control
- HIPAA-grade audit/security controls
- Real EHR integration
- Real claims feed integration
- Real policy engine with versioned rules
- Clinician/coder-validated ground truth
- Formal model validation or performance metrics
- Appeals / denial workflow integration
- FHIR, HL7, X12, or CMS data pipeline support

## What Is Needed for Real Industry Use

### 1. Data Integration

Minimum production integrations should include:

- Claims data feed
- EHR/chart data
- Provider order data
- Scheduling/referral data
- Prior authorization or payer status data
- Care coordination / SDOH notes

### 2. Policy Pack System

CGIF needs versioned policy packs, for example:

- Service name
- Applicable population
- Required evidence
- Claims-observable signals
- EHR-required signals
- Routing rules
- Review questions
- Do-not-conclude guardrails
- Effective date
- Policy owner

### 3. Human Review Workflow

Industry use requires a closed-loop workflow:

1. CGIF routes case to queue
2. Reviewer confirms or overrides
3. Reviewer adds rationale
4. CGIF preserves decision receipt
5. Outcome is used to improve rules and validation

### 4. Validation

CGIF should be validated against human expert review.

Useful metrics include:

- Routing accuracy
- Evidence gap detection accuracy
- Over-inference prevention rate
- Reviewer time saved
- Percentage of cases resolved without escalation
- Agreement with coder / compliance reviewer
- Reduction in ambiguous or misrouted cases

### 5. Governance and Security

A production version would require:

- Role-based access control
- Immutable audit logs
- PHI minimization
- Secure data storage
- Access logging
- Export controls
- Reviewer sign-off
- Policy version history
- Security review

## Next Build Priorities

### Phase 1 — Make the MVP operationally useful

- Add batch upload support
- Add work queue summary
- Add owner routing
- Add priority and risk score
- Add missing evidence list
- Add do-not-conclude guardrails
- Add audit receipt export

Status: implemented in the v3 Streamlit page.

### Phase 2 — Make rules configurable

- Move rules out of code into a policy pack JSON/YAML file
- Allow different services beyond LDCT
- Support configurable review queues and owners

### Phase 3 — Add reviewer feedback loop

- Add reviewer decision field
- Add reviewer override reason
- Add final disposition
- Export labeled review outcomes

### Phase 4 — Prepare for real pilot discussion

- Define one target workflow
- Define required data fields
- Define validation methodology
- Define who reviews routed cases
- Define success metrics

## Recommended Pilot Framing

A realistic pilot should not promise clinical automation.

A better pilot framing is:

> Can CGIF reduce ambiguity and improve routing in policy-sensitive claims or care-gap review by showing what evidence is present, what is missing, what should not be concluded, and who should review next?

## One-Sentence Pitch

CGIF turns claims and workflow evidence into an audit-ready review queue by showing what the data supports, what it does not support, and which team should review the case next.
