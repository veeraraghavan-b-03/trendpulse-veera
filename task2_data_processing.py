import json

# Load the raw data
with open("raw_data.json", "r", encoding="utf-8") as file:
    stories = json.load(file)

print("Total stories loaded:", len(stories))

# Display the first story
print("\nFirst story:")
print(stories[0])

# Check for missing values
print("\nMissing values:")

for field in ["post_id", "title", "category", "score", "num_comments", "author"]:
    missing = sum(
        1 for story in stories
        if story.get(field) is None or story.get(field) == ""
    )
    print(f"{field}: {missing}")

    # Clean and standardize the data

for story in stories:
    story["title"] = story["title"].strip()
    story["category"] = story["category"].strip()
    story["author"] = story["author"].strip()

    story["score"] = int(story["score"])
    story["num_comments"] = int(story["num_comments"])


# Remove duplicate stories based on post_id

unique_stories = {}
for story in stories:
    unique_stories[story["post_id"]] = story

stories = list(unique_stories.values())


print("\nData cleaning completed.")
print("Total stories after cleaning:", len(stories))


# Save processed data

with open("processed_data.json", "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=4)

print("Processed data saved to processed_data.json")

