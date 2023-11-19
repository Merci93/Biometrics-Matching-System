"""Create a connection to Mongodb database to store or retrieve data."""

import base64

import pandas
import pymongo

from logger import log


class ConnectToDb:
    """A class to create a connection to the database."""

    def __init__(self) -> None:
        """Connect to the database collection."""
        mongo_db_uri = "mongodb://localhost:27017"
        self.client = pymongo.MongoClient(mongo_db_uri)
        self.db = self.client["finger_knuckle_prints"]
        self.available_collections = [collection["name"] for collection in self.db.list_collections()]
        if self.client.server_info()["ok"]:
            log.info("Successfully connected to MongoDB database.")
            log.info(f"Available collections: {self.available_collections}")
        else:
            log.debug("Unable to connect to the database.")

    def close(self) -> None:
        """Close database connection."""
        self.client.close()
        log.info("Database connection closed.")

    def get_collections(self, collection: str = "minutiae") -> pandas.DataFrame:
        """
        Fetch data from the database collection.
        
        :param collection: Database collection name.
        :return: A pandas data frame containing extracted data from the collection."""
        assert collection in self.available_collections, "The collection does not exist in the database."
        log.info(f"Getting Minutiae features from {collection}.")
        cursor = self.db[collection].find()
        data = list(cursor)
        return pandas.DataFrame(data)
    
    def upload_data(self, finger_data_path, knuckle_data_path, collection: str = "minutiae") -> None:
        """
        Upload finger and knuckle print data to mongodb.
        
        :param finger_data_path: Path to the finger_print_minutiae.
        :param knuckle_data_path: Path to the knuckle_print_minutiae.
        """
        assert collection in self.available_collections, "The collection does not exist in the database."
        available_data = collection.count_documents({})
        log.info("Uploading finger and knuckle data to database ...")
        with open(finger_data_path, "rb") as finger_data:
            finger_binary = base64.b64encode(finger_data.read())
        with open(knuckle_data_path, "rb") as knuckle_data:
            knuckle_binary = base64.b64encode(knuckle_data.read())
        data = {"finger": finger_binary, "knuckle": knuckle_binary}
        collection.insert_one(data)
        new_data_count = collection.count_documents({})
        log.info(f"{new_data_count - available_data} added to the {collection} collection.")
