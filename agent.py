import pandas as pd
from categorizer import categorize
from analytics import compute_metrics
from advisor import advisor

df = pd.read_csv("sample_data.csv")
df["category"] = df["description"].apply(categorize)

metrics = compute_metrics(df)

while True:
    q = input("Ask: ")
    print(advisor(q, metrics, []))
