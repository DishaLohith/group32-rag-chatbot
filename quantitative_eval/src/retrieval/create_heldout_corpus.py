import pandas as pd
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

DATA_DIR = Path("../../gst_data/walert_data")

COLLECTION_FILE = DATA_DIR / "collection.csv"

OUTPUT_DIR = DATA_DIR / "heldout"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = OUTPUT_DIR / "collection_heldout.csv"
OUTPUT_JSONL = OUTPUT_DIR / "collection_heldout.jsonl"


# =========================================================
# LOAD ORIGINAL COLLECTION
# =========================================================

print("Loading original GST collection...")

df = pd.read_csv(COLLECTION_FILE)

print("Original passages:", len(df))


# =========================================================
# DIRECT TEST-ANSWER PASSAGES TO HOLD OUT
# =========================================================

heldout_ids = [
    "DFL_939",   # plain bread rolls
    "DFL_655",   # restaurant bread rolls
    "DFL_333",   # flavoured milk
    "DFL_184",   # raw chicken
    "DFL_180",   # hot cooked chicken
    "DFL_411",   # hot chicken / prepared food
    "DFL_196",   # chocolate confectionery
    "DFL_733",   # carbonated soft drinks
    "DFL_1244",  # fruit juice
    "DFL_810",   # raw almonds
    "DFL_536",   # almonds
    "DFL_537",   # roasted/salted almonds
    "DFL_669",   # roasted/salted almonds
    "DFL_528",   # bottled water
    "DFL_971",   # carbonated mineral water
    "DFL_656"    # rice cakes
]


# =========================================================
# CHECK IDS
# =========================================================

existing_ids = set(df["passage_id"].astype(str))

print("\nChecking held-out passages...")

for passage_id in heldout_ids:

    if passage_id in existing_ids:
        print("FOUND:", passage_id)

    else:
        print("WARNING - NOT FOUND:", passage_id)


# =========================================================
# REMOVE DIRECT TEST ANSWERS
# =========================================================

heldout_df = df[
    ~df["passage_id"].isin(heldout_ids)
].copy()


print("\n========================================")
print("HELD-OUT CORPUS")
print("========================================")

print("Original passages:", len(df))
print("Passages removed:", len(df) - len(heldout_df))
print("Remaining passages:", len(heldout_df))


# =========================================================
# SAVE CSV
# =========================================================

heldout_df.to_csv(
    OUTPUT_CSV,
    index=False
)


# =========================================================
# SAVE JSONL FOR DENSE ENCODING
# =========================================================

dense_df = heldout_df[
    ["passage_id", "passage"]
].copy()

dense_df.columns = [
    "id",
    "text"
]

dense_df.to_json(
    OUTPUT_JSONL,
    orient="records",
    lines=True,
    force_ascii=False
)


print("\nSaved CSV:")
print(OUTPUT_CSV)

print("\nSaved dense JSONL:")
print(OUTPUT_JSONL)

print("\nHeld-out corpus creation complete.")