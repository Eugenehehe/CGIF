# CGIF-Accounting Scenario: Accounting Judgment Evidence Workbench

## Why this scenario exists

Jiayi's feedback changes the accounting version of CGIF.

The product should not force one rigid conclusion when a company may need professional judgment, documentation support, and defensible interpretation space.

In accounting, a useful system should not say:

> This is definitely the only correct treatment.

A better system says:

> Based on the evidence currently available, these treatments appear supportable or risky; these documents are missing; these conclusions should not be made yet; and this case should be reviewed by the appropriate accounting or audit owner.

## Core positioning

CGIF-Accounting is an evidence-boundary and review-routing workbench for accounting judgment areas.

It helps finance, accounting, audit, and controllership teams determine:

1. What accounting treatment is supported by current evidence.
2. What evidence is missing.
3. Which conclusion would be overconfident or unsupported.
4. Which reviewer should own the next step.
5. What audit-ready rationale should be preserved.

## Demo scenario

### Scenario: Software / SaaS implementation cost treatment

A company signs a SaaS or enterprise software arrangement. Related invoices include:

- Setup fee
- Configuration work
- Data migration
- Training
- Customization
- Ongoing support
- Subscription license

The accounting team must decide whether each cost should be capitalized, expensed, deferred, or sent for technical accounting review.

This is a strong scenario because the answer often depends on evidence:

- What phase is the project in?
- Is the cost directly related to implementation?
- Is it training or general support?
- Is it customization or maintenance?
- Is there an approved project plan?
- Is there a contract or statement of work?
- Is there management approval?
- Is the service already live?

## Why this matches Jiayi's feedback

A company may not want software to make a final rigid accounting conclusion without room for professional judgment.

CGIF-Accounting should preserve judgment space by showing:

- Supported treatment
- Alternative treatment
- Missing evidence
- Risk level
- Do-not-conclude guardrails
- Reviewer routing
- Audit receipt

The system should assist decision-making, not lock the company into a conclusion before accounting review.

## Before CGIF-Accounting

1. Accounting receives vendor invoices and contracts.
2. Staff manually read descriptions.
3. Costs are categorized in Excel.
4. Ambiguous items are discussed through email or chat.
5. Evidence may be scattered across contract, purchase order, invoice, project plan, and approval records.
6. Some items may be over-capitalized, over-expensed, or inconsistently classified.
7. Audit support is recreated later.

## After CGIF-Accounting

1. User uploads or enters invoice / contract / project evidence.
2. CGIF classifies each line item by evidence pattern.
3. CGIF shows supported treatment, missing evidence, and unsupported conclusions.
4. CGIF routes ambiguous items to accounting manager, technical accounting, procurement, or project owner.
5. Reviewer approves, overrides, or requests more evidence.
6. CGIF generates an audit-ready evidence receipt.

## Example routing logic

| Finding | Meaning | Reviewer |
|---|---|---|
| Implementation evidence strong | Capitalization may be supportable | Accounting Manager Review |
| Training or support service | Expense treatment likely | Accounting Close Review |
| Contract language ambiguous | Need contract / SOW interpretation | Technical Accounting Review |
| Missing project approval | Evidence gap before capitalization | Project Owner / Controller Review |
| Mixed invoice line | Allocation needed | Accounting Manager Review |
| Management appears to prefer aggressive treatment but evidence weak | Judgment risk | Controller / Audit Review |

## Evidence boundary rules

CGIF-Accounting should not conclude:

- Capitalize simply because management prefers capitalization.
- Expense simply because the invoice description is vague.
- Treat a cost as implementation without contract/SOW/project evidence.
- Treat training as capitalizable without stronger support.
- Treat a mixed invoice as one category without allocation evidence.
- Replace professional accounting judgment.

## Product value

CGIF-Accounting does not remove accounting judgment.

It makes judgment more organized, reviewable, and defensible.

The main value is:

- Faster review of ambiguous accounting items
- Better evidence checklist
- Consistent reviewer routing
- Reduced unsupported conclusions
- Clear audit trail
- Preservation of professional judgment space

## Prototype boundary

This is a demo scenario only. It is not accounting advice, audit advice, tax advice, or a replacement for CPA / controller / auditor judgment.
