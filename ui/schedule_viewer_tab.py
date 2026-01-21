from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QDateEdit, QHeaderView, QGroupBox,
    QFormLayout, QRadioButton, QButtonGroup
)
from datetime import datetime, timedelta
from db import reservation_queries


class ScheduleViewerTab(QWidget):
    """Tab for viewing schedules (by instructor or room)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Schedule Viewer")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # View type selection
        view_type_group = QGroupBox("View Type")
        view_type_layout = QHBoxLayout()
        
        self.view_type_group = QButtonGroup()
        
        self.instructor_radio = QRadioButton("Instructor Schedule")
        self.instructor_radio.setChecked(True)
        self.instructor_radio.toggled.connect(self.on_view_type_changed)
        
        self.room_radio = QRadioButton("Room Schedule")
        self.room_radio.toggled.connect(self.on_view_type_changed)
        
        self.view_type_group.addButton(self.instructor_radio)
        self.view_type_group.addButton(self.room_radio)
        
        view_type_layout.addWidget(self.instructor_radio)
        view_type_layout.addWidget(self.room_radio)
        view_type_layout.addStretch()
        
        view_type_group.setLayout(view_type_layout)
        layout.addWidget(view_type_group)
        
        # Selection criteria
        criteria_group = QGroupBox("Selection")
        criteria_layout = QFormLayout()
        
        # Instructor combo
        self.instructor_combo = QComboBox()
        instructors = reservation_queries.ReservationQueries.get_all_instructors()
        self.instructor_data = {}
        for instructor_id, name in instructors:
            self.instructor_combo.addItem(name)
            self.instructor_data[name] = instructor_id
        criteria_layout.addRow("Instructor:", self.instructor_combo)
        
        # Room combo
        # Room combo
        self.room_combo = QComboBox()
        rooms = reservation_queries.ReservationQueries.get_all_rooms()
        self.room_data = {}
        for building, roomno, capacity in rooms:  # ← CHANGED: removed room_type
            display_text = f"{building}{roomno} (Cap: {capacity})"  # ← CHANGED: removed type display
            self.room_combo.addItem(display_text)
            self.room_data[display_text] = (building, roomno)
        self.room_combo.setEnabled(False)
        criteria_layout.addRow("Room:", self.room_combo)

        
        # Date range
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        criteria_layout.addRow("Start Date:", self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(7))
        criteria_layout.addRow("End Date:", self.end_date_edit)
        
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        # Quick date range buttons
        quick_layout = QHBoxLayout()
        
        today_btn = QPushButton("Today")
        today_btn.clicked.connect(self.set_today)
        
        week_btn = QPushButton("This Week")
        week_btn.clicked.connect(self.set_this_week)
        
        month_btn = QPushButton("This Month")
        month_btn.clicked.connect(self.set_this_month)
        
        quick_layout.addWidget(today_btn)
        quick_layout.addWidget(week_btn)
        quick_layout.addWidget(month_btn)
        quick_layout.addStretch()
        
        layout.addLayout(quick_layout)
        
        # View button
        view_btn = QPushButton("View Schedule")
        view_btn.clicked.connect(self.view_schedule)
        layout.addWidget(view_btn)
        
        # Schedule table
        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
    
    def on_view_type_changed(self):
        """Toggle between instructor and room view"""
        if self.instructor_radio.isChecked():
            self.instructor_combo.setEnabled(True)
            self.room_combo.setEnabled(False)
        else:
            self.instructor_combo.setEnabled(False)
            self.room_combo.setEnabled(True)
    
    def set_today(self):
        """Set date range to today"""
        today = QDate.currentDate()
        self.start_date_edit.setDate(today)
        self.end_date_edit.setDate(today)
    
    def set_this_week(self):
        """Set date range to current week (Mon-Sun)"""
        today = QDate.currentDate()
        start_of_week = today.addDays(-(today.dayOfWeek() - 1))  # Monday
        end_of_week = start_of_week.addDays(6)  # Sunday
        
        self.start_date_edit.setDate(start_of_week)
        self.end_date_edit.setDate(end_of_week)
    
    def set_this_month(self):
        """Set date range to current month"""
        today = QDate.currentDate()
        start_of_month = QDate(today.year(), today.month(), 1)
        
        # Last day of month
        if today.month() == 12:
            end_of_month = QDate(today.year() + 1, 1, 1).addDays(-1)
        else:
            end_of_month = QDate(today.year(), today.month() + 1, 1).addDays(-1)
        
        self.start_date_edit.setDate(start_of_month)
        self.end_date_edit.setDate(end_of_month)
    
    def view_schedule(self):
        """View schedule based on selection"""
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        
        if self.instructor_radio.isChecked():
            self.view_instructor_schedule(start_date, end_date)
        else:
            self.view_room_schedule(start_date, end_date)
    
    def view_instructor_schedule(self, start_date, end_date):
        """View instructor schedule"""
        instructor_name = self.instructor_combo.currentText()
        if not instructor_name:
            return
        
        instructor_id = self.instructor_data.get(instructor_name)
        
        schedule = reservation_queries.ReservationQueries.get_instructor_schedule(
            instructor_id, start_date, end_date
        )
        
        # Configure table for instructor view
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Start", "End", "Hours", "Course", "Activity", "Room"
        ])
        
        self.table.setRowCount(0)
        
        for row_data in schedule:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)
            
            # Format: date, start_time, end_time, course_name, activity_type, building, roomno, hours
            display_data = [
                str(row_data[0]),  # date
                str(row_data[1])[:5],  # start time
                str(row_data[2])[:5],  # end time
                str(row_data[7]),  # hours
                str(row_data[3]),  # course name
                str(row_data[4]),  # activity type
                f"{row_data[5]}{row_data[6]}"  # room
            ]
            
            for col_num, data in enumerate(display_data):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)
    
    def view_room_schedule(self, start_date, end_date):
        """View room schedule"""
        room_text = self.room_combo.currentText()
        if not room_text:
            return
        
        building, roomno = self.room_data.get(room_text)
        
        schedule = reservation_queries.ReservationQueries.get_room_schedule(
            building, roomno, start_date, end_date
        )
        
        # Configure table for room view
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Date", "Start", "End", "Hours", "Course", "Activity", "Instructor"
        ])
        
        self.table.setRowCount(0)
        
        for row_data in schedule:
            row_num = self.table.rowCount()
            self.table.insertRow(row_num)
            
            # Format: date, start_time, end_time, course_name, activity_type, instructor_name, hours
            display_data = [
                str(row_data[0]),  # date
                str(row_data[1])[:5],  # start time
                str(row_data[2])[:5],  # end time
                str(row_data[6]),  # hours
                str(row_data[3]),  # course name
                str(row_data[4]),  # activity type
                str(row_data[5])  # instructor name
            ]
            
            for col_num, data in enumerate(display_data):
                item = QTableWidgetItem(data)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)
