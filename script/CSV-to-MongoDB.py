import os
import glob
import pandas as pd

import logging

from pymongo import MongoClient


CSV_PATH = "./output"
DB_NAME = "news"

IP = "0.0.0.0"
PORT = 27017

USERNAME = "devroot"
PASSWORD = "devroot"

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

    csv_paths = extract_csvs(CSV_PATH)
    logging.info("Storing {} files to MongoDB".format(len(csv_paths)))
    for csv_path in csv_paths:
        csv_rel_path = os.path.relpath(csv_path, CSV_PATH)
        csv_rel_path_norm = os.path.normpath(csv_rel_path)
        csv_source = csv_rel_path_norm.split(os.sep)[0]
        
        col = db[csv_source]

        df = pd.read_csv(csv_path)
        logging.info("-- Storing {} files to {}".format(len(df), csv_source))
        for _, row in df.iterrows():
            data = dict(row)
            data_op = {'$set': data}
            col.update_one(data, data_op, upsert=True)
            

if __name__ == '__main__':
    main()