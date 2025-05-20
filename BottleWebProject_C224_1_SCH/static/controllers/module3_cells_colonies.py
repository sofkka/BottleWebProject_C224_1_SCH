import random

class GameOfLife:
    def __init__(self, width, height, a=2, b=3, c=3):
        # Initialize the game with grid dimensions and rule parameters
        self.width = width
        self.height = height
        self.a = a  
        self.b = b  
        self.c = c  
        # Create an empty grid with all cells dead (0)
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.initial_cells = []  # Store initial alive cell positions
        self.initial_cell_count = 0  # Count of initial alive cells
        self.current_cell_count = 0  # Count of currently alive cells
        self.initialize_grid()  # Randomly initialize grid with alive cells
        self.update_cell_count()  # Update the count of alive cells

    def initialize_grid(self):
        """Initialize grid with random alive cells (20% chance)."""
        for i in range(self.height):
            for j in range(self.width):
                if random.random() < 0.2:  # 20% chance to set cell as alive
                    self.grid[i][j] = 1
                    self.initial_cells.append([i, j])  # Save position of initial alive cell
        self.initial_cell_count = len(self.initial_cells)  # Save total initial alive cells

    def count_neighbors(self, x, y):
        """Count alive neighbors for a cell at position (x, y)."""
        count = 0
        # Check all neighbors in the 8 surrounding positions
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the cell itself
                nx, ny = x + i, y + j
                # Use modulo for toroidal (wrap-around) boundary conditions
                nx = nx % self.height
                ny = ny % self.width
                count += self.grid[nx][ny]
        return count

    def next_generation(self):
        """Compute the next generation based on the rules."""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    # Cell is alive: survives if neighbors in [a, b], otherwise dies
                    if neighbors < self.a or neighbors > self.b:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1
                else:
                    # Cell is dead: becomes alive if exactly c neighbors
                    if neighbors == self.c:
                        new_grid[i][j] = 1
        # Update grid to the new generation
        self.grid = new_grid
        self.update_cell_count()

    def toggle_cell(self, x, y):
        """Toggle the state of a cell at position (x, y)."""
        # Switch between alive (1) and dead (0)
        self.grid[int(x)][int(y)] = 1 if self.grid[int(x)][int(y)] == 0 else 0
        self.update_cell_count()

    def reset(self):
        """Reset the grid to a new random state."""
        # Clear the grid
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.initial_cells = []
        self.initialize_grid()  # Re-initialize with new random alive cells
        self.update_cell_count()

    def update_cell_count(self):
        """Update the current number of alive cells."""
        self.current_cell_count = sum(row.count(1) for row in self.grid)

    def to_json(self):
        """Return the grid and related info as a JSON-serializable dict."""
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