from pyspark.sql import SparkSession
from pathlib import Path
import zipfile, os, glob, subprocess, time

def extract_data(file_path:str):
    spark = SparkSession.builder \
        .appName("Data Extraction") \
        .getOrCreate()
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found : {file_path}")
    
    print(f"Extracting Data from {file_path}")
    data = spark.read.csv(str(path))

    print(f"Dataset size: {data.count()}")
    return data

def kaggle_extract_data():
    data_completed=[]
    datasets =['tanishqdublish/vehcile-fuel-consumption',
               'msjahid/colorado-motor-vehicle-sales-data',
               'ricardobj/electric-vehicle-population',
                'willianoliveiragibin/electric-vehicle-population',
                'syedanwarafridi/vehicle-sales-data',
                "sahirmaharajj/fuel-economy",
                "kanchana1990/vehicle-dataset-2024"]
    
    for ds in datasets:   
        print(f"Downloading : {ds}")
        subprocess.run([
            r"C:\Users\josec\AppData\Roaming\Python\Python313\Scripts\kaggle.exe",
            "datasets", "download",
            "-d", ds,
            "-p", "data/",
            "--force"  
        ])
        data_completed.append(ds)
    print(f"Datasets downloaded: {data_completed}")
    time.sleep(2)
    return unzip_all(output_dir = "data", extracted_datasets='extracted_data')
    
def unzip_all(output_dir, extracted_datasets):
    os.makedirs(extracted_datasets, exist_ok=True)
    new_df=[]
    print("Compressing files to zip.")
    
    for zip in glob.glob(os.path.join(output_dir,"*zip")):
        zip_name=os.path.basename(zip).replace(".zip","")
        extract_to = os.path.join(extracted_datasets, zip_name)
        os.makedirs(extract_to, exist_ok=True)

        print(f"Extracting {zip_name} to {extract_to}")

        with zipfile.ZipFile(zip, "r") as z:
            z.extractall(extract_to)

        for csv_file in glob.glob(os.path.join(extract_to, "*.csv")):
            df = extract_data(csv_file)
            new_df.append(df)

    print("File Compression Complete")
    return new_df
