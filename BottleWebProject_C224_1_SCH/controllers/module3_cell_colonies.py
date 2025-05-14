import copy

def create_empty_grid(width, height):

    return [[0 for _ in range(width)] for _ in range(height)]

def count_alive_neighbors(grid, x, y):

    count = 0
    height = len(grid)
    width = len(grid[0])
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                count += grid[ny][nx]
    return count

def step_grid(grid, a, b, c):

    height = len(grid)
    width = len(grid[0])
    new_grid = copy.deepcopy(grid)
    for y in range(height):
        for x in range(width):
            neighbors = count_alive_neighbors(grid, x, y)
            if grid[y][x] == 1:
                if neighbors < a or neighbors > b:
                    new_grid[y][x] = 0
            else:
                if neighbors == c:
                    new_grid[y][x] = 1
    return new_grid