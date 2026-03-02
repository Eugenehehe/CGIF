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
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- Governance Logic Core ---
def evaluate_detailed(data):
    """
    Simulates a rule-based engine that evaluates data against compliance policies.
    Returns a list of audit results with evidence.
    """
    audit_trail = []
    
    # Rule 1: Safety Critical Validation
    safety_check = {
        "rule": "SAFETY-001",
        "description": "Safety-Critical Validation",
        "status": "PASS",
        "severity": "CRITICAL",
        "details": "Ensuring safety-critical components have an attached validation report.",
        "evidence": f"Critical: {data.get('safety_critical')}, Report Found: {data.get('safety_validation_report') is not None}"
    }
    if data.get("safety_critical") is True and data.get("safety_validation_report") is None:
        safety_check["status"] = "FAIL"
        audit_trail.append(safety_check)
    
    # Rule 2: Production Freeze
    freeze_check = {
        "rule": "FREEZE-001",
        "description": "Manufacturing Change Control",
        "status": "PASS",
        "severity": "HIGH",
        "details": "Ensuring no geometry changes occur during active production freezes.",
        "evidence": f"Freeze: {data.get('production_freeze_active')}, Type: {data.get('change_type')}"
    }
    if data.get("production_freeze_active") is True and data.get("change_type") != "EMERGENCY_REPAIR":
        freeze_check["status"] = "FAIL"
        audit_trail.append(freeze_check)
        
    # Rule 3: Data Integrity
    finance_check = {
        "rule": "FINANCE-001",
        "description": "Financial Data Validation",
        "status": "PASS",
        "severity": "MEDIUM",
        "details": "Preventing invalid cost data entries.",
        "evidence": f"Cost Delta: {data.get('cost_delta')}"
    }
    if data.get("cost_delta", 0) < 0:
        finance_check["status"] = "FAIL"
        audit_trail.append(finance_check)
        
    return audit_trail

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("⚙️ Data Inputs")
    default_json = {
        "ecn_id": "ECO-2026-992",
        "safety_critical": True,
        "safety_validation_report": None,
        "production_freeze_active": True,
        "change_type": "GEOMETRY_ADJUSTMENT",
        "cost_delta": 4500.00
    }
    input_text = st.text_area("Engineering Change Data (JSON)", value=json.dumps(default_json, indent=4), height=300)
    run_btn = st.button("Run Governance Audit", type="primary")

# --- Tab Layout ---
tab1, tab2 = st.tabs(["🚀 Governance Engine", "📊 Impact Simulation"])

# --- Tab 1: Governance Engine ---
with tab1:
    st.title("🛡️ Governance Intelligence Engine")
    
    if run_btn:
        try:
            data = json.loads(input_text)
            audit_results = evaluate_detailed(data)
            
            # Dashboard Metrics
            status_color = "red" if any(r['status'] == "FAIL" for r in audit_results) else "green"
            st.subheader(f"Evaluation Status: :{status_color}[{ 'BLOCKED' if audit_results else 'APPROVED' }]")
            
            if audit_results:
                st.info("The engine identified the following policy violations based on the current data state:")
                for res in audit_results:
                    with st.container():
                        st.markdown(f"""
                        **Rule:** `{res['rule']}` | **Severity:** `{res['severity']}`
                        * **Intent:** {res['description']}
                        * **Reasoning:** {res['details']}
                        * **Audit Evidence:** `{res['evidence']}`
                        """)
                        st.divider()
                
                with st.expander("📄 View Immutable Audit Log (JSON)"):
                    st.json({"timestamp": datetime.now().isoformat(), "evaluations": audit_results})
            else:
                st.success("✅ All governance checks passed. The data footprint satisfies all configured business rules.")
                
        except Exception as e:
            st.error(f"JSON Parsing Error: {e}")
    else:
        st.info("👈 Modify the JSON data in the sidebar and click 'Run Governance Audit'.")

# --- Tab 2: Impact Simulation ---
with tab2:
    st.title("📊 Operational Performance Impact")
    st.markdown("### Legacy vs. CGIF Framework Simulation")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Legacy Process", "5-10 Days", delta="Detection Lag")
        st.write("Manual monthly audit cycles relying on email approvals and spreadsheet consolidation.")
    with c2:
        st.metric("CGIF Framework", "< 1 Day", delta="Detection Lag", delta_color="inverse")
        st.write("Event-driven, automated validation at the moment of change release.")

    st.markdown("---")
    st.subheader("Performance Comparison (Days to Detect)")
    chart_data = pd.DataFrame({'Days': [7.5, 0.5]}, index=['Legacy Manual Process', 'CGIF Framework'])
    st.bar_chart(chart_data)
    
    st.success("By automating governance gates, the framework reduces the 'time-to-detection' for non-compliant changes by over 90%.")