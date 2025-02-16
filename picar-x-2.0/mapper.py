from picarx import Picarx
import time
import numpy as np
import math

class Mapper:
    def __init__(self, car, map_size = 100, cell_size = 1):
        self.car = car
        self.map_size = map_size
        self.cell_size = cell_size
        self.grid = np.zeros((self.map_size, self.map_size))

        self.x = 50
        self.y = 50

    def scan(self, range_deg = 60, deg_interval = 5):

        sensor_readings = []

        for angle in range(-range_deg, range_deg, deg_interval):
            self.car.set_cam_pan_angle(angle)
            time.sleep(0.1)

            angle_readings = []
            for _ in range(3):
                distance = self.car.ultrasonic.read()
                if distance is not None and distance < 200: 
                    angle_readings.append(distance)
                time.sleep(0.05)

            if angle_readings:
                avg_distance = sum(angle_readings) / len(angle_readings)
                sensor_readings.append((angle, avg_distance))

        return sensor_readings
    
    def update_grid(self, sensor_readings):

        obstacle_points = []
        for angle, distance in sensor_readings:
            obstacle_x = int(distance * math.cos(math.radians(angle)))
            obstacle_y = int(distance * math.sin(math.radians(angle)))

            grid_x = self.x + obstacle_x
            grid_y = self.y + obstacle_y

            if 0 <= grid_x < self.map_size and 0 <= grid_y < self.map_size:
                obstacle_points.append((grid_x, grid_y))
                self.grid[grid_y, grid_x] = 1 
        
        for i in range(len(obstacle_points) - 1):
            x0, y0 = obstacle_points[i]
            x1, y1 = obstacle_points[i + 1]

            avg_distance = (sensor_readings[i][1] + sensor_readings[i + 1][1]) / 2
            max_gap = 2 * avg_distance * math.sin(math.radians(2.5)) 

            distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if distance <= max_gap:
                points = self.bresenham_line(x0, y0, x1, y1)
                for x, y in points: 
                    if 0 <= x < self.map_size and 0 <= y < self.map_size:
                        self.grid[y, x] = 1
                    
    def update_position(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def get_grid(self):
        return self.grid

    def bresenham_line(self, x0, y0, x1, y1):
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x,y = x0,y0 

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1 
       
        if dx > dy: 
            err = dx / 2
            while x != x1:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2
            while y != y1:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points.append((x, y)) 
        return points
    
    def visualize_grid(self):
        
        rotated_grid = np.rot90(self.grid, k=1)
        
        for i, row in enumerate(rotated_grid):
            line = ""
            for j, cell in enumerate(row):
                if i == self.x and j == self.y:
                    line += "O"
                elif cell == 1:
                    line += "X"
                else:
                    line += "."
            print(line)
    
def main():
    mapper = Mapper(Picarx())
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
