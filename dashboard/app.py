import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import sys

# ---------------------------------------------------
# PATH SETUP
# ---------------------------------------------------
current_script_path = os.path.dirname(os.path.abspath(__file__))
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
# HELPER: build heatmap for a given level and color
# ---------------------------------------------------
def build_heatmap(df, level, colorscale):
    """
    Groups logs by second and service, returns a heatmap figure.
    colorscale options: 'Reds', 'Blues', 'Oranges', 'Greens', etc.
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["time_bucket"] = df["timestamp"].dt.floor("5s")

    pivot = (
        df.groupby(["time_bucket", "service"])
        .size()
        .reset_index(name="count")
        .pivot(index="service", columns="time_bucket", values="count")
        .fillna(0)
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=[str(t) for t in pivot.columns],
            y=pivot.index.tolist(),
            colorscale=colorscale,
            showscale=True,
        )
    )
    fig.update_layout(
        title=f"{level} Log Heatmap (Service vs Time)",
        xaxis_title="Time",
        yaxis_title="Service",
        xaxis=dict(tickangle=-45),
        height=350,
        margin=dict(l=20, r=20, t=50, b=80),
    )
    return fig


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
try:
    log_df_dask = build_pipeline(log_file_path)
    log_data = log_df_dask.compute()

    anomaly_result = detect_anamoly(log_df_dask)
    anomaly_df = (
        anomaly_result.compute()
        if hasattr(anomaly_result, "compute")
        else anomaly_result
    )

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
        title="Distribution of Log Levels",
        color="level",
        color_discrete_map={
            "ERROR": "#EF4444",
            "WARN":  "#F59E0B",
            "INFO":  "#3B82F6",
            "DEBUG": "#10B981",
        }
    )
    st.plotly_chart(pie_chart, use_container_width=True)

    # ---------------------------------------------------
    # FILTER LEVELS
    # ---------------------------------------------------
    error_df = log_data[log_data["level"] == "ERROR"].copy()
    info_df  = log_data[log_data["level"] == "INFO"].copy()
    warn_df  = log_data[log_data["level"] == "WARN"].copy()

    # ---------------------------------------------------
    # HEATMAP — ERROR (Red)
    # ---------------------------------------------------
    st.subheader("ERROR Log Heatmap")
    if not error_df.empty:
        st.plotly_chart(
            build_heatmap(error_df, "ERROR", "Reds"),
            use_container_width=True
        )
    else:
        st.info("No ERROR logs found")

    # ---------------------------------------------------
    # HEATMAP — INFO (Blue)
    # ---------------------------------------------------
    st.subheader("INFO Log Heatmap")
    if not info_df.empty:
        st.plotly_chart(
            build_heatmap(info_df, "INFO", "Blues"),
            use_container_width=True
        )
    else:
        st.info("No INFO logs found")

    # ---------------------------------------------------
    # HEATMAP — WARN (Orange)
    # ---------------------------------------------------
    st.subheader("WARN Log Heatmap")
    if not warn_df.empty:
        st.plotly_chart(
            build_heatmap(warn_df, "WARN", "Oranges"),
            use_container_width=True
        )
    else:
        st.info("No WARN logs found")

    # ---------------------------------------------------
    # ERROR TREND LINE — FIXED
    # ---------------------------------------------------
    st.subheader("Error Count Over Time")

    if not error_df.empty:
        error_df["timestamp"] = pd.to_datetime(error_df["timestamp"])

        # Auto resample: use seconds for short datasets, minutes for longer
        time_range = error_df["timestamp"].max() - error_df["timestamp"].min()
        resample_rule = "1min" if time_range.total_seconds() > 120 else "5s"

        error_trend = (
            error_df
            .set_index("timestamp")
            .resample(resample_rule)
            .size()
            .reset_index(name="error_count")
        )

        # Drop zero-count buckets so the line is not flat
        error_trend = error_trend[error_trend["error_count"] > 0]

        if len(error_trend) >= 2:
            line_chart = px.line(
                error_trend,
                x="timestamp",
                y="error_count",
                title="Error Frequency Over Time",
                markers=True,
                color_discrete_sequence=["#EF4444"],
            )
            line_chart.update_traces(line=dict(width=2))
            line_chart.update_layout(
                xaxis_title="Time",
                yaxis_title="Error Count",
                yaxis=dict(rangemode="tozero"),
            )
            st.plotly_chart(line_chart, use_container_width=True)
        else:
            # Not enough time buckets — show bar chart instead
            bar_chart = px.bar(
                error_trend,
                x="timestamp",
                y="error_count",
                title="Error Frequency (Bar — not enough time range for line)",
                color_discrete_sequence=["#EF4444"],
            )
            st.plotly_chart(bar_chart, use_container_width=True)
    else:
        st.info("No error data available for trend analysis")

    # ---------------------------------------------------
    # ANOMALY TABLE
    # ---------------------------------------------------
    st.subheader("Detected Anomalies")

    if anomaly_df.empty:
        st.success("✅ No anomalies detected")
    else:
        st.warning(f"🚨 {len(anomaly_df)} anomalies detected!")
        st.dataframe(anomaly_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing data: {str(e)}")