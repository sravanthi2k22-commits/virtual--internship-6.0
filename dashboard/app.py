import streamlit as st
import plotly.express as px
import pandas as pd
import os
import sys

# ---------------------------------------------------
# PATH SETUP
# ---------------------------------------------------
current_script_path = os.path.dirname(os.path.abspath(__file__))

# Define the root of your project (one level up from dashboard)
root_path = os.path.abspath(os.path.join(current_script_path, ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from backend.pipeline.processing import build_pipeline
from backend.anomaly.detection import detect_anamoly

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Log Analytics Engine",
    layout="wide"
)

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("Settings")
log_file_path = st.sidebar.text_input(
    "Log File Path",
    value=r"D:\log-analytics-monitoring-engine\backend\sample_log\data_log.log"
)

if st.sidebar.button("Refresh Dashboard"):
    st.rerun()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
try:
    log_df_dask = build_pipeline(log_file_path)
    log_data = log_df_dask.compute()

    anomaly_result = detect_anamoly(log_df_dask)
    anomaly_df = anomaly_result.compute() if hasattr(anomaly_result, "compute") else anomaly_result

# ---------------------------------------------------
# PIE CHART
# ---------------------------------------------------
    st.subheader("Log Level Distribution")

    level_counts = log_data["level"].value_counts().reset_index()
    level_counts.columns = ["level", "count"]

    pie_chart = px.pie(
        level_counts,
        names="level",
        values="count",
        title="Distribution of Log Levels"
    )

    st.plotly_chart(pie_chart, use_container_width=True)

# ---------------------------------------------------
# FILTER LEVELS — .copy() prevents SettingWithCopyWarning
# ---------------------------------------------------
    error_df = log_data[log_data["level"] == "ERROR"].copy()
    info_df  = log_data[log_data["level"] == "INFO"].copy()
    warn_df  = log_data[log_data["level"] == "WARN"].copy()

# ---------------------------------------------------
# THREE TIMELINE GRAPHS
# ---------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("ERROR Logs Over Time")
        if not error_df.empty:
            fig_error = px.histogram(error_df, x="timestamp")
            st.plotly_chart(fig_error, use_container_width=True)
        else:
            st.info("No ERROR logs")

    with col2:
        st.subheader("INFO Logs Over Time")
        if not info_df.empty:
            fig_info = px.histogram(info_df, x="timestamp")
            st.plotly_chart(fig_info, use_container_width=True)
        else:
            st.info("No INFO logs")

    with col3:
        st.subheader("WARN Logs Over Time")
        if not warn_df.empty:
            fig_warn = px.histogram(warn_df, x="timestamp")
            st.plotly_chart(fig_warn, use_container_width=True)
        else:
            st.info("No WARN logs")

# ---------------------------------------------------
# ERROR TREND PER MINUTE
# ---------------------------------------------------
    st.subheader("Error Count Per Minute")

    if not error_df.empty:
        # error_df is already a copy so modifying is safe
        error_df["timestamp"] = pd.to_datetime(error_df["timestamp"])

        # Auto-detect resample rule based on time range
        time_range = error_df["timestamp"].max() - error_df["timestamp"].min()
        resample_rule = "1min" if time_range.total_seconds() > 120 else "5s"

        error_trend = (
            error_df
            .set_index("timestamp")
            .resample(resample_rule)
            .size()
            .reset_index(name="error_count")
        )

        line_chart = px.line(
            error_trend,
            x="timestamp",
            y="error_count",
            title="Error Frequency",
            markers=True  # show dots on each data point
        )

        st.plotly_chart(line_chart, use_container_width=True)
    else:
        st.info("No error data available for trend analysis")

# ---------------------------------------------------
# ANOMALY TABLE
# ---------------------------------------------------
    st.subheader("Detected Anomalies")

    if anomaly_df.empty:
        st.success("No anomalies detected")
    else:
        st.warning(f"🚨 {len(anomaly_df)} anomalies detected!")
        st.dataframe(anomaly_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing data: {str(e)}")