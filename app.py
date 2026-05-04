import streamlit as st
import pandas as pd
import json
from datetime import datetime

# --- Page Setup ---
st.set_page_config(page_title="CGIF Dashboard", layout="wide", page_icon="🛡️")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .scenario-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Scenario Defaults
# -----------------------------------------------------------------------------
PDM_DEFAULT_JSON = {
    "ecn_id": "ECO-2026-992",
    "safety_critical": True,
    "safety_validation_report": None,
    "production_freeze_active": True,
    "change_type": "GEOMETRY_ADJUSTMENT",
    "cost_delta": 4500.00
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
            "manager_exception_attached": False
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
            "manager_exception_attached": False
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
            "manager_exception_attached": False
        }
    ]
}

HEALTHCARE_REFERRAL_DEFAULT_JSON = {
    "case_id": "LCS-CASE-2026-0001",
    "patient_id": "PT-1048",
    "service_requested": "Lung cancer screening / referral readiness",
    "clinical_eligibility_status_from_record": "appears_eligible",
    "age_documented": True,
    "smoking_history_documented": True,
    "provider_order_present": True,
    "shared_decision_making_note_present": False,
    "prior_auth_status": "approved",
    "transportation_language_barrier_assessed": True,
    "transportation_barrier_present": False,
    "language_barrier_present": False,
    "referral_sent": True,
    "service_completed": False,
    "clinical_note_quality": "clear",
    "smoking_history_clarity": "clear",
    "conflicting_documentation": False,
    "subjective_medical_necessity_language": False,
    "follow_up_reason_present": True,
    "reviewer_note": ""
}


# -----------------------------------------------------------------------------
# Shared Helpers
# -----------------------------------------------------------------------------
def _safe_date(date_text):
    return datetime.strptime(date_text, "%Y-%m-%d").date()


def _status_label(is_ready):
    return "Present" if is_ready else "Missing"


# -----------------------------------------------------------------------------
# PDM / Engineering Governance Logic
# -----------------------------------------------------------------------------
def evaluate_pdm_change(data):
    audit_trail = []

    safety_check = {
        "rule": "SAFETY-001",
        "description": "Safety-Critical Validation",
        "status": "PASS",
        "severity": "CRITICAL",
        "details": "Ensuring safety-critical components have an attached validation report.",
        "evidence": f"Critical: {data.get('safety_critical')}, Report Found: {data.get('safety_validation_report') is not None}",
        "recommendation": "Attach a validation report before releasing the engineering change."
    }
    if data.get("safety_critical") is True and data.get("safety_validation_report") is None:
        safety_check["status"] = "FAIL"
        audit_trail.append(safety_check)

    freeze_check = {
        "rule": "FREEZE-001",
        "description": "Manufacturing Change Control",
        "status": "PASS",
        "severity": "HIGH",
        "details": "Ensuring no geometry changes occur during active production freezes.",
        "evidence": f"Freeze: {data.get('production_freeze_active')}, Type: {data.get('change_type')}",
        "recommendation": "Route this change through an emergency repair or formal exception workflow."
    }
    if data.get("production_freeze_active") is True and data.get("change_type") != "EMERGENCY_REPAIR":
        freeze_check["status"] = "FAIL"
        audit_trail.append(freeze_check)

    finance_check = {
        "rule": "FINANCE-001",
        "description": "Financial Data Validation",
        "status": "PASS",
        "severity": "MEDIUM",
        "details": "Preventing invalid cost data entries.",
        "evidence": f"Cost Delta: {data.get('cost_delta')}",
        "recommendation": "Correct the cost delta before approval."
    }
    if data.get("cost_delta", 0) < 0:
        finance_check["status"] = "FAIL"
        audit_trail.append(finance_check)

    return audit_trail


def classify_pdm_risk(audit_results):
    if any(r["severity"] == "CRITICAL" for r in audit_results):
        return "BLOCKED", "red"
    if audit_results:
        return "REVIEW REQUIRED", "orange"
    return "APPROVED", "green"


# -----------------------------------------------------------------------------
# Travel Expense Governance Logic
# -----------------------------------------------------------------------------
def _expense_dict_to_rows(expenses):
    rows = []
    for exp in expenses:
        rows.append({
            "Expense ID": exp.get("expense_id"),
            "Category": exp.get("category"),
            "Merchant": exp.get("merchant"),
            "Amount": exp.get("amount"),
            "Currency": exp.get("currency"),
            "Date": exp.get("expense_date"),
            "Receipt": "Attached" if exp.get("receipt_attached") else "Missing",
            "Exception": "Attached" if exp.get("manager_exception_attached") else "None"
        })
    return rows


def evaluate_travel_expense_case(data):
    audit_trail = []
    expenses = data.get("expenses", [])
    travel_start = _safe_date(data.get("travel_start_date"))
    travel_end = _safe_date(data.get("travel_end_date"))
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
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-RECEIPT-001",
                "description": "Required Receipt Validation",
                "status": "FAIL",
                "severity": "HIGH",
                "risk_class": "Red",
                "details": "Required receipt is missing for this reimbursement line.",
                "evidence": f"Expense {expense_id} has receipt_attached={exp.get('receipt_attached')}",
                "recommendation": "Request the missing receipt before payment approval."
            })

        if receipt_hash in reimbursed_hashes or receipt_hash in current_hashes:
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-DUPLICATE-001",
                "description": "Duplicate Receipt Detection",
                "status": "FAIL",
                "severity": "CRITICAL",
                "risk_class": "Red",
                "details": "The same receipt appears to have been submitted before or appears more than once in this case.",
                "evidence": f"Receipt hash: {receipt_hash}",
                "recommendation": "Block auto-approval and route to finance review."
            })
        if receipt_hash:
            current_hashes.add(receipt_hash)

        expense_date = _safe_date(exp.get("expense_date"))
        if expense_date < travel_start or expense_date > travel_end:
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-DATE-001",
                "description": "Travel Period Validation",
                "status": "FAIL",
                "severity": "HIGH",
                "risk_class": "Red",
                "details": "Expense date falls outside the approved travel period.",
                "evidence": f"Expense date: {expense_date}; Travel window: {travel_start} to {travel_end}",
                "recommendation": "Require explanation or manager exception before approval."
            })

        if category not in approved_scope:
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-SCOPE-001",
                "description": "Manager Preapproval Scope",
                "status": "FAIL",
                "severity": "MEDIUM",
                "risk_class": "Yellow",
                "details": "Expense category is outside the manager's pre-approved scope.",
                "evidence": f"Category: {category}; Approved scope: {sorted(approved_scope)}",
                "recommendation": "Ask manager to confirm whether this category is allowed."
            })

        if category == "meal" and daily_meal_limit and amount > daily_meal_limit and not exception_attached:
            over_pct = ((amount - daily_meal_limit) / daily_meal_limit) * 100
            risk_class = "Red" if over_pct > 35 else "Yellow"
            severity = "HIGH" if risk_class == "Red" else "MEDIUM"
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-MEAL-001",
                "description": "Daily Meal Limit",
                "status": "FAIL",
                "severity": severity,
                "risk_class": risk_class,
                "details": "Meal expense exceeds the daily meal limit and no manager exception was attached.",
                "evidence": f"Meal amount: ${amount:.2f}; Limit: ${daily_meal_limit:.2f}; Over limit: {over_pct:.1f}%",
                "recommendation": "Route to finance reviewer for confirmation or request exception approval."
            })

        if category == "hotel" and city_hotel_limit and amount > city_hotel_limit and not exception_attached:
            over_pct = ((amount - city_hotel_limit) / city_hotel_limit) * 100
            risk_class = "Red" if over_pct > 25 else "Yellow"
            severity = "HIGH" if risk_class == "Red" else "MEDIUM"
            audit_trail.append({
                "expense_id": expense_id,
                "rule": "TRAVEL-HOTEL-001",
                "description": "City Hotel Limit",
                "status": "FAIL",
                "severity": severity,
                "risk_class": risk_class,
                "details": "Hotel expense exceeds the city-specific hotel limit and no exception approval was attached.",
                "evidence": f"Hotel amount: ${amount:.2f}; City limit: ${city_hotel_limit:.2f}; Over limit: {over_pct:.1f}%",
                "recommendation": "Finance reviewer should verify conference rate, city rate, or manager exception."
            })

    total_expense = sum(float(exp.get("amount", 0)) for exp in expenses)
    budget_remaining = float(data.get("department_budget_remaining", 0))
    if budget_remaining and total_expense > budget_remaining:
        audit_trail.append({
            "expense_id": "CASE-LEVEL",
            "rule": "TRAVEL-BUDGET-001",
            "description": "Department Budget Check",
            "status": "FAIL",
            "severity": "HIGH",
            "risk_class": "Red",
            "details": "Total reimbursement exceeds the remaining department or project budget.",
            "evidence": f"Total expense: ${total_expense:.2f}; Budget remaining: ${budget_remaining:.2f}",
            "recommendation": "Require budget owner approval before payment."
        })

    return audit_trail


def classify_travel_risk(audit_results):
    if any(r.get("risk_class") == "Red" for r in audit_results):
        return "Red", "red", "High-risk issue; finance review required before payment."
    if any(r.get("risk_class") == "Yellow" for r in audit_results):
        return "Yellow", "orange", "Minor exception; human confirmation recommended."
    return "Green", "green", "Compliant with policy; eligible for auto-approval."


# -----------------------------------------------------------------------------
# Healthcare Referral Readiness Logic
# -----------------------------------------------------------------------------
def build_healthcare_checklist(data):
    return [
        {"Required Item": "Age", "Status": _status_label(data.get("age_documented") is True), "Why It Matters": "Eligibility evidence"},
        {"Required Item": "Smoking history", "Status": _status_label(data.get("smoking_history_documented") is True), "Why It Matters": "Eligibility evidence"},
        {"Required Item": "Provider order", "Status": _status_label(data.get("provider_order_present") is True), "Why It Matters": "Workflow readiness"},
        {"Required Item": "Shared decision-making note", "Status": _status_label(data.get("shared_decision_making_note_present") is True), "Why It Matters": "Documentation readiness"},
        {"Required Item": "Prior auth status", "Status": _status_label(data.get("prior_auth_status") not in [None, "", "missing"]), "Why It Matters": "Payer readiness"},
        {"Required Item": "Transportation/language barrier assessment", "Status": _status_label(data.get("transportation_language_barrier_assessed") is True), "Why It Matters": "Access readiness"}
    ]


def evaluate_healthcare_referral_case(data):
    """
    Evaluates referral readiness and barrier type. This is workflow decision support only.
    It does not make final clinical decisions.
    """
    checklist = build_healthcare_checklist(data)
    evidence_present = [x["Required Item"] for x in checklist if x["Status"] == "Present"]
    evidence_missing = [x["Required Item"] for x in checklist if x["Status"] == "Missing"]

    ambiguity_signals = []
    if data.get("clinical_note_quality") == "vague":
        ambiguity_signals.append("vague clinical note")
    if data.get("smoking_history_clarity") == "unclear":
        ambiguity_signals.append("unclear smoking history")
    if data.get("conflicting_documentation") is True:
        ambiguity_signals.append("conflicting documentation")
    if data.get("subjective_medical_necessity_language") is True:
        ambiguity_signals.append("subjective medical necessity language")
    if data.get("follow_up_reason_present") is False and data.get("service_completed") is False:
        ambiguity_signals.append("missing follow-up reason")

    clinical_status = data.get("clinical_eligibility_status_from_record", "unknown")
    prior_auth_status = data.get("prior_auth_status")

    if ambiguity_signals:
        final_status = "Needs Human Review"
        color = "orange"
        barrier_category = "Needs human review"
        recommended_action = "A human reviewer should resolve the ambiguity before the case is classified."
        explanation = "This classification was made because the record contains ambiguity: " + ", ".join(ambiguity_signals) + "."
    elif clinical_status == "not_eligible":
        final_status = "Patient Does Not Appear Eligible From Record"
        color = "red"
        barrier_category = "Clinical ineligibility"
        recommended_action = "Route to clinician or clinical operations reviewer to confirm whether the requested workflow is appropriate."
        explanation = "This classification was made because the available record indicates the patient does not qualify for this workflow."
    elif clinical_status == "unknown" or "Age" in evidence_missing or "Smoking history" in evidence_missing:
        final_status = "Insufficient Evidence"
        color = "orange"
        barrier_category = "Insufficient evidence"
        recommended_action = "Collect missing eligibility evidence before deciding whether the referral is ready."
        explanation = "This classification was made because required evidence is missing: " + ", ".join(evidence_missing) + "."
    elif "Provider order" in evidence_missing or "Shared decision-making note" in evidence_missing:
        final_status = "Appears Eligible but Documentation Gap"
        color = "orange"
        barrier_category = "Documentation gap"
        recommended_action = "Request the missing order or documentation before routing the case downstream."
        explanation = "This classification was made because eligibility evidence is present, but documentation is missing: " + ", ".join(evidence_missing) + "."
    elif prior_auth_status in ["denied", "pending", "delayed", "missing"]:
        final_status = "Appears Eligible but Payer Blocked/Delayed"
        color = "orange"
        barrier_category = "Payer friction"
        recommended_action = "Review payer requirements or prior authorization status before scheduling completion."
        explanation = f"This classification was made because the case appears eligible, but prior auth status is `{prior_auth_status}`."
    elif data.get("transportation_barrier_present") is True or data.get("language_barrier_present") is True:
        final_status = "Appears Eligible but Access Barrier"
        color = "orange"
        barrier_category = "Access barrier"
        recommended_action = "Route to care coordination for access support."
        active_barriers = []
        if data.get("transportation_barrier_present") is True:
            active_barriers.append("transportation barrier")
        if data.get("language_barrier_present") is True:
            active_barriers.append("language barrier")
        explanation = "This classification was made because the case appears eligible, but access barriers were documented: " + ", ".join(active_barriers) + "."
    elif data.get("referral_sent") is True and data.get("service_completed") is False:
        final_status = "Appears Eligible but Workflow Breakdown"
        color = "orange"
        barrier_category = "Workflow breakdown"
        recommended_action = "Check referral handoff, scheduling status, and downstream completion owner."
        explanation = "This classification was made because referral was sent, but the service was not completed."
    else:
        final_status = "Referral Ready"
        color = "green"
        barrier_category = "Ready / no barrier detected"
        recommended_action = "Proceed with the normal scheduling or completion workflow."
        explanation = "This classification was made because required evidence, documentation, payer readiness, and access readiness are present."

    flags = []
    if ambiguity_signals:
        flags.append({
            "rule": "HEALTH-HUMAN-REVIEW-001",
            "description": "Human Review Required",
            "severity": "HIGH",
            "barrier_category": "Needs human review",
            "evidence": ", ".join(ambiguity_signals),
            "recommendation": recommended_action
        })
    if evidence_missing:
        flags.append({
            "rule": "HEALTH-EVIDENCE-001",
            "description": "Missing Evidence Checklist",
            "severity": "MEDIUM",
            "barrier_category": barrier_category,
            "evidence": "Missing items: " + ", ".join(evidence_missing),
            "recommendation": "Complete missing evidence before final review."
        })

    decision_receipt = {
        "case_id": data.get("case_id"),
        "service_requested": data.get("service_requested"),
        "policy_workflow_criteria_checked": [x["Required Item"] for x in checklist],
        "evidence_present": evidence_present,
        "evidence_missing": evidence_missing,
        "barrier_category": barrier_category,
        "recommended_next_action": recommended_action,
        "classification_explanation": explanation,
        "reviewer_note": data.get("reviewer_note", "")
    }

    return {
        "final_status": final_status,
        "color": color,
        "barrier_category": barrier_category,
        "recommended_action": recommended_action,
        "explanation": explanation,
        "checklist": checklist,
        "evidence_present": evidence_present,
        "evidence_missing": evidence_missing,
        "flags": flags,
        "decision_receipt": decision_receipt
    }


# -----------------------------------------------------------------------------
# Audit Log
# -----------------------------------------------------------------------------
def build_audit_log(scenario_name, data, audit_results, final_status):
    return {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario_name,
        "case_id": data.get("case_id") or data.get("ecn_id"),
        "final_status": final_status,
        "evaluations": audit_results,
        "review_model": "Human-in-the-loop review for flagged or ambiguous cases",
        "audit_principle": "Every decision should preserve policy, evidence, exception, reviewer, and rationale."
    }


# -----------------------------------------------------------------------------
# Sidebar Inputs
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Data Inputs")

    scenario = st.selectbox(
        "Select CGIF Scenario",
        [
            "PDM / Engineering Change Governance",
            "Travel Expense Reimbursement",
            "Healthcare Referral Readiness"
        ]
    )

    if scenario == "Travel Expense Reimbursement":
        default_json = TRAVEL_EXPENSE_DEFAULT_JSON
        text_label = "Travel Expense Case Data (JSON)"
        button_label = "Run Travel Expense Audit"
    elif scenario == "Healthcare Referral Readiness":
        default_json = HEALTHCARE_REFERRAL_DEFAULT_JSON
        text_label = "Healthcare Referral Readiness Case Data (JSON)"
        button_label = "Run Referral Readiness Check"
    else:
        default_json = PDM_DEFAULT_JSON
        text_label = "Engineering Change Data (JSON)"
        button_label = "Run Governance Audit"

    input_text = st.text_area(text_label, value=json.dumps(default_json, indent=4), height=440)
    run_btn = st.button(button_label, type="primary")


# -----------------------------------------------------------------------------
# Tab Layout
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🚀 Governance Engine",
    "📊 Impact Simulation",
    "📄 Scenario Design"
])


# -----------------------------------------------------------------------------
# Tab 1: Governance Engine
# -----------------------------------------------------------------------------
with tab1:
    st.title("🛡️ CGIF Governance Intelligence Engine")
    st.caption("Policy-to-Decision intelligence for structured, explainable, and auditable workflow decisions.")

    if run_btn:
        try:
            data = json.loads(input_text)

            if scenario == "Healthcare Referral Readiness":
                result = evaluate_healthcare_referral_case(data)
                st.subheader(f"Case Classification: :{result['color']}[{result['final_status']}]")
                st.write(result["explanation"])

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Service", "Lung Screening")
                m2.metric("Barrier Category", result["barrier_category"])
                m3.metric("Evidence Present", len(result["evidence_present"]))
                m4.metric("Evidence Missing", len(result["evidence_missing"]))

                st.markdown("### Missing Evidence Checklist")
                st.dataframe(pd.DataFrame(result["checklist"]), use_container_width=True)

                st.markdown("### What should a human review next?")
                st.warning(result["recommended_action"])

                if result["flags"]:
                    st.markdown("### Review Flags")
                    for res in result["flags"]:
                        with st.container():
                            st.markdown(f"""
                            **Rule:** `{res['rule']}` | **Severity:** `{res['severity']}`  
                            - **Intent:** {res['description']}
                            - **Evidence:** `{res['evidence']}`
                            - **Recommended Action:** {res['recommendation']}
                            """)
                            st.divider()

                with st.expander("🧾 View Decision Receipt"):
                    st.json(result["decision_receipt"])

                with st.expander("📄 View Immutable Audit Log (JSON)"):
                    st.json(build_audit_log(scenario, data, result["flags"], result["final_status"]))

                st.info("Clinical safety note: this demo provides workflow and evidence-readiness support only. It does not make final clinical decisions.")

            elif scenario == "Travel Expense Reimbursement":
                audit_results = evaluate_travel_expense_case(data)
                final_status, status_color, status_explanation = classify_travel_risk(audit_results)

                st.subheader(f"Risk Classification: :{status_color}[{final_status}]")
                st.write(status_explanation)

                total_amount = sum(float(exp.get("amount", 0)) for exp in data.get("expenses", []))
                flagged_count = len(set(r.get("expense_id") for r in audit_results))

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Claimed", f"${total_amount:,.2f}")
                m2.metric("Expense Lines", len(data.get("expenses", [])))
                m3.metric("Flagged Items", flagged_count)
                m4.metric("Final Class", final_status)

                st.markdown("### Submitted Expense Lines")
                st.dataframe(pd.DataFrame(_expense_dict_to_rows(data.get("expenses", []))), use_container_width=True)

                if audit_results:
                    st.info("The engine identified the following policy exceptions and review reasons:")
                    for res in audit_results:
                        with st.container():
                            st.markdown(f"""
                            **Expense:** `{res['expense_id']}`  
                            **Rule:** `{res['rule']}` | **Risk:** `{res['risk_class']}` | **Severity:** `{res['severity']}`

                            - **Policy Intent:** {res['description']}
                            - **Reasoning:** {res['details']}
                            - **Audit Evidence:** `{res['evidence']}`
                            - **Recommended Action:** {res['recommendation']}
                            """)
                            st.divider()
                else:
                    st.success("✅ All travel expense checks passed. This case is eligible for auto-approval.")

                with st.expander("📄 View Immutable Audit Log (JSON)"):
                    st.json(build_audit_log(scenario, data, audit_results, final_status))

            else:
                audit_results = evaluate_pdm_change(data)
                final_status, status_color = classify_pdm_risk(audit_results)

                st.subheader(f"Evaluation Status: :{status_color}[{final_status}]")

                if audit_results:
                    st.info("The engine identified the following policy violations based on the current data state:")
                    for res in audit_results:
                        with st.container():
                            st.markdown(f"""
                            **Rule:** `{res['rule']}` | **Severity:** `{res['severity']}`

                            - **Intent:** {res['description']}
                            - **Reasoning:** {res['details']}
                            - **Audit Evidence:** `{res['evidence']}`
                            - **Recommended Action:** {res['recommendation']}
                            """)
                            st.divider()
                else:
                    st.success("✅ All governance checks passed. The data footprint satisfies all configured business rules.")

                with st.expander("📄 View Immutable Audit Log (JSON)"):
                    st.json(build_audit_log(scenario, data, audit_results, final_status))

        except Exception as e:
            st.error(f"JSON Parsing or Evaluation Error: {e}")
    else:
        st.info("👈 Select a scenario, modify the JSON in the sidebar, and run the CGIF audit.")


# -----------------------------------------------------------------------------
# Tab 2: Impact Simulation
# -----------------------------------------------------------------------------
with tab2:
    st.title("📊 Operational Performance Impact")

    if scenario == "Healthcare Referral Readiness":
        st.markdown("### Manual Referral Follow-Up vs. CGIF Referral Readiness")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Legacy Review", "Days to Weeks", delta="Manual chart chasing")
            st.write("Staff manually inspect notes, orders, authorization status, scheduling status, and patient access barriers.")
        with c2:
            st.metric("CGIF-Assisted Review", "Minutes", delta="Structured barrier classification", delta_color="inverse")
            st.write("CGIF separates ineligibility evidence, documentation gaps, payer friction, access barriers, workflow breakdowns, and insufficient evidence.")

        st.markdown("---")
        st.subheader("Structured Reasons Behind Non-Completion")
        chart_data = pd.DataFrame(
            {"Cases": [18, 24, 16, 12, 9, 21]},
            index=[
                "Clinical ineligibility",
                "Documentation gap",
                "Payer friction",
                "Access barrier",
                "Workflow breakdown",
                "Insufficient evidence"
            ]
        )
        st.bar_chart(chart_data)

        st.success("Research framing: CGIF helps answer whether the patient did not receive care because they did not need it, or because the system failed to deliver it.")

    elif scenario == "Travel Expense Reimbursement":
        st.markdown("### Legacy Travel Reimbursement vs. CGIF Review Flow")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Legacy Finance Review", "3-5 Days", delta="Manual line-by-line review")
            st.write("Finance staff manually inspect receipts, dates, policy limits, exceptions, and duplicate submissions.")
        with c2:
            st.metric("CGIF-Assisted Review", "< 1 Day", delta="Flagged-case review", delta_color="inverse")
            st.write("CGIF structures receipts, matches policies, classifies risk, and routes only Yellow / Red cases to finance.")

        st.markdown("---")
        st.subheader("Estimated Days to Detect Policy Exceptions")
        chart_data = pd.DataFrame({"Days": [4.0, 0.5]}, index=["Legacy Manual Review", "CGIF-Assisted Review"])
        st.bar_chart(chart_data)

        st.success("CGIF does not remove finance reviewers. It focuses them on exceptions while preserving policy evidence and audit rationale.")

    else:
        st.markdown("### Legacy PDM Process vs. CGIF Framework Simulation")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Legacy Process", "5-10 Days", delta="Detection Lag")
            st.write("Manual monthly audit cycles relying on email approvals and spreadsheet consolidation.")
        with c2:
            st.metric("CGIF Framework", "< 1 Day", delta="Detection Lag", delta_color="inverse")
            st.write("Event-driven, automated validation at the moment of change release.")

        st.markdown("---")
        st.subheader("Performance Comparison: Days to Detect")
        chart_data = pd.DataFrame({"Days": [7.5, 0.5]}, index=["Legacy Manual Process", "CGIF Framework"])
        st.bar_chart(chart_data)

        st.success("By automating governance gates, CGIF reduces time-to-detection for non-compliant changes by over 90%.")


# -----------------------------------------------------------------------------
# Tab 3: Scenario Design
# -----------------------------------------------------------------------------
with tab3:
    st.title("📄 Scenario Design")

    if scenario == "Healthcare Referral Readiness":
        st.markdown("""
        ### Healthcare Referral Readiness Scenario

        **First use case:** Lung cancer screening / referral readiness.

        **Business focus:** A patient appears eligible for a service, but the service is delayed, denied, or not completed.

        #### Core Value
        CGIF separates different failure reasons instead of collapsing everything into a vague "not completed" outcome:

        | Situation | Meaning |
        |---|---|
        | Patient does not qualify | Clinical ineligibility |
        | Patient qualifies but note is incomplete | Documentation gap |
        | Patient qualifies but payer blocks/delays | Payer friction |
        | Patient qualifies but cannot access service | Access barrier |
        | Order/referral breaks downstream | Workflow breakdown |
        | Not enough information | Insufficient evidence |

        #### Product Boundary
        CGIF does **not** replace clinicians and does **not** make final clinical decisions. It answers:

        ```text
        What is missing, what may be blocking the case, and what should a human review next?
        ```

        #### MVP Success Criteria
        The MVP succeeds if one sample case can clearly output one of the following:

        - Patient appears clinically eligible, but screening is blocked because shared decision-making documentation is missing.
        - Patient appears eligible, but service was not completed due to a transportation barrier.
        - Patient is not clinically eligible based on available evidence.

        #### Primary Users
        1. Clinical operations staff — reduce rework and delays.
        2. Care coordination / referral staff — identify what blocks completion.
        3. Health services researchers — study structured reasons behind utilization gaps.
        4. Compliance / audit reviewers — preserve defensible explanation trails.
        """)
    elif scenario == "Travel Expense Reimbursement":
        st.markdown("""
        ### Travel Expense Implementation Scenario

        **Positioning:** CGIF / P2D does not replace finance review. It structures receipts, policy rules, exceptions,
        and reviewer rationale so reimbursement decisions become faster, more consistent, and easier to audit.

        #### Workflow
        1. **Submission Stage** — Employee submits receipts, travel purpose, date, location, and project or department budget.
        2. **Policy Matching Stage** — CGIF compares each expense against travel policy rules.
        3. **Risk Classification Stage** — Each case is classified as Green, Yellow, or Red.
        4. **Human Review Stage** — Finance reviews only Yellow / Red cases with clear explanations.
        5. **Payment / Audit Stage** — Policy, evidence, exception, reviewer, and rationale are saved for audit.

        #### Example Rule
        ```text
        IF meal expense > daily limit
        AND no manager exception attached
        THEN flag for review
        ```

        #### Example Explanation
        ```text
        This hotel expense exceeds the city limit by 18% and no exception approval was attached.
        ```
        """)
    else:
        st.markdown("""
        ### PDM / Engineering Change Governance Scenario

        **Positioning:** CGIF checks engineering change data against governance rules before risky changes move forward.

        #### Workflow
        1. Engineering change data is submitted.
        2. CGIF validates safety-critical evidence, production freeze rules, and financial data quality.
        3. Failed rules generate an explainable audit trail.
        4. Reviewers receive clear policy reasons and recommended next actions.
        5. The immutable audit log preserves the decision trail.
        """)
