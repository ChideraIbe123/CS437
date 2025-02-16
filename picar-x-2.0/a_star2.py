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
            while current in came_from:
                path.append(current)
                current = came_from[current]
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
    return other
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
        
