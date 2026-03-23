import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data 
data = {
    "minute": [
        "10:00", "10:01", "10:02", "10:03", "10:04",
        "10:05", "10:06", "10:07", "10:08", "10:09"
    ],
    "error_count": [5, 7, 6, 8, 50, 9, 6, 55, 7, 8],  
    "service": [
        "auth", "payment", "inventory", "shipping", "user",
        "orders", "auth", "payment", "inventory", "shipping"
    ]
}

df = pd.DataFrame(data)

# Anomalies = error count above 30
anomalies = df[df["error_count"] > 30]

#1. Line Chart – Error Trend 
fig_line = px.line(df, x="minute", y="error_count", title="Error Trend – Errors Over Time")
fig_line.add_scatter(
    x=anomalies["minute"],
    y=anomalies["error_count"],
    mode="markers",
    name="Anomalies"
)
st.plotly_chart(fig_line)

#  2. Bar Chart – Errors per Minute
fig_bar = px.bar(
df, x="minute", y="error_count", color="error_count", title="Bar Chart  Error Count per Minute")
st.plotly_chart(fig_bar)

#3. Scatter Plot – Anomaly Detection 
fig_scatter = px.scatter(df, x="minute", y="error_count", color="error_count", size="error_count", title="Scatter Plot  Anomaly Detection")
fig_scatter.add_scatter(x=anomalies["minute"], y=anomalies["error_count"], mode="markers", marker=dict(size=12, color="red"), name="Anomalies")
st.plotly_chart(fig_scatter)

# 4. Pie Chart – Error Share by Service 
service_errors = df.groupby("service")["error_count"].sum().reset_index()
fig_pie = px.pie(
    service_errors,
    names="service", values="error_count",
    title="Pie Chart Error Distribution by Service"
)
st.plotly_chart(fig_pie)

# 5. Heatmap – Error Intensity 
df["minute"] = pd.to_datetime(df["minute"], format="%H:%M")
heatmap_data = df.pivot_table(values="error_count", index="service", columns="minute")
fig_heatmap = px.imshow(heatmap_data, aspect="auto", title="Heatmap  Error Intensity by Service & Time")
st.plotly_chart(fig_heatmap)