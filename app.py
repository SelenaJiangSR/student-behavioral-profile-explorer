import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Student Behavioral Profile Explorer",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🎓 Student Behavioral Profile Explorer")

st.markdown("""
This interactive dashboard explores student behavioral patterns
using the UCI Student Performance Dataset and K-Means clustering.
""")

# =====================================================
# LOAD DATA
# =====================================================

df_mat = pd.read_csv("student-mat.csv", sep=";")
df_por = pd.read_csv("student-por.csv", sep=";")

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.header("📊 Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Math Dataset")
    st.write(df_mat.head())

with col2:
    st.subheader("Portuguese Dataset")
    st.write(df_por.head())

# =====================================================
# USER INPUT SECTION
# =====================================================

st.header("🧠 Behavioral Profile Input")

studytime = st.slider(
    "Weekly Study Time",
    1, 4, 2
)

goout = st.slider(
    "Going Out with Friends",
    1, 5, 3
)

dalc = st.slider(
    "Workday Alcohol Consumption",
    1, 5, 1
)

walc = st.slider(
    "Weekend Alcohol Consumption",
    1, 5, 2
)

absences = st.slider(
    "Number of Absences",
    0, 30, 5
)

failures = st.slider(
    "Past Class Failures",
    0, 4, 0
)

# =====================================================
# SIMPLE PROFILE LOGIC
# =====================================================

st.header("📌 Estimated Behavioral Profile")

if (
    studytime >= 3
    and goout <= 2
    and walc <= 2
    and failures == 0
):
    profile = "📚 Academically Focused"

elif (
    goout >= 4
    and walc >= 3
):
    profile = "🎉 Social / Lifestyle-Oriented"

elif (
    failures >= 2
    or absences >= 15
):
    profile = "⚠️ Academically At-Risk"

else:
    profile = "⚖️ Balanced / Moderate"

st.success(f"Predicted Profile: {profile}")

# =====================================================
# RESEARCH FINDINGS
# =====================================================

st.header("🔍 Key Research Findings")

st.markdown("""
- Students with higher study time generally showed stronger academic performance.
- Higher alcohol consumption and social activity were associated with increased absences.
- Some clusters demonstrated balanced behavioral patterns with moderate academic outcomes.
- Cross-dataset analysis showed similar behavioral archetypes in both subjects.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.markdown("Built using Streamlit + Python + UCI Student Dataset")
