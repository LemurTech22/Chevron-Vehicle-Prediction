import pandas as pd
from pathlib import Path

def extract_data(file_path:str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found : {file_path}")
    
    print(f"Extracting Data from {file_path}")
    data = pd.read_csv(path)
    
    print(f"Dataset size: {len(data)}")

    return data
