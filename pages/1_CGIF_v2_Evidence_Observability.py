import json
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="CGIF v2 Evidence Observability",
    page_icon="🧾",
    layout="wide",
)

st.title("🧾 CGIF v2 — Evidence Observability Framework")
st.caption(
    "Revised after Dr. Jacobs' feedback: CGIF should not assume why care did not occur unless the available data supports that conclusion."
)

st.markdown(
    """
## Revised thesis

CGIF is no longer framed as a direct reason-classification tool.

Instead, CGIF asks:

1. **What is observable in claims-level data?**
2. **What requires EHR, workflow, or care-coordination evidence?**
3. **What should remain indeterminate because the available data does not support a responsible conclusion?**

The purpose is **responsible inference**: separate what we can prove from what we cannot prove.
"""
)

CLAIMS_FIRST_CASES = {
    "Case A — Service observed in claims": {
        "case_id": "CGIF-FFS-001",
        "data_mode": "claims_only",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": True,
        "ldct_claim_code": "G0297 / 71271",
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "conflicting_claims_signal": False,
        "reviewer_note": "Synthetic claims-style case for demonstration only.",
    },
    "Case B — Service not observed; reason indeterminate": {
        "case_id": "CGIF-FFS-002",
        "data_mode": "claims_only",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": False,
        "ldct_claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "conflicting_claims_signal": False,
        "reviewer_note": "Claims do not show service completion, but claims alone cannot explain why.",
    },
    "Case C — Possible coding / payer issue": {
        "case_id": "CGIF-FFS-003",
        "data_mode": "claims_only",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": True,
        "ldct_claim_code": "71271",
        "screening_related_visit_observed": False,
        "diagnosis_or_risk_code_support_present": False,
        "denial_or_nonpayment_observed": True,
        "ehr_order_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "conflicting_claims_signal": False,
        "reviewer_note": "Synthetic case representing claims/code-level support issue.",
    },
    "Case D — EHR evidence required for documentation gap": {
        "case_id": "CGIF-FFS-004",
        "data_mode": "hybrid_needed",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": False,
        "ldct_claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": True,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "conflicting_claims_signal": False,
        "reviewer_note": "EHR/order evidence suggests a documentation-readiness gap; claims alone would not support this conclusion.",
    },
    "Case E — Access barrier documented outside claims": {
        "case_id": "CGIF-FFS-005",
        "data_mode": "hybrid_needed",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": False,
        "ldct_claim_code": None,
        "screening_related_visit_observed": True,
        "diagnosis_or_risk_code_support_present": True,
        "denial_or_nonpayment_observed": False,
        "ehr_order_available": True,
        "shared_decision_making_note_available": True,
        "scheduling_record_available": True,
        "care_coordination_note_available": True,
        "access_barrier_documented": True,
        "access_barrier_type": "transportation barrier documented in care coordination note",
        "conflicting_claims_signal": False,
        "reviewer_note": "Access barrier is only supported because care coordination evidence is available.",
    },
    "Case F — Conflicting signal; human review required": {
        "case_id": "CGIF-FFS-006",
        "data_mode": "claims_only",
        "patient_group": "Medicare Fee-for-Service beneficiary",
        "service": "Low-dose CT lung cancer screening",
        "ldct_claim_observed": True,
        "ldct_claim_code": "71271",
        "screening_related_visit_observed": False,
        "diagnosis_or_risk_code_support_present": False,
        "denial_or_nonpayment_observed": True,
        "ehr_order_available": False,
        "shared_decision_making_note_available": False,
        "scheduling_record_available": False,
        "care_coordination_note_available": False,
        "access_barrier_documented": False,
        "conflicting_claims_signal": True,
        "reviewer_note": "Conflicting claims/code-level signals require manual review.",
    },
}


def yes_no(value):
    return "Yes" if value else "No"


def evidence_row(item, source, status, inference_boundary):
    return {
        "Evidence item": item,
        "Source layer": source,
        "Status": status,
        "Inference boundary": inference_boundary,
    }


def evaluate_case(case):
    rows = []

    rows.append(
        evidence_row(
            "LDCT service claim",
            "Claims",
            "Observed" if case.get("ldct_claim_observed") else "Not observed",
            "Claims can show whether a service was billed/observed, but not necessarily why a service did not occur.",
        )
    )
    rows.append(
        evidence_row(
            "LDCT claim code",
            "Claims",
            case.get("ldct_claim_code") or "Not observed",
            "Code-level evidence can support a claims-based interpretation but is not the full clinical story.",
        )
    )
    rows.append(
        evidence_row(
            "Screening-related visit",
            "Claims",
            "Observed" if case.get("screening_related_visit_observed") else "Not observed",
            "A related visit may support context but does not prove full clinical eligibility.",
        )
    )
    rows.append(
        evidence_row(
            "Diagnosis/risk code support",
            "Claims",
            "Observed" if case.get("diagnosis_or_risk_code_support_present") else "Not observed",
            "Claims codes may suggest relevance but usually cannot fully establish clinical eligibility.",
        )
    )
    rows.append(
        evidence_row(
            "Provider order",
            "EHR / Order system",
            "Available" if case.get("ehr_order_available") else "Not available in current data",
            "Usually not responsibly inferable from claims alone.",
        )
    )
    rows.append(
        evidence_row(
            "Shared decision-making documentation",
            "EHR / Clinical note",
            "Available" if case.get("shared_decision_making_note_available") else "Not available in current data",
            "Documentation gap conclusions require EHR or chart evidence.",
        )
    )
    rows.append(
        evidence_row(
            "Scheduling status",
            "Workflow / Scheduling system",
            "Available" if case.get("scheduling_record_available") else "Not available in current data",
            "Workflow breakdown conclusions require order/scheduling/referral evidence.",
        )
    )
    rows.append(
        evidence_row(
            "Access barrier",
            "Care coordination / SDOH / Notes",
            case.get("access_barrier_type", "Documented") if case.get("access_barrier_documented") else "Not available in current data",
            "Access barrier should not be inferred from claims-only noncompletion.",
        )
    )

    if case.get("conflicting_claims_signal"):
        primary_output = "Needs human review"
        inference_level = "Conflicting / manual review required"
        explanation = "Available claims/code-level signals conflict or are insufficiently aligned. CGIF should not force a final classification."
        next_action = "Route to human reviewer for code, policy, and documentation review."
        color = "orange"
    elif case.get("ldct_claim_observed") and not case.get("denial_or_nonpayment_observed"):
        primary_output = "Service observed in claims"
        inference_level = "Claims-supported"
        explanation = "Claims-level evidence supports that the LDCT service was observed/billed. This does not by itself prove all clinical documentation requirements were satisfied."
        next_action = "If audit-readiness is needed, verify supporting EHR documentation separately."
        color = "green"
    elif case.get("denial_or_nonpayment_observed") or (
        case.get("ldct_claim_observed") and not case.get("diagnosis_or_risk_code_support_present")
    ):
        primary_output = "Possible coding / payer support issue"
        inference_level = "Claims-supported concern; clinical reason not determined"
        explanation = "Claims/code-level evidence suggests a possible coding, payment, or policy-support issue. CGIF should not infer clinician intent or patient access reason."
        next_action = "Review claim code, diagnosis support, coverage rules, and related documentation."
        color = "orange"
    elif case.get("access_barrier_documented") and case.get("care_coordination_note_available"):
        primary_output = "Access barrier supported by non-claims evidence"
        inference_level = "Hybrid evidence-supported"
        explanation = "The access barrier conclusion is only supported because care coordination evidence is available. Claims alone would only show service not observed."
        next_action = "Route to care coordination or patient navigation workflow."
        color = "orange"
    elif case.get("ehr_order_available") and not case.get("shared_decision_making_note_available"):
        primary_output = "Documentation gap requires EHR evidence"
        inference_level = "EHR-supported; not claims-only"
        explanation = "A documentation-readiness gap can be stated only because EHR/order evidence is available. Claims alone would be indeterminate."
        next_action = "Verify or document shared decision-making before treating this as workflow-ready."
        color = "orange"
    elif not case.get("ldct_claim_observed"):
        primary_output = "Service not observed; reason indeterminate"
        inference_level = "Claims-limited / indeterminate"
        explanation = "The available claims-style data does not show the service, but it does not support a responsible conclusion about why the service did not occur."
        next_action = "Do not assign an access, workflow, or documentation reason without EHR, scheduling, payer, or care coordination evidence."
        color = "red"
    else:
        primary_output = "Indeterminate"
        inference_level = "Insufficient evidence"
        explanation = "Available evidence does not support a responsible classification."
        next_action = "Collect additional evidence or route for manual review."
        color = "red"

    receipt = {
        "case_id": case.get("case_id"),
        "service": case.get("service"),
        "patient_group": case.get("patient_group"),
        "data_mode": case.get("data_mode"),
        "primary_output": primary_output,
        "inference_level": inference_level,
        "claims_observable": {
            "ldct_claim_observed": case.get("ldct_claim_observed"),
            "ldct_claim_code": case.get("ldct_claim_code"),
            "screening_related_visit_observed": case.get("screening_related_visit_observed"),
            "diagnosis_or_risk_code_support_present": case.get("diagnosis_or_risk_code_support_present"),
            "denial_or_nonpayment_observed": case.get("denial_or_nonpayment_observed"),
        },
        "requires_additional_evidence": {
            "ehr_order": not case.get("ehr_order_available"),
            "shared_decision_making_note": not case.get("shared_decision_making_note_available"),
            "scheduling_record": not case.get("scheduling_record_available"),
            "care_coordination_note": not case.get("care_coordination_note_available"),
        },
        "indeterminate_items": [
            "clinical eligibility cannot be fully established from claims alone",
            "reason for noncompletion cannot be inferred from service-not-observed alone",
            "access barrier requires documented access or care coordination evidence",
        ],
        "responsible_inference_statement": explanation,
        "recommended_next_action": next_action,
        "human_reviewer_note": case.get("reviewer_note"),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    return {
        "rows": rows,
        "primary_output": primary_output,
        "inference_level": inference_level,
        "explanation": explanation,
        "next_action": next_action,
        "color": color,
        "receipt": receipt,
    }


with st.sidebar:
    st.header("CGIF v2 Inputs")
    selected_case_name = st.selectbox("Select revised evidence case", list(CLAIMS_FIRST_CASES.keys()))
    default_case = CLAIMS_FIRST_CASES[selected_case_name]
    case_text = st.text_area(
        "Synthetic claims / workflow evidence JSON",
        value=json.dumps(default_case, indent=4),
        height=520,
    )
    run = st.button("Run Evidence Observability Evaluation", type="primary")

if not run:
    st.info("Select a case in the sidebar and run the evidence observability evaluation.")
    st.markdown(
        """
### Why this version is different

Older framing: **CGIF classifies why care did not happen.**  
Revised framing: **CGIF shows what the available data can and cannot responsibly support.**

This directly addresses the problem Dr. Jacobs raised: sometimes the real reason is not observable, and the system should not guess.
"""
    )
else:
    try:
        case = json.loads(case_text)
        result = evaluate_case(case)

        st.subheader(f"Primary Output: :{result['color']}[{result['primary_output']}]")
        st.write(result["explanation"])

        c1, c2, c3 = st.columns(3)
        c1.metric("Inference Level", result["inference_level"])
        c2.metric("Data Mode", case.get("data_mode", "unknown"))
        c3.metric("Patient Group", case.get("patient_group", "unknown"))

        st.markdown("### Evidence Observability Matrix")
        st.dataframe(pd.DataFrame(result["rows"]), use_container_width=True)

        st.markdown("### Recommended Next Action")
        st.info(result["next_action"])

        st.markdown("### Claims Evidence Receipt")
        st.json(result["receipt"])

        st.warning(
            "Boundary: This prototype does not determine clinical truth. It separates claims-observable facts, evidence gaps, and indeterminate conclusions."
        )
    except json.JSONDecodeError as exc:
        st.error(f"Invalid JSON input: {exc}")
    except Exception as exc:
        st.error(f"Evaluation failed: {exc}")
