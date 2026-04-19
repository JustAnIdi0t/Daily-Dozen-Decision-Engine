Daily Dozen Decision Engine 🥗
An AI-powered, data-driven meal prep coordinator based on the NutritionFacts.org "Daily Dozen" framework.

This tool moves beyond traditional recipe searching. Instead, it utilizes a "Component Cooking" philosophy—allowing you to prep isolated "hero" ingredients once a week that can be mixed and matched like a professional kitchen line (e.g., Chipotle), while ensuring 100% nutritional coverage.

🧠 The Philosophy
The core of this application is built on three pillars:

Synergy Logic: Understanding that nutrients don't work in isolation (e.g., Vitamin C triples non-heme iron absorption).

The Bucket System: Categorizing food into Dr. Michael Greger's essential groups (Cruciferous, Beans, Greens, etc.) to ensure no micronutrient is left behind.

Efficiency: Quantifying dry-to-cooked yields to minimize food waste and maximize prep speed for a 1x-per-week kitchen session.

✨ Features
Searchable Arsenal: Filter through a massive JSON database of plant-based whole foods.

Real-time Dashboard: Watch your weekly micronutrient progress bars (Iron, Zinc, Calcium, Omega-3s) update as you select your ingredients.

Nutritional Auditor: A "consultant" in the sidebar that identifies deficits and suggests "Best Source" fixes from your database.

Bioavailability Alerts: Sophisticated logic that warns you about high-oxalate traps or the need for "Hack & Hold" sulforaphane activation.

PDF Kitchen Guide: Export a clean, printable guide containing your quantified shopping list (in dry weights) and prep instructions.

🛠️ Technical Stack
Language: Python 3.x

GUI: CustomTkinter (Modernized UI/UX)

PDF Engine: FPDF

Data Structure: Modular JSON-based ingredient library

🚀 Getting Started
Prerequisites
Ensure you have Python installed and the following libraries:

Bash
pip install customtkinter fpdf
Installation
Clone the repository:

Bash
git clone https://github.com/YourUsername/Daily-Dozen-Decision-Engine.git
Navigate to the folder and run the app:

Bash
python main.py
Directory Structure
main.py: The application entry point.

app_gui.py: The interface, search engine, and PDF logic.

nutrition_data.py: The mathematical engine and conversion factors.

food_data.json: The "Arsenal" – fully customizable food database.

/Weekly_History: Automatic storage for your exported PDF guides.

⚖️ License
This project is for personal educational use. Nutritional data is sourced from USDA and NutritionFacts.org. Always consult with a healthcare professional regarding dietary changes.
