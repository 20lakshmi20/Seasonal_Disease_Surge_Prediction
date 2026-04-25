import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ------------------------------------
# PAGE CONFIG
# ------------------------------------

st.set_page_config(
page_title="Disease Early Warning System",
layout="wide"
)

# ------------------------------------
# STYLE
# ------------------------------------

st.markdown("""
<style>
.big-title{
font-size:40px;
font-weight:bold;
color:#1f77b4;
}

.sub{
font-size:18px;
color:gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
'<h3 class="big-title">AI-Based Seasonal Disease Early Warning System</h3>',
unsafe_allow_html=True
)

st.markdown(
'<p class="sub">Predicting disease outbreaks 7 days in advance using weather and healthcare indicators</p>',
unsafe_allow_html=True
)

# ------------------------------------
# LOAD DATA
# ------------------------------------

df = pd.read_csv(
"cleaned_disease_dataset_v2.csv"
)

# ------------------------------------
# DISTRICT LOCATIONS
# ------------------------------------

district_map = {
"Chennai":(13.0827,80.2707),
"Coimbatore":(11.0168,76.9558),
"Madurai":(9.9252,78.1198),
"Salem":(11.6643,78.1460),
"Trichy":(10.7905,78.7047),
"Tirunelveli":(8.7139,77.7567),
"Erode":(11.3410,77.7172),
"Vellore":(12.9165,79.1325)
}

# ------------------------------------
# ENCODE DISTRICT
# ------------------------------------

df = pd.get_dummies(
df,
columns=["District"]
)

# ------------------------------------
# FEATURES
# ------------------------------------

feature_cols = [
"Rainfall_mm",
"Temperature_C",
"Humidity",
"OPD_Visits",
"Month",
"Outbreak_Index",
"Rain_7DayAvg",
"OPD_7DayAvg"
]

for col in df.columns:
    if col.startswith("District_"):
        feature_cols.append(col)

X=df[feature_cols]

# ------------------------------------
# TARGETS
# ------------------------------------

y_risk=df["Future_Risk"]

df["Predicted_Disease"]="Influenza"

df.loc[
df["Future_Risk"]=="High",
"Predicted_Disease"
]="Dengue"

df.loc[
(df["Humidity"]>75) &
(df["Future_Risk"]=="High"),
"Predicted_Disease"
]="Malaria"

df.loc[
(df["Rainfall_mm"]>100) &
(df["OPD_Visits"]>150) &
(df["Future_Risk"]=="Medium"),
"Predicted_Disease"
]="Leptospirosis"

y_disease=df["Predicted_Disease"]

# ------------------------------------
# TRAIN MODELS
# ------------------------------------

risk_model=RandomForestClassifier(
n_estimators=300,
max_depth=10,
random_state=42
)

risk_model.fit(X,y_risk)

disease_model=RandomForestClassifier(
n_estimators=300,
max_depth=10,
random_state=42
)

disease_model.fit(X,y_disease)

# ------------------------------------
# INPUTS
# ------------------------------------

col1,col2=st.columns(2)

with col1:

    district=st.selectbox(
    "District",
    list(district_map.keys())
    )

    rainfall=st.slider(
    "Rainfall (mm)",
    0,200,120
    )

    temperature=st.slider(
    "Temperature (°C)",
    20,45,32
    )

with col2:

    humidity=st.slider(
    "Humidity",
    30,100,75
    )

    opd=st.slider(
    "OPD Visits",
    0,300,150
    )

    month=st.slider(
    "Month",
    1,12,10
    )

# default values before prediction
risk="Low"
disease="Influenza"

# ------------------------------------
# PREDICT BUTTON
# ------------------------------------

if st.button("Predict Outbreak Risk"):

    outbreak_index=(
    0.3*rainfall+
    0.2*humidity+
    0.5*opd
    )

    sample=pd.DataFrame([{
    "Rainfall_mm":rainfall,
    "Temperature_C":temperature,
    "Humidity":humidity,
    "OPD_Visits":opd,
    "Month":month,
    "Outbreak_Index":outbreak_index,
    "Rain_7DayAvg":rainfall,
    "OPD_7DayAvg":opd
    }])

    for col in X.columns:
        if col not in sample.columns:
            sample[col]=0

    district_col="District_"+district

    if district_col in sample.columns:
        sample[district_col]=1

    sample=sample[X.columns]

    # predictions
    risk=risk_model.predict(sample)[0]

    disease=disease_model.predict(sample)[0]

    # --------------------------
    # RULE OVERRIDE
    # --------------------------

    if (
    rainfall>=140 and
    humidity>=80 and
    opd>=180
    ):
        risk="High"

    elif (
    temperature>=35 and
    opd>=80 and
    risk!="High"
    ):
        risk="Medium"

    # disease alignment
    if risk=="High" and humidity>=80:
        disease="Malaria"

    elif risk=="High":
        disease="Dengue"

    elif risk=="Medium" and rainfall>100:
        disease="Leptospirosis"

    elif risk=="Medium":
        disease="Influenza"

    # results
    st.subheader(
    f"Predicted Outbreak Risk in 7 Days: {risk}"
    )

    st.subheader(
    f"Predicted Disease: {disease}"
    )

    if risk=="High":

        st.error(
        f"⚠ High {disease} Outbreak Risk"
        )

    elif risk=="Medium":

        st.warning(
        f"Moderate {disease} Risk"
        )

    else:

        st.success(
        "Low Outbreak Risk"
        )


# ------------------------------------
# BETTER DISTRICT RISK BAR CHART
# ------------------------------------

st.markdown("---")

st.subheader(
"District Risk Levels"
)

risk_summary=pd.DataFrame({
"District":[
"Chennai",
"Coimbatore",
"Madurai",
"Salem",
"Trichy",
"Tirunelveli",
"Erode",
"Vellore"
],

"Risk Score":[
82,65,75,40,60,55,35,30
]
})

# Highlight selected district based on prediction

if risk=="High":
    risk_summary.loc[
risk_summary["District"]==district,
"Risk Score"
]=95

elif risk=="Medium":
    risk_summary.loc[
risk_summary["District"]==district,
"Risk Score"
]=70

elif risk=="Low":
    risk_summary.loc[
risk_summary["District"]==district,
"Risk Score"
]=30


st.bar_chart(
risk_summary.set_index("District")
)

# ------------------------------------
# COLOR-CODED DISTRICT RISK MAP
# ------------------------------------

st.subheader(
"District Risk Map"
)

map_data=[]

for i,row in risk_summary.iterrows():

    d=row["District"]

    lat,lon=district_map[d]

    score=row["Risk Score"]

    map_data.append({
    "District":d,
    "lat":lat,
    "lon":lon,
    "Risk_Score":score
    })

map_df=pd.DataFrame(map_data)

st.write(
"Higher risk districts appear as larger map points."
)

st.dataframe(
map_df[
["District","Risk_Score"]
]
)

# point size reflects risk
st.map(
map_df,
size="Risk_Score"
)