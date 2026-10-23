from pyserini.search.faiss import FaissSearcher
from pyserini.output_writer import OutputFormat, get_output_writer
import pandas as pd

# Paths
DATA_DIR = "../../gst_data/walert_data"
TOPICS = DATA_DIR + "/topics.csv"

INDEX = "../../target/indexes/gst-tct_colbert-v2-hnp-msmarco-faiss"
OUTPUT = "../../target/runs/gst-rag-dense-faiss.txt"

# Same encoder used to create the embeddings
QUERY_ENCODER = "castorini/tct_colbert-v2-hnp-msmarco"

# Load GST questions
topics = pd.read_csv(TOPICS)

print("Topics loaded:", len(topics))
print(topics[["question_id", "question"]].head())

print("\nLoading GST FAISS index...")

searcher = FaissSearcher(
    INDEX,
    QUERY_ENCODER
)

num_hits = 100
run_tag = "gst.rag.dense.faiss"

output_writer = get_output_writer(
    OUTPUT,
    OutputFormat("trec"),
    "w",
    max_hits=num_hits,
    tag=run_tag,
    topics=topics
)

print("\nRunning dense retrieval...")

with output_writer:
    for question_id, question in topics[
        ["question_id", "question"]
    ].values:

        hits = searcher.search(question, num_hits)

        print(
            f"{question_id}: "
            f"{len(hits)} passages retrieved"
        )

        output_writer.write(
            question_id,
            hits
        )

print("\nDense retrieval complete.")
print("Results saved to:", OUTPUT)