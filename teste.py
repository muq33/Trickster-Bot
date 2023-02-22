import cv2
import numpy as np
import pyautogui

# Create a flag to indicate whether the window has been created
window_created = False

while True:
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a numpy array
    frame = np.array(screenshot)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Wait for 1 millisecond to allow OpenCV to properly render the window
    cv2.waitKey(1)

    # Compute the absolute difference between the current frame and the previous frame
    if 'last_frame' not in globals():
        last_frame = gray
    diff = cv2.absdiff(last_frame, gray)
    last_frame = gray

    # Apply a threshold to the difference image to extract the moving regions
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]

    # Perform some morphological operations to remove noise and fill in gaps
    kernel = np.ones((5,5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find contours of the moving regions
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw rectangles around the moving regions
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # If the window has not been created, create it and set the flag
    if not window_created:
        cv2.namedWindow('frame')
        window_created = True

    # Display the original frame with the rectangles around the moving regions
    cv2.imshow('frame', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all windows
cv2.destroyAllWindows()
