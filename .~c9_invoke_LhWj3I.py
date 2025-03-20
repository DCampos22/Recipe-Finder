import flask
import os
import requests
import json

app = flask.Flask(__name__)


@app.route('/')
def index():
    API_KEY = '5c54397af8994b99a2e0599c9cdb53f3'  

    # Get user input for search query, cuisine, diet, max protein, and type
    query = flask.request.args.get('query', '')
    cuisine = flask.request.args.get('cuisine', '')
    diet = flask.request.args.get('diet', '')
    max_protein = flask.request.args.get('max_protein', '')
    meal_type = flask.request.args.get('type', '')

    # Log the input for debugging
    print("User input -> Query: " + query)
    print("User input -> Cuisine: " + cuisine)
    print("User input -> Diet: " + diet)
    print("User input -> Max Protein: " + max_protein)
    print("User input -> Type: " + meal_type)

    # Construct the API request URL using string concatenation
    url = 'https://api.spoonacular.com/recipes/complexSearch?apiKey=' + API_KEY
    if query:
        url += '&query=' + query
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

    # Extract relevant data (image, source URL, and ready in minutes)
    recipes = []
    for recipe in json_body.get('results', []):
        recipe_id = recipe.get('id')
        
        # Fetch additional information about the recipe
        info_url = 'https://api.spoonacular.com/recipes/{}/information?includeNutrition=false&apiKey={}'.format(recipe_id, API_KEY)
        info_response = requests.get(info_url)
        info_json = info_response.json()
        
        recipes.append({
            'id': recipe_id,
            'title': recipe.get('title'),
            'image': recipe.get('image'),
            'sourceUrl': info_json.get('sourceUrl'),
            'readyInMinutes': info_json.get('readyInMinutes')
        })

    return flask.render_template("index.html", recipes=recipes)
    
    
@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    API_KEY = '5c54397af8994b99a2e0599c9cdb53f3'  # Replace with your actual API key
    
    # Fetch recipe information with nutrition data disabled
    recipe_url = 'https://api.spoonacular.com/recipes/{}/information?includeNutrition=false&apiKey={}'.format(recipe_id, API_KEY)
    response = requests.get(recipe_url)
    recipe_info = response.json()

    # Extract ingredients
    ingredients = [ingredient['original'] for ingredient in recipe_info.get('extendedIngredients', [])]

    # Optionally, if you want to fetch nutritional information separately
    # Fetch nutritional information (if needed)
    nutrients_url = 'https://api.spoonacular.com/recipes/{}/nutritionWidget.json?apiKey={}'.format(recipe_id, API_KEY)
    nutrients_response = requests.get(nutrients_url)
    nutrients_info = nutrients_response.json()

    # Return the recipe details and nutritional information
    return flask.render_template("recipe.html",
                                 title=recipe_info.get('title'),
                                 image=recipe_info.get('image'),
                                 ingredients=ingredients,
                                 nutrients=nutrients_info)
    

# Run the app
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)
