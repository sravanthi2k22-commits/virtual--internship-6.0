#from backend.config.data_config import create_dask_client
'''def main():
    client = create_dask_client()
    print(client)
    print(f"Dashboard: {client.dashboard_link}")
    print("Cluster running...")
if __name__ == "__main__":
    main()'''
from datetime import time

from backend.config.dask_config import start_dask
from backend.ingection.loader import load_logs
#from processing.pipeline import build_pipeline


def main():
    print("Starting Log Processing...")
    client = start_dask()
    print("Dask Started Successfully")

    df = load_logs("D:\\log-analytics-monitoring-engine\\backend\\Log_data.log")
    print("Logs Loaded Successfully")

    print("\nFirst 5 Parsed Logs:")
    print(df.head())

    print("\nLog Count by Level:")
    result = df.count().compute()
    print(result)

    input("Press Enter to stop the cluster...")  # keep cluster alive
    client.close()
    print("\nProcessing Finished Successfully!")


if __name__ == "__main__":
    main()