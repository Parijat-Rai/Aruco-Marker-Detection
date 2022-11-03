import cv2 as cv
from cv2 import aruco
import numpy as np
import requests

marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

user_id_tag=-1

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        for ids, corners in zip(marker_IDs, marker_corners):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            cv.putText(
                frame,
                f"id: {ids[0]}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (200, 100, 0),
                2,
                cv.LINE_AA,
            )
            user_id_tag=ids[0]
            # print(ids, "  ", corners)
    cv.imshow("frame", frame)  
    
    cv.waitKey(10)

    if user_id_tag>=0:
        break
cap.release()
cv.destroyAllWindows()

# defining the api-endpoint
cart_api = "http://10.12.35.165:3000/cart"

# data to be sent to api
data = { "userTag" : int(user_id_tag) }
# print(data)
# sending post request and saving response as response object
r = requests.post(url = cart_api, json= data)

data = r.json()
# print(data)
