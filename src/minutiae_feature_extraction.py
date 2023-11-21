"""A Module to extract finger and knuckle print features."""

import math
import os

import cv2
import numpy as np
import imageio
from skimage.morphology import convex_hull_image, erosion
from skimage.morphology import square
import skimage


class MinutiaeFeature(object):
    """Minutiae Feature."""
    def __init__(self, loc_x, loc_y, orientation, type_) -> None:
        """Minutiae Feature."""
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.orientation = orientation
        self.type_ = type_


class FingerPrintMinutiae():
    "Extract finger and knuckle print features."

    def __init__(self, image_path: str, save_path: str = None):
        "Extract and process finger and knuckle print minutiae."
        self.save_path = save_path
        self.image_path = image_path
        self.base_name = os.path.basename(image_path)
        self.threshold = imageio.v3.imread(image_path).mean()

    def get_termination_bifurcation(self, img: np.ndarray, mask: np.ndarray):
        """get termination bifurcation."""
        img = img == 255
        rows, cols = img.shape
        minutiae_term = np.zeros(img.shape)
        minutiae_bif = np.zeros(img.shape)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if img[i][j] == 1:
                    block = img[i - 1:i + 2, j - 1:j + 2]
                    block_val = np.sum(block)
                    if block_val == 2:
                        minutiae_term[i, j] = 1
                    elif block_val == 4:
                        minutiae_bif[i, j] = 1

        mask = convex_hull_image(mask > 0)
        mask = erosion(mask, square(5))
        minutiae_term = np.uint8(mask) * minutiae_term
        return minutiae_term, minutiae_bif

    def compute_angle(self, block: np.ndarray, minutiae_type: str):
        """Compute angle"""
        angle = 0
        blk_rows, blk_cols = np.shape(block)
        center_x, center_y = (blk_rows - 1) / 2, (blk_cols - 1) / 2
        if minutiae_type.lower() == "termination":
            sum_val = 0
            for i in range(blk_rows):
                for j in range(blk_cols):
                    if (i == 0 or i == blk_rows - 1 or j == 0 or j == blk_cols - 1) and block[i][j] != 0:
                        angle = -math.degrees(math.atan2(i - center_y, j - center_x))
                        sum_val += 1
                        if sum_val > 1:
                            angle = float("nan")
                return angle
        elif minutiae_type.lower() == "bifurcation":
            blk_rows, blk_cols = np.shape(block)
            center_x, center_y = (blk_rows - 1) / 2, (blk_cols - 1) / 2
            angle = []
            sum_val = 0
            for i in range(blk_rows):
                for j in range(blk_cols):
                    if (i == 0 or i == blk_rows - 1 or j == 0 or j == blk_cols - 1) and block[i][j] != 0:
                        angle.append(-math.degrees(math.atan2(i - center_y, j - center_x)))
                        sum_val += 1
            if sum_val != 3:
                angle = float("nan")
                return angle

    def extract_minutiae_features(self, skel: np.ndarray, minutiae_term: np.ndarray, minutiae_bif: np.ndarray) -> list:
        """Extract minutiae features from provided finger or knuckle print image."""
        minutiae_term = skimage.measure.label(minutiae_term, connectivity=2)
        rp = skimage.measure.regionprops(minutiae_term)
        window_size = 2
        features_term = []
        for i in rp:
            row, col = np.int16(np.round(i["Centroid"]))
            block = skel[row - window_size:row + window_size + 1, col - window_size:col + window_size + 1]
            angle = self.compute_angle(block, "Termination")
            features_term.append(MinutiaeFeature(row, col, angle, "Termination"))

        features_bif = []
        minutiae_bif = skimage.measure.label(minutiae_bif, connectivity=2)
        rp = skimage.measure.regionprops(minutiae_bif)
        window_size = 1
        for i in rp:
            row, col = np.int16(np.round(i["Centroid"]))
            block = skel[row - window_size:row + window_size + 1, col - window_size:col + window_size + 1]
            angle = self.compute_angle(block, "Bifurcation")
            features_bif.append(MinutiaeFeature(row, col, angle, "Bifurcation"))
        return features_term, features_bif

    def process_data(self, run_local: bool = False) -> None:
        """Perform finger/knuckle print image processing."""
        img = cv2.imread(self.image_path, 0)
        img = np.array(img > self.threshold).astype(int)
        skel = skimage.morphology.skeletonize(img)
        skel = np.uint8(skel) * 255
        mask = img * 255

        minutiae_term, minutiae_bif = self.get_termination_bifurcation(skel, mask)
        features_term, features_bif = self.extract_minutiae_features(skel, minutiae_term, minutiae_bif)
        skimage.measure.label(minutiae_bif, connectivity=1)
        skimage.measure.label(minutiae_term, connectivity=1)

        result_image = np.zeros((skel.shape[0], skel.shape[1], 3), dtype=np.uint8)
        result_image[:, :, 0] = skel
        result_image[:, :, 1] = skel
        result_image[:, :, 2] = skel
        
        desired_size = (800, 800)
        result_image = cv2.resize(result_image, desired_size)
        saved_data = os.listdir(self.save_path)
        
        if run_local == True:
            processed_files = [os.path.basename(file) for file in saved_data if file.endswith("BMP")]
            if self.base_name not in processed_files:
                cv2.imwrite(os.path.join(self.save_path, f"{self.base_name}"), result_image)
        else:
            return result_image
