import cv2

cap = cv2.VideoCapture("cal4_CAM1.avi")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    ts = cap.get(cv2.CAP_PROP_POS_MSEC)
    print(ts)
