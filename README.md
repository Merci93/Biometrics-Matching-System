# Finger_and_Knuckle_Print_Matching
A finger and knuckle print matching algorithm. the algorithm uses both finger and knuckle prints to identify an individual. The finger and knuckle prints are passed through `minutiae_feature_extraction`. The minutiae feature of the input finger is compared with the available data in the MongoDB collection `minutiae` and the fussion score calculated. The score threshold is set at **90%** for both finger and knuckle prints to pass the detetction algorithm.

## Run instructions
Provide the path with the knuckle and finger prints to be matched as input arguments to the `run` function in the `main.py` script. In the `run` function, the argument **upload_db** is set to True by default and this uploads the finger and knuckle data to the database in a situ
