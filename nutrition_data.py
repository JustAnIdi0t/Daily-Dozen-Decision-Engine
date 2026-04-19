import json
import os

def load_food_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'food_data.json')
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

RAW_DATA = load_food_data()
FOOD_LIBRARY = {category: list(items.keys()) for category, items in RAW_DATA.items()}
NUTRITION_DATA = {}
for category in RAW_DATA.values():
    NUTRITION_DATA.update(category)

DAILY_DOZEN_TARGETS = {
    "Beans": 3, "Berries": 1, "Other Fruits": 3, "Cruciferous Veg": 1,
    "Greens": 2, "Other Veggies": 2, "Whole Grains": 3, "Nuts & Seeds": 1
}

WEEKLY_TARGETS = {
    "calories": 14000, "protein": 350, "fiber": 210, "iron": 126,
    "calcium": 7000, "vitamin_c": 630, "zinc": 77, "omega_3": 11.2
}

CONVERSION_FACTORS = {
    "Lentils": 2.5, "Chickpeas": 2.2, "Black Beans": 2.2,
    "Quinoa": 3.0, "Brown Rice": 3.0, "Oats": 2.5,
    "Spinach": 0.2, "Mushrooms": 0.7, "Kale": 0.5
}

SERVING_SIZES = {
    "Beans": 130, "Whole Grains": 100, "Greens": 50, "Berries": 75,
    "Cruciferous Veg": 80, "Other Veggies": 100, "Other Fruits": 150, "Nuts & Seeds": 30
}

FOOD_TIPS = {
    "Lentils": "Pair with Vit-C to triple absorption.",
    "Broccoli": "Chop 40m early for sulforaphane.",
    "Spinach": "High-oxalate; steam or rotate with kale.",
    "Chia Seeds": "Massive ALA source for brain health."
}

def get_best_sources(nutrient, limit=3):
    sources = [(item, stats[nutrient]) for item, stats in NUTRITION_DATA.items() if nutrient in stats]
    sources.sort(key=lambda x: x[1], reverse=True)
    return sources[:limit]