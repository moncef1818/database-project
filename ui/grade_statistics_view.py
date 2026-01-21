#Grade statistics and overview reports

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

from db.results_queries import ResultsQueries


class GradeStatisticsView(QWidget):

    def __init__(self, parent=None, results_parent=None):

        super().__init__(parent)
        self.results_parent = results_parent

        # Main layout
        self.layout = QVBoxLayout(self)

        # Stacked widget for menu and report pages
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Report pages
        self.overview_page = self.create_overview_page()
        self.stack.addWidget(self.overview_page)

        self.comparison_page = self.create_comparison_page()
        self.stack.addWidget(self.comparison_page)

        self.distribution_page = self.create_distribution_page()
        self.stack.addWidget(self.distribution_page)

        # Start with menu
        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Grade Statistics & Reports")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid for report buttons
        grid = QGridLayout()

        reports = [
            ("Semester\nOverview", 0, 0, "#3498db", "overview"),
            (" Course\nComparison", 0, 1, "#9b59b6", "comparison"),
            (" Grade\nDistribution", 1, 0, "#e67e22", "distribution"),
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

    def create_overview_page(self):
        """
        Creates the semester overview page.
        Returns:
            QWidget: Report page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Semester Performance Overview")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Semester:"))
        self.overview_semester_combo = QComboBox()
        filter_layout.addWidget(self.overview_semester_combo)

        btn_load = QPushButton("🔍 Load Overview")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(self.load_overview_report)
        filter_layout.addWidget(btn_load)
        layout.addLayout(filter_layout)

        # Stats cards
        stats_layout = QGridLayout()

        # Create stat cards
        self.stat_total = self.create_stat_card("Total Students", "0", "#3498db")
        self.stat_passed = self.create_stat_card("Passed", "0", "#27ae60")
        self.stat_failed = self.create_stat_card("Failed", "0", "#e74c3c")
        self.stat_resit = self.create_stat_card("Resit Eligible", "0", "#f39c12")
        self.stat_avg = self.create_stat_card("Average Grade", "0.00", "#9b59b6")
        self.stat_pass_rate = self.create_stat_card("Pass Rate", "0%", "#16a085")

        stats_layout.addWidget(self.stat_total, 0, 0)
        stats_layout.addWidget(self.stat_passed, 0, 1)
        stats_layout.addWidget(self.stat_failed, 0, 2)
        stats_layout.addWidget(self.stat_resit, 1, 0)
        stats_layout.addWidget(self.stat_avg, 1, 1)
        stats_layout.addWidget(self.stat_pass_rate, 1, 2)

        layout.addLayout(stats_layout)
        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def create_stat_card(self, label, value, color):

        card = QWidget()
        card.setStyleSheet(
            f"""
            QWidget {{
                background-color: {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """
        )
        layout = QVBoxLayout(card)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)

        val = QLabel(value)
        val.setObjectName("value")
        val.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        val.setAlignment(Qt.AlignCenter)
        layout.addWidget(val)

        return card

    def create_comparison_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Course Performance Comparison")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Semester:"))
        self.comparison_semester_combo = QComboBox()
        filter_layout.addWidget(self.comparison_semester_combo)

        btn_load = QPushButton("🔍 Load Comparison")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(self.load_comparison_report)
        filter_layout.addWidget(btn_load)
        layout.addLayout(filter_layout)

        # Table
        self.comparison_table = QTableWidget()
        self.comparison_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.comparison_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.comparison_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.comparison_table)

        # Export button
        btn_export = QPushButton("📄 Export to CSV")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(lambda: self.export_report("comparison"))
        layout.addWidget(btn_export)

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def create_distribution_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Grade Distribution")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filter section
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Course:"))
        self.distribution_course_combo = QComboBox()
        filter_layout.addWidget(self.distribution_course_combo)

        btn_load = QPushButton("🔍 Load Distribution")
        btn_load.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_load.clicked.connect(self.load_distribution_report)
        filter_layout.addWidget(btn_load)
        layout.addLayout(filter_layout)

        # Table
        self.distribution_table = QTableWidget()
        self.distribution_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.distribution_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.distribution_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.distribution_table)

        # Export button
        btn_export = QPushButton("📄 Export to CSV")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(lambda: self.export_report("distribution"))
        layout.addWidget(btn_export)

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def show_report(self, report_type):

        self.load_filters(report_type)

        page_map = {"overview": 1, "comparison": 2, "distribution": 3}
        self.stack.setCurrentIndex(page_map.get(report_type, 0))

    def load_filters(self, report_type):

        if report_type in ["overview", "comparison"]:
            semesters = ResultsQueries.get_semesters()
            combo = (
                self.overview_semester_combo
                if report_type == "overview"
                else self.comparison_semester_combo
            )
            combo.clear()
            combo.addItem("-- Select Semester --", None)
            for semester_id, name in semesters:
                combo.addItem(name, semester_id)

        elif report_type == "distribution":
            courses = ResultsQueries.get_courses()
            combo = self.distribution_course_combo
            combo.clear()
            combo.addItem("-- Select Course --", None)
            for course_id, dept_id, name in courses:
                combo.addItem(f"{name} (Dept {dept_id})", (course_id, dept_id))

    def load_overview_report(self):

        try:
            semester_id = self.overview_semester_combo.currentData()
            if not semester_id:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a semester."
                )
                return

            results, columns = ResultsQueries.execute_function(
                "get_semester_overview", (semester_id,)
            )

            if results and len(results) > 0:
                row = results[0]
                # Update stat cards
                self.stat_total.findChild(QLabel, "value").setText(str(row[0]))
                self.stat_passed.findChild(QLabel, "value").setText(str(row[1]))
                self.stat_failed.findChild(QLabel, "value").setText(str(row[2]))
                self.stat_resit.findChild(QLabel, "value").setText(str(row[3]))
                self.stat_avg.findChild(QLabel, "value").setText(
                    f"{float(row[4]):.2f}" if row[4] else "0.00"
                )

                # Calculate pass rate
                total = int(row[0]) if row[0] else 0
                passed = int(row[1]) if row[1] else 0
                pass_rate = (passed / total * 100) if total > 0 else 0
                self.stat_pass_rate.findChild(QLabel, "value").setText(
                    f"{pass_rate:.1f}%"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load overview: {str(e)}")
            print(f" Error loading overview: {e}")

    def load_comparison_report(self):

        try:
            semester_id = self.comparison_semester_combo.currentData()
            if not semester_id:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a semester."
                )
                return

            results, columns = ResultsQueries.execute_function(
                "get_course_comparison", (semester_id,)
            )

            self.populate_table(self.comparison_table, results, columns)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load comparison: {str(e)}")
            print(f" Error loading comparison: {e}")

    def load_distribution_report(self):

        try:
            course_data = self.distribution_course_combo.currentData()
            if not course_data:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a course."
                )
                return

            course_id, dept_id = course_data

            results, columns = ResultsQueries.execute_function(
                "get_grade_distribution", (course_id, dept_id)
            )

            self.populate_table(self.distribution_table, results, columns)

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to load distribution: {str(e)}"
            )
            print(f" Error loading distribution: {e}")

    def populate_table(self, table, results, columns):

        table.setRowCount(len(results))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()

        if not results:
            QMessageBox.information(self, "No Results", "No data found.")

    def export_report(self, report_type):

        from PyQt5.QtWidgets import QFileDialog
        import csv

        table = (
            self.comparison_table
            if report_type == "comparison"
            else self.distribution_table
        )

        if table.rowCount() == 0:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Report", f"{report_type}_report.csv", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                headers = [
                    table.horizontalHeaderItem(i).text()
                    for i in range(table.columnCount())
                ]
                writer.writerow(headers)

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
            QMessageBox.critical(self, "Export Failed", f"Failed to export: {str(e)}")

    def go_back_to_results_menu(self):

        if self.results_parent:
           self.results_parent.show_menu()
