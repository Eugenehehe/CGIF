# Moral Violation Judgment Annotation Tool

A lightweight Streamlit research prototype for annotating moral / semantic / neutral language judgments and exporting audit-style decision receipts.

## Purpose

This tool supports sentence-level annotation for moral-violation research workflows. It does not process EEG data. It focuses on the stimulus and judgment layer:

- context sentence
- target sentence
- critical word or region
- human label
- confidence score
- criteria flags
- rationale
- optional LLM baseline comparison
- downloadable audit receipt

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Use this GitHub repo and app path:

```text
Repository: Eugenehehe/CGIF
Branch: main
Main file path: moral-violation-annotation-tool/app.py
```

## CSV schema

Required columns:

```text
stimulus_id, context_sentence, target_sentence, critical_word, language
```

Optional columns:

```text
true_condition_optional, notes, source, version
```

## Deployment note

This demo writes annotations to the app filesystem. On Streamlit Community Cloud, file writes may not be reliable as permanent storage across app restarts. For a real multi-user study, connect the annotation output to persistent storage such as Google Sheets, PostgreSQL, Firebase, Supabase, or S3.
