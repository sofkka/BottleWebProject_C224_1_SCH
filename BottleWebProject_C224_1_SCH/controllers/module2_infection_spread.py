"""
Logic for the infection spread simulation page.
"""

from bottle import request, response
import json
import random
import time

class InfectionModel:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 0 - здоровая, 1 - заражённая, 2 - с иммунитетом
        self.initialize_grid()

    def initialize_grid(self):
        center = self.size // 2
        self.grid[center][center] = 1  # Начальное заражение в центре

    def spread_infection(self):
        new_grid = [row[:] for row in self.grid]
        for i in range(self.size):
            for j in range(self.size):
                # Заражённые клетки могут стать иммунными с вероятностью 30%
                if self.grid[i][j] == 1 and random.random() < 0.3:
                    new_grid[i][j] = 2  # Становится иммунной
                # Заражение соседних клеток
                elif self.grid[i][j] == 1:
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni][nj] == 0:
                            new_grid[ni][nj] = 1  # Заражение здоровой клетки
        self.grid = new_grid

    def get_grid_state(self):
        return self.grid

# Глобальные переменные
model = None

def get_initial_data():
    """Returns the initial data for rendering the page."""
    global model
    size = request.GET.get('size', '9')
    try:
        size = int(size)
        if size % 2 == 0 or size < 3 or size > 15:
            size = 3
    except ValueError:
        size = 3

    # Обновляем модель, если размер изменился
    if model is None or model.size != size:
        model = InfectionModel(size)

    return {
        'size': size,
        'grid': model.get_grid_state()
    }

def stream_simulation():
    """Stream updates to the client using Server-Sent Events."""
    global model
    size = request.GET.get('size', '3')
    try:
        size = int(size)
        if size % 2 == 0 or size < 3 or size > 15:
            size = 3
    except ValueError:
        size = 3

    # Обновляем модель, если размер изменился
    if model is None or model.size != size:
        model = InfectionModel(size)

    # Настраиваем заголовки для SSE
    response.content_type = 'text/event-stream'
    response.cache_control = 'no-cache'
    response.set_header('Connection', 'keep-alive')

    while True:
        # Обновляем сетку (симуляция всегда активна)
        model.spread_infection()

        # Отправляем данные клиенту
        data = {
            'size': model.size,
            'grid': model.get_grid_state()
        }
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)  # Обновляем каждую секунду