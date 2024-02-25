import cv2
import os
import keyboard

# Define the function to handle the camera feed
def camera_feed(capture_event, image_folder, image_name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Camera feed is now live. Press SPACE to capture the image.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot capture frame from camera. Exiting...")
            break
        
        # Display the resulting frame
        cv2.imshow('Live Cam', frame)
        
        # Check if the space bar was pressed
        if capture_event.is_set():
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            img_path = os.path.join(image_folder, image_name)
            cv2.imwrite(img_path, frame)
            print(f"Image captured and saved as {img_path}")
            capture_event.clear()
            break
        
        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()