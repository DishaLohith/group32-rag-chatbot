from pyserini.search.faiss import FaissSearcher
import pandas as pd
import re


# =========================================================
# CONFIGURATION
# =========================================================

DATA_DIR = "../../gst_data/walert_data"

COLLECTION = DATA_DIR + "/collection.csv"

INDEX = "../../target/indexes/gst-tct_colbert-v2-hnp-msmarco-faiss"

QUERY_ENCODER = "castorini/tct_colbert-v2-hnp-msmarco"

TOP_K = 3


# =========================================================
# LOAD COLLECTION
# =========================================================

print("Loading GST collection...")

collection_df = pd.read_csv(COLLECTION)

print("GST passages loaded:", len(collection_df))


# =========================================================
# LOAD DENSE RETRIEVER
# =========================================================

print("Loading GST Dense FAISS retriever...")

searcher = FaissSearcher(
    INDEX,
    QUERY_ENCODER
)

print("Retriever loaded.")


# =========================================================
# RETRIEVE EVIDENCE
# =========================================================

def get_context_passages(question, top_k=TOP_K):

    hits = searcher.search(question, 10)

    contexts = []

    for hit in hits[:top_k]:

        row = collection_df[
            collection_df["passage_id"] == hit.docid
        ]

        if len(row) == 0:
            continue

        passage = str(row.iloc[0]["passage"])

        contexts.append({
            "passage_id": hit.docid,
            "score": float(hit.score),
            "passage": passage
        })

    return contexts


# =========================================================
# EXTRACT EXPLICIT GST STATUS FROM A PASSAGE
# =========================================================

def extract_status(passage):

    text = passage.lower()

    # Explicit status fields from the Detailed Food List
    if re.search(r"gst status:\s*gst[- ]free", text):
        return "GST-free"

    if re.search(r"gst status:\s*taxable", text):
        return "Taxable"

    # Explicit legislative statements
    if "supply of *food is gst-free" in text:
        return "GST-free"

    if "supply of food is gst-free" in text:
        return "GST-free"

    return None


# =========================================================
# EVIDENCE-BASED CLASSIFIER
# =========================================================

def classify_from_evidence(contexts):

    evidence = []

    for context in contexts:

        status = extract_status(
            context["passage"]
        )

        if status is not None:

            evidence.append({
                "passage_id": context["passage_id"],
                "score": context["score"],
                "status": status
            })


    # -----------------------------------------------------
    # No explicit status evidence
    # -----------------------------------------------------

    if len(evidence) == 0:

        return {
            "classification": "Abstain",
            "reason": "No retrieved passage contained an explicit GST classification.",
            "evidence": []
        }


    # -----------------------------------------------------
    # Count classifications
    # -----------------------------------------------------

    taxable = [
        item for item in evidence
        if item["status"] == "Taxable"
    ]

    gst_free = [
        item for item in evidence
        if item["status"] == "GST-free"
    ]


    # -----------------------------------------------------
    # All explicit evidence agrees
    # -----------------------------------------------------

    if len(taxable) > 0 and len(gst_free) == 0:

        return {
            "classification": "Taxable",
            "reason": (
                "The retrieved passages containing explicit GST "
                "status information consistently classify the "
                "relevant products as taxable."
            ),
            "evidence": taxable
        }


    if len(gst_free) > 0 and len(taxable) == 0:

        return {
            "classification": "GST-free",
            "reason": (
                "The retrieved passages containing explicit GST "
                "status information consistently classify the "
                "relevant products as GST-free."
            ),
            "evidence": gst_free
        }


    # -----------------------------------------------------
    # Conflicting explicit evidence
    # -----------------------------------------------------

    return {
        "classification": "Abstain",
        "reason": (
            "The retrieved passages contain conflicting explicit "
            "GST classifications, so the system abstains."
        ),
        "evidence": evidence
    }


# =========================================================
# TEST ONE QUESTION
# =========================================================

if __name__ == "__main__":

    question = "Is flavoured chocolate milk taxable?"

    print("\nQuestion:")
    print(question)

    contexts = get_context_passages(question)

    print("\n========================================")
    print("TOP 3 RETRIEVED PASSAGES")
    print("========================================")

    for i, context in enumerate(contexts, start=1):

        print(f"\n--- Document {i} ---")
        print("Passage ID:", context["passage_id"])
        print("Score:", context["score"])
        print(context["passage"])

        extracted = extract_status(
            context["passage"]
        )

        print("Extracted status:", extracted)


    result = classify_from_evidence(contexts)


    print("\n========================================")
    print("IMPROVED GST CLASSIFICATION")
    print("========================================")

    print("Classification:", result["classification"])
    print("Reason:", result["reason"])

    print("\nEvidence used:")

    if len(result["evidence"]) == 0:

        print("None")

    else:

        for item in result["evidence"]:

            print(
                item["passage_id"],
                "->",
                item["status"]
            )