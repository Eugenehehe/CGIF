# Healthcare Referral Readiness Scenario

## First Use Case

CGIF should focus on one healthcare workflow first:

> A patient appears eligible for a service, but the service is delayed, denied, or not completed.

Recommended initial use case:

> Lung cancer screening / referral readiness.

---

## Product Boundary

CGIF must not replace clinicians and must not make final clinical decisions.

The system should only answer:

> What is missing, what may be blocking the case, and what should a human review next?

The implementation treats clinical eligibility as an evidence status coming from the record or reviewer input, rather than having the system independently make clinical determinations.

---

## Core Value: Separate Failure Reasons

CGIF should distinguish between different reasons a service did not happen.

| Situation | Meaning |
|---|---|
| Patient does not qualify | Clinical ineligibility |
| Patient qualifies but note is incomplete | Documentation gap |
| Patient qualifies but payer blocks/delays | Payer friction |
| Patient qualifies but cannot access service | Access barrier |
| Order/referral breaks downstream | Workflow breakdown |
| Not enough information | Insufficient evidence |
| Ambiguous or conflicting record | Needs human review |

This distinction is the core product value.

---

## Missing Evidence Checklist

For each case, CGIF should produce a checklist showing what is present and what is missing.

| Required Item | Status | Why It Matters |
|---|---|---|
| Age | Present / Missing | Eligibility evidence |
| Smoking history | Present / Missing | Eligibility evidence |
| Provider order | Present / Missing | Workflow readiness |
| Shared decision-making note | Present / Missing | Documentation readiness |
| Prior auth status | Present / Missing | Payer readiness |
| Transportation/language barrier assessment | Present / Missing | Access readiness |

---

## Explainable Output

Every result should show an explanation in this structure:

```text
This classification was made because X evidence was present and Y evidence was missing.
```

No black-box classification should be shown without the underlying evidence trail.

---

## Decision Receipt

Each case should generate a short decision receipt containing:

- Case ID
- Service requested
- Policy/workflow criteria checked
- Evidence present
- Evidence missing
- Barrier category
- Recommended next action
- Reviewer note field

This receipt is the product audit trail.

---

## Human Review Required

If a case involves ambiguity, CGIF should not force a decision. It should label the case as:

```text
Needs Human Review
```

Examples include:

- Vague clinical note
- Unclear smoking history
- Conflicting documentation
- Subjective medical necessity language
- Missing follow-up reason

---

## Research Value

CGIF should create structured signals that help answer:

> Did the patient not receive care because they did not need it, or because the system failed to deliver it?

This is the Dr. Jacobs framing and is the main research value of this scenario.

---

## Primary Users

1. Clinical operations staff  
   Need to reduce rework and delays.

2. Care coordination / referral staff  
   Need to know what is blocking completion.

3. Health services researchers  
   Need structured reasons behind utilization gaps.

4. Compliance / audit reviewers  
   Need defensible explanation of decisions.

---

## MVP Success Criteria

The MVP succeeds if it can take one sample case and clearly output one of these results:

```text
Patient appears clinically eligible, but screening is blocked because shared decision-making documentation is missing.
```

```text
Patient appears eligible, but service was not completed due to transportation barrier.
```

```text
Patient is not clinically eligible based on available evidence.
```

That is enough for the first demo.
