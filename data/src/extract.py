import pandas as pd
from pathlib import Path
import zipfile, os, glob
import subprocess

def extract_data(file_path:str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found : {file_path}")
    
    print(f"Extracting Data from {file_path}")
    data = pd.read_csv(path)
    
    print(f"Dataset size: {len(data)}")

    return data

def kaggle_extract_data():

    datasets =['tanishqdublish/vehcile-fuel-consumption',
               'msjahid/colorado-motor-vehicle-sales-data',
               'ricardobj/electric-vehicle-population',
                'willianoliveiragibin/electric-vehicle-population',
                'syedanwarafridi/vehicle-sales-data',
                "sahirmaharajj/fuel-economy",
                "kanchana1990/vehicle-dataset-2024"]

    for ds in datasets:
        subprocess.run([
            r"C:\Users\josec\AppData\Roaming\Python\Python313\Scripts\kaggle.exe",
            "datasets", "download",
            "-d", ds,
            "-p", "data/",
            "--force"
            
        ])
    new_data=unzip_all()
    return new_data
    

def unzip_all(output_dir = "data"):
    for zip in glob.glob(os.path.join(output_dir,"*zip")):
        with zipfile.ZipFile(zip, 'r') as z:
            z.extractall(output_dir)

    print("Done.\n")
    print("Loading CSV: ")
    new_df = []
    

    for file in glob.glob(os.path.join(output_dir,"*.csv")):
        df = pd.read_csv(file)
        new_df.append(df)

    print("Complete")

    return new_df

