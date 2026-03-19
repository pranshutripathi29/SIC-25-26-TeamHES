from ultralytics import YOLO

model = YOLO("models/weights/best.pt")

def detect_equation(frame, conf=0.5):
    results = model(frame, conf=conf)[0]
    symbols = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls = int(box.cls[0])
        confidence = float(box.conf[0])

        if confidence < conf:
            continue

        label = model.names[cls]
        x_center = (x1 + x2) // 2

        symbols.append((x_center, label, (x1,y1,x2,y2)))

    symbols = sorted(symbols, key=lambda x: x[0])
    equation = "".join([s[1] for s in symbols])

    return equation, symbols