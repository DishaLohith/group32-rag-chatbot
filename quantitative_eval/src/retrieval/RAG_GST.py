from pyserini.search.faiss import FaissSearcher
import pandas as pd

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


# =========================================================
# GST RAG CONFIGURATION
# =========================================================

DATA_DIR = "../../gst_data/walert_data"

COLLECTION = DATA_DIR + "/collection.csv"
TOPICS = DATA_DIR + "/topics.csv"

INDEX = "../../target/indexes/gst-tct_colbert-v2-hnp-msmarco-faiss"

QUERY_ENCODER = "castorini/tct_colbert-v2-hnp-msmarco"

TOP_K = 3


# =========================================================
# LOAD GST COLLECTION
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
# RETRIEVE CONTEXT
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

        passage = row.iloc[0]["passage"]

        contexts.append({
            "passage_id": hit.docid,
            "score": hit.score,
            "passage": passage
        })

    return contexts


# =========================================================
# BUILD GST CLASSIFICATION PROMPT
# =========================================================

def build_prompt(question, contexts):

    context_text = ""

    for i, context in enumerate(contexts, start=1):
        context_text += (
            f"Document {i}: {context['passage']}\n"
        )

    prompt = f"""
Classify the Australian GST status using only the evidence below.

Possible answers:
GST-free
Taxable
Abstain

If the evidence clearly says the product is taxable, answer Taxable.
If the evidence clearly says the product is GST-free, answer GST-free.
If the evidence does not clearly support either classification, answer Abstain.

Evidence:
{context_text}

Question: {question}

Answer with only one label:
"""

    return prompt


# =========================================================
# LOAD GENERATION MODEL
# =========================================================

MODEL_NAME = "google/flan-t5-base"
print("Loading generation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

model.eval()

print("Generation model loaded.")


# =========================================================
# GENERATE GST CLASSIFICATION
# =========================================================

def generate_answer(prompt):

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer


# =========================================================
# TEST ONE QUESTION
# =========================================================

if __name__ == "__main__":

    question = "Is flavoured chocolate milk taxable?"

    print("\nQuestion:")
    print(question)

    # Retrieve top 3 passages
    contexts = get_context_passages(question)

    print("\n==============================")
    print("TOP 3 RETRIEVED GST PASSAGES")
    print("==============================")

    for i, context in enumerate(contexts, start=1):

        print(f"\n--- Document {i} ---")
        print("Passage ID:", context["passage_id"])
        print("Score:", context["score"])
        print(context["passage"])

    # Build prompt
    prompt = build_prompt(
        question,
        contexts
    )

    print("\n==============================")
    print("PROMPT THAT WILL GO TO THE LLM")
    print("==============================")

    print(prompt)

    # Generate classification
    print("\n==============================")
    print("GST RAG CLASSIFICATION")
    print("==============================")

    answer = generate_answer(prompt)

    print(answer)