from vilib import Vilib
from ultralytics import YOLO
import cv2
import time

def main():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    print("Vilib camera started. Display enabled.")

    model = YOLO("yolov8n.pt")
    print("YOLO model loaded.")

    while True:
       
        frame = Vilib.get_frame()  
        if frame is None:
            time.sleep(0.1)
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = model(frame_rgb)
        annotated_frame = results[0].plot() 

        for result in results:
            for box in result.boxes:
                detected_class = box.cls[0]
                confidence = box.conf[0]
                print(f"Detected class: {detected_class} with confidence: {confidence:.2f}")

        cv2.imshow("Vilib + YOLO Object Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    Vilib.camera_close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
