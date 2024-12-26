const texts = ['Breakfast ?', 'Lunch ?', 'Dinner ?'];
const images = [
    'https://myeverydaytable.com/wp-content/uploads/FullEnglishBreakfast-7.jpg',
    'https://bellyfull.net/wp-content/uploads/2023/03/Million-Dollar-Spaghetti-Alfredo-blog-2.jpg',
    'https://www.calgarycoop.com/wp-content/uploads/2023/07/restaurant-style-steak-dinner.jpeg',
];

let index = 0;
const typedTextElement = document.getElementById("typed-text");
const foodImageElement = document.getElementById("food-image");

function typeText(text, callback) {
    let i = 0;
    typedTextElement.textContent = ''; // Clear previous text
    const typingInterval = setInterval(() => {
        if (i < text.length) {
            typedTextElement.textContent += text.charAt(i);
            i++;
        } else {
            clearInterval(typingInterval);
            setTimeout(callback, 1250); // Wait before moving to the next
        }
    }, 210); // Adjust typing speed here
}

function showImage(index) {
    foodImageElement.style.opacity = 0; // Fade out
    setTimeout(() => {
        foodImageElement.src = images[index]; // Change image
        foodImageElement.style.opacity = 1; // Fade in
    }, 1550); // Adjust timing for seamless transition
}

function startTypingAnimation() {
    typeText(texts[index], () => {
        index = (index + 1) % texts.length; // Move to next text
        showImage(index);
        setTimeout(startTypingAnimation, 1970); // Wait before next text
    });
}

// Start the animation
startTypingAnimation();

const apiKey = 'c964e9508dad440cb0220a49bd3e0b1e'; // Replace with your API key

// Element references
const searchButton = document.getElementById('search-button');
const recipeSearch = document.getElementById('recipe-search');
const recipeResults = document.querySelector('.recipe-results');

// Event listener for search button
searchButton.addEventListener('click', () => {
    const query = recipeSearch.value.trim();
    if (query) {
        fetchRecipes(query);
    }
});

// Function to fetch recipes from Spoonacular API
async function fetchRecipes(query) {
    try {
        // Fetch recipes using Spoonacular API
        const response = await fetch(`https://api.spoonacular.com/recipes/complexSearch?query=${query}&apiKey=${apiKey}&number=10`);
        const data = await response.json();

        // Clear previous results
        recipeResults.innerHTML = '';

        // Check if recipes are found
        if (data.results && data.results.length > 0) {
            data.results.forEach(recipe => {
                const recipeCard = document.createElement('div');
                recipeCard.classList.add('recipe-card');
                
                // Create a link to the recipe details page with the recipe ID as a parameter
                const link = document.createElement('a');
                link.href = `recipe-details.html?id=${recipe.id}`;  // Link to recipe details page with the recipe ID

                // Add image and title for each recipe
                link.innerHTML = `
                    <img src="${recipe.image}" alt="${recipe.title}">
                    <h3>${recipe.title}</h3>
                `;

                // Append the link to the recipe card and the card to the results
                recipeCard.appendChild(link);
                recipeResults.appendChild(recipeCard);
            });
        } else {
            recipeResults.innerHTML = '<p>No recipes found.</p>';
        }
    } catch (error) {
        console.error('Error fetching recipes:', error);
        recipeResults.innerHTML = '<p>Error fetching recipes. Please try again.</p>';
    }
}
// Example for adding the title in the search results
link.innerHTML = `
    <img src="${recipe.image}" alt="${recipe.title}">
    <h3>${recipe.title}</h3>
`;

// Sample recipes for demonstration
const recipes = [
    "Spaghetti Carbonara",
    "Chicken Alfredo",
    "Beef Stroganoff",
    "Vegan Salad Bowl",
    "Chocolate Chip Cookies",
    "Blueberry Pancakes",
    "Grilled Cheese Sandwich",
];

// Filter suggestions as user types
function filterSuggestions() {
    const searchInput = document.getElementById("search-bar").value.toLowerCase();
    const suggestionsContainer = document.getElementById("suggestions");
    
    // Clear previous suggestions
    suggestionsContainer.innerHTML = "";
    if (searchInput === "") {
        suggestionsContainer.style.display = "none";
        return;
    }

    // Filter recipes
    const filteredRecipes = recipes.filter(recipe =>
        recipe.toLowerCase().includes(searchInput)
    );

    // Populate suggestions
    filteredRecipes.forEach(recipe => {
        const suggestion = document.createElement("div");
        suggestion.textContent = recipe;
        suggestion.onclick = () => selectSuggestion(recipe);
        suggestionsContainer.appendChild(suggestion);
    });

    suggestionsContainer.style.display = filteredRecipes.length ? "block" : "none";
}

// Select a suggestion and show loading screen
function selectSuggestion(recipe) {
    document.getElementById("search-bar").value = recipe;
    document.getElementById("suggestions").style.display = "none";

    // Simulate loading
    showLoading();
}

// Show the loading screen
function showLoading() {
    const loadingScreen = document.getElementById("loading-screen");
    loadingScreen.classList.add("show");
    
    // Simulate loading duration
    setTimeout(() => {
        loadingScreen.classList.remove("show");
        // Navigate or fetch data here after loading
        console.log("Loading complete!");
    }, 2000); // Adjust duration as needed
}
