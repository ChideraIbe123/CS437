from picarx import Picarx
import time
import numpy as np
import math

class Mapper:
    def __init__(self, map_size = 100, cell_size = 1):
        self.car = Picarx()
        self.map_size = map_size
        self.cell_size = cell_size
        # initially all cells have no obstacle
        self.grid = np.zeros((self.map_size, self.map_size))

        # starting position
        self.x = self.map_size // 2
        self.y = 0

    def scan(self, range_deg = 60, deg_interval = 5):
        # scan the environment using the ultrasonic sensor

        sensor_readings = []

        for angle in range(-range_deg, range_deg, deg_interval):
            #self.car.set_dir_servo_angle(angle)
            self.car.set_cam_pan_angle(angle)
            time.sleep(0.1)

            # take 3 readings and average them for accuracy
            angle_readings = []
            for _ in range(3):
                distance = self.car.ultrasonic.read()
                if distance is not None and distance < 100: # only consider valid readings within our grid size
                    angle_readings.append(distance)
                time.sleep(0.05)

            # average the readings
            if angle_readings:
                avg_distance = sum(angle_readings) / len(angle_readings)
                sensor_readings.append((angle, avg_distance)) # associate each angle with its obstacle distance

        return sensor_readings
    
    def update_grid(self, sensor_readings):
        # update the grid based on the sensor readings

        obstacle_points = []
        for angle, distance in sensor_readings:
            obstacle_x = int(distance * math.cos(math.radians(angle)))
            obstacle_y = int(distance * math.sin(math.radians(angle)))

            # convert to grid coordinates
            grid_x = self.x + obstacle_x
            grid_y = self.y + obstacle_y

            # check if the obstacle is within the grid
            if 0 <= grid_x < self.map_size and 0 <= grid_y < self.map_size:
                obstacle_points.append((grid_x, grid_y))
                self.grid[grid_y, grid_x] = 1 # mark as obstacle
        
        # If 2 adjacent angles have obstacles, fill in the gap
        for i in range(len(obstacle_points) - 1):
            x0, y0 = obstacle_points[i]
            x1, y1 = obstacle_points[i + 1]

            # calculate the average disctance and max gap between the points
            avg_distance = (sensor_readings[i][1] + sensor_readings[i + 1][1]) / 2
            max_gap = 2 * avg_distance * math.sin(math.radians(2.5)) # max gap between 2 points 5 degrees apart

            distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance <= max_gap:
                points = self.bresenham_line(x0, y0, x1, y1)
                for x, y in points: # fill in the gap
                    if 0 <= x < self.map_size and 0 <= y < self.map_size:
                        self.grid[y, x] = 1
                    
    def update_position(self, dx, dy):
        # update the position of the car
        self.x += dx
        self.y += dy

    def bresenham_line(self, x0, y0, x1, y1):
        # Bresenham's line algorithm to get all points in a line
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x,y = x0,y0 # start point

        sx = 1 if x0 < x1 else -1 #step in x direction
        sy = 1 if y0 < y1 else -1 #step in y direction
       
        if dx > dy: # more horizontal than vertical
            err = dx / 2
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else: # more vertical than horizontal
            err = dy / 2
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points.append((x, y)) # add the last point
        return points
    
    def visualize_grid(self):
        # visualize the grid
        # transpose and reverse rows for -90 degree rotation
        rotated_grid = np.rot90(self.grid, k=1)  # k=1 for -90 degrees
        
        for row in rotated_grid:
            line = ""
            for cell in row:
                if cell == 1:
                    line += "X"
                else:
                    line += "."
            print(line)
    
def main():
    mapper = Mapper()
    try:
        while True:
            print("Scanning...")
            sensor_readings = mapper.scan()
            print(f"Found {len(sensor_readings)} obstacles")
            mapper.update_grid(sensor_readings)
            mapper.visualize_grid()
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("Exiting...")
        mapper.car.reset()

if __name__ == "__main__":
    main()
                    
                
        
        



        

