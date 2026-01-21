from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from db import results_queries  # Import the database query class


class Report_analytics(QWidget):


    def __init__(self, parent=None):

        super().__init__(parent)
        self.current_query = None  # Tracks which query is active (a-j)
        self.initUI()

    def initUI(self):

        main_layout = QVBoxLayout(self)

        # Stacked widget allows switching between menu and results
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Create both screens
        self.operations_menu = self.create_operations_menu()
        self.stack.addWidget(self.operations_menu)

        self.result_screen = self.create_result_screen()
        self.stack.addWidget(self.result_screen)

        # Start with menu visible
        self.stack.setCurrentIndex(0)

    def create_operations_menu(self):

        menu = QWidget()
        layout = QVBoxLayout(menu)

        # Title
        title = QLabel("Report analytics ")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid layout for buttons
        grid = QGridLayout()

        # Define all query buttons with their grid positions
        buttons = [
            ("a) Students by Group", 0, 0),
            ("b) Students by Section", 0, 1),
            ("c) Instructor Timetable", 1, 0),
            ("d) Student Timetable by Section/Group", 1, 1),
            ("e) Students Passed Semester", 2, 0),
            ("f) Disqualifying Marks by Module", 2, 1),
            ("g) Average Marks by Course/Group", 3, 0),
            ("h) Students Failing Module", 3, 1),
            ("i) Students Eligible for Resit", 4, 0),
            ("j) Students Excluded from Module", 4, 1),
        ]

        # Create and configure each button
        for name, row, col in buttons:
            btn = QPushButton(name)
            btn.setFixedSize(250, 80)  # Fixed size for uniform grid
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-size: 12px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
            )
            # Lambda captures button name to pass to show_result()
            btn.clicked.connect(lambda checked, n=name: self.show_result(n))
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)
        layout.addStretch()

        # Back button to main menu
        btn_back = QPushButton("← Back to Main")
        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )
        btn_back.clicked.connect(lambda: self.parent().content_stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return menu

    def create_result_screen(self):
        """
        Builds the results screen with dynamic parameter form and table.

        Components:
        - Title (updated per query)
        - Parameter form (dynamically populated)
        - Run Query button
        - Results table (auto-populated from DB)
        - Back to Menu button

            """
        screen = QWidget()
        layout = QVBoxLayout(screen)

        # Dynamic title
        self.result_title = QLabel("Query Results")
        self.result_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.result_title)

        # Parameter form (dynamically populated in show_result())
        self.param_form = QFormLayout()

        # Pre-create all possible input widgets (shown/hidden based on query)
        self.course_id_input = QSpinBox()
        self.course_id_input.setMinimum(0)
        self.course_id_input.setMaximum(9999)

        self.department_id_input = QSpinBox()
        self.department_id_input.setMinimum(0)
        self.department_id_input.setMaximum(9999)

        self.semester_id_input = QSpinBox()
        self.semester_id_input.setMinimum(0)
        self.semester_id_input.setMaximum(9999)

        self.group_id_input = QSpinBox()
        self.group_id_input.setMinimum(0)
        self.group_id_input.setMaximum(9999)

        self.section_id_input = QSpinBox()
        self.section_id_input.setMinimum(0)
        self.section_id_input.setMaximum(9999)

        self.instructor_id_input = QSpinBox()
        self.instructor_id_input.setMinimum(0)
        self.instructor_id_input.setMaximum(9999)

        layout.addLayout(self.param_form)

        # Run Query button
        btn_run = QPushButton("Run Query")
        btn_run.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_run.clicked.connect(self.run_query)
        layout.addWidget(btn_run)

        # Results table
        self.result_table = QTableWidget()
        # Auto-resize columns to fit content
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Allow selecting entire rows
        self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.result_table)

        # Back button
        btn_back = QPushButton("Back to Menu")
        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def show_result(self, query_name):

        # Extract query identifier (first letter: a-j)
        self.current_query = query_name.lower()[0]
        self.result_title.setText(query_name)

        # CLEAR PREVIOUS TABLE DATA - This was missing!
        self.result_table.setRowCount(0)  # Remove all rows
        self.result_table.setColumnCount(0)  # Remove all columns
        self.result_table.clear()  # Clear any remaining data

        # Clear parameter form safely
        while self.param_form.count():
            child = self.param_form.takeAt(0)
            if child.widget():
                child.widget().setParent(None)  # Detach widget without deleting

        # Add parameters based on query requirements
        # Query a: get_student_by_group(group_id)
        if self.current_query == "a":
            self.param_form.addRow("Group ID (optional):", self.group_id_input)

        # Query b: get_students_by_section(section_id)
        elif self.current_query == "b":
            self.param_form.addRow("Section ID (optional):", self.section_id_input)

        # Query c: get_instructor_timetable(instructor_id)
        elif self.current_query == "c":
            self.param_form.addRow("Instructor ID:", self.instructor_id_input)

        # Query d: get_student_timetable_by_section_group(section_id, group_id)
        elif self.current_query == "d":
            self.param_form.addRow("Section ID (optional):", self.section_id_input)
            self.param_form.addRow("Group ID (optional):", self.group_id_input)

        # Query e: get_student_passed_semester(semester_id)
        elif self.current_query == "e":
            self.param_form.addRow("Semester ID:", self.semester_id_input)

        # Query f: get_disqualifying_marks_by_module(course_id, department_id)
        elif self.current_query == "f":
            self.param_form.addRow("Course ID:", self.course_id_input)
            self.param_form.addRow("Department ID:", self.department_id_input)

        # Query g: get_average_marks_by_course_group(course_id, department_id)
        elif self.current_query == "g":
            self.param_form.addRow("Course ID:", self.course_id_input)
            self.param_form.addRow("Department ID:", self.department_id_input)

        # Query h: get_students_failing_module(course_id, department_id)
        elif self.current_query == "h":
            self.param_form.addRow("Course ID:", self.course_id_input)
            self.param_form.addRow("Department ID:", self.department_id_input)

        # Query i: get_students_resit_eligible(course_id, department_id)
        elif self.current_query == "i":
            self.param_form.addRow("Course ID:", self.course_id_input)
            self.param_form.addRow("Department ID:", self.department_id_input)

        # Query j: get_students_excluded_from_module(course_id, department_id)
        elif self.current_query == "j":
            self.param_form.addRow("Course ID:", self.course_id_input)
            self.param_form.addRow("Department ID:", self.department_id_input)

        # Switch to results screen
        self.stack.setCurrentIndex(1)

    def run_query(self):

        # Map query identifiers to SQL function names
        function_map = {
            "a": "get_student_by_group",
            "b": "get_students_by_section",
            "c": "get_instructor_timetable",
            "d": "get_student_timetable_by_section_group",
            "e": "get_student_passed_semester",
            "f": "get_disqualifying_marks_by_module",
            "g": "get_average_marks_by_course_group",
            "h": "get_students_failing_module",
            "i": "get_students_resit_eligible",
            "j": "get_students_excluded_from_module",
        }

        # Get SQL function name for current query
        function_name = function_map.get(self.current_query)
        if not function_name:
            QMessageBox.critical(self, "Error", "Invalid query selected!")
            return

        # Collect parameters based on query requirements
        params = []

        if self.current_query == "a":
            # get_student_by_group(group_id)
            params.append(self.group_id_input.value() or None)

        elif self.current_query == "b":
            # get_students_by_section(section_id)
            params.append(self.section_id_input.value() or None)

        elif self.current_query == "c":
            # get_instructor_timetable(instructor_id)
            params.append(self.instructor_id_input.value())

        elif self.current_query == "d":
            # get_student_timetable_by_section_group(section_id, group_id)
            params.append(self.section_id_input.value() or None)
            params.append(self.group_id_input.value() or None)

        elif self.current_query == "e":
            # get_student_passed_semester(semester_id)
            params.append(self.semester_id_input.value())

        elif self.current_query in ["f", "g", "h", "i", "j"]:
            # All require (course_id, department_id)
            params.append(self.course_id_input.value())
            params.append(self.department_id_input.value())

        # Execute query and get results
        results, columns = results_queries.ResultsQueries.execute_function(
            function_name, tuple(params)
        )

        # Handle empty results
        if not results:
            QMessageBox.information(
                self,
                "No Results",
                "No data found for these parameters. Try different values.",
            )
            return

        # Populate table with results
        self.result_table.setColumnCount(len(columns))
        self.result_table.setRowCount(len(results))
        self.result_table.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                # Convert None to empty string for display
                display_value = str(value) if value is not None else ""
                self.result_table.setItem(
                    row_idx, col_idx, QTableWidgetItem(display_value)
                )

        # Reset all input fields to 0 for better UX
        self.course_id_input.setValue(0)
        self.department_id_input.setValue(0)
        self.semester_id_input.setValue(0)
        self.group_id_input.setValue(0)
        self.section_id_input.setValue(0)
        self.instructor_id_input.setValue(0)
