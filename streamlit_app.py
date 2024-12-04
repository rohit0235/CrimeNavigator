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
file_paths = [
    'data/01_District_wise_crimes_committed_IPC_2013.csv',
    'data/02_01_District_wise_crimes_committed_against_SC_2001_2012',
    'data/01_District_wise_crimes_committed_IPC_2014.csv',

    # Add paths for other years as needed
]

# # Read and combine the datasets
dataframes = [pd.read_csv(file_path) for file_path in file_paths]
data = pd.concat(dataframes, ignore_index=True)
# data = data.drop_duplicates()  # Remove duplicates


crime_columns = ['Murder', 'Rape', 'KIDNAPPING & ABDUCTION', 'Arson', 'Grievous Hurt']
# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Select a view:",
    ("Home", "Crime Data Visualization", "Danger Level Assessment", "Woman Safety")
)

if option == "Home":
    st.write("Welcome to the Crime Navigator App!")
    st.write("Use the sidebar to navigate through different views of the crime data.")

elif option == "Crime Data Visualization":
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
    crime_columns = ['Murder', 'Rape', 'KIDNAPPING & ABDUCTION', 'Arson', 'Grievous Hurt']

    # Sum of crimes for each category
    crime_counts = city_data[crime_columns].sum()
    # Sort the crime counts in descending order
    sorted_crime_counts = crime_counts.sort_values(ascending=False)

    # Display the sorted crime counts
    st.bar_chart(sorted_crime_counts)

    # Comparison Visualization: Crime data for all cities in the selected state
    st.subheader(f'Crime Comparison in {selected_state}')
    state_crime_totals = state_data.groupby('District')[crime_columns].sum().reset_index()
    # Create a bar chart comparison of crimes across cities in the selected state
    state_crime_chart = alt.Chart(state_crime_totals).mark_bar().encode(
        x='District:N',
        y='sum(Murder):Q',
        color='District:N',
        tooltip=crime_columns
    ).properties(
        title=f'Comparison of Murder Crime across Cities in {selected_state}'
    )
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
    st.altair_chart(state_crime_chart, use_container_width=True)

elif option == "Danger Level Assessment":
    # Danger Level Assessment
    st.subheader('Danger Level Assessment')
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

    danger_levels = city_data[crime_columns].sum().sum()  # Sum of all crimes in the selected city

    if danger_levels > 500:
        st.error(f'Danger Level: High ({danger_levels} crimes reported)')
    elif 100 < danger_levels <= 500:
        st.warning(f'Danger Level: Medium ({danger_levels} crimes reported)')
    else:
        st.success(f'Danger Level: Low ({danger_levels} crimes reported)')

elif option == "Crime Type Distribution":
    # Additional Plot: Crime Type Distribution across the State

    
    # Dropdown for state selection
    states = data['States/UTs'].unique()
    selected_state = st.selectbox('Select a state:', states)

    st.subheader(f'Crime Type Distribution in {selected_state}')
    # Filter data for the selected state
    state_data = data[data['States/UTs'] == selected_state]
    
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

elif option == "Woman Safety":
    # Additional Plot: Crime Type Distribution across the State

    
    rape_victims = pd.read_csv('data/20_Victims_of_rape.csv')  # Load your rape victims dataset here

    # State Selection
    states = rape_victims['Area_Name'].unique()
    selected_state = st.selectbox('Select a state:', states)

    # Filter data based on selected state
    filtered_data = rape_victims[rape_victims['Area_Name'] == selected_state]

    # 1. Trend Analysis
    trend_data = filtered_data.groupby('Year')['Rape_Cases_Reported'].sum().reset_index()
    trend_chart = alt.Chart(trend_data).mark_line(point=True).encode(
        x='Year:O',
        y='Rape_Cases_Reported:Q',
        tooltip=['Year', 'Rape_Cases_Reported']
    ).properties(title='Trend Analysis of Reported Rape Cases')
    st.altair_chart(trend_chart, use_container_width=True)

    # 2. Age Group Analysis
    age_group_data = filtered_data.groupby('Subgroup')[['Victims_Above_50_Yrs', 'Victims_Between_10-14_Yrs', 
                     'Victims_Between_14-18_Yrs', 'Victims_Between_18-30_Yrs', 
                     'Victims_Between_30-50_Yrs', 'Victims_Upto_10_Yrs']].sum().reset_index()
    age_group_chart = alt.Chart(age_group_data).mark_bar().encode(
        x='Subgroup:N',
        y=alt.Y('sum(Victims_Above_50_Yrs):Q', title='Number of Cases'),
        color='Subgroup:N',
        tooltip=['Subgroup', 'sum(Victims_Above_50_Yrs)', 'sum(Victims_Between_10-14_Yrs)', 
                 'sum(Victims_Between_14-18_Yrs)', 'sum(Victims_Between_18-30_Yrs)', 
                 'sum(Victims_Between_30-50_Yrs)', 'sum(Victims_Upto_10_Yrs)']
    ).properties(title='Age Group Analysis of Reported Rape Cases')
    st.altair_chart(age_group_chart, use_container_width=True)

    # 3. Regional Comparison
    regional_data = filtered_data.pivot_table(values='Rape_Cases_Reported', index='Area_Name', columns='Year', aggfunc='sum').fillna(0)
    heatmap_data = regional_data.reset_index().melt(id_vars='Area_Name', var_name='Year', value_name='Rape_Cases_Reported')
    heatmap = alt.Chart(heatmap_data).mark_rect().encode(
        x='Year:N',
        y='Area_Name:N',
        color='Rape_Cases_Reported:Q'
    ).properties(title='Regional Comparison of Reported Rape Cases Over Years')
    st.altair_chart(heatmap, use_container_width=True)

    victim_demographics_data = filtered_data[['Victims_Above_50_Yrs', 'Victims_Between_10-14_Yrs', 
                                               'Victims_Between_14-18_Yrs', 'Victims_Between_18-30_Yrs', 
                                               'Victims_Between_30-50_Yrs', 'Victims_Upto_10_Yrs']].sum().reset_index()
    victim_demographics_data.columns = ['Demographic', 'Count']  # Rename columns for the pie chart
    victim_demographics_chart = alt.Chart(victim_demographics_data).mark_arc().encode(
        theta=alt.Theta(field='Count', type='quantitative', title='Number of Victims'),
        color=alt.Color(field='Demographic', type='nominal', title='Demographic Group'),
        tooltip=['Demographic', 'Count']
    ).properties(title='Demographics of Rape Victims')
    st.altair_chart(victim_demographics_chart, use_container_width=True)
