from pathlib import Path
import pytrec_eval

root = Path(__file__).resolve().parents[2]

qrels_path = root / "gst_data/walert_data/qrels.txt"
run_path = root / "target/runs/gst-rag-dense-faiss.txt"

with open(qrels_path, encoding="utf-8") as f:
    qrels = pytrec_eval.parse_qrel(f)

with open(run_path, encoding="utf-8") as f:
    run = pytrec_eval.parse_run(f)

evaluator = pytrec_eval.RelevanceEvaluator(
    qrels, {"ndcg_cut_3", "ndcg_cut_5"}
)
results = evaluator.evaluate(run)

print("\nGST DENSE RETRIEVAL: nDCG VERIFICATION")
print("-" * 55)
print(f"{'Query':<10} {'Relevant ranks':<25} {'Relevant at 4-5'}")

total = 0

for qid in sorted(qrels):
    ranked = sorted(
        run.get(qid, {}).items(),
        key=lambda item: (-item[1], item[0])
    )

    relevant_ranks = [
        rank
        for rank, (docid, _) in enumerate(ranked, start=1)
        if qrels[qid].get(docid, 0) > 0
    ]

    extra = [r for r in relevant_ranks if r in (4, 5)]
    total += len(extra)

    print(
        f"{qid:<10} {str(relevant_ranks):<25} "
        f"{len(extra)}"
    )

n = len(results)
ndcg3 = sum(v["ndcg_cut_3"] for v in results.values()) / n
ndcg5 = sum(v["ndcg_cut_5"] for v in results.values()) / n

print("-" * 55)
print(f"Additional relevant documents at ranks 4-5: {total}")
print(f"nDCG@3: {ndcg3:.4f}")
print(f"nDCG@5: {ndcg5:.4f}")

if total == 0 and abs(ndcg3 - ndcg5) < 1e-10:
    print("CONFIRMED: Equal scores are expected.")
else:
    print("REVIEW: Inspect ranking and evaluation settings.")