import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import hashlib

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
STIMULI_PATH = DATA_DIR / "sample_stimuli.csv"
ANNOTATIONS_PATH = DATA_DIR / "annotations.csv"
RECEIPT_DIR = APP_DIR / "receipts"
RECEIPT_DIR.mkdir(exist_ok=True)

LABELS = [
    "moral_violation",
    "semantic_violation",
    "neutral",
    "ambiguous",
    "insufficient_context",
]

CRITERIA_FLAGS = [
    "harm_or_care_violation",
    "fairness_or_cheating",
    "authority_or_rule_violation",
    "loyalty_or_betrayal",
    "purity_or_disgust",
    "semantic_anomaly",
    "world_knowledge_conflict",
    "language_ambiguity",
    "cultural_context_dependency",
    "insufficient_information",
]

REQUIRED_STIMULI_COLUMNS = [
    "stimulus_id",
    "context_sentence",
    "target_sentence",
    "critical_word",
    "language",
]


def load_stimuli(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(STIMULI_PATH)

    missing = [c for c in REQUIRED_STIMULI_COLUMNS if c not in df.columns]
    if missing:
        st.error(f"Stimuli file is missing required columns: {missing}")
        st.stop()
    return df


def init_annotations_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not ANNOTATIONS_PATH.exists():
        pd.DataFrame(columns=[
            "annotation_id",
            "timestamp_utc",
            "annotator_id",
            "stimulus_id",
            "selected_label",
            "confidence",
            "criteria_flags",
            "rationale",
            "llm_baseline_label",
            "llm_baseline_rationale",
            "app_version",
        ]).to_csv(ANNOTATIONS_PATH, index=False)


def load_annotations():
    init_annotations_file()
    return pd.read_csv(ANNOTATIONS_PATH)


def make_annotation_id(row: dict) -> str:
    raw = json.dumps(row, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def save_annotation(row: dict):
    init_annotations_file()
    row["annotation_id"] = make_annotation_id(row)
    pd.DataFrame([row]).to_csv(ANNOTATIONS_PATH, mode="a", header=False, index=False)
    return row["annotation_id"]


def create_receipt(stimulus: pd.Series, annotation: dict) -> str:
    criteria = annotation.get("criteria_flags", [])
    if isinstance(criteria, str):
        try:
            criteria = json.loads(criteria)
        except Exception:
            criteria = [criteria]

    criteria_md = "\n".join([f"- {flag}" for flag in criteria]) if criteria else "- None selected"

    return f"""# Moral Violation Judgment Receipt

## Stimulus
- Stimulus ID: `{stimulus.get('stimulus_id', '')}`
- Language: `{stimulus.get('language', '')}`
- Critical word/region: `{stimulus.get('critical_word', '')}`

### Context sentence
{stimulus.get('context_sentence', '')}

### Target sentence
{stimulus.get('target_sentence', '')}

## Human Annotation
- Annotation ID: `{annotation.get('annotation_id', '')}`
- Timestamp UTC: `{annotation.get('timestamp_utc', '')}`
- Annotator ID: `{annotation.get('annotator_id', '')}`
- Selected label: `{annotation.get('selected_label', '')}`
- Confidence: `{annotation.get('confidence', '')}/100`

## Criteria Flags
{criteria_md}

## Annotator Rationale
{annotation.get('rationale', '').strip() or 'No rationale provided.'}

## Optional LLM Baseline
- LLM label: `{annotation.get('llm_baseline_label', '') or 'not provided'}`

### LLM rationale
{annotation.get('llm_baseline_rationale', '').strip() or 'No LLM baseline rationale provided.'}

## Audit Notes
This receipt records the judgment path for later review. It does not claim that the label is objectively correct. It records who judged the item, what criteria they used, how confident they were, and whether a model baseline disagreed.
"""


st.set_page_config(
    page_title="Moral Violation Judgment Annotation Tool",
    page_icon="🧠",
    layout="wide",
)

st.title("Moral Violation Judgment Annotation Tool")
st.caption("Research prototype for annotating moral / semantic / neutral language judgments with audit receipts.")

with st.sidebar:
    st.header("Setup")
    annotator_id = st.text_input("Annotator ID", value="annotator_001")
    uploaded = st.file_uploader("Upload stimuli CSV", type=["csv"])
    show_gold = st.checkbox("Researcher mode: show optional condition column", value=False)
    st.markdown("---")
    st.markdown("**Required CSV columns**")
    st.code("stimulus_id, context_sentence, target_sentence, critical_word, language")

stimuli_df = load_stimuli(uploaded)
annotations_df = load_annotations()

tab_annotate, tab_dashboard, tab_export, tab_schema = st.tabs([
    "Annotate",
    "Dashboard",
    "Export Receipt",
    "Schema",
])

with tab_annotate:
    st.subheader("Annotation Workspace")

    stimulus_options = stimuli_df["stimulus_id"].astype(str).tolist()
    selected_id = st.selectbox("Select stimulus", stimulus_options)
    stim = stimuli_df[stimuli_df["stimulus_id"].astype(str) == selected_id].iloc[0]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Stimulus")
        st.markdown(f"**Context:** {stim['context_sentence']}")
        st.markdown(f"**Target:** {stim['target_sentence']}")
        st.markdown(f"**Critical word/region:** `{stim['critical_word']}`")
        st.markdown(f"**Language:** `{stim['language']}`")

        if show_gold and "true_condition_optional" in stimuli_df.columns:
            st.info(f"Optional researcher condition: {stim.get('true_condition_optional', '')}")

    with col2:
        previous = annotations_df[annotations_df["stimulus_id"].astype(str) == str(selected_id)]
        st.metric("Existing annotations for this stimulus", len(previous))
        if len(previous) > 0:
            st.write(previous[["annotator_id", "selected_label", "confidence"]].tail(5))

    st.markdown("---")
    st.markdown("### Human Judgment")

    selected_label = st.radio("Selected label", LABELS, horizontal=True)
    confidence = st.slider("Confidence", min_value=0, max_value=100, value=70)
    selected_flags = st.multiselect("Criteria flags", CRITERIA_FLAGS)
    rationale = st.text_area(
        "Rationale",
        placeholder="Explain why this is a moral violation, semantic violation, neutral item, ambiguous case, or insufficient-context case.",
        height=120,
    )

    with st.expander("Optional LLM baseline comparison"):
        llm_label = st.selectbox("LLM baseline label", [""] + LABELS)
        llm_rationale = st.text_area("LLM baseline rationale", height=100)

    if st.button("Save annotation", type="primary"):
        row = {
            "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "annotator_id": annotator_id.strip() or "anonymous",
            "stimulus_id": str(selected_id),
            "selected_label": selected_label,
            "confidence": confidence,
            "criteria_flags": json.dumps(selected_flags, ensure_ascii=False),
            "rationale": rationale,
            "llm_baseline_label": llm_label,
            "llm_baseline_rationale": llm_rationale,
            "app_version": "0.1-streamlit",
        }
        annotation_id = save_annotation(row)
        row["annotation_id"] = annotation_id
        receipt = create_receipt(stim, row)
        receipt_path = RECEIPT_DIR / f"{annotation_id}_{selected_id}.md"
        receipt_path.write_text(receipt, encoding="utf-8")
        st.success(f"Saved annotation `{annotation_id}` and generated receipt `{receipt_path.name}`.")
        st.download_button(
            "Download this receipt",
            data=receipt,
            file_name=receipt_path.name,
            mime="text/markdown",
        )

with tab_dashboard:
    st.subheader("Annotation Dashboard")
    annotations_df = load_annotations()

    if annotations_df.empty:
        st.info("No annotations yet. Save an annotation first.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total annotations", len(annotations_df))
        col2.metric("Unique stimuli annotated", annotations_df["stimulus_id"].nunique())
        col3.metric("Unique annotators", annotations_df["annotator_id"].nunique())

        st.markdown("### Label Distribution")
        st.bar_chart(annotations_df["selected_label"].value_counts())

        st.markdown("### Stimulus-Level Agreement View")
        grouped = (
            annotations_df
            .groupby("stimulus_id")
            .agg(
                annotation_count=("annotation_id", "count"),
                labels=("selected_label", lambda x: ", ".join(sorted(set(x)))),
                avg_confidence=("confidence", "mean"),
            )
            .reset_index()
        )
        grouped["avg_confidence"] = grouped["avg_confidence"].round(1)
        st.dataframe(grouped, use_container_width=True)

        st.markdown("### Raw Annotations")
        st.dataframe(annotations_df, use_container_width=True)

        csv_bytes = annotations_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download annotations CSV", csv_bytes, "annotations.csv", "text/csv")

with tab_export:
    st.subheader("Export / Review Receipts")
    annotations_df = load_annotations()

    if annotations_df.empty:
        st.info("No receipts available yet.")
    else:
        selected_annotation = st.selectbox(
            "Select annotation ID",
            annotations_df["annotation_id"].astype(str).tolist(),
        )
        ann = annotations_df[annotations_df["annotation_id"].astype(str) == selected_annotation].iloc[0].to_dict()
        stim_match = stimuli_df[stimuli_df["stimulus_id"].astype(str) == str(ann["stimulus_id"])]

        if stim_match.empty:
            st.error("Matching stimulus not found.")
        else:
            receipt = create_receipt(stim_match.iloc[0], ann)
            st.markdown(receipt)
            st.download_button(
                "Download receipt",
                data=receipt,
                file_name=f"{selected_annotation}_{ann['stimulus_id']}.md",
                mime="text/markdown",
            )

with tab_schema:
    st.subheader("CSV Schema")

    st.markdown("""
### Required stimulus columns
- `stimulus_id`: unique item identifier
- `context_sentence`: context sentence shown before target
- `target_sentence`: sentence containing the critical word or region
- `critical_word`: the critical word or phrase
- `language`: language of the stimulus

### Optional stimulus columns
- `true_condition_optional`: researcher-only condition label, hidden by default
- `notes`: internal research notes
- `source`: source or study version
- `version`: stimulus version

### Annotation labels
- `moral_violation`: the sentence violates a moral norm
- `semantic_violation`: the sentence is semantically anomalous or world-knowledge inconsistent
- `neutral`: no clear violation
- `ambiguous`: multiple plausible interpretations
- `insufficient_context`: not enough information to judge

### Deployment note
This demo writes annotations to the app filesystem. For a real multi-user study, connect it to persistent storage such as Google Sheets, PostgreSQL, Firebase, Supabase, or S3.
""")
