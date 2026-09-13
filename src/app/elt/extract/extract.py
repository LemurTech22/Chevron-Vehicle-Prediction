from pyspark.sql import SparkSession
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile, os, glob, time, json
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = "kaggle_dataset_state.json"
EXTERNAL_DIRECTORY = "../datasets/external"
EXTRACTED_ROOT = os.path.join(EXTERNAL_DIRECTORY, "extracted")

DATASETS = [
    'tanishqdublish/vehcile-fuel-consumption',
    'msjahid/colorado-motor-vehicle-sales-data',
    'ricardobj/electric-vehicle-population',
    'willianoliveiragibin/electric-vehicle-population',
    'syedanwarafridi/vehicle-sales-data',
    'sahirmaharajj/fuel-economy',
    'kanchana1990/vehicle-dataset-2024',
]


def extract_data(file_path: str):
    """Read a single CSV file into a Spark DataFrame."""
    spark = SparkSession.builder \
        .appName("Data Extraction") \
        .getOrCreate()
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found : {file_path}")
    print(f"Extracting Data from {file_path}")
    data = spark.read.csv(str(path),header=True, inferSchema=True)
    print(f"Dataset size: {data.count()}")
    return data


def load_state():
    """Load the last-known 'lastUpdated' timestamp per dataset."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    """Persist the current per-dataset timestamps to disk."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_remote_last_updated(api, ds):
    """Look up a dataset's last-updated timestamp via Kaggle search."""
    owner, dataset_name = ds.split("/")
    results = api.dataset_list(search=dataset_name, user=owner)
    match = next((r for r in results if r.ref == ds), None)

    if match is None:
        print(f"WARNING: '{ds}' not found via Kaggle search — will download to be safe.")
        return None

    last_updated = match.last_updated
    return last_updated.isoformat() if hasattr(last_updated, "isoformat") else str(last_updated)


def get_dataset_paths(ds):
    """Compute the zip path and extraction folder for a given dataset ref."""
    dataset_slug = ds.split("/")[1]
    zip_path = os.path.join(EXTERNAL_DIRECTORY, f"{dataset_slug}.zip")
    extract_to = os.path.join(EXTRACTED_ROOT, dataset_slug)
    return dataset_slug, zip_path, extract_to


def is_up_to_date(ds, state, extract_to):
    """A dataset is up to date if its timestamp hasn't changed AND it's already extracted."""
    remote_updated = get_remote_last_updated(_api, ds)
    local_updated = state.get(ds)
    already_extracted = os.path.exists(extract_to) and bool(glob.glob(os.path.join(extract_to, "*.csv")))
    return (local_updated == remote_updated and already_extracted), remote_updated


def download_and_extract(ds, zip_path, extract_to):
    """Download a dataset from Kaggle and unzip it into extract_to."""
    print(f"Downloading (changed): {ds}")
    _api.dataset_download_files(ds, path=EXTERNAL_DIRECTORY, force=True)

    os.makedirs(extract_to, exist_ok=True)
    print(f"Extracting {ds} to {extract_to}")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_to)


def load_csvs_as_dataframes(extract_to):
    """Load every CSV found in a folder into a list of Spark DataFrames."""
    dfs = []
    for csv_file in glob.glob(os.path.join(extract_to, "*.csv")):
        dfs.append(extract_data(csv_file))
        time.sleep(1)
    return dfs


def kaggle_extract_data(datasets=None):
    """Download (if changed), extract, and load all configured Kaggle datasets."""
    global _api
    if datasets is None:
        datasets = DATASETS

    _api = KaggleApi()
    _api.authenticate()

    state = load_state()
    data_completed = []
    all_dataframes = []

    for ds in datasets:
        _, zip_path, extract_to = get_dataset_paths(ds)
        up_to_date, remote_updated = is_up_to_date(ds, state, extract_to)

        if up_to_date:
            print(f"Skipping '{ds}' — no changes since last pull ({state.get(ds)})")
        else:
            download_and_extract(ds, zip_path, extract_to)
            state[ds] = remote_updated
            data_completed.append(ds)

        all_dataframes.extend(load_csvs_as_dataframes(extract_to))

    save_state(state)
    print(f"Datasets downloaded: {data_completed}")
    print("File extraction complete")

    return all_dataframes