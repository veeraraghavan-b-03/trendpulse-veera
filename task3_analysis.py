import json
import statistics

# Load processed data
with open("processed_data.json", "r", encoding="utf-8") as file:
    stories = json.load(file)

print("Total stories loaded:", len(stories))

# 1. Average score
scores = [story["score"] for story in stories]

average_score = statistics.mean(scores)

print("\nAverage score:", round(average_score, 2))

# 2. Highest scoring story
highest_story = max(stories, key=lambda story: story["score"])

print("\nHighest scoring story:")
print("Title:", highest_story["title"])
print("Author:", highest_story["author"])
print("Score:", highest_story["score"])

# 3. Category counts
category_counts = {}

for story in stories:
    category = story["category"]

    if category not in category_counts:
        category_counts[category] = 0

    category_counts[category] += 1

print("\nCategory counts:")

for category, count in category_counts.items():
    print(f"{category}: {count}")

# 4. Average score by category
category_scores = {}

for story in stories:
    category = story["category"]
    score = story["score"]

    if category not in category_scores:
        category_scores[category] = []

    category_scores[category].append(score)

print("\nAverage score by category:")

for category, scores_list in category_scores.items():
    average = statistics.mean(scores_list)
    print(f"{category}: {round(average, 2)}")