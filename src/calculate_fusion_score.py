import cv2

def compare_fingerprints(fingerprint_1, fingerprint_2) -> None:
    """
    Calculate the fusion score match between the input finger/knuckle print and the data available in the database.

    :param fingerprint_1: _description_
    :param fingerprint2: _description_
    :return: _description_
    """
    orb = cv2.ORB_create()
    key_points1, descriptors1 = orb.detectAndCompute(fingerprint_1, None)
    key_points2, descriptors2 = orb.detectAndCompute(fingerprint_2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)

    # Threshold for matching
    threshold = 50  # Adjust this value based on your requirements
    matching_points = [m for m in matches if m.distance < threshold]
    similarity_score = len(matching_points) / len(key_points1)
    return similarity_score