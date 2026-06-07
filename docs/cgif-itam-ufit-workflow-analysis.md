# CGIF-ITAM: UFIT Inventory Evidence & Flowtrac Reconciliation Workbench

## Purpose

CGIF-ITAM applies the CGIF evidence-boundary concept to UFIT Data Centers and Logistics inventory operations.

The goal is not to replace Flowtrac. The goal is to reconcile Flowtrac records against vendor, receiving, scanner, deployment, and bin transportation evidence before updates are made.

## Current UFIT Workflow Based on User-Observed Process

1. A UF department sends a request-for-quote ticket to UFIT DCL.
2. DCL receives the ticket.
3. DCL emails at least three vendors and asks for quotes.
4. DCL sends the quotes back to the requesting department.
5. The requesting department chooses an option and the order is made.
6. The vendor ships items to the warehouse.
7. The warehouse receives the items.
8. DCL or warehouse workers scan the received items.
9. A spreadsheet/script creates or prepares Flowtrac records from the scan data.
10. A technician picks up items from the warehouse and deploys them into buildings.
11. The technician should send a ticket to DCL for bin transportation.
12. Flowtrac bin/location should be updated.

## Current Pain Point

Flowtrac data may not be up to date. The audit task is to verify whether Flowtrac data matches available evidence sources such as vendor records, scan spreadsheets, serial numbers, bin records, and deployment/ticket information.

Two suspected failure points:

1. Serial numbers may be wrong because of scanner, import, or label/format issues.
2. Bin records may be inaccurate because technicians may deploy devices without sending a bin transportation ticket.

## Core Product Hypothesis

CGIF-ITAM turns inventory uncertainty into an actionable review workflow.

Instead of manually checking every mismatch in Excel, CGIF-ITAM classifies each asset record as:

- Matched
- Serial mismatch
- Possible scanner error
- Missing in Flowtrac
- Possible stale bin
- Missing deployment evidence
- Conflicting bin evidence
- Ready for Flowtrac update
- Needs physical audit

## Evidence Sources

Potential sources:

- RFQ / department request ticket
- Vendor quote / packing slip / order source
- Warehouse receiving scan spreadsheet
- Flowtrac inventory export
- Bin transportation ticket
- Technician deployment ticket
- Manual physical audit note
- Network or device management source if available

## Evidence Boundary Rules

CGIF-ITAM should avoid unsafe conclusions:

- Vendor serial mismatch does not automatically prove Flowtrac is wrong.
- Scanner serial mismatch does not automatically prove the physical device label is wrong.
- Flowtrac bin showing warehouse does not prove the device is physically still in the warehouse.
- DNS/location clue does not prove physical location unless confirmed by ticket, audit, or trusted system.
- Missing ticket does not prove the technician failed to deploy; it only means deployment evidence is missing.
- A proposed Flowtrac update should be separated from an approved Flowtrac update.

## Routing Logic

| CGIF-ITAM Finding | Likely Cause | Review Queue |
|---|---|---|
| Serial matches across vendor, scanner, and Flowtrac | Clean receiving/import | No exception / sampling |
| Vendor serial differs from scanner/Flowtrac | Scanner/import/vendor label issue | Warehouse Receiving Review |
| Vendor source has item but Flowtrac missing | Import incomplete or scan missed | DCL Inventory Review |
| Flowtrac bin remains warehouse but deployment ticket exists | Stale Flowtrac bin | Flowtrac Update Review |
| Flowtrac bin remains warehouse and no deployment ticket exists | Missing deployment evidence | Technician Confirmation |
| Bin evidence conflicts across sources | Unclear physical location | Physical Audit |
| Multiple sources support same proposed bin update | Update candidate | Flowtrac Update Review |
| Repeated missing bin tickets by deployment workflow | Process gap | Process Gap Escalation |

## Reviewer Roles

- DCL Inventory Review: checks Flowtrac and import readiness.
- Warehouse Receiving Review: checks scanner data and receiving records.
- Technician Confirmation: confirms whether deployment happened and whether bin transportation ticket should exist.
- Physical Audit: confirms actual physical location when evidence conflicts.
- Flowtrac Update Review: approves prepared update file before import/update.
- Process Gap Escalation: identifies repeated workflow breakdowns, such as missing transportation tickets.

## Product Output

For each asset, CGIF-ITAM should output:

- Asset ID / case ID
- Item type
- Vendor serial
- Scanner serial
- Flowtrac serial
- Current Flowtrac bin
- Evidence-supported proposed bin
- Match status
- Confidence level
- Missing evidence
- Do-not-conclude guardrails
- Recommended reviewer
- Recommended next action
- Reviewer decision and rationale
- Audit receipt
- Update file preview

## What Makes This CGIF

The point is not just matching strings.

The point is evidence governance:

1. What does each source say?
2. Which sources agree?
3. Which sources conflict?
4. What evidence is missing?
5. What conclusion is not allowed yet?
6. Who is responsible for the next review step?
7. What can safely be prepared for Flowtrac update?

## Prototype Boundary

This version must use synthetic/anonymized data only. Real UFIT serial numbers, ticket IDs, bins, device names, or internal records should not be uploaded to public GitHub Pages.
