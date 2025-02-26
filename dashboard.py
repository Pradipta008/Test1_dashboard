import pandas as pd
import streamlit as st

# Load sample data
data = pd.read_csv("student_data.csv")

# Title of the dashboard
st.title("Student Performance Dashboard")

# Display the data
st.write("### Student Data")
st.write(data)

# Visualization: Average Scores
st.write("### Average Scores by Subject")
avg_scores = data[["Math", "Science", "English"]].mean()
st.bar_chart(avg_scores)

# Identify At-Risk Students
st.write("### At-Risk Students")
data["Average Score"] = data[["Math", "Science", "English"]].mean(axis=1)
at_risk = data[data["Average Score"] < 75]
st.write(at_risk[["Name", "Average Score", "Attendance"]])

# Attendance Analysis
st.write("### Attendance Analysis")
st.write(f"Average Attendance: {data['Attendance'].mean():.2f}%")
