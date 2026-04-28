// Gets user input for season and plant type
function getUserInput() {
    const season = prompt("Enter season (summer/winter):").toLowerCase();
    const plantType = prompt("Enter plant type (flower/vegetable):").toLowerCase();
    return { season, plantType };
}

// Advice data
const adviceData = {
    seasons: {
        summer: "Water your plants regularly and provide some shade.",
        winter: "Protect your plants from frost with covers."
    },
    plants: {
        flower: "Use fertiliser to encourage blooms.",
        vegetable: "Keep an eye out for pests!"
    }
};

// Returns advice based on season
function getSeasonAdvice(season) {
    return adviceData.seasons[season] || "No advice for this season.";
}

// Returns advice based on plant type
function getPlantAdvice(plantType) {
    return adviceData.plants[plantType] || "No advice for this type of plant.";
}

// Main function to generate and display advice
function generateAdvice() {
    const { season, plantType } = getUserInput();

    let advice = "";
    advice += getSeasonAdvice(season) + "\n";
    advice += getPlantAdvice(plantType);

    console.log(advice);
}

// Run app
generateAdvice();