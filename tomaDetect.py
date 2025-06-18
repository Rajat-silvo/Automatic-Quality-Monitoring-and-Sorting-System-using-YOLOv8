## most frequent class considered
from ultralytics import YOLO
import cv2
import numpy as np
from collections import Counter

# Load the YOLO model
model_path = 'results/Iteration/weights/best.pt'
my_model = YOLO(model_path)

threshold = 0.7  # Confidence threshold

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    frame = cv2.resize(frame, (640, 480))
    
    # Run inference on the frame
    results = my_model.predict(frame)
    
    # Extract detection results
    boxes = results[0].boxes  # Bounding boxes
    confidences = boxes.conf  # Confidence scores
    class_ids = boxes.cls.cpu().numpy()  # Class IDs

    # Filter out low-confidence detections
    high_conf_indices = confidences >= threshold
    boxes = boxes[high_conf_indices]
    class_ids = class_ids[high_conf_indices.cpu().numpy()]

    # Determine the most frequent class
    if len(class_ids) > 0:
        class_counts = Counter(class_ids)
        most_frequent_class = max(class_counts, key=class_counts.get)
        most_frequent_count = class_counts[most_frequent_class]
        
        # # Display the most frequent class
        # cv2.putText(frame, f"Most Frequent Class: {most_frequent_class} ({most_frequent_count} times)",
        #             (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Annotate the frame
    annotated_frame = results[0].plot(boxes=boxes)

    # Display the annotated frame
    cv2.imshow("YOLO Detection", annotated_frame)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
