import cv2
import math
import numpy as np
import serial
from collections import Counter
from ultralytics import YOLO

# Load the YOLO model
model_path = 'results/Iteration/weights/best.pt'
my_model = YOLO(model_path)

# Pixels to cm ratio (update accordingly)
ratio = 10 / 517.05    #replace 517.05 with the distance in pixels between 0-10 cm from the calibration step

# Initialize serial communication
ser = serial.Serial('COM5', 9600, timeout=1)  # Update with correct port and baud rate

while True:
    if ser.in_waiting > 0:  # Check if data is available
        print(ser.readline().decode().strip())  # Read & print data
        data = ser.readline().decode('utf-8').strip()  # Read and decode
        print("Received:", data)

        # If the IR sensor is triggered (IR1 == 0)
        if "x" in data:
            # Open webcam
            cap = cv2.VideoCapture(0)
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
                
                # Run YOLO inference on the frame
                results = my_model.predict(frame)
                boxes = results[0].boxes  # Bounding boxes
                confidences = boxes.conf.cpu().numpy()  # Confidence scores
                class_ids = boxes.cls.cpu().numpy()  # Class IDs
                class_names = results[0].names  # Class names
                # Print raw detections
                print("Raw Detections:")
                for i in range(len(class_ids)):
                    print(f"Class: {class_names[int(class_ids[i])]}, Confidence: {confidences[i]:.2f}")

                # Filter out low-confidence detections
                threshold = 0  # Confidence threshold
                high_conf_indices = confidences >= threshold
                boxes = boxes[high_conf_indices]
                class_ids = class_ids[high_conf_indices]
                confidences = confidences[high_conf_indices]
                
                most_frequent_class = None
                if len(class_ids) > 0:
                    class_counts = Counter(class_ids)
                    max_frequency = max(class_counts.values())
                    
                    # Get classes with max frequency (handle ties)
                    most_frequent_classes = [cls for cls, count in class_counts.items() if count == max_frequency]
                    
                    if len(most_frequent_classes) == 1:
                        most_frequent_class = most_frequent_classes[0]
                    else:
                        # If multiple classes have the same frequency, select the one with highest confidence
                        max_conf_idx = np.argmax([confidences[i] for i in range(len(class_ids)) if class_ids[i] in most_frequent_classes])
                        most_frequent_class = class_ids[max_conf_idx]
                    
                    most_frequent_class_name = class_names[int(most_frequent_class)]
                   
                # Process each detected object
                for i, box in enumerate(boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    width_px = x2 - x1
                    height_px = y2 - y1
                    width_cm = round(width_px * ratio, 2)
                    height_cm = round(height_px * ratio, 2)
                    class_name = class_names[int(class_ids[i])]
                    
                    # Classify by size
                    size_category = "Small" if width_cm < 4.8 or height_cm < 4.8 else "Medium" if width_cm < 6.5 and height_cm < 6.5 else "Large"
                    print("Size Category:", size_category)
                    

                ## Classes-   
                # - b_fully_ripened
                # - b_half_ripened
                # - b_green
                # - l_fully_ripened
                # - l_half_ripened
                # - l_green
                
                    if size_category == 'Small' and class_name in ['b_fully_ripened', 'b_half_ripened', 'b_green', 'l_half_ripened', 'l_fully_ripened', 'l_green']:
                        ser.write(b's')
                        print("Sent:", b's')
                        
                    elif class_name in ['b_green','l_green']:
                        ser.write(b'g')
                        print("Sent:", b'g') 

                    elif size_category in ['Medium', 'Large'] and class_name in ['b_fully_ripened', 'b_half_ripened', 'l_half_ripened', 'l_fully_ripened']:
                        ser.write(b'r')
                        print("Sent:", b'r')
                        

                    # # Draw bounding box and size info
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # cv2.putText(frame, f"{class_name}: {width_cm}cm x {height_cm}cm ({size_category})", (x1, y1 - 10),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)      
                # Display the frame
                #cv2.imshow("Tomato Detection with Size Measurement", frame)
                break
            print("Exiting loop")
            cap.release()
            cv2.destroyAllWindows()      
    
    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()