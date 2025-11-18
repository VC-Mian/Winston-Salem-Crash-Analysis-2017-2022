# Winston-Salem-Crash-Analysis-2017-2022
An interactive data analysis of traffic crashes in Winston-Salem, NC (2016-2023)  using Python, Pandas, and Streamlit. Identifies high-risk locations, temporal  patterns, and severity trends to support evidence-based traffic safety interventions.

**Workflow:**
1. **Explore** data in `DataAnalysis.ipynb` (research questions, cleaning, patterns)
2. **Build** dashboard in `crash_dashboard.py` (implement insights, add interactivity)
3. **Deploy** to Streamlit Cloud
   
## Research Questions
1. **Where** are the most dangerous locations for crashes in Winston-Salem?
2. **When** do crashes occur most frequently (hour, day, month, year)?
3. **What types of roads** (highways vs. surface streets) experience the highest crash severity?
4. **Which locations** should be prioritized for safety interventions?

## 🔗 Live Dashboard
[View Dashboard](https://winston-salem-crash-analysis-2017-2022.streamlit.app/)

## Key Features
- Interactive crash location maps
- Temporal pattern analysis (hourly, daily, monthly, yearly)
- Highway vs. surface street comparison
- Severity-weighted risk assessment
- Data-driven safety recommendations

## Technologies
- **Python**: Pandas, Plotly, matplotlib
- **Dashboard**: Streamlit
- **Data Source**: [US Accidents Dataset (Kaggle)]([https://www.kaggle.com/sobhanmoosavi/us-accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents))

## Run Locally
```bash
pip install -r requirements.txt
streamlit run crash_dashboard.py or python -m streamlit run crash_dashboard.py
```

## Key Findings
- 58.6% of crashes occur on highways despite representing <5% of road infrastructure
- I-40 corridor accounts for 250+ severe crashes (highest risk area)
- Morning rush hour (8 AM) shows peak crash frequency
- 25% of all crashes are classified as severe (Level 3+)

## Data Analysis Skills I Developed

- Standardized inconsistent text fields (Winston-Salem was entered two different ways)
- Filtered incomplete years to avoid seasonal bias (2016 & 2023 were incomplete years)
- Validated anomalies through external research instead of blindly removing them (some outliers were due to emergency events)
- Built reusable filtering functions for highway classification (separating highways from surface streets for accurate results)


