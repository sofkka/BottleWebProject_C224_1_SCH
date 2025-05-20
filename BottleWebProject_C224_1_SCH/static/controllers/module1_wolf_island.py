# -*- coding: cp1251 -*-
import random
from datetime import datetime

# ���������� ������� ��� �������� ��������� ���������
simulation_state = {}

# ����� ��� ��������
class Rabbit:
    # ������������� ���������� ������� � ������������
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ����� ��� ������
class Wolf:
    # ������������� ���������� ����� � ������������ � ������
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 1.0  # ��������� ���� �����

# ����� ��� ������
class SheWolf:
    # ������������� ���������� ������� � ������������ � ������
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = 1.0  # ��������� ���� �������

# ������� ��� ���������� �������� ������ � �����
def get_neighbors(x, y, N, M):
    # ������ ��� �������� ��������� �������� ������
    neighbors = []
    # ������� ���� �������� ������ �� ��� X
    for dx in [-1, 0, 1]:
        # ������� ���� �������� ������ �� ��� Y
        for dy in [-1, 0, 1]:
            # ��������, ����� �� �������� ������� ������
            if dx == 0 and dy == 0:
                # ������� ������� ������
                continue
            # ���������� ��������� �������� ������
            new_x = x + dx
            new_y = y + dy
            # ��������, ��� ���������� ��������� ������ �����
            if 0 <= new_x < N and 0 <= new_y < M:
                # ���������� ��������� �������� ������ � ������
                neighbors.append((new_x, new_y))
    # ������� ������ �������� ������
    return neighbors

# ������� ��� ������������� ���������
def initialize_simulation(N, M, num_rabbits, num_wolves, num_she_wolves):
    # �������� ����� �������� N x M � ������� �������� � �������
    grid = [[[] for i in range(M)] for i in range(N)]
    # �������� ������� ��� �������� ��������, ������ � ������
    rabbits_list = []
    wolves_list = []
    she_wolves_list = []

    # ��������� ������ ���� ��������� ������ �� �����
    available_cells = [(i, j) for i in range(N) for j in range(M)]
    # ������������� ������ ��� ���������� ����������
    random.shuffle(available_cells)
    
    # ���������� �������� �� �����
    for i in range(min(num_rabbits, len(available_cells))):
        # ���������� ��������� ��������� �� ������ ��������� ������ (����� ��������� �������)
        x, y = available_cells.pop()
        # �������� ������ ������� � ��������� ������������
        rabbit = Rabbit(x, y)
        # ���������� ������� � ������ �� �����
        grid[x][y].append(rabbit)
        # ���������� ������� � ������ ��������
        rabbits_list.append(rabbit)

    # ���������� ������ �� �����
    for i in range(min(num_wolves, len(available_cells))):
        # ���������� ��������� ��������� (����� ��������� �������, ������ -1)
        x, y = available_cells.pop()
        # �������� ������ �����
        wolf = Wolf(x, y)
        # ���������� ����� � ������
        grid[x][y].append(wolf)
        # ���������� ����� � ������ ������
        wolves_list.append(wolf)

    # ���������� ������ �� �����
    for i in range(min(num_she_wolves, len(available_cells))):
        # ���������� ��������� ��������� (����� ��������� �������, ������ -1)
        x, y = available_cells.pop()
        # �������� ����� �������
        she_wolf = SheWolf(x, y)
        # ���������� ������� � ������
        grid[x][y].append(she_wolf)
        # ���������� ������� � ������ ������
        she_wolves_list.append(she_wolf)

    # ������� ����� � ������� ��������
    return grid, rabbits_list, wolves_list, she_wolves_list

# ������� ��� ������� ����� ����� ���� ���������
def clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M):
    # �������� ����� ������� ��� ���������� ��������
    new_rabbits_list = []
    new_wolves_list = []
    new_she_wolves_list = []

    # ������ �� ���� ������� �����
    for i in range(N):
        for j in range(M):
            # �������� ������� �������� � ������� ������
            if len(grid[i][j]) > 0:
                # ������������ ������ �������� � ������
                rabbits_in_cell = [e for e in grid[i][j] if isinstance(e, Rabbit)]
                # �������� ������� ��������
                if rabbits_in_cell:
                    # ������������ ������ �������� � �������������� ������
                    predators = [e for e in grid[i][j] if isinstance(e, (Wolf, SheWolf)) and e.points > 0]
                    # �������� ������� ��������
                    if predators:
                        # ����� ������� ��� ��������
                        rabbit = rabbits_in_cell[0]
                        # ����� ���������� �������
                        predator = random.choice(predators)
                        # ���������� ����� �������
                        predator.points += 1
                        # �������� ������� �� ������
                        grid[i][j].remove(rabbit)
                        # �������� ������� ������� � ����� ������
                        if rabbit in rabbits_list:
                            # �������� ������� �� ������
                            rabbits_list.remove(rabbit)
                
                # �������� ������� ���������� �������� � ������
                if len(grid[i][j]) > 1:
                    # ���������� ������ ����� ������� (��������� 1)
                    she_wolf = next((e for e in grid[i][j] if isinstance(e, SheWolf) and e.points > 0), None)
                    # ���������� ������� ������ ����� (��������� 2)
                    wolf = next((e for e in grid[i][j] if isinstance(e, Wolf) and e.points > 0), None)
                    # ���������� ������� ������� (��������� 3)
                    rabbit = next((e for e in grid[i][j] if isinstance(e, Rabbit)), None)
                    # �������� ������� �������
                    if she_wolf:
                        # �������� ������� � ������
                        grid[i][j] = [she_wolf]
                        # ���������� ������� � ����� ������
                        new_she_wolves_list.append(she_wolf)
                    # �������� ������� ����� ��� ���������� �������
                    elif wolf:
                        # �������� �����
                        grid[i][j] = [wolf]
                        # ���������� ����� � ����� ������
                        new_wolves_list.append(wolf)
                    # �������� ������� ������� ��� ���������� ��������
                    elif rabbit:
                        # �������� �������
                        grid[i][j] = [rabbit]
                        # ���������� ������� � ����� ������
                        new_rabbits_list.append(rabbit)
                    # ��������� ������ ���������� ���������� ��������
                    else:
                        # ������� ������
                        grid[i][j] = []
                # �������� ������� ������ ��������� � ������
                elif grid[i][j]:
                    # ��������� ������������� ���������
                    entity = grid[i][j][0]
                    # �������� ���� ���������
                    if isinstance(entity, Rabbit):
                        # ���������� ������� � ����� ������
                        new_rabbits_list.append(entity)
                    # �������� ������� ������ �����
                    elif isinstance(entity, Wolf) and entity.points > 0:
                        # ���������� ����� � ����� ������
                        new_wolves_list.append(entity)
                    # �������� ������� ����� �������
                    elif isinstance(entity, SheWolf) and entity.points > 0:
                        # ���������� ������� � ����� ������
                        new_she_wolves_list.append(entity)
                    # ��������� �������� ���������
                    else:
                        # ������� ������
                        grid[i][j] = []
                # ��������� ������ ������
                else:
                    # �������� ������ ������
                    grid[i][j] = []

    # ���������� ������� ��������
    rabbits_list[:] = new_rabbits_list
    wolves_list[:] = new_wolves_list
    she_wolves_list[:] = new_she_wolves_list

    # ������� ����������� ����� � �������
    return grid, rabbits_list, wolves_list, she_wolves_list

# ������� ��� ��������� ��������� ��������
def process_rabbits(grid, rabbits_list, N, M):
    # �������� ������ ��� ����� ��������
    new_rabbits = []
    # ������ �� ����� ������ ��������
    for rabbit in rabbits_list[:]:
        # ��������� ������� ������ �������
        current_cell = grid[rabbit.x][rabbit.y]
        # �������� ������� ������� � ����� ������
        if rabbit not in current_cell:
            # ������� �������� ��� ���������� �������
            continue
        
        # �������� ����������� �����������, ��������� � ��������� ������ �� 0 �� 1
        if random.random() < 0.3:
            # ��������� �������� ������
            neighbors = get_neighbors(rabbit.x, rabbit.y, N, M)
            # ���������� ��������� �������� ������
            free_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # �������� ������� ��������� ������
            if free_neighbors:
                # ����� ��������� ��������� ��� �����������
                new_x, new_y = random.choice(free_neighbors)
                # �������� ������ ������� � ������� ������
                new_rabbit = Rabbit(rabbit.x, rabbit.y)
                # ���������� ������ ������� � ������
                grid[rabbit.x][rabbit.y].append(new_rabbit)
                # ���������� ������ ������� � ������
                new_rabbits.append(new_rabbit)
                # �������� ������� ������� � ������� ������
                if rabbit in current_cell:
                    # �������� ������� ������� �� ������
                    current_cell.remove(rabbit)
                # ���������� ��������� ������� �������
                rabbit.x, rabbit.y = new_x, new_y
                # ���������� ������� ������� � ����� ������
                grid[new_x][new_y].append(rabbit)
        # ��������� ������ ��� �����������
        else:
            # �������� ����������� �������� �� ����� (1/9)
            if random.random() < 1/9:
                # ������� �����������
                continue
            # ��������� �������� ������
            neighbors = get_neighbors(rabbit.x, rabbit.y, N, M)
            # ���������� ��������� ������
            free_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # �������� ������� ��������� ������
            if free_neighbors:
                # ����� ��������� ���������
                new_x, new_y = random.choice(free_neighbors)
                # �������� ������� ������� � ������� ������
                if rabbit in current_cell:
                    # �������� ������� �� ������� ������
                    current_cell.remove(rabbit)
                # ���������� ��������� �������
                rabbit.x, rabbit.y = new_x, new_y
                # ���������� ������� � ����� ������
                grid[new_x][new_y].append(rabbit)
    
    # ���������� ����� �������� � ����� ������
    rabbits_list.extend(new_rabbits)
    
    # ������� ����������� ����� � ������ ��������
    return grid, rabbits_list

# ������� ��� ��������� ��������� ������
def process_she_wolves(grid, she_wolves_list, rabbits_list, N, M):
    # ������ �� ����� ������ ������
    for she_wolf in she_wolves_list[:]:
        # ��������� ������� ������ �������
        current_cell = grid[she_wolf.x][she_wolf.y]
        # �������� ������� ������� � ������
        if she_wolf not in current_cell:
            # ������� ��������
            continue
        
        # ��������� ����� �������� �������
        ate_rabbit = False
        # ������������ ������ �������� � ������� ������
        rabbits_in_cell = [e for e in grid[she_wolf.x][she_wolf.y] if isinstance(e, Rabbit)]
        # �������� ������� ��������
        if rabbits_in_cell:
            # ����� ������� ��� ��������
            rabbit_to_eat = rabbits_in_cell[0]
            # �������� ������� �� ������
            current_cell.remove(rabbit_to_eat)
            # �������� ������� ������� � ����� ������
            if rabbit_to_eat in rabbits_list:
                # �������� ������� �� ������
                rabbits_list.remove(rabbit_to_eat)
            # ���������� ����� �������
            she_wolf.points += 1
            # ��������� ����� ��������
            ate_rabbit = True
        # ��������� ���������� ������� � ������� ������
        else:
            # ��������� �������� ������
            neighbors = get_neighbors(she_wolf.x, she_wolf.y, N, M)
            # ���������� ������ � ���������
            rabbit_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, Rabbit) for e in grid[nx][ny])]
            # �������� ������� �������� � �������� �������
            if rabbit_neighbors:
                # ����� ��������� ������ � ��������
                target_x, target_y = random.choice(rabbit_neighbors)
                # �������� ������� ������� � ������� ������
                if she_wolf in current_cell:
                    # �������� ������� �� ������� ������
                    current_cell.remove(she_wolf)
                # ���������� ��������� �������
                she_wolf.x, she_wolf.y = target_x, target_y
                # ���������� ������� � ������� ������
                grid[target_x][target_y].append(she_wolf)
                # ������������ ������ �������� � ������� ������
                rabbits_in_target = [e for e in grid[target_x][target_y] if isinstance(e, Rabbit)]
                # �������� ������� ��������
                if rabbits_in_target:
                    # ����� ������� ��� ��������
                    rabbit_to_eat = rabbits_in_target[0]
                    # �������� ������� �� ������
                    grid[target_x][target_y].remove(rabbit_to_eat)
                    # �������� ������� ������� � ������
                    if rabbit_to_eat in rabbits_list:
                        # �������� ������� �� ������
                        rabbits_list.remove(rabbit_to_eat)
                    # ���������� ����� �������
                    she_wolf.points += 1
                    # ��������� ����� ��������
                    ate_rabbit = True
        
        # �������� ���������� �������� �������
        if not ate_rabbit:
            # ���������� ����� �������
            she_wolf.points -= 0.1
            # ��������� �������� ������
            neighbors = get_neighbors(she_wolf.x, she_wolf.y, N, M)
            # ���������� ��������� ������
            empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # �������� ������� ��������� ������
            if empty_neighbors:
                # ����� ��������� ���������
                new_x, new_y = random.choice(empty_neighbors)
                # �������� ������� ������� � ������� ������
                if she_wolf in current_cell:
                    # �������� ������� �� ������� ������
                    current_cell.remove(she_wolf)
                # ���������� ��������� �������
                she_wolf.x, she_wolf.y = new_x, new_y
                # ���������� ������� � ����� ������
                grid[new_x][new_y].append(she_wolf)
        
        # �������� ������������� ����� � �������
        if she_wolf.points <= 0:
            # �������� ������� ������� � ������
            if she_wolf in grid[she_wolf.x][she_wolf.y]:
                # �������� ������� �� ������
                grid[she_wolf.x][she_wolf.y].remove(she_wolf)
            # �������� ������� ������� � ������
            if she_wolf in she_wolves_list:
                # �������� ������� �� ������
                she_wolves_list.remove(she_wolf)
    
    # ������� ����������� ����� � �������
    return grid, she_wolves_list, rabbits_list

# ������� ��� ��������� ��������� ������
def process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M):
    # ������ �� ����� ������ ������
    for wolf in wolves_list[:]:
        # ��������� ������� ������ �����
        current_cell = grid[wolf.x][wolf.y]
        # �������� ������� ����� � ������
        if wolf not in current_cell:
            # ������� ��������
            continue
        
        # ��������� ������ ��� �������� � �����������
        ate_rabbit = False
        reproduction = False
        # ������������ ������ �������� � ������� ������
        rabbits_in_cell = [e for e in current_cell if isinstance(e, Rabbit)]
        # �������� ������� ��������
        if rabbits_in_cell:
            # ����� ������� ��� ��������
            rabbit_to_eat = rabbits_in_cell[0]
            # �������� ������� �� ������
            current_cell.remove(rabbit_to_eat)
            # �������� ������� ������� � ������
            if rabbit_to_eat in rabbits_list:
                # �������� ������� �� ������
                rabbits_list.remove(rabbit_to_eat)
            # ���������� ����� �����
            wolf.points += 1
            # ��������� ����� ��������
            ate_rabbit = True
        # ��������� ���������� ������� � ������� ������
        else:
            # ��������� �������� ������
            neighbors = get_neighbors(wolf.x, wolf.y, N, M)
            # ���������� ������ � ���������
            rabbit_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, Rabbit) for e in grid[nx][ny])]
            # �������� ������� �������� � �������� �������
            if rabbit_neighbors:
                # ����� ��������� ������ � ��������
                target_x, target_y = random.choice(rabbit_neighbors)
                # �������� ������� ����� � ������� ������
                if wolf in current_cell:
                    # �������� ����� �� ������� ������
                    current_cell.remove(wolf)
                # ���������� ��������� �����
                wolf.x, wolf.y = target_x, target_y
                # ���������� ����� � ������� ������
                grid[target_x][target_y].append(wolf)
                # ������������ ������ �������� � ������� ������
                rabbits_in_target = [e for e in grid[target_x][target_y] if isinstance(e, Rabbit)]
                # �������� ������� ��������
                if rabbits_in_target:
                    # ����� ������� ��� ��������
                    rabbit_to_eat = rabbits_in_target[0]
                    # �������� ������� �� ������
                    grid[target_x][target_y].remove(rabbit_to_eat)
                    # �������� ������� ������� � ������
                    if rabbit_to_eat in rabbits_list:
                        # �������� ������� �� ������
                        rabbits_list.remove(rabbit_to_eat)
                    # ���������� ����� �����
                    wolf.points += 1
                    # ��������� ����� ��������
                    ate_rabbit = True
            # ��������� ���������� �������� ����������
            else:
                # ���������� ������ � ������ ���������
                she_wolf_neighbors = [(nx, ny) for nx, ny in neighbors if any(isinstance(e, SheWolf) and e.points > 0 for e in grid[nx][ny])]
                # �������� ������� ������ ����������
                if she_wolf_neighbors:
                    # ����� ��������� ������ � ��������
                    target_x, target_y = random.choice(she_wolf_neighbors)
                    # �������� ������� ����� � ������� ������
                    if wolf in current_cell:
                        # �������� ����� �� ������� ������
                        current_cell.remove(wolf)
                    # ���������� ��������� �����
                    wolf.x, wolf.y = target_x, target_y
                    # ���������� ����� � ������� ������
                    grid[target_x][target_y].append(wolf)
                    # ������������ ������ ����� ������ � ������
                    she_wolves_in_cell = [e for e in grid[target_x][target_y] if isinstance(e, SheWolf) and e.points > 0]
                    # �������� ������� ������
                    if she_wolves_in_cell:
                        # ����� ������ �������
                        she_wolf = she_wolves_in_cell[0]
                        # ��������� �������� ������
                        neighbors = get_neighbors(target_x, target_y, N, M)
                        # ���������� ��������� ������
                        empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
                        # �������� ������� ������� 3 ��������� ������ ��� �����������
                        if len(empty_neighbors) >= 3:
                            # ����������� ���� ��������� ��������� �������
                            descendant_gender = random.choice(['wolf', 'she_wolf'])
                            # �������� ���� ������� (����)
                            if descendant_gender == 'wolf':
                                # �������� ������ �����
                                descendant = Wolf(target_x, target_y)
                                # ���������� ����� � ������
                                wolves_list.append(descendant)
                            # �������� ���� ������� (�������)
                            else:
                                # �������� ����� �������
                                descendant = SheWolf(target_x, target_y)
                                # ���������� ������� � ������
                                she_wolves_list.append(descendant)
                            # ��������� ��������� ����� ���������
                            descendant.points = 1.0
                            # ���������� ��������� � ������
                            grid[target_x][target_y].append(descendant)
                            # ��������� ����� �����������
                            reproduction = True
                            # ����� ��������� ��� ����������� �������
                            new_x, new_y = random.choice(empty_neighbors)
                            # �������� ������� ������� � ������
                            if she_wolf in grid[target_x][target_y]:
                                # �������� ������� �� ������
                                grid[target_x][target_y].remove(she_wolf)
                            # ���������� ��������� �������
                            she_wolf.x, she_wolf.y = new_x, new_y
                            # ���������� ������� � ����� ������
                            grid[new_x][new_y].append(she_wolf)
                            # �������� �������������� ��������� �� ������
                            empty_neighbors.remove((new_x, new_y))
                            # ���������� ����� �������
                            she_wolf.points -= 0.1
                            # ����� ��������� ��� ����������� �����
                            new_x, new_y = random.choice(empty_neighbors)
                            # �������� ������� ����� � ������
                            if wolf in grid[target_x][target_y]:
                                # �������� ����� �� ������
                                grid[target_x][target_y].remove(wolf)
                            # ���������� ��������� �����
                            wolf.x, wolf.y = new_x, new_y
                            # ���������� ����� � ����� ������
                            grid[new_x][new_y].append(wolf)
                            # ���������� ����� �����
                            wolf.points -= 0.1
                        # ��������� ������ � ����������� ��������� ������
                        else:
                            # ������� �����������
                            continue
        
        # �������� ���������� �������� ��� �����������
        if not ate_rabbit and not reproduction:
            # ���������� ����� �����
            wolf.points -= 0.1
            # ��������� �������� ������
            neighbors = get_neighbors(wolf.x, wolf.y, N, M)
            # ���������� ��������� ������
            empty_neighbors = [(nx, ny) for nx, ny in neighbors if not grid[nx][ny]]
            # �������� ������� ��������� ������
            if empty_neighbors:
                # ����� ��������� ���������
                new_x, new_y = random.choice(empty_neighbors)
                # �������� ������� ����� � ������� ������
                if wolf in current_cell:
                    # �������� ����� �� ������� ������
                    current_cell.remove(wolf)
                # ���������� ��������� �����
                wolf.x, wolf.y = new_x, new_y
                # ���������� ����� � ����� ������
                grid[new_x][new_y].append(wolf)
        
        # �������� ������������� ����� � �����
        if wolf.points <= 0:
            # �������� ������� ����� � ������
            if wolf in grid[wolf.x][wolf.y]:
                # �������� ����� �� ������
                grid[wolf.x][wolf.y].remove(wolf)
            # �������� ������� ����� � ������
            if wolf in wolves_list:
                # �������� ����� �� ������
                wolves_list.remove(wolf)
    
    # ������� ����������� ����� � �������
    return grid, wolves_list, rabbits_list, she_wolves_list

# ������� ��� ���������� ������ ���� ���������
def run_simulation_step(grid, rabbits_list, wolves_list, she_wolves_list, N, M):
    # ��������� ��������� ������
    grid, wolves_list, rabbits_list, she_wolves_list = process_wolves(grid, wolves_list, rabbits_list, she_wolves_list, N, M)
    
    # ��������� ��������� ������
    grid, she_wolves_list, rabbits_list = process_she_wolves(grid, she_wolves_list, rabbits_list, N, M)
    
    # ��������� ��������� ��������
    grid, rabbits_list = process_rabbits(grid, rabbits_list, N, M)
    
    # ������� ����� � ����� ����
    grid, rabbits_list, wolves_list, she_wolves_list = clean_grid(grid, rabbits_list, wolves_list, she_wolves_list, N, M)
    
    # ������� ������������ ���������
    return grid, rabbits_list, wolves_list, she_wolves_list

# ������� ��� ���������� ������ ����� ��� �����������
def prepare_grid_data(grid, N, M):
    # �������� ����� 15x15 � ����������� ���������� None
    grid_data = [[None for i in range(15)] for i in range(15)]
    # ������ �� ������� ��������� ������� N x M
    for i in range(N):
        for j in range(M):
            # �������� ������� �������� � ������
            if grid[i][j]:
                # ��������� ������� ��������� � ������
                entity = grid[i][j][0]
                # �������� ���� ��������� (����)
                if isinstance(entity, Wolf):
                    # ��������� ���� � ����������� �����
                    grid_data[i][j] = '/static/images/wolf.png'
                # �������� ���� ��������� (�������)
                elif isinstance(entity, SheWolf):
                    # ��������� ���� � ����������� �������
                    grid_data[i][j] = '/static/images/she_wolf.png'
                # �������� ���� ��������� (������)
                elif isinstance(entity, Rabbit):
                    # ��������� ���� � ����������� �������
                    grid_data[i][j] = '/static/images/rabbit.png'
    # ������� �������������� ����� ������
    return grid_data

# ������� ��� ���������� ���������� ����� ���-���������
def wolf_island_controller(action, N_str, M_str, rabbits_str, wolves_str, she_wolves_str, steps_str):
    # ���������� ���������� ���������� simulation_state
    global simulation_state

    # �������� �������� �� ��������� �������� ��� �����
    if not action or action == 'reset':
        # ������� ��������� ���������
        simulation_state = {}
        # ������� ���������� ��������� ��������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': 15,
            'M': 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': '',
            'wolves': '',
            'she_wolves': '',
            'steps': '',
            'refresh': False,
            'error': ''
        }

    # �������� �������� �� ��������� ��������� ����������
    if action == 'generate':
        # ��������� ��������� �������� �����
        N = random.randint(5, 15)
        M = random.randint(5, 15)
        # ���������� ������������� ���������� ��������
        max_animals = (N * M) // 10
        # ��������� ��������� ��������� ��������
        rabbits = random.randint(1, max_animals)
        wolves = random.randint(1, max_animals)
        she_wolves = random.randint(1, max_animals)
        # ��������� ���������� ���������� �����
        steps = random.randint(10, 240)
        # ������� ��������� ���������
        simulation_state = {}
        # ���������� ��������������� ���������� � ��������� ��������� ��� ������������� ��������
        simulation_state = {
            'N': N,
            'M': M,
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves,
            'steps': steps
        }
        # �������� ������ ����� ��� �����������
        grid_data = [[None for i in range(15)] for i in range(15)]
        # ������������ ���������� � �������� ����������
        stats = {
            'step': 0,
            'rabbits': 0,
            'wolves': 0,
            'she_wolves': 0
        }
        # ������� ���������� ��������� � ������ ������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': grid_data,
            'stats': stats,
            'rabbits': rabbits,
            'wolves': wolves,
            'she_wolves': she_wolves,
            'steps': steps,
            'refresh': False,
            'error': ''
        }

    # ���������� ������� ������ ��� �������� � �����
    input_data = {
        'N': N_str if N_str else '15',
        'M': M_str if M_str else '15',
        'rabbits': rabbits_str,
        'wolves': wolves_str,
        'she_wolves': she_wolves_str,
        'steps': steps_str
    }

    # ��������� ��������� N
    try:
        # �������������� ������ N � ����� � ��������� �� ��������� 15
        N = int(N_str) if N_str else 15
        # �������� ����������� ��������� N
        if not (5 <= N <= 15):
            # ������� ���� N ��� ������
            input_data['N'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': 15,
                'M': int(input_data['M']) if input_data['M'] else 15,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of N. Must be an integer from 5 to 15.'
            }
    # ��������� ���������� ��� ������������ ������� N
    except ValueError:
        # ������� ���� N
        input_data['N'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': 15,
            'M': int(input_data['M']) if input_data['M'] else 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of N. Must be an integer from 5 to 15.'
        }

    # ��������� ��������� M
    try:
        # �������������� ������ M � �����
        M = int(M_str) if M_str else 15
        # �������� ����������� ��������� M
        if not (5 <= M <= 15):
            # ������� ���� M
            input_data['M'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': 15,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of M. Must be an integer from 5 to 15.'
            }
    # ��������� ���������� ��� ������������ ������� M
    except ValueError:
        # ������� ���� M
        input_data['M'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': 15,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of M. Must be an integer from 5 to 15.'
        }

    # ���������� ������������� ���������� ��������
    max_animals = (N * M) // 10
    # ��������� ���������� ��������
    try:
        # �������������� ������ �������� � �����
        rabbits = int(rabbits_str) if rabbits_str else 0
        # �������� ����������� ��������� ��������
        if rabbits_str and not (1 <= rabbits <= max_animals):
            # ������� ���� ��������
            input_data['rabbits'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of rabbits. Must be an integer from 1 to {max_animals}.'
            }
    # ��������� ���������� ��� ������������ �������
    except ValueError:
        # ������� ���� ��������
        input_data['rabbits'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of rabbits. Must be an integer from 1 to {max_animals}.'
        }

    # ��������� ���������� ������
    try:
        # �������������� ������ ������ � �����
        wolves = int(wolves_str) if wolves_str else 0
        # �������� ����������� ��������� ������
        if wolves_str and not (1 <= wolves <= max_animals):
            # ������� ���� ������
            input_data['wolves'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of wolves. Must be an integer from 1 to {max_animals}.'
            }
    # ��������� ���������� ��� ������������ �������
    except ValueError:
        # ������� ���� ������
        input_data['wolves'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of wolves. Must be an integer from 1 to {max_animals}.'
        }

    # ��������� ���������� ������
    try:
        # �������������� ������ ������ � �����
        she_wolves = int(she_wolves_str) if she_wolves_str else 0
        # �������� ����������� ��������� ������
        if she_wolves_str and not (1 <= she_wolves <= max_animals):
            # ������� ���� ������
            input_data['she_wolves'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': f'Incorrect value of she-wolves. Must be an integer from 1 to {max_animals}.'
            }
    # ��������� ���������� ��� ������������ �������
    except ValueError:
        # ������� ���� ������
        input_data['she_wolves'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': f'Incorrect value of she-wolves. Must be an integer from 1 to {max_animals}.'
        }

    # ��������� ���������� �����
    try:
        # �������������� ������ ����� � �����
        steps = int(steps_str) if steps_str else 0
        # �������� ����������� ��������� �����
        if steps_str and not (10 <= steps <= 240):
            # ������� ���� �����
            input_data['steps'] = ''
            # ������� ��������� � �������
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'Incorrect value of steps. Must be an integer from 10 to 240.'
            }
    # ��������� ���������� ��� ������������ �������
    except ValueError:
        # ������� ���� �����
        input_data['steps'] = ''
        # ������� ��������� � �������
        return {
            'title': 'The model of movement and death',
            'year': datetime.now().year,
            'N': N,
            'M': M,
            'grid_data': [[None for i in range(15)] for i in range(15)],
            'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
            'rabbits': input_data['rabbits'],
            'wolves': input_data['wolves'],
            'she_wolves': input_data['she_wolves'],
            'steps': input_data['steps'],
            'refresh': False,
            'error': 'Incorrect value of steps. Must be an integer from 10 to 240.'
        }

# �������� ������� ������� ���������
    if action == 'start' and not simulation_state.get('running'):
        # �������� ���������� ���� �����
        if not (rabbits and wolves and she_wolves and steps):
            return {
                'title': 'The model of movement and death',
                'year': datetime.now().year,
                'N': N,
                'M': M,
                'grid_data': [[None for i in range(15)] for i in range(15)],
                'stats': {'step': 0, 'rabbits': 0, 'wolves': 0, 'she_wolves': 0},
                'rabbits': input_data['rabbits'],
                'wolves': input_data['wolves'],
                'she_wolves': input_data['she_wolves'],
                'steps': input_data['steps'],
                'refresh': False,
                'error': 'All fields must be filled to start the simulation.'
            }
        # ������������� ��������� ���������
        simulation_state = {
            'N': N,
            'M': M,
            'steps': steps,
            'current_step': 0,
            'running': True,
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves
        }
        # ������������� ���������
        grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, rabbits, wolves, she_wolves)
        # ���������� ��������� ����� � �������
        simulation_state['grid'] = grid
        simulation_state['rabbits_list'] = rabbits_list
        simulation_state['wolves_list'] = wolves_list
        simulation_state['she_wolves_list'] = she_wolves_list
    # �������� ��������� ���������
    elif not simulation_state.get('running'):
        # ���������� ��������� �������� ��������
        simulation_state = {
            'initial_rabbits': rabbits,
            'initial_wolves': wolves,
            'initial_she_wolves': she_wolves
        }
        # ������������� ��������� ��� �������
        grid, rabbits_list, wolves_list, she_wolves_list = initialize_simulation(N, M, rabbits, wolves, she_wolves)
    # ��������� �������������� ���������
    else:
        # ���������� ���������� �� ���������
        N = simulation_state['N']
        M = simulation_state['M']
        steps = simulation_state['steps']
        current_step = simulation_state['current_step']
        grid = simulation_state['grid']
        rabbits_list = simulation_state['rabbits_list']
        wolves_list = simulation_state['wolves_list']
        she_wolves_list = simulation_state['she_wolves_list']
        rabbits = simulation_state['initial_rabbits']
        wolves = simulation_state['initial_wolves']
        she_wolves = simulation_state['initial_she_wolves']

        # �������� ���������� �����
        if current_step < steps:
            # ���������� ���� ���������
            grid, rabbits_list, wolves_list, she_wolves_list = run_simulation_step(
                grid, rabbits_list, wolves_list, she_wolves_list, N, M
            )
            # ���������� �������� �����
            simulation_state['current_step'] += 1
            # ���������� ���������
            simulation_state['grid'] = grid
            simulation_state['rabbits_list'] = rabbits_list
            simulation_state['wolves_list'] = wolves_list
            simulation_state['she_wolves_list'] = she_wolves_list
            
            # �������� �� ��������� ���� ��������
            if not rabbits_list and not wolves_list and not she_wolves_list:
                simulation_state['running'] = False
                simulation_state['extinction'] = True
        # ��������� ���������� ��������� �� �����
        else:
            # ��������� ���������
            simulation_state['running'] = False

    # ������������ ���������� �������� ���������
    stats = {
        'step': simulation_state.get('current_step', 0),
        'rabbits': len(simulation_state.get('rabbits_list', [])),
        'wolves': len(simulation_state.get('wolves_list', [])),
        'she_wolves': len(simulation_state.get('she_wolves_list', []))
    }
    # ���������� ������ ����� ��� �����������
    grid_data = prepare_grid_data(grid, N, M)

    # ����������� ��������� � ��������� ���������
    error_message = ''
    if simulation_state.get('extinction', False):
        error_message = 'All animals have died out, simulation stopped'
    elif not simulation_state.get('running', False) and simulation_state.get('current_step', 0) >= steps:
        error_message = 'Simulation completed'

    # ������� �������� ��������� ���������
    return {
        'title': 'The model of movement and death',
        'year': datetime.now().year,
        'N': N,
        'M': M,
        'grid_data': grid_data,
        'stats': stats,
        'rabbits': input_data['rabbits'],
        'wolves': input_data['wolves'],
        'she_wolves': input_data['she_wolves'],
        'steps': input_data['steps'],
        'refresh': simulation_state.get('running', False),
        'error': error_message
    }