import cv2
import os
import keyboard

#Asynchronously tarts live feed and captures when space bar is pressed and saves the image
#Input:file path and image name
#Output: None

def camera_feed(capture_event, image_folder, image_name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Camera feed is now live. Press SPACE to capture the image.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot capture frame from camera. Exiting...")
            break
        
        cv2.imshow('Live Cam', frame)
        
        if capture_event.is_set():
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            img_path = os.path.join(image_folder, image_name)
            cv2.imwrite(img_path, frame)
            print(f"Image captured and saved as {img_path}")
            capture_event.clear()
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()