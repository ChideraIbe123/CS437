import time
import picar_4wd as fc

def get_distance():
    return fc.get_distance_at(0)

def forward(speed=10, duration=10):
    fc.forward(speed)
    time.sleep(duration)
    stop()

def backward(speed=10, duration=10):
    fc.backward(speed)
    time.sleep(duration)
    stop()

def stop(): 
    fc.stop()

def turn_left(degrees=90):
    fc.turn_left(degrees)

def turn_right(degrees=90):
    fc.turn_right(degrees)

if __name__ == "__main__":
    forward()
    stop()
    backward()
    stop()
    