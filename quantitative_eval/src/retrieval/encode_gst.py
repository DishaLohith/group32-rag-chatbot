import subprocess
import sys
from pathlib import Path

CORPUS = "../../gst_data/walert_data/collection.jsonl"

ENCODER = "tct_colbert-v2-hnp-msmarco"

EMBEDDINGS = (
    "../../target/embeddings/"
    "gst-tct_colbert-v2-hnp-msmarco"
)

Path(EMBEDDINGS).mkdir(parents=True, exist_ok=True)

command = [
    sys.executable,
    "-m",
    "pyserini.encode",

    "input",
    "--corpus", CORPUS,
    "--fields", "passage",
    "--docid-field", "passage_id",
    "--shard-id", "0",
    "--shard-num", "1",

    "output",
    "--embeddings", EMBEDDINGS,
    "--to-faiss",

    "encoder",
    "--encoder", f"castorini/{ENCODER}",
    "--fields", "passage",
    "--batch", "32",
    "--device", "cpu"
]

print("Starting GST dense encoding...")
print("Corpus:", CORPUS)
print("Encoder:", ENCODER)
print("Output:", EMBEDDINGS)

subprocess.run(command, check=True)

print("\nGST dense encoding complete.")