from pyspark.sql import SparkSession
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
from logs.logger import ETL_Logger, ErrorCategory
from dotenv import load_dotenv

import zipfile, os, glob, json, shutil


load_dotenv()

STATE_FILE = "kaggle_dataset_state.json"
EXTERNAL_DIRECTORY = "datasets/external"
EXTRACTED_ROOT = os.path.join(EXTERNAL_DIRECTORY, "extracted")

# Each dataset gets its own staging table — no shared/forced schema across datasets.
DATASET_TABLE_MAP = {
    'ricardobj/electric-vehicle-population': 'raw_ev_population',
    'syedanwarafridi/vehicle-sales-data': 'raw_vehicle_sales',
    'sahirmaharajj/fuel-economy': 'raw_fuel_economy',
}

DATASETS = list(DATASET_TABLE_MAP.keys())

log = ETL_Logger(ErrorCategory.GENERAL)

def extract_data(file_path: str):
    """Read a single CSV file into a Spark DataFrame."""
    spark = SparkSession.builder \
        .appName("Data Extraction") \
        .getOrCreate()
    path = Path(file_path)
    
    if not path.exists():        
        log.error(f"File not Found: {file_path}")
        raise FileNotFoundError(f"File not found : {file_path}")
    log.info(f"Extracting Data from {file_path}")

    data = spark.read.csv(str(path), header=True, inferSchema=True)

    log.info(f"Dataset size: {data.count()}")
    print(f"Dataset size: {data.count()}")
    return data

def load_state():
    if os.path.exists(STATE_FILE):
        log.info(f"Loading Kaggle version file from {STATE_FILE}")
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        log.info(f"Saving {STATE_FILE}")
        json.dump(state, f, indent=2)

def get_remote_last_updated(api, ds):
    owner, dataset_name = ds.split("/")
    results = api.dataset_list(search=dataset_name, user=owner)
    match = next((r for r in results if r.ref == ds), None)

    if match is None:
        log.warning(f"'{ds}' not found via Kaggle search — will download to be safe.")
        print(f"WARNING: '{ds}' not found via Kaggle search — will download to be safe.")
        return None

    last_updated = match.last_updated
    return last_updated.isoformat() if hasattr(last_updated, "isoformat") else str(last_updated)

def get_dataset_paths(ds):
    dataset_slug = ds.split("/")[1]
    zip_path = os.path.join(EXTERNAL_DIRECTORY, f"{dataset_slug}.zip")
    extract_to = os.path.join(EXTRACTED_ROOT, dataset_slug)
    log.info("Extraction Complete")
    return dataset_slug, zip_path, extract_to

def is_up_to_date(ds, state, extract_to):
    remote_updated = get_remote_last_updated(_api, ds)
    local_updated = state.get(ds)
    already_extracted = os.path.exists(extract_to) and bool(glob.glob(os.path.join(extract_to, "*.csv")))
    
    return (local_updated == remote_updated and already_extracted), remote_updated

def _extract(zip_path, ds, extract_to):
    with zipfile.ZipFile(zip_path, "r") as z:
        log.info(f"Extracting {ds} to {extract_to}")
        z.extractall(extract_to) 
        
def download_and_extract(ds, zip_path, extract_to, up_to_date):
    
    if not os.path.exists(extract_to) and not up_to_date:
        log.info(f"Creating file directory: {extract_to}")
        os.makedirs(extract_to, exist_ok=True)
        _api.dataset_download_files(ds, path=EXTERNAL_DIRECTORY, force=True)
        _extract(zip_path,ds,extract_to)
        
        log.info(f"Downloading (changed): {ds}")
    elif not up_to_date:
        _api.dataset_download_files(ds, path=EXTERNAL_DIRECTORY, force=True)
        _extract(zip_path,ds,extract_to)
    else:
        log.info(f"Path exists: {extract_to}")
        shutil.rmtree(extract_to)


def load_csvs_as_dataframes(extract_to):
    dfs = []
    
    log.info("Loading CSV's as Dataframes")
    for csv_file in glob.glob(os.path.join(extract_to, "*.csv")):
        dfs.append(extract_data(csv_file))
        
    return dfs

def kaggle_extract_data(datasets=None):

    global _api
    if datasets is None:
        datasets = DATASETS

    _api = KaggleApi()
    _api.authenticate()

    state = load_state()
    data_completed = []
    results = []  # list of (table_name, dataframe)
    for ds in datasets:
        _, zip_path, extract_to = get_dataset_paths(ds)
        log.info("Checking if datasets are up to date")
        up_to_date, remote_updated = is_up_to_date(ds, state, extract_to)

        if up_to_date:
            log.info(f"Skipping {ds} - no changes since last pull ({state.get(ds)})")
            continue
        
        else:
            log.info(f"Downloading {ds} from Kaggle please wait.")
            download_and_extract(ds, zip_path, extract_to, up_to_date)
            state[ds] = remote_updated
            data_completed.append(ds)
            log.info(f"Finished Downloading and extracting {ds}")

        table_name = DATASET_TABLE_MAP[ds]
        for df in load_csvs_as_dataframes(extract_to):
            results.append((table_name, df))
        log.info(f"Finished loading {ds}")
        
    save_state(state)
    return results
