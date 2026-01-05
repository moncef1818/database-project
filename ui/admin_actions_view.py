
# Purpose: Administrative actions for grade management

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from db.results_queries import ResultsQueries


class AdminActionsView(QWidget):

    def __init__(self, parent=None, results_parent=None):

        super().__init__(parent)
        self.results_parent = results_parent

        # Main layout
        self.layout = QVBoxLayout(self)

        # Stacked widget for menu and action pages
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Action pages
        self.update_status_page = self.create_update_status_page()
        self.stack.addWidget(self.update_status_page)

        self.generate_resit_page = self.create_generate_resit_page()
        self.stack.addWidget(self.generate_resit_page)

        # Start with menu
        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Administrative Actions")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Warning
        warning = QLabel("⚠️ These actions modify database records. Use with caution.")
        warning.setStyleSheet("color: #e67e22; font-weight: bold; font-style: italic;")
        warning.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning)

        # Grid for action buttons
        grid = QGridLayout()

        actions = [
            (" Update Enrollment\nStatus", 0, 0, "#27ae60", "update_status"),
            (" Generate Resit\nList", 0, 1, "#3498db", "generate_resit"),
        ]

        for name, row, col, color, action_type in actions:
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
            btn.clicked.connect(lambda checked, t=action_type: self.show_action(t))
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

    def create_update_status_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Update Enrollment Status")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "Automatically update student enrollment status based on their grades:\n"
            "• Average ≥ 10 → Passed\n"
            "• 8 ≤ Average < 10 → Resit Eligible\n"
            "• Average < 8 → Failed"
        )
        desc.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(desc)

        # Filter section
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Course:"))
        self.update_course_combo = QComboBox()
        filter_layout.addWidget(self.update_course_combo)

        filter_layout.addWidget(QLabel("Semester:"))
        self.update_semester_combo = QComboBox()
        filter_layout.addWidget(self.update_semester_combo)

        layout.addLayout(filter_layout)

        # Result display
        self.update_result_text = QTextEdit()
        self.update_result_text.setReadOnly(True)
        self.update_result_text.setMaximumHeight(200)
        layout.addWidget(self.update_result_text)

        # Execute button
        btn_execute = QPushButton(" Execute Update")
        btn_execute.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px; font-weight: bold;"
        )
        btn_execute.clicked.connect(self.execute_update_status)
        layout.addWidget(btn_execute)

        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def create_generate_resit_page(self):
        """
        Creates the generate resit list page.
        Returns:
            QWidget: Action page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Generate Resit List")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        desc = QLabel("Generate a list of students eligible for makeup exams")
        desc.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(desc)

        # Filter section
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Course:"))
        self.resit_course_combo = QComboBox()
        filter_layout.addWidget(self.resit_course_combo)

        layout.addLayout(filter_layout)

        # Result display
        self.resit_result_text = QTextEdit()
        self.resit_result_text.setReadOnly(True)
        layout.addWidget(self.resit_result_text)

        # Button row
        btn_layout = QHBoxLayout()

        btn_generate = QPushButton(" Generate List")
        btn_generate.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px;"
        )
        btn_generate.clicked.connect(self.generate_resit_list)
        btn_layout.addWidget(btn_generate)

        btn_export = QPushButton(" Export to File")
        btn_export.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 8px;"
        )
        btn_export.clicked.connect(self.export_resit_list)
        btn_layout.addWidget(btn_export)

        layout.addLayout(btn_layout)

        # Back button
        btn_back = QPushButton("← Back to Menu")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def show_action(self, action_type):

        self.load_filters(action_type)

        page_map = {"update_status": 1, "generate_resit": 2}
        self.stack.setCurrentIndex(page_map.get(action_type, 0))

    def load_filters(self, action_type):

        courses = ResultsQueries.get_courses()

        if action_type == "update_status":
            # Load courses
            self.update_course_combo.clear()
            self.update_course_combo.addItem("-- Select Course --", None)
            for course_id, dept_id, name in courses:
                self.update_course_combo.addItem(
                    f"{name} (Dept {dept_id})", (course_id, dept_id)
                )

            # Load semesters
            semesters = ResultsQueries.get_semesters()
            self.update_semester_combo.clear()
            self.update_semester_combo.addItem("-- Select Semester --", None)
            for semester_id, name in semesters:
                self.update_semester_combo.addItem(name, semester_id)

        elif action_type == "generate_resit":
            # Load courses
            self.resit_course_combo.clear()
            self.resit_course_combo.addItem("-- Select Course --", None)
            for course_id, dept_id, name in courses:
                self.resit_course_combo.addItem(
                    f"{name} (Dept {dept_id})", (course_id, dept_id)
                )

    def execute_update_status(self):

        try:
            # Get selections
            course_data = self.update_course_combo.currentData()
            semester_id = self.update_semester_combo.currentData()

            if not course_data or not semester_id:
                QMessageBox.warning(
                    self,
                    "Selection Required",
                    "Please select both course and semester.",
                )
                return

            course_id, dept_id = course_data

            # Confirmation dialog
            reply = QMessageBox.question(
                self,
                "Confirm Action",
                f"This will update enrollment status for all students in:\n"
                f"Course ID: {course_id}\n"
                f"Department ID: {dept_id}\n"
                f"Semester ID: {semester_id}\n\n"
                f"Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply != QMessageBox.Yes:
                return

            # Execute update
            results = ResultsQueries.update_enrollment_status(
                course_id, dept_id, semester_id
            )

            if results:
                # Display results
                result_text = f"✅ Successfully updated {len(results)} student(s):\n\n"
                for student_id, status in results:
                    result_text += f"Student ID {student_id}: {status}\n"

                self.update_result_text.setText(result_text)

                QMessageBox.information(
                    self,
                    "Success",
                    f"Updated enrollment status for {len(results)} students.",
                )
            else:
                self.update_result_text.setText("No students found to update.")
                QMessageBox.information(
                    self, "No Updates", "No students found matching the criteria."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update status: {str(e)}")
            print(f"❌ Error updating status: {e}")

    def generate_resit_list(self):

        try:
            # Get course selection
            course_data = self.resit_course_combo.currentData()

            if not course_data:
                QMessageBox.warning(
                    self, "Selection Required", "Please select a course."
                )
                return

            course_id, dept_id = course_data

            # Execute function
            results, columns = ResultsQueries.execute_function(
                "get_students_resit_eligible", (course_id, dept_id)
            )

            if results:
                # Format results
                result_text = f"  Resit Eligible Students List\n"
                result_text += f"{'='*60}\n\n"
                result_text += f"Course ID: {course_id} | Department ID: {dept_id}\n"
                result_text += f"Total Students: {len(results)}\n\n"
                result_text += (
                    f"{'ID':<10}{'Last Name':<20}{'First Name':<20}{'Avg':<10}\n"
                )
                result_text += f"{'-'*60}\n"

                for row in results:
                    student_id, last_name, first_name, avg = row
                    result_text += f"{student_id:<10}{last_name:<20}{first_name:<20}{float(avg):<10.2f}\n"

                self.resit_result_text.setText(result_text)

                QMessageBox.information(
                    self,
                    "List Generated",
                    f"Found {len(results)} student(s) eligible for resit.",
                )
            else:
                self.resit_result_text.setText("No students eligible for resit found.")
                QMessageBox.information(
                    self, "No Students", "No students found eligible for resit exam."
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate list: {str(e)}")
            print(f"❌ Error generating resit list: {e}")

    def export_resit_list(self):
        """
        Exports the resit list to a text file.
        """
        from PyQt5.QtWidgets import QFileDialog

        text = self.resit_result_text.toPlainText()

        if not text or "No students" in text:
            QMessageBox.warning(
                self, "No Data", "No resit list to export. Generate a list first."
            )
            return

        # Get file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Resit List",
            "resit_eligible_students.txt",
            "Text Files (*.txt);;All Files (*)",
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

            QMessageBox.information(
                self, "Export Successful", f"Resit list exported to:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Export Failed", f"Failed to export list:\n{str(e)}"
            )

    def go_back_to_results_menu(self):
        
        if self.results_parent:
            self.results_parent.show_menu()
