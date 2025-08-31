# ---------------------------------
# AI Virtual Mouse
# ---------------------------------

# 1. Import libraries
import cv2
import mediapipe as mp
import pyautogui
import math
import time
import winsound  # For Windows beep sounds

# 2. Initial configurations
pyautogui.FAILSAFE = False  # Disable fail-safe
pyautogui.PAUSE = 0.0       # No delay between actions

# 3. Camera & Hand Tracking setup
cap = cv2.VideoCapture(0)   # Webcam
cap.set(3, 640)             # Frame width
cap.set(4, 480)             # Frame height

hand_detector = mp.solutions.hands.Hands(min_detection_confidence=0.8, max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

# 4. State & control variables
is_mouse_active = False
activation_released = True

is_dragging = False
click_released = True
last_click_time = 0
DOUBLE_CLICK_INTERVAL = 0.4
is_scrolling_mode = False

prev_x, prev_y = 0, 0
SMOOTHING_FACTOR = 0.25
CLICK_DEAD_ZONE = 45  # Pixels for click threshold

# 5. Helper function
def play_beep(freq=600, dur=150):
    """Play a beep (Windows only)."""
    try:
        winsound.Beep(freq, dur)
    except:
        pass

# 6. Main loop
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        hand = hands[0]
        drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        landmarks = hand.landmark

        # --- Finger state detection ---
        is_thumb_up = landmarks[4].y < landmarks[3].y
        is_index_up = landmarks[8].y < landmarks[6].y
        is_middle_up = landmarks[12].y < landmarks[10].y
        is_ring_up = landmarks[16].y < landmarks[14].y
        is_pinky_up = landmarks[20].y < landmarks[18].y

        # --- Mouse activation gesture ---
        is_all_fingers_up = is_thumb_up and is_index_up and is_middle_up and is_ring_up and is_pinky_up
        
        if is_all_fingers_up and activation_released:
            is_mouse_active = not is_mouse_active
            activation_released = False
            play_beep(800 if is_mouse_active else 400)
            time.sleep(0.5)
        
        if not is_all_fingers_up:
            activation_released = True

        # --- Mouse functions (active only) ---
        if is_mouse_active:
            cv2.putText(frame, "Mouse Activated", (frame_width - 300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Scrolling gesture: index+middle up
            if is_index_up and is_middle_up and not is_ring_up and not is_pinky_up:
                is_scrolling_mode = True
                vertical_distance = (landmarks[12].y - landmarks[8].y) * frame_height
                DEAD_ZONE = 15
                SCROLL_SENSITIVITY = 5
                scroll_amount = 0
                if vertical_distance > DEAD_ZONE:
                    scroll_amount = -int((vertical_distance - DEAD_ZONE) * SCROLL_SENSITIVITY)
                elif vertical_distance < -DEAD_ZONE:
                    scroll_amount = -int((vertical_distance + DEAD_ZONE) * SCROLL_SENSITIVITY)
                if scroll_amount != 0:
                    pyautogui.scroll(scroll_amount)
            else:
                is_scrolling_mode = False

            # Cursor movement, clicking, dragging
            if not is_scrolling_mode:
                index_x_raw = landmarks[8].x * screen_width
                index_y_raw = landmarks[8].y * screen_height
                current_x = prev_x + (index_x_raw - prev_x) * SMOOTHING_FACTOR
                current_y = prev_y + (index_y_raw - prev_y) * SMOOTHING_FACTOR
                
                thumb_x = int(landmarks[4].x * screen_width)
                thumb_y = int(landmarks[4].y * screen_height)
                pinky_x = int(landmarks[20].x * screen_width)
                pinky_y = int(landmarks[20].y * screen_height)

                click_distance = math.hypot(thumb_x - current_x, thumb_y - current_y)
                drag_distance = math.hypot(pinky_x - thumb_x, pinky_y - thumb_y)

                # Drag & Drop: thumb+pinkie pinch
                if drag_distance < 60:
                    if not is_dragging:
                        pyautogui.mouseDown(button='left')
                        is_dragging = True
                else:
                    if is_dragging:
                        pyautogui.mouseUp(button='left')
                        is_dragging = False
                
                # Move cursor
                if is_dragging:
                    pyautogui.moveTo(thumb_x, thumb_y)
                else:
                    pyautogui.moveTo(current_x, current_y)
                
                prev_x, prev_y = current_x, current_y

                # Click: thumb+index pinch
                if not is_dragging and click_distance < CLICK_DEAD_ZONE and click_released:
                    current_time = time.time()
                    if current_time - last_click_time < DOUBLE_CLICK_INTERVAL:
                        pyautogui.doubleClick()
                        last_click_time = 0
                    else:
                        pyautogui.click()
                        last_click_time = current_time
                    click_released = False
                elif click_distance >= CLICK_DEAD_ZONE:
                    click_released = True
        else:
            cv2.putText(frame, "Mouse Deactivated", (frame_width - 320, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            is_dragging = False
            click_released = True
            is_scrolling_mode = False
    else:
        # Reset states if no hand detected
        is_dragging = False
        click_released = True
        is_scrolling_mode = False

    cv2.imshow('AI Virtual Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.01)

# 7. Cleanup
cap.release()
cv2.destroyAllWindows()
