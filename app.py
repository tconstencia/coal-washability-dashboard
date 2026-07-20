import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Coal Washability Dashboard", layout="wide")
st.title("Pit F HG Coal Washability Dashboard")

# 2. Load the Dataset
@st.cache_data
def load_data():
    data = {
        "Source": ["Pit F"] * 60,
        "Seam": (["Seam 4"] * 20) + (["Seam 2"] * 20) + (["Combined"] * 20),
        "Sizing": (["fines"] * 10 + ["coarse"] * 10) * 3,
        "RD": [1.40, 1.45, 1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85] * 6,
        "Yield": [
            14.83, 30.21, 43.66, 55.83, 65.27, 72.64, 78.07, 82.75, 85.13, 87.79,
            8.70, 23.28, 35.61, 48.93, 56.95, 66.92, 74.52, 80.15, 82.76, 85.58,
            11.12, 20.29, 30.14, 40.58, 50.56, 60.33, 67.74, 75.92, 80.43, 85.00,
            6.31, 16.83, 28.88, 39.12, 48.44, 58.75, 66.15, 73.25, 76.22, 79.59,
            12.36, 23.81, 34.74, 45.42, 59.31, 70.45, 77.31, 82.60, 85.56, 88.30,
            9.12, 21.22, 31.66, 44.37, 55.76, 66.96, 73.99, 77.51, 80.76, 83.71
        ],
        "Ash": [
            5.96, 7.68, 9.70, 11.70, 13.42, 14.93, 16.14, 17.29, 17.91, 18.69,
            8.09, 10.32, 12.44, 14.82, 16.44, 18.58, 20.23, 21.47, 22.11, 22.87,
            7.69, 9.27, 11.16, 13.16, 15.02, 17.04, 18.67, 20.54, 21.62, 22.83,
            9.57, 11.74, 13.79, 15.34, 16.90, 18.97, 20.55, 22.21, 22.99, 23.91,
            7.07, 8.78, 10.63, 12.10, 14.35, 16.50, 17.95, 19.17, 19.90, 20.66,
            7.41, 10.17, 12.35, 14.75, 16.43, 18.49, 19.96, 20.76, 21.51, 22.32
        ],
        "CV": [
            30.75, 29.87, 29.00, 28.12, 27.41, 26.79, 26.30, 25.84, 25.59, 25.28,
            29.39, 28.54, 27.60, 26.69, 26.08, 25.25, 24.60, 24.11, 23.86, 23.56,
            29.46, 28.85, 28.00, 27.16, 26.38, 25.54, 24.89, 24.17, 23.75, 23.27,
            28.33, 27.24, 26.39, 25.85, 25.28, 24.40, 23.78, 23.15, 22.86, 22.52,
            29.96, 29.22, 28.40, 27.78, 26.78, 25.90, 25.31, 24.83, 24.53, 24.23,
            29.58, 28.44, 27.60, 26.62, 25.93, 25.07, 24.46, 24.15, 23.82, 23.51
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Interactive Filters
st.sidebar.header("Filter Controls")
selected_seam = st.sidebar.selectbox("Select Seam:", options=df['Seam'].unique())
selected_size = st.sidebar.radio("Select Sizing:", options=df['Sizing'].unique())

# 4. Filter the DataFrame
filtered_df = df[(df['Seam'] == selected_seam) & (df['Sizing'] == selected_size)]

# 5. Build the Interactive Plotly Chart (Dual Axis)
fig = go.Figure()

# Add CV Trace (Primary Y-Axis)
fig.add_trace(go.Scatter(
    x=filtered_df['RD'], y=filtered_df['CV'],
    name='CV (MJ/kg)', mode='lines+markers', line=dict(color='blue', width=3)
))

# Add Ash Trace (Secondary Y-Axis)
fig.add_trace(go.Scatter(
    x=filtered_df['RD'], y=filtered_df['Ash'],
    name='Ash (%)', mode='lines+markers', line=dict(color='red', width=3, dash='dash'),
    yaxis='y2'
))

# Configure Dual Axis Layout
fig.update_layout(
    title=f"Washability Curves: {selected_seam} ({selected_size.capitalize()})",
    xaxis=dict(title='Relative Density (RD)'),
    
    # Define Y1
    yaxis=dict(
        title='Calorific Value (MJ/kg)', 
        titlefont=dict(color='blue'), 
        tickfont=dict(color='blue')
    ),
    
    # Define Y2 explicitly and link it to the plot
    yaxis2=dict(
        title='Ash (%)', 
        titlefont=dict(color='red'), 
        tickfont=dict(color='red'), 
        overlaying='y', 
        side='right'
    ),
    
    # Ensure the chart knows to use both y-axes
    hovermode="x unified"
)

# 6. Render on Dashboard
st.plotly_chart(fig, use_container_width=True)

# 7. Display the Raw Data Table
st.subheader("Tabular Data")
st.dataframe(filtered_df, use_container_width=True)
