import requests
import time
import json
import os
from datetime import datetime

CATEGORY_KEYWORDS = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}

def get_category(title):
    title_lower = title.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category

    return None

headers = {
    "User-Agent": "TrendPulse/1.0"
}

# Step 1: Get the top story IDs
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

response = requests.get(top_stories_url, headers=headers)

print("Top stories status:", response.status_code)

story_ids = response.json()[:500]

print("Number of story IDs:", len(story_ids))

# Step 2: Test fetching details of the first 5 stories
for story_id in story_ids[:5]:

    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    story_response = requests.get(story_url, headers=headers)

    print("Story ID:", story_id)
    print("Status:", story_response.status_code)

    if story_response.status_code == 200:
        story = story_response.json()
        print("Title:", story.get("title"))
        print("Author:", story.get("by"))
        print("Score:", story.get("score"))
        print()

story_ids = response.json()[:500]

# Store collected stories
collected_stories = []

# Keep track of how many stories we have collected per category
category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

# Fetch each story
for story_id in story_ids:

    # Stop when all categories have 25 stories
    if all(count == 25 for count in category_counts.values()):
        break

    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"

    try:
        story_response = requests.get(
            story_url,
            headers=headers,
            timeout=10
        )

        if story_response.status_code != 200:
            print(f"Request failed for story {story_id}")
            continue

        story = story_response.json()

        # Make sure this is a story with a title
        if not story or "title" not in story:
            continue

        title = story.get("title", "")
        category = get_category(title)

        # Skip stories that don't match any category
        if category is None:
            continue

        # Skip category if we already have 25 stories
        if category_counts[category] >= 25:
            continue

        collected_story = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().isoformat()
        }

        collected_stories.append(collected_story)
        category_counts[category] += 1

        print(
            f"Collected {category}: "
            f"{category_counts[category]}/25 - {title}"
        )

    except requests.RequestException as error:
        print(f"Request failed for story {story_id}: {error}")
        continue

        print("\nCategory totals:")

for category, count in category_counts.items():
    print(f"{category}: {count}")

print(f"\nTotal stories collected: {len(collected_stories)}")

import json

with open("raw_data.json", "w", encoding="utf-8") as file:
    json.dump(collected_stories, file, indent=4)

print("Raw data saved to raw_data.json")