# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Note: matplotlib and seaborn are optional for this version

# --- Enhanced Configuration ---
st.set_page_config(
    page_title="Global Renewable Energy Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern Styling ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Metric Cards */
    .metric-container {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.2rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
        font-size: 1.3rem;
        box-shadow: 0 4px 10px rgba(116, 185, 255, 0.3);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        border: none;
        border-radius: 8px;
        color: white;
    }
    
    /* Buttons and Interactive Elements */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #74b9ff;
        box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.1);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #2d3436, #636e72);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 3rem;
    }
    
    /* Animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final_renewables_dataset.csv")

        # Data Cleaning and Type Conversion
        if 'Year' in df.columns:
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        else:
            st.error("Column 'Year' not found in the dataset. Please check your CSV.")
            st.stop()

        numeric_cols = [
            'Solar_GW', 'Wind_GW', 'Hydro_GW', 'Total_GW',
            'Population', 'GDP_per_Capita', 'Capacity_per_Capita_kW'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                st.warning(f"Column '{col}' not found in the dataset. Some plots may not work as expected.")

        df = df.drop(columns=['Country Name_x', 'Country Name_y', 'Country'], errors='ignore')
        df.dropna(subset=['Entity', 'Code', 'Year'], inplace=True)

        return df

    except FileNotFoundError:
        st.error("Error: 'final_renewables_dataset.csv' not found. Please ensure it's in the same directory as app.py.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading or processing data: {e}. Please check your CSV file's format and column names.")
        st.stop()

df = load_data()

# --- Enhanced Dashboard Header ---
st.markdown("""
<div class="main-header fade-in">
    <h1 class="main-title">Global Renewable Energy Dashboard</h1>
    <p class="main-subtitle">Exploring the future of sustainable energy across the globe</p>
</div>
""", unsafe_allow_html=True)

# --- Enhanced Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>🎛️ Control Panel</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get unique years and countries for filters
    years = sorted(df["Year"].dropna().unique())
    countries = sorted(df["Entity"].dropna().unique())
    
    # Enhanced year slider
    st.markdown("**📅 Select Year**")
    selected_year = st.slider(
        "",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=2023,
        help="Choose a year to explore renewable energy data"
    )
    
    st.markdown("---")
    
    # Enhanced country selector
    st.markdown("**🌍 Select Country**")
    selected_country = st.selectbox(
        "",
        countries,
        index=countries.index("World") if "World" in countries else 0,
        help="Choose a country for detailed analysis"
    )
    
    # Add some sidebar info
    st.markdown("---")
    st.markdown("""
    **💡 Dashboard Features:**
    - Interactive world map
    - Time series analysis
    - Country comparisons
    - Economic correlations
    - Per-capita insights
    """)

# --- Enhanced Key Metrics Section ---
st.markdown(f"""
<div class="section-header fade-in">
    📊 Key Insights for {selected_country} in {selected_year}
</div>
""", unsafe_allow_html=True)

filtered_country_data = df[(df["Year"] == selected_year) & (df["Entity"] == selected_country)]

if not filtered_country_data.empty:
    country_row = filtered_country_data.iloc[0]
    
    # Create enhanced metric cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("☀️ Solar Capacity", f"{country_row.get('Solar_GW', 0):,.1f} GW", col1),
        ("💨 Wind Capacity", f"{country_row.get('Wind_GW', 0):,.1f} GW", col2),
        ("💧 Hydro Capacity", f"{country_row.get('Hydro_GW', 0):,.1f} GW", col3),
        ("⚡ Total Renewable", f"{country_row.get('Total_GW', 0):,.1f} GW", col4),
        ("👤 Per Capita", f"{country_row.get('Capacity_per_Capita_kW', 0):,.2f} kW", col5)
    ]
    
    for label, value, col in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{value.split()[0]}</div>
                <div class="metric-label">{label}</div>
                <div style="font-size: 0.8rem; color: #95a5a6;">{' '.join(value.split()[1:])}</div>
            </div>
            """, unsafe_allow_html=True)

    # Enhanced Energy Mix Visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader(f"🔋 Renewable Energy Mix - {selected_country}")
    
    mix_data = {
        'Solar': country_row.get('Solar_GW', 0),
        'Wind': country_row.get('Wind_GW', 0),
        'Hydro': country_row.get('Hydro_GW', 0)
    }
    
    if sum(mix_data.values()) > 0:
        # Create an enhanced donut chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(mix_data.keys()),
            values=list(mix_data.values()),
            hole=0.4,
            hovertemplate="<b>%{label}</b><br>" +
                         "Capacity: %{value:.1f} GW<br>" +
                         "Percentage: %{percent}<br>" +
                         "<extra></extra>",
            textinfo="label+percent",
            textposition="outside",
            marker=dict(
                colors=['#ff7675', '#74b9ff', '#00b894'],
                line=dict(color='#FFFFFF', width=3)
            )
        )])
        
        fig_pie.update_layout(
            title=dict(
                text=f"Energy Mix Distribution ({sum(mix_data.values()):.1f} GW Total)",
                x=0.5,
                font=dict(size=16, color='#2d3436')
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=50, b=50, l=50, r=50),
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("🔍 No renewable energy data available for the selected country and year.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced World Map and Global Trends ---
st.markdown("""
<div class="section-header fade-in">
    🗺️ Global Renewable Energy Landscape
</div>
""", unsafe_allow_html=True)

col_map, col_trends = st.columns([1.2, 0.8])

with col_map:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    map_data = df[(df['Year'] == selected_year) & (df['Entity'] != 'World')].dropna(subset=['Total_GW', 'Code'])
    
    if not map_data.empty:
        fig_map = px.choropleth(
            map_data,
            locations="Code",
            color="Total_GW",
            hover_name="Entity",
            hover_data={'Total_GW': ':,.1f', 'Code': False},
            color_continuous_scale="Viridis",
            title=f"🌍 Global Renewable Capacity Distribution ({selected_year})",
            projection="natural earth"
        )
        
        fig_map.update_layout(
            title=dict(x=0.5, font=dict(size=16)),
            geo=dict(
                showframe=False,
                showcoastlines=True,
                bgcolor='rgba(0,0,0,0)'
            ),
            coloraxis_colorbar=dict(
                title="Capacity (GW)"
            ),
            margin=dict(t=50, b=0, l=0, r=0),
            height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_trends:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Global Growth Trends")
    
    # Global renewable trends
    global_trend_data = df[df['Entity'] != 'World'].groupby('Year')[['Solar_GW', 'Wind_GW', 'Hydro_GW']].sum().reset_index()
    
    if not global_trend_data.empty:
        fig_trends = go.Figure()
        
        colors = {'Solar_GW': '#ff7675', 'Wind_GW': '#74b9ff', 'Hydro_GW': '#00b894'}
        names = {'Solar_GW': 'Solar', 'Wind_GW': 'Wind', 'Hydro_GW': 'Hydro'}
        
        for col in ['Solar_GW', 'Wind_GW', 'Hydro_GW']:
            fig_trends.add_trace(go.Scatter(
                x=global_trend_data['Year'],
                y=global_trend_data[col],
                mode='lines+markers',
                name=names[col],
                line=dict(color=colors[col], width=3),
                marker=dict(size=6),
                hovertemplate=f"<b>{names[col]}</b><br>" +
                             "Year: %{x}<br>" +
                             "Capacity: %{y:.1f} GW<br>" +
                             "<extra></extra>"
            ))
        
        fig_trends.update_layout(
            title="Global Renewable Capacity Growth",
            xaxis_title="Year",
            yaxis_title="Capacity (GW)",
            hovermode='x unified',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            margin=dict(t=50, b=50, l=50, r=50),
            height=500
        )
        st.plotly_chart(fig_trends, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Country Analysis ---
st.markdown("""
<div class="section-header fade-in">
    🏆 Leading Nations & Economic Analysis
</div>
""", unsafe_allow_html=True)

col_leaders, col_economics = st.columns(2)

with col_leaders:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🥇 Top 10 Renewable Leaders")
    
    # Top countries analysis
    latest_data = df[(df['Year'] == selected_year) & (df['Entity'] != 'World')].dropna(subset=['Total_GW'])
    top_10 = latest_data.nlargest(10, 'Total_GW').sort_values('Total_GW')
    
    if not top_10.empty:
        fig_leaders = px.bar(
            top_10,
            x='Total_GW',
            y='Entity',
            orientation='h',
            color='Total_GW',
            color_continuous_scale='Viridis',
            title=f"Top 10 Countries by Total Renewable Capacity ({selected_year})",
            labels={'Total_GW': 'Total Capacity (GW)', 'Entity': 'Country'}
        )
        
        fig_leaders.update_layout(
            showlegend=False,
            margin=dict(t=50, b=50, l=100, r=50),
            height=450,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_leaders, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_economics:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💰 Economic vs. Renewable Capacity")
    
    scatter_data = df[(df['Year'] == selected_year) & (df['Entity'] != 'World')].dropna(
        subset=['GDP_per_Capita', 'Capacity_per_Capita_kW', 'Population']
    )
    
    if not scatter_data.empty:
        fig_scatter = px.scatter(
            scatter_data,
            x="GDP_per_Capita",
            y="Capacity_per_Capita_kW",
            size="Population",
            color="Total_GW",
            hover_name="Entity",
            log_x=True,
            color_continuous_scale="Plasma",
            title=f"GDP vs. Per-Capita Renewable Capacity ({selected_year})",
            labels={
                "GDP_per_Capita": "GDP per Capita (USD)",
                "Capacity_per_Capita_kW": "Renewable Capacity per Capita (kW)"
            }
        )
        
        fig_scatter.update_layout(
            margin=dict(t=50, b=50, l=50, r=50),
            height=450
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Historical Comparison ---
st.markdown("""
<div class="section-header fade-in">
    ⏰ Historical Comparison: Leaders Then vs. Now
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)

# Comparison between 2010 and 2023
year_2010, year_2023 = 2010, 2023
df_2010 = df[(df['Year'] == year_2010) & (df['Entity'] != 'World')].dropna(subset=['Capacity_per_Capita_kW'])
df_2023 = df[(df['Year'] == year_2023) & (df['Entity'] != 'World')].dropna(subset=['Capacity_per_Capita_kW'])

if not df_2010.empty and not df_2023.empty:
    top10_2023 = df_2023.nlargest(10, 'Capacity_per_Capita_kW')['Entity'].tolist()
    
    comparison_data = df[
        (df['Entity'].isin(top10_2023)) &
        (df['Year'].isin([year_2010, year_2023]))
    ].dropna(subset=['Capacity_per_Capita_kW'])
    
    if not comparison_data.empty:
        fig_comparison = px.bar(
            comparison_data,
            x='Capacity_per_Capita_kW',
            y='Entity',
            color='Year',
            orientation='h',
            barmode='group',
            title=f"Per-Capita Renewable Capacity: {year_2010} vs. {year_2023}",
            labels={'Capacity_per_Capita_kW': 'Renewable Capacity per Capita (kW)'},
            color_discrete_map={year_2010: '#74b9ff', year_2023: '#00b894'}
        )
        
        fig_comparison.update_layout(
            height=500,
            margin=dict(t=50, b=50, l=100, r=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Enhanced Footer ---
st.markdown("""
<div class="footer fade-in">
    <h4>Dashboard By - </h4>
    <p><strong>Created by:</strong> Nagesh Chillale R. | Second year IT | Walchand College of Engineering, Sangli</p>
    <p><strong>Data Source:</strong> E = MC^2 Cell , VJTI, Mumbai</p>
    
</div>
""", unsafe_allow_html=True)