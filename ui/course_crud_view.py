# New file: ui/course_crud_view.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QFormLayout,
    QMessageBox,
    QHeaderView,
    QComboBox,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from db import course_crud_queries


class CourseView(QWidget):
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

        title = QLabel("Course Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nCourse")
        btn_read = QPushButton("View All\nCourses")
        btn_update = QPushButton("Update\nCourse")
        btn_delete = QPushButton("Delete\nCourse")
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

        title = QLabel("Create New Course")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        self.create_department_combo = QComboBox()
        self.load_departments_combo(self.create_department_combo)

        self.create_name_input = QLineEdit()
        self.create_name_input.setPlaceholderText("e.g., Database Systems")
        self.create_name_input.setMaxLength(60)

        self.create_description_input = QTextEdit()
        self.create_description_input.setPlaceholderText(
            "Course description and learning objectives..."
        )
        self.create_description_input.setMaximumHeight(150)

        form.addRow("Department:*", self.create_department_combo)
        form.addRow("Course Name:*", self.create_name_input)
        form.addRow("Description:", self.create_description_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Course")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_save.clicked.connect(self.save_new_course)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Courses")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(
            ["Course ID", "Department ID", "Course Name", "Department Name"]
        )
        self.search_field_combo.setFixedWidth(130)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "Course ID (Asc)",
                "Course ID (Desc)",
                "Course Name (A-Z)",
                "Course Name (Z-A)",
                "Department (A-Z)",
                "Department (Z-A)",
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
        self.read_table.setColumnCount(5)
        self.read_table.setHorizontalHeaderLabels(
            ["Course ID", "Dept ID", "Department", "Course Name", "Description"]
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

        title = QLabel("Update Course")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(5)
        self.update_table.setHorizontalHeaderLabels(
            ["Course ID", "Dept ID", "Department", "Course Name", "Description"]
        )
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()

        self.update_id_label = QLabel("Select a course above")

        self.update_department_combo = QComboBox()
        self.load_departments_combo(self.update_department_combo)

        self.update_name_input = QLineEdit()
        self.update_name_input.setMaxLength(60)

        self.update_description_input = QTextEdit()
        self.update_description_input.setMaximumHeight(150)

        form.addRow("Course ID:", self.update_id_label)
        form.addRow("Department:*", self.update_department_combo)
        form.addRow("Course Name:*", self.update_name_input)
        form.addRow("Description:", self.update_description_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Course")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_update.clicked.connect(self.update_course)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Course")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(5)
        self.delete_table.setHorizontalHeaderLabels(
            ["Course ID", "Dept ID", "Department", "Course Name", "Description"]
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

        btn_delete.clicked.connect(self.delete_course)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def load_departments_combo(self, combo):
        """Load departments into combo box"""
        combo.clear()
        departments = course_crud_queries.CourseCRUD.get_all_departments()
        for dept_id, dept_name in departments:
            combo.addItem(f"{dept_name} (ID: {dept_id})", dept_id)

    def save_new_course(self):
        department_id = self.create_department_combo.currentData()
        name = self.create_name_input.text().strip()
        description = self.create_description_input.toPlainText().strip() or None

        if not department_id or not name:
            QMessageBox.warning(
                self, "Validation Error", "Department and Course Name are required!"
            )
            return

        success = course_crud_queries.CourseCRUD.create_course(
            department_id, name, description
        )
        if success:
            QMessageBox.information(self, "Success", "Course created successfully!")
            self.create_name_input.clear()
            self.create_description_input.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self, "Error", "Failed to create course—check DB constraints."
            )

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = "course_id", "ASC"
        elif sort_index == 1:
            sort_by, sort_order = "course_id", "DESC"
        elif sort_index == 2:
            sort_by, sort_order = "name", "ASC"
        elif sort_index == 3:
            sort_by, sort_order = "name", "DESC"
        elif sort_index == 4:
            sort_by, sort_order = "dept_name", "ASC"
        else:
            sort_by, sort_order = "dept_name", "DESC"

        results = course_crud_queries.CourseCRUD.get_all_courses(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.read_table.setRowCount(len(results))
        for row_idx, course in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(course[0])))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(str(course[1])))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(course[2] or ""))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(course[3]))
            self.read_table.setItem(row_idx, 4, QTableWidgetItem(course[4] or ""))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        course_id = int(self.update_table.item(row, 0).text())
        department_id = int(self.update_table.item(row, 1).text())
        name = self.update_table.item(row, 3).text()
        description = self.update_table.item(row, 4).text()

        self.current_course_id = course_id
        self.current_department_id = department_id
        self.update_id_label.setText(str(course_id))

        # Set department combo
        for i in range(self.update_department_combo.count()):
            if self.update_department_combo.itemData(i) == department_id:
                self.update_department_combo.setCurrentIndex(i)
                break

        self.update_name_input.setText(name)
        self.update_description_input.setPlainText(description)

    def update_course(self):
        if not hasattr(self, "current_course_id"):
            QMessageBox.warning(self, "No Selection", "Please select a course first!")
            return

        department_id = self.update_department_combo.currentData()
        name = self.update_name_input.text().strip()
        description = self.update_description_input.toPlainText().strip() or None

        if not department_id or not name:
            QMessageBox.warning(
                self, "Validation Error", "Department and Course Name are required!"
            )
            return

        success = course_crud_queries.CourseCRUD.update_course(
            self.current_course_id, department_id, name, description
        )
        if success:
            QMessageBox.information(self, "Success", "Course updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update course!")

    def delete_course(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select a course to delete!"
            )
            return

        row = selected[0].row()
        course_id = int(self.delete_table.item(row, 0).text())
        department_id = int(self.delete_table.item(row, 1).text())
        course_name = self.delete_table.item(row, 3).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{course_name}' (ID: {course_id})?\n\n"
            f"Warning: This will also delete all related activities, enrollments, and exams!",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success = course_crud_queries.CourseCRUD.delete_course(
                course_id, department_id
            )
            if success:
                QMessageBox.information(self, "Success", "Course deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete course!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = course_crud_queries.CourseCRUD.get_all_courses()
        self.update_table.setRowCount(len(results))
        for row_idx, course in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(course[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(str(course[1])))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(course[2] or ""))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(course[3]))
            self.update_table.setItem(row_idx, 4, QTableWidgetItem(course[4] or ""))

        self.update_id_label.setText("Select a course above")
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = course_crud_queries.CourseCRUD.get_all_courses()
        self.delete_table.setRowCount(len(results))
        for row_idx, course in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(course[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(str(course[1])))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(course[2] or ""))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(course[3]))
            self.delete_table.setItem(row_idx, 4, QTableWidgetItem(course[4] or ""))

        self.stack.setCurrentIndex(4)
