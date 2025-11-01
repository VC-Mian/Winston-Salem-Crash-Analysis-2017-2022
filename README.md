# Winston-Salem-Crash-Analysis-2016-2023-
An interactive data analysis of traffic crashes in Winston-Salem, NC (2016-2023)  using Python, Pandas, and Streamlit. Identifies high-risk locations, temporal  patterns, and severity trends to support evidence-based traffic safety interventions.

## 🔗 Live Dashboard
[View Dashboard]([https://YOUR-APP-URL-HERE](https://winston-salem-crash-analysis-2016-2023-2ixuwpq3a4l6d3gh3xgppq.streamlit.app/))

## Key Features
- Interactive crash location maps
- Temporal pattern analysis (hourly, daily, monthly, yearly)
- Highway vs. surface street comparison
- Severity-weighted risk assessment
- Data-driven safety recommendations

## Technologies
- **Python**: Pandas, Plotly
- **Dashboard**: Streamlit
- **Data Source**: [US Accidents Dataset (Kaggle)]([https://www.kaggle.com/sobhanmoosavi/us-accidents](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents))

## Run Locally
```bash
pip install -r requirements.txt
streamlit run crash_dashboard.py or python -m streamlit run crash_dashboard.py
```

## 📈 Key Findings
- 58.6% of crashes occur on highways despite representing <5% of road infrastructure
- I-40 corridor accounts for 250+ severe crashes (highest risk area)
- Morning rush hour (8 AM) shows peak crash frequency
- 25% of all crashes are classified as severe (Level 3+)
```
