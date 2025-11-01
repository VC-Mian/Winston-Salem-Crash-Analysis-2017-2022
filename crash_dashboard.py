import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page settings
st.set_page_config(
    page_title="Winston-Salem Crash Analysis",
    page_icon="🚗",
    layout="wide"
)

# Title
st.title("Winston-Salem Traffic Crash Analysis (2017-2022)")
st.markdown("An interactive analysis of traffic crashes in Winston-Salem, NC over 6 complete years")

# Load data
@st.cache_data
# Highway classification function
def is_highway(street):
    if pd.isna(street):
        return False
    street_str = str(street).upper()
    
    # Specific highway patterns
    highway_patterns = [
        'I-40', 'I-74',
        'JOHN GOLD', 'JOHN M GOLD',
        'EXPY', 'FWY',
        'US-421', 'US-52', 'US-158', 'US-311',
        'SALEM PKWY', 'PETERS CREEK PKWY', 
        'SILAS CREEK PKWY', 'UNIVERSITY PKWY'
    ]
    
    return any(pattern in street_str for pattern in highway_patterns)

# Load the data
st.info("Loading data... This may take a moment.")
ws_df = pd.read_csv('data/WS_Crashes_2017_2022.csv')

# Add highway classification to main dataframe
ws_df['Is_Highway'] = ws_df['Street'].apply(is_highway)

# Sidebar filters
st.sidebar.header("Filters")

# Year filter
years = sorted(ws_df['Year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Years",
    options=years,
    default=years
)

# Severity filter
severity_options = sorted(ws_df['Severity'].unique())
selected_severity = st.sidebar.multiselect(
    "Select Severity Levels",
    options=severity_options,
    default=severity_options
)

# Apply filters
filtered_df = ws_df[
    (ws_df['Year'].isin(selected_years)) & 
    (ws_df['Severity'].isin(selected_severity))
]

st.sidebar.markdown(f"**Filtered Results:** {len(filtered_df):,} crashes")

# Main content
st.success(f"Loaded {len(ws_df):,} crashes from Winston-Salem")

# Data quality note
with st.expander("📋 Data Quality & Methodology"):
    st.markdown("""
    **Date Range Selection:**
    
    This analysis covers **2017-2022 (6 complete years)**. The original dataset includes 
    2016 and 2023, but these years contain incomplete data:
    - **2016**: Only June-December (7 months)
    - **2023**: Only January-March (3 months)
    
    To ensure accurate year-over-year comparisons and avoid seasonal bias, only complete 
    calendar years are included in this analysis.
    
    **Geographic Filtering:**
    
    Focuses on crashes within **Forsyth County**. When filtering by city name alone, 
    we identified 98 additional crashes labeled "Winston-Salem" but located outside 
    Forsyth County boundaries. County-level filtering provides more reliable geographic 
    boundaries than city name text fields.
    
    **Data Integrity Note:**
    
    This dataset includes all reported traffic incidents. During analysis, certain dates 
    showed unusual clustering patterns that, upon investigation, corresponded to emergency 
    or community events. These outliers are retained as they reflect actual traffic 
    conditions, but demonstrate the importance of contextual analysis when interpreting data.
    """)

# Separate data note about analysis period
st.info("Analysis period: 2017-2022 (6 complete calendar years)")

st.markdown("---")

# Key Metrics Row
st.header("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Crashes", f"{len(filtered_df):,}")
    
with col2:
    severe_count = len(filtered_df[filtered_df['Severity'] >= 3])
    severe_pct = (severe_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    st.metric("Severe Crashes", f"{severe_count:,}", f"{severe_pct:.1f}%")
    
with col3:
    if len(filtered_df) > 0:
        peak_hour = filtered_df['Hour'].mode()[0]
        st.metric("Peak Crash Hour", f"{peak_hour}:00", "Morning Rush")
    else:
        st.metric("Peak Crash Hour", "N/A")
    
with col4:
    avg_severity = filtered_df['Severity'].mean() if len(filtered_df) > 0 else 0
    st.metric("Avg Severity", f"{avg_severity:.2f}")

st.markdown("---")

# Interactive Map Section
st.header("Crash Location Map")

# Map type selector
map_type = st.radio(
    "Select map view:",
    options=["Scatter Plot", "Density Heatmap"],
    horizontal=True
)

if len(filtered_df) > 0:
    if map_type == "Scatter Plot":
        # Scatter plot with color by severity
        fig = px.scatter_map(
            filtered_df,
            lat="Start_Lat",
            lon="Start_Lng",
            color="Severity",
            size_max=8,
            zoom=11,
            height=600,
            hover_data={
                "Start_Lat": False,
                "Start_Lng": False,
                "Street": True,
                "Severity": True,
                "Start_Time": True
            },
            color_continuous_scale="Reds",
            title="Crash Locations by Severity"
        )
    else:
        # Density heatmap
        fig = px.density_map(
            filtered_df,
            lat="Start_Lat",
            lon="Start_Lng",
            radius=10,
            zoom=11,
            height=600,
            title="Crash Density Heatmap"
        )
    
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True, key="map_chart")
else:
    st.warning("No data to display with current filters")

st.markdown("---")

# Time Analysis Section
st.header("Temporal Patterns")

col1, col2 = st.columns(2)

with col1:
    # Crashes by hour
    if len(filtered_df) > 0:
        hourly = filtered_df['Hour'].value_counts().sort_index()
        fig_hour = px.bar(
            x=hourly.index,
            y=hourly.values,
            labels={'x': 'Hour of Day', 'y': 'Number of Crashes'},
            title='Crashes by Hour of Day',
            color=hourly.values,
            color_continuous_scale='Reds'
        )
        fig_hour.add_vrect(x0=7, x1=9, fillcolor="orange", opacity=0.2, line_width=0)
        fig_hour.add_vrect(x0=16, x1=18, fillcolor="orange", opacity=0.2, line_width=0)
        st.plotly_chart(fig_hour, use_container_width=True, key="hour_chart")

with col2:
    # Crashes by day of week
    if len(filtered_df) > 0:
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily = filtered_df['DayOfWeek'].value_counts().sort_index()
        fig_day = px.bar(
            x=[day_names[i] for i in daily.index],
            y=daily.values,
            labels={'x': 'Day of Week', 'y': 'Number of Crashes'},
            title='Crashes by Day of Week',
            color=daily.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_day, use_container_width=True, key="day_chart")

# Crashes by year
if len(filtered_df) > 0:
    yearly = filtered_df['Year'].value_counts().sort_index()
    fig_year = px.line(
        x=yearly.index,
        y=yearly.values,
        labels={'x': 'Year', 'y': 'Number of Crashes'},
        title='Crashes by Year (2017-2022)',
        markers=True
    )
    fig_year.update_traces(line_color='steelblue', line_width=3, marker=dict(size=10))
    st.plotly_chart(fig_year, use_container_width=True, key="year_chart")

st.markdown("---")

# Monthly/Seasonal Analysis
st.subheader("Seasonal Patterns")

col1, col2 = st.columns(2)

with col1:
    # Crashes by month
    if len(filtered_df) > 0:
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly = filtered_df['Month'].value_counts().sort_index()
        
        fig_month = px.bar(
            x=[month_names[i-1] for i in monthly.index],
            y=monthly.values,
            labels={'x': 'Month', 'y': 'Number of Crashes'},
            title='Crashes by Month (All Years Combined)',
            color=monthly.values,
            color_continuous_scale='Reds'
        )
        # Highlight September
        fig_month.add_annotation(
            x='Nov',
            y=monthly.loc[11] if 11 in monthly.index else 0,
            text="Peak Month",
            showarrow=True,
            arrowhead=2,
            arrowcolor="red",
            ax=20,
            ay=-40
        )
        st.plotly_chart(fig_month, use_container_width=True, key="month_chart")

with col2:
    # Year-over-year comparison by month
    if len(filtered_df) > 0:
        monthly_year = filtered_df.groupby(['Year', 'Month']).size().reset_index(name='Count')
        
        fig_month_year = px.line(
            monthly_year,
            x='Month',
            y='Count',
            color='Year',
            labels={'Month': 'Month', 'Count': 'Number of Crashes'},
            title='Monthly Crash Trends by Year',
            markers=True
        )
        fig_month_year.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=month_names
        )
        st.plotly_chart(fig_month_year, use_container_width=True, key="month_year_chart")

st.markdown("---")

# Severity Analysis Section
st.header("Severity Breakdown")

col1, col2 = st.columns(2)

with col1:
    # Severity distribution pie chart
    if len(filtered_df) > 0:
        severity_counts = filtered_df['Severity'].value_counts().sort_index()
        fig_severity = px.pie(
            values=severity_counts.values,
            names=[f"Level {s}" for s in severity_counts.index],
            title='Crash Severity Distribution',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(fig_severity, use_container_width=True, key="severity_pie")

with col2:
    # Severity by year
    if len(filtered_df) > 0:
        severity_year = filtered_df.groupby(['Year', 'Severity']).size().reset_index(name='Count')
        fig_sev_year = px.bar(
            severity_year,
            x='Year',
            y='Count',
            color='Severity',
            title='Crash Severity Trends by Year',
            barmode='stack',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_sev_year, use_container_width=True, key="severity_year")

st.markdown("---")

# Highway vs Surface Streets Analysis
st.header("Highway vs Surface Street Analysis")

highway_crashes = filtered_df[filtered_df['Is_Highway'] == True]
surface_crashes = filtered_df[filtered_df['Is_Highway'] == False]

col1, col2, col3 = st.columns(3)

with col1:
    # Overall distribution
    if len(filtered_df) > 0:
        road_type_counts = pd.Series({
            'Highways': len(highway_crashes),
            'Surface Streets': len(surface_crashes)
        })
        
        fig_road_type = px.pie(
            values=road_type_counts.values,
            names=road_type_counts.index,
            title='Crash Distribution by Road Type',
            color_discrete_sequence=['#d62728', '#1f77b4']
        )
        st.plotly_chart(fig_road_type, use_container_width=True, key="road_type_pie")

with col2:
    # Severity comparison
    if len(filtered_df) > 0:
        severity_comparison = pd.DataFrame({
            'Road Type': ['Highways', 'Surface Streets'],
            'Average Severity': [
                highway_crashes['Severity'].mean() if len(highway_crashes) > 0 else 0,
                surface_crashes['Severity'].mean() if len(surface_crashes) > 0 else 0
            ]
        })
        
        fig_severity_comp = px.bar(
            severity_comparison,
            x='Road Type',
            y='Average Severity',
            title='Average Crash Severity by Road Type',
            color='Road Type',
            color_discrete_map={'Highways': '#d62728', 'Surface Streets': '#1f77b4'}
        )
        fig_severity_comp.update_layout(showlegend=False)
        st.plotly_chart(fig_severity_comp, use_container_width=True, key="severity_comparison")

with col3:
    # Severe crash distribution
    if len(filtered_df) > 0:
        severe_filtered = filtered_df[filtered_df['Severity'] >= 3]
        severe_highway = severe_filtered[severe_filtered['Is_Highway'] == True]
        severe_surface = severe_filtered[severe_filtered['Is_Highway'] == False]
        
        severe_road_type = pd.Series({
            'Highways': len(severe_highway),
            'Surface Streets': len(severe_surface)
        })
        
        fig_severe_road = px.pie(
            values=severe_road_type.values,
            names=severe_road_type.index,
            title='Severe Crashes (Level 3+) by Road Type',
            color_discrete_sequence=['#ff6b6b', '#4ecdc4']
        )
        st.plotly_chart(fig_severe_road, use_container_width=True, key="severe_road_type")

# Add insight callout
if len(filtered_df) > 0:
    highway_pct = (len(highway_crashes) / len(filtered_df)) * 100
    severe_highway_pct = (len(severe_highway) / len(severe_filtered)) * 100 if len(severe_filtered) > 0 else 0
    
    st.info(f"""
     **Key Insight**: While highways account for {highway_pct:.1f}% of all crashes, 
    they represent {severe_highway_pct:.1f}% of severe crashes (Level 3+) - indicating 
    highways have a disproportionately higher rate of serious injuries.
    """)

st.markdown("---")

# Top Dangerous Streets Section
st.header(" Most Dangerous Locations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Streets by Total Crashes")
    if len(filtered_df) > 0:
        top_streets = filtered_df['Street'].value_counts().head(10)
        fig_streets = px.bar(
            x=top_streets.values,
            y=top_streets.index,
            orientation='h',
            labels={'x': 'Number of Crashes', 'y': 'Street'},
            color=top_streets.values,
            color_continuous_scale='Reds'
        )
        fig_streets.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_streets, use_container_width=True, key="top_streets")

with col2:
    st.subheader("Top 10 Streets by Severe Crashes")
    if len(filtered_df) > 0:
        severe_df = filtered_df[filtered_df['Severity'] >= 3]
        if len(severe_df) > 0:
            top_severe_streets = severe_df['Street'].value_counts().head(10)
            fig_severe_streets = px.bar(
                x=top_severe_streets.values,
                y=top_severe_streets.index,
                orientation='h',
                labels={'x': 'Number of Severe Crashes', 'y': 'Street'},
                color=top_severe_streets.values,
                color_continuous_scale='Oranges'
            )
            fig_severe_streets.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_severe_streets, use_container_width=True, key="top_severe_streets")
        else:
            st.info("No severe crashes in filtered data")

st.markdown("---")

# Key Findings Section
st.header("Key Findings & Recommendations")

# Calculate updated statistics
total_crashes = len(ws_df)
severe_crashes_all = ws_df[ws_df['Severity'] >= 3]
highway_crashes_all = ws_df[ws_df['Is_Highway'] == True]
surface_crashes_all = ws_df[ws_df['Is_Highway'] == False]
severe_highway_all = severe_crashes_all[severe_crashes_all['Is_Highway'] == True]

highway_pct_all = (len(highway_crashes_all) / total_crashes) * 100
severe_pct_all = (len(severe_crashes_all) / total_crashes) * 100
severe_highway_pct_all = (len(severe_highway_all) / len(severe_crashes_all)) * 100 if len(severe_crashes_all) > 0 else 0

peak_hour = ws_df['Hour'].mode()[0]
peak_month_num = ws_df['Month'].mode()[0]
month_names_full = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
peak_month = month_names_full[peak_month_num - 1]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Major Insights")
    st.markdown(f"""
        **Dataset Overview:**
        - **{total_crashes:,} total crashes** analyzed (2017-2022)
        - **{len(severe_crashes_all):,} severe crashes** (Level 3+) = **{severe_pct_all:.1f}%** of total

        ---

        **1. Highway Concentration**

        Despite highways representing a small fraction of total road miles, they account 
        for **{highway_pct_all:.1f}%** of all crashes. More critically, severe crashes are 
        disproportionately concentrated on highways (**{severe_highway_pct_all:.1f}%** of 
        Level 3+ crashes).

        *Key corridors: I-40 and Business 40 (John Gold Memorial Expressway)*

        ---

        **2. Rush Hour Pattern**

        **{peak_hour}:00 AM** (morning rush hour) shows the highest crash frequency, with 
        secondary peaks during evening commute (4-6 PM). Weekday crashes significantly 
        exceed weekend crashes, correlating with commuter traffic patterns.
        """)

with col2:
    st.markdown(f"""
        
        **3. Seasonal Variation**

        **{peak_month}** consistently shows the highest crash rates. This seasonal spike 
        may be linked to holiday travel and weather transitions. 

        ---

        **4. I-40 as Primary Risk Factor**

        The **I-40 corridor (East and West combined) accounts for 250+ severe crashes**, 
        making it the single most dangerous location in Winston-Salem. Business 40 
        (John Gold Memorial Expressway) follows with 110+ severe crashes. Together, 
        these two highway systems represent **over 40% of all severe crashes** in the city.

        While certain surface streets like S Stratford Rd show concerning severe crash 
        rates relative to their volume, the absolute priority must be addressing the 
        I-40 corridor where the highest number of serious injuries occur.

        ---

        **5. Cloverleaf Interchanges**

        Highway interchanges, particularly cloverleaf-style designs, emerge as critical 
        crash hotspots due to merging traffic, speed differentials, and limited visibility.
                
        
        """)
st.markdown("--------------------------------")
# Recommendations
col3, col4 = st.columns(2)

with col3:
    st.subheader("Recommendations")
    st.markdown(f"""
        **High-Priority Interventions:**

        **I-40 Corridor (Critical Priority)**
        - **I-40 East and West** account for 250+ severe crashes combined - the single 
            highest-risk area in Winston-Salem
        - Immediate focus areas:
            - Enhanced median barriers to prevent crossover collisions
            - Improved merge zone signage and lighting at interchanges
            - Variable speed limits during peak traffic or adverse weather
            - Increased enforcement of distracted driving and speeding
        - Consider comprehensive safety audit of entire I-40 corridor through Winston-Salem

        ---

        **Business 40 (John Gold Memorial Expressway)**
        - **Second-highest crash concentration** with 110+ severe crashes on north and 
            south sections combined
        - Recommended interventions:
            - Cloverleaf interchange redesigns (known high-risk design)
            - Enhanced exit warning systems
            - Improved lighting at merge zones
            - Clear zone improvements to reduce severity of run-off-road crashes

        ---

          **High-Risk Surface Streets**
        - **S Stratford Rd** shows disproportionately high severe crash rate despite lower volume
            - Railroad crossing safety improvements
            - Commercial vehicle route assessment
            - Enhanced crosswalk/pedestrian safety measures
        - Other surface streets require individual site assessments based on local conditions

        """)

with col4:
    st.markdown(f"""
        ---     

        **Resource Allocation Priority**

        Based on crash data, safety investments should prioritize:
        1. **I-40 corridor** (250+ severe crashes) - Highest impact potential
        2. **Business 40 interchanges** (110+ severe crashes) - Major risk areas  
        3. **US-421 intersections** (50+ severe crashes) - Significant risk
        4. **High-rate surface streets** (S Stratford Rd and similar) - Targeted interventions

        Given that **{severe_highway_pct_all:.1f}%** of severe crashes occur on highways 
        representing <5% of road infrastructure, highway safety investments offer the 
        highest return in lives saved and injuries prevented.
                      
        ---
                    
        **Time-Based Strategies**
        - Deploy additional enforcement during morning rush hour (7-9 AM) when crash risk peaks
        - Consider dynamic messaging boards on I-40 and Business 40 warning of high-risk periods
        - Coordinate with employers for flexible work hours to reduce peak congestion

        ---

        **Seasonal Awareness**
        - Increase enforcement and safety campaigns during {peak_month}
        - Back-to-school traffic management (late August/September)
        - Enhanced winter weather response on highway corridors

        ---

        **US-421 North**
            - **50+ severe crashes** indicate significant risk
            - Target areas: Intersections and merge points
            - Consider: Signal timing optimization, turn lane improvements, sight distance analysis

        """)

st.markdown(f"*Analysis based on {total_crashes:,} traffic crashes in Winston-Salem, Forsyth County, NC (2017-2022)*")

# Display first few rows
if st.checkbox("Show raw data"):
    st.dataframe(ws_df.head())