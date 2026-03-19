# SIC-25-26-TeamHES
# Handwritten Equation Solver (Real-Time)

A real-time AI-powered application that detects and solves mathematical equations using a camera feed. Built with **YOLO (Ultralytics)** for symbol detection, **SymPy** for solving equations, and **PyQt5** for a modern GUI.

---

## Features

* Real-time camera feed
* Detects handwritten/printed mathematical symbols
* Solves equations instantly
* Uses AI (YOLO) for symbol recognition
* Clean and modern PyQt5 GUI
* Capture-based solving (instance-wise, no continuous flickering)

---

## Tech Stack

* Python
* PyQt5 (GUI)
* OpenCV (Camera handling)
* YOLO (Ultralytics) – Object Detection
* SymPy – Equation solving

---

## Project Structure

```
AI-Equation-Solver/
│
├── gui.py              # GUI application
├── detect.py           # YOLO-based symbol detection
├── solver.py           # Equation solving logic
├── main.py             # Entry point
├── models/
│   └── weights/        # YOLO model 
├── README.md
├── .gitignore
```

---

Installation

1. Clone the repository

```
git clone https://github.com/your-username/AI-Equation-Solver.git
cd AI-Equation-Solver
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

Or manually:

```
pip install ultralytics opencv-python pyqt5 sympy
```

---

## How to Run

```
python main.py
```

---

## How It Works

1. Camera captures live video.
2. YOLO model detects individual symbols (digits/operators).
3. Symbols are sorted left-to-right to form an equation.
4. SymPy processes and solves the equation.
5. Result is displayed in the GUI.

---

 Usage

1. Click **▶ Start** to enable camera
2. Show equation in front of camera
3. Click **📸 Capture** to solve
4. Result appears instantly

---

## Notes

* Model file (`best.pt`) is not included due to size.
* Place your trained model inside:

  ```
  models/weights/best.pt
  ```
* Detection works best when symbols are **clearly visible and moderately sized**.

---

## Future Improvements

* Improve detection accuracy with better dataset
* Add OCR-based fallback for small text
* Step-by-step solution display
* Mobile / web version

---

##  Contributing

Feel free to fork this repo and improve it!

---


## Author

Developed by 
Pranshu Tripathi
Uday Katoch
Shivam Kumar
Sangam Yadav
Rohan Jangra

