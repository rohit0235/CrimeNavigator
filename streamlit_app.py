import altair as alt
import pandas as pd
import streamlit as st
st.set_page_config(
    page_title="Crime Navigator App",  # App title
    page_icon="🔍",  # App icon (you can use an emoji or path to an image)
    layout="wide"  # Use wide layout to increase the width of the app
)

# Load CSS file
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Your Streamlit app code goes here

# Load the dataset
file_path = 'data/01_District_wise_crimes_committed_IPC_2014.csv'
data = pd.read_csv(file_path)

# Convert column names to camel case
# data.columns = data.columns.str.title().str.replace(' ', '')

# Streamlit app title
st.title('Crime Navigator - Crime Data Visualization for Cities and States')

# Dropdown for state selection
states = data['States/UTs'].unique()
selected_state = st.selectbox('Select a state:', states)

# Filter the data for the selected state
state_data = data[data['States/UTs'] == selected_state]

# Dropdown for city selection (within the selected state)
cities_in_state = state_data['District'].unique()
selected_city = st.selectbox('Select a city in the state:', cities_in_state)

# Filter data based on the selected city
city_data = state_data[state_data['District'] == selected_city]

# Display filtered data
st.subheader(f'Crime Data for {selected_city} in {selected_state}')
st.write(city_data)

# Data Visualization: Show crime counts per category
st.subheader(f'Crime Statistics in {selected_city}')
crime_columns = ['Murder', 'Rape', 'Kidnapping & Abduction', 'Arson', 'Grievous Hurt']

# Sum of crimes for each category
crime_counts = city_data[crime_columns].sum()
# Sort the crime counts in descending order
sorted_crime_counts = crime_counts.sort_values(ascending=False)

# Display the sorted crime counts
st.bar_chart(sorted_crime_counts)

# Comparison Visualization: Crime data for all cities in the selected state
st.subheader(f'Crime Comparison in {selected_state}')
state_crime_totals = state_data.groupby('District')[crime_columns].sum()
# Create a bar chart comparison of crimes across cities in the selected state
state_crime_chart = alt.Chart(state_crime_totals).mark_bar().encode(
    x='District:N',
    y='sum(Murder):Q',
    color='District:N',
    tooltip=crime_columns
).properties(
    title=f'Comparison of Murder Crime across Cities in {selected_state}'
)

st.altair_chart(state_crime_chart, use_container_width=True)

# Danger Level Assessment
st.subheader('Danger Level Assessment')
danger_levels = city_data[crime_columns].sum().sum()  # Sum of all crimes in the selected city

if danger_levels > 500:
    st.error(f'Danger Level: High ({danger_levels} crimes reported)')
elif 100 < danger_levels <= 500:
    st.warning(f'Danger Level: Medium ({danger_levels} crimes reported)')
else:
    st.success(f'Danger Level: Low ({danger_levels} crimes reported)')

# Additional Plot: Crime Type Distribution across the State
st.subheader(f'Crime Type Distribution in {selected_state}')
crime_type_distribution = state_data.melt(id_vars='District', value_vars=crime_columns, 
                                          var_name='CrimeType', value_name='CrimeCount')

crime_distribution_chart = alt.Chart(crime_type_distribution).mark_bar(size=20).encode(
    x=alt.X('CrimeType:N', axis=alt.Axis(labelAngle=0),  # Keep crime types in their original order
            sort=None),  # Ensure no sorting happens
    y='sum(CrimeCount):Q',
    color='CrimeType:N',
    tooltip=['CrimeType', 'sum(CrimeCount)']
).properties(
    width=400,  # Adjust the width of the chart to reduce overall bar spacing
    title=f'Crime Type Distribution in {selected_state}'
).configure_axisX(
    labelAngle=0,  # Ensures labels are horizontal
    labelPadding=5  # Adjusts padding for label readability
).configure_view(
    strokeWidth=0  # Removes border around the chart for a cleaner look
)


st.altair_chart(crime_distribution_chart, use_container_width=True)
