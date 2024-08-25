# Recipe Finder

## Theme
The theme I chose for this project is a **food web app** that allows users to search for recipes based on their preferences, such as cuisine, diet, and meal type. Eventually, I plan to extend this app to include personalized meal planning features.

## Challenges Encountered and Solutions

### 1. Dynamic Queries Based on User Input
**Issue:** I faced difficulties adding different queries based on the user’s input, such as filtering recipes by cuisine, diet, and meal type.

**Solution:** I created dynamic query strings that change based on user inputs, allowing for customized searches. This was implemented by checking if each field was provided by the user and then appending it to the query string used to call the Spoonacular API.

### 2. Displaying Images Dynamically
**Issue:** Initially, the images were not displaying correctly because the API sometimes provided relative URLs instead of full URLs.

**Solution:** I handled this by checking if the image URL provided by the API was relative or absolute. If it was relative, I appended the necessary base URL to display the image correctly on the site.

### 3. Adding Another Endpoint for Detailed Recipe Information
**Issue:** I needed to create an additional endpoint to display detailed recipe information, including ingredients and nutritional details, but I wasn't sure how to manage multiple routes in Flask initially.

**Solution:** I separated the functionality into distinct routes in my Flask application. The main route displays search results, while a secondary route fetches and displays detailed recipe information based on the recipe ID.

## Known Problems
Currently, there are no major issues with the project. However, minor improvements and refinements are always ongoing.

## Future Improvements
In the future, I plan to expand this project by adding a **meal planning feature**. This feature will allow users to create and manage meal plans based on their dietary preferences, nutritional goals, and recipe preferences.

