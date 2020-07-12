import os
import glob
import pandas as pd

import schedule
import time

from pymongo import MongoClient


CSV_PATH = "/pipelines"
DB_NAME = os.environ['MONGO_DATABASE_NAME']

IP = "0.0.0.0"
PORT = 27017

USERNAME = os.environ['MONGO_ROOT_USER']
PASSWORD = os.environ['MONGO_ROOT_PASSWORD']

def get_all_csv_paths(path):
    csv_paths = []
    for root, dirs, files in os.walk(CSV_PATH):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(root, file))
    return csv_paths

def main():
    client = MongoClient(IP, PORT, username = USERNAME, password = PASSWORD)
    db = client[DB_NAME]

    csv_paths = get_all_csv_paths(CSV_PATH)
    print("Storing {} files to MongoDB".format(len(csv_paths)))
    for csv_path in csv_paths:
        csv_rel_path = os.path.relpath(csv_path, CSV_PATH)
        csv_rel_path_norm = os.path.normpath(csv_rel_path)
        csv_source = csv_rel_path_norm.split(os.sep)[0]
        
        col = db[csv_source]

        df = pd.read_csv(csv_path)
        print("--Storing {} files to {}".format(len(df), csv_source))
        for _, row in df.iterrows():
            data = dict(row)
            data_op = {'$set': data}
            col.update_one(data, data_op, upsert=True)
            

if __name__ == '__main__':
    print("Start reading CSV files to MongoDB")
    schedule.every().day.at("00:00").do(main)
    while 1:
        schedule.run_pending()
        time.sleep(30)