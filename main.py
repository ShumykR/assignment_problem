import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

class AssignmentProblemSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задача про призначення")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Створюємо таблицю для введення вартостей
        self.table = QTableWidget(self)
        self.table.setRowCount(5)  # Кількість працівників
        self.table.setColumnCount(5)  # Кількість завдань
        self.table.setHorizontalHeaderLabels([f"Завдання {i+1}" for i in range(5)])
        self.table.setVerticalHeaderLabels([f"Працівник {i+1}" for i in range(5)])
        
        self.layout.addWidget(self.table)

        # Додаємо тестові дані за замовчуванням
        self.set_default_data()

        # Кнопка для розв'язування задачі
        self.solve_button = QPushButton("Розв'язати задачу", self)
        self.solve_button.clicked.connect(self.solve_assignment_problem)
        self.layout.addWidget(self.solve_button)

        self.result_label = QTableWidget(self)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def set_default_data(self):
        # Тестові дані (матриця вартостей)
        default_data = [
            [5, 9, 1, 7, 8],
            [3, 6, 2, 4, 10],
            [4, 9, 6, 2, 7],
            [8, 3, 7, 6, 5],
            [6, 4, 8, 10, 2]
        ]

        # Заповнюємо таблицю тестовими даними
        for i in range(5):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(str(default_data[i][j])))

    def solve_assignment_problem(self):
        # Зчитуємо дані з таблиці
        cost_matrix = []
        for i in range(5):
            row = []
            for j in range(5):
                item = self.table.item(i, j)
                if item is None:
                    row.append(0)
                else:
                    row.append(int(item.text()))
            cost_matrix.append(row)
        
        # Перетворюємо в NumPy масив
        cost_matrix = np.array(cost_matrix)

        # Етап І: Редукція рядків та стовпців
        # 1. Редукція рядків
        for i in range(cost_matrix.shape[0]):
            min_val = np.min(cost_matrix[i])
            cost_matrix[i] -= min_val

        # 2. Редукція стовпців
        for j in range(cost_matrix.shape[1]):
            min_val = np.min(cost_matrix[:, j])
            cost_matrix[:, j] -= min_val

        # Етап ІІ: Пошук нулів і оптимізація
        row_mark = [-1] * cost_matrix.shape[0]
        col_mark = [-1] * cost_matrix.shape[1]
        
        def find_zero():
            for i in range(cost_matrix.shape[0]):
                for j in range(cost_matrix.shape[1]):
                    if cost_matrix[i, j] == 0 and row_mark[i] == -1 and col_mark[j] == -1:
                        row_mark[i] = j
                        col_mark[j] = i
                        return True
            return False

        while find_zero():
            pass  # Продовжуємо пошук до тих пір, поки всі нулі не будуть відмічені

        # Пошук для оптимального розв'язку, поки не знайдемо рішення
        result = [[""] * 5 for _ in range(5)]
        for i, j in zip(range(len(row_mark)), row_mark):
            if j != -1:
                result[i][j] = f"Призначено до {j+1}"

        # Виведення результату
        self.result_label.setRowCount(5)
        self.result_label.setColumnCount(5)
        for i in range(5):
            for j in range(5):
                self.result_label.setItem(i, j, QTableWidgetItem(result[i][j]))


if __name__ == "__main__":
    app = QApplication([])
    window = AssignmentProblemSolver()
    window.show()
    app.exec()
