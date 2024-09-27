import cv2

video_capture =  cv2.VideoCapture(0)

while True :

    ret, frame = video_capture.read()

    cv2.imshow('Camera 01', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()