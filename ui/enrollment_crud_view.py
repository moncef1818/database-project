# Cleaned file: ui/enrollment_crud_view.py
# NO UPDATE OPERATION - Only Create, Read, Delete
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

        # Only 3 screens: Menu, Create, Read, Delete
        self.operations_menu = self.create_operations_menu()
        self.stack.addWidget(self.operations_menu)

        self.create_screen = self.create_create_screen()
        self.stack.addWidget(self.create_screen)

        self.read_screen = self.create_read_screen()
        self.stack.addWidget(self.read_screen)

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

        info = QLabel(
            "⚠️ Note: Enrollments cannot be updated. To change, delete and create new."
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "color: #e67e22; padding: 10px; background: #fef5e7; border-radius: 5px; margin: 10px;"
        )
        layout.addWidget(info)

        grid = QGridLayout()

        btn_create = QPushButton("📝 Create New\nEnrollment")
        btn_read = QPushButton("👁️ View All\nEnrollments")
        btn_delete = QPushButton("🗑️ Delete\nEnrollment")

        for btn in [btn_create, btn_read, btn_delete]:
            btn.setFixedSize(200, 120)
            btn.setStyleSheet(
                """
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 10px;
                }
            """
            )

        grid.addWidget(btn_create, 0, 0)
        grid.addWidget(btn_read, 0, 1)
        grid.addWidget(btn_delete, 1, 0, 1, 2)  # Delete spans 2 columns

        layout.addLayout(grid)
        layout.addStretch()

        btn_create.clicked.connect(self.show_create_screen)
        btn_read.clicked.connect(self.show_read_screen)
        btn_delete.clicked.connect(self.show_delete_screen)

        return menu

    def create_create_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Create New Enrollment")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        # Dropdowns
        self.create_student_combo = QComboBox()
        self.create_department_combo = QComboBox()
        self.create_course_combo = QComboBox()
        self.create_semester_combo = QComboBox()
        self.create_status_combo = QComboBox()
        self.create_status_combo.addItems(
            ["Enrolled", "Passed", "Failed", "Excluded", "Resit Eligible"]
        )

        # Connect department change to update courses
        self.create_department_combo.currentIndexChanged.connect(
            self.load_courses_for_create
        )

        form.addRow("Student:*", self.create_student_combo)
        form.addRow("Department:*", self.create_department_combo)
        form.addRow("Course:*", self.create_course_combo)
        form.addRow("Semester:*", self.create_semester_combo)
        form.addRow("Status:", self.create_status_combo)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("💾 Save Enrollment")
        btn_cancel = QPushButton("❌ Cancel")

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
            [
                "ID",
                "Student ID",
                "Student Name",
                "Course Name",
                "Department Name",
                "Status",
            ]
        )

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "ID (Asc)",
                "ID (Desc)",
                "Student Name (A-Z)",
                "Student Name (Z-A)",
                "Course Name (A-Z)",
                "Course Name (Z-A)",
                "Status (A-Z)",
                "Status (Z-A)",
            ]
        )

        btn_search = QPushButton("🔍 Search")
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
        self.read_table.setColumnCount(10)
        self.read_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Student ID",
                "Student Name",
                "Course ID",
                "Course Name",
                "Dept ID",
                "Department",
                "Sem ID",
                "Semester",
                "Status",
            ]
        )
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.read_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("⬅️ Back to Menu")
        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Enrollment")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        warning = QLabel(
            "⚠️ Warning: Deleting an enrollment may also delete related grades and attendance records!"
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "color: #c0392b; padding: 10px; background: #fadbd8; border-radius: 5px;"
        )
        layout.addWidget(warning)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(10)
        self.delete_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Student ID",
                "Student Name",
                "Course ID",
                "Course Name",
                "Dept ID",
                "Department",
                "Sem ID",
                "Semester",
                "Status",
            ]
        )
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("🗑️ Delete Selected")
        btn_cancel = QPushButton("⬅️ Cancel")

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

    # ==================== HELPER FUNCTIONS ====================

    def populate_table(self, table, results):
        """Fill table with enrollment data"""
        table.setRowCount(len(results))
        for row_idx, enrollment in enumerate(results):
            for col_idx in range(10):
                value = (
                    str(enrollment[col_idx]) if enrollment[col_idx] is not None else ""
                )
                table.setItem(row_idx, col_idx, QTableWidgetItem(value))

    def load_dropdowns_for_create(self):
        """Load all dropdowns for CREATE screen"""
        # Students
        students = enrollment_crud_queries.EnrollmentCRUD.get_students_for_dropdown()
        self.create_student_combo.clear()
        for student_id, name in students:
            self.create_student_combo.addItem(f"{name} (ID: {student_id})", student_id)

        # Departments
        departments = (
            enrollment_crud_queries.EnrollmentCRUD.get_departments_for_dropdown()
        )
        self.create_department_combo.clear()
        for dept_id, name in departments:
            self.create_department_combo.addItem(f"{name} (ID: {dept_id})", dept_id)

        # Semesters
        semesters = enrollment_crud_queries.EnrollmentCRUD.get_semesters_for_dropdown()
        self.create_semester_combo.clear()
        for sem_id, name in semesters:
            self.create_semester_combo.addItem(f"{name} (ID: {sem_id})", sem_id)

        # Courses (empty until department selected)
        self.create_course_combo.clear()
        self.create_course_combo.addItem("Select department first", None)

    def load_courses_for_create(self):
        """Update courses when department changes"""
        dept_id = self.create_department_combo.currentData()
        self.create_course_combo.clear()

        if dept_id:
            courses = enrollment_crud_queries.EnrollmentCRUD.get_courses_for_dropdown(
                dept_id
            )
            for course_id, name, dept_id in courses:
                self.create_course_combo.addItem(
                    f"{name} (ID: {course_id})", (course_id, dept_id)
                )
        else:
            self.create_course_combo.addItem("Select department first", None)

    # ==================== SCREEN SHOW FUNCTIONS ====================

    def show_create_screen(self):
        """Load dropdowns and show CREATE screen"""
        self.load_dropdowns_for_create()
        self.stack.setCurrentIndex(1)

    def show_read_screen(self):
        """Refresh data and show READ screen"""
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_delete_screen(self):
        """Refresh table and show DELETE screen"""
        results = enrollment_crud_queries.EnrollmentCRUD.get_all_enrollments()
        self.populate_table(self.delete_table, results)
        self.stack.setCurrentIndex(3)

    # ==================== CRUD OPERATIONS ====================

    def save_new_enrollment(self):
        """Save new enrollment to database"""
        student_id = self.create_student_combo.currentData()
        course_data = self.create_course_combo.currentData()
        department_id = self.create_department_combo.currentData()
        semester_id = self.create_semester_combo.currentData()
        status = self.create_status_combo.currentText()

        # Validation
        if not student_id or not course_data or not department_id or not semester_id:
            QMessageBox.warning(
                self, "Validation Error", "Please fill all required fields!"
            )
            return

        # Extract course_id
        course_id = course_data[0] if isinstance(course_data, tuple) else course_data

        # Save to database
        success = enrollment_crud_queries.EnrollmentCRUD.create_enrollment(
            student_id, course_id, department_id, semester_id, status
        )

        if success:
            QMessageBox.information(
                self, "Success", "✅ Enrollment created successfully!"
            )
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self,
                "Error",
                "❌ Failed to create enrollment. Check console for details.",
            )

    def perform_search(self):
        """Search/filter/sort enrollments"""
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        # Map sort dropdown to database columns
        sort_mappings = {
            0: ("enrollment_id", "ASC"),
            1: ("enrollment_id", "DESC"),
            2: ("student_name", "ASC"),
            3: ("student_name", "DESC"),
            4: ("course_name", "ASC"),
            5: ("course_name", "DESC"),
            6: ("status", "ASC"),
            7: ("status", "DESC"),
        }
        sort_by, sort_order = sort_mappings.get(
            self.sort_combo.currentIndex(), ("enrollment_id", "ASC")
        )

        # Get results
        results = enrollment_crud_queries.EnrollmentCRUD.get_all_enrollments(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        # Display
        self.populate_table(self.read_table, results)

    def delete_enrollment(self):
        """Delete selected enrollment"""
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select an enrollment to delete!"
            )
            return

        row = selected[0].row()
        enrollment_id = int(self.delete_table.item(row, 0).text())
        student_name = self.delete_table.item(row, 2).text()
        course_name = self.delete_table.item(row, 4).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"⚠️ Delete Enrollment ID {enrollment_id}?\n\n"
            f"Student: {student_name}\n"
            f"Course: {course_name}\n\n"
            f"This may also delete related grades and attendance!",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success = enrollment_crud_queries.EnrollmentCRUD.delete_enrollment(
                enrollment_id
            )
            if success:
                QMessageBox.information(
                    self, "Success", "✅ Enrollment deleted successfully!"
                )
                # REFRESH TABLE IMMEDIATELY
                self.show_delete_screen()
            else:
                QMessageBox.critical(self, "Error", "❌ Failed to delete enrollment!")
