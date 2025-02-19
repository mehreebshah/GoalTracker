import streamlit as st
import json
import datetime
import random
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='Goal Tracker', page_icon='📈', layout='wide')

st.title('📈 Goal Tracker & Motivation Hub')

# Motivational Quotes
quotes = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
    "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
    "Great things are done by a series of small things brought together. – Vincent Van Gogh"
]

st.write("💡 **Motivational Quote:**")
st.success(random.choice(quotes))

# Load & Save Goals
def load_goals():
    try:
        with open('goals.json', 'r') as file:
            goals = json.load(file)
            if isinstance(goals, list):
                for g in goals:
                    if "priority" not in g:
                        g["priority"] = "Not Set"  # Default value
            return goals
    except (FileNotFoundError, json.JSONDecodeError):
        return []
def save_goals(goals):
    with open('goals.json', 'w') as file:
        json.dump(goals, file, indent=4)

# Goal Input
goal = st.text_input('Enter your Goal:')
priority = st.selectbox("📌 Set Priority:", ["High", "Medium", "Low"])
deadline = st.date_input("Set a Deadline:", min_value=datetime.date.today())


if st.button('Save Goal'):
    if goal:
        goals = load_goals()
        new_goal = {
            "goal": goal,
            "priority": priority,
            "deadline": str(deadline),
            "progress": 0,
            "streak": 0,
            
        }
        goals.append(new_goal)
        save_goals(goals)
        st.success(f"🎯 Goal Added: {goal} (Priority: {priority}, Deadline: {deadline})")
    else:
        st.warning("Please enter a goal before saving!")

# Display Goals
st.title('📜 **Your Goals:**')
goals = load_goals()
updated = False

for index, g in enumerate(goals):
    if "goal" in g:
        st.write(f"✅ **{g['goal']}** | 📌 Priority: {g['priority']} | ⏳ Deadline: {g.get('deadline', 'Not Set')}")

        # Unique Key for each slider
        progress = st.slider(
            f"📊 Progress for '{g['goal']}'", 
        0, 100, 
        g.get("progress", 0),
         key=f"progress_{index}"  # Adding unique key
)
        if progress > g.get("progress", 0):
            goals[index]["progress"] = progress
            goals[index]["streak"] = goals[index].get("streak", 0) + 1  # Increase streak when progress is made
            updated = True

        
# Check if the deadline is approaching
        if "deadline" in g:
            goal_deadline = datetime.datetime.strptime(g["deadline"], "%Y-%m-%d").date()
            days_left = (goal_deadline - datetime.date.today()).days

            if days_left == 1:
                st.warning(f"⏳ Reminder: Your goal **'{g['goal']}'** is due **tomorrow!** Keep going! 💪")
                
# Save updates
if updated:
    save_goals(goals)

# 🔥 Streak Tracker
st.subheader("🔥 Streak Tracker")
for g in goals:
    st.write(f"🏆 **{g['goal']}** - {g.get('streak', 0)} day streak!")


# 📊 Goal Progress Visualization
st.subheader("📈 Goal Progress Over Time")

if goals:
    # Sorting goals by progress (optional)
    sorted_goals = sorted(goals, key=lambda x: x.get("progress", 0), reverse=True)

    goal_names = [g["goal"] for g in sorted_goals]
    progress_values = [g["progress"] for g in sorted_goals]

    # Generate a list of indices for x-axis (to track goals sequentially)
    x_values = np.arange(len(goal_names))

    # Create figure & axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot Line Graph
    ax.plot(x_values, progress_values, marker="o", linestyle="-", color="#2E86C1", linewidth=2, markersize=8, markerfacecolor="white", markeredgewidth=2, label="Goal Progress")

    # Add labels for each point
    for i, txt in enumerate(progress_values):
        ax.text(x_values[i], progress_values[i] + 2, f"{txt}%", ha="center", fontsize=10, fontweight="bold")

    # Customize appearance
    ax.set_ylabel("Progress (%)", fontsize=12)
    ax.set_xlabel("Goals", fontsize=12)
    ax.set_title("📈 Goal Progress Trend", fontsize=14, fontweight="bold")
    ax.set_xticks(x_values)
    ax.set_xticklabels(goal_names, rotation=30, ha="right")
    ax.set_ylim(0, 110)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
    # Show the graph in Streamlit
    st.pyplot(fig)

# 🏆 Achievement Badges
st.subheader("🏆 Achievements")
for g in goals:
    if g.get("progress", 0) >= 100:
        st.success(f"🎖️ **{g['goal']}** - Completed! Well done! 🏆")
    elif g.get("streak", 0) >= 5:
        st.info(f"🔥 **{g['goal']}** - 5-Day Streak! Keep it up!")

# Daily Reflection Journal
st.subheader("📝 Daily Reflection Journal")
reflection = st.text_area("What did you learn today?", placeholder="Write about your daily learning experience...")

if st.button("Save Reflection"):
    if "reflections" not in st.session_state:
        st.session_state.reflections = []
    st.session_state.reflections.append(reflection)
    st.success("Your reflection has been saved!")

# Display saved reflections
if "reflections" in st.session_state:
    st.write("📖 **Your Past Reflections:**")
    for i, ref in enumerate(st.session_state.reflections, 1):
        st.write(f"📌 {i}. {ref}")
