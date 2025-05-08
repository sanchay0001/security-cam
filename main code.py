import cv2
import pygame
import time

# Initialize pygame mixer
pygame.mixer.init()
alert_sound = pygame.mixer.Sound('alert.wav')  # Load sound once

# Initialize webcam
cam = cv2.VideoCapture(0)

# Read first frame
ret, frame1 = cam.read()
last_alert_time = 0

while cam.isOpened():
    ret, frame2 = cam.read()
    if not ret:
        break

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # Corrected BGR
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Play sound if enough time has passed (avoid overlap)
        if time.time() - last_alert_time > 1:
            alert_sound.play()
            last_alert_time = time.time()

    cv2.imshow('Security CAM', frame1)

    frame1 = frame2  # update frame1 for next loop

    if cv2.waitKey(10) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
