import requests
import json
import os
import time
from datetime import datetime

BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {
  "User-Agent": "TrendPulse/1.0"
}

# Keywords for each category (case-insensitive)
CATEGORIES = {
  "technology": [
    "AI", "software", "tech", "code", "computer",
    "data", "cloud", "API", "GPU", "LLM"
  ],

  "worldnews": [
    "war", "government", "country", "president",
    "election", "climate", "attack", "global"
  ],

  "sports": [
    "NFL", "NBA", "FIFA", "sport", "game",
    "team", "player", "league", "championship"
  ],

  "science": [
    "research", "study", "space", "physics",
    "biology", "discovery", "NASA", "genome"
  ],

  "entertainment": [
    "movie", "film", "music", "Netflix", "game",
    "book", "show", "award", "streaming"
  ]

}

MAX_STORIES_PER_CATEGORY = 25

MAX_TOP_STORIES = 500

def fetch_top_story_ids():
  """Fetch the top 500 story IDs from Hacker News."""
  url = f"{BASE_URL}/topstories.json"
  try:
    response = requests.get(
      url,
      headers=HEADERS,
      timeout=15
    )
    response.raise_for_status()
    story_ids = response.json()
    # Return only the first 500 IDs
    return story_ids[:MAX_TOP_STORIES]

  except requests.exceptions.RequestException as e:
    print(f"Error fetching top story IDs: {e}")

    return []

def fetch_story(story_id):
  """Fetch details of a single Hacker News story."""

  url = f"{BASE_URL}/item/{story_id}.json"

  try:
    response = requests.get(
      url,
      headers=HEADERS,
      timeout=15
    )

    response.raise_for_status()

    story = response.json()
    # Ignore deleted, missing, or non-story items
    if not story or story.get("type") != "story":
      return None

    if story.get("deleted") or story.get("dead"):
      return None
    return story
  except requests.exceptions.RequestException as e:
    print(f"Error fetching story {story_id}: {e}")
    return None
def assign_category(title):
  """
  Check the title against category keywords.
  Matching is case-insensitive.
  Return the first matching category.
  """
  title_lower = title.lower()
  for category, keywords in CATEGORIES.items():
    for keyword in keywords:

      if keyword.lower() in title_lower:
        return category
  # Ignore titles that do not match any category
  return None
def extract_story_data(story, category):
  """Extract the seven required fields."""
  return {
    "post_id": story.get("id"),
    "title": story.get("title", ""),
    "category": category,
    "score": story.get("score", 0),
    "num_comments": story.get("descendants", 0),
    "author": story.get("by", "unknown"),
    "collected_at": datetime.now().astimezone().isoformat(
      timespec="seconds"
    )
  }
def collect_stories():
  """Fetch stories and collect up to 25 per category."""
  story_ids = fetch_top_story_ids()
  if not story_ids:
    print("No story IDs received. Please try again.")
    return []
  print(f"Found {len(story_ids)} top story IDs.")
  # Create an empty list for every category
  collected = {
    category: []
    for category in CATEGORIES
  }
  # Fetch each story only once
  for story_id in story_ids:
    # Stop if every category has 25 stories
    if all(
      len(stories) >= MAX_STORIES_PER_CATEGORY
      for stories in collected.values()
    ):
      break
    story = fetch_story(story_id)
    if story is None:
      continue
    title = story.get("title", "")
    if not title:
      continue
    category = assign_category(title)
    # Add the story if its category still needs data
    if category and len(collected[category]) < MAX_STORIES_PER_CATEGORY:
      story_data = extract_story_data(story, category)
      collected[category].append(story_data)
  # Combine all category lists into one list.
  # Wait 2 seconds between category processing loops.
  all_stories = []
  for index, (category, stories) in enumerate(collected.items()):
    all_stories.extend(stories)
    print(f"{category}: {len(stories)} stories collected")
    # Sleep between categories, not between API requests
    if index < len(collected) - 1:
      time.sleep(2)
  return all_stories

def save_to_json(stories):
  """Save collected stories in the data folder."""
  # Create data folder if it does not exist
  os.makedirs("data", exist_ok=True)
  # Generate filename using today's date
  today = datetime.now().strftime("%Y%m%d")
  filename = f"data/trends_{today}.json"
  try:
    with open(filename, "w", encoding="utf-8") as file:
      json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
      )
    print(
      f"Collected {len(stories)} stories. "
      f"Saved to {filename}"
    )
  except OSError as e:
    print(f"Error saving JSON file: {e}")

def main():
  """Run the complete TrendPulse pipeline."""
  stories = collect_stories()
  if stories:
    save_to_json(stories)
  else:
    print("No stories collected.")

if __name__ == "__main__":

  main()
