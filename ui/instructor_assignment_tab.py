from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QHeaderView, QMessageBox, QGroupBox
)
from db import reservation_queries


class InstructorAssignmentTab(QWidget):
    """Tab for viewing instructor assignments and workload"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_instructors()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Instructor Assignments & Workload")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Instructor selection
        select_layout = QHBoxLayout()
        
        select_layout.addWidget(QLabel("Select Instructor:"))
        
        self.instructor_combo = QComboBox()
        self.instructor_combo.currentIndexChanged.connect(self.on_instructor_changed)
        select_layout.addWidget(self.instructor_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_instructors)
        select_layout.addWidget(refresh_btn)
        
        select_layout.addStretch()
        
        layout.addLayout(select_layout)
        
        # Workload summary group
        workload_group = QGroupBox("Workload Summary")
        workload_layout = QHBoxLayout()
        
        self.total_reservations_label = QLabel("Total Reservations: -")
        self.total_hours_label = QLabel("Total Hours: -")
        self.courses_count_label = QLabel("Courses: -")
        
        workload_layout.addWidget(self.total_reservations_label)
        workload_layout.addWidget(self.total_hours_label)
        workload_layout.addWidget(self.courses_count_label)
        workload_layout.addStretch()
        
        workload_group.setLayout(workload_layout)
        layout.addWidget(workload_group)
        
        # Assignments table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Start", "End", "Hours", "Course", "Activity", "Room"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def load_instructors(self):
        """Load all instructors into combo box"""
        instructors = reservation_queries.ReservationQueries.get_all_instructors()
        
        self.instructor_combo.clear()
        self.instructor_data = {}
        
        for instructor_id, name in instructors:
            self.instructor_combo.addItem(name)
            self.instructor_data[name] = instructor_id
        
        if instructors:
            self.on_instructor_changed()
    
    def on_instructor_changed(self):
        """Load assignments for selected instructor"""
        if not self.instructor_combo.currentText():
            return
        
        instructor_name = self.instructor_combo.currentText()
        instructor_id = self.instructor_data.get(instructor_name)
        
        if not instructor_id:
            return
        
        # Load workload summary
        workload = reservation_queries.ReservationQueries.get_instructor_workload(instructor_id)
        
        if workload:
            total_reservations, total_hours, courses_count = workload
            self.total_reservations_label.setText(f"Total Reservations: {total_reservations or 0}")
            self.total_hours_label.setText(f"Total Hours: {total_hours or 0:.2f}")
            self.courses_count_label.setText(f"Courses: {courses_count or 0}")
        
        # Load all assignments (no date range limit for full view)
        from datetime import date, timedelta
        today = date.today()
        start_date = today - timedelta(days=365)  # Last year
        end_date = today + timedelta(days=365)    # Next year
        
        assignments = reservation_queries.ReservationQueries.get_instructor_schedule(
            instructor_id, start_date, end_date
        )
        
        self.table.setRowCount(0)
        
        for row_data in assignments:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)
            
            # Format data: date, start_time, end_time, course_name, activity_type, building, roomno, hours
            display_data = [
                str(row_data[0]),  # date
                str(row_data[1])[:5],  # start time (HH:MM)
                str(row_data[2])[:5],  # end time (HH:MM)
                str(row_data[7]),  # hours
                str(row_data[3]),  # course name
                str(row_data[4]),  # activity type
                f"{row_data[5]}{row_data[6]}"  # building + room
            ]
            
            for col_num, data in enumerate(display_data):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)
