🌍 Global Renewable Energy Trends Dashboard
This repository contains the code for an interactive Streamlit web application that visualizes global renewable energy trends, capacity, and related economic/demographic factors from 2010 to 2023. The dashboard allows users to explore insights into solar, wind, and hydro energy across various countries.

✨ Features
The dashboard provides the following key visualizations:

Global Overview: Key metrics for selected countries and years, including total solar, wind, and hydro capacity.

Renewable Energy Mix (Pie Chart): A dynamic pie chart showing the breakdown of solar, wind, and hydro capacity for a selected country and year.

World Map (Choropleth): A geographical representation of total renewable capacity (GW) by country in a selected year.

Global Renewable-Source Mix Over Time (Stacked Area Chart): Visualizes the evolution of solar, wind, and hydro contributions to the global renewable energy mix from 2010 to 2023.

Top 5 Countries Growth (Time Series): A line chart comparing the growth in total renewable capacity for the top 5 countries from 2010 to 2023.

GDP vs. Renewable Capacity per Capita (Scatter Plot): Explores the relationship between a country's GDP per capita and its renewable capacity per capita, with points sized by population for the selected year.

Top 10 Per-Capita Leaders Comparison (Bar Chart): A comparison bar chart showcasing the top 10 per-capita leaders in renewable generation for both 2010 and 2023.

🚀 Getting Started
Follow these instructions to set up and run the Streamlit dashboard on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7+: Download Python

pip: Python's package installer (usually comes with Python)


Installation
Clone the Repository (or Download Files):
If you are using Git, clone this repository:

git clone [www.github.com/nageshchillale/]
cd [Renewable Energy Analysis and Visualization]

If you downloaded the files, navigate to the project directory in your terminal.

Create a Virtual Environment (Recommended):
It's good practice to use a virtual environment to manage project dependencies.

python -m venv venv

Activate the Virtual Environment:

Windows:

.\venv\Scripts\activate



Install Dependencies:
Install the required Python libraries using pip:

pip install streamlit pandas plotly matplotlib seaborn numpy

Data Setup
The dashboard relies on a pre-processed CSV file.

Place the Data File:
Ensure your final cleaned and merged dataset, named final_renewables_dataset.csv, is placed in the same directory as the app.py file.

Note: This final_renewables_dataset.csv should contain columns such as Entity, Code, Year, Solar_GW, Wind_GW, Hydro_GW, Total_GW, Population, GDP_per_Capita, and Capacity_per_Capita_kW.

Running the Application
Navigate to the Project Directory:
Open your terminal or command prompt and navigate to the directory where app.py and final_renewables_dataset.csv are located.

cd /path/to/your/project/folder

(Replace /path/to/your/project/folder with the actual path.)

Run the Streamlit App:
Execute the following command:

streamlit run app.py

Access the Dashboard:
Your default web browser should automatically open a new tab displaying the dashboard (usually at http://localhost:8501).

📊🙏 Acknowledgements
Thanks to the maintainers of pandas, streamlit, plotly, matplotlib, and seaborn for their excellent libraries.

Special thanks to Prof. Ankur , Prof. Wagh , VJTI-Mumbai
