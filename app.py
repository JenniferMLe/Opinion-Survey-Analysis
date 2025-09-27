import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sample data ---
df1 = pd.DataFrame({
    "year": [2020, 2021, 2022],
    "sales": [10, 15, 8]
})

df2 = pd.DataFrame({
    "year": [2020, 2021, 2022],
    "sales": [7, 12, 6]
})

df_name = {
    'Age':'AGEGRP2',
    'Race':'RACE',
    'Gender':'GENDER',
    'Income':'INCOMEGRP',
    'Education':'EDUCATION',
    'Party':'PARTY',
    'Religion':'RELIG'
}

# --- Streamlit UI ---
st.title("Opinion Survey Analysis")

# Dropdown to select dataset
dataset_choice = st.selectbox("Choose a demographic", ['Age','Race','Gender','Income','Education','Party','Religion'])

# Map selection to actual DataFrame
df = df1

# Dropdown to select year
year_choice = st.selectbox("Select year", df1)

# Filter data for selected year
df_filtered = df[df["year"] == year_choice]

# Display filtered data
st.write("Filtered Data:", df_filtered)

# Plot bar chart
fig = px.bar(df_filtered, x="year", y="sales", title='Title')
st.plotly_chart(fig)