import pandas as pd

df_2024 = pd.read_csv("ICLR_2024_papers.csv")
df_2025 = pd.read_csv("ICLR_2025_papers.csv")

sample_2024 = df_2024.sample(n=100, random_state=42)
sample_2025 = df_2025.sample(n=100, random_state=42)

combined_df = pd.concat([sample_2024, sample_2025], ignore_index=True)
combined_df.to_csv("data.csv", index=False)

print("✅ data.csv created with 200 rows (100 from each file)")
