# Here we detect anomalies from log data by comparing current errors and normal behavior using statistics

import dask.dataframe as dd

def detect_anamoly(log_df, z_threshold=3):

    log_df["timestamp"] = dd.to_datetime(log_df["timestamp"])

    # filter error logs
    error_logs = log_df[log_df["level"] == "ERROR"].copy()

    # count error per minute
    error_logs["minute"] = error_logs["timestamp"].dt.floor("min")

    error_counts = (
        error_logs.groupby("minute")
        .size()
        .to_frame("error_count")
    )

    # Normal behavior statistics
    mean = error_counts["error_count"].mean().compute()
    std = error_counts["error_count"].std().compute()

    if std == 0:
         result = error_counts.compute()
         result["is_anomaly"] = True   # flag all as anomalies when std is 0
         result["z_score"] = 0
         return result

    error_counts["anomaly_score"] = (error_counts["error_count"] - mean) / std
    error_counts["is_anomaly"] = error_counts["anomaly_score"].abs() > z_threshold

    return error_counts[error_counts["is_anomaly"]].compute()