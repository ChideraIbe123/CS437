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
	start = (50,0)
	end = (50,60)
	path = run_astar(car,start,end)
	dx = path[0][0] - start[0]
	dy = path[0][1] - start[1]
	if dx == 0 and dy == 0:
		print("Goal location reached")
	elif dy != 0:
		car.set_dir_servo_angle(0)
		car.forward(30)
		time.sleep(0.5)
		car.forward(0)
	elif dx > 0:
		car.set_dir_servo_angle(-30)
		car.backward(30)
		car.set_dir_servo_angle(30)
		car.forward(30)
		time.sleep(0.5)
		car.forward(0)
	else:
		car.set_dir_servo_angle(30)
		car.backward(30)
		car.set_dir_servo_angle(-30)
		car.forward(30)
		time.sleep(0.5)
		car.forward(0)
	time.sleep(1.0)
	start = (start[0] + dx * k, start[1] + dy * k)
	path = run_astar(car,start,end)
	
				
				
			

if __name__ == "__main__":
    run()
