import streamlit as st
import pandas as pd
from nutrition_app import load_models, predict_goal, predict_calories, recommend_plan


st.set_page_config(page_title="Fitness Planner", page_icon="🏋️", layout="wide")
st.title("🏋️ Fitness Goal & Diet Planner")
st.markdown(
    "Fill in your details to generate a personalized plan. "
    "Models will be used if available; otherwise safe fallbacks apply."
)

st.info(
    "For Android emulator access, start Streamlit with `--server.address 0.0.0.0` and use "
    "`http://10.0.2.2:8501` from the emulator browser."
)

# Load models (may be None if files missing)
models = load_models(base_path=".")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
    age = st.slider("Age", 15, 80, 30)
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.70)

with col2:
    water = st.number_input("Water Intake (liters/day)", min_value=0.0, max_value=10.0, value=2.0)
    exp = st.selectbox("Experience Level", [1, 2, 3], index=1, format_func=lambda x: {1: "Beginner", 2: "Intermediate", 3: "Advanced"}[x])
    workout = st.slider("Workout Days per Week", 0, 7, 3)
    bpm = st.number_input("Resting BPM", min_value=30.0, max_value=200.0, value=70.0)

if st.button("🚀 Generate My Plan", use_container_width=True):
    # Build user dict
    user_input = {
        "Gender": int(gender),
        "Age": int(age),
        "Weight (kg)": float(weight),
        "Height (m)": float(height),
        "Water_Intake (liters)": float(water),
        "Experience_Level": int(exp),
        "Workout_Frequency (days/week)": int(workout),
        "Resting_BPM": float(bpm),
    }

    # Predict using loaded models or fallbacks
    goal_pred = predict_goal(models.get("goal"), user_input)
    calories_pred = predict_calories(models.get("calories"), user_input)

    plan = recommend_plan(user_input, goal_pred, calories_pred)

    st.success("✅ Your personalized plan is ready!")
    st.divider()

    st.subheader("🎯 Your Goal")
    st.info(plan["goal"])

    st.subheader("📊 BMI Check")
    st.write(plan.get("bmi_note"))

    st.subheader("🔥 Daily Calorie Target")
    st.metric(label="Calories", value=f"{plan['calories_target']} kcal")

    st.subheader("🥗 Diet Type")
    st.write(plan.get("diet"))

    st.subheader("🍽️ Meal Plan")
    meals = plan.get("meals", {})
    keys = list(meals.keys())
    if keys:
        c1, c2, c3 = st.columns(min(3, len(keys)))
        cols = [c1, c2, c3]
        for i, k in enumerate(keys):
            with cols[i]:
                st.markdown(f"**{k}**")
                for item in meals[k]:
                    st.write(f"- {item}")

    st.subheader("🏃 Exercise Plan")
    for ex in plan.get("exercise_plan", []):
        st.write(f"- {ex}")

    st.subheader("💧 Water Intake Advice")
    st.write(plan.get("water_advice"))

    st.subheader("❤️ Heart Health")
    st.write(plan.get("health_note"))
