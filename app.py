import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load Excel file
file_path = "Commitments of Trade Report.xlsx"
df = pd.read_excel(file_path)

# Get column Q (17th column)
column_q_name = df.columns[16]

# Prepare data
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date', column_q_name])
df = df.sort_values('Date')

# Convert values to percentages
df[column_q_name] = df[column_q_name] * 100

# App layout
st.title("Scrollable Time Series Line Graph")

st.write(f"Displaying: **{column_q_name}** vs **Date** (as percentage)")

# Plotly figure
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df[column_q_name],
    mode='lines+markers',
    name=column_q_name,
    line=dict(color='blue'),
    marker=dict(size=6)
))

# Initial range: 30-day window or fewer if less data
start_date = df['Date'].iloc[0]
end_index = min(30, len(df)-1)
end_date = df['Date'].iloc[end_index]

# Layout tweaks
fig.update_layout(
    xaxis=dict(
        title='Date',
        type='date',
        range=[start_date, end_date],
        rangeslider=dict(visible=True),
        tickangle=45,
        tickformat='%b %d\n%Y',
        ticklabelmode="period"
    ),
    yaxis=dict(
        title=f"{column_q_name} (%)",
        tickformat=".1f",  # Adjust decimal places if needed
        dtick=5  # Spacing of 5 units on the y-axis
    ),
    title=f"{column_q_name} Over Time (Percentage)",
    hovermode='x unified',
    height=600,
    margin=dict(l=40, r=40, t=60, b=100)
)

st.plotly_chart(fig, use_container_width=True)
