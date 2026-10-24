# Australian GST Food Classification — RAG Evaluation

## Project Overview

This project adapts the Walert retrieval and question-answering framework to Australian GST food classification.

The system retrieves evidence from official GST resources and classifies questions as GST-free, Taxable or Abstain.

## Folder Structure

- `src/retrieval/` — GST retrieval, RAG, classification and evaluation Python scripts.
- `gst_data/processed/` — Master GST corpus and GST-specific classification ground truth.
- `gst_data/walert_data/` — Retrieval collections, topics, qrels and supporting evaluation datasets.
- `gst_data/walert_data/heldout/` — Modified corpus with selected direct-answer passages removed.
- `target/runs/` — Saved retrieval runs, classification predictions and evaluation results.
- `requirements.txt` — Python dependencies.

## Models and Methods

- BM25: Keyword-based retrieval baseline.
- TCT-ColBERT-v2: Dense retrieval embeddings.
- FAISS: Dense vector search.
- FLAN-T5-base: Answer generation in the original adapted RAG baseline.
- Evidence-based classifier: Final classification method using explicit GST evidence and abstention rules.

## Running the Evaluation

Run commands from `quantitative_eval/src/retrieval/` after installing the project dependencies and preparing the required indexes.

Retrieval comparison:

```bash
python eval_compare_gst.py
```

Verify dense retrieval rankings:

```bash
python verify_gst_ndcg.py
```

Original GST RAG evaluation:

```bash
python evaluate_rag_gst.py
```

Improved classification evaluation:

```bash
python evaluate_improved_gst.py
```

Held-out evaluation:

```bash
python evaluate_improved_gst_heldout.py
```

Final system evaluation:

```bash
python evaluate_final_gst.py
```

The retrieval and RAG components require the appropriate Java/Pyserini environment and existing retrieval indexes. The commands above assume these dependencies and indexes have been configured.

## Results

On the original 14-question GST test set:

| Method | Result |
|---|---|
| BM25 nDCG@1 | 0.4286 |
| Dense FAISS nDCG@1 | 0.7857 |
| Dense FAISS nDCG@3 | 0.6621 |
| Dense FAISS nDCG@5 | 0.6621 |
| FLAN-T5 RAG classification | 7/14 (50%) |
| Improved evidence-based classification | 13/14 (92.86%) |
| Improved held-out classification | 13/14 (92.86%) |

The improved classifier abstained on GST13 (carbonated mineral water) because retrieved evidence contained conflicting explicit classifications.

These results are based on a small evaluation set and should not be interpreted as general real-world performance.
