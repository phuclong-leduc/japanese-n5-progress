# This program shows the current Japanese learning progress of Le Duc Phuc Long
# (and was made by him too! =))

import streamlit as st
from datetime import date, timedelta

# --- Page Configuration ---
# This should be the first Streamlit command in your script
st.set_page_config(
    page_title="Le Duc Phuc Long's Japanese Journey",
    page_icon="🇯🇵",
    layout="centered"
)

# --- Calculation Logic ---
# This function remains the same as its logic is independent of the UI
def calculate_progress(start_date, lessons_in_course, days_per_lesson):
    """Calculates all the necessary progress details."""
    today = date.today()
    days_passed = (today - start_date).days

    # Return None if the start date is in the future
    if days_passed < 0:
        return None

    current_lesson_number = (days_passed // days_per_lesson) + 1
    day_in_current_lesson = (days_passed % days_per_lesson) + 1
    
    total_days_for_course = lessons_in_course * days_per_lesson
    estimated_end_date = start_date + timedelta(days=total_days_for_course - 1)

    # Calculate completion percentage, ensuring it doesn't go over 100
    completion_percentage = min(100.0, (days_passed / total_days_for_course) * 100.0)

    return {
        "today": today,
        "current_lesson": current_lesson_number,
        "day_in_lesson": day_in_current_lesson,
        "completion_percentage": completion_percentage,
        "estimated_end": estimated_end_date,
        "course_completed": current_lesson_number > lessons_in_course
    }

# --- Sidebar for User Configuration ---
# Using a sidebar keeps the main area clean and focused on the dashboard
st.sidebar.header("My Study Plan")

# Interactive widgets to adjust the learning plan
start_date_input = st.sidebar.date_input(
    "Start Date", 
    date(2025, 10, 18)
)
lessons_in_course_input = st.sidebar.number_input(
    "Total Lessons in Course", 
    min_value=1, 
    value=25, 
    step=1
)
days_per_lesson_input = st.sidebar.number_input(
    "Days to Spend per Lesson", 
    min_value=1, 
    value=3, 
    step=1
)

# --- Main Page UI ---

# Header Section
st.title("🇯🇵 Le Duc Phuc Long's Japanese N5 Journey 🇯🇵")
st.caption(f"Today's Date: {date.today().strftime('%A, %B %d, %Y')}")

# Calculate progress based on the sidebar inputs
progress_data = calculate_progress(
    start_date_input,
    lessons_in_course_input,
    days_per_lesson_input
)

st.divider()

# --- Display Logic ---

# 1. Handle case where the start date is in the future
if progress_data is None:
    st.info(f"Your learning journey is scheduled to begin on **{start_date_input.strftime('%B %d, %Y')}**.", icon="🗓️")

# 2. Handle case where the course is already completed
elif progress_data['course_completed']:
    st.balloons()
    st.success("🎉 Congratulations! You have completed the course! 🎉", icon="🏆")
    st.metric(
        label="Estimated Completion Date",
        value=progress_data['estimated_end'].strftime('%B %d, %Y')
    )

# 3. Display the main progress dashboard
else:
    # Key Metrics in columns for a clean layout
    col1, col2 = st.columns(2)
    col1.metric(
        label="Current Focus",
        value=f"Lesson {progress_data['current_lesson']}"
    )
    col2.metric(
        label="Progress in Lesson",
        value=f"Day {progress_data['day_in_lesson']} of {days_per_lesson_input}"
    )

    st.text("") # Add a little vertical space
    
    # Course Overview section
    st.subheader("Course Overview")
    
    # Display the progress bar and the percentage text
    progress_percentage = int(progress_data['completion_percentage'])
    st.progress(progress_percentage, text=f"{progress_percentage}% Complete")
    
    st.info(f"Your estimated finish date is **{progress_data['estimated_end'].strftime('%B %d, %Y')}**.", icon="🏁")

# --- Footer ---
st.divider()
st.markdown("<h3 style='text-align: center; color: #88C0D0;'>頑張ってください (Ganbatte kudasai!)</h3>", unsafe_allow_html=True)
