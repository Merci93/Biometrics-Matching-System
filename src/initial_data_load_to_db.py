"""
Initial data uploade to mongodb collection.
Process finger and knuckle prints and upload to MongoDB collection to create a reference data for comparison.
"""

import glob
import os

from database_connection import ConnectToDb
from logger import log
from minutiae_feature_extraction import FingerPrintMinutiae


finger_print_path = r"../data/raw/real/"
knuckle_print_path = r"../data/raw/knuckles/"

finger_prints = glob.glob(os.path.join(finger_print_path, "*.BMP"))
knuckle_prints = glob.glob(os.path.join(knuckle_print_path, "*.BMP"))

connection = ConnectToDb()

log.info("Processing data and extracting minutiae ...")
for i in range(len(knuckle_prints)):
    process_finger = FingerPrintMinutiae(finger_prints[i])
    process_knuckle = FingerPrintMinutiae(knuckle_prints[i])
    finger_input = process_finger.process_data()
    knuckle_input = process_knuckle.process_data()
    connection.upload_data(finger_input, knuckle_input)
connection.close()
