import random

class GameOfLife:
    def __init__(self, width, height, a=2, b=3, c=3):
        # Initialize the game with given grid size and rule parameters
        self.width = width  # width of the grid
        self.height = height  # height of the grid
        self.a = a  # minimum number of neighbors for survival (lower bound)
        self.b = b  # maximum number of neighbors for survival (upper bound)
        self.c = c  # number of neighbors required for a dead cell to become alive
        
        # Create an empty grid with all cells dead (0)
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        
        self.initial_cells = []  # list of positions of initially alive cells
        self.initial_cell_count = 0  # count of initial alive cells
        self.current_cell_count = 0  # current count of alive cells
        
        # Initialize grid with random alive cells
        self.initialize_grid()
        # Update the count of alive cells
        self.update_cell_count()

    def initialize_grid(self):
        """Fill the grid with random alive cells with a 20% chance."""
        for i in range(self.height):
            for j in range(self.width):
                # With a 20% probability, set the cell as alive
                if random.random() < 0.2:
                    self.grid[i][j] = 1  # make the cell alive
                    # Save the position of this cell in the list of initial alive cells
                    self.initial_cells.append([i, j])
        # Save the total number of initial alive cells
        self.initial_cell_count = len(self.initial_cells)

    def count_neighbors(self, x, y):
        """Count the number of alive neighbors for the cell at position (x, y)."""
        count = 0
        # Check all 8 surrounding neighbors (including diagonals)
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Skip the cell itself
                if i == 0 and j == 0:
                    continue
                # Calculate neighbor coordinates with wrap-around (toroidal boundary)
                nx, ny = x + i, y + j
                nx = nx % self.height  # vertical boundary
                ny = ny % self.width   # horizontal boundary
                # Count how many neighboring cells are alive
                count += self.grid[nx][ny]
        return count

    def next_generation(self):
        """Compute the next generation based on the game rules."""
        # Create a new empty grid for the next generation
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                # Count neighbors for the current cell
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    # If the cell is alive: it stays alive if neighbors in [a, b]
                    if neighbors < self.a or neighbors > self.b:
                        new_grid[i][j] = 0  # otherwise, it dies
                    else:
                        new_grid[i][j] = 1  # remains alive
                else:
                    # If the cell is dead: it becomes alive if exactly c neighbors
                    if neighbors == self.c:
                        new_grid[i][j] = 1
        # Update the grid to the new generation
        self.grid = new_grid
        # Update the count of alive cells
        self.update_cell_count()

    def toggle_cell(self, x, y):
        """Toggle the state of the cell at position (x, y)."""
        # Switch between dead (0) and alive (1)
        self.grid[int(x)][int(y)] = 1 if self.grid[int(x)][int(y)] == 0 else 0
        # Update the count of alive cells
        self.update_cell_count()

    def reset(self):
        """Reset the grid to a new random state."""
        # Clear the grid
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # Clear list of initial cells
        self.initial_cells = []
        # Re-initialize with new random alive cells
        self.initialize_grid()
        # Update the count of alive cells
        self.update_cell_count()

    def update_cell_count(self):
        """Update the current number of alive cells."""
        self.current_cell_count = sum(row.count(1) for row in self.grid)

    def to_json(self):
        """Return the game state as a dictionary suitable for JSON serialization."""
        return {
            'width': self.width,
            'height': self.height,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'grid': self.grid,
            'initial_cell_count': self.initial_cell_count,
            'initial_cells': self.initial_cells,
            'current_cell_count': self.current_cell_count
        }