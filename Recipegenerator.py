import streamlit as st
import requests
import openai
import pandas as pd
import os
from dotenv import load_dotenv


# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

openai.api_key = openai_api_key

# Set page configuration
st.set_page_config(
    page_title="Hot Girls Plan Meals",  # Title of the browser tab
    page_icon="🍜",  # You can use an emoji or a local file path
    layout="centered",  # Options: "centered" or "wide"
    initial_sidebar_state="collapsed"  # Options: "expanded", "collapsed", "auto"
)
# Function to calculate macronutrients with OpenAI
def calculate_macronutrients_with_ai(recipe_text):
    prompt = (
        f"The following recipe needs macronutrient analysis (protein, fat, carbohydrates, and total calories) per ingredient, and totals for all. Ensure measurements are in grams (European metric standard):\n\n"
        f"{recipe_text}\n\n"
        f"Provide a table with columns: Ingredient, Protein (g), Fat (g), Carbohydrates (g), and Calories (kcal). Include totals in the last row."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in food nutrition analysis and European measurement standards."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error calculating macronutrients: {e}")
        return "Error in macronutrient analysis."

# Function to generate recipes using OpenAI
def generate_recipe_with_ai(cuisine, meal_type, calories, ingredients, protein_grams):
    prompt = (
        f"Create a {meal_type} recipe for {cuisine} cuisine with the following constraints:\n"
        f"- Maximum calories: {calories} kcal\n"
        f"- Minimum protein: {protein_grams} g\n"
        f"- Ingredients to include: {', '.join(ingredients) if ingredients else 'any'}\n"
        f"Provide the recipe name, ingredients with quantities in grams (European metric standards), and detailed instructions."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative assistant that ensures recipes use European measurement standards. Focus on high protein meals and don't use meat substitutes"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating recipe with AI: {e}")
        return "Error generating recipe."

# Streamlit UI
st.title("🍒 Hot Girls Plan Meals 🍑")
st.write("Generate recAIpes tailored to your preferences and calorie goals!")

# Input fields
cuisine = st.selectbox("Preferred Cuisine", ["Any", "Italian", "Indian", "Mexican", "Asian", "Dutch", "Belgian", "American", "Greek", "Turkish", "Spanish"])
meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
calories = st.slider("Max Calories per Serving", 100, 800, 300)
protein_grams = st.slider("Minimum Protein (g)", 0, 100, 20)
ingredients = st.text_input("Ingredients to Include (comma-separated)").split(",")

# Generate recipe
if st.button("Generate Recipe 🪄"):
    ai_recipe = generate_recipe_with_ai(cuisine, meal_type, calories, ingredients, protein_grams)
    if "Error" not in ai_recipe:
        st.subheader("AI-Generated Recipe")
        st.write(ai_recipe)

        # Calculate and display macronutrient information for AI-generated recipe
        st.write("### Macronutrient Breakdown by Ingredient")
        macronutrient_analysis = calculate_macronutrients_with_ai(ai_recipe)
        st.markdown(macronutrient_analysis)
    else:
        st.error("Failed to generate recipe with AI.")

# Save functionality
if st.button("Save Recipe"):
    st.success("Recipe saved successfully!")
