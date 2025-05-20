// Объявляются константы и переменные для управления данными симуляции и её состоянием, получаемые из глобальных переменных.

// Массив состояний сетки для каждого шага симуляции, где каждое состояние
// представляет двумерный массив объектов с полями 'state'('H', 'I', 'R') и 'timer'.
const steps = window.simulationSteps;

// Хранит размер сетки.
const size = window.gridSize;

// Финальное состояние сетки после всех шагов симуляции
// Используется для продолжения симуляции, если достигнуто максимальное количество шагов.
const finalGrid = window.finalGridState;

// Здоровы ли все клетки в финальной сетке ('H').
const allHealthy = window.allCellsHealthy;

// Переменные для отслеживания текущего состояния симуляции.
let stepIndex = 0, intervalId = null, startTime = null, timerInterval = null, elapsedTime = 0;

// Функция для визуального рендеринга сетки на основе текущего шага симуляции.
function updateGrid() {
    // Получается состояние сетки для текущего stepIndex из массива steps.
    const grid = steps[stepIndex];

    // Получается DOM-элемент, который служит контейнером для визуализации сетки.
    const cont = document.getElementById('grid');

    // Очищается весь существующий контент контейнера сетки для подготовки к рендерингу нового состояния.
    cont.innerHTML = '';

    // Проходим по каждой строке сетки.
    for (let i = 0; i < size; i++) {
        // Новый элемент div для представления строки в сетке.
        const row = document.createElement('div');

        // Присваивается класс 'grid-row'.
        row.className = 'grid-row';

        // Производится итерация по каждому столбцу в текущей строке.
        for (let j = 0; j < size; j++) {
            // Новый элемент div для представления отдельной клетки в сетке.
            const cell = document.createElement('div');

            // Присваивается базовый класс 'grid-cell' для каждой клетки.
            cell.className = 'grid-cell';

            // Добавляется класс 'infected', если состояние клетки равно 'I' (заражённая).
            if (grid[i][j].state === 'I') {
                cell.className += ' infected';
            }
            // Добавляется класс 'immune', если состояние клетки равно 'R' (иммунная).
            else if (grid[i][j].state === 'R') {
                cell.className += ' immune';
            }
            // Здоровые клетки ('H') не получают дополнительных классов, сохраняя стандартный вид.
            else { }

            // Добавляется элемент клетки в текущую строку.
            row.appendChild(cell);
        }

        // Добавляется элемент строки в контейнер сетки.
        cont.appendChild(row);
    }
}

// Функция для обновления и отображения прошедшего времени симуляции.
function updateTimer() {
    // Проверяется, запущена ли симуляция.
    if (startTime) {
        // Рассчитывается прошедшее время в секундах с момента начала текущего сегмента симуляции.
        const currentElapsed = Math.floor((Date.now() - startTime) / 1000);

        // Общее время равно сумме накопленного elapsedTime и текущего сегмента.
        const totalElapsed = elapsedTime + currentElapsed;

        // Вычисляются минуты и секунды из общего прошедшего времени.
        const minutes = Math.floor(totalElapsed / 60).toString().padStart(2, '0');
        const seconds = (totalElapsed % 60).toString().padStart(2, '0');

        // Обновляется текстовое содержимое элемента таймера с отформатированным временем (MM:SS).
        document.getElementById('timer').textContent = `${minutes}:${seconds}`;
    }
}

// Функция для перехода к следующему шагу симуляции и обновления отображения.
function nextStep() {
    // Проверяется наличие шагов для отображения - что симуляция не пытается обратиться к шагу за пределами массива.
    if (stepIndex < steps.length - 1) {
        // Увеличивается stepIndex для перехода к следующему шагу симуляции.
        stepIndex++;

        // Вызывается updateGrid для рендеринга нового состояния сетки в DOM.
        updateGrid();
    } else {
        // Выполняется в конце симуляции - останавливается интервал анимации для остановки симуляции.
        clearInterval(intervalId);

        // Сбрасывается intervalId в null, указывая, что симуляция не активна.
        intervalId = null;

        // Обновляется текст кнопки Start, позволяя пользователю перезапустить симуляцию.
        document.getElementById('start-button').textContent = 'Start';

        // Скрывается кнопка Reset, устанавливая её стиль display в 'none', так как симуляция завершена.
        document.getElementById('reset-button').style.display = 'none';

        // Останавливается таймер, очищая интервал обновления.
        clearInterval(timerInterval);
        timerInterval = null;

        // Проверяется, здоровы ли все клетки в финальной сетке.
        // Если да, отображается сообщение о завершении для информирования пользователя.
        if (allHealthy) {
            document.getElementById('simulation-message').style.display = 'block';
        }
    }
}

// Слушатель событий кнопки Start/Stop для управления началом и остановкой симуляции.
document.getElementById('start-button').addEventListener('click', () => {
    // Вывод данных в консоль
    console.log('Button Start/Stop', { intervalId, stepIndex });

    // Проверяется, запущена ли симуляция в данный момент.
    if (intervalId) {
        // Останавливается симуляция, очищая активный интервал.
        clearInterval(intervalId);

        // Сбрасывается intervalId в null - симуляция остановлена.
        intervalId = null;

        // Обновляется текст кнопки Start на 'Start', указывая, что симуляцию можно перезапустить.
        document.getElementById('start-button').textContent = 'Start';

        // Скрывается кнопка Reset, так как она актуальна только во время активной симуляции.
        document.getElementById('reset-button').style.display = 'none';

        // Останавливается таймер, очищая интервал обновления.
        clearInterval(timerInterval);
        timerInterval = null;

        // Сохраняется текущее значение таймера в elapsedTime, исключая время паузы - сбрасывается startTime.
        elapsedTime += Math.floor((Date.now() - startTime) / 1000);
        startTime = null;
    } else {
        // Когда симуляция не запущена, нужно понять - начинать, сбрасывать или продолжать.
        if (allHealthy && stepIndex >= steps.length - 1) {
            // Инициируется новая симуляция с одной заражённой клеткой в центре.
            window.location.href = `/infection_spread?size=${size}`;

          // Проверяется, достигнут ли последний шаг, но не все клетки здоровы.
        } else if (stepIndex >= steps.length - 1) {
            // Кодируется finalGrid как строка JSON и включается в URL как параметр continue_from.
            window.location.href = `/infection_spread?size=${size}&continue_from=${encodeURIComponent(JSON.stringify(finalGrid))}`;
        } else {
            // Запускается новый цикл симуляции, если остались шаги для отображения.
            // Устанавливается интервал для вызова nextStep каждые 1000 миллисекунд (1 секунда) для анимации.
            intervalId = setInterval(nextStep, 1000);

            // Если startTime не установлен, фиксируется текущее время как начало.
            // Если установлен, корректируется с учётом elapsedTime для продолжения с последнего значения.
            if (!startTime) startTime = Date.now();
            else startTime = Date.now() - (elapsedTime * 1000);

            // Запускается таймер, устанавливая интервал для обновления отображения каждые 1000 миллисекунд (1 секунда).
            timerInterval = setInterval(updateTimer, 1000);

            // Обновляется текст кнопки Start на 'Stop', указывая, что повторный клик приостановит симуляцию.
            document.getElementById('start-button').textContent = 'Stop';

            // Отображается кнопка Reset, позволяя пользователю перезапустить симуляцию во время её выполнения.
            document.getElementById('reset-button').style.display = 'block';

            // Скрывается сообщение о завершении симуляции, чтобы избежать путаницы во время её работы.
            document.getElementById('simulation-message').style.display = 'none';
        }
    }
});

// Слушатель событий кнопки Reset для обработки запросов на сброс симуляции.
document.getElementById('reset-button').addEventListener('click', () => {
    // Перенаправляется браузер на тот же маршрут с текущим размером сетки для начала новой симуляции.
    window.location.href = `/infection_spread?size=${size}`;
});

// Слушатель событий кнопки Save to JSON для обработки сохранения текущего состояния сетки.
document.getElementById('save-button').addEventListener('click', () => {
    // Получаем текущий шаг симуляции из глобальной переменной
    const currentStep = stepIndex;

    // Получаем текущее состояние сетки из массива steps по индексу текущего шага
    const currentGrid = steps[currentStep];

    // Отправляем POST-запрос на сервер с параметрами
    fetch(`/infection_spread?size=${size}&continue_from=${encodeURIComponent(JSON.stringify(currentGrid))}&save=true&step=${currentStep}`)
        // Обрабатываем ответ от сервера как текстовые данные
        .then(response => response.text())
        // Выводим сообщение от сервера в alert
        .then(() => {
            // Success message in English
            alert('Data successfully saved to JSON!');
        })
        .catch(error => {
            // Enhanced error message
            console.error('Save error:', error);
            alert('Failed to save data. Please check console for details.');
        });
});

// Слушатель событий ползунка размера сетки для обработки изменений размера и обновления отображаемого значения в реальном времени.
document.getElementById('field-size').addEventListener('input', e => {
    // Обеспечивает немедленную обратную связь при перемещении ползунка пользователем.
    document.getElementById('field-value').textContent = e.target.value;

    // Перенаправляется браузер на тот же маршрут с новым размером сетки, выбранным пользователем.
    window.location.href = `/infection_spread?size=${e.target.value}`;
});

// Инициализируется отображение сетки при загрузке страницы.
// Гарантируется, что начальное состояние сетки видно сразу после рендеринга страницы.
updateGrid();
