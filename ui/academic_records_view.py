from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.attendance_crud_view import AttendanceCrudView
from ui.grade_crud_view import GradeCrudView


class AcademicRecordsView(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("Academic Records Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)


        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)


        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)


        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)


        grid = QGridLayout()


        btn_grades = QPushButton("📊 Manage Grades")
        btn_grades.setFixedSize(200, 80)
        btn_grades.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        )
        btn_grades.clicked.connect(self.show_grades_crud)
        grid.addWidget(btn_grades, 0, 0)


        btn_attendance = QPushButton("Manage Attendance")
        btn_attendance.setFixedSize(200, 80)
        btn_attendance.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """
        )
        btn_attendance.clicked.connect(self.show_attendance_crud)
        grid.addWidget(btn_attendance, 0, 1)

        layout.addLayout(grid)
        layout.addStretch()


        btn_back = QPushButton("← Back to Main Menu")
        btn_back.setStyleSheet(
            """
            background-color: #34495e;
            color: white;
            padding: 10px;
            font-size: 12px;
            border-radius: 5px;
        """
        )
        btn_back.clicked.connect(self.go_back_to_main)
        layout.addWidget(btn_back)

        return menu_widget

    def show_grades_crud(self):
        """
        Displays the Grades CRUD view.
        Creates new instance if needed and switches to it.
        """
        grades_crud = GradeCrudView(parent=self)

        self.stack.addWidget(grades_crud)
        self.stack.setCurrentWidget(grades_crud)

    def show_attendance_crud(self):

        # Create attendance CRUD view with self as parent
        attendance_crud = AttendanceCrudView(parent=self)

        # Add to stack (index 2+)
        self.stack.addWidget(attendance_crud)
        self.stack.setCurrentWidget(attendance_crud)

    def go_back_to_main(self):
        """
        Returns to the main application menu.
        Navigates through parent hierarchy to find main window.
        """
        main_window = self.window()  # Gets top-level window
        if hasattr(main_window, "content_stack"):
            main_window.content_stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(0)

    def show_menu(self):

        # Remove all CRUD views from stack (keep only menu)
        while self.stack.count() > 1:
            widget = self.stack.widget(1)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        # Show menu
        self.stack.setCurrentIndex(0)
