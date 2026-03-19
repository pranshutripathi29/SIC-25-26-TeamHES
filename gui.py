# gui.py
from detect import detect_equation
from solver import solve_equation
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
from collections import deque

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Equation Solver")
        self.setGeometry(100, 100, 1200, 750)

        self.setStyleSheet(self.dark_theme())

        # ===== MAIN LAYOUT =====
        main_layout = QHBoxLayout()

        # ===== LEFT PANEL (Camera) =====
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("border-radius:15px; background:#111;")
        self.camera_label.setMinimumSize(800, 600)

        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.camera_label.setGraphicsEffect(shadow)

        # ===== RIGHT PANEL =====
        right_panel = QVBoxLayout()

        # Title
        title = QLabel("AI Equation Solver")
        title.setObjectName("title")

        # Equation Card
        self.eq_card = QLabel("Equation: ")
        self.eq_card.setObjectName("card")

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("separator")

        # Result Card
        self.res_card = QLabel("Result: ")
        self.res_card.setObjectName("card")

        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start")
        self.stop_btn = QPushButton("■ Stop")
        self.capture_btn = QPushButton("📸 Capture")

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.capture_btn)

        # Add widgets to right panel
        right_panel.addWidget(title)
        right_panel.addSpacing(20)
        right_panel.addWidget(self.eq_card)
        right_panel.addWidget(separator)
        right_panel.addWidget(self.res_card)
        right_panel.addSpacing(20)
        right_panel.addLayout(btn_layout)
        right_panel.addStretch()

        # Add panels
        main_layout.addWidget(self.camera_label)
        main_layout.addLayout(right_panel)

        self.setLayout(main_layout)

        # ===== CAMERA =====
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Stability buffer
        self.history = deque(maxlen=10)

        # Buttons
        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn.clicked.connect(self.stop_camera)
        self.capture_btn.clicked.connect(self.capture)

        # Last solved equation for instance-wise solving
        self.last_equation = None
        self.last_result = ""
        self.last_steps = []

    # ===== DARK THEME =====
    def dark_theme(self):
        return """
        QWidget {
            background-color: #0f1115;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }

        QLabel#title {
            font-size: 28px;
            font-weight: bold;
            color: #1f6feb;
        }

        QLabel#card {
            background-color: #161b22;
            border-radius: 20px;
            padding: 20px;
            font-size: 20px;
            min-height: 80px;
            border: 1px solid #222831;
            qproperty-alignment: 'AlignCenter';
        }

        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1f6feb, stop:1 #1158c7);
            color: white;
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #388bfd, stop:1 #1a4db7);
        }

        QFrame#separator {
            background-color: #222831;
            max-height: 2px;
        }

        QHBoxLayout, QVBoxLayout {
            spacing: 15px;
        }
        """

    # ===== CAMERA CONTROL =====
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()

    # ===== INSTANCE-WISE CAPTURE & SOLVE =====
    def capture(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite("capture.jpg", frame)  # optional save

                # Detect equation
                equation, symbols = detect_equation(frame)

                # Solve only if new equation
                if self.last_equation != equation:
                    result, steps = solve_equation(equation)
                    self.last_equation = equation
                    self.last_result = result
                    self.last_steps = steps
                else:
                    result = self.last_result
                    steps = self.last_steps

                # Draw bounding boxes
                for _, label, (x1, y1, x2, y2) in symbols:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Update UI
                self.eq_card.setText(f"Equation: {equation}")
                self.res_card.setText(f"Result: {result}")

                # Update camera feed
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.camera_label.setPixmap(QPixmap.fromImage(qt_image))

    # ===== FRAME UPDATE (Camera Preview Only) =====
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Optional: Draw symbol boxes only (no solving)
        equation, symbols = detect_equation(frame)
        for _, label, (x1, y1, x2, y2) in symbols:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image))

    # ===== SAFE CAMERA RELEASE ON EXIT =====
    def closeEvent(self, event):
        self.stop_camera()
        event.accept()