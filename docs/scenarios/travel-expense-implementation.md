# Travel Expense Implementation Scenario

## One-Sentence Positioning

P2D in the travel expense scenario does not replace finance review. It structures receipts, policies, exceptions, and review rationale so the reimbursement workflow becomes faster, more consistent, and more auditable.

---

## 1. Submission Stage

Employees submit a travel expense reimbursement request that includes:

- Airfare, hotel, transportation, and meal receipts
- Business travel purpose
- Travel dates and locations
- Related project or department budget

The system first converts PDF or image receipts into structured data, such as:

- Amount
- Date
- Merchant
- Currency
- Tax amount
- Expense category
- Receipt attachment reference

### Example Structured Receipt Object

```json
{
  "expense_id": "EXP-001",
  "employee_id": "EMP-1024",
  "category": "hotel",
  "merchant": "Hilton Downtown Chicago",
  "amount": 236.00,
  "currency": "USD",
  "tax_amount": 18.20,
  "expense_date": "2026-04-14",
  "travel_start_date": "2026-04-13",
  "travel_end_date": "2026-04-16",
  "city": "Chicago",
  "project_code": "PRJ-OPS-2026",
  "receipt_attached": true,
  "manager_exception_attached": false
}
```

---

## 2. Policy Matching Stage

P2D compares each submitted expense against the company travel policy.

Policy checks may include:

- Whether meal expenses exceed the daily meal limit
- Whether hotel prices exceed the city-specific standard
- Whether the same receipt has already been reimbursed
- Whether the expense date falls within the approved travel period
- Whether required receipts are missing
- Whether the expense falls within the manager's pre-approved scope

### Example Rule

```text
IF meal expense > daily limit
AND no manager exception attached
THEN flag for review
```

### Example Policy Logic Object

```json
{
  "policy_id": "TRAVEL-MEAL-001",
  "policy_name": "Daily Meal Limit",
  "condition": {
    "category": "meal",
    "amount_greater_than": "daily_meal_limit",
    "manager_exception_attached": false
  },
  "action": "flag_for_review",
  "risk_signal": "meal_limit_exceeded_without_exception"
}
```

---

## 3. Risk Classification Stage

The system does not directly reject reimbursement requests. Instead, it classifies each case based on policy fit and risk level.

### Risk Classes

| Risk Class | Meaning | Example |
|---|---|---|
| Green | Compliant with policy; eligible for auto-approval | Receipt attached, date valid, amount within policy limit |
| Yellow | Minor exception; needs human confirmation | Meal cost slightly above limit without clear explanation |
| Red | High-risk issue; requires finance review | Duplicate receipt, abnormal amount, missing approval, or missing receipt |

### Example Classification Logic

```text
IF all required fields are present
AND amount is within policy threshold
AND expense date is within travel period
AND no duplicate receipt is detected
THEN classify as Green

IF amount exceeds policy threshold by a small margin
OR explanation is incomplete
THEN classify as Yellow

IF receipt is duplicated
OR required approval is missing
OR amount is materially abnormal
THEN classify as Red
```

---

## 4. Human Review Stage

Finance staff only review Yellow and Red cases instead of manually checking every reimbursement line.

The system provides a clear explanation for each flagged case.

### Example Explanation

```text
This hotel expense exceeds the city limit by 18% and no exception approval was attached.
```

### Review UI Requirements

The reviewer should be able to see:

- The original receipt
- Extracted structured fields
- The policy clause that was applied
- The triggered risk signal
- The reason the case was classified as Yellow or Red
- Any manager exception or approval document
- The final reviewer decision and rationale

---

## 5. Payment / Audit Stage

After approval, the case moves into the payment workflow.

All decision logic should be saved for auditability, including:

- Which policy was applied
- Which receipt or data field triggered the warning
- Who approved the reimbursement
- Whether an exception was granted
- The reason for the exception
- Final payment status

### Example Audit Record

```json
{
  "case_id": "TRAVEL-CASE-2026-0001",
  "expense_id": "EXP-001",
  "final_status": "approved_with_exception",
  "risk_class": "Yellow",
  "applied_policies": [
    {
      "policy_id": "TRAVEL-HOTEL-002",
      "policy_name": "City Hotel Limit",
      "result": "flagged",
      "reason": "Hotel expense exceeded Chicago city limit by 18%."
    }
  ],
  "reviewer": {
    "name": "Finance Reviewer",
    "decision": "approved",
    "rationale": "Conference hotel rate was reasonable based on event location."
  },
  "audit_timestamp": "2026-05-03T21:00:00-04:00"
}
```

---

## Implementation Value

This scenario demonstrates how CGIF / P2D can convert an unstructured reimbursement workflow into an auditable decision-support process.

Instead of treating travel reimbursement as a simple OCR or approval automation problem, the system separates the workflow into:

1. Evidence extraction
2. Policy matching
3. Risk classification
4. Human review
5. Payment and audit logging

This keeps finance staff in control while reducing repetitive manual checks and improving consistency across reimbursement decisions.
