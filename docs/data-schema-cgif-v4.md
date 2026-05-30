# CGIF v4 Data Schema

## Purpose

This schema defines the minimum case-level data CGIF needs to create an evidence review queue, route work, and generate audit receipts.

The schema is intentionally source-neutral. It can be populated from claims, EHR exports, scheduling systems, payer systems, or manual review extracts.

## Case Input Schema

| Field | Type | Required | Source Layer | Description |
|---|---:|---:|---|---|
| case_id | string | yes | CGIF / source system | Unique case identifier |
| service | string | recommended | policy pack | Policy-sensitive service under review |
| patient_group | string | recommended | cohort definition | Population label, not direct PHI |
| policy_pack_id | string | recommended | CGIF policy pack | Versioned policy/routing rules |
| data_mode | string | recommended | CGIF | claims_only, hybrid_claims_ehr, hybrid_claims_workflow, etc. |
| claim_service_observed | boolean | yes | claims | Whether service claim was observed |
| claim_code | string | no | claims | Procedure / claim code observed |
| screening_related_visit_observed | boolean | no | claims | Whether related encounter was observed |
| diagnosis_or_risk_code_support_present | boolean | no | claims | Whether claims-level diagnosis/risk support was observed |
| payment_status | string | no | claims / payer | paid, denied, rejected, no_service_claim_observed, unknown |
| denial_or_nonpayment_observed | boolean | no | claims / payer | Whether denial/nonpayment signal exists |
| ehr_order_available | boolean | no | EHR | Whether provider order evidence is available |
| clinical_eligibility_evidence_available | boolean | no | EHR / chart | Whether chart evidence supports eligibility review |
| shared_decision_making_note_available | boolean | no | EHR / note | Whether required documentation evidence is available |
| scheduling_record_available | boolean | no | scheduling / referral | Whether scheduling/referral evidence is available |
| prior_authorization_status | string | no | payer / authorization | approved, pending, delayed, denied, not_observed |
| care_coordination_note_available | boolean | no | care coordination | Whether navigation / SDOH notes are available |
| access_barrier_documented | boolean | no | care coordination | Whether access barrier is documented |
| access_barrier_type | string | no | care coordination | Transportation, language, cost, digital, caregiver, etc. |
| conflicting_signal | boolean | no | CGIF / reviewer | Whether source signals conflict |
| source_reference | string | no | source system | Reference to source extract, not raw PHI |
| reviewer_note | string | no | reviewer / demo | Optional note |

## Receipt Schema

Each audit receipt contains:

| Field | Description |
|---|---|
| receipt_id | Unique receipt ID |
| generated_at_utc | Receipt generation time |
| app_version | CGIF app version |
| policy_pack_id | Policy pack used |
| generated_by_role | Simulated or real role that generated receipt |
| case_id | Case identifier |
| service | Service under review |
| source_reference | Source extract reference |
| source_hash | Hash of normalized source payload |
| primary_output | CGIF output |
| queue | Recommended work queue |
| recommended_owner | Recommended reviewer/team |
| priority | Low / Medium / High |
| risk_score | 0-100 score for triage |
| evidence_coverage | Percent of core evidence items available |
| known_facts | Evidence-supported facts |
| missing_evidence | Evidence needed before stronger conclusions |
| do_not_conclude | Unsupported conclusions to avoid |
| review_questions | Questions for human reviewer |
| recommended_next_action | Practical next step |
| reviewer_status | Human reviewer decision, status, rationale |
| boundary_statement | Safety and governance boundary |

## Production Data Model

A production implementation should separate data into normalized tables:

### cases

- case_id
- service
- patient_group
- policy_pack_id
- data_mode
- source_reference
- source_hash
- created_at
- updated_at

### evidence_items

- evidence_id
- case_id
- evidence_name
- source_layer
- status
- value
- inference_boundary
- source_reference

### routing_results

- routing_id
- case_id
- primary_output
- queue
- recommended_owner
- priority
- risk_score
- evidence_coverage
- generated_at
- app_version
- policy_pack_id

### reviewer_actions

- action_id
- case_id
- actor_id
- actor_role
- status
- reviewer_decision
- final_queue
- rationale
- created_at

### audit_receipts

- receipt_id
- case_id
- receipt_json
- generated_at
- generated_by
- source_hash
- policy_pack_id

### policy_packs

- policy_pack_id
- service
- version
- effective_date
- owner
- rules_json
- approved_by
- approved_at

## PHI Guidance

The prototype should avoid direct PHI. For pilots, prefer:

- synthetic data
- de-identified extracts
- hashed source references
- minimum necessary fields
- no names, SSNs, addresses, phone numbers, or free-text PHI unless governed by proper agreements

Production use would require formal privacy, security, legal, and compliance review.
