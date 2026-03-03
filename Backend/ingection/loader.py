import dask.bag as db
from backend.ingection.parser import parse_log_line
from backend.schema.schema import LOG_SCHEMA

def load_logs(file_path):
    bag = db.read_text(file_path)
    return bag
