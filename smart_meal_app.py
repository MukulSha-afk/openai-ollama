import streamlit as st
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ===============================
# Load Food Dataset
# ===============================
df_food = pd.read_excel("Anuvaad_INDB_2024.11.xlsx")
df_food = df_food[["food_name","energy_kcal","protein_g","fat_g","carb_g"]].dropna()

# ===============================
# Load or Create User History
# ===============================
if os.path.exists("user_history.csv"):
    df_history = pd.read_csv("user_history.csv")
else:
    df_history = pd.DataFrame(columns=["age","weight","goal","meal_time","food_name"])
    df_history.to_csv("user_history.csv", index=False)

# ===============================
# Calorie Calculation
# ===============================
def calculate_calories(age, height, weight, goal):
    bmr = 10*weight + 6.25*height - 5*age + 5
    tdee = bmr * 1.2

    if goal == "Weight Loss":
        return tdee - 500
    elif goal == "Muscle Gain":
        return tdee + 300
    else:
        return tdee

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(layout="wide")
st.title("🤖 AI Predictive Meal Planner")

st.sidebar.header("User Input")

age = st.sidebar.slider("Age",18,60,25)
height = st.sidebar.slider("Height (cm)",140,200,170)
weight = st.sidebar.slider("Weight (kg)",40,120,70)
goal = st.sidebar.selectbox("Goal",["Weight Loss","Muscle Gain","Maintenance"])
meal_time = st.sidebar.selectbox("Meal Time",["Breakfast","Lunch","Dinner"])

# ===============================
# Train ML if history exists
# ===============================
if len(df_history) > 5:

    le_goal = LabelEncoder()
    le_meal = LabelEncoder()
    le_food = LabelEncoder()

    df_history["goal_enc"] = le_goal.fit_transform(df_history["goal"])
    df_history["meal_enc"] = le_meal.fit_transform(df_history["meal_time"])
    df_history["food_enc"] = le_food.fit_transform(df_history["food_name"])

    X = df_history[["age","weight","goal_enc","meal_enc"]]
    y = df_history["food_enc"]

    model = RandomForestClassifier()
    model.fit(X,y)

else:
    model = None

# ===============================
# Generate Prediction
# ===============================
if st.sidebar.button("Predict Meal"):

    daily_cal = calculate_calories(age,height,weight,goal)
    st.write("Daily Calorie Target:", round(daily_cal,2),"kcal")

    if model:
        goal_enc = le_goal.transform([goal])[0]
        meal_enc = le_meal.transform([meal_time])[0]

        input_data = pd.DataFrame([[age,weight,goal_enc,meal_enc]],
                                  columns=["age","weight","goal_enc","meal_enc"])

        pred = model.predict(input_data)[0]
        food_pred = le_food.inverse_transform([pred])[0]

        st.subheader("🔮 Predicted Food (ML Based)")
        st.success(food_pred)

    else:
        st.warning("Not enough history. Showing rule-based recommendation.")

        food_pred = df_food.sort_values("protein_g",ascending=False).iloc[0]["food_name"]
        st.success(food_pred)

    # Save to history
    new_entry = pd.DataFrame([[age,weight,goal,meal_time,food_pred]],
                             columns=["age","weight","goal","meal_time","food_name"])

    df_history = pd.concat([df_history,new_entry])
    df_history.to_csv("user_history.csv", index=False)

    st.subheader("📊 Food Nutrition Info")
    info = df_food[df_food["food_name"]==food_pred]
    st.dataframe(info)