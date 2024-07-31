import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data (replace with your own data loading logic)
file_path = 'fixed_ssb_startup_table.xlsx'
data = pd.read_excel(file_path, sheet_name=None)
df = data['Sheet1']

# Set index for MultiIndex data structure
df.set_index(['Survival Years', 'Metric'], inplace=True)

# Streamlit app
st.title('Norwegian Startup Landscape')

# Sidebar for user inputs
st.sidebar.header('Filter Data')
years = df.columns.tolist()

# Select year range
year_range = st.sidebar.slider('Select Year Range:', min_value=int(years[0]), max_value=int(years[-1]), value=(int(years[0]), int(years[-1])))

# Select metric
metric = st.sidebar.selectbox('Select Metric:', ['Total', 'Survived', 'Not survived', 'Asleep'])

# Extract data based on user selection
filtered_df = df.loc[:, f'{year_range[0]}':f'{year_range[1]}']

try:
    selected_metric_data = filtered_df.xs(metric, level='Metric').iloc[0, :]
except KeyError:
    st.error(f"Metric '{metric}' not found in the dataset. Please check the metric names.")
    st.stop()

# Plotting total number of startups per selected metric and year range
st.header(f'{metric} Startups from {year_range[0]} to {year_range[1]}')
fig, ax = plt.subplots(figsize=(12, 6))  # Increased figure size
ax.plot(filtered_df.columns, selected_metric_data.values, marker='o', label=f'{metric} Startups')
ax.set_xlabel('Year')
ax.set_ylabel(f'Number of {metric} Startups')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# Display additional insights
st.subheader('Insights')
st.write(f"The {metric} startups data from {year_range[0]} to {year_range[1]} shows the following trends:")
st.write(f"- The maximum number of {metric.lower()} startups in this range is {selected_metric_data.max()} in {selected_metric_data.idxmax()}.")
st.write(f"- The minimum number of {metric.lower()} startups in this range is {selected_metric_data.min()} in {selected_metric_data.idxmin()}.")
