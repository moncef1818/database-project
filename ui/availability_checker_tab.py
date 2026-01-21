from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QDateEdit, QTimeEdit, QSpinBox, QHeaderView,
    QFormLayout, QGroupBox, QMessageBox
)
from db import reservation_queries


class AvailabilityCheckerTab(QWidget):
    """Tab for checking room availability"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Room Availability Checker")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search criteria group
        criteria_group = QGroupBox("Search Criteria")
        criteria_layout = QFormLayout()
        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        criteria_layout.addRow("Date:", self.date_edit)
        
        # Start time
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime(8, 0))
        criteria_layout.addRow("Start Time:", self.start_time_edit)
        
        # End time
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime(10, 0))
        criteria_layout.addRow("End Time:", self.end_time_edit)
        
        # Minimum capacity
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setMinimum(0)
        self.capacity_spin.setMaximum(500)
        self.capacity_spin.setValue(0)
        self.capacity_spin.setSpecialValueText("Any")
        criteria_layout.addRow("Min Capacity:", self.capacity_spin)
        
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        # Search button
        search_btn = QPushButton("Find Available Rooms")
        search_btn.clicked.connect(self.search_available_rooms)
        layout.addWidget(search_btn)
        
        # Results table
        # Results table
        results_label = QLabel("Available Rooms:")
        results_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(results_label)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)  # ← CHANGED: was 4
        self.results_table.setHorizontalHeaderLabels([
            "Building", "Room No", "Capacity"  # ← CHANGED: removed "Type"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.results_table)

        
        # Summary label
        self.summary_label = QLabel("No search performed yet")
        self.summary_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.summary_label)
    
    def search_available_rooms(self):
        """Search for available rooms"""
        # Validate time range
        if self.start_time_edit.time() >= self.end_time_edit.time():
            QMessageBox.warning(self, "Invalid Time", "End time must be after start time!")
            return
        
        # Get search parameters
        date = self.date_edit.date().toString("yyyy-MM-dd")
        start = self.start_time_edit.time().toString("HH:mm:ss")
        end = self.end_time_edit.time().toString("HH:mm:ss")
        min_capacity = self.capacity_spin.value() if self.capacity_spin.value() > 0 else None
        
        # Search
        available_rooms = reservation_queries.ReservationQueries.get_available_rooms(
            date, start, end, min_capacity
        )
        
        # Display results
        self.results_table.setRowCount(0)
        
        for row_data in available_rooms:
            row_num = self.results_table.rowCount()
            self.results_table.insertRow(row_num)
            
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data) if data is not None else "")
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.results_table.setItem(row_num, col_num, item)
        
        # Update summary
        count = len(available_rooms)
        date_str = self.date_edit.date().toString("dd/MM/yyyy")
        time_str = f"{self.start_time_edit.time().toString('HH:mm')} - {self.end_time_edit.time().toString('HH:mm')}"
        
        if count > 0:
            self.summary_label.setText(
                f"✅ Found {count} available room(s) on {date_str} from {time_str}"
            )
            self.summary_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.summary_label.setText(
                f"❌ No rooms available on {date_str} from {time_str}"
            )
            self.summary_label.setStyleSheet("color: red; font-weight: bold;")
