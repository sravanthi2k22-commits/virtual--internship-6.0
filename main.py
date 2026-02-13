from backend.config.data_config import create_dask_client
def main():
    client = create_dask_client()
    print(client)
    print(f"Dashboard: {client.dashboard_link}")
    print("Cluster running...")
if __name__ == "__main__":
    main()
