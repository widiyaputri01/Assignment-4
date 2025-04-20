import heapq
import time

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def parse_grid(grid):
    start = goal = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'G':
                goal = (i, j)
    return start, goal

def is_valid(grid, pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#'

def elevation(grid, pos):
    val = grid[pos[0]][pos[1]]
    if val in 'SG':
        return 1  # default base cost for S/G
    return int(val)

def move_cost(grid, current, neighbor):
    return abs(elevation(grid, neighbor) - elevation(grid, current)) + elevation(grid, neighbor)

def heuristic(grid, a, b):
    return manhattan(a, b) + abs(elevation(grid, a) - elevation(grid, b))

def a_star(grid, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    explored = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        explored += 1

        if current == goal:
            return reconstruct_path(came_from, current), explored

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if is_valid(grid, neighbor):
                cost = move_cost(grid, current, neighbor)
                tentative_g = g_score[current] + cost
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(grid, neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    return None, explored

def gbfs(grid, start, goal):
    open_set = [(heuristic(grid, start, goal), start)]
    came_from = {}
    visited = set()
    explored = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        explored += 1

        if current == goal:
            return reconstruct_path(came_from, current), explored

        visited.add(current)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if is_valid(grid, neighbor) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(grid, neighbor, goal), neighbor))

    return None, explored

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def visualize(grid, path):
    grid_copy = [list(row) for row in grid]
    for x, y in path:
        if grid_copy[x][y] not in 'SG':
            grid_copy[x][y] = '*'
    for row in grid_copy:
        print("".join(row))

def compare(grid):
    start, goal = parse_grid(grid)

    print(" A* Search:")
    t0 = time.time()
    path_a, nodes_a = a_star(grid, start, goal)
    t1 = time.time()

    print(" GBFS Search:")
    t2 = time.time()
    path_g, nodes_g = gbfs(grid, start, goal)
    t3 = time.time()

    print("\n A* Path:")
    if path_a:
        visualize(grid, path_a)
        print(f"Nodes Explored: {nodes_a}")
        print(f"Time: {(t1 - t0)*1000:.3f} ms")
    else:
        print("No path found.")

    print("\n GBFS Path:")
    if path_g:
        visualize(grid, path_g)
        print(f"Nodes Explored: {nodes_g}")
        print(f"Time: {(t3 - t2)*1000:.3f} ms")
    else:
        print("No path found.")

# Example terrain grid
terrain = [
    ['S', '1', '2', '#', '3'],
    ['1', '2', '#', '4', 'G'],
    ['1', '1', '2', '5', '6']
]

if __name__ == "__main__":
    compare(terrain)
