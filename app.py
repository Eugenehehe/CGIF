import json
from datetime import datetime

import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# Page setup
# -----------------------------------------------------------------------------
st.set_page_config(page_title="CGIF Dashboard", layout="wide", page_icon="🛡️")

st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Demo data
# -----------------------------------------------------------------------------
PDM_DEFAULT_JSON = {
    "ecn_id": "ECO-2026-992",
    "safety_critical": True,
    "safety_validation_report": None,
    "production_freeze_active": True,
    "change_type": "GEOMETRY_ADJUSTMENT",
    "cost_delta": 4500.00,
}

TRAVEL_EXPENSE_DEFAULT_JSON = {
    "case_id": "TRAVEL-CASE-2026-0001",
    "employee_id": "EMP-1024",
    "employee_name": "Alex Chen",
    "business_purpose": "Client implementation workshop",
    "travel_start_date": "2026-04-13",
    "travel_end_date": "2026-04-16",
    "destination_city": "Chicago",
    "project_code": "PRJ-OPS-2026",
    "department_budget_remaining": 1800.00,
    "manager_preapproval_scope": ["airfare", "hotel", "transportation", "meal"],
    "city_hotel_limit": 200.00,
    "daily_meal_limit": 75.00,
    "previously_reimbursed_receipt_hashes": ["old-receipt-0007"],
    "expenses": [
        {
            "expense_id": "EXP-001",
            "category": "hotel",
            "merchant": "Hilton Downtown Chicago",
            "amount": 236.00,
            "currency": "USD",
            "tax_amount": 18.20,
            "expense_date": "2026-04-14",
            "receipt_attached": True,
            "receipt_hash": "hotel-chi-236",
            "manager_exception_attached": False,
        },
        {
            "expense_id": "EXP-002",
            "category": "meal",
            "merchant": "River North Steakhouse",
            "amount": 92.50,
            "currency": "USD",
            "tax_amount": 7.40,
            "expense_date": "2026-04-14",
            "receipt_attached": True,
            "receipt_hash": "meal-chi-9250",
            "manager_exception_attached": False,
        },
        {
            "expense_id": "EXP-003",
            "category": "transportation",
            "merchant": "Uber",
            "amount": 34.60,
            "currency": "USD",
            "tax_amount": 0.00,
            "expense_date": "2026-04-15",
            "receipt_attached": True,
            "receipt_hash": "uber-chi-3460",
            "manager_exception_attached": False,
        },
    ],
}

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

# -----------------------------------------------------------------------------
# Shared helpers
# -----------------------------------------------------------------------------
def status_label(value: bool) -> str:
    return "Present" if value else "Missing"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def safe_date(date_text: str):
    return datetime.strptime(date_text, "%Y-%m-%d").date()


def build_audit_log(scenario_name, data, evaluations, final_status):
    return {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario_name,
        "case_id": data.get("case_id") or data.get("ecn_id"),
        "final_status": final_status,
        "evaluations": evaluations,
        "audit_principle": "Every CGIF output should preserve evidence present, evidence missing, classification, and reviewer rationale.",
    }

# -----------------------------------------------------------------------------
# PDM logic
# -----------------------------------------------------------------------------
def evaluate_pdm_change(data):
    audit_trail = []

    if data.get("safety_critical") is True and data.get("safety_validation_report") is None:
        audit_trail.append(
            {
                "rule": "SAFETY-001",
                "severity": "CRITICAL",
                "description": "Safety-critical validation report is required.",
                "evidence": f"safety_critical={data.get('safety_critical')}; safety_validation_report=None",
                "recommendation": "Attach validation evidence before release.",
            }
        )

    if data.get("production_freeze_active") is True and data.get("change_type") != "EMERGENCY_REPAIR":
        audit_trail.append(
            {
                "rule": "FREEZE-001",
                "severity": "HIGH",
                "description": "Non-emergency changes should not proceed during a production freeze.",
                "evidence": f"production_freeze_active={data.get('production_freeze_active')}; change_type={data.get('change_type')}",
                "recommendation": "Route through an exception or emergency workflow.",
            }
        )

    if data.get("cost_delta", 0) < 0:
        audit_trail.append(
            {
                "rule": "FINANCE-001",
                "severity": "MEDIUM",
                "description": "Cost delta needs validation.",
                "evidence": f"cost_delta={data.get('cost_delta')}",
                "recommendation": "Correct or explain the cost value.",
            }
        )

    return audit_trail


def classify_pdm(audit_results):
    if any(r["severity"] == "CRITICAL" for r in audit_results):
        return "BLOCKED", "red"
    if audit_results:
        return "REVIEW REQUIRED", "orange"
    return "APPROVED", "green"

# -----------------------------------------------------------------------------
# Travel expense logic
# -----------------------------------------------------------------------------
def expense_rows(expenses):
    return [
        {
            "Expense ID": exp.get("expense_id"),
            "Category": exp.get("category"),
            "Merchant": exp.get("merchant"),
            "Amount": exp.get("amount"),
            "Date": exp.get("expense_date"),
            "Receipt": "Attached" if exp.get("receipt_attached") else "Missing",
            "Exception": "Attached" if exp.get("manager_exception_attached") else "None",
        }
        for exp in expenses
    ]


def evaluate_travel_expense_case(data):
    audit_trail = []
    expenses = data.get("expenses", [])
    travel_start = safe_date(data.get("travel_start_date"))
    travel_end = safe_date(data.get("travel_end_date"))
    daily_meal_limit = float(data.get("daily_meal_limit", 0))
    city_hotel_limit = float(data.get("city_hotel_limit", 0))
    reimbursed_hashes = set(data.get("previously_reimbursed_receipt_hashes", []))
    current_hashes = set()
    approved_scope = set(data.get("manager_preapproval_scope", []))

    for exp in expenses:
        expense_id = exp.get("expense_id", "UNKNOWN")
        category = exp.get("category")
        amount = float(exp.get("amount", 0))
        receipt_hash = exp.get("receipt_hash")
        exception_attached = exp.get("manager_exception_attached") is True

        if exp.get("receipt_attached") is not True:
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-RECEIPT-001",
                    "risk_class": "Red",
                    "severity": "HIGH",
                    "details": "Required receipt is missing.",
                    "evidence": f"receipt_attached={exp.get('receipt_attached')}",
                    "recommendation": "Request the missing receipt before payment approval.",
                }
            )

        if receipt_hash in reimbursed_hashes or receipt_hash in current_hashes:
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-DUPLICATE-001",
                    "risk_class": "Red",
                    "severity": "CRITICAL",
                    "details": "Duplicate receipt detected.",
                    "evidence": f"receipt_hash={receipt_hash}",
                    "recommendation": "Route to finance review.",
                }
            )
        if receipt_hash:
            current_hashes.add(receipt_hash)

        expense_date = safe_date(exp.get("expense_date"))
        if expense_date < travel_start or expense_date > travel_end:
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-DATE-001",
                    "risk_class": "Red",
                    "severity": "HIGH",
                    "details": "Expense date is outside travel period.",
                    "evidence": f"expense_date={expense_date}; travel_window={travel_start} to {travel_end}",
                    "recommendation": "Require explanation or manager exception.",
                }
            )

        if category not in approved_scope:
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-SCOPE-001",
                    "risk_class": "Yellow",
                    "severity": "MEDIUM",
                    "details": "Expense category is outside pre-approved scope.",
                    "evidence": f"category={category}; approved_scope={sorted(approved_scope)}",
                    "recommendation": "Ask manager to confirm whether this category is allowed.",
                }
            )

        if category == "meal" and amount > daily_meal_limit and not exception_attached:
            over_pct = ((amount - daily_meal_limit) / daily_meal_limit) * 100
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-MEAL-001",
                    "risk_class": "Red" if over_pct > 35 else "Yellow",
                    "severity": "HIGH" if over_pct > 35 else "MEDIUM",
                    "details": "Meal expense exceeds daily limit with no exception.",
                    "evidence": f"amount=${amount:.2f}; limit=${daily_meal_limit:.2f}; over={over_pct:.1f}%",
                    "recommendation": "Route to finance reviewer or request exception approval.",
                }
            )

        if category == "hotel" and amount > city_hotel_limit and not exception_attached:
            over_pct = ((amount - city_hotel_limit) / city_hotel_limit) * 100
            audit_trail.append(
                {
                    "expense_id": expense_id,
                    "rule": "TRAVEL-HOTEL-001",
                    "risk_class": "Red" if over_pct > 25 else "Yellow",
                    "severity": "HIGH" if over_pct > 25 else "MEDIUM",
                    "details": "Hotel expense exceeds city limit with no exception.",
                    "evidence": f"amount=${amount:.2f}; city_limit=${city_hotel_limit:.2f}; over={over_pct:.1f}%",
                    "recommendation": "Finance reviewer should verify rate or exception.",
                }
            )

    return audit_trail


def classify_travel(audit_results):
    if any(r.get("risk_class") == "Red" for r in audit_results):
        return "Red", "red", "High-risk issue; finance review required before payment."
    if any(r.get("risk_class") == "Yellow" for r in audit_results):
        return "Yellow", "orange", "Minor exception; human confirmation recommended."
    return "Green", "green", "Compliant with policy; eligible for auto-approval."

# -----------------------------------------------------------------------------
# LDCT logic
# -----------------------------------------------------------------------------
def build_ldct_checklist(case):
    return [
        {
            "Required item": "Age",
            "Status": status_label(case.get("age_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("age"),
        },
        {
            "Required item": "Smoking history",
            "Status": status_label(case.get("smoking_history_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("smoking_history"),
        },
        {
            "Required item": "Quit timing",
            "Status": status_label(case.get("quit_timing_documented") is True),
            "Why it matters": "Eligibility evidence",
            "Evidence value": case.get("quit_timing"),
        },
        {
            "Required item": "Provider order",
            "Status": status_label(case.get("provider_order_present") is True),
            "Why it matters": "Workflow readiness",
            "Evidence value": yes_no(case.get("provider_order_present") is True),
        },
        {
            "Required item": "Shared decision-making documentation",
            "Status": status_label(case.get("shared_decision_making_documented") is True),
            "Why it matters": "Documentation readiness",
            "Evidence value": yes_no(case.get("shared_decision_making_documented") is True),
        },
        {
            "Required item": "Prior authorization status",
            "Status": status_label(case.get("prior_auth_status") not in [None, "", "missing"]),
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


def classify_ldct_case(case):
    checklist = build_ldct_checklist(case)
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
        classification = "Needs human review"
        readiness_status = "Needs human review before classification"
        barrier_detected = ", ".join(ambiguity)
        action = "Human reviewer should reconcile ambiguous or conflicting evidence before assigning a drop-off reason."
        explanation = "Evidence is conflicting. Human review required."
        color = "orange"
    elif clinical_status == "not_eligible":
        classification = "Clinically ineligible"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Available record indicates clinical ineligibility"
        action = "Confirm with the appropriate clinical reviewer whether this patient belongs in the LDCT screening pathway."
        explanation = "Patient does not meet available eligibility criteria based on the supplied record status."
        color = "red"
    elif clinical_status in ["unknown", "unclear"] or any(
        item in evidence_missing for item in ["Age", "Smoking history", "Quit timing"]
    ):
        classification = "Evidence missing"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Required eligibility evidence is missing or unclear"
        action = "Collect or verify age, smoking history, and quit timing evidence before continuing the workflow."
        explanation = "Eligibility may be true, but required evidence is absent or unclear."
        color = "orange"
    elif case.get("provider_order_present") is not True:
        classification = "Workflow breakdown"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Provider order missing"
        action = "Obtain or place the LDCT provider order before routing the case downstream."
        explanation = "Patient appears eligible, but screening cannot proceed because no provider order is present."
        color = "orange"
    elif case.get("shared_decision_making_documented") is not True:
        classification = "Documentation gap"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Shared decision-making documentation missing"
        action = "Obtain or document the shared decision-making discussion before proceeding."
        explanation = "The patient appears clinically eligible for LDCT screening, but the case is not documentation-ready because the shared decision-making note is missing."
        color = "orange"
    elif payer_status in ["denied", "pending", "delayed"]:
        classification = "Payer friction"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = f"Prior authorization status: {payer_status}"
        action = "Resolve the authorization or coverage issue before scheduling or completion."
        explanation = "Screening pathway is blocked by payer friction."
        color = "orange"
    elif access_barriers:
        classification = "Access barrier"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = ", ".join(access_barriers)
        action = "Route to care coordination to address the patient-facing access barrier."
        explanation = "Screening was not completed due to a patient access barrier, not clinical ineligibility."
        color = "orange"
    elif case.get("referral_sent") is False or case.get("appointment_scheduled") is False or case.get("service_completed") is False:
        classification = "Workflow breakdown"
        readiness_status = "Not ready for screening workflow completion"
        barrier_detected = "Referral, scheduling, or follow-up step failed"
        action = "Check referral handoff, scheduling queue, and follow-up owner."
        explanation = "Patient appears eligible, but the order/referral/scheduling pathway did not complete."
        color = "orange"
    else:
        classification = "Ready / completed"
        readiness_status = "Ready or completed"
        barrier_detected = "None identified"
        action = "No drop-off reason detected in the supplied case."
        explanation = "Required evidence, documentation, payer readiness, and access readiness are present."
        color = "green"

    receipt = {
        "Case ID": case.get("case_id"),
        "Requested service": case.get("requested_service"),
        "Primary classification": classification,
        "Readiness status": readiness_status,
        "Evidence present": evidence_present,
        "Evidence missing": evidence_missing,
        "Barrier detected": barrier_detected,
        "Policy/workflow requirement": [
            "Eligibility evidence: age, smoking history, and quit timing available from record",
            "Provider order required for workflow readiness",
            "Shared decision-making documentation required before first screening workflow completion",
            "Payer / authorization status checked",
            "Referral, scheduling, completion, and access barriers checked",
        ],
        "Recommended next action": action,
        "Human reviewer note": case.get("human_reviewer_note", "Pending review"),
        "Explainability statement": explanation,
    }

    return {
        "classification": classification,
        "readiness_status": readiness_status,
        "barrier_detected": barrier_detected,
        "recommended_action": action,
        "explanation": explanation,
        "color": color,
        "checklist": checklist,
        "receipt": receipt,
    }

# -----------------------------------------------------------------------------
# Sidebar inputs
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Data Inputs")

    scenario = st.selectbox(
        "Select CGIF Scenario",
        [
            "PDM / Engineering Change Governance",
            "Travel Expense Reimbursement",
            "LDCT Screening Readiness",
        ],
    )

    selected_ldct_case = None
    if scenario == "LDCT Screening Readiness":
        selected_ldct_case = st.selectbox("Select LDCT Demo Case", list(LDCT_DEMO_CASES.keys()))
        default_json = LDCT_DEMO_CASES[selected_ldct_case]
        text_label = "LDCT Screening Readiness Case Data (JSON)"
        button_label = "Run LDCT Readiness Classification"
        text_key = f"ldct_{selected_ldct_case}"
    elif scenario == "Travel Expense Reimbursement":
        default_json = TRAVEL_EXPENSE_DEFAULT_JSON
        text_label = "Travel Expense Case Data (JSON)"
        button_label = "Run Travel Expense Audit"
        text_key = "travel_json"
    else:
        default_json = PDM_DEFAULT_JSON
        text_label = "Engineering Change Data (JSON)"
        button_label = "Run Governance Audit"
        text_key = "pdm_json"

    input_text = st.text_area(text_label, value=json.dumps(default_json, indent=4), height=460, key=text_key)
    run_btn = st.button(button_label, type="primary")

# -----------------------------------------------------------------------------
# Tabs
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🚀 Governance Engine", "📊 Impact Simulation", "📄 Scenario Design"])

with tab1:
    st.title("🛡️ CGIF Governance Intelligence Engine")
    st.caption("Structured, explainable, human-in-the-loop decision support. CGIF does not replace clinicians, reviewers, or source systems.")

    if not run_btn:
        st.info("👈 Select a scenario, modify the JSON in the sidebar, and run the CGIF audit.")
    else:
        try:
            data = json.loads(input_text)

            if scenario == "LDCT Screening Readiness":
                result = classify_ldct_case(data)
                st.subheader(f"Primary Classification: :{result['color']}[{result['classification']}]")
                st.write(result["explanation"])

                c1, c2, c3 = st.columns(3)
                c1.metric("Readiness Status", result["readiness_status"])
                c2.metric("Barrier Detected", result["barrier_detected"])
                c3.metric("Requested Service", "LDCT Screening")

                st.markdown("### LDCT Readiness Checklist")
                st.dataframe(pd.DataFrame(result["checklist"]), use_container_width=True)

                st.markdown("### Recommended Next Action")
                st.info(result["recommended_action"])

                with st.expander("🧾 Decision Readiness Receipt", expanded=True):
                    st.json(result["receipt"])

                with st.expander("📄 Immutable Audit Log"):
                    st.json(build_audit_log(scenario, data, [result["receipt"]], result["classification"]))

                st.success(
                    "Research framing: this separates clinical ineligibility from documentation gaps, payer friction, access barriers, workflow failures, and ambiguous evidence."
                )
                st.warning(
                    "Clinical safety boundary: this demo classifies readiness and drop-off reasons from supplied record/workflow fields. It does not make final clinical decisions."
                )

            elif scenario == "Travel Expense Reimbursement":
                audit_results = evaluate_travel_expense_case(data)
                final_status, status_color, status_explanation = classify_travel(audit_results)
                st.subheader(f"Risk Classification: :{status_color}[{final_status}]")
                st.write(status_explanation)

                total_amount = sum(float(exp.get("amount", 0)) for exp in data.get("expenses", []))
                flagged_count = len(set(r.get("expense_id") for r in audit_results))

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Claimed", f"${total_amount:,.2f}")
                c2.metric("Expense Lines", len(data.get("expenses", [])))
                c3.metric("Flagged Items", flagged_count)
                c4.metric("Final Class", final_status)

                st.markdown("### Submitted Expense Lines")
                st.dataframe(pd.DataFrame(expense_rows(data.get("expenses", []))), use_container_width=True)

                if audit_results:
                    st.markdown("### Policy Exceptions")
                    for res in audit_results:
                        st.markdown(
                            f"""
                            **Expense:** `{res['expense_id']}`  
                            **Rule:** `{res['rule']}` | **Risk:** `{res['risk_class']}` | **Severity:** `{res['severity']}`

                            - **Reasoning:** {res['details']}
                            - **Audit Evidence:** `{res['evidence']}`
                            - **Recommended Action:** {res['recommendation']}
                            """
                        )
                        st.divider()
                else:
                    st.success("✅ All travel expense checks passed. This case is eligible for auto-approval.")

                with st.expander("📄 Immutable Audit Log"):
                    st.json(build_audit_log(scenario, data, audit_results, final_status))

            else:
                audit_results = evaluate_pdm_change(data)
                final_status, status_color = classify_pdm(audit_results)
                st.subheader(f"Evaluation Status: :{status_color}[{final_status}]")

                if audit_results:
                    st.markdown("### Governance Exceptions")
                    for res in audit_results:
                        st.markdown(
                            f"""
                            **Rule:** `{res['rule']}` | **Severity:** `{res['severity']}`

                            - **Intent:** {res['description']}
                            - **Audit Evidence:** `{res['evidence']}`
                            - **Recommended Action:** {res['recommendation']}
                            """
                        )
                        st.divider()
                else:
                    st.success("✅ All governance checks passed.")

                with st.expander("📄 Immutable Audit Log"):
                    st.json(build_audit_log(scenario, data, audit_results, final_status))

        except Exception as exc:
            st.error(f"JSON parsing or evaluation error: {exc}")

with tab2:
    st.title("📊 Operational Performance Impact")

    if scenario == "LDCT Screening Readiness":
        st.markdown("### LDCT Drop-off Classification Value")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Raw EHR / Workflow Status", "Not Completed", delta="Ambiguous")
            st.write("A raw status such as 'LDCT screening not completed' does not explain whether the issue is eligibility, documentation, payer, access, or workflow failure.")
        with c2:
            st.metric("CGIF Output", "Primary Drop-off Reason", delta="Explainable", delta_color="inverse")
            st.write("CGIF turns the same case into a structured reason with evidence present, evidence missing, and the next human action.")

        st.markdown("---")
        chart_data = pd.DataFrame(
            {"Sample cases": [1, 1, 1, 1, 1, 1]},
            index=["Documentation gap", "Clinically ineligible", "Workflow breakdown", "Access barrier", "Payer friction", "Needs human review"],
        )
        st.bar_chart(chart_data)
        st.success("Research value: this helps answer whether the patient did not receive care because they did not need it, or because the system failed to deliver it.")

    elif scenario == "Travel Expense Reimbursement":
        st.markdown("### Legacy Travel Reimbursement vs. CGIF Review Flow")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Legacy Finance Review", "3-5 Days", delta="Manual line-by-line review")
            st.write("Finance staff manually inspect receipts, dates, policy limits, exceptions, and duplicate submissions.")
        with c2:
            st.metric("CGIF-Assisted Review", "< 1 Day", delta="Flagged-case review", delta_color="inverse")
            st.write("CGIF structures receipts, matches policies, classifies risk, and routes only Yellow / Red cases to finance.")
    else:
        st.markdown("### Legacy PDM Process vs. CGIF Framework Simulation")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Legacy Process", "5-10 Days", delta="Detection Lag")
            st.write("Manual monthly audit cycles relying on email approvals and spreadsheet consolidation.")
        with c2:
            st.metric("CGIF Framework", "< 1 Day", delta="Detection Lag", delta_color="inverse")
            st.write("Event-driven validation at the moment of change release.")

with tab3:
    st.title("📄 Scenario Design")

    if scenario == "LDCT Screening Readiness":
        st.markdown(
            """
            ### CGIF MVP: LDCT Screening Readiness & Drop-off Classification

            **Product thesis:** CGIF helps healthcare teams answer:

            > Why did an apparently eligible patient fail to complete LDCT lung cancer screening?

            #### What CGIF classifies

            | Classification | Meaning |
            |---|---|
            | Clinically ineligible | Patient does not meet screening criteria based on available evidence |
            | Evidence missing | Eligibility may be true, but required evidence is absent |
            | Documentation gap | Patient appears eligible, but required documentation is missing |
            | Workflow breakdown | Order, referral, scheduling, or follow-up step failed |
            | Payer friction | Authorization or coverage issue blocks progress |
            | Access barrier | Transportation, language, cost, digital access, or patient-facing barrier |
            | Needs human review | Evidence is ambiguous, conflicting, or subjective |

            #### Demo focus

            Show raw workflow data: `LDCT screening not completed`.

            Then show CGIF output: `Patient appears eligible, but screening was blocked by missing shared decision-making documentation.`

            That case should not be counted as clinical ineligibility. It is a documentation / workflow failure.
            """
        )
    elif scenario == "Travel Expense Reimbursement":
        st.markdown(
            """
            ### Travel Expense Implementation Scenario

            CGIF structures receipts, policy rules, exceptions, and reviewer rationale so reimbursement decisions become faster, more consistent, and easier to audit.
            """
        )
    else:
        st.markdown(
            """
            ### PDM / Engineering Change Governance Scenario

            CGIF checks engineering change data against governance rules before risky changes move forward.
            """
        )
