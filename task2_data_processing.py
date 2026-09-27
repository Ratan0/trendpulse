import pandas as pd
import os
import glob

# Find the latest JSON file inside the data folder
json_files = glob.glob("data/trends_*.json")
if not json_files:
  raise FileNotFoundError("No JSON file found in the data folder.")
file_path = max(json_files, key=os.path.getmtime)
df = pd.read_json(file_path)
print(f"Loaded {len(df)} stories from {file_path}")

# Step 1: Remove duplicate stories using post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")
# Step 2: Remove rows with missing required values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")
# Step 3: Convert score and num_comments to integers
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
  df["num_comments"], errors="coerce"
)
# Remove rows where integer fields cannot be converted
df = df.dropna(subset=["score", "num_comments"])
df = df[
  (df["score"] % 1 == 0) &
  (df["num_comments"] % 1 == 0)
].copy()
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
# Step 4: Remove stories with score less than 5
df = df[df["score"] >= 5].copy()
print(f"After removing low scores: {len(df)}")
# Step 5: Remove extra spaces from titles
df["title"] = df["title"].astype(str).str.strip()
# Task 3: Save the cleaned data as CSV
output_path = "data/trends_clean.csv"
df.to_csv(output_path, index=False)
print(f"Saved {len(df)} rows to {output_path}")
# Print stories per category
print("\nStories per category:")
print(df["category"].value_counts().to_string())
