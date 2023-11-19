import glob
import os

import cv2

from calculate_fusion_score import compare_fingerprints
from logger import log
from minutiae_feature_extraction import FingerPrintMinutiae

log.info("Starting print processing ...")
finger_print_path = r"../data/raw/real/"
knuckle_print_path = r"../data/raw/knuckles/"
finger_save_path = r"../data/extracted_minutiae/fingers"
knuckle_save_path = r"../data/extracted_minutiae/knuckle"

os.makedirs(finger_save_path, exist_ok=True)
os.makedirs(knuckle_save_path, exist_ok=True)

log.info("Loading finger and knuckle print data ...")
finger_prints = glob.glob(os.path.join(finger_print_path, "*.BMP"))
knuckle_prints = glob.glob(os.path.join(knuckle_print_path, "*.BMP"))

log.info("Processing data and extracting minutiae ...")
for i in range(len(knuckle_prints)):
    process_finger = FingerPrintMinutiae(finger_prints[i], finger_save_path)
    process_knuckle = FingerPrintMinutiae(knuckle_prints[i], knuckle_save_path)
    process_finger.process_data()
    process_knuckle.process_data()

log.info("Calculating fusion score ...")
finger_minutiae = [file for file in glob.glob(os.path.join(finger_save_path, "*.BMP")) if file.endswith("BMP")]
knuckle_minutiae = [file for file in glob.glob(os.path.join(knuckle_save_path, "*.BMP")) if file.endswith("BMP")]

fingerprint1_image = cv2.imread(finger_minutiae[2], cv2.IMREAD_GRAYSCALE)
fingerprint2_image = cv2.imread(finger_minutiae[3], cv2.IMREAD_GRAYSCALE)
finger_fusion_score = compare_fingerprints(fingerprint1_image, fingerprint2_image)

knuckle_print1_image = cv2.imread(knuckle_minutiae[2], cv2.IMREAD_GRAYSCALE)
knuckle_print2_image = cv2.imread(knuckle_minutiae[2], cv2.IMREAD_GRAYSCALE)
knuckle_fusion_score = compare_fingerprints(knuckle_print1_image, knuckle_print2_image)
log.info(f"Finger Print Fusion Score: {round(finger_fusion_score, 3)}")
log.info(f"Knuckle Print Fusion Score: {round(knuckle_fusion_score, 3)}")
