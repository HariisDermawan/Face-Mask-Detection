import cv2
import serial
import time
from playsound import playsound

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

faceCascade = cv2.CascadeClassifier("asset/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("asset/Nariz.xml")

video_capture = cv2.VideoCapture(0)
mask_on_count = 0
mask_off_count = 0
total_faces_detected = 0

last_mask_status = None
mask_on_frames = 0
mask_off_frames = 0
frame_threshold = 10

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    wajah_detected = faceCascade.detectMultiScale(gray, 1.1, 5)
    total_faces_detected = len(wajah_detected)

    for (x, y, w, h) in wajah_detected:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        hidung = noseCascade.detectMultiScale(roi_gray, 1.18, 35)
        mask_on = len(hidung) == 0

        if mask_on:
            mask_on_frames += 1
            mask_off_frames = 0
        else:
            mask_off_frames += 1
            mask_on_frames = 0

        if mask_on_frames > frame_threshold and last_mask_status != '1':
            mask_on_count += 1
            arduino.write(b'1')
            playsound('masker_on.mp3')
            last_mask_status = '1'
        elif mask_off_frames > frame_threshold and last_mask_status != '2':
            mask_off_count += 1
            arduino.write(b'2')
            playsound('mask_off.mp3')
            last_mask_status = '2'

        text = 'Mask On' if mask_on else 'Mask Off'
        cv2.rectangle(frame, (x, y - 50), (x + w, y), (0, 255, 0)
                      if mask_on else (0, 0, 255), -1)
        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)[0]
        f = x + (w - size[0]) // 2
        c = y - 15
        cv2.putText(frame, text, (f, c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) 
                      if mask_on else (0, 0, 255), 3)

        for (sx, sy, sw, sh) in hidung:
            cv2.rectangle(roi_color, (sx, sy),(sx + sw, sy + sh), (255, 0, 0), 2)
            cv2.putText(frame, 'Hidung', (x + sx, y + sy), 1, 1, (0, 255, 0), 1)

    if total_faces_detected > 0:
        mask_on_accuracy = (mask_on_count / total_faces_detected) * 100
        mask_off_accuracy = (mask_off_count / total_faces_detected) * 100
    else:
        mask_on_accuracy = 0
        mask_off_accuracy = 0

    print(f'Mask On Accuracy: {mask_on_accuracy:.2f}% | Mask Off Accuracy: {mask_off_accuracy:.2f}%')

    current_time = time.strftime('%H:%M:%S')
    size = cv2.getTextSize(current_time, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    cv2.rectangle(frame, (20, 10), (20 + size[0] + 20, 40 + size[1]), (0, 0, 0), -1)
    cv2.putText(frame, current_time, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    watermark = '05TPLP013'
    watermark_size = cv2.getTextSize(watermark, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    frame_width = frame.shape[1]
    watermark_x = frame_width - watermark_size[0] - 30
    watermark_y = 40
    cv2.rectangle(frame, (watermark_x - 10, 10), (watermark_x + watermark_size[0] + 10, 40 + watermark_size[1]), (0, 0, 0), -1)
    cv2.putText(frame, watermark, (watermark_x, watermark_y),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
arduino.close()
