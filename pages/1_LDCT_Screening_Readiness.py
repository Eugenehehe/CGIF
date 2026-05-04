import json
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="LDCT Screening Readiness",
    layout="wide",
    page_icon="🫁",
)

st.title("🫁 CGIF MVP: LDCT Screening Readiness & Drop-off Classification")
st.caption(
    "A narrow CGIF demo for explaining why an apparently eligible patient failed to complete LDCT lung cancer screening. "
    "This is workflow and evidence-readiness support only; it does not replace clinician judgment."
)

LDCT_DEMO_CASES = {
    "Case 1 — Eligible, missing shared decision-making note": {
        "case_id": "LDCT-001",
        "patient_id": "PT-1001",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "appears_eligible",
        "age": 62,
        "age_documented": True,
        "smoking_history": "30 pack-years",
        "smoking_history_documented": True,
        "quit_timing": "quit 5 years ago",
        "quit_timing_documented": True,
        "provider_order_present": True,
        "shared_decision_making_documented": False,
        "prior_auth_status": "approved",
        "referral_sent": True,
        "appointment_scheduled": False,
        "service_completed": False,
        "transportation_barrier_present": False,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": False,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
    "Case 2 — Clinically ineligible from available evidence": {
        "case_id": "LDCT-002",
        "patient_id": "PT-1002",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "not_eligible",
        "age": 45,
        "age_documented": True,
        "smoking_history": "10 pack-years",
        "smoking_history_documented": True,
        "quit_timing": "current smoker",
        "quit_timing_documented": True,
        "provider_order_present": False,
        "shared_decision_making_documented": False,
        "prior_auth_status": "not_started",
        "referral_sent": False,
        "appointment_scheduled": False,
        "service_completed": False,
        "transportation_barrier_present": False,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": False,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
    "Case 3 — Eligible, no provider order": {
        "case_id": "LDCT-003",
        "patient_id": "PT-1003",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "appears_eligible",
        "age": 61,
        "age_documented": True,
        "smoking_history": "35 pack-years",
        "smoking_history_documented": True,
        "quit_timing": "quit 4 years ago",
        "quit_timing_documented": True,
        "provider_order_present": False,
        "shared_decision_making_documented": True,
        "prior_auth_status": "not_started",
        "referral_sent": False,
        "appointment_scheduled": False,
        "service_completed": False,
        "transportation_barrier_present": False,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": False,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
    "Case 4 — Eligible, transportation barrier": {
        "case_id": "LDCT-004",
        "patient_id": "PT-1004",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "appears_eligible",
        "age": 67,
        "age_documented": True,
        "smoking_history": "40 pack-years",
        "smoking_history_documented": True,
        "quit_timing": "current smoker",
        "quit_timing_documented": True,
        "provider_order_present": True,
        "shared_decision_making_documented": True,
        "prior_auth_status": "approved",
        "referral_sent": True,
        "appointment_scheduled": True,
        "service_completed": False,
        "transportation_barrier_present": True,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": False,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
    "Case 5 — Eligible, prior authorization delay": {
        "case_id": "LDCT-005",
        "patient_id": "PT-1005",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "appears_eligible",
        "age": 59,
        "age_documented": True,
        "smoking_history": "28 pack-years",
        "smoking_history_documented": True,
        "quit_timing": "quit 2 years ago",
        "quit_timing_documented": True,
        "provider_order_present": True,
        "shared_decision_making_documented": True,
        "prior_auth_status": "delayed",
        "referral_sent": True,
        "appointment_scheduled": False,
        "service_completed": False,
        "transportation_barrier_present": False,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": False,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
    "Case 6 — Conflicting smoking history": {
        "case_id": "LDCT-006",
        "patient_id": "PT-1006",
        "requested_service": "Low-dose CT lung cancer screening",
        "clinical_eligibility_status_from_record": "unclear",
        "age": 63,
        "age_documented": True,
        "smoking_history": "conflict: 30 pack-years in one note, 10 pack-years in another",
        "smoking_history_documented": True,
        "quit_timing": "quit 6 years ago",
        "quit_timing_documented": True,
        "provider_order_present": True,
        "shared_decision_making_documented": True,
        "prior_auth_status": "approved",
        "referral_sent": True,
        "appointment_scheduled": False,
        "service_completed": False,
        "transportation_barrier_present": False,
        "language_barrier_present": False,
        "cost_barrier_present": False,
        "digital_access_barrier_present": False,
        "conflicting_evidence": True,
        "ambiguous_note": False,
        "human_reviewer_note": "Pending review",
    },
}


def present_missing(value: bool) -> str:
    return "Present" if value else "Missing"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def build_readiness_checklist(case: dict) -> list[dict]:
    return [
        {
            "Required item": "Age",
            "Status": present_missing(case.get("age_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("age"),
        },
        {
            "Required item": "Smoking history",
            "Status": present_missing(case.get("smoking_history_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("smoking_history"),
        },
        {
            "Required item": "Quit timing",
            "Status": present_missing(case.get("quit_timing_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("quit_timing"),
        },
        {
            "Required item": "Provider order",
            "Status": present_missing(case.get("provider_order_present") is True),
            "Why it matters": "Workflow readiness",
            "Evidence value": yes_no(case.get("provider_order_present") is True),
        },
        {
            "Required item": "Shared decision-making documentation",
            "Status": present_missing(case.get("shared_decision_making_documented") is True),
            "Why it matters": "Documentation readiness",
            "Evidence value": yes_no(case.get("shared_decision_making_documented") is True),
        },
        {
            "Required item": "Prior authorization status",
            "Status": present_missing(case.get("prior_auth_status") not in [None, "", "missing"]),
            "Why it matters": "Payer readiness",
            "Evidence value": case.get("prior_auth_status"),
        },
        {
            "Required item": "Referral / scheduling / completion status",
            "Status": "Present",
            "Why it matters": "Workflow completion",
            "Evidence value": f"referral_sent={case.get('referral_sent')}, scheduled={case.get('appointment_scheduled')}, completed={case.get('service_completed')}",
        },
        {
            "Required item": "Access barrier signals",
            "Status": "Present",
            "Why it matters": "Access readiness",
            "Evidence value": f"transportation={case.get('transportation_barrier_present')}, language={case.get('language_barrier_present')}, cost={case.get('cost_barrier_present')}, digital={case.get('digital_access_barrier_present')}",
        },
    ]


def classify_ldct_case(case: dict) -> dict:
    checklist = build_readiness_checklist(case)
    evidence_present = []
    evidence_missing = []

    for item in checklist:
        if item["Status"] == "Present":
            evidence_present.append(f"{item['Required item']}: {item['Evidence value']}")
        else:
            evidence_missing.append(item["Required item"])

    ambiguity = []
    if case.get("conflicting_evidence") is True:
        ambiguity.append("conflicting evidence")
    if case.get("ambiguous_note") is True:
        ambiguity.append("ambiguous or subjective note")

    access_barriers = []
    if case.get("transportation_barrier_present") is True:
        access_barriers.append("transportation barrier")
    if case.get("language_barrier_present") is True:
        access_barriers.append("language barrier")
    if case.get("cost_barrier_present") is True:
        access_barriers.append("cost barrier")
    if case.get("digital_access_barrier_present") is True:
        access_barriers.append("digital access barrier")

    clinical_status = case.get("clinical_eligibility_status_from_record", "unknown")
    payer_status = case.get("prior_auth_status")

    if ambiguity:
        primary_classification = "Needs human review"
        readiness_status = "Needs human review before classification"
        barrier_detected = ", ".join(ambiguity)
        next_action = "Human reviewer should reconcile the ambiguous or conflicting evidence before assigning a drop-off reason."
        explanation = "Evidence is conflicting. Human review required."
        color = "orange"
    elif clinical_status == "not_eligible":
        primary_classification = "Clinically ineligible"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Available record indicates clinical ineligibility"
        next_action = "Confirm with the appropriate clinical reviewer whether the patient belongs in the LDCT screening pathway."
        explanation = "Patient does not meet available eligibility criteria based on the supplied record status."
        color = "red"
    elif clinical_status in ["unknown", "unclear"] or any(
        item in evidence_missing for item in ["Age", "Smoking history", "Quit timing"]
    ):
        primary_classification = "Evidence missing"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Required eligibility evidence is missing or unclear"
        next_action = "Collect or verify age, smoking history, and quit timing evidence before continuing the workflow."
        explanation = "Eligibility may be true, but required evidence is absent or unclear."
        color = "orange"
    elif case.get("provider_order_present") is not True:
        primary_classification = "Workflow breakdown"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Provider order missing"
        next_action = "Obtain or place the LDCT provider order before routing the case downstream."
        explanation = "Patient appears eligible, but screening cannot proceed because no provider order is present."
        color = "orange"
    elif case.get("shared_decision_making_documented") is not True:
        primary_classification = "Documentation gap"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Shared decision-making documentation missing"
        next_action = "Obtain or document the shared decision-making discussion before proceeding."
        explanation = "The patient appears clinically eligible for LDCT screening, but the case is not documentation-ready because the shared decision-making note is missing."
        color = "orange"
    elif payer_status in ["denied", "pending", "delayed"]:
        primary_classification = "Payer friction"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = f"Prior authorization status: {payer_status}"
        next_action = "Resolve the authorization or coverage issue before scheduling or completion."
        explanation = "Screening pathway is blocked by payer friction."
        color = "orange"
    elif access_barriers:
        primary_classification = "Access barrier"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = ", ".join(access_barriers)
        next_action = "Route to care coordination to address the patient-facing access barrier."
        explanation = "Screening was not completed due to a patient access barrier, not clinical ineligibility."
        color = "orange"
    elif case.get("referral_sent") is False or case.get("appointment_scheduled") is False or case.get("service_completed") is False:
        primary_classification = "Workflow breakdown"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Referral, scheduling, or follow-up step failed"
        next_action = "Check referral handoff, scheduling queue, and follow-up owner."
        explanation = "Patient appears eligible, but the order/referral/scheduling pathway did not complete."
        color = "orange"
    else:
        primary_classification = "Ready / completed"
        readiness_status = "Ready or completed"
        barrier_detected = "None identified"
        next_action = "No drop-off reason detected in the supplied case."
        explanation = "Required evidence, documentation, payer readiness, and access readiness are present."
        color = "green"

    policy_workflow_requirement = [
        "Eligibility evidence: age, smoking history, and quit timing available from record",
        "Provider order required for workflow readiness",
        "Shared decision-making documentation required before first screening workflow completion",
        "Payer / authorization status checked",
        "Referral, scheduling, completion, and access barriers checked",
    ]

    receipt = {
        "Case ID": case.get("case_id"),
        "Requested service": case.get("requested_service"),
        "Primary classification": primary_classification,
        "Readiness status": readiness_status,
        "Evidence present": evidence_present,
        "Evidence missing": evidence_missing,
        "Barrier detected": barrier_detected,
        "Policy/workflow requirement": policy_workflow_requirement,
        "Recommended next action": next_action,
        "Human reviewer note": case.get("human_reviewer_note", "Pending review"),
        "Explainability statement": explanation,
    }

    audit_log = {
        "timestamp": datetime.now().isoformat(),
        "case_id": case.get("case_id"),
        "scenario": "LDCT Screening Readiness & Drop-off Classification",
        "receipt": receipt,
    }

    return {
        "primary_classification": primary_classification,
        "readiness_status": readiness_status,
        "barrier_detected": barrier_detected,
        "recommended_next_action": next_action,
        "explanation": explanation,
        "color": color,
        "checklist": checklist,
        "receipt": receipt,
        "audit_log": audit_log,
    }


with st.sidebar:
    st.header("LDCT Demo Case")
    selected_case = st.selectbox("Select case", list(LDCT_DEMO_CASES.keys()))
    default_case = LDCT_DEMO_CASES[selected_case]
    case_json = st.text_area(
        "Case Data (JSON)",
        value=json.dumps(default_case, indent=4),
        height=520,
    )
    run_button = st.button("Run LDCT Readiness Classification", type="primary")

st.markdown(
    """
    ### Product thesis

    CGIF helps healthcare teams answer:

    > **Why did an apparently eligible patient fail to complete LDCT lung cancer screening?**

    The point is not to approve or deny screening. The point is to explain why the pathway is not ready or did not complete.
    """
)

if run_button:
    try:
        case = json.loads(case_json)
        result = classify_ldct_case(case)

        st.subheader(f"Primary Classification: :{result['color']}[{result['primary_classification']}]")
        st.write(result["explanation"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Readiness status", result["readiness_status"])
        c2.metric("Barrier detected", result["barrier_detected"])
        c3.metric("Requested service", "LDCT screening")

        st.markdown("### Readiness Checklist")
        st.dataframe(pd.DataFrame(result["checklist"]), use_container_width=True)

        st.markdown("### Recommended next action")
        st.info(result["recommended_next_action"])

        with st.expander("🧾 Decision Readiness Receipt", expanded=True):
            st.json(result["receipt"])

        with st.expander("📄 Immutable Audit Log"):
            st.json(result["audit_log"])

        st.success(
            "Dr. Jacobs framing: this case should not automatically be counted as clinical ineligibility. "
            "CGIF separates documentation, workflow, payer, access, and evidence barriers."
        )
        st.warning(
            "Clinical safety boundary: this demo uses supplied record/workflow fields to classify readiness and drop-off reasons. "
            "It does not make final clinical decisions."
        )
    except Exception as exc:
        st.error(f"JSON parsing or classification error: {exc}")
else:
    st.info("Select a demo case in the sidebar and run the classification.")

st.markdown("---")
st.markdown(
    """
    ### What CGIF classifies

    | Classification | Meaning |
    |---|---|
    | Clinically ineligible | Patient does not meet screening criteria based on available evidence |
    | Evidence missing | Eligibility may be true, but required evidence is absent |
    | Documentation gap | Patient appears eligible, but required documentation is missing |
    | Workflow breakdown | Order, referral, scheduling, or follow-up step failed |
    | Payer friction | Authorization or coverage issue blocks progress |
    | Access barrier | Transportation, language, cost, digital access, or patient-facing barrier |
    | Needs human review | Evidence is ambiguous, conflicting, or subjective |

    ### What not to build yet

    - Full EHR integration
    - Full claims submission
    - General chatbot
    - Multi-policy engine
    - OCR pipeline
    - Automatic clinical decision-making
    - Epic replacement
    """
)
