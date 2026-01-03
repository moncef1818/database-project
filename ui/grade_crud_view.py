# ui/grade_crud_view.py
# Purpose: Complete CRUD operations for Grade management

from db.grade_queries import GradeQueries
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDateEdit,
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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class GradeCrudView(QWidget):
    def __init__(self, parent=None):
        """
        Initializes Grade CRUD view with menu and operation pages.
        Args:
            parent: AcademicRecordsView reference
        """
        super().__init__(parent)
        self.selected_grade_id = None  # Stores selected grade ID for update/delete

        # Main layout with stacked pages
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Page setup (indexes: 0=menu, 1=create, 2=read, 3=update, 4=delete)
        self.menu_page = self.setup_menu_page()
        self.stack.addWidget(self.menu_page)

        self.create_page = self.setup_create_page()
        self.stack.addWidget(self.create_page)

        self.read_page = self.setup_read_page()
        self.stack.addWidget(self.read_page)

        self.update_page = self.setup_update_page()
        self.stack.addWidget(self.update_page)

        self.delete_page = self.setup_delete_page()
        self.stack.addWidget(self.delete_page)

        # Start with menu
        self.stack.setCurrentIndex(0)

    def setup_menu_page(self):
        """
        Creates the CRUD operations menu.
        Returns:
            QWidget: Menu page with action buttons
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Grade Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid for action buttons
        grid = QGridLayout()

        actions = [
            ("Add Grade", 0, 0, "#27ae60"),
            ("View Grades", 0, 1, "#3498db"),
            ("Update Grade", 1, 0, "#f39c12"),
            ("Delete Grade", 1, 1, "#e74c3c"),
        ]

        for name, row, col, color in actions:
            btn = QPushButton(name)
            btn.setFixedSize(150, 100)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)
            btn.clicked.connect(lambda checked, n=name: self.open_action(n))
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)
        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Academic Menu")
        btn_back.setStyleSheet("""
            background-color: #34495e;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """)
        btn_back.clicked.connect(self.go_back_to_academic_menu)
        layout.addWidget(btn_back)

        return page

    def open_action(self, action_name):
        """
        Routes to appropriate CRUD operation based on action name.
        Args:
            action_name: String identifying the action
        """
        if action_name == "Add Grade":
            self.load_create_combos()
            self.stack.setCurrentIndex(1)
        elif action_name == "View Grades":
            self.load_read_filters()  # Load semester filter
            self.load_grades()
            self.stack.setCurrentIndex(2)
        elif action_name == "Update Grade":
            self.load_update_combos()  # Load combos before showing
            self.load_read_filters()
            self.load_grades_for_update()
            self.stack.setCurrentIndex(3)
        elif action_name == "Delete Grade":
            self.load_grades_for_delete()
            self.stack.setCurrentIndex(4)

    def setup_create_page(self):
        """
        Creates the form page for adding new grades.
        Returns:
            QWidget: Create form page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Add New Grade")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Form layout
        form = QFormLayout()

        # Student dropdown
        self.student_combo = QComboBox()
        form.addRow("Student *:", self.student_combo)

        # Course dropdown
        self.course_combo = QComboBox()
        form.addRow("Course *:", self.course_combo)

        # Department ID
        self.department_spin = QSpinBox()
        self.department_spin.setMinimum(1)
        self.department_spin.setMaximum(999)
        form.addRow("Department ID *:", self.department_spin)

        # Exam dropdown (optional)
        self.exam_combo = QComboBox()
        form.addRow("Exam (optional):", self.exam_combo)

        # Semester dropdown
        self.semester_combo = QComboBox()
        form.addRow("Semester *:", self.semester_combo)

        # Grade type dropdown
        self.grade_type_combo = QComboBox()
        self.grade_type_combo.addItems([
            "Quiz", "Midterm", "Final", "Assignment",
            "Project", "Practical Test", "Homework",
            "Oral Exam", "Resit"
        ])
        form.addRow("Grade Type *:", self.grade_type_combo)

        # Grade date
        self.grade_date = QDateEdit()
        self.grade_date.setDate(QDate.currentDate())
        self.grade_date.setCalendarPopup(True)
        form.addRow("Grade Date *:", self.grade_date)

        # Grade source
        self.grade_source_combo = QComboBox()
        self.grade_source_combo.addItems(["Exam", "Other"])
        form.addRow("Grade Source *:", self.grade_source_combo)

        # Grade value
        self.grade_value_spin = QSpinBox()
        self.grade_value_spin.setMinimum(0)
        self.grade_value_spin.setMaximum(1000)
        form.addRow("Grade Value *:", self.grade_value_spin)

        # Max points
        self.max_points_spin = QSpinBox()
        self.max_points_spin.setMinimum(1)
        self.max_points_spin.setMaximum(1000)
        self.max_points_spin.setValue(20)  # Default to 20
        form.addRow("Max Points *:", self.max_points_spin)

        # Comments
        self.comments_text = QTextEdit()
        self.comments_text.setMaximumHeight(80)
        form.addRow("Comments:", self.comments_text)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_submit = QPushButton("✓ Add Grade")
        btn_submit.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        btn_submit.clicked.connect(self.submit_create)
        btn_layout.addWidget(btn_submit)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_back)

        layout.addLayout(btn_layout)

        return page

    def load_create_combos(self):
        """
        Populates dropdowns for create form from database.
        """
        # Load students
        students = GradeQueries.get_students()
        self.student_combo.clear()
        for student_id, name in students:
            self.student_combo.addItem(name, student_id)

        # Load courses
        courses = GradeQueries.get_courses()
        self.course_combo.clear()
        for course_id, name in courses:
            self.course_combo.addItem(name, course_id)

        # Load exams
        exams = GradeQueries.get_exams()
        self.exam_combo.clear()
        self.exam_combo.addItem("None", None)
        for exam_id, name in exams:
            self.exam_combo.addItem(name, exam_id)

        # Load semesters
        semesters = GradeQueries.get_semesters()
        self.semester_combo.clear()
        for semester_id, name in semesters:
            self.semester_combo.addItem(name, semester_id)

    def submit_create(self):
        """
        Validates form data and creates new grade record.
        """
        # Get form values
        student_id = self.student_combo.currentData()
        course_id = self.course_combo.currentData()
        department_id = self.department_spin.value()
        exam_id = self.exam_combo.currentData()
        semester_id = self.semester_combo.currentData()
        grade_type = self.grade_type_combo.currentText()
        grade_date = self.grade_date.date().toString("yyyy-MM-dd")
        grade_source = self.grade_source_combo.currentText()
        grade_value = self.grade_value_spin.value()
        max_points = self.max_points_spin.value()
        comments = self.comments_text.toPlainText().strip()

        # Validation checks
        if not all([student_id, course_id, department_id, semester_id, grade_type, grade_source]):
            QMessageBox.warning(
                self,
                "Validation Error",
                "All required fields (*) must be filled."
            )
            return

        if max_points <= 0:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Max Points must be greater than 0."
            )
            return

        if grade_value > max_points:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Grade Value cannot exceed Max Points."
            )
            return

        if grade_source == "Exam" and not exam_id:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Exam ID is required when Grade Source is 'Exam'."
            )
            return

        # Create grade in database
        new_id = GradeQueries.create_grade(
            student_id, course_id, department_id, exam_id, semester_id,
            grade_type, grade_date, grade_source, grade_value, max_points, comments
        )

        if new_id:
            QMessageBox.information(
                self,
                "Success",
                f"Grade added successfully with ID: {new_id}"
            )
            # Clear form
            self.grade_value_spin.setValue(0)
            self.comments_text.clear()
            # Go back to menu
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to add grade. Check database connection and logs."
            )

    def setup_read_page(self):
        """
        Creates the view page for displaying grades with filters.
        Returns:
            QWidget: Read page with table and filters
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("View Grades")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Search and filter controls
        filter_layout = QHBoxLayout()

        # Search input
        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Student name or course...")
        filter_layout.addWidget(self.search_input)

        # Semester filter
        filter_layout.addWidget(QLabel("Semester:"))
        self.filter_semester_combo = QComboBox()
        filter_layout.addWidget(self.filter_semester_combo)

        # Grade type filter
        filter_layout.addWidget(QLabel("Type:"))
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems([
            "All", "Quiz", "Midterm", "Final", "Assignment",
            "Project", "Practical Test", "Homework", "Oral Exam", "Resit"
        ])
        filter_layout.addWidget(self.filter_type_combo)

        # Search button
        btn_search = QPushButton("🔍 Search")
        btn_search.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_search.clicked.connect(self.load_grades)
        filter_layout.addWidget(btn_search)

        layout.addLayout(filter_layout)

        # Table for displaying grades
        self.grades_table = QTableWidget()
        self.grades_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.grades_table.setSelectionMode(QTableWidget.SingleSelection)
        self.grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.grades_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        layout.addWidget(self.grades_table)

        # Back button
        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def load_read_filters(self):
        """
        Populates semester filter dropdown.
        """
        semesters = GradeQueries.get_semesters()
        self.filter_semester_combo.clear()
        self.filter_semester_combo.addItem("All Semesters", None)
        for semester_id, name in semesters:
            self.filter_semester_combo.addItem(name, semester_id)

    def load_grades(self):
        """
        Loads grades into table based on search/filter criteria.
        Also calculates and displays weighted average.
        """
        # Get filter values
        search_term = self.search_input.text().strip()
        semester_id = self.filter_semester_combo.currentData()
        grade_type = self.filter_type_combo.currentText()

        # Fetch grades from database
        grades = GradeQueries.get_all_grades(search_term, semester_id, grade_type)

        # Setup table
        self.grades_table.setRowCount(len(grades))
        self.grades_table.setColumnCount(7)
        self.grades_table.setHorizontalHeaderLabels([
            "ID", "Student", "Course", "Type", "Value", "Max", "Weighted Avg"
        ])

        # Populate table
        for row_idx, grade in enumerate(grades):
            # grade tuple: (grade_id, student_name, course_name, grade_type, grade_value, max_points)
            for col_idx, value in enumerate(grade):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.grades_table.setItem(row_idx, col_idx, item)

            # Calculate and add weighted average
            grade_id = grade[0]
            avg = self.calculate_weighted_avg(grade_id)
            avg_item = QTableWidgetItem(f"{avg:.2f}")
            avg_item.setTextAlignment(Qt.AlignCenter)
            self.grades_table.setItem(row_idx, 6, avg_item)

        # Resize columns to content
        self.grades_table.resizeColumnsToContents()

        # Show message if no results
        if not grades:
            QMessageBox.information(
                self,
                "No Results",
                "No grades found matching your criteria."
            )
    def calculate_weighted_avg(self, grade_id):
        """
        Calculates weighted average for a student's course grades.
        Uses predefined weights for different grade types.

        Args:
            grade_id: ID of the grade record

        Returns:
            float: Weighted average (0-20 scale)
        """
        # Get full grade info
        full_grade = GradeQueries.get_grade_by_id(grade_id)
        if not full_grade:
            return 0.0

        student_id, course_id, department_id = full_grade[0], full_grade[1], full_grade[2]

        # Get all grades for this student/course combination
        grades = GradeQueries.get_grades_for_avg(student_id, course_id, department_id)
        if not grades:
            return 0.0

        # Define weights for each grade type
        weights = {
            "Quiz": 0.10,
            "Assignment": 0.10,
            "Homework": 0.05,
            "Project": 0.10,
            "Midterm": 0.30,
            "Final": 0.40,
            "Practical Test": 0.10,
            "Oral Exam": 0.15,
            "Resit": 0.40,
        }

        total_weighted = 0.0
        total_weight = 0.0

        # Calculate weighted sum
        for grade_type, value, max_points in grades:
            try:
                # 1. Convert DB values to float to handle Decimals or Strings safely
                val_float = float(value) if value is not None else 0.0
                max_float = float(max_points) if max_points is not None else 0.0
            except (ValueError, TypeError):
                continue  # Skip invalid data rows

            if max_float > 0:
                # 2. Normalize to 20-point scale using float values
                normalized = (val_float / max_float) * 20

                # 3. Get weight (default 0.0 if type not found)
                weight = weights.get(grade_type, 0.0)

                # 4. Perform calculation (now float * float, preventing TypeError)
                total_weighted += normalized * weight
                total_weight += weight

        # Return weighted average
        return (total_weighted / total_weight) if total_weight > 0 else 0.0
    def setup_update_page(self):
        """
        Creates the page for updating existing grades.
        Returns:
            QWidget: Update form page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Update Grade")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Instructions
        instructions = QLabel("Double-click a row in the table below to edit it")
        instructions.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(instructions)

        # Table for selecting grade to update
        self.update_table = QTableWidget()
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.setSelectionMode(QTableWidget.SingleSelection)
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.itemDoubleClicked.connect(self.pre_fill_update)
        layout.addWidget(self.update_table)

        # Update form (initially hidden)
        self.update_form_widget = QWidget()
        self.update_form = QFormLayout(self.update_form_widget)

        # Form fields (same as create)
        self.update_student_combo = QComboBox()
        self.update_form.addRow("Student *:", self.update_student_combo)

        self.update_course_combo = QComboBox()
        self.update_form.addRow("Course *:", self.update_course_combo)

        self.update_department_spin = QSpinBox()
        self.update_department_spin.setMinimum(1)
        self.update_department_spin.setMaximum(999)
        self.update_form.addRow("Department ID *:", self.update_department_spin)

        self.update_exam_combo = QComboBox()
        self.update_form.addRow("Exam (optional):", self.update_exam_combo)

        self.update_semester_combo = QComboBox()
        self.update_form.addRow("Semester *:", self.update_semester_combo)

        self.update_grade_type_combo = QComboBox()
        self.update_grade_type_combo.addItems([
            "Quiz", "Midterm", "Final", "Assignment",
            "Project", "Practical Test", "Homework",
            "Oral Exam", "Resit"
        ])
        self.update_form.addRow("Grade Type *:", self.update_grade_type_combo)

        self.update_grade_date = QDateEdit()
        self.update_grade_date.setCalendarPopup(True)
        self.update_form.addRow("Grade Date *:", self.update_grade_date)

        self.update_grade_source_combo = QComboBox()
        self.update_grade_source_combo.addItems(["Exam", "Other"])
        self.update_form.addRow("Grade Source *:", self.update_grade_source_combo)

        self.update_grade_value_spin = QSpinBox()
        self.update_grade_value_spin.setMinimum(0)
        self.update_grade_value_spin.setMaximum(1000)
        self.update_form.addRow("Grade Value *:", self.update_grade_value_spin)

        self.update_max_points_spin = QSpinBox()
        self.update_max_points_spin.setMinimum(1)
        self.update_max_points_spin.setMaximum(1000)
        self.update_form.addRow("Max Points *:", self.update_max_points_spin)

        self.update_comments_text = QTextEdit()
        self.update_comments_text.setMaximumHeight(80)
        self.update_form.addRow("Comments:", self.update_comments_text)

        self.update_form_widget.setVisible(False)  # Hidden until selection
        layout.addWidget(self.update_form_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_submit = QPushButton("✓ Update Grade")
        btn_submit.setStyleSheet("background-color: #f39c12; color: white; padding: 8px;")
        btn_submit.clicked.connect(self.submit_update)
        btn_layout.addWidget(btn_submit)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_back)

        layout.addLayout(btn_layout)

        return page

    def load_update_combos(self):
        """
        Populates dropdowns for update form.
        """
        # Load students
        students = GradeQueries.get_students()
        self.update_student_combo.clear()
        for student_id, name in students:
            self.update_student_combo.addItem(name, student_id)

        # Load courses
        courses = GradeQueries.get_courses()
        self.update_course_combo.clear()
        for course_id, name in courses:
            self.update_course_combo.addItem(name, course_id)

        # Load exams
        exams = GradeQueries.get_exams()
        self.update_exam_combo.clear()
        self.update_exam_combo.addItem("None", None)
        for exam_id, name in exams:
            self.update_exam_combo.addItem(name, exam_id)

        # Load semesters
        semesters = GradeQueries.get_semesters()
        self.update_semester_combo.clear()
        for semester_id, name in semesters:
            self.update_semester_combo.addItem(name, semester_id)

    def load_grades_for_update(self):
        """
        Loads grades into update table for selection.
        """
        # Get filter values
        search_term = self.search_input.text().strip()
        semester_id = self.filter_semester_combo.currentData()
        grade_type = self.filter_type_combo.currentText()

        # Fetch grades
        grades = GradeQueries.get_all_grades(search_term, semester_id, grade_type)

        # Setup table
        self.update_table.setRowCount(len(grades))
        self.update_table.setColumnCount(6)
        self.update_table.setHorizontalHeaderLabels([
            "ID", "Student", "Course", "Type", "Value", "Max Points"
        ])

        # Populate table
        for row_idx, grade in enumerate(grades):
            for col_idx, value in enumerate(grade):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.update_table.setItem(row_idx, col_idx, item)

        self.update_table.resizeColumnsToContents()

        if not grades:
            QMessageBox.information(
                self,
                "No Results",
                "No grades found. Add some grades first."
            )

    def pre_fill_update(self, item):
        """
        Pre-fills update form when a grade is selected from table.
        Args:
            item: Table item that was double-clicked
        """
        row = item.row()
        # Get grade ID from first column
        grade_id_item = self.update_table.item(row, 0)
        if not grade_id_item:
            return

        self.selected_grade_id = int(grade_id_item.text())

        # Fetch full grade details
        full_grade = GradeQueries.get_grade_by_id(self.selected_grade_id)
        if not full_grade:
            QMessageBox.warning(self, "Error", "Could not load grade details.")
            return

        # full_grade tuple: (student_id, course_id, department_id, exam_id, semester_id,
        #                    grade_type, grade_date, grade_source, grade_value, max_points, comments)

        # Pre-fill form fields
        self.update_student_combo.setCurrentIndex(
            self.update_student_combo.findData(full_grade[0])
        )
        self.update_course_combo.setCurrentIndex(
            self.update_course_combo.findData(full_grade[1])
        )
        self.update_department_spin.setValue(full_grade[2])

        # Handle None exam_id
        if full_grade[3]:
            self.update_exam_combo.setCurrentIndex(
                self.update_exam_combo.findData(full_grade[3])
            )
        else:
            self.update_exam_combo.setCurrentIndex(0)  # "None"

        self.update_semester_combo.setCurrentIndex(
            self.update_semester_combo.findData(full_grade[4])
        )
        self.update_grade_type_combo.setCurrentText(full_grade[5])
        self.update_grade_date.setDate(QDate.fromString(full_grade[6], "yyyy-MM-dd"))
        self.update_grade_source_combo.setCurrentText(full_grade[7])
        self.update_grade_value_spin.setValue(int(full_grade[8]))
        self.update_max_points_spin.setValue(int(full_grade[9]))
        self.update_comments_text.setText(full_grade[10] if full_grade[10] else "")

        # Show form
        self.update_form_widget.setVisible(True)

    def submit_update(self):
        """
        Validates and submits updated grade data.
        """
        if not self.selected_grade_id:
            QMessageBox.warning(self, "Error", "No grade selected for update.")
            return

        # Get form values
        student_id = self.update_student_combo.currentData()
        course_id = self.update_course_combo.currentData()
        department_id = self.update_department_spin.value()
        exam_id = self.update_exam_combo.currentData()
        semester_id = self.update_semester_combo.currentData()
        grade_type = self.update_grade_type_combo.currentText()
        grade_date = self.update_grade_date.date().toString("yyyy-MM-dd")
        grade_source = self.update_grade_source_combo.currentText()
        grade_value = self.update_grade_value_spin.value()
        max_points = self.update_max_points_spin.value()
        comments = self.update_comments_text.toPlainText().strip()

        # Validation
        if not all([student_id, course_id, department_id, semester_id, grade_type, grade_source]):
            QMessageBox.warning(self, "Validation Error", "All required fields must be filled.")
            return

        if max_points <= 0:
            QMessageBox.warning(self, "Validation Error", "Max Points must be greater than 0.")
            return

        if grade_value > max_points:
            QMessageBox.warning(self, "Validation Error", "Grade Value cannot exceed Max Points.")
            return

        if grade_source == "Exam" and not exam_id:
            QMessageBox.warning(self, "Validation Error", "Exam ID required for 'Exam' source.")
            return

        # Update in database
        success = GradeQueries.update_grade(
            self.selected_grade_id, student_id, course_id, department_id, exam_id,
            semester_id, grade_type, grade_date, grade_source, grade_value, max_points, comments
        )

        if success:
            QMessageBox.information(self, "Success", "Grade updated successfully.")
            self.update_form_widget.setVisible(False)
            self.load_grades_for_update()  # Refresh table
        else:
            QMessageBox.critical(self, "Error", "Failed to update grade.")

    def setup_delete_page(self):
        """
        Creates the page for deleting grades.
        Returns:
            QWidget: Delete confirmation page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Delete Grade")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Warning
        warning = QLabel("⚠️ Select a grade and click Delete. This action cannot be undone!")
        warning.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(warning)

        # Table for displaying grades
        self.delete_table = QTableWidget()
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.delete_table.setSelectionMode(QTableWidget.SingleSelection)
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.delete_table)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_delete = QPushButton("🗑️ Delete Selected")
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        btn_delete.clicked.connect(self.confirm_delete)
        btn_layout.addWidget(btn_delete)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_back)

        layout.addLayout(btn_layout)

        return page

    def load_grades_for_delete(self):
        """
        Loads grades into delete table.
        """
        # Fetch all grades (no filters for delete)
        grades = GradeQueries.get_all_grades("", None, "All")

        # Setup table
        self.delete_table.setRowCount(len(grades))
        self.delete_table.setColumnCount(6)
        self.delete_table.setHorizontalHeaderLabels([
            "ID", "Student", "Course", "Type", "Value", "Max Points"
        ])

        # Populate table
        for row_idx, grade in enumerate(grades):
            for col_idx, value in enumerate(grade):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.delete_table.setItem(row_idx, col_idx, item)

        self.delete_table.resizeColumnsToContents()

        if not grades:
            QMessageBox.information(self, "No Data", "No grades found in database.")

    def confirm_delete(self):
        """
        Confirms deletion and removes selected grade.
        """
        # Get selected row
        selected_items = self.delete_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a grade to delete.")
            return

        # Get grade ID from first column of selected row
        row = selected_items[0].row()
        grade_id_item = self.delete_table.item(row, 0)
        grade_id = int(grade_id_item.text())

        # Get student and course names for confirmation
        student_name = self.delete_table.item(row, 1).text()
        course_name = self.delete_table.item(row, 2).text()

        # Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete this grade?\n\n"
            f"Student: {student_name}\n"
            f"Course: {course_name}\n\n"
            f"This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Delete from database
            success = GradeQueries.delete_grade(grade_id)

            if success:
                QMessageBox.information(self, "Success", "Grade deleted successfully.")
                self.load_grades_for_delete()  # Refresh table
            else:
                QMessageBox.critical(self, "Error", "Failed to delete grade.")

    def go_back_to_academic_menu(self):
        """
        Returns to the Academic Records menu.
        """
        if self.parent():
            self.parent().show_menu()
