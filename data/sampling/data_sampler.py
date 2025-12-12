import pandas as pd

# Input
df = pd.read_csv("original_data_200.csv")

# random sample with seed
df_sampled = df.sample(n=150, random_state=100)

# Add a new column for the bias result
df_sampled["bias_result"] = ""

# Output
df_sampled.to_csv("sampled_data.csv", index=False)
