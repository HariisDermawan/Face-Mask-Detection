import cv2
import time

faceCascade = cv2.CascadeClassifier("asset/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("asset/Nariz.xml")
 
video_capture = cv2.VideoCapture(0)
mask_on = False

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wajah = faceCascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in wajah:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        
        hidung = noseCascade.detectMultiScale(roi_gray, 1.18, 35)
        for (sx, sy, sw, sh) in hidung:
            cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)
            cv2.putText(frame, 'Hidung', (x + sx, y + sy), 1, 1, (0, 255, 0), 1)

        mask_on = len(hidung) == 0 

        if mask_on:
            cv2.rectangle(frame, (x, y - 50), (x + w, y), (0, 255, 0), -1)
            text = 'Mask On'
        else:
            cv2.rectangle(frame, (x, y - 50), (x + w, y), (0, 0, 255), -1)
            text = 'Mask Off'

        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)[0]
        f = x + (w - size[0]) // 2
        c = y - 15
        cv2.putText(frame, text, (f, c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) if mask_on else (0, 0, 255), 3)

    current_time = time.strftime("%H:%M:%S", time.localtime())
    size = cv2.getTextSize(current_time, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    cv2.rectangle(frame, (20, 10), (20 + size[0] + 20, 40 + size[1]), (0, 0, 0), -1)
    cv2.putText(frame, current_time, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Camera ', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
