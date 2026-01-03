# ui/attendance_crud_view.py
# Purpose: Complete CRUD operations for Attendance management

from db.attendance_queries import AttendanceQueries
from db.grade_queries import GradeQueries
from PyQt5.QtCore import QDate, Qt, QTime
from PyQt5.QtWidgets import (
    QCheckBox,
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
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class AttendanceCrudView(QWidget):
    def __init__(self, parent=None):
        """
        Initializes Attendance CRUD view with menu and operation pages.
        Args:
            parent: AcademicRecordsView reference
        """
        super().__init__(parent)
        # Stores (student_id, activity_id, attendance_date, activity_type) for operations
        self.selected_attendance = None

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
        title = QLabel("Attendance Management")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid for action buttons
        grid = QGridLayout()

        actions = [
            ("Add Attendance", 0, 0, "#27ae60"),
            ("View Attendance", 0, 1, "#3498db"),
            ("Update Attendance", 1, 0, "#f39c12"),
            ("Delete Attendance", 1, 1, "#e74c3c"),
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
        Routes to appropriate CRUD operation.
        Args:
            action_name: String identifying the action
        """
        if action_name == "Add Attendance":
            self.load_create_combos()
            self.clear_create_form()
            self.stack.setCurrentIndex(1)
        elif action_name == "View Attendance":
            self.clear_read_filters()
            self.load_attendance()
            self.stack.setCurrentIndex(2)
        elif action_name == "Update Attendance":
            self.load_update_combos()
            self.clear_read_filters()
            self.load_attendance_for_update()
            self.stack.setCurrentIndex(3)
        elif action_name == "Delete Attendance":
            self.load_attendance_for_delete()
            self.stack.setCurrentIndex(4)

    def setup_create_page(self):
        """
        Creates the form page for adding new attendance records.
        Returns:
            QWidget: Create form page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Add Attendance Record")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Form layout
        form = QFormLayout()

        # Student dropdown
        self.student_combo = QComboBox()
        form.addRow("Student *:", self.student_combo)

        # Activity dropdown
        self.activity_combo = QComboBox()
        form.addRow("Activity *:", self.activity_combo)

        # Activity type dropdown
        self.activity_type_combo = QComboBox()
        self.activity_type_combo.addItems(["Lecture", "Tutorial", "Practical"])
        form.addRow("Activity Type *:", self.activity_type_combo)

        # Attendance date
        self.attendance_date = QDateEdit()
        self.attendance_date.setDate(QDate.currentDate())
        self.attendance_date.setCalendarPopup(True)
        form.addRow("Attendance Date *:", self.attendance_date)

        # Attended checkbox
        self.attended_check = QCheckBox()
        self.attended_check.stateChanged.connect(self.toggle_time_field)
        form.addRow("Attended:", self.attended_check)

        # Attendance time (conditional)
        self.attendance_time = QTimeEdit()
        self.attendance_time.setTime(QTime.currentTime())
        self.attendance_time.setEnabled(False)  # Initially disabled
        form.addRow("Attendance Time:", self.attendance_time)

        # Special accommodations
        self.accommodations_text = QTextEdit()
        self.accommodations_text.setMaximumHeight(80)
        self.accommodations_text.setPlaceholderText("Enter any special accommodations...")
        form.addRow("Special Accommodations:", self.accommodations_text)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_submit = QPushButton("✓ Add Attendance")
        btn_submit.setStyleSheet("background-color: #27ae60; color: white; padding: 8px;")
        btn_submit.clicked.connect(self.submit_create)
        btn_layout.addWidget(btn_submit)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_back)

        layout.addLayout(btn_layout)

        return page

    def toggle_time_field(self, state):
        """
        Enables/disables time field based on attended checkbox.
        Args:
            state: Checkbox state (Qt.Checked or Qt.Unchecked)
        """
        self.attendance_time.setEnabled(state == Qt.Checked)
        if state != Qt.Checked:
            self.attendance_time.setTime(QTime.currentTime())  # Reset time

    def clear_create_form(self):
        """Clears all create form fields."""
        self.attendance_date.setDate(QDate.currentDate())
        self.attended_check.setChecked(False)
        self.attendance_time.setTime(QTime.currentTime())
        self.accommodations_text.clear()

    def load_create_combos(self):
        """Populates dropdowns for create form from database."""
        # Load students
        students = GradeQueries.get_students()
        self.student_combo.clear()
        for student_id, name in students:
            self.student_combo.addItem(name, student_id)

        # Load activities
        activities = AttendanceQueries.get_activities()
        self.activity_combo.clear()
        for activity_id, name in activities:
            self.activity_combo.addItem(name, activity_id)

    def submit_create(self):
        """Validates form data and creates new attendance record."""
        # Get form values
        student_id = self.student_combo.currentData()
        activity_id = self.activity_combo.currentData()
        activity_type = self.activity_type_combo.currentText()
        attendance_date = self.attendance_date.date().toString("yyyy-MM-dd")
        attended = self.attended_check.isChecked()
        attendance_time = self.attendance_time.time().toString("HH:mm:ss") if attended else None
        special_accommodations = self.accommodations_text.toPlainText().strip()

        # Validation
        if not all([student_id, activity_id, activity_type]):
            QMessageBox.warning(
                self,
                "Validation Error",
                "All required fields (*) must be filled."
            )
            return

        if attended and not attendance_time:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Attendance time is required when student attended."
            )
            return

        # Create in database
        success = AttendanceQueries.create_attendance(
            student_id, activity_id, attendance_date, attended,
            attendance_time, special_accommodations, activity_type
        )

        if success:
            QMessageBox.information(
                self,
                "Success",
                "Attendance record added successfully."
            )
            self.clear_create_form()
            self.stack.setCurrentIndex(0)  # Back to menu
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to add attendance. Check database connection and logs."
            )

    def setup_read_page(self):
        """
        Creates the view page for displaying attendance with filters.
        Returns:
            QWidget: Read page with table and filters
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("View Attendance Records")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Search and filter controls
        filter_layout = QHBoxLayout()

        # Search by student name
        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Student name...")
        filter_layout.addWidget(self.search_input)

        # Filter by activity type
        filter_layout.addWidget(QLabel("Activity Type:"))
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItems(["All", "Lecture", "Tutorial", "Practical"])
        filter_layout.addWidget(self.filter_type_combo)

        # Search button
        btn_search = QPushButton("🔍 Search")
        btn_search.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_search.clicked.connect(self.load_attendance)
        filter_layout.addWidget(btn_search)

        layout.addLayout(filter_layout)

        # Table for displaying attendance
        self.attendance_table = QTableWidget()
        self.attendance_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.attendance_table.setSelectionMode(QTableWidget.SingleSelection)
        self.attendance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.attendance_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        layout.addWidget(self.attendance_table)

        # Back button
        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return page

    def clear_read_filters(self):
        """Clears search filters."""
        self.search_input.clear()
        self.filter_type_combo.setCurrentIndex(0)  # "All"

    def load_attendance(self):
        """
        Loads attendance records into table with search/filter.
        Calculates and displays attendance percentage.
        """
        # Get filter values
        search_term = self.search_input.text().strip()
        activity_type = self.filter_type_combo.currentText()
        if activity_type == "All":
            activity_type = None

        # Fetch attendance from database
        attendances = AttendanceQueries.get_all_attendance(activity_type, search_term)

        # Setup table with 9 columns (including hidden IDs)
        self.attendance_table.setRowCount(len(attendances))
        self.attendance_table.setColumnCount(9)
        self.attendance_table.setHorizontalHeaderLabels([
            "Student", "Activity Type", "Date", "Attended",
            "Time", "Accommodations", "Attendance %",
            "Student ID", "Activity ID"
        ])

        # Hide ID columns (for internal use)
        self.attendance_table.setColumnHidden(7, True)  # student_id
        self.attendance_table.setColumnHidden(8, True)  # activity_id

        # Populate table
        for row_idx, att in enumerate(attendances):
            # att tuple: (student_name, activity_type, date, attended, time, accommodations, student_id, activity_id)
            # Display columns (0-5)
            for col_idx in range(6):
                value = att[col_idx]
                # Format boolean values
                if col_idx == 3:  # attended column
                    value = "✓ Yes" if value else "✗ No"
                # Format None values
                if value is None:
                    value = "N/A"

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)

                # Color code attended status
                if col_idx == 3:
                    if att[3]:  # attended = True
                        item.setForeground(Qt.darkGreen)
                    else:
                        item.setForeground(Qt.red)

                self.attendance_table.setItem(row_idx, col_idx, item)

            # Calculate and add attendance percentage
            student_id = att[6]
            activity_id = att[7]
            percent = self.calculate_attendance_percent(student_id, activity_id)
            percent_item = QTableWidgetItem(f"{percent:.1f}%")
            percent_item.setTextAlignment(Qt.AlignCenter)

            # Color code percentage
            if percent >= 75:
                percent_item.setForeground(Qt.darkGreen)
            elif percent >= 50:
                percent_item.setForeground(Qt.darkYellow)
            else:
                percent_item.setForeground(Qt.red)

            self.attendance_table.setItem(row_idx, 6, percent_item)

            # Add hidden ID columns
            self.attendance_table.setItem(row_idx, 7, QTableWidgetItem(str(student_id)))
            self.attendance_table.setItem(row_idx, 8, QTableWidgetItem(str(activity_id)))

        # Resize visible columns
        for i in range(7):  # Visible columns only
            self.attendance_table.resizeColumnToContents(i)

        # Show message if no results
        if not attendances:
            QMessageBox.information(
                self,
                "No Results",
                "No attendance records found matching your criteria."
            )

    def calculate_attendance_percent(self, student_id, activity_id):
        """
        Calculates attendance percentage for student/activity.
        Formula: (attended_count / total_count) * 100

        Args:
            student_id: Student ID
            activity_id: Activity ID

        Returns:
            float: Attendance percentage (0-100)
        """
        total, attended_count = AttendanceQueries.get_attendance_for_percent(
            student_id, activity_id
        )
        return (attended_count / total * 100) if total > 0 else 0.0

    def setup_update_page(self):
        """
        Creates the page for updating attendance records.
        Returns:
            QWidget: Update page with table and form
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Update Attendance Record")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Instructions
        instructions = QLabel("Double-click a row to edit it")
        instructions.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(instructions)

        # Search and filter (reuse from read page)
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Search:"))
        self.update_search_input = QLineEdit()
        self.update_search_input.setPlaceholderText("Student name...")
        filter_layout.addWidget(self.update_search_input)

        filter_layout.addWidget(QLabel("Type:"))
        self.update_filter_type_combo = QComboBox()
        self.update_filter_type_combo.addItems(["All", "Lecture", "Tutorial", "Practical"])
        filter_layout.addWidget(self.update_filter_type_combo)

        btn_search = QPushButton("🔍 Search")
        btn_search.setStyleSheet("background-color: #3498db; color: white; padding: 5px;")
        btn_search.clicked.connect(self.load_attendance_for_update)
        filter_layout.addWidget(btn_search)

        layout.addLayout(filter_layout)

        # Table for selecting attendance to update
        self.update_table = QTableWidget()
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.setSelectionMode(QTableWidget.SingleSelection)
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.itemDoubleClicked.connect(self.pre_fill_update)
        layout.addWidget(self.update_table)

        # Update form (initially hidden)
        self.update_form_widget = QWidget()
        self.update_form = QFormLayout(self.update_form_widget)

        # Form fields
        self.update_student_combo = QComboBox()
        self.update_student_combo.setEnabled(False)  # Can't change student
        self.update_form.addRow("Student:", self.update_student_combo)

        self.update_activity_combo = QComboBox()
        self.update_activity_combo.setEnabled(False)  # Can't change activity
        self.update_form.addRow("Activity:", self.update_activity_combo)

        self.update_activity_type_combo = QComboBox()
        self.update_activity_type_combo.addItems(["Lecture", "Tutorial", "Practical"])
        self.update_activity_type_combo.setEnabled(False)  # Can't change type
        self.update_form.addRow("Activity Type:", self.update_activity_type_combo)

        self.update_attendance_date = QDateEdit()
        self.update_attendance_date.setCalendarPopup(True)
        self.update_attendance_date.setEnabled(False)  # Can't change date
        self.update_form.addRow("Date:", self.update_attendance_date)

        self.update_attended_check = QCheckBox()
        self.update_attended_check.stateChanged.connect(self.toggle_update_time_field)
        self.update_form.addRow("Attended:", self.update_attended_check)

        self.update_attendance_time = QTimeEdit()
        self.update_form.addRow("Attendance Time:", self.update_attendance_time)

        self.update_accommodations_text = QTextEdit()
        self.update_accommodations_text.setMaximumHeight(80)
        self.update_form.addRow("Special Accommodations:", self.update_accommodations_text)

        self.update_form_widget.setVisible(False)
        layout.addWidget(self.update_form_widget)

        # Buttons
        btn_layout = QHBoxLayout()

        btn_submit = QPushButton("✓ Update Attendance")
        btn_submit.setStyleSheet("background-color: #f39c12; color: white; padding: 8px;")
        btn_submit.clicked.connect(self.submit_update)
        btn_layout.addWidget(btn_submit)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_layout.addWidget(btn_back)

        layout.addLayout(btn_layout)

        return page

    def toggle_update_time_field(self, state):
        """
        Enables/disables time field in update form.
        Args:
            state: Checkbox state
        """
        self.update_attendance_time.setEnabled(state == Qt.Checked)

    def load_update_combos(self):
        """Populates dropdowns for update form."""
        # Load students
        students = GradeQueries.get_students()
        self.update_student_combo.clear()
        for student_id, name in students:
            self.update_student_combo.addItem(name, student_id)

        # Load activities
        activities = AttendanceQueries.get_activities()
        self.update_activity_combo.clear()
        for activity_id, name in activities:
            self.update_activity_combo.addItem(name, activity_id)

    def load_attendance_for_update(self):
        """Loads attendance records for selection in update."""
        # Get filter values
        search_term = self.update_search_input.text().strip()
        activity_type = self.update_filter_type_combo.currentText()
        if activity_type == "All":
            activity_type = None

        # Fetch attendance
        attendances = AttendanceQueries.get_all_attendance(activity_type, search_term)

        # Setup table
        self.update_table.setRowCount(len(attendances))
        self.update_table.setColumnCount(9)
        self.update_table.setHorizontalHeaderLabels([
            "Student", "Type", "Date", "Attended",
            "Time", "Accommodations", "%",
            "Student ID", "Activity ID"
        ])

        # Hide ID columns
        self.update_table.setColumnHidden(7, True)
        self.update_table.setColumnHidden(8, True)

        # Populate table
        for row_idx, att in enumerate(attendances):
            for col_idx in range(6):
                value = att[col_idx]
                if col_idx == 3:
                    value = "✓ Yes" if value else "✗ No"
                if value is None:
                    value = "N/A"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.update_table.setItem(row_idx, col_idx, item)

            # Percentage
            percent = self.calculate_attendance_percent(att[6], att[7])
            self.update_table.setItem(row_idx, 6, QTableWidgetItem(f"{percent:.1f}%"))

            # Hidden IDs
            self.update_table.setItem(row_idx, 7, QTableWidgetItem(str(att[6])))
            self.update_table.setItem(row_idx, 8, QTableWidgetItem(str(att[7])))

        self.update_table.resizeColumnsToContents()

        if not attendances:
            QMessageBox.information(
                self,
                "No Results",
                "No attendance records found."
            )

    def pre_fill_update(self, item):
        """
        Pre-fills update form when an attendance record is selected.
        Args:
            item: Table item that was double-clicked
        """
        row = item.row()

        # Get data from hidden columns
        student_id = int(self.update_table.item(row, 7).text())
        activity_id = int(self.update_table.item(row, 8).text())
        attendance_date = self.update_table.item(row, 2).text()
        activity_type = self.update_table.item(row, 1).text()

        # Store for update operation
        self.selected_attendance = (student_id, activity_id, attendance_date, activity_type)

        # Fetch full details
        full_attendance = AttendanceQueries.get_attendance_by_key(
            student_id, activity_id, attendance_date, activity_type
        )

        if not full_attendance:
            QMessageBox.warning(self, "Error", "Could not load attendance details.")
            return

        # full_attendance tuple: (student_id, activity_id, date, attended, time, accommodations)

        # Pre-fill form
        self.update_student_combo.setCurrentIndex(
            self.update_student_combo.findData(student_id)
        )
        self.update_activity_combo.setCurrentIndex(
            self.update_activity_combo.findData(activity_id)
        )
        self.update_activity_type_combo.setCurrentText(activity_type)
        self.update_attendance_date.setDate(
            QDate.fromString(attendance_date, "yyyy-MM-dd")
        )
        self.update_attended_check.setChecked(full_attendance[3])

        # Set time if attended
        if full_attendance[4]:
            self.update_attendance_time.setTime(
                QTime.fromString(full_attendance[4], "HH:mm:ss")
            )
            self.update_attendance_time.setEnabled(True)
        else:
            self.update_attendance_time.setTime(QTime.currentTime())
            self.update_attendance_time.setEnabled(False)

        # Set accommodations
        self.update_accommodations_text.setText(
            full_attendance[5] if full_attendance[5] else ""
        )

        # Show form
        self.update_form_widget.setVisible(True)

    def submit_update(self):
        """Validates and submits updated attendance data."""
        if not self.selected_attendance:
            QMessageBox.warning(self, "Error", "No attendance record selected.")
            return

        student_id, activity_id, attendance_date, activity_type = self.selected_attendance

        # Get form values (only editable fields)
        attended = self.update_attended_check.isChecked()
        attendance_time = self.update_attendance_time.time().toString("HH:mm:ss") if attended else None
        special_accommodations = self.update_accommodations_text.toPlainText().strip()

        # Validation
        if attended and not attendance_time:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Attendance time required when student attended."
            )
            return

        # Update in database
        success = AttendanceQueries.update_attendance(
            student_id, activity_id, attendance_date, attended,
            attendance_time, special_accommodations, activity_type
        )

        if success:
            QMessageBox.information(self, "Success", "Attendance updated successfully.")
            self.update_form_widget.setVisible(False)
            self.load_attendance_for_update()  # Refresh table
        else:
            QMessageBox.critical(self, "Error", "Failed to update attendance.")

    def setup_delete_page(self):
        """
        Creates the page for deleting attendance records.
        Returns:
            QWidget: Delete confirmation page
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title = QLabel("Delete Attendance Record")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Warning
        warning = QLabel("⚠️ Select a record and click Delete. This action cannot be undone!")
        warning.setStyleSheet("color: #e74c3c; font-weight: bold;")
        layout.addWidget(warning)

        # Table
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

    def load_attendance_for_delete(self):
        """Loads all attendance records for deletion."""
        # Fetch all attendance (no filters)
        attendances = AttendanceQueries.get_all_attendance(None, "")

        # Setup table
        self.delete_table.setRowCount(len(attendances))
        self.delete_table.setColumnCount(9)
        self.delete_table.setHorizontalHeaderLabels([
            "Student", "Type", "Date", "Attended",
            "Time", "Accommodations", "%",
            "Student ID", "Activity ID"
        ])

        # Hide ID columns
        self.delete_table.setColumnHidden(7, True)
        self.delete_table.setColumnHidden(8, True)

        # Populate table
        for row_idx, att in enumerate(attendances):
            for col_idx in range(6):
                value = att[col_idx]
                if col_idx == 3:
                    value = "✓ Yes" if value else "✗ No"
                if value is None:
                    value = "N/A"
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.delete_table.setItem(row_idx, col_idx, item)

            # Percentage
            percent = self.calculate_attendance_percent(att[6], att[7])
            self.delete_table.setItem(row_idx, 6, QTableWidgetItem(f"{percent:.1f}%"))

            # Hidden IDs
            self.delete_table.setItem(row_idx, 7, QTableWidgetItem(str(att[6])))
            self.delete_table.setItem(row_idx, 8, QTableWidgetItem(str(att[7])))

        self.delete_table.resizeColumnsToContents()

        if not attendances:
            QMessageBox.information(self, "No Data", "No attendance records in database.")

    def confirm_delete(self):
        """Confirms and deletes selected attendance record."""
        # Get selected row
        selected_items = self.delete_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a record to delete.")
            return

        row = selected_items[0].row()

        # Get data from table
        student_id = int(self.delete_table.item(row, 7).text())
        activity_id = int(self.delete_table.item(row, 8).text())
        attendance_date = self.delete_table.item(row, 2).text()
        activity_type = self.delete_table.item(row, 1).text()

        student_name = self.delete_table.item(row, 0).text()

        # Confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete this attendance record?\n\n"
            f"Student: {student_name}\n"
            f"Activity Type: {activity_type}\n"
            f"Date: {attendance_date}\n\n"
            f"This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Delete from database
            success = AttendanceQueries.delete_attendance(
                student_id, activity_id, attendance_date, activity_type
            )

            if success:
                QMessageBox.information(self, "Success", "Attendance deleted successfully.")
                self.load_attendance_for_delete()  # Refresh table
            else:
                QMessageBox.critical(self, "Error", "Failed to delete attendance.")

    def go_back_to_academic_menu(self):
        """Returns to the Academic Records menu."""
        if self.parent():
            self.parent().show_menu()
