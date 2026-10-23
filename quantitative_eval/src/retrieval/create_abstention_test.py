import pandas as pd

tests = [
    {
        "query_id": "ABS01",
        "query": "What is the capital of France?",
        "expected_label": "Abstain",
        "reason": "General knowledge question unrelated to Australian GST food classification."
    },
    {
        "query_id": "ABS02",
        "query": "Will it rain in Melbourne tomorrow?",
        "expected_label": "Abstain",
        "reason": "Weather question outside the GST knowledge base."
    },
    {
        "query_id": "ABS03",
        "query": "Who won the FIFA World Cup in 2022?",
        "expected_label": "Abstain",
        "reason": "Sports question outside the GST knowledge base."
    },
    {
        "query_id": "ABS04",
        "query": "How do I reset my laptop password?",
        "expected_label": "Abstain",
        "reason": "Technical-support question outside the GST knowledge base."
    },
    {
        "query_id": "ABS05",
        "query": "What is the distance from Earth to Mars?",
        "expected_label": "Abstain",
        "reason": "Astronomy question outside the GST knowledge base."
    }
]

df = pd.DataFrame(tests)

output = "../../gst_data/walert_data/gst_abstention_test.csv"

df.to_csv(output, index=False)

print(df.to_string(index=False))
print("\nSaved to:", output)