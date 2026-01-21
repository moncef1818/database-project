
# Purpose: Course analysis reports (Disqualifying marks, Average by group)

from db.results_queries import ResultsQueries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CourseAnalysisView(QWidget):
    def __init__(self, parent=None, results_parent=None):

        super().__init__(parent)
        self.results_parent = results_parent  # Store reference for navigation

        # Main layout
        self.layout = QVBoxLayout(self)

        # Stacked widget for menu and report pages
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Report pages
        self.disqualify_page = self.create_disqualify_page()
        self.stack.addWidget(self.disqualify_page)

        self.avg_by_group_page = self.create_avg_by_group_page()
        self.stack.addWidget(self.avg_by_group_page)

        # Start with menu
        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Course Analysis Reports")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid for report buttons
        grid = QGridLayout()

        reports = [
            ("Disqualifying Marks\nReport", 0, 0, "#e74c3c", "disqualify"),
            (" Average Marks\nby Group", 0, 1, "#3498db", "avg_group"),
        ]

        for name, row, col, color, report_type in reports:
            btn = QPushButton(name)
            btn.setFixedSize(180, 100)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    opacity: 0.9;
                }}
            """
            )
            btn.clicked.connect(lambda checked, t=report_type: self.show_report(t))
            grid.addWidget(btn, row, col)

        grid.setAlignment(Qt.AlignCenter)
        layout.addLayout(grid)
        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Results Menu")
        btn_back.setStyleSheet(
            """
            background-color: #34495e;
            color: white;
            padding: 10px;
            border-radius: 5px;
        """
        )
        btn_back.clicked.connect(self.go_back_to_results_menu)
        layout.addWidget(btn_back)

        return page

    def create_disqualify_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Disqualifying Marks Report")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        desc = QLabel("Shows students scoring below 60% of the class average")
        desc.setStyleSheet("color: #7f8c8d; font-style: italic;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Filter section
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Course:"))
        self.disqualify_course_combo = QComboBox()
        filter_layout.addWidget(self.disqualify_course_combo)

        # Load button
        btn_load = QPushButton("🔍 Load Report")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(self.load_disqualify_report)
        filter_layout.addWidget(btn_load)

        layout.addLayout(filter_layout)

        # Table
        self.disqualify_table = QTableWidget()
        self.disqualify_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.disqualify_table.setSelectionMode(QTableWidget.SingleSelection)
        self.disqualify_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.disqualify_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.disqualify_table)

        # Export button
        btn_export = QPushButton("📄 Export to CSV")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(lambda: self.export_report("disqualify"))
        layout.addWidget(btn_export)

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def create_avg_by_group_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Average Marks by Group")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        desc = QLabel("Compare group performance for a selected course")
        desc.setStyleSheet("color: #7f8c8d; font-style: italic;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Filter section
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Course:"))
        self.avg_course_combo = QComboBox()
        filter_layout.addWidget(self.avg_course_combo)

        # Load button
        btn_load = QPushButton("🔍 Load Report")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(self.load_avg_by_group_report)
        filter_layout.addWidget(btn_load)

        layout.addLayout(filter_layout)

        # Table
        self.avg_table = QTableWidget()
        self.avg_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.avg_table.setSelectionMode(QTableWidget.SingleSelection)
        self.avg_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.avg_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.avg_table)

        # Export button
        btn_export = QPushButton("📄 Export to CSV")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(lambda: self.export_report("avg_group"))
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
        page_map = {"disqualify": 1, "avg_group": 2}
        self.stack.setCurrentIndex(page_map.get(report_type, 0))

    def load_filters(self, report_type):

        # Load courses for both reports
        courses = ResultsQueries.get_courses()

        if report_type == "disqualify":
            combo = self.disqualify_course_combo
        else:  # avg_group
            combo = self.avg_course_combo

        combo.clear()
        combo.addItem("-- Select Course --", None)
        for course_id, dept_id, name in courses:
            combo.addItem(f"{name} (Dept {dept_id})", (course_id, dept_id))

    def load_disqualify_report(self):
        """
        Loads the disqualifying marks report.
        """
        try:
            # Get course and department
            course_data = self.disqualify_course_combo.currentData()

            if not course_data:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a course."
                )
                return

            course_id, dept_id = course_data

            # Execute function
            results, columns = ResultsQueries.execute_function(
                "get_disqualifying_marks_by_module", (course_id, dept_id)
            )

            # Display in table
            self.populate_table(self.disqualify_table, results, columns)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load report: {str(e)}")
            print(f" Error loading disqualify report: {e}")

    def load_avg_by_group_report(self):
        try:
            # Get course and department
            course_data = self.avg_course_combo.currentData()

            if not course_data:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a course."
                )
                return

            course_id, dept_id = course_data

            # Execute function
            results, columns = ResultsQueries.execute_function(
                "get_average_marks_by_course_group", (course_id, dept_id)
            )

            # Display in table
            self.populate_table(self.avg_table, results, columns)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load report: {str(e)}")
            print(f" Error loading average by group report: {e}")

    def populate_table(self, table, results, columns):

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
                self, "No Results", "No data found matching the criteria."
            )

    def export_report(self, report_type):

        import csv

        from PyQt5.QtWidgets import QFileDialog

        # Get the appropriate table
        table = self.disqualify_table if report_type == "disqualify" else self.avg_table

        if table.rowCount() == 0:
            QMessageBox.warning(
                self, "No Data", "No data to export. Please load a report first."
            )
            return

        # Get file path
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", f"{report_type}_report.csv", "CSV Files (*.csv)"
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
