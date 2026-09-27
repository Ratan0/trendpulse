import pandas as pd
import numpy as np
from pathlib import Path

# Define input and output file paths
input_file = Path("data/trends_clean.csv")
output_file = Path("data/trends_analysed.csv")
# Load the cleaned CSV file into a Pandas DataFrame
df = pd.read_csv(input_file)
# Display the first 5 rows
print("First 5 rows:")
print(df.head())
# Print the shape of the DataFrame
print("\nLoaded data:", df.shape)
# Calculate and print average score and comments
print("\nAverage score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())
# Convert score column into a NumPy array
scores = df["score"].to_numpy()
# Calculate mean, median, and standard deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
print("\n--- NumPy Stats ---")
print("Mean score:", mean_score)
print("Median score:", median_score)
print("Std deviation:", std_score)
# Find the highest and lowest scores
max_score = np.max(scores)
min_score = np.min(scores)
print("Max score:", max_score)
print("Min score:", min_score)
# Find the category with the most stories
category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()
print(
  f"Most stories in: {most_common_category} "
  f"({most_common_count} stories)"
)
# Find the story with the highest number of comments
most_commented_index = df["num_comments"].idxmax()
most_commented_story = df.loc[most_commented_index, "title"]
most_commented_count = df.loc[
  most_commented_index, "num_comments"
]
print(
  f'Most commented story: "{most_commented_story}" '
  f"— {most_commented_count} comments"
)
# Engagement: comments received per upvote
# Adding 1 to score avoids division by zero
df["engagement"] = df["num_comments"] / (df["score"] + 1)
# Popularity: True if score is above the average score
average_score = df["score"].mean()
df["is_popular"] = df["score"] > average_score
# Display the new columns for verification
print("\nNew columns:")
print(df[["title", "engagement", "is_popular"]].head())
# Save the analyzed DataFrame to a new CSV file
df.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")
