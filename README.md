# Seasonal_Disease_Surge_Prediction
AI-based early warning system that predicts seasonal disease surges using weather and healthcare indicators, providing outbreak risk prediction, disease alerts, estimated cases, resource planning, and district-level risk visualization.
# AI-Based Seasonal Disease Early Warning System

## Overview
This project predicts seasonal disease surges in advance using weather and healthcare indicators.

The system provides:
- Early outbreak risk prediction (Low / Medium / High)
- Disease prediction (Dengue, Malaria, Influenza, Leptospirosis)
- Estimated case burden
- Resource planning recommendations
- District-level risk visualization
- Interactive Streamlit alert dashboard

Goal:
Support proactive healthcare response before outbreaks overwhelm hospitals.

---

## Problem Statement
Develop an AI-based early warning system that predicts seasonal disease surges in Tamil Nadu government hospitals using leading indicators such as:

- Rainfall
- Temperature
- Humidity
- OPD Visits

The system helps forecast disease surge risk and support preparedness planning.

---

## Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib

---

## Dataset
Dataset contains:
- Date
- District
- Rainfall_mm
- Temperature_C
- Humidity
- OPD_Visits
- Disease_Name
- Risk_Level

Additional engineered features:
- Month
- Outbreak_Index
- Rain_7DayAvg
- OPD_7DayAvg
- Future_Risk

Files:
- seasonal_disease_dataset_500.csv
- cleaned_disease_dataset_v2.csv


## Data Preprocessing
Performed:
- Missing value handling
- Outlier removal
- Feature engineering
- Rolling averages
- Future risk labeling

---

## Machine Learning Model
Model Used:
Random Forest Classifier

Baseline Model Accuracy:
0.47

Improved Model Accuracy:
0.98

Improvement achieved through data enrichment.

---

## Features
### Disease Risk Prediction
Predicts:
- Low Risk
- Medium Risk
- High Risk

### Disease Prediction
Possible diseases:
- Dengue
- Malaria
- Influenza
- Leptospirosis

### Severity Estimation
Example:
- High Risk → Estimated 450 cases
- Medium Risk → Estimated 180 cases
- Low Risk → Estimated 40 cases

### Resource Planning
System recommends:
- Bed preparation
- Medicine stock readiness
- Staff readiness

---

## Streamlit Dashboard
Includes:
- User input interface
- Outbreak prediction
- Disease alerts
- District risk chart
- District risk map

---

## Project Workflow
Raw Data  
↓  
Data Cleaning  
↓  
Feature Engineering  
↓  
Random Forest Model  
↓  
Disease Surge Prediction  
↓  
Alert Generation  
↓  
Resource Planning Dashboard

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run Jupyter notebook
Open:

```bash
Seasonal_Disease_Surge_Prediction.ipynb
```

Run all cells.

### Launch Streamlit app
```bash
streamlit run app.py
```

---

## Repository Structure
text
project/
│
├── seasonal_disease_dataset_500.csv
├── cleaned_disease_dataset_v2.csv
├── Seasonal_Disease_Surge_Prediction.ipynb
├── app.py
├── requirements.txt
├── AI-Based-Seasonal-Disease-Early-Warning-System.pptx
└── README.md


---

## Limitations
- Current prototype demonstrates 7-day forecasting and is designed to scale toward 14–21 days.
- Uses synthetic signals for simulation.
- Requires validation using real hospital surveillance data.

---

## Future Improvements
- 14–21 day forecasting
- Real-time weather API integration
- Live hospital data integration
- Advanced district heatmap
