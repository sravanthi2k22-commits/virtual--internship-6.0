import streamlit as st

file = st.file_uploader("Upload file")
day = st.selectbox("Select day", [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
])
st.write("Selected day:", day)
st.title("log analytics monitoring engine")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is some text")
st.markdown("This is **markdown** text with *emphasis* and [a link](https://www.google.com).")
st.button("Click me")
st.checkbox("Check me")
st.radio("Choose an option", ["Option 1", "Option 2", "Option 3"])
st.selectbox("Select an option", ["Option A", "Option B", "Option C"])
st.multiselect("Select multiple options", ["Option X", "Option Y", "Option Z"])
st.slider("Select a value", 0, 100, 50)
st.table({"Column 1": [1, 2, 3], "Column 2": ["A", "B", "C"]})

data = {
    "minute": [
        "10:00", "10:01", "10:02", "10:03", "10:04",
        "10:05", "10:06", "10:07", "10:08", "10:09"
    ],
    "error_count": [
        5, 7, 6, 8, 50, 9, 6, 55, 7, 8
    ],  # spikes = anomalies
    "service": [
        "auth", "payment", "inventory", "shipping", "user",
        "orders", "auth", "payment", "inventory", "shipping"
    ]
}
import pandas as pd
import plotly.express as px

df = pd.DataFrame(data)
df["is_anomaly"] = df["error_count"] > 30
st.subheader("Error Trend")

fig_line = px.line(df, x="minute", y="error_count", title="Errors Over Time")
anomalies = df[df["is_anomaly"]]

fig_line.add_scatter(
    x=anomalies["minute"],
    y=anomalies["error_count"],
    mode="markers",
    name="Anomalies"
)

st.plotly_chart(fig_line)
fig = px.line(df, x="minute", y="error_count", color="service", title="Error Count Over Time by Service")
st.plotly_chart(fig)
         