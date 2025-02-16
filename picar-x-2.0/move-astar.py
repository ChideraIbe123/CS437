from picarx import Picarx
import time
import mapper 
from a_star2 import run_astar

from gpiozero import Device
from gpiozero.pins.native import NativeFactory
Device.pin_factory = NativeFactory()

def run():
	car = Picarx()
	car.set_cam_tilt_angle(30)
	k = 12
	start = (50,50)
	end = (50,60)
	path = run_astar(car,start,end)

	for dir in path:
		if dir[0] == 'F':
			print("Current direction: ", dir[0], "  number: ", dir[1])
			car.set_dir_servo_angle(0)
			car.forward(30)
			time.sleep(dir[1] / 24.0)
			car.forward(0)
		elif dir[0] == 'R':
			print("Current direction: ", dir[0], "  number: ", dir[1])
			turn_right(car)
		else:
			print("Current direction: ", dir[0], "  number: ", dir[1])
			turn_left(car)
		time.sleep(1.0)
	print("Goal location reached")
	
def turn_right(car):
	car.set_dir_servo_angle(-30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(30)
	car.forward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(-30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(30)
	car.forward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(-30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(30)
	car.forward(30)
	time.sleep(0.3)
	car.set_dir_servo_angle(0)
	car.backward(30)
	time.sleep(0.2)
	car.backward(0)

def turn_left(car):
	car.set_dir_servo_angle(30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(-30)
	car.forward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(-30)
	car.forward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(30)
	car.backward(30)
	time.sleep(0.5)
	car.backward(0)
	car.set_dir_servo_angle(-30)
	car.forward(30)
	time.sleep(0.3)
	car.set_dir_servo_angle(0)
	car.forward(0)
	time.sleep(0.3)
	car.backward(30)
	time.sleep(0.2)
	car.backward(0)
				
				
			

if __name__ == "__main__":
    run()
