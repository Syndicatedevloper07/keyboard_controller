import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
sleep_duration = float(input("Enter sleep duration (in seconds): "))
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            index_tip = landmarks[8]  
            middle_tip = landmarks[12]  
            thumb_tip = landmarks[4]
            pinky_tip = landmarks[20]
            ring_tip = landmarks[16]
             
            
            index_x = int(index_tip.x * frame_width)
            index_y = int(index_tip.y * frame_height)
            
            middle_x = int(middle_tip.x * frame_width)
            middle_y = int(middle_tip.y * frame_height)
            
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            
            pinky_x = int(pinky_tip.x * frame_width)
            pinky_y = int(pinky_tip.y * frame_height)
            
            ring_x = int(ring_tip.x * frame_width)
            ring_y = int(ring_tip.y * frame_height)

            cv2.circle(img=frame, center=(index_x, index_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(middle_x, middle_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(thumb_x, thumb_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(pinky_x, pinky_y), radius=10, color=(0, 255, 255))
            cv2.circle(img=frame, center=(ring_x, ring_y), radius=10, color=(0, 255, 255))
            
            # Check for index and middle fingers shown together for 'up arrow' gesture
            if index_y < frame_height * 0.5 and middle_y < frame_height * 0.5 and abs(index_x - middle_x) < frame_width * 0.15:
            # if index_y < frame_height * 0.5 and middle_y < frame_height * 0.5:
            #     if abs(index_x - middle_x) < frame_width * 0.15:
                    pyautogui.keyDown('up')
                    time.sleep(0.5)
                    pyautogui.keyUp('up')
                
            if pinky_y < index_y and pinky_y < middle_y:
                pyautogui.keyDown('down')
                time.sleep(0.5)     
                pyautogui.keyUp('down')
          
            if index_y < middle_y:
                pyautogui.keyDown('left')  
                time.sleep(0.5)  
                pyautogui.keyUp('left')  
                
            if all(finger_y < frame_height * 0.7 for finger_y in [index_y, middle_y, ring_y]):
                print("thumb detected") 
                pyautogui.keyDown('right')  
                time.sleep(0.5)  
                pyautogui.keyUp('right')  
                
    cv2.imshow('Virtual Controller', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
