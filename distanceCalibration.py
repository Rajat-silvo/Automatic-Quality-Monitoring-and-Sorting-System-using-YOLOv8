## Go to line 43 and follow the two instructions to calibrate the distance in pixels to cm.

## Pixel to CM calibaration
import cv2
import math

points = []

#Pixels to cm ratio
ratio = 10/517.05

def draw_circle(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) == 2:
            points = []
        points.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    frame = cv2.resize(frame, (640, 480))

    for pt in points:
        cv2.circle(frame, pt, 5, (26, 15, 255), -1)

    #Measure the distance between the two points
    if len(points) == 2:
        pt1 = points[0]
        pt2 = points[1]
        distance_px = math.hypot((pt2[0] - pt1[0]), (pt2[1] - pt1[1]))

        #Convert distance to cm
        distance_cm = distance_px * ratio

        #Instruction 1- Put a scale in the frame and measure the pixels between 0-10 cm
        cv2.putText(frame, f"Distance: {distance_px:.2f} px", (pt1[0], pt1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        #Instruction 2- After getting the distance in pixels, divide it by 10 in the 'ratio' variable defined above to get the correct distance in cm
        cv2.putText(frame, f"Distance: {distance_cm:.2f} cm", (pt1[0], pt1[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break