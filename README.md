# 🖐️ ComputerVision-HandGestureMouse

An advanced Python application that transforms your webcam into a powerful, gesture-controlled mouse. This project uses `OpenCV` for video capture and `MediaPipe` for real-time hand tracking to control your computer's cursor with natural hand movements.

---

## ✨ Core Features

- **Cursor Control:** Fluid, low-latency cursor movement that follows your index finger.
- **Clicking:** Supports both single and double-clicking.
- **Drag & Drop:** An intuitive gesture to grab, move, and release windows or files.
- **Proportional Scrolling:** Smooth, variable-speed scrolling controlled by finger distance.
- **Activation Mode:** Toggle the mouse on and off with an open-palm gesture to prevent accidental inputs.
- **Audio Feedback:** Instant beeps to confirm when the mouse is activated or deactivated.
- **High Performance:** Optimized for low CPU usage.

---

## 🛠️ Requirements & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AyaatMohammed/ComputerVision-HandGestureMouse.git
    cd ComputerVision-HandGestureMouse
    ```

2.  **Install dependencies:**
    ```bash
    pip install opencv-python mediapipe pyautogui
    ```

---

## 🚀 How to Use

1.  Navigate to the project directory in your terminal.
2.  Run the script:
    ```bash
    python ComputerVision-HandGestureMouse.py
    ```
3.  The camera window will appear. The mouse is **deactivated** by default.
4.  Use the gestures below to control your computer!
5.  To quit, press the **'q'** key while the camera window is active.

---

## 🤌 Gesture Guide

| Function            | Gesture                  | How to Perform                                                              |
| :------------------ | :----------------------- | :-------------------------------------------------------------------------- |
| **Activate/Deactivate** | 🖐️ (Open Palm )           | Show your open palm to the camera to toggle the mouse ON/OFF.               |
| **Move Cursor**     | ☝️ (Index Finger Up)     | Raise only your index finger. The cursor will follow its tip.               |
| **Click**           | 🤏 (Thumb + Index)       | Pinch your thumb and index finger together.                                 |
| **Drag & Drop**     | 🤏 (Thumb + Pinky)       | Pinch your thumb and pinky finger to "grab". Move your hand, then release.  |
| **Scrolling**       | ✌️ (Peace Sign)          | Make a peace sign. The distance between your fingers controls scroll speed. |
