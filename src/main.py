"""
A script to run the finger and knuckle print minutiae extraction and matching. The path containing the finger print and
the knuckle print to be processed and matched with the data available in the database is inputed as arguments to the
`run` function. Also a boolean value that indicates if the database should be updated if a match is not found can also
be inputed, and the default value is `True`.
"""

import base64
import glob
import os

import numpy as np

from calculate_fusion_score import compare_fingerprints
from database_connection import ConnectToDb
from logger import log
from minutiae_feature_extraction import FingerPrintMinutiae


def check_db_match(finger_print_path: str, knuckle_print_path: str) -> (bool, np.ndarray, np.ndarray):
    """
    Run finger and knuckle print match with connection to MongoDB.
    
    :param finger_print_path: Path to finger print data to be processed.
    :param knuckl_print_path: Path to knuckle print data to be processed.
    :return: True if a match is found or False if no match is found, with finger and knuckle print numpy array.
    """
    connection = ConnectToDb()
    database_data = connection.get_collection_data()

    finger_print = glob.glob(os.path.join(finger_print_path, "*.BMP"))
    knuckle_print = glob.glob(os.path.join(knuckle_print_path, "*.BMP"))

    log.info("Processing data and extracting minutiae ...")
    process_finger = FingerPrintMinutiae(finger_print[0])
    process_knuckle = FingerPrintMinutiae(knuckle_print[0])
    finger_input = process_finger.process_data()
    knuckle_input = process_knuckle.process_data()

    for _, row in database_data.iterrows():
        decode_finger = np.frombuffer(base64.b64decode(row["finger"]), dtype=np.uint8).reshape(finger_input.shape)
        decode_knuckle = np.frombuffer(base64.b64decode(row["knuckle"]),
                                       dtype=np.uint8).reshape(knuckle_input.shape)
        finger_fusion_score = compare_fingerprints(finger_input, decode_finger)
        knuckle_fusion_score = compare_fingerprints(knuckle_input, decode_knuckle)
        
        if finger_fusion_score >= 0.9 and knuckle_fusion_score >= 0.9:
            log.info(f"Match found!!!\n"
                    f"\t\t\t      Finger score: {round(finger_fusion_score, 5)}\n"
                    f"\t\t\t      Knuckle score: {round(knuckle_fusion_score, 5)}\n"
                    f"\t\t\t      Average score: {round((finger_fusion_score + knuckle_fusion_score) / 2, 5)}")
            return True, finger_input, knuckle_input

    if finger_fusion_score < 0.9 or knuckle_fusion_score < 0.9:
        log.info("No match found in the database.")
        return False, finger_input, knuckle_input
    connection.close()

def run(finger_print_path: str, knuckle_print_path: str, update_db: bool = True) -> None:
    """Run"""
    match, finger, knuckle = check_db_match(finger_print_path, knuckle_print_path)
    if not match and update_db:
        connection = ConnectToDb()
        connection.upload_data(finger, knuckle)
        connection.close()


if __name__ == "__main__":
    finger_print_pass = r"../data/test_data/pass/finger"
    knuckle_print_pass = r"../data/test_data/pass/knuckle"

    finger_print_fail = r"../data/test_data/fail/finger"
    knuckle_print_fail = r"../data/test_data/fail/knuckle"
    
    run(finger_print_fail, knuckle_print_fail, False)
