from dask.distributed import Client, LocalCluster
def start_dask():
    cluster = LocalCluster(
        n_workers=4,
        threads_per_worker=2,
        memory_limit='1GB',
        dashboard_address=":8790"
    )
    return Client(cluster)