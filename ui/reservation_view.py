from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.reservation_crud_tab import ReservationCRUDTab
from ui.instructor_assignment_tab import InstructorAssignmentTab
from ui.availability_checker_tab import AvailabilityCheckerTab
from ui.schedule_viewer_tab import ScheduleViewerTab


class ReservationView(QWidget):
    """Main container for Reservation & Module Assignment submenu"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.crud_tab = ReservationCRUDTab()
        self.assignment_tab = InstructorAssignmentTab()
        self.availability_tab = AvailabilityCheckerTab()
        self.schedule_tab = ScheduleViewerTab()
        
        self.tabs.addTab(self.crud_tab, "Reservations")
        self.tabs.addTab(self.assignment_tab, "Instructor Assignments")
        self.tabs.addTab(self.availability_tab, "Room Availability")
        self.tabs.addTab(self.schedule_tab, "Schedules")
        
        layout.addWidget(self.tabs)
