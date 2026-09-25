import json
import matplotlib.pyplot as plt

# Load processed data
with open("processed_data.json", "r", encoding="utf-8") as file:
    stories = json.load(file)

# Count stories by category
category_counts = {}

for story in stories:
    category = story["category"]

    if category not in category_counts:
        category_counts[category] = 0

    category_counts[category] += 1

# Prepare data for the chart
categories = list(category_counts.keys())
counts = list(category_counts.values())

# Create bar chart
plt.figure(figsize=(10, 6))

plt.bar(categories, counts)

plt.title("Number of Hacker News Stories by Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=45)

plt.tight_layout()

# Save the chart
plt.savefig("category_distribution.png")

# Display the chart
plt.show()

print("Visualization saved to category_distribution.png")