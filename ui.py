# ui.py
import streamlit as st
import pandas as pd
from agent_logic import parse_goal_request

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🎾 AI Goal Planner", layout="wide")

st.title("🎯 Tennis Diary - AI Goal Planner")
st.write("Set, view, and manage your tennis goals with AI assistance.")

# --- Initialize session storage ---
if "goals" not in st.session_state:
    st.session_state.goals = []

if "selected_goal" not in st.session_state:
    st.session_state.selected_goal = None


# --- Sidebar Section ---
st.sidebar.header("📌 My Goals")

# Clear all goals button
if st.sidebar.button("🧹 Clear All Goals"):
    st.session_state.goals = []
    st.session_state.selected_goal = None
    st.rerun()

# Display clickable goals in sidebar
if st.session_state.goals:
    for idx, goal in enumerate(st.session_state.goals):
        goal_name = goal.get("Subject", f"Goal {idx+1}")
        if st.sidebar.button(f"🏆 {goal_name}", key=f"goal_{idx}"):
            st.session_state.selected_goal = idx
else:
    st.sidebar.info("No goals yet. Add one below!")


# --- Add New Goal Section ---
st.subheader("🗣️ Add a New Goal")

# Wrap input in a form to prevent repeated runs
with st.form("add_goal_form", clear_on_submit=True):
    user_input = st.text_input(
        "💬 Describe your goal:",
        placeholder="e.g., Add a technical goal to improve my serve accuracy before next Sunday."
    )
    submitted = st.form_submit_button("➕ Add Goal")

# Only trigger logic when submitted
if submitted and user_input:
    with st.spinner("Thinking..."):
        result = parse_goal_request(user_input)

    if "error" in result:
        st.error(result["error"])
        st.code(result["raw_response"])
    else:
        st.session_state.goals.append(result)
        st.session_state.selected_goal = len(st.session_state.goals) - 1
        st.success(f"✅ Goal '{result.get('Subject', 'Unnamed Goal')}' added successfully!")
        st.rerun()


# --- Display Goals in Table ---
st.subheader("📋 My Goals (Session)")

if st.session_state.goals:
    df = pd.DataFrame(st.session_state.goals)
    preferred_order = ["Goal Type", "Topic", "Subject", "Date", "Time", "About Goal"]
    df = df[[col for col in preferred_order if col in df.columns]]
    st.dataframe(df, use_container_width=True)
else:
    st.info("No goals added yet. Describe one above!")


# --- Selected Goal Details (View & Edit) ---
if st.session_state.selected_goal is not None:
    st.markdown("---")
    goal = st.session_state.goals[st.session_state.selected_goal]
    st.subheader(f"🎯 Selected Goal: {goal.get('Subject', 'Unnamed Goal')}")

    # Editable form for selected goal
    with st.form(f"edit_goal_{st.session_state.selected_goal}"):
        col1, col2 = st.columns(2)
        with col1:
            goal_type = st.text_input("Goal Type", goal.get("Goal Type", ""))
            topic = st.text_input("Topic", goal.get("Topic", ""))
            subject = st.text_input("Subject", goal.get("Subject", ""))
        with col2:
            date = st.text_input("Date", goal.get("Date", ""))
            time = st.text_input("Time", goal.get("Time", ""))
            about = st.text_area("About Goal", goal.get("About Goal", ""))

        save = st.form_submit_button("💾 Save Changes")
        if save:
            updated_goal = {
                "Goal Type": goal_type,
                "Topic": topic,
                "Subject": subject,
                "Date": date,
                "Time": time,
                "About Goal": about,
            }
            st.session_state.goals[st.session_state.selected_goal] = updated_goal
            st.success("✅ Goal updated successfully!")
            st.rerun()

    # Delete goal button
    if st.button("🗑️ Delete This Goal"):
        del st.session_state.goals[st.session_state.selected_goal]
        st.session_state.selected_goal = None
        st.success("🗑️ Goal deleted successfully!")
        st.rerun()
