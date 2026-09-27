import os
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file from Task 3
df = pd.read_csv("data/trends_analysed.csv")
# Create output folder if it does not exist
os.makedirs("outputs", exist_ok=True)
# Check required columns
required_columns = [
  "title",
  "score",
  "category",
  "num_comments",
  "is_popular"
]
# Convert column names to lowercase and remove spaces
df.columns = df.columns.str.strip().str.lower()
for col in required_columns:
  if col not in df.columns:
    raise ValueError(f"Missing required column: {col}")
# Handle missing values
df["title"] = df["title"].fillna("Untitled")
df["category"] = df["category"].fillna("Unknown")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
  df["num_comments"], errors="coerce"
).fillna(0)
# Remove rows without a valid score
df = df.dropna(subset=["score"])
# Convert popular column to boolean if needed
if df["is_popular"].dtype != bool:
  df["is_popular"] = (
    df["is_popular"]
    .astype(str)
    .str.lower()
    .isin(["true", "1", "yes"])
  )
top10 = df.nlargest(10, "score").sort_values("score")
plt.figure(figsize=(12, 7))
plt.barh(
  top10["title"],
  top10["score"],
  color="steelblue"
)
plt.title("Top 10 Trending Stories by Score", fontsize=16)
plt.xlabel("Story Score", fontsize=12)
plt.ylabel("Story Title", fontsize=12)
plt.tight_layout()
plt.savefig(
  "outputs/chart1_top_stories.png",
  dpi=300,
  bbox_inches="tight"
)
plt.close()
category_counts = df["category"].value_counts()
plt.figure(figsize=(10, 6))
plt.bar(
  category_counts.index,
  category_counts.values,
  color=plt.cm.Set3(
    range(len(category_counts))
  )
)
plt.title("Number of Stories by Category", fontsize=16)
plt.xlabel("Category", fontsize=12)
plt.ylabel("Number of Stories", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(
  "outputs/chart2_categories.png",
  dpi=300,
  bbox_inches="tight"
)
plt.close()
popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]
plt.figure(figsize=(10, 6))
# Non-popular stories
plt.scatter(
  non_popular["score"],
  non_popular["num_comments"],
  color="gray",
  alpha=0.7,
  label="Non-Popular Stories"
)
# Popular stories
plt.scatter(
  popular["score"],
  popular["num_comments"],
  color="red",
  alpha=0.7,
  label="Popular Stories"
)
plt.title("Story Score vs Number of Comments", fontsize=16)
plt.xlabel("Story Score", fontsize=12)
plt.ylabel("Number of Comments", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
  "outputs/chart3_scatter.png",
  dpi=300,
  bbox_inches="tight"
)
plt.close()
fig, axes = plt.subplots(
  1, 3,
  figsize=(22, 8)
)
# Chart 1: Top 10 Stories
axes[0].barh(
  top10["title"],
  top10["score"],
  color="steelblue"
)
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
# Chart 2: Category Counts
axes[1].bar(
  category_counts.index,
  category_counts.values,
  color=plt.cm.Set3(
    range(len(category_counts))
  )
)
axes[1].set_title("Stories by Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(
  axis="x",
  rotation=45
)
# Chart 3: Score vs Comments
axes[2].scatter(
  non_popular["score"],
  non_popular["num_comments"],
  color="gray",
  alpha=0.7,
  label="Non-Popular"
)
axes[2].scatter(
  popular["score"],
  popular["num_comments"],
  color="red",
  alpha=0.7,
  label="Popular"
)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()
axes[2].grid(True, alpha=0.3)
# Add overall dashboard title
fig.suptitle(
  "TrendPulse Dashboard",
  fontsize=22,
  fontweight="bold"
)
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(
  "outputs/dashboard.png",
  dpi=300,
  bbox_inches="tight"
)
plt.close()
print("All visualizations created successfully!")
print("Output files:")
print("outputs/chart1_top_stories.png")
print("outputs/chart2_categories.png")
print("outputs/chart3_scatter.png")
print("outputs/dashboard.png")
