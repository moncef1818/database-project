# New file: ui/enrollment_crud_view.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from db import enrollment_crud_queries


class EnrollmentView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        self.operations_menu = self.create_operations_menu()
        self.stack.addWidget(self.operations_menu)

        self.create_screen = self.create_create_screen()
        self.stack.addWidget(self.create_screen)

        self.read_screen = self.create_read_screen()
        self.stack.addWidget(self.read_screen)

        self.update_screen = self.create_update_screen()
        self.stack.addWidget(self.update_screen)

        self.delete_screen = self.create_delete_screen()
        self.stack.addWidget(self.delete_screen)

        self.stack.setCurrentIndex(0)

    def create_operations_menu(self):
        menu = QWidget()
        layout = QVBoxLayout(menu)

        title = QLabel("Enrollment Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nEnrollment")
        btn_read = QPushButton("View All\nEnrollments")
        btn_update = QPushButton("Update\nEnrollment")
        btn_delete = QPushButton("Delete\nEnrollment")
        btn_back = QPushButton("← Back to Core Data")

        for btn in [btn_create, btn_read, btn_update, btn_delete]:
            btn.setFixedSize(180, 120)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-size: 14px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
            )

        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )

        grid.addWidget(btn_create, 0, 0)
        grid.addWidget(btn_read, 0, 1)
        grid.addWidget(btn_update, 1, 0)
        grid.addWidget(btn_delete, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()
        layout.addWidget(btn_back)

        btn_create.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_read.clicked.connect(self.show_read_screen)
        btn_update.clicked.connect(self.show_update_screen)
        btn_delete.clicked.connect(self.show_delete_screen)

        return menu

    def create_create_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Create New Enrollment")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        self.create_student_id_input = QSpinBox()
        self.create_student_id_input.setMinimum(1)
        self.create_student_id_input.setMaximum(999999)

        self.create_course_id_input = QSpinBox()
        self.create_course_id_input.setMinimum(1)
        self.create_course_id_input.setMaximum(999999)

        self.create_department_id_input = QSpinBox()
        self.create_department_id_input.setMinimum(1)
        self.create_department_id_input.setMaximum(9999)

        self.create_semester_id_input = QSpinBox()
        self.create_semester_id_input.setMinimum(1)
        self.create_semester_id_input.setMaximum(9999)

        self.create_status_combo = QComboBox()
        self.create_status_combo.addItems(
            ["Enrolled", "Passed", "Failed", "Excluded", "Resit Eligible"]
        )

        form.addRow("Student ID:*", self.create_student_id_input)
        form.addRow("Course ID:*", self.create_course_id_input)
        form.addRow("Department ID:*", self.create_department_id_input)
        form.addRow("Semester ID:*", self.create_semester_id_input)
        form.addRow("Status:", self.create_status_combo)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Enrollment")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_save.clicked.connect(self.save_new_enrollment)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Enrollments")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(
            ["ID", "Student ID", "Course ID", "Department ID", "Semester ID", "Status"]
        )
        self.search_field_combo.setFixedWidth(120)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "ID (Asc)",
                "ID (Desc)",
                "Student ID (Asc)",
                "Student ID (Desc)",
                "Course ID (Asc)",
                "Course ID (Desc)",
                "Status (A-Z)",
                "Status (Z-A)",
            ]
        )

        btn_search = QPushButton("Search")
        btn_search.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px;"
        )
        btn_search.clicked.connect(self.perform_search)

        controls.addWidget(search_label)
        controls.addWidget(self.search_field_combo)
        controls.addWidget(search_input_label)
        controls.addWidget(self.search_input)
        controls.addWidget(sort_label)
        controls.addWidget(self.sort_combo)
        controls.addWidget(btn_search)

        layout.addLayout(controls)

        self.read_table = QTableWidget()
        self.read_table.setColumnCount(6)
        self.read_table.setHorizontalHeaderLabels(
            ["ID", "Student ID", "Course ID", "Dept ID", "Semester ID", "Status"]
        )
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.read_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("Back to Menu")
        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def create_update_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Update Enrollment")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(6)
        self.update_table.setHorizontalHeaderLabels(
            ["ID", "Student ID", "Course ID", "Dept ID", "Semester ID", "Status"]
        )
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()

        self.update_id_label = QLabel("Select an enrollment above")

        self.update_student_id_input = QSpinBox()
        self.update_student_id_input.setMinimum(1)
        self.update_student_id_input.setMaximum(999999)

        self.update_course_id_input = QSpinBox()
        self.update_course_id_input.setMinimum(1)
        self.update_course_id_input.setMaximum(999999)

        self.update_department_id_input = QSpinBox()
        self.update_department_id_input.setMinimum(1)
        self.update_department_id_input.setMaximum(9999)

        self.update_semester_id_input = QSpinBox()
        self.update_semester_id_input.setMinimum(1)
        self.update_semester_id_input.setMaximum(9999)

        self.update_status_combo = QComboBox()
        self.update_status_combo.addItems(
            ["Enrolled", "Passed", "Failed", "Excluded", "Resit Eligible"]
        )

        form.addRow("ID:", self.update_id_label)
        form.addRow("Student ID:*", self.update_student_id_input)
        form.addRow("Course ID:*", self.update_course_id_input)
        form.addRow("Department ID:*", self.update_department_id_input)
        form.addRow("Semester ID:*", self.update_semester_id_input)
        form.addRow("Status:", self.update_status_combo)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Enrollment")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_update.clicked.connect(self.update_enrollment)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Enrollment")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(6)
        self.delete_table.setHorizontalHeaderLabels(
            ["ID", "Student ID", "Course ID", "Dept ID", "Semester ID", "Status"]
        )
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")

        btn_delete.setStyleSheet(
            "background-color: #e74c3c; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_delete.clicked.connect(self.delete_enrollment)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def save_new_enrollment(self):
        student_id = self.create_student_id_input.value()
        course_id = self.create_course_id_input.value()
        department_id = self.create_department_id_input.value()
        semester_id = self.create_semester_id_input.value()
        status = self.create_status_combo.currentText()

        if not student_id or not course_id or not department_id or not semester_id:
            QMessageBox.warning(self, "Validation Error", "All IDs are required!")
            return

        success = enrollment_crud_queries.EnrollmentCRUD.create_enrollment(
            student_id, course_id, department_id, semester_id, status
        )
        if success:
            QMessageBox.information(self, "Success", "Enrollment created successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to create enrollment—check FK or unique constraints.",
            )

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = "enrollment_id", "ASC"
        elif sort_index == 1:
            sort_by, sort_order = "enrollment_id", "DESC"
        elif sort_index == 2:
            sort_by, sort_order = "student_id", "ASC"
        elif sort_index == 3:
            sort_by, sort_order = "student_id", "DESC"
        elif sort_index == 4:
            sort_by, sort_order = "course_id", "ASC"
        elif sort_index == 5:
            sort_by, sort_order = "course_id", "DESC"
        elif sort_index == 6:
            sort_by, sort_order = "status", "ASC"
        else:
            sort_by, sort_order = "status", "DESC"

        results = enrollment_crud_queries.EnrollmentCRUD.get_all_enrollments(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.read_table.setRowCount(len(results))
        for row_idx, enrollment in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(enrollment[0])))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(str(enrollment[1])))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(str(enrollment[2])))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(str(enrollment[3])))
            self.read_table.setItem(row_idx, 4, QTableWidgetItem(str(enrollment[4])))
            self.read_table.setItem(row_idx, 5, QTableWidgetItem(enrollment[5]))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        enrollment_id = int(self.update_table.item(row, 0).text())
        student_id = int(self.update_table.item(row, 1).text())
        course_id = int(self.update_table.item(row, 2).text())
        department_id = int(self.update_table.item(row, 3).text())
        semester_id = int(self.update_table.item(row, 4).text())
        status = self.update_table.item(row, 5).text()

        self.current_enrollment_id = enrollment_id
        self.update_id_label.setText(str(enrollment_id))
        self.update_student_id_input.setValue(student_id)
        self.update_course_id_input.setValue(course_id)
        self.update_department_id_input.setValue(department_id)
        self.update_semester_id_input.setValue(semester_id)
        self.update_status_combo.setCurrentText(status)

    def update_enrollment(self):
        if not hasattr(self, "current_enrollment_id"):
            QMessageBox.warning(
                self, "No Selection", "Please select an enrollment first!"
            )
            return

        student_id = self.update_student_id_input.value()
        course_id = self.update_course_id_input.value()
        department_id = self.update_department_id_input.value()
        semester_id = self.update_semester_id_input.value()
        status = self.update_status_combo.currentText()

        if not student_id or not course_id or not department_id or not semester_id:
            QMessageBox.warning(self, "Validation Error", "All IDs are required!")
            return

        success = enrollment_crud_queries.EnrollmentCRUD.update_enrollment(
            self.current_enrollment_id,
            student_id,
            course_id,
            department_id,
            semester_id,
            status,
        )
        if success:
            QMessageBox.information(self, "Success", "Enrollment updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to update enrollment—check FK or unique constraints.",
            )

    def delete_enrollment(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select an enrollment to delete!"
            )
            return

        row = selected[0].row()
        enrollment_id = int(self.delete_table.item(row, 0).text())
        student_id = self.delete_table.item(row, 1).text()
        course_id = self.delete_table.item(row, 2).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete Enrollment ID: {enrollment_id} (Student {student_id}, Course {course_id})?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success = enrollment_crud_queries.EnrollmentCRUD.delete_enrollment(
                enrollment_id
            )
            if success:
                QMessageBox.information(
                    self, "Success", "Enrollment deleted successfully!"
                )
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete enrollment!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = enrollment_crud_queries.EnrollmentCRUD.get_all_enrollments()
        self.update_table.setRowCount(len(results))
        for row_idx, enrollment in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(enrollment[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(str(enrollment[1])))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(enrollment[2])))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(str(enrollment[3])))
            self.update_table.setItem(row_idx, 4, QTableWidgetItem(str(enrollment[4])))
            self.update_table.setItem(row_idx, 5, QTableWidgetItem(enrollment[5]))

        self.update_id_label.setText("Select an enrollment above")
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = enrollment_crud_queries.EnrollmentCRUD.get_all_enrollments()
        self.delete_table.setRowCount(len(results))
        for row_idx, enrollment in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(enrollment[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(str(enrollment[1])))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(str(enrollment[2])))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(str(enrollment[3])))
            self.delete_table.setItem(row_idx, 4, QTableWidgetItem(str(enrollment[4])))
            self.delete_table.setItem(row_idx, 5, QTableWidgetItem(enrollment[5]))

        self.stack.setCurrentIndex(4)
