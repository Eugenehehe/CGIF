import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

APP_VERSION = "CGIF-v4.0-reviewer-workbench"
DEFAULT_POLICY_PACK_ID = "CMS-LDCT-FFS-DEMO-2026.05"

st.set_page_config(
    page_title="CGIF v4 Reviewer Workbench",
    page_icon="🏥",
    layout="wide",
)

# -----------------------------------------------------------------------------
# Industry-style configuration
# -----------------------------------------------------------------------------
ROLES = {
    "Admin": ["All queues", "Policy pack", "Audit receipts"],
    "Chart Reviewer": ["Chart review intake", "Clinical documentation review"],
    "Coding Analyst": ["Coding and revenue cycle review"],
    "Prior Auth Specialist": ["Prior authorization review"],
    "Care Coordinator": ["Patient navigation / care coordination"],
    "Compliance Reviewer": ["Manual compliance review"],
    "Quality Analyst": ["No immediate exception / sampling queue", "Chart review intake"],
}

POLICY_PACK = {
    "policy_pack_id": DEFAULT_POLICY_PACK_ID,
    "service": "Low-dose CT lung cancer screening",
    "population": "Medicare Fee-for-Service inspired demo population",
    "effective_date": "2026-05-01",
    "version": "0.4-demo",
    "owner": "CGIF demo policy owner",
    "claims_observable_signals": [
        "service claim observed",
        "claim/procedure code",
        "screening-related visit",
        "diagnosis or risk code support",
        "payment or denial status",
    ],
    "ehr_required_signals": [
        "provider order",
        "clinical eligibility evidence",
        "shared decision-making documentation",
    ],
    "workflow_required_signals": [
        "scheduling/referral status",
        "prior authorization status",
        "care coordination note",
        "documented access barrier",
    ],
    "guardrails": [
        "Do not infer patient refusal from claims-only service non-observation.",
        "Do not infer access barrier without documented care coordination or SDOH evidence.",
        "Do not infer provider failure without order/referral/scheduling evidence.",
        "Do not infer full clinical eligibility without chart-level evidence.",
        "Do not call a claim improper before coding and documentation review.",
    ],
}

REQUIRED_COLUMNS = [
    "case_id",
    "service",
    "patient_group",
    "data_mode",
    "claim_service_observed",
    "claim_code",
    "screening_related_visit_observed",
    "diagnosis_or_risk_code_support_present",
    "payment_status",
    "denial_or_nonpayment_observed",
    "ehr_order_available",
    "clinical_eligibility_evidence_available",
    "shared_decision_making_note_available",
    "scheduling_record_available",
    "prior_authorization_status",
    "care_coordination_note_available",
    "access_barrier_documented",
    "access_barrier_type",
    "conflicting_signal",
    "source_reference",
    "reviewer_note",
]

SAMPLE_CASES = [
    {
        "case_id": "FFS-LDCT-001",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
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
        "prior_authorization_status": "not_observed",
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "access_barrier_type": "",
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_001",
        "reviewer_note": "Service observed in claims; chart support not available in demo data.",
    },
    {
        "case_id": "FFS-LDCT-002",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
        "data_mode": "claims_only",
        "claim_service_observed": False,
        "claim_code": "",
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
        "access_barrier_type": "",
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_002",
        "reviewer_note": "Claims show no LDCT service claim; reason is not inferable from claims alone.",
    },
    {
        "case_id": "FFS-LDCT-003",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
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
        "access_barrier_type": "",
        "conflicting_signal": False,
        "source_reference": "synthetic_claims_record_003",
        "reviewer_note": "Claim observed but weak support and denial signal suggest coding/payer review.",
    },
    {
        "case_id": "FFS-LDCT-004",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
        "data_mode": "hybrid_claims_ehr",
        "claim_service_observed": False,
        "claim_code": "",
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
        "access_barrier_type": "",
        "conflicting_signal": False,
        "source_reference": "synthetic_hybrid_record_004",
        "reviewer_note": "Order and eligibility evidence available; SDM documentation missing.",
    },
    {
        "case_id": "FFS-LDCT-005",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
        "data_mode": "hybrid_claims_workflow",
        "claim_service_observed": False,
        "claim_code": "",
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
        "reviewer_note": "Access barrier is supported because non-claims evidence is available.",
    },
    {
        "case_id": "FFS-LDCT-006",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "policy_pack_id": DEFAULT_POLICY_PACK_ID,
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
        "access_barrier_type": "",
        "conflicting_signal": True,
        "source_reference": "synthetic_claims_record_006",
        "reviewer_note": "Conflicting claims/code-level signals require manual review.",
    },
]

# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
def init_state() -> None:
    if "cases" not in st.session_state:
        st.session_state.cases = SAMPLE_CASES.copy()
    if "reviews" not in st.session_state:
        st.session_state.reviews = {}
    if "audit_events" not in st.session_state:
        st.session_state.audit_events = []
    if "active_case_id" not in st.session_state:
        st.session_state.active_case_id = SAMPLE_CASES[0]["case_id"]


init_state()

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------
TRUE_VALUES = {"true", "1", "yes", "y", "observed", "available", "present"}
FALSE_VALUES = {"false", "0", "no", "n", "missing", "not_observed", "none", "", "nan"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def stable_hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return False


def normalize_case(case: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(case)
    for key in REQUIRED_COLUMNS:
        normalized.setdefault(key, "")
    normalized.setdefault("policy_pack_id", DEFAULT_POLICY_PACK_ID)
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
        normalized[field] = parse_bool(normalized.get(field))
    if not normalized.get("case_id"):
        normalized["case_id"] = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    if not normalized.get("service"):
        normalized["service"] = POLICY_PACK["service"]
    return normalized


def validate_cases(cases: List[Dict[str, Any]]) -> List[str]:
    errors = []
    seen = set()
    for idx, raw in enumerate(cases, start=1):
        case_id = str(raw.get("case_id", "")).strip()
        if not case_id:
            errors.append(f"Row {idx}: case_id is required.")
        if case_id in seen:
            errors.append(f"Row {idx}: duplicate case_id '{case_id}'.")
        seen.add(case_id)
        if not raw.get("service"):
            errors.append(f"Row {idx}: service is recommended for routing context.")
    return errors


def add_audit_event(case_id: str, actor_role: str, action: str, details: Dict[str, Any]) -> None:
    st.session_state.audit_events.append(
        {
            "event_id": uuid.uuid4().hex,
            "timestamp_utc": now_utc(),
            "case_id": case_id,
            "actor_role": actor_role,
            "action": action,
            "details": details,
        }
    )


def evidence_matrix(case: Dict[str, Any]) -> List[Dict[str, str]]:
    rows = [
        ("Service claim", "Claims", "Observed" if case["claim_service_observed"] else "Not observed", "Can show service was billed/observed, not why it did not occur."),
        ("Claim/procedure code", "Claims", str(case.get("claim_code") or "Not observed"), "Supports code-level review, not final clinical truth."),
        ("Screening-related visit", "Claims", "Observed" if case["screening_related_visit_observed"] else "Not observed", "Identifies possible episode context."),
        ("Diagnosis/risk support", "Claims", "Observed" if case["diagnosis_or_risk_code_support_present"] else "Not observed", "Can support relevance but not full eligibility."),
        ("Payment/denial status", "Claims / payer", str(case.get("payment_status") or "unknown"), "Can trigger coding, payer, or documentation review."),
        ("Provider order", "EHR / order", "Available" if case["ehr_order_available"] else "Not available", "Needed for order/workflow readiness."),
        ("Clinical eligibility evidence", "EHR / chart", "Available" if case["clinical_eligibility_evidence_available"] else "Not available", "Needed before calling a patient clinically eligible."),
        ("Shared decision-making note", "EHR / note", "Available" if case["shared_decision_making_note_available"] else "Not available", "Needed before claiming documentation readiness."),
        ("Scheduling/referral record", "Workflow", "Available" if case["scheduling_record_available"] else "Not available", "Needed before assigning scheduling breakdown."),
        ("Prior authorization", "Payer workflow", str(case.get("prior_authorization_status") or "not_observed"), "Needed before routing to payer operations."),
        ("Care coordination note", "Care coordination", "Available" if case["care_coordination_note_available"] else "Not available", "Needed before assigning patient access barrier."),
        ("Documented access barrier", "Care coordination / SDOH", str(case.get("access_barrier_type") or ("Documented" if case["access_barrier_documented"] else "Not available")), "Access barriers require supporting evidence."),
    ]
    return [
        {"Evidence": item, "Source": source, "Status": status, "Inference boundary": boundary}
        for item, source, status, boundary in rows
    ]


def evidence_coverage(case: Dict[str, Any]) -> int:
    fields = [
        "claim_service_observed",
        "screening_related_visit_observed",
        "diagnosis_or_risk_code_support_present",
        "ehr_order_available",
        "clinical_eligibility_evidence_available",
        "shared_decision_making_note_available",
        "scheduling_record_available",
        "care_coordination_note_available",
    ]
    return int(round(sum(1 for f in fields if case.get(f)) / len(fields) * 100))


def missing_evidence(case: Dict[str, Any]) -> List[str]:
    missing = []
    if not case["ehr_order_available"]:
        missing.append("EHR provider order")
    if not case["clinical_eligibility_evidence_available"]:
        missing.append("Clinical eligibility / chart evidence")
    if not case["shared_decision_making_note_available"]:
        missing.append("Shared decision-making documentation")
    if not case["scheduling_record_available"]:
        missing.append("Scheduling / referral record")
    if str(case.get("prior_authorization_status") or "").lower() in ["", "not_observed", "unknown"]:
        missing.append("Prior authorization / payer status")
    if not case["care_coordination_note_available"]:
        missing.append("Care coordination / access note")
    return missing


def do_not_conclude(case: Dict[str, Any]) -> List[str]:
    guardrails = []
    if not case["claim_service_observed"]:
        guardrails += [
            "Do not conclude patient refusal from claims-only service non-observation.",
            "Do not conclude provider failure without order/referral evidence.",
        ]
    if not case["clinical_eligibility_evidence_available"]:
        guardrails.append("Do not conclude full clinical eligibility without chart evidence.")
    if not case["scheduling_record_available"]:
        guardrails.append("Do not conclude scheduling breakdown without scheduling/referral data.")
    if not case["care_coordination_note_available"] or not case["access_barrier_documented"]:
        guardrails.append("Do not conclude transportation, language, or cost barrier without documented access evidence.")
    if case["denial_or_nonpayment_observed"]:
        guardrails.append("Do not label a claim improper before coding and chart documentation review.")
    return list(dict.fromkeys(guardrails))


def route_case(case: Dict[str, Any]) -> Dict[str, Any]:
    auth = str(case.get("prior_authorization_status") or "").lower()
    payment = str(case.get("payment_status") or "").lower()

    if case["conflicting_signal"]:
        output = "Conflicting evidence; human review required"
        queue = "Manual compliance review"
        owner = "Compliance reviewer"
        priority = "High"
        risk = 92
        next_action = "Escalate to compliance review to reconcile claim, code, payer, and documentation signals."
        questions = [
            "Are the claim code and denial/payment outcome internally consistent?",
            "Does chart documentation support the billed service and code level?",
            "Should the case be corrected, appealed, excluded, or escalated?",
        ]
    elif case["denial_or_nonpayment_observed"] or payment in ["denied", "rejected", "nonpayment"]:
        output = "Possible coding / payer support issue"
        queue = "Coding and revenue cycle review"
        owner = "Coding / revenue cycle analyst"
        priority = "High"
        risk = 84
        next_action = "Review claim code, diagnosis support, payer rule, denial reason, and chart documentation."
        questions = [
            "Does diagnosis/risk support align with the claim code?",
            "Is documentation sufficient for the submitted service/code?",
            "Is this an appeal, coding correction, or documentation issue?",
        ]
    elif auth in ["pending", "delayed", "denied"]:
        output = "Payer / prior authorization friction"
        queue = "Prior authorization review"
        owner = "Prior authorization / payer operations team"
        priority = "High" if auth in ["delayed", "denied"] else "Medium"
        risk = 78 if auth in ["delayed", "denied"] else 64
        next_action = "Resolve payer authorization status or document why authorization is not required."
        questions = [
            "Was prior authorization required?",
            "Was it delayed, denied, missing, or pending?",
            "What evidence is needed for payer review?",
        ]
    elif case["access_barrier_documented"] and case["care_coordination_note_available"]:
        output = "Access barrier supported by non-claims evidence"
        queue = "Patient navigation / care coordination"
        owner = "Care coordinator / patient navigator"
        priority = "Medium"
        risk = 67
        next_action = "Route to care coordination and document follow-up outcome."
        questions = [
            "What barrier was documented?",
            "Was navigation support attempted?",
            "Did follow-up lead to service completion?",
        ]
    elif case["ehr_order_available"] and not case["shared_decision_making_note_available"]:
        output = "Documentation gap; EHR evidence required"
        queue = "Clinical documentation review"
        owner = "Chart reviewer / documentation specialist"
        priority = "High"
        risk = 74
        next_action = "Verify whether required documentation exists before treating the episode as ready or complete."
        questions = [
            "Is the required note actually missing or not extracted?",
            "Does the chart support service readiness?",
            "Should the case be returned to clinical documentation workflow?",
        ]
    elif not case["claim_service_observed"]:
        output = "Service not observed; reason indeterminate"
        queue = "Chart review intake"
        owner = "EHR / chart review team"
        priority = "Medium"
        risk = 56
        next_action = "Pull EHR order, eligibility, scheduling, payer, and care coordination evidence before assigning a cause."
        questions = [
            "Was the patient clinically eligible?",
            "Was an order placed?",
            "Was the service scheduled, canceled, refused, or inaccessible?",
            "Is payer or documentation friction present outside claims?",
        ]
    else:
        output = "Service observed; first-pass claims evidence sufficient"
        queue = "No immediate exception / sampling queue"
        owner = "Quality analyst / audit sampling"
        priority = "Low"
        risk = 20
        next_action = "No urgent exception. Use audit sampling or chart verification if required."
        questions = [
            "Should this be counted as service observed?",
            "Is chart support required for audit sampling?",
        ]

    facts = []
    facts.append("Service claim observed" if case["claim_service_observed"] else "Service claim not observed")
    if case.get("claim_code"):
        facts.append(f"Claim code: {case['claim_code']}")
    if case["screening_related_visit_observed"]:
        facts.append("Screening-related visit observed")
    if case["diagnosis_or_risk_code_support_present"]:
        facts.append("Claims-level diagnosis/risk support observed")
    if case["denial_or_nonpayment_observed"]:
        facts.append("Denial or nonpayment signal observed")
    if case["ehr_order_available"]:
        facts.append("EHR order available")
    if case["shared_decision_making_note_available"]:
        facts.append("Shared decision-making note available")
    if case["access_barrier_documented"]:
        facts.append(f"Access barrier documented: {case.get('access_barrier_type') or 'unspecified'}")

    return {
        "case_id": case["case_id"],
        "service": case["service"],
        "primary_output": output,
        "queue": queue,
        "recommended_owner": owner,
        "priority": priority,
        "risk_score": risk,
        "evidence_coverage": evidence_coverage(case),
        "known_facts": facts,
        "missing_evidence": missing_evidence(case),
        "do_not_conclude": do_not_conclude(case),
        "review_questions": questions,
        "next_action": next_action,
        "evidence_matrix": evidence_matrix(case),
        "source_hash": stable_hash(case),
        "raw_case": case,
    }


def review_status(case_id: str) -> Dict[str, Any]:
    return st.session_state.reviews.get(case_id, {"status": "Open", "decision": "Pending", "rationale": "", "assigned_to": "Unassigned"})


def generate_receipt(routed: Dict[str, Any], role: str) -> Dict[str, Any]:
    review = review_status(routed["case_id"])
    return {
        "receipt_id": f"{routed['case_id']}-{uuid.uuid4().hex[:8]}",
        "generated_at_utc": now_utc(),
        "app_version": APP_VERSION,
        "policy_pack_id": routed["raw_case"].get("policy_pack_id", DEFAULT_POLICY_PACK_ID),
        "generated_by_role": role,
        "case_id": routed["case_id"],
        "service": routed["service"],
        "source_reference": routed["raw_case"].get("source_reference"),
        "source_hash": routed["source_hash"],
        "primary_output": routed["primary_output"],
        "queue": routed["queue"],
        "recommended_owner": routed["recommended_owner"],
        "priority": routed["priority"],
        "risk_score": routed["risk_score"],
        "evidence_coverage": routed["evidence_coverage"],
        "known_facts": routed["known_facts"],
        "missing_evidence": routed["missing_evidence"],
        "do_not_conclude": routed["do_not_conclude"],
        "review_questions": routed["review_questions"],
        "recommended_next_action": routed["next_action"],
        "reviewer_status": review,
        "boundary_statement": "CGIF supports evidence review and routing. It is not a final clinical, coverage, fraud, reimbursement, or legal decision system.",
    }


def get_routed_cases() -> List[Dict[str, Any]]:
    return [route_case(normalize_case(c)) for c in st.session_state.cases]


def to_summary_df(routed_cases: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in routed_cases:
        status = review_status(item["case_id"])
        rows.append(
            {
                "Case ID": item["case_id"],
                "Service": item["service"],
                "Output": item["primary_output"],
                "Queue": item["queue"],
                "Owner": item["recommended_owner"],
                "Priority": item["priority"],
                "Risk": item["risk_score"],
                "Evidence %": item["evidence_coverage"],
                "Status": status["status"],
                "Reviewer decision": status["decision"],
                "Assigned to": status["assigned_to"],
            }
        )
    return pd.DataFrame(rows)


def load_cases_from_upload(uploaded_file) -> Optional[List[Dict[str, Any]]]:
    if uploaded_file is None:
        return None
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return df.where(pd.notnull(df), None).to_dict(orient="records")
    if uploaded_file.name.endswith(".json"):
        payload = json.loads(uploaded_file.read().decode("utf-8"))
        return payload if isinstance(payload, list) else [payload]
    raise ValueError("Upload must be CSV or JSON.")


# -----------------------------------------------------------------------------
# Header and sidebar
# -----------------------------------------------------------------------------
st.title("🏥 CGIF v4 — Reviewer Workbench")
st.caption("Industry-facing prototype for evidence review, routing, human decisions, and audit receipts.")

st.warning(
    "Prototype boundary: this app does not store PHI securely, does not implement production authentication, and is not a final clinical, legal, coverage, fraud, or reimbursement decision system."
)

with st.sidebar:
    st.header("Workspace")
    current_role = st.selectbox("Simulated role", list(ROLES.keys()))
    visible_queues = ROLES[current_role]
    st.caption("This is simulated role-based filtering, not real authentication.")

    st.divider()
    st.subheader("Data input")
    uploaded = st.file_uploader("Upload cases CSV/JSON", type=["csv", "json"])
    if st.button("Load uploaded cases"):
        try:
            loaded = load_cases_from_upload(uploaded)
            if loaded is None:
                st.error("Upload a CSV or JSON file first.")
            else:
                errors = validate_cases(loaded)
                if errors:
                    st.error("Data validation failed.")
                    for err in errors[:8]:
                        st.write(f"- {err}")
                else:
                    st.session_state.cases = [normalize_case(c) for c in loaded]
                    st.session_state.reviews = {}
                    st.session_state.audit_events = []
                    st.success(f"Loaded {len(loaded)} cases.")
        except Exception as exc:
            st.error(f"Upload failed: {exc}")

    if st.button("Reset to sample cases"):
        st.session_state.cases = SAMPLE_CASES.copy()
        st.session_state.reviews = {}
        st.session_state.audit_events = []
        st.success("Reset to sample cases.")

    with st.expander("CSV schema"):
        st.code(", ".join(REQUIRED_COLUMNS))

# -----------------------------------------------------------------------------
# Main app tabs
# -----------------------------------------------------------------------------
routed_cases = get_routed_cases()
summary_df = to_summary_df(routed_cases)

if current_role != "Admin":
    summary_view = summary_df[summary_df["Queue"].isin(visible_queues)].copy()
else:
    summary_view = summary_df.copy()

if st.session_state.active_case_id not in summary_df["Case ID"].tolist() and not summary_df.empty:
    st.session_state.active_case_id = summary_df.iloc[0]["Case ID"]

tab_dashboard, tab_queue, tab_review, tab_receipts, tab_policy, tab_admin = st.tabs(
    ["Dashboard", "Work Queue", "Case Review", "Audit Receipts", "Policy Pack", "Admin / Readiness"]
)

with tab_dashboard:
    st.subheader("Operational Dashboard")
    total = len(summary_view)
    high = int((summary_view["Priority"] == "High").sum()) if not summary_view.empty else 0
    open_cases = int((summary_view["Status"] == "Open").sum()) if not summary_view.empty else 0
    avg_cov = summary_view["Evidence %"].mean() if not summary_view.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Visible cases", total)
    c2.metric("High priority", high)
    c3.metric("Open", open_cases)
    c4.metric("Avg evidence coverage", f"{avg_cov:.0f}%")

    st.markdown("### Queue distribution")
    if summary_view.empty:
        st.info("No visible cases for this role.")
    else:
        queue_counts = summary_view.groupby(["Queue", "Priority"]).size().reset_index(name="Cases")
        st.dataframe(queue_counts, use_container_width=True)

    st.markdown("### Why this meets a real workflow")
    st.write(
        "CGIF does not stop at 'indeterminate'. It creates an operational queue: what is known, what is missing, what not to conclude, who should review next, and how the reviewer closed the case."
    )

with tab_queue:
    st.subheader("Work Queue")
    if summary_view.empty:
        st.info("No visible cases for this role.")
    else:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            priority_filter = st.multiselect("Priority", sorted(summary_view["Priority"].unique()), default=sorted(summary_view["Priority"].unique()))
        with col_b:
            queue_filter = st.multiselect("Queue", sorted(summary_view["Queue"].unique()), default=sorted(summary_view["Queue"].unique()))
        with col_c:
            status_filter = st.multiselect("Status", sorted(summary_view["Status"].unique()), default=sorted(summary_view["Status"].unique()))

        filtered = summary_view[
            summary_view["Priority"].isin(priority_filter)
            & summary_view["Queue"].isin(queue_filter)
            & summary_view["Status"].isin(status_filter)
        ].copy()
        filtered = filtered.sort_values(["Priority", "Risk"], ascending=[True, False])
        st.dataframe(filtered, use_container_width=True)

        if not filtered.empty:
            selected = st.selectbox("Open case", filtered["Case ID"].tolist())
            if st.button("Open selected case in Case Review"):
                st.session_state.active_case_id = selected
                add_audit_event(selected, current_role, "case_opened", {"from": "work_queue"})
                st.success(f"Opened {selected}. Go to Case Review tab.")

with tab_review:
    st.subheader("Case Review")
    case_ids = summary_view["Case ID"].tolist() if not summary_view.empty else summary_df["Case ID"].tolist()
    if not case_ids:
        st.info("No cases available.")
    else:
        active = st.selectbox(
            "Case",
            case_ids,
            index=case_ids.index(st.session_state.active_case_id) if st.session_state.active_case_id in case_ids else 0,
        )
        st.session_state.active_case_id = active
        routed = next(item for item in routed_cases if item["case_id"] == active)
        current_review = review_status(active)

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Priority", routed["priority"])
        d2.metric("Risk", routed["risk_score"])
        d3.metric("Evidence coverage", f"{routed['evidence_coverage']}%")
        d4.metric("Status", current_review["status"])

        st.markdown("### CGIF recommendation")
        st.info(routed["primary_output"])
        st.write(f"**Recommended queue:** {routed['queue']}")
        st.write(f"**Recommended owner:** {routed['recommended_owner']}")
        st.write(f"**Next action:** {routed['next_action']}")

        left, right = st.columns(2)
        with left:
            st.markdown("### What is known")
            for item in routed["known_facts"]:
                st.write(f"- {item}")
            st.markdown("### Missing evidence")
            for item in routed["missing_evidence"]:
                st.write(f"- {item}")

        with right:
            st.markdown("### Do not conclude")
            for item in routed["do_not_conclude"]:
                st.write(f"- {item}")
            st.markdown("### Reviewer questions")
            for item in routed["review_questions"]:
                st.write(f"- {item}")

        with st.expander("Evidence matrix", expanded=False):
            st.dataframe(pd.DataFrame(routed["evidence_matrix"]), use_container_width=True)

        st.markdown("---")
        st.markdown("### Human reviewer action")
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            decision = st.selectbox(
                "Reviewer decision",
                ["Pending", "Agree with CGIF", "Override routing", "Need more evidence", "Escalate to compliance", "Exclude from analysis", "Closed"],
                index=["Pending", "Agree with CGIF", "Override routing", "Need more evidence", "Escalate to compliance", "Exclude from analysis", "Closed"].index(current_review.get("decision", "Pending"))
                if current_review.get("decision", "Pending") in ["Pending", "Agree with CGIF", "Override routing", "Need more evidence", "Escalate to compliance", "Exclude from analysis", "Closed"]
                else 0,
            )
            assigned_to = st.text_input("Assigned to", value=current_review.get("assigned_to", "Unassigned"))
        with action_col2:
            status = st.selectbox(
                "Case status",
                ["Open", "In review", "Waiting for evidence", "Escalated", "Closed"],
                index=["Open", "In review", "Waiting for evidence", "Escalated", "Closed"].index(current_review.get("status", "Open"))
                if current_review.get("status", "Open") in ["Open", "In review", "Waiting for evidence", "Escalated", "Closed"]
                else 0,
            )
            final_queue = st.selectbox(
                "Final queue / routing",
                sorted(summary_df["Queue"].unique()),
                index=sorted(summary_df["Queue"].unique()).index(routed["queue"]),
            )
        rationale = st.text_area("Reviewer rationale", value=current_review.get("rationale", ""), height=120)

        if st.button("Save reviewer action", type="primary"):
            st.session_state.reviews[active] = {
                "status": status,
                "decision": decision,
                "assigned_to": assigned_to,
                "final_queue": final_queue,
                "rationale": rationale,
                "updated_at_utc": now_utc(),
                "updated_by_role": current_role,
            }
            add_audit_event(active, current_role, "review_saved", st.session_state.reviews[active])
            st.success("Reviewer action saved in session state.")

        receipt = generate_receipt(routed, current_role)
        with st.expander("Current audit receipt", expanded=False):
            st.json(receipt)

with tab_receipts:
    st.subheader("Audit Receipts")
    receipts = [generate_receipt(item, current_role) for item in routed_cases]
    receipts_df = pd.DataFrame(
        [
            {
                "Receipt ID": r["receipt_id"],
                "Case ID": r["case_id"],
                "Queue": r["queue"],
                "Priority": r["priority"],
                "Status": r["reviewer_status"].get("status"),
                "Decision": r["reviewer_status"].get("decision"),
                "Generated": r["generated_at_utc"],
            }
            for r in receipts
        ]
    )
    st.dataframe(receipts_df, use_container_width=True)
    st.download_button(
        "Download receipts JSON",
        data=json.dumps(receipts, indent=2),
        file_name="cgif_v4_audit_receipts.json",
        mime="application/json",
    )
    st.download_button(
        "Download work queue CSV",
        data=summary_df.to_csv(index=False).encode("utf-8"),
        file_name="cgif_v4_work_queue.csv",
        mime="text/csv",
    )

    st.markdown("### Audit event log")
    if st.session_state.audit_events:
        st.dataframe(pd.DataFrame(st.session_state.audit_events), use_container_width=True)
    else:
        st.info("No reviewer actions recorded yet.")

with tab_policy:
    st.subheader("Policy Pack")
    st.write("This shows how production CGIF should externalize rules instead of hiding them inside code.")
    st.json(POLICY_PACK)
    st.download_button(
        "Download policy pack JSON",
        data=json.dumps(POLICY_PACK, indent=2),
        file_name="cms_ldct_ffs_demo_policy_pack.json",
        mime="application/json",
    )

with tab_admin:
    st.subheader("Industry Readiness Checklist")
    readiness = pd.DataFrame(
        [
            {"Area": "User workflow", "Current status": "Implemented in prototype", "Production need": "Connect to real work management and persistence"},
            {"Area": "Batch queue", "Current status": "Implemented", "Production need": "Scheduled ingestion and queue refresh"},
            {"Area": "Human review", "Current status": "Session-state reviewer actions", "Production need": "Database-backed reviewer decisions and permissions"},
            {"Area": "Audit receipt", "Current status": "Implemented export", "Production need": "Immutable audit log and retention policy"},
            {"Area": "Policy pack", "Current status": "Visible demo JSON", "Production need": "Versioned policy repository with approvals"},
            {"Area": "Security", "Current status": "Not production-ready", "Production need": "Authentication, RBAC, encryption, access logging"},
            {"Area": "PHI handling", "Current status": "Synthetic/demo only", "Production need": "PHI minimization, HIPAA program, BAA/vendor review"},
            {"Area": "Data integration", "Current status": "CSV/JSON upload", "Production need": "Claims/EHR/scheduling/payer interfaces"},
            {"Area": "Validation", "Current status": "Rule-based prototype", "Production need": "Expert-labeled test set and routing accuracy metrics"},
        ]
    )
    st.dataframe(readiness, use_container_width=True)

    st.markdown("### Data quality validation")
    errors = validate_cases(st.session_state.cases)
    if errors:
        st.error("Validation issues found")
        for err in errors:
            st.write(f"- {err}")
    else:
        st.success("Loaded cases pass basic prototype validation.")

    st.markdown("### Raw active cases")
    st.dataframe(pd.DataFrame(st.session_state.cases), use_container_width=True)

    st.download_button(
        "Download sample cases CSV",
        data=pd.DataFrame(SAMPLE_CASES).to_csv(index=False).encode("utf-8"),
        file_name="cgif_v4_sample_cases.csv",
        mime="text/csv",
    )
