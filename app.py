# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # For numerical operations, e.g., handling NaNs

# --- Configuration ---
st.set_page_config(
    page_title="Global Renewable Energy Dashboard",
    page_icon="🌍",
    layout="wide" # Use 'wide' for a broader layout
)

# --- Load Data ---
# Use st.cache_data to cache the DataFrame, improving performance on re-runs
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final_renewables_dataset.csv")

        # --- Data Cleaning and Type Conversion ---
        # Ensure 'Year' is integer
        if 'Year' in df.columns:
            # Coerce errors to NaN, then fill NaN with a common value (e.g., 0) before converting to int
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
        else:
            st.error("Column 'Year' not found in the dataset. Please check your CSV.")
            st.stop() # Stop the app if a critical column is missing

        # Ensure numeric columns are proper floats, coercing errors to NaN
        # Using the exact column names provided by the user
        numeric_cols = [
            'Solar_GW', 'Wind_GW', 'Hydro_GW', 'Total_GW',
            'Population', 'GDP_per_Capita', 'Capacity_per_Capita_kW'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                st.warning(f"Column '{col}' not found in the dataset. Some plots may not work as expected.")

        # Handle potential duplicate country name columns if they exist, keeping 'Entity' primary
        df = df.drop(columns=['Country Name_x', 'Country Name_y', 'Country'], errors='ignore')

        # Drop rows where 'Entity' or 'Code' (for map) or 'Year' are missing
        df.dropna(subset=['Entity', 'Code', 'Year'], inplace=True)

        return df

    except FileNotFoundError:
        st.error("Error: 'final_renewables_dataset.csv' not found. Please ensure it's in the same directory as app.py.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading or processing data: {e}. Please check your CSV file's format and column names.")
        st.stop()

df = load_data()


# --- Dashboard Title and Introduction ---
st.title("🌍 Global Renewable Energy Trends Dashboard")
st.markdown("A comprehensive look at renewable energy capacity, GDP, and population dynamics across the globe.")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Get unique years and countries for filters
years = sorted(df["Year"].dropna().unique())
countries = sorted(df["Entity"].dropna().unique())

# Year slider for interactive charts
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=2023 # Default to the latest year
)

# Country selectbox for country-specific charts
selected_country = st.sidebar.selectbox(
    "Select Country",
    countries,
    index=countries.index("World") if "World" in countries else 0 # Default to 'World' or first country
)


# --- Row 1: Key Metrics & Country-Specific Mix (Pie Chart) ---
st.header(f"Insights for {selected_country} in {selected_year}")

# Filter data for selected country and year
filtered_country_data = df[(df["Year"] == selected_year) & (df["Entity"] == selected_country)]

if not filtered_country_data.empty:
    # Use .iloc[0] to get the row as a Series for easier access
    country_row = filtered_country_data.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    # Display key metrics using .get() for safe access in case a column is sometimes missing
    with col1:
        st.metric(label="Total Solar (GW)", value=f"{country_row.get('Solar_GW', 0):,.2f}")
    with col2:
        st.metric(label="Total Wind (GW)", value=f"{country_row.get('Wind_GW', 0):,.2f}")
    with col3:
        st.metric(label="Total Hydro (GW)", value=f"{country_row.get('Hydro_GW', 0):,.2f}")
    with col4:
        st.metric(label="Total Renewable (GW)", value=f"{country_row.get('Total_GW', 0):,.2f}")
    with col5:
        st.metric(label="Per Capita Capacity (kW)", value=f"{country_row.get('Capacity_per_Capita_kW', 0):,.2f}")


    # Pie chart for energy mix (Plotly for interactivity)
    st.subheader(f"Renewable Energy Mix in {selected_country} ({selected_year})")
    mix_data = {
        'Solar (GW)': country_row.get('Solar_GW', 0),
        'Wind (GW)': country_row.get('Wind_GW', 0),
        'Hydro (GW)': country_row.get('Hydro_GW', 0)
    }
    mix_df = pd.DataFrame([mix_data]).melt(var_name='Source', value_name='Capacity_GW')
    mix_df = mix_df[mix_df['Capacity_GW'] > 0] # Only show sources with actual capacity

    if not mix_df.empty and mix_df['Capacity_GW'].sum() > 0:
        fig_pie = px.pie(
            mix_df,
            names='Source',
            values='Capacity_GW',
            title="Breakdown by Source",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No renewable energy mix data available for the selected country and year.")

else:
    st.info(f"No detailed data available for {selected_country} in {selected_year}. Please select a different country or year.")


# --- Row 2: World Map (Choropleth) & Global Stacked Area Chart ---
st.markdown("---") # Separator
col_map, col_stacked_area = st.columns(2)

with col_map:
    st.header(f"Total Renewable Capacity (GW) by Country in {selected_year}")

    # Filter data for the selected year and exclude 'World' for the map
    map_data = df[(df['Year'] == selected_year) & (df['Entity'] != 'World')].dropna(subset=['Total_GW', 'Code'])

    if not map_data.empty:
        fig_map = px.choropleth(
            map_data,
            locations="Code", # Use 'Code' for ISO country codes
            color="Total_GW", # Color intensity based on total renewable GW
            hover_name="Entity", # Show country name on hover
            color_continuous_scale=px.colors.sequential.Plasma, # A nice color scale
            title=f"Total Renewable Capacity (GW) in {selected_year}",
            projection="natural earth" # Good projection for world maps
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info(f"No global renewable capacity data for map in {selected_year}.")


with col_stacked_area:
    st.header("Global Renewable-Source Mix Over Time")

    # Aggregate global data by summing up all countries' capacities for each year
    # Exclude 'World' entity if it's a sum of all others to avoid double counting
    global_trend_data = df[df['Entity'] != 'World'].groupby('Year')[['Solar_GW', 'Wind_GW', 'Hydro_GW']].sum().reset_index()
    global_trend_data.rename(columns={'Solar_GW': 'Solar (GW)', 'Wind_GW': 'Wind (GW)', 'Hydro_GW': 'Hydro (GW)'}, inplace=True)


    stacked_cols = ['Solar (GW)', 'Wind (GW)', 'Hydro (GW)']

    # Melt data for stacked area chart
    global_mix_long = global_trend_data.melt(id_vars=['Year'], value_vars=stacked_cols,
                                             var_name='Source', value_name='Capacity_GW')
    global_mix_long = global_mix_long.dropna(subset=['Capacity_GW']) # Remove rows with NaN capacity

    if not global_mix_long.empty:
        fig_stacked = px.area(
            global_mix_long,
            x="Year",
            y="Capacity_GW",
            color="Source",
            title="Global Renewable Capacity Mix Over Time (GW)",
            color_discrete_map={
                'Solar (GW)': 'orange',
                'Wind (GW)': 'lightblue',
                'Hydro (GW)': 'blue'
            }
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
    else:
        st.info("No global renewable mix data available for charting.")


# --- Row 3: Top 5 Countries Time Series & GDP vs Per-Capita Scatter Plot ---
st.markdown("---") # Separator
col_top5_ts, col_gdp_scatter = st.columns(2)

with col_top5_ts:
    st.header("Top 5 Countries Growth in Total Renewable Capacity (2010–2023)")

    # Calculate total renewable capacity for each country over time
    country_total_renewable = df.groupby(['Entity', 'Year'])['Total_GW'].sum().reset_index()
    country_total_renewable = country_total_renewable[country_total_renewable['Entity'] != 'World'] # Exclude 'World' or other aggregates

    # Get the latest year's total capacity for ranking
    latest_year_data = country_total_renewable[country_total_renewable['Year'] == selected_year].copy()
    if not latest_year_data.empty:
        # Ensure 'Total_GW' is numeric and handle NaNs for sorting
        latest_year_data['Total_GW'] = pd.to_numeric(latest_year_data['Total_GW'], errors='coerce').fillna(0) # Fill for sorting

        top_5_entities = latest_year_data.nlargest(5, 'Total_GW')['Entity'].tolist()

        if top_5_entities:
            # Filter the main DataFrame for these top 5 countries over all years
            top5_time_series = df[df['Entity'].isin(top_5_entities)].sort_values(by='Year').copy()
            top5_time_series.dropna(subset=['Total_GW'], inplace=True) # Drop NaNs for plotting

            if not top5_time_series.empty:
                fig_top5_ts = px.line(
                    top5_time_series,
                    x="Year",
                    y="Total_GW",
                    color="Entity",
                    title="Top 5 Countries Total Renewable Capacity Over Time (GW)",
                    labels={"Total_GW": "Total Renewable Capacity (GW)"}
                )
                st.plotly_chart(fig_top5_ts, use_container_width=True)
            else:
                st.info("Insufficient data for selected top 5 countries time series.")
        else:
            st.info(f"Could not determine top 5 countries for {selected_year}. Data might be insufficient.")
    else:
        st.info(f"No data available for top 5 country growth in {selected_year}.")


with col_gdp_scatter:
    st.header("GDP per Capita vs. Renewable Capacity per Capita")

    # Data for scatter plot (latest year, excluding 'World')
    scatter_data = df[(df['Year'] == selected_year) & (df['Entity'] != 'World')].copy()
    # Ensure columns are numeric and drop NaNs for plotting
    scatter_data = scatter_data.dropna(subset=['GDP_per_Capita', 'Capacity_per_Capita_kW', 'Population']) # Also drop NaN in Population for sizing

    if not scatter_data.empty:
        fig_scatter = px.scatter(
            scatter_data,
            x="GDP_per_Capita",
            y="Capacity_per_Capita_kW",
            hover_name="Entity",
            size="Population", # Size points by population
            color="Entity", # Color by country
            log_x=True, # GDP often benefits from log scale
            title=f"GDP per Capita vs. Per-Capita Renewable Capacity ({selected_year})",
            labels={
                "GDP_per_Capita": "GDP per Capita (USD)",
                "Capacity_per_Capita_kW": "Renewable Capacity per Capita (kW)"
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info(f"No scatter plot data for GDP vs. Per-Capita Renewable Capacity in {selected_year}.")


# --- Row 4: Top 10 Per-Capita Leaders (Before/After Comparison) ---
st.markdown("---") # Separator
st.header("Top 10 Per-Capita Renewable Leaders: 2010 vs. 2023 Comparison")

# Define the comparison years
year_2010 = 2010
year_2023 = 2023

# Filter data for both years and exclude 'World'
df_comp_2010 = df[(df['Year'] == year_2010) & (df['Entity'] != 'World')].dropna(subset=['Capacity_per_Capita_kW']).copy()
df_comp_2023 = df[(df['Year'] == year_2023) & (df['Entity'] != 'World')].dropna(subset=['Capacity_per_Capita_kW']).copy()

if not df_comp_2010.empty and not df_comp_2023.empty:
    # Identify top 10 from 2023 for consistent comparison
    top10_2023_entities = df_comp_2023.nlargest(10, 'Capacity_per_Capita_kW')['Entity'].tolist()

    if top10_2023_entities:
        # Filter both years for these top 10 countries
        comparison_data = df[
            (df['Entity'].isin(top10_2023_entities)) &
            (df['Year'].isin([year_2010, year_2023]))
        ].copy()

        # Ensure numeric columns are proper floats before plotting
        comparison_data['Capacity_per_Capita_kW'] = pd.to_numeric(comparison_data['Capacity_per_Capita_kW'], errors='coerce')
        comparison_data.dropna(subset=['Capacity_per_Capita_kW'], inplace=True)

        if not comparison_data.empty:
            # Create a combined bar chart
            fig_comp_bar = px.bar(
                comparison_data,
                x='Capacity_per_Capita_kW',
                y='Entity',
                color='Year', # Color bars by year for comparison
                barmode='group', # Group bars by country
                orientation='h', # Horizontal bars
                title=f"Top 10 Per-Capita Renewable Leaders ({year_2010} vs. {year_2023})",
                labels={
                    "Capacity_per_Capita_kW": "Renewable Capacity per Capita (kW)",
                    "Entity": "Country"
                },
                # Order countries by their 2023 capacity for better readability
                category_orders={"Entity": df_comp_2023.set_index('Entity').loc[top10_2023_entities].sort_values(by='Capacity_per_Capita_kW', ascending=True).index.tolist()}
            )
            st.plotly_chart(fig_comp_bar, use_container_width=True)
        else:
            st.info("No comparison data available for the top 10 countries across both years.")
    else:
        st.info("Could not determine top 10 countries for comparison (data might be missing for 2023).")
else:
    st.info(f"Data for {year_2010} or {year_2023} is insufficient for comparison chart.")


# --- Footer ---
st.markdown("---")
st.markdown("Dashboard by Your Nagesh Chillale R. , Walchand College of engineering , Sangli | Data Source: By Prof. Shashank Verma , VJTI , Mumbai")
