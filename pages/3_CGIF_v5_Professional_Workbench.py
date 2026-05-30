import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

APP_VERSION = "CGIF-v5.0-professional-workbench"
POLICY_PACK_ID = "CMS-LDCT-FFS-DEMO-2026.05"

st.set_page_config(
    page_title="CGIF Professional Workbench",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Professional visual system
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
:root {
  --cgif-bg: #f6f8fb;
  --cgif-card: #ffffff;
  --cgif-ink: #111827;
  --cgif-muted: #667085;
  --cgif-line: #e5e7eb;
  --cgif-navy: #0b1f3a;
  --cgif-blue: #2563eb;
  --cgif-blue-soft: #eff6ff;
  --cgif-green: #059669;
  --cgif-green-soft: #ecfdf5;
  --cgif-amber: #d97706;
  --cgif-amber-soft: #fffbeb;
  --cgif-red: #dc2626;
  --cgif-red-soft: #fef2f2;
}

.stApp { background: var(--cgif-bg); }
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1440px; }

h1, h2, h3 { color: var(--cgif-ink); letter-spacing: -0.02em; }
p, li, div { font-size: 0.97rem; }

[data-testid="stSidebar"] { background: #0b1f3a; }
[data-testid="stSidebar"] * { color: #f9fafb !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label { color: #dbeafe !important; }

.hero {
  background: linear-gradient(135deg, #0b1f3a 0%, #123b70 52%, #2563eb 100%);
  color: white;
  padding: 26px 30px;
  border-radius: 22px;
  margin-bottom: 18px;
  box-shadow: 0 18px 42px rgba(12, 31, 58, 0.20);
}
.hero h1 { color: white; margin: 0 0 8px 0; font-size: 2.15rem; }
.hero p { color: #dbeafe; margin: 0; max-width: 920px; line-height: 1.55; }
.hero-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; }
.product-badge {
  display: inline-block;
  background: rgba(255,255,255,0.14);
  border: 1px solid rgba(255,255,255,0.22);
  color: white;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 0.83rem;
  white-space: nowrap;
}

.card {
  background: var(--cgif-card);
  border: 1px solid var(--cgif-line);
  border-radius: 18px;
  padding: 18px 20px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  margin-bottom: 14px;
}
.card h3 { margin-top: 0; margin-bottom: 10px; font-size: 1.05rem; }
.card-subtle { color: var(--cgif-muted); font-size: 0.9rem; line-height: 1.45; }

.metric-card {
  background: white;
  border: 1px solid var(--cgif-line);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
  min-height: 122px;
}
.metric-label { color: var(--cgif-muted); font-size: 0.82rem; font-weight: 650; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { color: var(--cgif-ink); font-size: 2rem; font-weight: 800; margin-top: 8px; }
.metric-help { color: var(--cgif-muted); font-size: 0.86rem; margin-top: 4px; }

.pill { display:inline-flex; align-items:center; gap:6px; padding:5px 10px; border-radius:999px; font-size:0.82rem; font-weight:700; }
.pill-high { color:#991b1b; background:#fee2e2; border:1px solid #fecaca; }
.pill-medium { color:#92400e; background:#fef3c7; border:1px solid #fde68a; }
.pill-low { color:#065f46; background:#d1fae5; border:1px solid #a7f3d0; }
.pill-open { color:#1e40af; background:#dbeafe; border:1px solid #bfdbfe; }
.pill-closed { color:#065f46; background:#d1fae5; border:1px solid #a7f3d0; }
.pill-neutral { color:#374151; background:#f3f4f6; border:1px solid #e5e7eb; }

.section-title { font-size: 1rem; font-weight: 800; color: #111827; margin: 0 0 10px 0; }
.list-clean { margin: 0; padding-left: 18px; color:#374151; line-height:1.55; }

.notice-blue { border-left: 5px solid #2563eb; background:#eff6ff; color:#1e3a8a; padding:14px 16px; border-radius:12px; }
.notice-amber { border-left: 5px solid #d97706; background:#fffbeb; color:#92400e; padding:14px 16px; border-radius:12px; }
.notice-red { border-left: 5px solid #dc2626; background:#fef2f2; color:#991b1b; padding:14px 16px; border-radius:12px; }
.notice-green { border-left: 5px solid #059669; background:#ecfdf5; color:#065f46; padding:14px 16px; border-radius:12px; }

.case-header {
  background:white;
  border:1px solid var(--cgif-line);
  border-radius:20px;
  padding:18px 20px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  margin-bottom:14px;
}
.case-title { font-size:1.28rem; font-weight:800; color:#111827; margin-bottom:6px; }
.case-meta { color:#667085; font-size:0.9rem; }

.footer-boundary {
  margin-top: 18px;
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #991b1b;
  border-radius: 14px;
  padding: 14px 16px;
  font-size: 0.9rem;
}

[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }
.stButton>button { border-radius: 10px; font-weight: 700; }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Sample data
# -----------------------------------------------------------------------------
SAMPLE_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "FFS-LDCT-001",
        "service": "Low-dose CT lung cancer screening",
        "patient_group": "Medicare Fee-for-Service beneficiary",
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

ROLE_QUEUES = {
    "Executive view": [],
    "Chart Reviewer": ["Chart Review Intake", "Clinical Documentation Review"],
    "Coding Analyst": ["Coding & Revenue Cycle"],
    "Prior Auth Specialist": ["Prior Authorization"],
    "Care Coordinator": ["Care Coordination"],
    "Compliance Reviewer": ["Compliance Review"],
}

POLICY_PACK = {
    "policy_pack_id": POLICY_PACK_ID,
    "service": "Low-dose CT lung cancer screening",
    "version": "0.5-demo",
    "product_boundary": "Evidence review and routing only; not a final clinical, legal, coverage, fraud, or reimbursement decision system.",
    "guardrails": [
        "Do not infer patient refusal from claims-only service non-observation.",
        "Do not infer access barrier without documented care coordination or SDOH evidence.",
        "Do not infer provider failure without order/referral/scheduling evidence.",
        "Do not infer full clinical eligibility without chart-level evidence.",
        "Do not call a claim improper before coding and chart documentation review.",
    ],
}

# -----------------------------------------------------------------------------
# State and logic
# -----------------------------------------------------------------------------
def init_state() -> None:
    if "v5_cases" not in st.session_state:
        st.session_state.v5_cases = SAMPLE_CASES.copy()
    if "v5_reviews" not in st.session_state:
        st.session_state.v5_reviews = {}
    if "v5_active_case" not in st.session_state:
        st.session_state.v5_active_case = SAMPLE_CASES[0]["case_id"]


init_state()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y", "observed", "available", "present"}


def normalize_case(case: Dict[str, Any]) -> Dict[str, Any]:
    c = dict(case)
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
        c[field] = parse_bool(c.get(field, False))
    c.setdefault("case_id", f"CASE-{uuid.uuid4().hex[:8].upper()}")
    c.setdefault("service", "Policy-sensitive service")
    c.setdefault("patient_group", "Unspecified cohort")
    c.setdefault("source_reference", "manual_input")
    return c


def hash_case(case: Dict[str, Any]) -> str:
    raw = json.dumps(case, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:14]


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
    return int(round(sum(1 for field in fields if case.get(field)) / len(fields) * 100))


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
        missing.append("Care coordination / access-barrier note")
    return missing


def guardrails(case: Dict[str, Any]) -> List[str]:
    items = []
    if not case["claim_service_observed"]:
        items.extend([
            "Do not conclude patient refusal from claims-only non-observation.",
            "Do not conclude provider failure without order/referral evidence.",
        ])
    if not case["clinical_eligibility_evidence_available"]:
        items.append("Do not conclude full clinical eligibility without chart evidence.")
    if not case["scheduling_record_available"]:
        items.append("Do not conclude scheduling breakdown without scheduling/referral data.")
    if not case["care_coordination_note_available"] or not case["access_barrier_documented"]:
        items.append("Do not conclude transportation/language/cost barrier without documented access evidence.")
    if case["denial_or_nonpayment_observed"]:
        items.append("Do not label a claim improper before coding and documentation review.")
    return list(dict.fromkeys(items))


def route_case(raw: Dict[str, Any]) -> Dict[str, Any]:
    case = normalize_case(raw)
    payment = str(case.get("payment_status") or "").lower()
    auth = str(case.get("prior_authorization_status") or "").lower()

    if case["conflicting_signal"]:
        output, queue, owner, priority, risk = "Conflicting evidence", "Compliance Review", "Compliance reviewer", "High", 92
        action = "Escalate for manual reconciliation of claim, payer, and documentation signals."
    elif case["denial_or_nonpayment_observed"] or payment in {"denied", "rejected", "nonpayment"}:
        output, queue, owner, priority, risk = "Coding / payer support issue", "Coding & Revenue Cycle", "Coding analyst", "High", 84
        action = "Review claim code, diagnosis support, denial reason, payer rule, and chart documentation."
    elif auth in {"pending", "delayed", "denied"}:
        output, queue, owner, priority, risk = "Prior authorization friction", "Prior Authorization", "Prior auth specialist", "High", 78
        action = "Resolve payer authorization status or document why authorization is not required."
    elif case["access_barrier_documented"] and case["care_coordination_note_available"]:
        output, queue, owner, priority, risk = "Access barrier supported", "Care Coordination", "Care coordinator", "Medium", 67
        action = "Route to patient navigation and document follow-up outcome."
    elif case["ehr_order_available"] and not case["shared_decision_making_note_available"]:
        output, queue, owner, priority, risk = "Documentation gap", "Clinical Documentation Review", "Chart reviewer", "High", 74
        action = "Verify required documentation before treating the episode as ready or complete."
    elif not case["claim_service_observed"]:
        output, queue, owner, priority, risk = "Reason indeterminate", "Chart Review Intake", "EHR / chart review team", "Medium", 56
        action = "Pull EHR, scheduling, payer, and care coordination evidence before assigning a cause."
    else:
        output, queue, owner, priority, risk = "Service observed", "Sampling / No Immediate Exception", "Quality analyst", "Low", 20
        action = "No urgent exception. Use audit sampling or chart verification if required."

    known = ["Service claim observed" if case["claim_service_observed"] else "Service claim not observed"]
    if case.get("claim_code"):
        known.append(f"Claim code: {case['claim_code']}")
    if case["screening_related_visit_observed"]:
        known.append("Screening-related visit observed")
    if case["diagnosis_or_risk_code_support_present"]:
        known.append("Claims-level diagnosis/risk support observed")
    if case["denial_or_nonpayment_observed"]:
        known.append("Denial or nonpayment signal observed")
    if case["ehr_order_available"]:
        known.append("EHR order available")
    if case["access_barrier_documented"]:
        known.append(f"Access barrier documented: {case.get('access_barrier_type') or 'unspecified'}")

    return {
        "case": case,
        "case_id": case["case_id"],
        "service": case["service"],
        "output": output,
        "queue": queue,
        "owner": owner,
        "priority": priority,
        "risk": risk,
        "coverage": evidence_coverage(case),
        "known": known,
        "missing": missing_evidence(case),
        "guardrails": guardrails(case),
        "action": action,
        "source_hash": hash_case(case),
    }


def review_for(case_id: str) -> Dict[str, Any]:
    return st.session_state.v5_reviews.get(
        case_id,
        {"status": "Open", "decision": "Pending", "assigned_to": "Unassigned", "rationale": ""},
    )


def make_receipt(item: Dict[str, Any], role: str) -> Dict[str, Any]:
    return {
        "receipt_id": f"{item['case_id']}-{uuid.uuid4().hex[:8]}",
        "generated_at_utc": now_utc(),
        "app_version": APP_VERSION,
        "policy_pack_id": POLICY_PACK_ID,
        "generated_by_role": role,
        "case_id": item["case_id"],
        "service": item["service"],
        "primary_output": item["output"],
        "recommended_queue": item["queue"],
        "recommended_owner": item["owner"],
        "priority": item["priority"],
        "risk_score": item["risk"],
        "evidence_coverage": item["coverage"],
        "known_facts": item["known"],
        "missing_evidence": item["missing"],
        "do_not_conclude": item["guardrails"],
        "recommended_next_action": item["action"],
        "source_reference": item["case"].get("source_reference"),
        "source_hash": item["source_hash"],
        "reviewer_status": review_for(item["case_id"]),
        "boundary_statement": "CGIF supports evidence review and routing only. It is not a final clinical, coverage, fraud, reimbursement, or legal decision system.",
    }


def priority_pill(priority: str) -> str:
    css = {"High": "pill-high", "Medium": "pill-medium", "Low": "pill-low"}.get(priority, "pill-neutral")
    return f'<span class="pill {css}">{priority}</span>'


def status_pill(status: str) -> str:
    css = "pill-closed" if status == "Closed" else "pill-open" if status in {"Open", "In Review"} else "pill-neutral"
    return f'<span class="pill {css}">{status}</span>'


def metric_card(label: str, value: Any, help_text: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_uploaded(file) -> List[Dict[str, Any]]:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
        return df.where(pd.notnull(df), None).to_dict(orient="records")
    payload = json.loads(file.read().decode("utf-8"))
    return payload if isinstance(payload, list) else [payload]

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ CGIF")
    st.markdown("Evidence Review Workbench")
    role = st.selectbox("Workspace view", list(ROLE_QUEUES.keys()))
    st.divider()
    uploaded = st.file_uploader("Load cases", type=["csv", "json"])
    if st.button("Load uploaded data", use_container_width=True):
        if uploaded is None:
            st.error("Upload CSV or JSON first.")
        else:
            try:
                st.session_state.v5_cases = [normalize_case(x) for x in load_uploaded(uploaded)]
                st.session_state.v5_reviews = {}
                st.success("Cases loaded.")
            except Exception as exc:
                st.error(f"Upload failed: {exc}")
    if st.button("Reset demo data", use_container_width=True):
        st.session_state.v5_cases = SAMPLE_CASES.copy()
        st.session_state.v5_reviews = {}
        st.success("Demo data restored.")
    st.divider()
    st.caption("v5 professional UI prototype")

# -----------------------------------------------------------------------------
# Main layout
# -----------------------------------------------------------------------------
routed = [route_case(case) for case in st.session_state.v5_cases]
rows = []
for item in routed:
    review = review_for(item["case_id"])
    rows.append(
        {
            "Case ID": item["case_id"],
            "Service": item["service"],
            "Output": item["output"],
            "Queue": item["queue"],
            "Owner": item["owner"],
            "Priority": item["priority"],
            "Risk": item["risk"],
            "Evidence %": item["coverage"],
            "Status": review["status"],
            "Decision": review["decision"],
        }
    )
summary = pd.DataFrame(rows)

if role != "Executive view":
    allowed = ROLE_QUEUES[role]
    view = summary[summary["Queue"].isin(allowed)].copy()
else:
    view = summary.copy()

st.markdown(
    """
    <div class="hero">
      <div class="hero-row">
        <div>
          <h1>CGIF Professional Workbench</h1>
          <p>Audit-ready evidence review and routing for policy-sensitive healthcare cases. CGIF shows what the data supports, what it cannot support, and who should review next.</p>
        </div>
        <div class="product-badge">v5 · Reviewer Workbench</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if view.empty:
    total, high, open_count, avg_cov = 0, 0, 0, 0
else:
    total = len(view)
    high = int((view["Priority"] == "High").sum())
    open_count = int((view["Status"] == "Open").sum())
    avg_cov = int(round(view["Evidence %"].mean()))

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("Cases in view", total, "Visible under current workspace")
with m2:
    metric_card("High priority", high, "Needs faster human review")
with m3:
    metric_card("Open cases", open_count, "Not yet closed by reviewer")
with m4:
    metric_card("Avg evidence", f"{avg_cov}%", "Core evidence coverage")

page_overview, page_queue, page_review, page_receipts, page_policy = st.tabs(
    ["Overview", "Work Queue", "Case Detail", "Audit Receipts", "Policy Pack"]
)

with page_overview:
    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown('<div class="card"><h3>Queue Distribution</h3>', unsafe_allow_html=True)
        if view.empty:
            st.info("No cases visible for this role.")
        else:
            queue_df = view.groupby(["Queue", "Priority"]).size().reset_index(name="Cases")
            st.dataframe(queue_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown(
            """
            <div class="card">
              <h3>Product Boundary</h3>
              <div class="notice-amber">
                CGIF is a reviewer workbench. It does not make final clinical, legal, coverage, fraud, or reimbursement decisions.
              </div>
              <p class="card-subtle">The product value is evidence boundary control: known facts, missing evidence, unsupported conclusions, and correct review routing.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with page_queue:
    st.markdown('<div class="case-header"><div class="case-title">Work Queue</div><div class="case-meta">Triage cases by queue, priority, risk, evidence coverage, and reviewer status.</div></div>', unsafe_allow_html=True)
    if view.empty:
        st.info("No cases visible for this role.")
    else:
        f1, f2, f3 = st.columns(3)
        with f1:
            priority_filter = st.multiselect("Priority", sorted(view["Priority"].unique()), default=sorted(view["Priority"].unique()))
        with f2:
            queue_filter = st.multiselect("Queue", sorted(view["Queue"].unique()), default=sorted(view["Queue"].unique()))
        with f3:
            status_filter = st.multiselect("Status", sorted(view["Status"].unique()), default=sorted(view["Status"].unique()))
        filtered = view[view["Priority"].isin(priority_filter) & view["Queue"].isin(queue_filter) & view["Status"].isin(status_filter)].copy()
        filtered = filtered.sort_values(["Risk", "Evidence %"], ascending=[False, True])
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        if not filtered.empty:
            selected = st.selectbox("Open case", filtered["Case ID"].tolist())
            if st.button("Open in Case Detail", type="primary"):
                st.session_state.v5_active_case = selected
                st.success(f"Opened {selected}. Switch to Case Detail.")

with page_review:
    available_ids = view["Case ID"].tolist() if not view.empty else summary["Case ID"].tolist()
    if not available_ids:
        st.info("No case available.")
    else:
        if st.session_state.v5_active_case not in available_ids:
            st.session_state.v5_active_case = available_ids[0]
        case_id = st.selectbox("Case", available_ids, index=available_ids.index(st.session_state.v5_active_case))
        st.session_state.v5_active_case = case_id
        item = next(x for x in routed if x["case_id"] == case_id)
        review = review_for(case_id)

        st.markdown(
            f"""
            <div class="case-header">
              <div class="case-title">{case_id} · {item['output']}</div>
              <div class="case-meta">{item['service']} · Queue: {item['queue']} · Owner: {item['owner']} · Source hash: {item['source_hash']}</div>
              <div style="margin-top:12px;">{priority_pill(item['priority'])} {status_pill(review['status'])} <span class="pill pill-neutral">Risk {item['risk']}</span> <span class="pill pill-neutral">Evidence {item['coverage']}%</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f'<div class="notice-blue"><b>Recommended next action:</b> {item["action"]}</div>', unsafe_allow_html=True)

        c_left, c_mid, c_right = st.columns(3)
        with c_left:
            st.markdown('<div class="card"><div class="section-title">What is known</div><ul class="list-clean">' + ''.join(f'<li>{x}</li>' for x in item["known"]) + '</ul></div>', unsafe_allow_html=True)
        with c_mid:
            st.markdown('<div class="card"><div class="section-title">Missing evidence</div><ul class="list-clean">' + ''.join(f'<li>{x}</li>' for x in item["missing"]) + '</ul></div>', unsafe_allow_html=True)
        with c_right:
            st.markdown('<div class="card"><div class="section-title">Do not conclude</div><ul class="list-clean">' + ''.join(f'<li>{x}</li>' for x in item["guardrails"]) + '</ul></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><h3>Reviewer Action</h3>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            decision = st.selectbox("Decision", ["Pending", "Agree with CGIF", "Override routing", "Need more evidence", "Escalate", "Exclude", "Close case"], index=0)
        with b:
            status = st.selectbox("Status", ["Open", "In Review", "Waiting for Evidence", "Escalated", "Closed"], index=["Open", "In Review", "Waiting for Evidence", "Escalated", "Closed"].index(review.get("status", "Open")) if review.get("status", "Open") in ["Open", "In Review", "Waiting for Evidence", "Escalated", "Closed"] else 0)
        with c:
            assigned_to = st.text_input("Assigned to", value=review.get("assigned_to", "Unassigned"))
        rationale = st.text_area("Reviewer rationale", value=review.get("rationale", ""), height=100)
        if st.button("Save review action", type="primary"):
            st.session_state.v5_reviews[case_id] = {
                "status": status,
                "decision": decision,
                "assigned_to": assigned_to,
                "rationale": rationale,
                "updated_at_utc": now_utc(),
                "updated_by_workspace": role,
            }
            st.success("Review action saved.")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Raw case evidence"):
            st.json(item["case"])

with page_receipts:
    st.markdown('<div class="case-header"><div class="case-title">Audit Receipts</div><div class="case-meta">Exportable evidence receipts with source hash, routing, reviewer status, guardrails, and boundary statement.</div></div>', unsafe_allow_html=True)
    receipts = [make_receipt(item, role) for item in routed]
    receipt_df = pd.DataFrame([
        {
            "Case ID": r["case_id"],
            "Output": r["primary_output"],
            "Queue": r["recommended_queue"],
            "Priority": r["priority"],
            "Reviewer status": r["reviewer_status"].get("status"),
            "Decision": r["reviewer_status"].get("decision"),
            "Evidence %": r["evidence_coverage"],
        }
        for r in receipts
    ])
    st.dataframe(receipt_df, use_container_width=True, hide_index=True)
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("Download audit receipts JSON", json.dumps(receipts, indent=2), "cgif_v5_audit_receipts.json", "application/json", use_container_width=True)
    with d2:
        st.download_button("Download work queue CSV", summary.to_csv(index=False).encode("utf-8"), "cgif_v5_work_queue.csv", "text/csv", use_container_width=True)

with page_policy:
    st.markdown('<div class="case-header"><div class="case-title">Policy Pack</div><div class="case-meta">Visible rule package: source layers, guardrails, and product boundary.</div></div>', unsafe_allow_html=True)
    st.json(POLICY_PACK)
    st.download_button("Download policy pack JSON", json.dumps(POLICY_PACK, indent=2), "cgif_v5_policy_pack.json", "application/json")
    st.markdown(
        """
        <div class="footer-boundary">
          <b>Production gap:</b> This professional UI is still a prototype. Real deployment requires authentication, RBAC, database persistence, immutable audit logging, PHI-safe infrastructure, integrations, validation, and compliance approval.
        </div>
        """,
        unsafe_allow_html=True,
    )
