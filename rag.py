import chromadb
import pandas as pd

client = chromadb.Client()


def build_rag(df: pd.DataFrame):
    try:
        client.delete_collection("transactions")
    except Exception:
        pass

    collection = client.create_collection("transactions")

    docs, ids, metas = [], [], []
    for i, row in df.iterrows():
        doc = f"{row['date']} | {row['description']} | ₹{row['amount']} | {row['category']}"
        docs.append(doc)
        ids.append(str(i))
        metas.append({
            "date": str(row["date"]),
            "category": row["category"],
            "amount": float(row["amount"])
        })

    collection.add(documents=docs, ids=ids, metadatas=metas)
    return collection


def retrieve(collection, query: str, n=5):
    results = collection.query(query_texts=[query], n_results=min(n, collection.count()))
    docs = results["documents"][0] if results["documents"] else []
    return "\n".join(docs)
