from ranx import compare, Qrels, Run
import pandas as pd

# Paths
QRELS_PATH = "../../gst_data/walert_data/qrels.txt"
BM25_RUN_PATH = "../../target/runs/gst-rag-bm25.txt"

# Load GST qrels
qrels_df = pd.read_csv(
    QRELS_PATH,
    sep=r"\s+",
    names=["q_id", "zero", "doc_id", "score"],
    header=None
)

print("Qrels loaded:", len(qrels_df))
print("Questions:", qrels_df["q_id"].nunique())

print("\nFirst qrels:")
print(qrels_df.head())

# Convert qrels to ranx format
qrels = Qrels.from_df(
    qrels_df,
    q_id_col="q_id",
    doc_id_col="doc_id",
    score_col="score"
)

# Load BM25 retrieval results
bm25_run = Run.from_file(
    BM25_RUN_PATH,
    kind="trec"
)

bm25_run.name = "GST BM25"

# Evaluate
report = compare(
    qrels=qrels,
    runs=[bm25_run],
    metrics=[
        "ndcg@1",
        "ndcg@3",
        "ndcg@5"
    ],
    make_comparable=True,
    rounding_digits=4
)

print("\n==============================")
print("GST BM25 Retrieval Evaluation")
print("==============================")

print(report)

print("\nLaTeX:")
print(report.to_latex())