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


# -----------------------------------------------------------------------------
# PDM / Engineering Governance Logic
# -----------------------------------------------------------------------------
def evaluate_pdm_change(data):
    """
    Simulates a rule-based engine that evaluates engineering change data against
    PDM governance policies. Returns a list of audit results with evidence.
    """
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
def _safe_date(date_text):
    return datetime.strptime(date_text, "%Y-%m-%d").date()


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
    """
    Evaluates travel expense reimbursement data against travel policy.
    The engine does not directly reject the case. It produces Green / Yellow / Red
    risk classification and an auditable explanation trail.
    """
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

        # Rule 1: Required receipt
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

        # Rule 2: Duplicate reimbursement
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

        # Rule 3: Travel date alignment
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

        # Rule 4: Manager preapproval scope
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

        # Rule 5: Meal limit
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

        # Rule 6: Hotel city limit
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

    # Rule 7: Budget pressure at case level
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


def build_audit_log(scenario_name, data, audit_results, final_status):
    return {
        "timestamp": datetime.now().isoformat(),
        "scenario": scenario_name,
        "case_id": data.get("case_id") or data.get("ecn_id"),
        "final_status": final_status,
        "evaluations": audit_results,
        "review_model": "Human-in-the-loop review for flagged cases",
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
            "Travel Expense Reimbursement"
        ]
    )

    if scenario == "Travel Expense Reimbursement":
        default_json = TRAVEL_EXPENSE_DEFAULT_JSON
        text_label = "Travel Expense Case Data (JSON)"
        button_label = "Run Travel Expense Audit"
    else:
        default_json = PDM_DEFAULT_JSON
        text_label = "Engineering Change Data (JSON)"
        button_label = "Run Governance Audit"

    input_text = st.text_area(text_label, value=json.dumps(default_json, indent=4), height=420)
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

            if scenario == "Travel Expense Reimbursement":
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

    if scenario == "Travel Expense Reimbursement":
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

    if scenario == "Travel Expense Reimbursement":
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
