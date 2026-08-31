def generate_report(df):
    return df.to_csv(index=False).encode("utf-8")