import cv2 as cv
from cv2 import aruco
import numpy as np
import requests
import random

user_id_tag =  int(2) #random.randint(0,100)
product_id=int(1)
thres_dist = int(100)
counter=int(1)
calib_data_path = "./calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 8  # centimeters

marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)


while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Since there was mistake in calculating the distance approach point-outed in the Video Tutorial's comment
            # so I have rectified that mistake, I have test that out it increase the accuracy overall.
            # Calculating the distance
            distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)
            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )

            product_id=int(ids[0])


            

            while(ids[0]>-1):
                if (distance>thres_dist):
                            counter -= 1
                            print("Item Removed")
                            print(counter)
                            break
                         
                if (distance<thres_dist):
                        counter += 1
                        print("Item Added")
                        print(counter)
                        break

            
            # if ids[0] in list_id:
            #     if (dict_counter[ids[0]]==1):
            #         if (distance>thres_dist):
            #                 dict_counter[ids[0]] -= 1
            #                 print("Item Removed")
            #                 print(dict_counter)
            #                 break

            #     if (dict_counter[ids[0]]==0 ):             
            #         if (distance<thres_dist):
            #                 dict_counter[ids[0]] += 1
            #                 print("Item Added")
            #                 print(dict_counter)
            #                 break
            
    cv.imshow("frame", frame)
    
    cv.waitKey(10)
    
    # if key == ord("q"):
    if (counter==4):
        break

cap.release()
cv.destroyAllWindows()


# defining the api-endpoint
cart_api = "http://10.12.35.165:3000/addCart"

# data to be sent to api
data = { "userTag" : user_id_tag, "productTag" : product_id, "qty" : counter }
print(data)
# sending post request and saving response as response object
r = requests.post(url = cart_api, json= data)

data = r.json()
print(data)