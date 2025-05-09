import cv2
url = 'http:172.20.10.14:81/stream'
cap = cv2. VideoCapture(filename=url)
while True:
# Capture frame-by-frame
  ret, frame = cap.read ()
  if not ret:
    print("Failed to grab frame")
    break

# DispLay the resulting frame
  cv2. imshow (winname=' ESP32-CAM', mat=frame)
# Break the Loop when 'q' key is pressed
  if cv2.waitKey(delay=1) & 0xFF == ord ('q'):
    break
# Release the capture and close OpenCV
cap.release ()
cv2.destroyAllWindows()