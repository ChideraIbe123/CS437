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

def move25():
    speed4 = fc.Speed(25)
    speed4.start()  
    fc.backward(100)
    x = 0
    while x < range(1):
        time.sleep(0.1)
        speed = speed4
        x += speed * 0.1 
        print("%smm/s"%speed)
    print("%smm"%speed)    
    speed4.definit()
    fc.stop(0)

def move_autonomous():
    while True:
        if get_distance() < 15:
            stop()
            backward()
            turn_left()
        else:
            forward()

if __name__ == "__main__":
    move_autonomous()
    