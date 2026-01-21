from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QComboBox, QFormLayout, QDialog,
    QDialogButtonBox, QMessageBox, QHeaderView, QDateEdit, QTimeEdit,
    QSpinBox, QGroupBox
)
from datetime import datetime, timedelta
from db import reservation_queries


class ReservationCRUDTab(QWidget):
    """Tab for managing reservations (CRUD operations)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_reservations()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Reservation Management")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search and filter controls
        filter_layout = QHBoxLayout()
        
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems([
            "All", "Course", "Instructor", "Activity Type", "Building", "Date"
        ])
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.on_search)
        
        filter_layout.addWidget(QLabel("Search by:"))
        filter_layout.addWidget(self.search_field_combo)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(search_btn)
        
        # Sort controls
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Date", "Time", "Course", "Instructor", "Building"])
        
        self.sort_order_combo = QComboBox()
        self.sort_order_combo.addItems(["ASC", "DESC"])
        
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addWidget(self.sort_order_combo)
        
        layout.addLayout(filter_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Start", "End", "Hours", "Course", "Department",
            "Activity", "Instructor", "Building", "Room"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        create_btn = QPushButton("Create Reservation")
        create_btn.clicked.connect(self.create_reservation)
        
        update_btn = QPushButton("Update Selected")
        update_btn.clicked.connect(self.update_reservation)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_reservation)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_reservations)
        
        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)
    
    def load_reservations(self):
        """Load all reservations into table"""
        sort_map = {
            "Date": "reserv_date",
            "Time": "start_time",
            "Course": "course_name",
            "Instructor": "instructor_name",
            "Building": "building"
        }
        
        sort_by = sort_map.get(self.sort_combo.currentText(), "reserv_date")
        sort_order = self.sort_order_combo.currentText()
        
        reservations = reservation_queries.ReservationQueries.get_all_reservations(
            sort_by=sort_by, sort_order=sort_order
        )
        
        self.table.setRowCount(0)
        
        for row_data in reservations:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)
            
            for col_num, data in enumerate(row_data[:11]):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)
    
    def on_search(self):
        """Search reservations"""
        search_field_map = {
            "Course": "course_name",
            "Instructor": "instructor_name",
            "Activity Type": "activity_type",
            "Building": "building",
            "Date": "reserv_date"
        }
        
        field_text = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()
        
        if field_text == "All" or not search_value:
            self.load_reservations()
            return
        
        search_field = search_field_map.get(field_text)
        
        sort_map = {
            "Date": "reserv_date",
            "Time": "start_time",
            "Course": "course_name",
            "Instructor": "instructor_name",
            "Building": "building"
        }
        sort_by = sort_map.get(self.sort_combo.currentText(), "reserv_date")
        sort_order = self.sort_order_combo.currentText()
        
        reservations = reservation_queries.ReservationQueries.get_all_reservations(
            search_field=search_field,
            search_value=search_value,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        self.table.setRowCount(0)
        
        for row_data in reservations:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)
            
            for col_num, data in enumerate(row_data[:11]):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)
    
    def create_reservation(self):
        """Open dialog to create new reservation"""
        dialog = ReservationDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reservations()
    
    def update_reservation(self):
        """Open dialog to update selected reservation"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a reservation to update.")
            return
        
        reservation_id = int(self.table.item(selected_rows[0].row(), 0).text())
        
        dialog = ReservationDialog(self, reservation_id=reservation_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_reservations()
    
    def delete_reservation(self):
        """Delete selected reservation"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a reservation to delete.")
            return
        
        reservation_id = int(self.table.item(selected_rows[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete reservation ID {reservation_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                reservation_queries.ReservationQueries.delete_reservation(reservation_id)
                QMessageBox.information(self, "Success", "Reservation deleted successfully!")
                self.load_reservations()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete reservation:\n{str(e)}")


class ReservationDialog(QDialog):
    """Dialog for creating/updating reservations"""
    
    def __init__(self, parent=None, reservation_id=None):
        super().__init__(parent)
        self.reservation_id = reservation_id
        self.is_update = reservation_id is not None
        
        self.setWindowTitle("Update Reservation" if self.is_update else "Create Reservation")
        self.setMinimumWidth(500)
        
        self.initUI()
        
        if self.is_update:
            self.load_reservation_data()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        
        # Course
        self.course_combo = QComboBox()
        courses = reservation_queries.ReservationQueries.get_all_courses()
        self.course_data = {}
        for course_id, name, dept_id in courses:
            display_text = f"{name} (ID: {course_id})"
            self.course_combo.addItem(display_text)
            self.course_data[display_text] = (course_id, dept_id)
        
        self.course_combo.currentTextChanged.connect(self.on_course_changed)
        form.addRow("Course:", self.course_combo)
        
        # Activity Type
        self.activity_combo = QComboBox()
        self.activity_combo.addItems(["Lecture", "Tutorial", "Practical"])
        form.addRow("Activity Type:", self.activity_combo)
        
        # Instructor
        self.instructor_combo = QComboBox()
        instructors = reservation_queries.ReservationQueries.get_all_instructors()
        self.instructor_data = {}
        for inst_id, name in instructors:
            self.instructor_combo.addItem(name)
            self.instructor_data[name] = inst_id
        form.addRow("Instructor:", self.instructor_combo)
        
        # Room
        # Room
        self.room_combo = QComboBox()
        rooms = reservation_queries.ReservationQueries.get_all_rooms()
        self.room_data = {}
        for building, roomno, capacity in rooms:  # ← CHANGED: removed room_type
            display_text = f"{building}{roomno} (Cap: {capacity})"  # ← CHANGED: removed type display
            self.room_combo.addItem(display_text)
            self.room_data[display_text] = (building, roomno)
        form.addRow("Room:", self.room_combo)

        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date:", self.date_edit)
        
        # Start Time
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime(8, 0))
        self.start_time_edit.timeChanged.connect(self.calculate_hours)
        form.addRow("Start Time:", self.start_time_edit)
        
        # End Time
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime(10, 0))
        self.end_time_edit.timeChanged.connect(self.calculate_hours)
        form.addRow("End Time:", self.end_time_edit)
        
        # Hours (auto-calculated, read-only)
        self.hours_label = QLabel("2.0")
        form.addRow("Hours:", self.hours_label)
        
        layout.addLayout(form)
        
        # Check conflicts button
        check_btn = QPushButton("Check Conflicts")
        check_btn.clicked.connect(self.check_conflicts)
        layout.addWidget(check_btn)
        
        # Dialog buttons
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.save_reservation)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
    
    def on_course_changed(self):
        """Update activity types when course changes"""
        course_text = self.course_combo.currentText()
        if course_text in self.course_data:
            course_id, dept_id = self.course_data[course_text]
            activities = reservation_queries.ReservationQueries.get_activities_for_course(course_id, dept_id)
            
            self.activity_combo.clear()
            for (activity_type,) in activities:
                self.activity_combo.addItem(activity_type)
    
    def calculate_hours(self):
        """Calculate hours from start and end time"""
        start = self.start_time_edit.time()
        end = self.end_time_edit.time()
        
        start_minutes = start.hour() * 60 + start.minute()
        end_minutes = end.hour() * 60 + end.minute()
        
        if end_minutes > start_minutes:
            hours = (end_minutes - start_minutes) / 60.0
            self.hours_label.setText(f"{hours:.2f}")
        else:
            self.hours_label.setText("Invalid")
    
    def check_conflicts(self):
        """Check for scheduling conflicts"""
        building, roomno = self.room_data[self.room_combo.currentText()]
        instructor_id = self.instructor_data[self.instructor_combo.currentText()]
        
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start = self.start_time_edit.time().toString("HH:mm:ss")
        end = self.end_time_edit.time().toString("HH:mm:ss")
        
        exclude_id = self.reservation_id if self.is_update else None
        
        # Check room conflict
        room_conflicts = reservation_queries.ReservationQueries.check_room_conflict(
            building, roomno, date, start, end, exclude_id
        )
        
        # Check instructor conflict
        instructor_conflicts = reservation_queries.ReservationQueries.check_instructor_conflict(
            instructor_id, date, start, end, exclude_id
        )
        
        messages = []
        
        if room_conflicts:
            messages.append(f"❌ Room {building}{roomno} is already booked:")
            for conflict in room_conflicts:
                messages.append(f"  - {conflict[3]} from {conflict[1]} to {conflict[2]}")
        
        if instructor_conflicts:
            messages.append(f"\n❌ Instructor is already assigned:")
            for conflict in instructor_conflicts:
                messages.append(f"  - {conflict[3]} in {conflict[4]}{conflict[5]} from {conflict[1]} to {conflict[2]}")
        
        if messages:
            QMessageBox.warning(self, "Conflicts Found", "\n".join(messages))
        else:
            QMessageBox.information(self, "No Conflicts", "✅ No scheduling conflicts found!")
    
    def load_reservation_data(self):
        """Load existing reservation data for update"""
        data = reservation_queries.ReservationQueries.get_reservation_by_id(self.reservation_id)
        
        if data:
            # Find and select course
            course_id, dept_id = data[3], data[4]
            for i in range(self.course_combo.count()):
                text = self.course_combo.itemText(i)
                if self.course_data[text] == (course_id, dept_id):
                    self.course_combo.setCurrentIndex(i)
                    break
            
            # Activity type
            self.activity_combo.setCurrentText(data[5])
            
            # Find and select instructor
            instructor_id = data[6]
            for name, inst_id in self.instructor_data.items():
                if inst_id == instructor_id:
                    self.instructor_combo.setCurrentText(name)
                    break
            
            # Find and select room
            building, roomno = data[1], data[2]
            for i in range(self.room_combo.count()):
                text = self.room_combo.itemText(i)
                if self.room_data[text] == (building, roomno):
                    self.room_combo.setCurrentIndex(i)
                    break
            
            # Date and time
            self.date_edit.setDate(QDate.fromString(str(data[7]), "yyyy-MM-dd"))
            self.start_time_edit.setTime(QTime.fromString(str(data[8]), "HH:mm:ss"))
            self.end_time_edit.setTime(QTime.fromString(str(data[9]), "HH:mm:ss"))
    
    def save_reservation(self):
        """Save reservation to database"""
        # Validate
        if self.start_time_edit.time() >= self.end_time_edit.time():
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time!")
            return
        
        # Get values
        course_id, dept_id = self.course_data[self.course_combo.currentText()]
        activity_type = self.activity_combo.currentText()
        instructor_id = self.instructor_data[self.instructor_combo.currentText()]
        building, roomno = self.room_data[self.room_combo.currentText()]
        
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start = self.start_time_edit.time().toString("HH:mm:ss")
        end = self.end_time_edit.time().toString("HH:mm:ss")
        hours = float(self.hours_label.text())
        
        try:
            if self.is_update:
                reservation_queries.ReservationQueries.update_reservation(
                    self.reservation_id, building, roomno, course_id, dept_id,
                    activity_type, instructor_id, date, start, end, hours
                )
                QMessageBox.information(self, "Success", "Reservation updated successfully!")
            else:
                reservation_queries.ReservationQueries.create_reservation(
                    building, roomno, course_id, dept_id, activity_type,
                    instructor_id, date, start, end, hours
                )
                QMessageBox.information(self, "Success", "Reservation created successfully!")
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save reservation:\n{str(e)}")
