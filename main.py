import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMessageBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout, QSpinBox, QDoubleSpinBox, QLabel, QStyle, QTableWidget, QPushButton, QTableWidgetItem
)

from PyQt5.QtGui import (
    QIcon,
)

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="javod",
    password="hHh(26Y2%C~w",
    database="student_management"
)
cursor = conn.cursor()


class StudentManagementApp(QWidget):
    name: QLineEdit
    age: QSpinBox
    year: QSpinBox
    scholarship: QDoubleSpinBox

    table: QTableWidget
    search_input: QLineEdit

    def __init__(self):
        super().__init__()

        try:
            self.init_ui()
        except Exception as exp:
            print(exp)

    def init_ui(self):
        self.setWindowTitle("Student Management System")
        self.setWindowIcon(QIcon("./student_management_system_logo.png"))

        v_layout = QVBoxLayout()

        self.name = QLineEdit(self)
        self.name.setPlaceholderText("Enter name")
        v_layout.addWidget(self.name)

        age_h_layout = QHBoxLayout()
        age_label = QLabel("Age:", self)
        age_h_layout.addWidget(age_label)
        self.age = QSpinBox(self)
        self.age.setRange(16, 60)
        self.age.setSingleStep(1)
        age_h_layout.addWidget(self.age)
        v_layout.addLayout(age_h_layout)

        year_h_layout = QHBoxLayout()
        year_label = QLabel("Educational Year:", self)
        year_h_layout.addWidget(year_label)
        self.year = QSpinBox(self)
        self.year.setRange(1, 4)
        self.year.setSingleStep(1)
        year_h_layout.addWidget(self.year)
        v_layout.addLayout(year_h_layout)

        scholarship_h_layout = QHBoxLayout()
        scholarship_label = QLabel("Scholarship:", self)
        scholarship_h_layout.addWidget(scholarship_label)
        self.scholarship = QDoubleSpinBox(self)
        self.scholarship.setRange(100, 1000)
        self.scholarship.setSingleStep(1)
        scholarship_h_layout.addWidget(self.scholarship)
        v_layout.addLayout(scholarship_h_layout)

        add_button = QPushButton("Add Student", self)
        add_button.clicked.connect(self.add_student)
        v_layout.addWidget(add_button)

        update_button = QPushButton("Update Selected Student", self)
        update_button.clicked.connect(self.update_student)
        v_layout.addWidget(update_button)

        delete_button = QPushButton("Delete Selected Student", self)
        delete_button.clicked.connect(self.delete_student)
        v_layout.addWidget(delete_button)
        v_layout.addWidget(delete_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Age",
            "Year",
            "Scholarship"
        ])
        self.table.cellClicked.connect(self.select_student)
        v_layout.addWidget(self.table)

        self.load_students()

        self.setStyleSheet(
            """
            QWidget {
                font-size: 20px;
            }
            """
        )

        # search by name
        search_h_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name")
        search_button = QPushButton("Search", self)
        search_button.clicked.connect(self.search_student)
        search_h_layout.addWidget(self.search_input)
        search_h_layout.addWidget(search_button)
        reset_button = QPushButton("Reset", self)
        reset_button.clicked.connect(self.reset_table)
        search_h_layout.addWidget(reset_button)
        v_layout.addLayout(search_h_layout)

        # DISTINCT aged employees
        h_layout = QHBoxLayout()
        distinct_button = QPushButton("Distinct aged students", self)
        distinct_button.clicked.connect(self.load_distinct_aged_students)
        h_layout.addWidget(distinct_button)
        salaries_sum_button = QPushButton("Sum of scholarships", self)
        salaries_sum_button.clicked.connect(self.show_scholarships_sum)
        h_layout.addWidget(salaries_sum_button)
        ne_button = QPushButton("Number of students", self)
        ne_button.clicked.connect(self.load_ns)
        h_layout.addWidget(ne_button)
        v_layout.addLayout(h_layout)

        h_2_layout = QHBoxLayout()
        asc_order_by_age_button = QPushButton("ORDER BY age ASC", self)
        asc_order_by_age_button.clicked.connect(self.asc_order_by_age)
        desc_order_by_age_button = QPushButton("ORDER BY age DESC", self)
        desc_order_by_age_button.clicked.connect(self.desc_order_by_age)
        h_2_layout.addWidget(asc_order_by_age_button)
        h_2_layout.addWidget(desc_order_by_age_button)
        v_layout.addLayout(h_2_layout)

        h_3_layout = QHBoxLayout()
        max_salary_button = QPushButton("MAX scholarship", self)
        max_salary_button.clicked.connect(self.max_scholarship)
        min_salary_button = QPushButton("MIN scholarship", self)
        min_salary_button.clicked.connect(self.min_scholarship)
        h_3_layout.addWidget(max_salary_button)
        h_3_layout.addWidget(min_salary_button)
        v_layout.addLayout(h_3_layout)

        self.setLayout(v_layout)

    def min_scholarship(self):
        cursor.execute("SELECT MIN(scholarship) FROM student")
        result = cursor.fetchone()
        min_scholarship = result[0] if result[0] is not None else 0
        QMessageBox.information(self, "MIN scholarship",
                                f"MIN scholarship is {min_scholarship}.")

    def max_scholarship(self):
        cursor.execute("SELECT MAX(scholarship) FROM student")
        result = cursor.fetchone()
        max_scholarship = result[0] if result[0] is not None else 0
        QMessageBox.information(self, "MAX scholarship",
                                f"MAX scholarship is {max_scholarship}.")

    def desc_order_by_age(self):
        self.table.setRowCount(0)  # birinchi
        # navbatda table-ni clear qilish
        cursor.execute("SELECT id, name, age, year, scholarship FROM student ORDER BY age DESC")
        for row_idx, (employee_id, name, age, year, scholarship) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(employee_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(age)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(scholarship)))

    def asc_order_by_age(self):
        self.table.setRowCount(0)  # birinchi
        # navbatda table-ni clear qilish
        cursor.execute("SELECT id, name, age, year, scholarship FROM student ORDER BY age ASC")
        for row_idx, (employee_id, name, age, year, scholarship) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(employee_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(age)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(scholarship)))

    def load_ns(self):
        cursor.execute("SELECT COUNT(*) FROM student")
        result = cursor.fetchone()
        count = result[0] if result[0] is not None else 0
        QMessageBox.information(self, "Number of students",
                                f"The total number of students is {count}.")

    def show_scholarships_sum(self):
        cursor.execute("SELECT SUM(scholarship) FROM student")
        result = cursor.fetchone()
        scholarships_sum = result[0] if result[0] is not None else 0
        QMessageBox.information(self, "Sum of scholarships",
                                f"The total sum of scholarships is {scholarships_sum}.")

    def load_distinct_aged_students(self):
        self.table.setRowCount(0)
        cursor.execute("SELECT DISTINCT age FROM student")
        for row_idx, age in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(age[0])))

    def reset_table(self):
        self.search_input.clear()
        self.load_students()

    def search_student(self):
        search_name = self.search_input.text()
        if search_name:
            query = ("SELECT id, name, age, year, scholarship FROM student WHERE name LIKE %s")
            cursor.execute(query, ('%' + search_name + '%',))
            self.table.setRowCount(0)
            for row_idx, (student_id, name, age, year, scholarship) in enumerate(cursor.fetchall()):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0,
                                   QTableWidgetItem(str(student_id)))
                self.table.setItem(row_idx, 1,
                                   QTableWidgetItem(name))
                self.table.setItem(row_idx, 2,
                                   QTableWidgetItem(str(age)))
                self.table.setItem(row_idx, 3,
                                   QTableWidgetItem(str(year)))
                self.table.setItem(row_idx, 4,
                                   QTableWidgetItem(str(scholarship)))
        else:
            self.load_students()

    def delete_student(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            student_id = int(self.table.item(selected_row, 0).text())
            cursor.execute("DELETE FROM student WHERE id=%s", (student_id,))
            conn.commit()
            self.load_students()
            self.name.clear()
            self.age.clear()
            self.year.clear()
            self.scholarship.clear()

    def update_student(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            student_id = int(self.table.item(selected_row, 0).text())
            new_name = self.name.text()
            new_age = int(self.age.text())
            new_year = int(self.year.text())
            new_scholarship = float(self.scholarship.text().replace(',', '.'))

            if new_name and new_age and new_year and new_scholarship:
                cursor.execute(
                    "UPDATE student SET name=%s, age=%s, year=%s, scholarship=%s WHERE id=%s",
                    (new_name, new_age, new_year, new_scholarship, student_id)
                )
                conn.commit()
                self.name.clear()
                self.age.clear()
                self.year.clear()
                self.scholarship.clear()
                self.load_students()

    def load_students(self):
        self.table.setRowCount(0)
        cursor.execute("SELECT * FROM student")
        for row_idx, (student_id, name, age, year, scholarship) in enumerate(cursor.fetchall()):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(student_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(age)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(year)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(scholarship)))

    def select_student(self, row, column):
        student_id = int(self.table.item(row, 0).text())
        cursor.execute("SELECT LENGTH(name) FROM student WHERE id=%s", (student_id,))
        result = cursor.fetchone()
        length = result[0] if result[0] is not None else 0
        name = self.table.item(row, 1).text()
        QMessageBox.information(self,
                                f"Length",
                                f"Length of {name} is {length}.")
        age = self.table.item(row, 2).text()
        year = self.table.item(row, 3).text()
        scholarship = self.table.item(row, 4).text()

        self.name.setText(name)
        self.age.setValue(int(age))
        self.year.setValue(int(year))
        self.scholarship.setValue(float(scholarship))

    def add_student(self):
        name = self.name.text()
        age = int(self.age.text())
        year = int(self.year.text())
        scholarship = float(self.scholarship.text().replace(',', '.'))

        if name and age and year and scholarship:
            cursor.execute(
                "INSERT INTO student (name, age, year, scholarship) VALUES (%s, %s, %s, %s)",
                (name, age, year, scholarship)
            )
            conn.commit()
            self.name.clear()
            self.age.clear()
            self.year.clear()
            self.scholarship.clear()
            self.load_students()


def main():
    app = QApplication(sys.argv)
    window = StudentManagementApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
