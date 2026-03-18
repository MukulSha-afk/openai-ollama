import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import random

df_food = pd.read_excel("Anuvaad_INDB_2024.11.xlsx")
df_food = df_food[["food_name","energy_kcal","protein_g","fat_g","carb_g"]].dropna()

HISTORY_FILE = "user_history.csv"

if os.path.exists(HISTORY_FILE):
    df_history = pd.read_csv(HISTORY_FILE)
else:
    df_history = pd.DataFrame(columns=["age","weight","goal","meal_time","food_name"])
    df_history.to_csv(HISTORY_FILE, index=False)

def calculate_calories(age, height, weight, goal):
    bmr = 10*weight + 6.25*height - 5*age + 5
    tdee = bmr * 1.2

    if goal == "Weight Loss":
        return tdee - 500
    elif goal == "Muscle Gain":
        return tdee + 300
    else:
        return tdee

import random

def predict_food(age, height, weight, goal, meal_time):

    daily_cal = calculate_calories(age, height, weight, goal)

    # 🎯 Calorie range per meal
    meal_calorie = daily_cal / 3

    # Filter foods near meal calories
    filtered = df_food[
        (df_food["energy_kcal"] >= meal_calorie * 0.8) &
        (df_food["energy_kcal"] <= meal_calorie * 1.2)
    ]

    if filtered.empty:
        filtered = df_food.copy()

    # Goal based sorting
    if goal == "Muscle Gain":
        filtered = filtered.sort_values("protein_g", ascending=False)

    elif goal == "Weight Loss":
        filtered = filtered.sort_values("energy_kcal")

    else:
        filtered = filtered.sample(frac=1)

    # Pick random from top 10
    top_choices = filtered.head(10)
    food_pred = random.choice(top_choices["food_name"].values)

    nutrition = df_food[df_food["food_name"] == food_pred].iloc[0].to_dict()

    return {
        "food": food_pred,
        "nutrition": nutrition,
        "calories_target": daily_cal
    }

    # Save history
    new_entry = pd.DataFrame([[age,weight,goal,meal_time,food_pred]],
                             columns=["age","weight","goal","meal_time","food_name"])
    df_history = pd.concat([df_history,new_entry])
    df_history.to_csv(HISTORY_FILE, index=False)

    nutrition = df_food[df_food["food_name"]==food_pred].iloc[0].to_dict()

    return {
        "food": food_pred,
        "nutrition": nutrition,
        "calories_target": calculate_calories(age,height,weight,goal)
    }