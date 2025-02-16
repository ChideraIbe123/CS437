from picarx import Picarx
from vilib import Vilib
import time

SPEED = 20

def init_vision():

    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=True, web=True)
    Vilib.face_detect_switch(True)
    print("Camera and face detection started.")

def face_detected():
    
    if Vilib.detect_obj_parameter.get('human_n', 0) > 0:
        human_x = Vilib.detect_obj_parameter.get('human_x', 0)
        human_y = Vilib.detect_obj_parameter.get('human_y', 0)
        human_w = Vilib.detect_obj_parameter.get('human_w', 0)
        human_h = Vilib.detect_obj_parameter.get('human_h', 0)
        print(f"Face detected! Coordinate: ({human_x}, {human_y}) Size: ({human_w}, {human_h})")
        return True
    return False

def main():
    car = Picarx()
    init_vision()
    time.sleep(10)

    try:
        print("Car is moving forward. Waiting for face detection...")
        while True:
            if face_detected():
                print("Face detected. Stopping car.")
                car.forward(0)  
                break
            else:
                car.forward(SPEED)
            time.sleep(0.1)  
    finally:
        car.forward(0)  
        print("Car motion halted.")

if __name__ == "__main__":
    main()
