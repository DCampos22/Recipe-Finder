import requests
import json
import os

API_KEY = os.environ.get('SPOONACULAR_API_KEY')
url = f'https://api.spoonacular.com/recipes/complexSearch?cuisine=italian&apiKey={API_KEY}'
title_to_find = "Turkey Tomato Cheese Pizza"

response = requests.get(url)
json_body = response.json()


print(json.dumps(json_body, indent=2))

# Normalize the title for comparison
title_to_find = title_to_find.lower().strip()

found_recipe = None
for recipe in json_body.get("results", []):
    recipe_title = recipe.get("title", "").lower().strip()
    if recipe_title == title_to_find:
        found_recipe = recipe
        break

if found_recipe:
    print("Recipe found:")
    print(json.dumps(found_recipe, indent=2))
else:
    print(f"No recipe found with the title '{title_to_find}'")
