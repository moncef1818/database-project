from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.department_crud_view import DepartmentView
from ui.instructor_crud_view import InstructorView  # type: ignore
from ui.room_crud_view import RoomView
from ui.student_crud_view import StudentView


class CrudView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.menu_page = QWidget()
        self.setup_menu_page()
        self.stack.addWidget(self.menu_page)

        self.dept_view = DepartmentView()
        self.stack.addWidget(self.dept_view)

        self.student_view = StudentView()
        self.stack.addWidget(self.student_view)

        self.room_view = RoomView()
        self.stack.addWidget(self.room_view)

        self.instructor_view = InstructorView()
        self.stack.addWidget(self.instructor_view)

        self.stack.setCurrentIndex(0)

    def setup_menu_page(self):
        grid = QGridLayout(self.menu_page)

        tables = [
            ("Department", 0, 0),
            ("Student", 0, 1),
            ("Instructor", 1, 0),
            ("Room", 1, 1),
        ]

        for name, row, col in tables:
            btn = QPushButton(name)
            btn.setFixedSize(150, 100)
            btn.clicked.connect(lambda checked, n=name: self.open_crud(n))
            grid.addWidget(btn, row, col)

    def open_crud(self, table_name):
        print(f"Opening CRUD for {table_name}")
        if table_name == "Department":
            self.stack.setCurrentWidget(self.dept_view)
        if table_name == "Student":
            self.stack.setCurrentWidget(self.student_view)
        if table_name == "Room":
            self.stack.setCurrentWidget(self.room_view)
        if table_name == "Instructor":
            self.stack.setCurrentWidget(self.instructor_view)
