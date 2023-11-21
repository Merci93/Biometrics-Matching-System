"""Create a connection to Mongodb database to store or retrieve data."""

import base64

import numpy as np
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

    def get_collection_data(self, collection: str = "minutiae") -> pandas.DataFrame:
        """
        Fetch data from the database collection.

        :param collection: Database collection name.
        :return: A pandas data frame containing extracted data from the collection."""
        assert collection in self.available_collections, "The collection does not exist in the database."
        log.info(f"Getting Minutiae features from the collection {collection}.")
        cursor = self.db[collection].find()
        data = list(cursor)
        return pandas.DataFrame(data)
    
    def upload_data(self, finger_data: np.ndarray, knuckle_data: np.ndarray, collection: str = "minutiae") -> None:
        """
        Upload finger and knuckle print data to mongodb.

        :param finger_data: Finger print minutiae as a numpy n-dimensional array.
        :param knuckle_data: Knuckle print minutiae as a numpy n-dimensional array.
        """
        assert collection in self.available_collections, "The col lection does not exist in the database."
        available_data = self.db[collection].count_documents({})
        log.info("Uploading finger and knuckle data to database ...")
        finger_binary = base64.b64encode(finger_data)
        knuckle_binary = base64.b64encode(knuckle_data)
        data = {"finger": finger_binary, "knuckle": knuckle_binary}
        self.db[collection].insert_one(data)
        new_data_count = self.db[collection].count_documents({})
        log.info(f"{new_data_count - available_data} data added to the {collection} collection.")
