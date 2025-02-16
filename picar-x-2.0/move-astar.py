from picarx import Picarx
import time
import mapper 
from a_star2 import run_astar
from vilib import Vilib

from gpiozero import Device
from gpiozero.pins.native import NativeFactory
Device.pin_factory = NativeFactory()

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

def run():
	car = Picarx()
	car.set_cam_tilt_angle(30)
	k = 12
	start = (50,50)
	end = (50,150)
	path = run_astar(car,start,end)
	car.set_cam_pan_angle(0)
	turn_count = 0
	for dir in path:
		print(type(dir))
		print(dir)
		if(dir[0] == '0'):
			continue
		elif dir[0] == 'F':
			print("Current direction: ", dir[0], "  number: ", dir[1])
			car.set_dir_servo_angle(0)
			car.forward(30)
			t = 0
			if dir[1] > 4 and dir[2] == "North":
				t = (dir[1] - 3) / 24.0 # stop before the obstacle
			else: #  go to the side longer just to be safe
				t = (dir[1] + 20) / 24.0
			time.sleep(t)
			car.forward(0)
			if dir[2] == "North":
				end = (end[0] ,end[1] - dir[1])
			elif dir[2] == "East":
				end = (end[0] - dir[1] , end[1])
			elif dir[2] == "West":
				end = (end[0] + dir[1],end[1])
				
		elif dir[0] == 'R':
			print("Current direction: ", dir[0], "  number: ", dir[1])
			turn_right(car)
			car.forward(30)
			time.sleep(0.2)
			turn_count += 1
		else:
			print("Current direction: ", dir[0], "  number: ", dir[1])
			turn_left(car)
			car.forward(30)
			time.sleep(0.2)
			turn_count+= 1
		if turn_count%2 == 0 and turn_count != 0:
			car.set_dir_servo_angle(0)
			car.forward(30)
			time.sleep(1.5)
			car.forward(0)
			path = run_astar(car,start,end)
			turn_count = 0
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
	time.sleep(0.3)
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
	time.sleep(0.3)
	car.backward(0)
				
				
			

if __name__ == "__main__":
	run()
	
