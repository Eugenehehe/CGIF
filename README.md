# CGIF

CGIF is a P2D-style compliance and decision-intelligence project focused on turning policies, evidence, exceptions, and reviewer rationale into structured, auditable workflows.

## Current Direction After Dr. Jacobs' Feedback

The healthcare version of CGIF is being revised from a direct reason-classification tool into an **evidence observability framework**.

The key lesson from the first meeting with Dr. Jacobs was:

> CGIF should not assume why a patient did not receive a service unless the available data supports that conclusion.

The revised healthcare framing asks:

1. What is observable in claims-level data?
2. What requires EHR, workflow, scheduling, payer, or care-coordination evidence?
3. What should remain indeterminate because the available data does not support a responsible conclusion?

This makes CGIF less like a black-box classifier and more like a responsible policy-to-evidence reasoning layer.

## Scenarios

- [Healthcare Referral Readiness Scenario](docs/scenarios/healthcare-referral-readiness.md)
- [Travel Expense Implementation Scenario](docs/scenarios/travel-expense-implementation.md)

## Streamlit Demo

The Streamlit app supports multiple CGIF scenarios:

1. PDM / Engineering Change Governance
2. Travel Expense Reimbursement
3. Healthcare Referral Readiness / LDCT Screening Readiness
4. CGIF v2 Evidence Observability Framework

The original healthcare scenario demonstrates LDCT screening readiness and several possible workflow drop-off categories.

The revised v2 page focuses on **Medicare Fee-for-Service / claims-first evidence observability**. It separates:

- claims-observable facts
- EHR-required evidence
- workflow-required evidence
- care-coordination-required evidence
- indeterminate conclusions

## Core Concept

The project is designed around the idea that policy-heavy workflows should not rely only on black-box automation. Instead, CGIF structures the decision process so that every output can be explained, reviewed, and audited.

Typical workflow layers:

1. Evidence intake and extraction
2. Policy matching
3. Evidence observability assessment
4. Risk / barrier classification only when supported by evidence
5. Human review for ambiguous or unsupported conclusions
6. Audit logging / decision receipt

## Positioning

CGIF does not replace human reviewers, clinicians, EHRs, or claims systems.

CGIF helps users see:

- what evidence is present
- what evidence is missing
- what can be responsibly inferred
- what requires additional evidence
- what should remain indeterminate

The principle is:

> We do not guess. We show what the evidence can and cannot support.
