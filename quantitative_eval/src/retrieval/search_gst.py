from pyserini.output_writer import OutputFormat, get_output_writer
from pyserini.search.lucene import LuceneSearcher
import pandas as pd

# Paths
DATA_DIR = "../../gst_data/walert_data"
TOPICS = DATA_DIR + "/topics.csv"

INDEX_BM25 = "../../target/indexes/gst-bm25"
OUTPUT_PATH_BM25 = "../../target/runs/gst-rag-bm25.txt"

# Load GST questions
topics = pd.read_csv(TOPICS)

print("Topics loaded:", len(topics))
print(topics[["question_id", "question"]].head())

# Load BM25 index
print("\nLoading GST BM25 index...")
searcher = LuceneSearcher(INDEX_BM25)

num_hits = 100
run_tag = "gst.rag.bm25"

# Output writer
output_writer = get_output_writer(
    OUTPUT_PATH_BM25,
    OutputFormat("trec"),
    "w",
    max_hits=num_hits,
    tag=run_tag,
    topics=topics
)

# Retrieval
with output_writer:
    for question_id, question in topics[
        ["question_id", "question"]
    ].values:

        hits = searcher.search(question, num_hits)

        print(
            f"{question_id}: {len(hits)} passages retrieved"
        )

        output_writer.write(question_id, hits)

print("\nBM25 retrieval complete.")
print("Results saved to:", OUTPUT_PATH_BM25)