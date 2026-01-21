# Display student status reports (Passed, Failed, Resit, Excluded)


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
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

from db.results_queries import ResultsQueries


class StudentStatusReportsView(QWidget):
    def __init__(self, parent=None, results_parent=None):

        super().__init__(parent)
        self.results_parent = results_parent

        # Main layout
        self.layout = QVBoxLayout(self)


        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Report pages
        self.passed_page = self.create_report_page("Passed Students", "passed")
        self.stack.addWidget(self.passed_page)

        self.failed_page = self.create_report_page("Failed Students", "failed")
        self.stack.addWidget(self.failed_page)

        self.resit_page = self.create_report_page("Resit Eligible Students", "resit")
        self.stack.addWidget(self.resit_page)

        self.excluded_page = self.create_report_page("Excluded Students", "excluded")
        self.stack.addWidget(self.excluded_page)

        # Start with menu
        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Student Status Reports")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)


        grid = QGridLayout()

        reports = [
            (" Passed Students", 0, 0, "#27ae60", "passed"),
            (" Failed Students", 0, 1, "#e74c3c", "failed"),
            (" Resit Eligible", 1, 0, "#f39c12", "resit"),
            (" Excluded Students", 1, 1, "#95a5a6", "excluded"),
        ]

        for name, row, col, color, report_type in reports:
            btn = QPushButton(name)
            btn.setFixedSize(180, 100)
            
            btn.clicked.connect(lambda checked, t=report_type: self.show_report(t))
            grid.addWidget(btn, row, col)

        grid.setAlignment(Qt.AlignCenter)
        layout.addLayout(grid)
        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Results Menu")
        
        btn_back.clicked.connect(self.go_back_to_results_menu)
        layout.addWidget(btn_back)

        return page

    def create_report_page(self, title, report_type):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Filter section
        filter_layout = QHBoxLayout()

        # Semester filter (for passed reports)
        if report_type == "passed":
            filter_layout.addWidget(QLabel("Semester:"))
            semester_combo = QComboBox()
            semester_combo.setObjectName(f"{report_type}_semester_combo")
            filter_layout.addWidget(semester_combo)
            setattr(self, f"{report_type}_semester_combo", semester_combo)

        # Course filter (for failed, resit, excluded)
        if report_type in ["failed", "resit", "excluded"]:
            filter_layout.addWidget(QLabel("Course:"))
            course_combo = QComboBox()
            course_combo.setObjectName(f"{report_type}_course_combo")
            filter_layout.addWidget(course_combo)
            setattr(self, f"{report_type}_course_combo", course_combo)

            filter_layout.addWidget(QLabel("Department:"))
            dept_combo = QComboBox()
            dept_combo.setObjectName(f"{report_type}_dept_combo")
            filter_layout.addWidget(dept_combo)
            setattr(self, f"{report_type}_dept_combo", dept_combo)

        # Search input
        filter_layout.addWidget(QLabel("Search:"))
        search_input = QLineEdit()
        search_input.setPlaceholderText("Student name...")
        search_input.setObjectName(f"{report_type}_search")
        filter_layout.addWidget(search_input)
        setattr(self, f"{report_type}_search", search_input)

        # Load button
        btn_load = QPushButton(" Load Report")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(lambda: self.load_report_data(report_type))
        filter_layout.addWidget(btn_load)

        layout.addLayout(filter_layout)

        # Table
        table = QTableWidget()
        table.setObjectName(f"{report_type}_table")
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table)
        setattr(self, f"{report_type}_table", table)

        # Export button
        btn_export = QPushButton(" Export to CSV")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(lambda: self.export_report(report_type))
        layout.addWidget(btn_export)

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def show_report(self, report_type):

        # Load filter dropdowns
        self.load_filters(report_type)

        # Switch to appropriate page
        page_map = {"passed": 1, "failed": 2, "resit": 3, "excluded": 4}
        self.stack.setCurrentIndex(page_map.get(report_type, 0))

    def load_filters(self, report_type):
        
        if report_type == "passed":
            # Load semesters
            semesters = ResultsQueries.get_semesters()
            combo = getattr(self, f"{report_type}_semester_combo")
            combo.clear()
            combo.addItem("-- Select Semester --", None)
            for semester_id, name in semesters:
                combo.addItem(name, semester_id)

        elif report_type in ["failed", "resit", "excluded"]:
            # Load courses
            courses = ResultsQueries.get_courses()
            course_combo = getattr(self, f"{report_type}_course_combo")
            course_combo.clear()
            course_combo.addItem("-- Select Course --", None)
            for course_id, dept_id, name in courses:
                course_combo.addItem(f"{name} (Dept {dept_id})", (course_id, dept_id))

            # Load departments
            departments = ResultsQueries.get_departments()
            dept_combo = getattr(self, f"{report_type}_dept_combo")
            dept_combo.clear()
            dept_combo.addItem("-- Select Department --", None)
            for dept_id, name in departments:
                dept_combo.addItem(name, dept_id)

    def load_report_data(self, report_type):

        try:
            results = []
            columns = []

            if report_type == "passed":
                semester_combo = getattr(self, f"{report_type}_semester_combo")
                semester_id = semester_combo.currentData()

                if not semester_id:
                    QMessageBox.warning(
                        self, "Selection Required", "Please select a semester."
                    )
                    return

                results, columns = ResultsQueries.execute_function(
                    "get_student_passed_semester", (semester_id,)
                )

            elif report_type == "failed":
                course_combo = getattr(self, f"{report_type}_course_combo")
                course_data = course_combo.currentData()

                if not course_data:
                    QMessageBox.warning(
                        self, "Selection Required", "Please select a course."
                    )
                    return

                course_id, dept_id = course_data

                results, columns = ResultsQueries.execute_function(
                    "get_students_failing_module", (course_id, dept_id)
                )

            elif report_type == "resit":
                course_combo = getattr(self, f"{report_type}_course_combo")
                course_data = course_combo.currentData()

                if not course_data:
                    QMessageBox.warning(
                        self, "Selection Required", "Please select a course."
                    )
                    return

                course_id, dept_id = course_data

                results, columns = ResultsQueries.execute_function(
                    "get_students_resit_eligible", (course_id, dept_id)
                )

            elif report_type == "excluded":
                course_combo = getattr(self, f"{report_type}_course_combo")
                course_data = course_combo.currentData()

                if not course_data:
                    QMessageBox.warning(
                        self, "Selection Required", "Please select a course."
                    )
                    return

                course_id, dept_id = course_data

                results, columns = ResultsQueries.execute_function(
                    "get_students_excluded_from_module", (course_id, dept_id)
                )

            # Filter by search term
            search_input = getattr(self, f"{report_type}_search")
            search_term = search_input.text().strip().lower()

            if search_term and len(results) > 0:
                # Filter results by student name (usually in columns 1 and 2)
                results = [
                    row
                    for row in results
                    if (len(row) > 1 and search_term in str(row[1]).lower())
                    or (len(row) > 2 and search_term in str(row[2]).lower())
                ]

            # Display in table
            self.populate_table(report_type, results, columns)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load report: {str(e)}")
            print(f"❌ Error loading {report_type} report: {e}")

    def populate_table(self, report_type, results, columns):

        table = getattr(self, f"{report_type}_table")

        # Setup table
        table.setRowCount(len(results))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        # Populate data
        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()

        # Show message if no results
        if not results:
            QMessageBox.information(
                self, "No Results", "No students found matching the criteria."
            )

    def export_report(self, report_type):

        from PyQt5.QtWidgets import QFileDialog
        import csv

        table = getattr(self, f"{report_type}_table")

        if table.rowCount() == 0:
            QMessageBox.warning(
                self, "No Data", "No data to export. Please load a report first."
            )
            return

        # Get file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Report",
            f"{report_type}_students_report.csv",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Write headers
                headers = [
                    table.horizontalHeaderItem(i).text()
                    for i in range(table.columnCount())
                ]
                writer.writerow(headers)

                # Write data
                for row in range(table.rowCount()):
                    row_data = [
                        table.item(row, col).text() if table.item(row, col) else ""
                        for col in range(table.columnCount())
                    ]
                    writer.writerow(row_data)

            QMessageBox.information(
                self, "Export Successful", f"Report exported to:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Export Failed", f"Failed to export report:\n{str(e)}"
            )

    def go_back_to_results_menu(self):

        if self.results_parent:
            self.results_parent.show_menu()
