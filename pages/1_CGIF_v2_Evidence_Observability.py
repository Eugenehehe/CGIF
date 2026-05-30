import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

import pandas as pd
import streamlit as st

APP_VERSION = "CGIF-v3.0-industry-review-routing"
DEFAULT_POLICY_PACK = "CMS-LDCT-FFS-DEMO-2026.05"

st.set_page_config(
    page_title="CGIF Evidence Review & Routing",
    page_icon="🧾",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Styling
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .small-note { color: #5f6368; font-size: 0.92rem; line-height: 1.45; }
    .risk-card {
        border: 1px solid #e6e8eb;
        border-radius: 12px;
        padding: 16px;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .boundary-box {
        border-left: 5px solid #f59e0b;
        padding: 12px 16px;
        background: #fff7ed;
        border-radius: 8px;
        margin: 8px 0 16px 0;
    }
    .safe-box {
        border-left: 5px solid #10b981;
        padding: 12px 16px;
        background: #ecfdf5;
        border-radius: 8px;
        margin: 8px 0 16px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Synthetic industry-style demo cases
# -----------------------------------------------------------------------------
DEMO_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "FFS-LDCT-001",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "claims_only",
        "claim_service_observed": True,
        "claim_code": "71271",
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "payment_status": "paid",
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": False,
        "clinical_eligibility_evidence_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "prior_authorization_status": "not_applicable_or_not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_001",
        "reviewer_note": "Clean claims-observed service example. EHR support not available in demo data.",
    },
    {
        "case_id": "FFS-LDCT-002",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "claims_only",
        "claim_service_observed": False,
        "claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "payment_status": "no_service_claim_observed",
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": False,
        "clinical_eligibility_evidence_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "prior_authorization_status": "not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_002",
        "reviewer_note": "Claims show no LDCT service claim; reason is not inferable from claims alone.",
    },
    {
        "case_id": "FFS-LDCT-003",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "claims_only",
        "claim_service_observed": True,
        "claim_code": "71271",
        "screening_related_visit_observed": False,
        "diagnosis_or_risk_code_support_present": False,
        "payment_status": "denied",
        "denial_or_nonpayment_observed": True,
        "ehr_order_available": False,
        "clinical_eligibility_evidence_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "prior_authorization_status": "not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_003",
        "reviewer_note": "Claim observed but weak support/denial pattern suggests coding or payer review.",
    },
    {
        "case_id": "FFS-LDCT-004",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "hybrid_claims_ehr",
        "claim_service_observed": False,
        "claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "payment_status": "no_service_claim_observed",
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": True,
        "clinical_eligibility_evidence_available": True,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "prior_authorization_status": "not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": False,
        "source_reference": "synthetic_hybrid_record_004",
        "reviewer_note": "Order and eligibility evidence available; SDM documentation missing.",
    },
    {
        "case_id": "FFS-LDCT-005",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "hybrid_claims_workflow",
        "claim_service_observed": False,
        "claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "payment_status": "no_service_claim_observed",
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": True,
        "clinical_eligibility_evidence_available": True,
        "shared_decision_making_note_available": True,
        "scheduling_record_available": True,
        "prior_authorization_status": "approved",
        "care_coordination_note_available": True,
        "access_barrier_documented": True,
        "access_barrier_type": "transportation barrier documented in care coordination note",
        "conflicting_signal": False,
        "source_reference": "synthetic_hybrid_record_005",
        "reviewer_note": "Access barrier is supported only because non-claims evidence is available.",
    },
    {
        "case_id": "FFS-LDCT-006",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "claims_only",
        "claim_service_observed": True,
        "claim_code": "71271",
        "screening_related_visit_observed": False,
        "diagnosis_or_risk_code_support_present": False,
        "payment_status": "denied",
        "denial_or_nonpayment_observed": True,
        "ehr_order_available": False,
        "clinical_eligibility_evidence_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "prior_authorization_status": "not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": True,
        "source_reference": "synthetic_claims_record_006",
        "reviewer_note": "Conflicting claims/code-level signals require manual review.",
    },
    {
        "case_id": "FFS-LDCT-007",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "hybrid_claims_payer",
        "claim_service_observed": False,
        "claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "payment_status": "no_service_claim_observed",
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": True,
        "clinical_eligibility_evidence_available": True,
        "shared_decision_making_note_available": True,
        "scheduling_record_available": False,
        "prior_authorization_status": "delayed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": None,
        "conflicting_signal": False,
        "source_reference": "synthetic_hybrid_record_007",
        "reviewer_note": "Prior authorization delay blocks workflow completion.",
    },
]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
TRUTHY = {"true", "1", "yes", "y", "observed", "available", "present"}
FALSY = {"false", "0", "no", "n", "not_observed", "missing", "none", ""}


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in TRUTHY:
        return True
    if text in FALSY:
        return False
    return False


def normalize_case(raw: Dict[str, Any]) -> Dict[str, Any]:
    case = dict(raw)
    bool_fields = [
        "claim_service_observed",
        "screening_related_visit_observed",
        "diagnosis_or_risk_code_support_present",
        "denial_or_nonpayment_observed",
        "ehr_order_available",
        "clinical_eligibility_evidence_available",
        "shared_decision_making_note_available",
        "scheduling_record_available",
        "care_coordination_note_available",
        "access_barrier_documented",
        "conflicting_signal",
    ]
    for field in bool_fields:
        case[field] = parse_bool(case.get(field, False))

    defaults = {
        "case_id": "UNSPECIFIED-CASE",
        "patient_group": "Unspecified population",
        "service": "Unspecified policy-sensitive service",
        "policy_pack_id": DEFAULT_POLICY_PACK,
        "data_mode": "unknown",
        "claim_code": None,
        "payment_status": "unknown",
        "prior_authorization_status": "not_observed",
        "access_barrier_type": None,
        "source_reference": "manual_input",
        "reviewer_note": "No reviewer note supplied.",
    }
    for key, value in defaults.items():
        case.setdefault(key, value)
    return case


def evidence_status(case: Dict[str, Any]) -> List[Dict[str, str]]:
    return [
        {
            "Evidence item": "Service claim observed",
            "Source layer": "Claims",
            "Status": "Observed" if case["claim_service_observed"] else "Not observed",
            "Use": "Shows whether a service was billed/observed; does not explain noncompletion reason by itself.",
        },
        {
            "Evidence item": "Claim / procedure code",
            "Source layer": "Claims",
            "Status": str(case.get("claim_code") or "Not observed"),
            "Use": "Supports code-level review; does not replace chart documentation.",
        },
        {
            "Evidence item": "Screening-related visit",
            "Source layer": "Claims",
            "Status": "Observed" if case["screening_related_visit_observed"] else "Not observed",
            "Use": "May identify a relevant episode but does not prove full eligibility.",
        },
        {
            "Evidence item": "Diagnosis / risk code support",
            "Source layer": "Claims",
            "Status": "Observed" if case["diagnosis_or_risk_code_support_present"] else "Not observed",
            "Use": "Can support claims-level relevance; usually cannot fully establish clinical eligibility.",
        },
        {
            "Evidence item": "Payment / denial signal",
            "Source layer": "Claims / payer",
            "Status": str(case.get("payment_status", "unknown")),
            "Use": "Can trigger coding, payer, or documentation-support review.",
        },
        {
            "Evidence item": "Provider order",
            "Source layer": "EHR / order system",
            "Status": "Available" if case["ehr_order_available"] else "Not available",
            "Use": "Needed before concluding order-level workflow readiness.",
        },
        {
            "Evidence item": "Clinical eligibility documentation",
            "Source layer": "EHR / chart",
            "Status": "Available" if case["clinical_eligibility_evidence_available"] else "Not available",
            "Use": "Needed before saying the patient was clinically eligible.",
        },
        {
            "Evidence item": "Shared decision-making note",
            "Source layer": "EHR / clinical note",
            "Status": "Available" if case["shared_decision_making_note_available"] else "Not available",
            "Use": "Needed for documentation-readiness conclusions in the LDCT example.",
        },
        {
            "Evidence item": "Scheduling / referral record",
            "Source layer": "Workflow system",
            "Status": "Available" if case["scheduling_record_available"] else "Not available",
            "Use": "Needed before concluding scheduling or referral workflow breakdown.",
        },
        {
            "Evidence item": "Prior authorization status",
            "Source layer": "Payer / authorization system",
            "Status": str(case.get("prior_authorization_status", "not_observed")),
            "Use": "Needed before assigning payer-friction ownership.",
        },
        {
            "Evidence item": "Care coordination / access note",
            "Source layer": "Care coordination / SDOH / notes",
            "Status": "Available" if case["care_coordination_note_available"] else "Not available",
            "Use": "Needed before concluding access barrier.",
        },
        {
            "Evidence item": "Documented access barrier",
            "Source layer": "Care coordination / SDOH / notes",
            "Status": str(case.get("access_barrier_type") or ("Documented" if case["access_barrier_documented"] else "Not available")),
            "Use": "Access barriers should not be inferred from claims-only service absence.",
        },
    ]


def compute_evidence_coverage(case: Dict[str, Any]) -> Tuple[int, int, int]:
    core_fields = [
        "claim_service_observed",
        "screening_related_visit_observed",
        "diagnosis_or_risk_code_support_present",
        "ehr_order_available",
        "clinical_eligibility_evidence_available",
        "shared_decision_making_note_available",
        "scheduling_record_available",
        "care_coordination_note_available",
    ]
    present = sum(1 for f in core_fields if parse_bool(case.get(f)))
    total = len(core_fields)
    pct = int(round((present / total) * 100))
    return present, total, pct


def missing_evidence(case: Dict[str, Any]) -> List[str]:
    missing = []
    if not case["ehr_order_available"]:
        missing.append("EHR provider order")
    if not case["clinical_eligibility_evidence_available"]:
        missing.append("Clinical eligibility evidence / chart support")
    if not case["shared_decision_making_note_available"]:
        missing.append("Shared decision-making note")
    if not case["scheduling_record_available"]:
        missing.append("Scheduling / referral status")
    if case.get("prior_authorization_status") in [None, "", "not_observed", "unknown"]:
        missing.append("Prior authorization / payer status")
    if not case["care_coordination_note_available"]:
        missing.append("Care coordination / access-barrier note")
    return missing


def prohibited_conclusions(case: Dict[str, Any]) -> List[str]:
    blocked = []
    if not case["claim_service_observed"]:
        blocked.append("Do not conclude patient refusal from claims-only non-observation.")
        blocked.append("Do not conclude provider failure without order/referral evidence.")
    if not case["clinical_eligibility_evidence_available"]:
        blocked.append("Do not conclude full clinical eligibility without chart evidence.")
    if not case["care_coordination_note_available"] or not case["access_barrier_documented"]:
        blocked.append("Do not conclude transportation/language/cost barrier without documented access evidence.")
    if not case["scheduling_record_available"]:
        blocked.append("Do not conclude scheduling breakdown without scheduling/referral data.")
    if case.get("payment_status") == "denied" and not case["shared_decision_making_note_available"]:
        blocked.append("Do not call the claim improper before checking chart documentation and coding context.")
    return list(dict.fromkeys(blocked))


def route_case(case: Dict[str, Any]) -> Dict[str, Any]:
    present, total, coverage_pct = compute_evidence_coverage(case)
    missing = missing_evidence(case)
    cannot_conclude = prohibited_conclusions(case)

    known_facts = []
    if case["claim_service_observed"]:
        known_facts.append(f"Service claim observed with code: {case.get('claim_code') or 'unspecified'}")
    else:
        known_facts.append("Service claim not observed in current claims-style data")
    if case["screening_related_visit_observed"]:
        known_facts.append("Screening-related visit observed")
    if case["diagnosis_or_risk_code_support_present"]:
        known_facts.append("Claims-level diagnosis/risk support observed")
    if case["denial_or_nonpayment_observed"]:
        known_facts.append("Denial or nonpayment signal observed")
    if case["ehr_order_available"]:
        known_facts.append("EHR order evidence available")
    if case["shared_decision_making_note_available"]:
        known_facts.append("Shared decision-making documentation available")
    if case["access_barrier_documented"]:
        known_facts.append(f"Access barrier documented: {case.get('access_barrier_type') or 'unspecified'}")

    auth_status = str(case.get("prior_authorization_status", "not_observed")).lower()
    payment_status = str(case.get("payment_status", "unknown")).lower()

    # Routing rules are intentionally conservative. They decide who should review next,
    # not the final clinical or legal truth.
    if case["conflicting_signal"]:
        primary_output = "Conflicting evidence; human review required"
        operational_queue = "Manual compliance review"
        owner = "Compliance reviewer"
        priority = "High"
        risk_score = 88
        inference_level = "Conflicting evidence"
        next_action = "Escalate to compliance reviewer to reconcile claim code, denial signal, and source documentation."
        review_questions = [
            "Are claim codes and payer outcome internally consistent?",
            "Does the chart support the billed service and code level?",
            "Should the case be corrected, appealed, or excluded from analysis?",
        ]
    elif case["denial_or_nonpayment_observed"] or payment_status in ["denied", "rejected", "nonpayment"]:
        primary_output = "Possible coding / payer support issue"
        operational_queue = "Coding and revenue cycle review"
        owner = "Coding / revenue cycle analyst"
        priority = "High"
        risk_score = 82
        inference_level = "Claims-supported concern; clinical reason not determined"
        next_action = "Review claim code, diagnosis support, coverage rule, denial reason, and chart documentation before making a final judgment."
        review_questions = [
            "Does diagnosis/risk-code support align with the service code?",
            "Was documentation sufficient for the submitted code?",
            "Is this a denial appeal, coding correction, or documentation gap?",
        ]
    elif auth_status in ["denied", "delayed", "pending"]:
        primary_output = "Payer / prior authorization friction"
        operational_queue = "Prior authorization review"
        owner = "Prior authorization / payer operations team"
        priority = "High" if auth_status in ["denied", "delayed"] else "Medium"
        risk_score = 76 if auth_status in ["denied", "delayed"] else 62
        inference_level = "Payer-status supported; clinical reason not determined"
        next_action = "Resolve payer authorization status or document why payer approval is not required."
        review_questions = [
            "Was prior authorization required for this pathway?",
            "Was the authorization delayed, denied, or missing?",
            "What documentation is required for payer review?",
        ]
    elif case["access_barrier_documented"] and case["care_coordination_note_available"]:
        primary_output = "Access barrier supported by non-claims evidence"
        operational_queue = "Patient navigation / care coordination"
        owner = "Care coordinator / patient navigator"
        priority = "Medium"
        risk_score = 67
        inference_level = "Hybrid evidence-supported"
        next_action = "Route to care coordination to address the documented barrier and record follow-up outcome."
        review_questions = [
            "What barrier was documented?",
            "Was follow-up attempted?",
            "Did the barrier resolution lead to service completion?",
        ]
    elif case["ehr_order_available"] and not case["shared_decision_making_note_available"]:
        primary_output = "Documentation gap; EHR evidence required"
        operational_queue = "Clinical documentation review"
        owner = "Chart reviewer / clinical documentation specialist"
        priority = "High"
        risk_score = 73
        inference_level = "EHR-supported; not claims-only"
        next_action = "Verify whether shared decision-making or required documentation exists before treating the episode as ready or complete."
        review_questions = [
            "Is required documentation truly missing or just not in the extracted fields?",
            "Does the chart support readiness for the service?",
            "Should the case be returned to clinic documentation workflow?",
        ]
    elif not case["claim_service_observed"]:
        primary_output = "Service not observed; reason indeterminate"
        operational_queue = "Chart review intake"
        owner = "EHR / chart review team"
        priority = "Medium"
        risk_score = 55
        inference_level = "Claims-limited / indeterminate"
        next_action = "Do not assign a reason from claims alone. Pull EHR order, eligibility, scheduling, payer, and care coordination evidence."
        review_questions = [
            "Was the patient actually clinically eligible?",
            "Was an order placed?",
            "Was the service scheduled, canceled, refused, or inaccessible?",
            "Is there payer or documentation friction outside claims?",
        ]
    elif case["claim_service_observed"] and case["diagnosis_or_risk_code_support_present"]:
        primary_output = "Service observed; claims-level evidence sufficient for first-pass review"
        operational_queue = "No immediate exception / sampling queue"
        owner = "Quality analyst / audit sampling"
        priority = "Low"
        risk_score = 22
        inference_level = "Claims-supported first-pass conclusion"
        next_action = "No urgent exception. Use sampling or chart verification if audit-readiness is required."
        review_questions = [
            "Is chart support required for audit sampling?",
            "Should this episode be counted as service observed?",
        ]
    else:
        primary_output = "Indeterminate; additional evidence required"
        operational_queue = "Manual review intake"
        owner = "Human reviewer"
        priority = "Medium"
        risk_score = 50
        inference_level = "Insufficient evidence"
        next_action = "Collect additional source evidence before assigning an operational cause."
        review_questions = [
            "Which source system contains the missing fact?",
            "Is the case analyzable with current data?",
        ]

    receipt = {
        "receipt_id": f"{case.get('case_id')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "app_version": APP_VERSION,
        "policy_pack_id": case.get("policy_pack_id", DEFAULT_POLICY_PACK),
        "case_id": case.get("case_id"),
        "patient_group": case.get("patient_group"),
        "service": case.get("service"),
        "source_reference": case.get("source_reference"),
        "data_mode": case.get("data_mode"),
        "primary_output": primary_output,
        "operational_queue": operational_queue,
        "recommended_owner": owner,
        "priority": priority,
        "risk_score": risk_score,
        "evidence_coverage": {
            "present_core_evidence_items": present,
            "total_core_evidence_items": total,
            "coverage_pct": coverage_pct,
        },
        "known_facts": known_facts,
        "missing_evidence": missing,
        "do_not_conclude": cannot_conclude,
        "review_questions": review_questions,
        "recommended_next_action": next_action,
        "inference_level": inference_level,
        "human_reviewer_note": case.get("reviewer_note"),
        "boundary_statement": "CGIF routes evidence review. It does not determine clinical truth, legal liability, fraud, or final coverage decisions.",
    }

    return {
        "case_id": case.get("case_id"),
        "service": case.get("service"),
        "primary_output": primary_output,
        "operational_queue": operational_queue,
        "recommended_owner": owner,
        "priority": priority,
        "risk_score": risk_score,
        "evidence_coverage_pct": coverage_pct,
        "inference_level": inference_level,
        "next_action": next_action,
        "known_facts": known_facts,
        "missing_evidence": missing,
        "do_not_conclude": cannot_conclude,
        "review_questions": review_questions,
        "evidence_matrix": evidence_status(case),
        "receipt": receipt,
    }


def evaluate_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [route_case(normalize_case(case)) for case in cases]


def summary_rows(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "Case ID": result["case_id"],
            "Primary output": result["primary_output"],
            "Queue": result["operational_queue"],
            "Owner": result["recommended_owner"],
            "Priority": result["priority"],
            "Risk score": result["risk_score"],
            "Evidence coverage %": result["evidence_coverage_pct"],
        }
        for result in results
    ]


def parse_uploaded_or_text(uploaded_file, text: str) -> List[Dict[str, Any]]:
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            return df.where(pd.notnull(df), None).to_dict(orient="records")
        if uploaded_file.name.endswith(".json"):
            payload = json.loads(uploaded_file.read().decode("utf-8"))
            return payload if isinstance(payload, list) else [payload]
        raise ValueError("Upload must be CSV or JSON.")

    payload = json.loads(text)
    return payload if isinstance(payload, list) else [payload]


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
st.title("🧾 CGIF — Evidence Review & Routing Engine")
st.caption(
    "Industry-oriented version: claims-to-evidence review, responsible inference boundaries, and operational routing."
)

st.markdown(
    """
<div class="boundary-box">
<b>Core positioning:</b> CGIF does not claim the real reason care did not happen from incomplete data. It shows what is known, what is missing, what should not be concluded, and which team should review next.
</div>
""",
    unsafe_allow_html=True,
)

with st.expander("What makes this version more industry-usable?", expanded=False):
    st.markdown(
        """
- **Batch review queue** instead of only one demo case.
- **Operational routing** to chart review, coding/revenue cycle, prior authorization, care coordination, or compliance.
- **Priority and risk score** for worklist triage.
- **Evidence coverage score** to show how complete the available data is.
- **Do-not-conclude guardrails** to prevent overclaiming from claims-only data.
- **Audit-ready receipt** with policy pack ID, known facts, missing evidence, reviewer questions, and timestamp.

This is still a prototype. For real deployment, it would need security, access control, PHI handling, integration contracts, validation, and compliance review.
"""
    )

with st.sidebar:
    st.header("Input")
    input_mode = st.radio(
        "Choose input mode",
        ["Synthetic demo batch", "Manual JSON", "Upload CSV / JSON"],
        index=0,
    )

    selected_case_names = []
    manual_text = ""
    uploaded = None

    if input_mode == "Synthetic demo batch":
        case_options = [case["case_id"] for case in DEMO_CASES]
        selected_case_names = st.multiselect(
            "Select cases",
            case_options,
            default=case_options,
        )
    elif input_mode == "Manual JSON":
        st.caption("Paste one case object or a list of case objects.")
        manual_text = st.text_area(
            "Case JSON",
            value=json.dumps(DEMO_CASES[1], indent=4),
            height=520,
        )
    else:
        uploaded = st.file_uploader("Upload CSV or JSON", type=["csv", "json"])
        with st.expander("Required / supported columns"):
            st.code(
                "case_id, service, patient_group, policy_pack_id, data_mode, "
                "claim_service_observed, claim_code, screening_related_visit_observed, "
                "diagnosis_or_risk_code_support_present, payment_status, "
                "denial_or_nonpayment_observed, ehr_order_available, "
                "clinical_eligibility_evidence_available, shared_decision_making_note_available, "
                "scheduling_record_available, prior_authorization_status, "
                "care_coordination_note_available, access_barrier_documented, "
                "access_barrier_type, conflicting_signal, source_reference, reviewer_note"
            )

    run = st.button("Run CGIF Review Routing", type="primary")

if not run:
    st.info("Choose input mode, then run CGIF Review Routing.")
    st.markdown("### Recommended first demo")
    st.write(
        "Use the synthetic batch first. It shows how CGIF turns a vague claims/care-gap problem into actionable work queues."
    )
else:
    try:
        if input_mode == "Synthetic demo batch":
            selected = [case for case in DEMO_CASES if case["case_id"] in selected_case_names]
            cases = selected or DEMO_CASES
        else:
            cases = parse_uploaded_or_text(uploaded, manual_text)

        results = evaluate_cases(cases)
        summary_df = pd.DataFrame(summary_rows(results))

        st.subheader("Work Queue Summary")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Cases reviewed", len(results))
        c2.metric("High priority", int((summary_df["Priority"] == "High").sum()))
        c3.metric("Needs human routing", int((summary_df["Queue"] != "No immediate exception / sampling queue").sum()))
        c4.metric("Avg evidence coverage", f"{summary_df['Evidence coverage %'].mean():.0f}%")

        st.dataframe(summary_df, use_container_width=True)

        queue_counts = summary_df.groupby(["Queue", "Priority"]).size().reset_index(name="Cases")
        st.markdown("### Queue distribution")
        st.dataframe(queue_counts, use_container_width=True)

        selected_case_id = st.selectbox("Inspect case", summary_df["Case ID"].tolist())
        selected_result = next(result for result in results if result["case_id"] == selected_case_id)

        st.markdown("---")
        st.subheader(f"Case Detail: {selected_case_id}")

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Priority", selected_result["priority"])
        d2.metric("Risk score", selected_result["risk_score"])
        d3.metric("Evidence coverage", f"{selected_result['evidence_coverage_pct']}%")
        d4.metric("Owner", selected_result["recommended_owner"])

        st.markdown("### Primary output")
        st.success(selected_result["primary_output"])
        st.info(selected_result["next_action"])

        left, right = st.columns(2)
        with left:
            st.markdown("### What is known")
            for item in selected_result["known_facts"]:
                st.write(f"- {item}")

            st.markdown("### Missing evidence")
            if selected_result["missing_evidence"]:
                for item in selected_result["missing_evidence"]:
                    st.write(f"- {item}")
            else:
                st.write("No major missing evidence flagged for this routing rule.")

        with right:
            st.markdown("### Do not conclude")
            if selected_result["do_not_conclude"]:
                for item in selected_result["do_not_conclude"]:
                    st.write(f"- {item}")
            else:
                st.write("No major over-inference guardrail triggered.")

            st.markdown("### Review questions")
            for item in selected_result["review_questions"]:
                st.write(f"- {item}")

        st.markdown("### Evidence matrix")
        st.dataframe(pd.DataFrame(selected_result["evidence_matrix"]), use_container_width=True)

        with st.expander("Audit-ready evidence receipt", expanded=True):
            st.json(selected_result["receipt"])

        export_payload = [result["receipt"] for result in results]
        st.download_button(
            "Download audit receipts JSON",
            data=json.dumps(export_payload, indent=2),
            file_name="cgif_audit_receipts.json",
            mime="application/json",
        )
        st.download_button(
            "Download work queue CSV",
            data=summary_df.to_csv(index=False).encode("utf-8"),
            file_name="cgif_work_queue.csv",
            mime="text/csv",
        )

        st.markdown(
            """
<div class="safe-box">
<b>Deployment boundary:</b> This prototype is designed for evidence review and routing. It should not be used as a final clinical, legal, coverage, fraud, or reimbursement decision system without validation and governance.
</div>
""",
            unsafe_allow_html=True,
        )

    except Exception as exc:
        st.error(f"CGIF evaluation failed: {exc}")
