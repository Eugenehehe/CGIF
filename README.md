# CGIF

CGIF is a P2D-style compliance and decision-intelligence project focused on turning policies, evidence, exceptions, and reviewer rationale into structured, auditable workflows.

## Scenarios

- [Healthcare Referral Readiness Scenario](docs/scenarios/healthcare-referral-readiness.md)
- [Travel Expense Implementation Scenario](docs/scenarios/travel-expense-implementation.md)

## Core Concept

The project is designed around the idea that policy-heavy workflows should not rely only on black-box automation. Instead, CGIF structures the decision process so that every output can be explained, reviewed, and audited.

Typical workflow layers:

1. Evidence intake and extraction
2. Policy matching
3. Risk / barrier classification
4. Human review
5. Audit logging / decision receipt

## Streamlit Demo

The Streamlit app supports multiple CGIF scenarios:

1. PDM / Engineering Change Governance
2. Travel Expense Reimbursement
3. Healthcare Referral Readiness

The healthcare scenario focuses on lung cancer screening / referral readiness and separates different reasons why a seemingly eligible service may be delayed, denied, or not completed.

## Positioning

CGIF does not replace human reviewers. It helps reviewers work faster and more consistently by showing which policy or workflow criteria were checked, what evidence is present, what evidence is missing, and why a case needs review.
