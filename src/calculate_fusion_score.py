"""Calculate the fusion score of two finger/knuckle prints."""

import cv2

def compare_fingerprints(data_1, data_2) -> float:
    """
    Calculate the fusion score match between the input finger/knuckle print and the data available in the database.

    :param data_1: Finger/knuckle print data
    :param data_2: Finger/knuckle print data
    :return: Float value indication the percentage match between the two finger/knuckle prints
    """
    orb = cv2.ORB_create()
    key_points1, descriptors1 = orb.detectAndCompute(data_1, None)
    key_points2, descriptors2 = orb.detectAndCompute(data_2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Threshold for matching
    threshold = 50
    matching_points = [m for m in matches if m.distance < threshold]
    similarity_score = len(matching_points) / len(key_points1)
    return similarity_score
