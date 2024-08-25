import flask
import os
import requests
import json

app = flask.Flask(__name__)

@app.route('/')
def index():
    API_KEY = '2bb32b28f20f4f639f15dfa0200c703c'  # Replace with your actual API key

    # Get user input for cuisine, diet, max protein, and type
    cuisine = flask.request.args.get('cuisine', '')
    diet = flask.request.args.get('diet', '')
    max_protein = flask.request.args.get('max_protein', '')
    meal_type = flask.request.args.get('type', '')

    # Log the input for debugging
    print("User input -> Cuisine: " + cuisine)
    print("User input -> Diet: " + diet)
    print("User input -> Max Protein: " + max_protein)
    print("User input -> Type: " + meal_type)

    # Construct the API request URL using string concatenation
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=' + API_KEY
    if cuisine:
        url += '&cuisine=' + cuisine
    if diet:
        url += '&diet=' + diet
    if max_protein:
        url += '&maxProtein=' + max_protein
    if meal_type:
        url += '&type=' + meal_type

    # Log the full URL for debugging
    print("API Request URL: " + url)
    
    response = requests.get(url)
    json_body = response.json()
    
    # Log the JSON response for debugging
    print("API Response: " + json.dumps(json_body, indent=2))
    
    # Extract relevant data (image and source URL)
    recipes = []
    for recipe in json_body.get('results', []):
        image_url = recipe.get('image')
        recipes.append({
            'id': recipe.get('id'),
            'title': recipe.get('title'),
            'image': image_url,
            'sourceUrl': recipe.get('sourceUrl')
        })

    return flask.render_template("index.html", recipes=recipes)

# Route to display recipe details and ingredients
@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    API_KEY = '2bb32b28f20f4f639f15dfa0200c703c'  # Replace with your actual API key
    
    # Fetch recipe information
    recipe_url = 'https://api.spoonacular.com/recipes/' + str(recipe_id) + '/information?apiKey=' + API_KEY
    response = requests.get(recipe_url)
    recipe_info = response.json()
    
    ingredients = [ingredient['original'] for ingredient in recipe_info['extendedIngredients']]
    
    # Fetch nutritional information
    nutrients_url = 'https://api.spoonacular.com/recipes/' + str(recipe_id) + '/nutritionWidget.json?apiKey=' + API_KEY
    response = requests.get(nutrients_url)
    nutrients_info = response.json()

    return flask.render_template("recipe.html", 
                                 title=recipe_info['title'], 
                                 image=recipe_info['image'], 
                                 ingredients=ingredients,
                                 nutrients=nutrients_info)

# Run the app
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)