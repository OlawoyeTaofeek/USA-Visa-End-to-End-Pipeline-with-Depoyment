import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
from typing import Union, Dict
import yaml
from box import ConfigBox
from typing import Dict
from pathlib import Path
import sys
from usa_visa.exception import USVisaException

# Load environment variables
load_dotenv()
import yaml
from box import ConfigBox
from typing import Dict
import sys

# Assuming you already have USVisaException class imported

def load_yaml(file_path: str) -> Dict:
    """
    Load YAML file and return as a ConfigBox (attribute-style access).
    """
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        logging.info(f"yaml file {file_path} loaded successfully")
        return ConfigBox(data)
    except Exception as e:
        raise USVisaException(e, sys) from e # type: ignore
        
class MongoDbConnection:
    """A class allowing data push into MongoDB, and data pull from MongoDB"""
    
    def __init__(self, uri: Union[str, None]= os.getenv("MONGODB_URI")) -> None:  
        self.uri = uri
        self.csv_path = r"C:\Users\user\Documents\mlops_with_aws\Data\Visadataset.csv"
        if not self.uri:
            raise ValueError("The MongoDB URI is missing")
        else:
            self.client = MongoClient(self.uri)
            self.db = self.client['usa_visa_db']
            self.collection = self.db['usa_visa']

    def df_to_mongo(self):
        """Insert CSV data into MongoDB"""
        try:
            df = pd.read_csv(self.csv_path)
            if df.empty:
                logging.info("The generated DataFrame is empty")
                return
            data = df.to_dict(orient="records")
            self.collection.create_index("case_id", unique=True)
            self.collection.insert_many(data)
            logging.info(f"Inserted {len(data)} records into MongoDB collection 'usa_visa'")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {e}")

    def count_documents(self, query=None):
        """Count documents in the usa_visa collection"""
        try:
            if query is None:
                query = {}
            count = self.collection.count_documents(query)
            logging.info(f"Total documents in collection: {count}")
            return count
        except Exception as e:
            logging.error(f"Error counting documents: {e}")
            return 0

    def mongo_to_df(self, query=None):
        """Retrieve data from MongoDB into pandas DataFrame"""
        try:
            if query is None:
                query = {}
            cursor = self.collection.find(query)
            df = pd.DataFrame(list(cursor)).drop(columns=["_id"])
            logging.info(f"Retrieved {len(df)} records from MongoDB")
            return df
        except Exception as e:
            logging.error(f"Error retrieving data from MongoDB: {e}")
            return pd.DataFrame()

    def close_connection(self):
        """Close MongoDB client connection"""
        self.client.close()
        logging.info("MongoDB connection closed")
