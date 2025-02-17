from mapper import Mapper
import time
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    open_set = [(0, start)]
    came_from = {}
    cost = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            print("solution path:")
            while current in came_from:
                path.append(current)
                current = came_from[current]
                print(current[0], ", " ,current[1])
            return path[::-1]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost[current] + 1
                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost + heuristic(neighbor, goal), neighbor))
                    came_from[neighbor] = current


    return None
    
def run_astar(car, start=(50,50), end=(100,100)):
    mapper = Mapper(car)
    try:
        print("Scanning...")
        sensor_readings = mapper.scan()
        print(f"Found {len(sensor_readings)} obstacles")
        mapper.update_grid(sensor_readings)
        mapper.visualize_grid()
        time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        mapper.car.reset()
    other = a_star(mapper.get_grid(), start, end)
    directions = []
    dir = '0'
    curr_x = start[0]
    curr_y = start[1]
    head = "North"
    for cord in other:
        dx = cord[0] - curr_x
        dy = cord[1] - curr_y
        curr_x = cord[0]
        curr_y = cord[1]
        if(dx > 0):
            if head == "North":
                head = "East"
                new_dir = 'R'
            elif head == "West":
                head = "North"
                new_dir = 'R'
            else:
                new_dir = 'F'
        elif(dx < 0):
            if head == "North":
                head = "West"
                new_dir = 'L'
            elif head == "East":
                head = "North"
                new_dir = 'L'
            else:
                new_dir = 'F'
        else:
            if head == "East":
                head = "North"
                new_dir = 'L'
            elif head == "West":
                head = "North"
                new_dir = 'R'
            else:
                new_dir = 'F'
        directions.append([new_dir,head])
    simple_directions = [['0',0,'Null']]
    for dir,pose in directions:
        if dir == 'F':
            if simple_directions[-1][0] == 'F':
                simple_directions[-1][1] += 1
            else:
                simple_directions.append(['F', 1,pose])
        elif dir == 'L':
            simple_directions.append(['L',1,'Null'])
        elif dir == 'R':
            simple_directions.append(['R',1,'Null'])
            
    return simple_directions
if __name__ == "__main__":
        start, end = (50, 50), (50,51) 
        mapper = Mapper()
        try:
            print("Scanning...")
            sensor_readings = mapper.scan()
            print(f"Found {len(sensor_readings)} obstacles")
            mapper.update_grid(sensor_readings)
            mapper.visualize_grid()
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            mapper.car.reset()
        other = a_star(mapper.get_grid(), start, end)
        print(other)
        
