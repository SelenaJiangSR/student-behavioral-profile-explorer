import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Behavioral Profile Analyzer",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F4F1EC 0%, #E8ECE7 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1050px;
}

h1, h2, h3 {
    color: #3F4A47;
}

p, li {
    color: #5F6B66;
    font-size: 16px;
    line-height: 1.6;
}

.hero-card, .result-card, .support-card {
    background: rgba(255, 255, 255, 0.88);
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0px 14px 35px rgba(84, 91, 86, 0.12);
    border: 1px solid rgba(255,255,255,0.7);
    margin-bottom: 22px;
}

.result-card {
    border-left: 8px solid #8A9A8B;
}

.highlight {
    color: #8A7E72;
    font-weight: 700;
}

.stButton > button {
    background-color: #7D8F86;
    color: white;
    border-radius: 14px;
    border: none;
    padding: 0.75rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #667A71;
    color: white;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    mat = pd.read_csv("student-mat.csv", sep=";")
    por = pd.read_csv("student-por.csv", sep=";")
    return mat, por


def get_profile(studytime, goout, freetime, dalc, walc, absences, failures):
    if failures >= 2 or absences >= 18:
        return {
            "name": "Academically At-Risk Profile",
            "summary": "Your input is closest to a profile with weaker academic stability.",
            "description": (
                "This profile is characterized by higher academic risk indicators, "
                "such as previous failures or higher absences."
            ),
            "strengths": [
                "This pattern can be identified early.",
                "With structured support, academic recovery is still possible."
            ],
            "risks": [
                "Higher absences",
                "Previous academic difficulties",
                "Less stable academic performance"
            ],
            "evidence": (
                "In the clustering analysis, at-risk groups were connected with higher previous "
                "failures, weaker academic stability, and lower final performance."
            )
        }

    if goout >= 4 and walc >= 3:
        return {
            "name": "Social / Lifestyle-Oriented Profile",
            "summary": "Your input is closest to a socially active lifestyle profile.",
            "description": (
                "This profile is associated with higher social activity, more frequent going out, "
                "and higher weekend alcohol consumption."
            ),
            "strengths": [
                "Strong social engagement",
                "Active lifestyle",
                "Potentially strong peer connection"
            ],
            "risks": [
                "Higher social activity may connect with higher absences",
                "Alcohol-related variables may increase behavioral risk"
            ],
            "evidence": (
                "In both datasets, socially active clusters showed higher goout and higher "
                "alcohol-related variables. These groups were not always the lowest-performing, "
                "but they showed less stable academic patterns than academically stable groups."
            )
        }

    if studytime >= 3 and failures == 0 and walc <= 2 and goout <= 3:
        return {
            "name": "Academically Stable Profile",
            "summary": "Your input is closest to an academically stable behavioral profile.",
            "description": (
                "This profile is associated with stronger study habits, lower alcohol consumption, "
                "fewer previous failures, and more stable academic behavior."
            ),
            "strengths": [
                "Consistent study behavior",
                "Lower behavioral risk",
                "Stronger academic stability"
            ],
            "risks": [
                "May need to maintain balance between academic work and social life"
            ],
            "evidence": (
                "In the clustering results, academically stable groups generally showed higher "
                "academic performance, lower alcohol consumption, fewer failures, and fewer absences."
            )
        }

    return {
        "name": "Balanced / Moderate Profile",
        "summary": "Your input is closest to a balanced or moderate behavioral profile.",
        "description": (
            "This profile does not show extreme values in most behavioral variables. "
            "It represents a middle-range behavioral pattern."
        ),
        "strengths": [
            "Moderate lifestyle balance",
            "No extreme risk indicators",
            "Flexible behavioral pattern"
        ],
        "risks": [
            "Academic performance may depend on consistency over time"
        ],
        "evidence": (
            "Balanced clusters appeared as middle-range behavioral groups across the datasets, "
            "suggesting that many students do not belong to extreme high-risk or high-performance profiles."
        )
    }


df_mat, df_por = load_data()

st.markdown("""
<div class="hero-card">
<h1>Student Behavioral Profile Analyzer</h1>
<p>
An interactive educational behavioral analytics tool that explores student lifestyle,
study behavior, social activity, and academic stability through data-driven behavioral profiles.
</p>
<p>
This app is based on the UCI Student Performance Dataset and a K-Means clustering research project.
</p>
</div>
""", unsafe_allow_html=True)

st.header("1. Enter Your Behavioral Profile")

st.write(
    "Adjust the sliders below based on your own behavior pattern. "
    "Then click the button to analyze which student behavioral profile your input is closest to."
)

left, right = st.columns(2)

with left:
    studytime = st.slider("Weekly Study Time", 1, 4, 2)
    goout = st.slider("Going Out with Friends", 1, 5, 3)
    freetime = st.slider("Free Time After School", 1, 5, 3)

with right:
    dalc = st.slider("Workday Alcohol Consumption", 1, 5, 1)
    walc = st.slider("Weekend Alcohol Consumption", 1, 5, 2)
    absences = st.slider("Number of Absences", 0, 30, 5)
    failures = st.slider("Past Class Failures", 0, 4, 0)

submit = st.button("Analyze My Behavioral Profile", use_container_width=True)

if submit:
    profile = get_profile(studytime, goout, freetime, dalc, walc, absences, failures)

    st.divider()
    st.header("2. Your Estimated Behavioral Profile")

    st.markdown(f"""
    <div class="result-card">
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
    st.header("3. Dataset Support")

    st.markdown(f"""
    <div class="support-card">
    <h3>Evidence from the Research Dataset</h3>
    <p>{profile["evidence"]}</p>
    <p>
    This result is not a personal diagnosis or grade prediction. It is an estimated
    profile based on patterns observed in the UCI Student Performance Dataset.
    </p>
    </div>
    """, unsafe_allow_html=True)

    summary_data = pd.DataFrame({
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
    })

    st.dataframe(summary_data, use_container_width=True)

    st.divider()
    st.header("4. Research Note")

    st.info(
        "This app does not diagnose students or predict exact grades. "
        "It estimates which behavioral profile your input is closest to based on patterns "
        "found in the UCI Student Performance Dataset."
    )

else:
    st.info("Adjust the sliders above, then click **Analyze My Behavioral Profile** to see your result.")
