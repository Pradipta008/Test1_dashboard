import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
data = pd.read_csv("student_historical_data.csv")

# Custom CSS for black background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📊 Student Performance Dashboard")

# Search bar
search_query = st.text_input("🔍 Search by Name, RollNo, or Class:", "")

# Filter data based on search
filtered_data = data[
    (data['Name'].str.contains(search_query, case=False)) |
    (data['RollNo'].astype(str).str.contains(search_query)) |
    (data['Class'].astype(str).str.contains(search_query))
]

# Display search results
if not filtered_data.empty:
    st.write("### Search Results")
    selected_student = st.selectbox(
        "Select a student:",
        filtered_data[['RollNo', 'Name', 'Class']].drop_duplicates().apply(
            lambda x: f"{x['Name']} (RollNo: {x['RollNo']}, Class: {x['Class']})", axis=1
        )
    )
    
    # Extract RollNo and Class from selection
    rollno = int(selected_student.split("RollNo: ")[1].split(",")[0])
    class_selected = int(selected_student.split("Class: ")[1].split(")")[0])
    
    # Get student's historical data
    student_data = data[(data['RollNo'] == rollno) & (data['Class'] == class_selected)]
    
    # Display student profile
    st.markdown("---")
    st.markdown(f"## 🧑🎓 Student Profile: **{student_data['Name'].iloc[0]}**")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Current Class", f"Class {class_selected}")
    with col2:
        st.metric("🎓 Average Score", f"{student_data[['Math', 'Science', 'English']].mean(axis=1).iloc[-1]:.1f}")
    with col3:
        st.metric("📅 Attendance", f"{student_data['Attendance'].iloc[-1]}%")
    
    # Historical trends
    st.write("### 📈 Performance Trends")
    fig = px.line(
        student_data,
        x='Year',
        y=['Math', 'Science', 'English'],
        markers=True,
        labels={'value': 'Score', 'variable': 'Subject'},
        color_discrete_sequence=['#FF4B4B', '#00FF00', '#00B4D8']
    )
    fig.update_layout(plot_bgcolor='#000000', paper_bgcolor='#000000', font_color='white')
    st.plotly_chart(fig)
    
    # Percentile scores
    st.write("### 📊 Percentile Scores (vs. Class)")
    current_year_data = data[(data['Class'] == class_selected) & (data['Year'] == student_data['Year'].max())]
    
    def calculate_percentile(subject):
        return (student_data[subject].iloc[-1] > current_year_data[subject]).mean() * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧮 Math Percentile", f"{calculate_percentile('Math'):.1f}%")
    with col2:
        st.metric("🔬 Science Percentile", f"{calculate_percentile('Science'):.1f}%")
    with col3:
        st.metric("📖 English Percentile", f"{calculate_percentile('English'):.1f}%")
    
else:
    st.warning("No students found. Try another search!")
