from picarx import Picarx
import time

SPEED = 100
DANGER = 20
TURN_DISTANCE = 20

def run():
    try:
        car = Picarx()
        
        while True:
            dist = round(car.ultrasonic.read(), 2)
            
            if dist >= DANGER:
                car.set_dir_servo_angle(0)
                car.forward(SPEED)
            elif dist >= TURN_DISTANCE:
                car.set_dir_servo_angle(30)
                car.forward(SPEED)
                time.sleep(0.1)
            else:
                car.set_dir_servo_angle(-30)
                car.backward(SPEED)
                time.sleep(0.5)

    finally:
        car.forward(0)


if __name__ == "__main__":
    run()
