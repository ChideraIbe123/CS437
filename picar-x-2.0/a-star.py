from picarx import Picarx
import time
import heapq

# --- Configuration Parameters ---
SPEED = 100         # Movement speed
DANGER = 20         # If ultrasonic distance < DANGER (in cm), treat as obstacle
CELL_MOVE_TIME = 0.5  # Time to move one grid cell (adjust based on your robot's speed)

# --- A* Pathfinding Functions ---
def heuristic(a, b):
    # Manhattan distance heuristic for grid movement.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node, grid):
    neighbors = []
    # Allowed moves: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows = len(grid)
    cols = len(grid[0])
    for d in directions:
        nxt = (node[0] + d[0], node[1] + d[1])
        if 0 <= nxt[0] < rows and 0 <= nxt[1] < cols:
            if grid[nxt[0]][nxt[1]] == 0:  # 0 means free space
                neighbors.append(nxt)
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)
        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# --- Movement and Navigation Functions ---
# For simplicity, we assume the robot is aligned with the grid.
# We define a mapping from grid movement (delta row, delta col)
# to a desired servo angle adjustment. (These angles are relative.)
# For example, assume initial heading is "up" (north).
def move_to_next_cell(car, current, next_cell):
    d_row = next_cell[0] - current[0]
    d_col = next_cell[1] - current[1]
    
    # Determine desired turn based on movement direction.
    # Using a simple approach:
    # - If moving up (d_row = -1, d_col = 0): go straight (servo angle 0)
    # - If moving down (d_row = 1, d_col = 0): turn 180 (simulate by turning left twice)
    # - If moving right (d_row = 0, d_col = 1): turn right (servo angle +30)
    # - If moving left (d_row = 0, d_col = -1): turn left (servo angle -30)
    if d_row == -1 and d_col == 0:
        angle = 0
    elif d_row == 1 and d_col == 0:
        # For simplicity, we simulate a 180 turn by turning left twice.
        angle = -30  # first turn; we will execute a double turn below
    elif d_row == 0 and d_col == 1:
        angle = 30
    elif d_row == 0 and d_col == -1:
        angle = -30
    else:
        angle = 0  # default
    
    # Check ultrasonic sensor before moving.
    dist = round(car.ultrasonic.read(), 2)
    if dist < DANGER:
        # If obstacle detected, perform an avoidance maneuver:
        print("Obstacle too close! Moving backward to avoid collision.")
        car.backward(SPEED)
        time.sleep(0.5)
        car.forward(0)  # stop movement
        return False

    # Set servo angle to desired direction.
    car.set_dir_servo_angle(angle)
    time.sleep(0.1)  # allow time for servo adjustment

    # For a 180 turn simulation (moving down), we perform a double turn.
    if d_row == 1 and d_col == 0:
        # First half-turn:
        car.backward(SPEED)
        time.sleep(0.3)
        car.forward(0)
        # Now simulate an additional turn if needed.
        car.set_dir_servo_angle(angle)
        time.sleep(0.1)
    
    # Move forward for the duration required to traverse one grid cell.
    car.forward(SPEED)
    time.sleep(CELL_MOVE_TIME)
    car.forward(0)  # Stop after cell move
    
    return True

def run():
    try:
        car = Picarx()
        # Define a sample grid (5x5) where 0 = free space, 1 = obstacle.
        grid = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        start = (0, 0)  # top-left cell
        goal = (4, 4)   # bottom-right cell
        
        # Compute A* path from start to goal.
        path = astar(grid, start, goal)
        if not path:
            print("No path found!")
            return
        print("Path found:", path)
        
        current = start
        # Iterate through the path (skipping the starting cell).
        for next_cell in path[1:]:
            print(f"Moving from {current} to {next_cell}...")
            success = move_to_next_cell(car, current, next_cell)
            if not success:
                print("Movement aborted due to an obstacle. Replanning required.")
                break
            current = next_cell
            time.sleep(0.2)
        
        print("Navigation complete.")
        
    finally:
        # Stop the car at the end.
        car.forward(0)

if __name__ == "__main__":
    run()
