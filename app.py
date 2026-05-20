import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Behavioral Profile Analyzer",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #F4F1EC 0%, #E8ECE7 100%);
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

h1 {
    color: #3F4A47;
    font-weight: 700;
    letter-spacing: -0.03em;
}

h2, h3 {
    color: #4F5D58;
    font-weight: 600;
}

p, li {
    color: #5F6B66;
    font-size: 16px;
    line-height: 1.65;
}

.profile-card {
    background: rgba(255, 255, 255, 0.82);
    padding: 30px;
    border-radius: 24px;
    box-shadow: 0px 18px 45px rgba(84, 91, 86, 0.12);
    border: 1px solid rgba(255,255,255,0.65);
    margin-top: 18px;
}

.profile-card h2 {
    color: #3E514A;
    font-size: 30px;
    margin-bottom: 12px;
}

.highlight {
    color: #8A7E72;
    font-weight: 700;
}

[data-testid="stSlider"] {
    background: rgba(255,255,255,0.68);
    padding: 18px 20px;
    border-radius: 18px;
    box-shadow: 0px 8px 24px rgba(90, 96, 92, 0.08);
    margin-bottom: 16px;
}

.stSuccess {
    background-color: #DDE7DF !important;
    color: #3F5B4A !important;
    border-radius: 16px;
}

.stInfo {
    background-color: #E7E1D8 !important;
    color: #5C524A !important;
    border-radius: 16px;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0px 10px 30px rgba(90, 96, 92, 0.1);
}

hr {
    border: none;
    height: 1px;
    background: rgba(95, 107, 102, 0.2);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    mat = pd.read_csv("student-mat.csv", sep=";")
    por = pd.read_csv("student-por.csv", sep=";")
    return mat, por

df_mat, df_por = load_data()

# -----------------------------
# Header
# -----------------------------
st.title("Student Behavioral Profile Analyzer")

st.markdown("""
This interactive tool is based on an educational behavioral analytics project using the UCI Student Performance Dataset.

Instead of predicting your grade, this app compares your behavior inputs with patterns found in the dataset and estimates which behavioral profile you are closest to.
""")

st.divider()

# -----------------------------
# Inputs
# -----------------------------
st.header("1. Enter Your Behavioral Profile")

left, right = st.columns(2)

with left:
    studytime = st.slider("Weekly Study Time", 1, 4, 2,
                          help="1 = <2 hours, 4 = >10 hours")
    goout = st.slider("Going Out with Friends", 1, 5, 3,
                      help="1 = very low, 5 = very high")
    freetime = st.slider("Free Time After School", 1, 5, 3)

with right:
    dalc = st.slider("Workday Alcohol Consumption", 1, 5, 1)
    walc = st.slider("Weekend Alcohol Consumption", 1, 5, 2)
    absences = st.slider("Number of Absences", 0, 30, 5)
    failures = st.slider("Past Class Failures", 0, 4, 0)

# -----------------------------
# Profile logic
# -----------------------------
def get_profile(studytime, goout, freetime, dalc, walc, absences, failures):
    if failures >= 2 or absences >= 18:
        return {
            "name": "Academically At-Risk Profile",
            "summary": "Your input is closest to a profile with weaker academic stability.",
            "description": """
This profile is characterized by higher academic risk indicators, such as previous failures or higher absences.

In the dataset, students with higher failures and more absences often appeared in clusters with lower academic stability.
""",
            "strengths": ["There may still be room for recovery with structured support.", "Identifying this pattern early can help guide better academic planning."],
            "risks": ["Higher absences", "Previous academic difficulties", "Less stable academic performance"]
        }

    if goout >= 4 and walc >= 3:
        return {
            "name": "Social / Lifestyle-Oriented Profile",
            "summary": "Your input is closest to a socially active lifestyle profile.",
            "description": """
This profile is associated with higher social activity, more frequent going out, and higher weekend alcohol consumption.

In the clustering analysis, similar groups often showed higher goout, higher Dalc/Walc, and sometimes higher absences.
""",
            "strengths": ["Strong social engagement", "Active lifestyle", "Potentially balanced social confidence"],
            "risks": ["Higher social activity may connect with higher absences", "Alcohol-related variables may increase behavioral risk"]
        }

    if studytime >= 3 and failures == 0 and walc <= 2 and goout <= 3:
        return {
            "name": "Academically Stable Profile",
            "summary": "Your input is closest to an academically stable behavioral profile.",
            "description": """
This profile is associated with higher study time, lower alcohol consumption, fewer failures, and relatively stable academic behavior.

In both Math and Portuguese datasets, academically stable clusters tended to show lower-risk behavioral patterns.
""",
            "strengths": ["Consistent academic habits", "Lower behavioral risk", "Stronger academic stability"],
            "risks": ["May need to maintain balance between academic work and social life"]
        }

    return {
        "name": "Balanced / Moderate Profile",
        "summary": "Your input is closest to a balanced or moderate behavioral profile.",
        "description": """
This profile does not show extreme values in most behavioral variables.

In the dataset, many students fell into moderate clusters where study behavior, social activity, and academic outcomes were relatively balanced.
""",
        "strengths": ["Moderate lifestyle balance", "No extreme risk indicators", "Flexible behavioral pattern"],
        "risks": ["Academic performance may depend on consistency over time"]
    }

profile = get_profile(studytime, goout, freetime, dalc, walc, absences, failures)

st.divider()

# -----------------------------
# Output
# -----------------------------
st.header("2. Your Estimated Behavioral Profile")

st.markdown(f"""
<div class="profile-card">
<h2>{profile["name"]}</h2>
<p><span class="highlight">{profile["summary"]}</span></p>
<p>{profile["description"]}</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Potential Strengths")
    for item in profile["strengths"]:
        st.write(f"- {item}")

with col2:
    st.subheader("Possible Risk Factors")
    for item in profile["risks"]:
        st.write(f"- {item}")

st.divider()

# -----------------------------
# Dataset support
# -----------------------------
st.header("3. Dataset Support")

st.markdown("""
The original clustering analysis found several recurring behavioral patterns across the Math and Portuguese datasets:

- Academically stable clusters generally showed higher study time, fewer failures, lower alcohol consumption, and stronger academic outcomes.
- Social / lifestyle-oriented clusters showed higher going-out behavior, higher alcohol consumption, and sometimes higher absences.
- At-risk academic clusters showed lower final grades and higher previous failures.
- Similar profile structures appeared in both datasets, suggesting that these patterns were not limited to one subject.
""")

summary_data = {
    "Profile Type": [
        "Academically Stable",
        "Social / Lifestyle-Oriented",
        "Academically At-Risk",
        "Balanced / Moderate"
    ],
    "Typical Pattern": [
        "Higher studytime, lower alcohol, fewer failures",
        "Higher goout, higher weekend alcohol, more social activity",
        "Higher failures or absences, weaker academic stability",
        "Moderate values across most behavior variables"
    ],
    "Dataset Evidence": [
        "Appeared in both Math and Portuguese clustering results",
        "Appeared as high-social / high-alcohol clusters",
        "Visible especially in clusters with high failures or low G3",
        "Appeared as middle-range behavioral groups"
    ]
}

st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

st.divider()

# -----------------------------
# Research note
# -----------------------------
st.header("4. Important Research Note")

st.info("""
This app does not diagnose students or predict exact grades.

It estimates which behavioral profile your input is closest to based on patterns found in the UCI Student Performance Dataset.

The result should be interpreted as an educational data exploration, not as a personal judgment.
""")
