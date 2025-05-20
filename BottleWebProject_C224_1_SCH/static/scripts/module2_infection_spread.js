// ����������� ��������� � ���������� ��� ���������� ������� ��������� � � ����������, ���������� �� ���������� ����������.

// ������ ��������� ����� ��� ������� ���� ���������, ��� ������ ���������
// ������������ ��������� ������ �������� � ������ 'state'('H', 'I', 'R') � 'timer'.
const steps = window.simulationSteps;

// ������ ������ �����.
const size = window.gridSize;

// ��������� ��������� ����� ����� ���� ����� ���������
// ������������ ��� ����������� ���������, ���� ���������� ������������ ���������� �����.
const finalGrid = window.finalGridState;

// ������� �� ��� ������ � ��������� ����� ('H').
const allHealthy = window.allCellsHealthy;

// ���������� ��� ������������ �������� ��������� ���������.
let stepIndex = 0, intervalId = null, startTime = null, timerInterval = null, elapsedTime = 0;

// ������� ��� ����������� ���������� ����� �� ������ �������� ���� ���������.
function updateGrid() {
    // ���������� ��������� ����� ��� �������� stepIndex �� ������� steps.
    const grid = steps[stepIndex];

    // ���������� DOM-�������, ������� ������ ����������� ��� ������������ �����.
    const cont = document.getElementById('grid');

    // ��������� ���� ������������ ������� ���������� ����� ��� ���������� � ���������� ������ ���������.
    cont.innerHTML = '';

    // �������� �� ������ ������ �����.
    for (let i = 0; i < size; i++) {
        // ����� ������� div ��� ������������� ������ � �����.
        const row = document.createElement('div');

        // ������������� ����� 'grid-row'.
        row.className = 'grid-row';

        // ������������ �������� �� ������� ������� � ������� ������.
        for (let j = 0; j < size; j++) {
            // ����� ������� div ��� ������������� ��������� ������ � �����.
            const cell = document.createElement('div');

            // ������������� ������� ����� 'grid-cell' ��� ������ ������.
            cell.className = 'grid-cell';

            // ����������� ����� 'infected', ���� ��������� ������ ����� 'I' (���������).
            if (grid[i][j].state === 'I') {
                cell.className += ' infected';
            }
            // ����������� ����� 'immune', ���� ��������� ������ ����� 'R' (��������).
            else if (grid[i][j].state === 'R') {
                cell.className += ' immune';
            }
            // �������� ������ ('H') �� �������� �������������� �������, �������� ����������� ���.
            else { }

            // ����������� ������� ������ � ������� ������.
            row.appendChild(cell);
        }

        // ����������� ������� ������ � ��������� �����.
        cont.appendChild(row);
    }
}

// ������� ��� ���������� � ����������� ���������� ������� ���������.
function updateTimer() {
    // �����������, �������� �� ���������.
    if (startTime) {
        // �������������� ��������� ����� � �������� � ������� ������ �������� �������� ���������.
        const currentElapsed = Math.floor((Date.now() - startTime) / 1000);

        // ����� ����� ����� ����� ������������ elapsedTime � �������� ��������.
        const totalElapsed = elapsedTime + currentElapsed;

        // ����������� ������ � ������� �� ������ ���������� �������.
        const minutes = Math.floor(totalElapsed / 60).toString().padStart(2, '0');
        const seconds = (totalElapsed % 60).toString().padStart(2, '0');

        // ����������� ��������� ���������� �������� ������� � ����������������� �������� (MM:SS).
        document.getElementById('timer').textContent = `${minutes}:${seconds}`;
    }
}

// ������� ��� �������� � ���������� ���� ��������� � ���������� �����������.
function nextStep() {
    // ����������� ������� ����� ��� ����������� - ��� ��������� �� �������� ���������� � ���� �� ��������� �������.
    if (stepIndex < steps.length - 1) {
        // ������������� stepIndex ��� �������� � ���������� ���� ���������.
        stepIndex++;

        // ���������� updateGrid ��� ���������� ������ ��������� ����� � DOM.
        updateGrid();
    } else {
        // ����������� � ����� ��������� - ��������������� �������� �������� ��� ��������� ���������.
        clearInterval(intervalId);

        // ������������ intervalId � null, ��������, ��� ��������� �� �������.
        intervalId = null;

        // ����������� ����� ������ Start, �������� ������������ ������������� ���������.
        document.getElementById('start-button').textContent = 'Start';

        // ���������� ������ Reset, ������������ � ����� display � 'none', ��� ��� ��������� ���������.
        document.getElementById('reset-button').style.display = 'none';

        // ��������������� ������, ������ �������� ����������.
        clearInterval(timerInterval);
        timerInterval = null;

        // �����������, ������� �� ��� ������ � ��������� �����.
        // ���� ��, ������������ ��������� � ���������� ��� �������������� ������������.
        if (allHealthy) {
            document.getElementById('simulation-message').style.display = 'block';
        }
    }
}

// ��������� ������� ������ Start/Stop ��� ���������� ������� � ���������� ���������.
document.getElementById('start-button').addEventListener('click', () => {
    // ����� ������ � �������
    console.log('Button Start/Stop', { intervalId, stepIndex });

    // �����������, �������� �� ��������� � ������ ������.
    if (intervalId) {
        // ��������������� ���������, ������ �������� ��������.
        clearInterval(intervalId);

        // ������������ intervalId � null - ��������� �����������.
        intervalId = null;

        // ����������� ����� ������ Start �� 'Start', ��������, ��� ��������� ����� �������������.
        document.getElementById('start-button').textContent = 'Start';

        // ���������� ������ Reset, ��� ��� ��� ��������� ������ �� ����� �������� ���������.
        document.getElementById('reset-button').style.display = 'none';

        // ��������������� ������, ������ �������� ����������.
        clearInterval(timerInterval);
        timerInterval = null;

        // ����������� ������� �������� ������� � elapsedTime, �������� ����� ����� - ������������ startTime.
        elapsedTime += Math.floor((Date.now() - startTime) / 1000);
        startTime = null;
    } else {
        // ����� ��������� �� ��������, ����� ������ - ��������, ���������� ��� ����������.
        if (allHealthy && stepIndex >= steps.length - 1) {
            // ������������ ����� ��������� � ����� ��������� ������� � ������.
            window.location.href = `/infection_spread?size=${size}`;

          // �����������, ��������� �� ��������� ���, �� �� ��� ������ �������.
        } else if (stepIndex >= steps.length - 1) {
            // ���������� finalGrid ��� ������ JSON � ���������� � URL ��� �������� continue_from.
            window.location.href = `/infection_spread?size=${size}&continue_from=${encodeURIComponent(JSON.stringify(finalGrid))}`;
        } else {
            // ����������� ����� ���� ���������, ���� �������� ���� ��� �����������.
            // ��������������� �������� ��� ������ nextStep ������ 1000 ����������� (1 �������) ��� ��������.
            intervalId = setInterval(nextStep, 1000);

            // ���� startTime �� ����������, ����������� ������� ����� ��� ������.
            // ���� ����������, �������������� � ������ elapsedTime ��� ����������� � ���������� ��������.
            if (!startTime) startTime = Date.now();
            else startTime = Date.now() - (elapsedTime * 1000);

            // ����������� ������, ������������ �������� ��� ���������� ����������� ������ 1000 ����������� (1 �������).
            timerInterval = setInterval(updateTimer, 1000);

            // ����������� ����� ������ Start �� 'Stop', ��������, ��� ��������� ���� ������������ ���������.
            document.getElementById('start-button').textContent = 'Stop';

            // ������������ ������ Reset, �������� ������������ ������������� ��������� �� ����� � ����������.
            document.getElementById('reset-button').style.display = 'block';

            // ���������� ��������� � ���������� ���������, ����� �������� �������� �� ����� � ������.
            document.getElementById('simulation-message').style.display = 'none';
        }
    }
});

// ��������� ������� ������ Reset ��� ��������� �������� �� ����� ���������.
document.getElementById('reset-button').addEventListener('click', () => {
    // ���������������� ������� �� ��� �� ������� � ������� �������� ����� ��� ������ ����� ���������.
    window.location.href = `/infection_spread?size=${size}`;
});

// ��������� ������� ������ Save to JSON ��� ��������� ���������� �������� ��������� �����.
document.getElementById('save-button').addEventListener('click', () => {
    // �������� ������� ��� ��������� �� ���������� ����������
    const currentStep = stepIndex;

    // �������� ������� ��������� ����� �� ������� steps �� ������� �������� ����
    const currentGrid = steps[currentStep];

    // ���������� POST-������ �� ������ � �����������
    fetch(`/infection_spread?size=${size}&continue_from=${encodeURIComponent(JSON.stringify(currentGrid))}&save=true&step=${currentStep}`)
        // ������������ ����� �� ������� ��� ��������� ������
        .then(response => response.text())
        // ������� ��������� �� ������� � alert
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

// ��������� ������� �������� ������� ����� ��� ��������� ��������� ������� � ���������� ������������� �������� � �������� �������.
document.getElementById('field-size').addEventListener('input', e => {
    // ������������ ����������� �������� ����� ��� ����������� �������� �������������.
    document.getElementById('field-value').textContent = e.target.value;

    // ���������������� ������� �� ��� �� ������� � ����� �������� �����, ��������� �������������.
    window.location.href = `/infection_spread?size=${e.target.value}`;
});

// ���������������� ����������� ����� ��� �������� ��������.
// �������������, ��� ��������� ��������� ����� ����� ����� ����� ���������� ��������.
updateGrid();
