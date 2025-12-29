from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.department_crud_view import DepartmentView
from ui.instructor_crud_view import InstructorView  
from ui.room_crud_view import RoomView
from ui.student_crud_view import StudentView
from ui.section_crud_view import SectionView  
from ui.group_crud_view import GroupView

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

        self.section_view = SectionView()
        self.stack.addWidget(self.section_view)

        self.group_view = GroupView()
        self.stack.addWidget(self.group_view)

        self.stack.setCurrentIndex(0)

    def setup_menu_page(self):
        grid = QGridLayout(self.menu_page)

        tables = [
            ("Department", 0, 0),
            ("Student", 0, 1),
            ("Instructor", 0, 2),
            ("Room", 1, 0),
            ("Section", 1, 1),
            ("Group", 1, 2),

        ]

        for name, row, col in tables:
            btn = QPushButton(name)
            btn.setFixedSize(150, 100)
            btn.clicked.connect(lambda checked, n=name: self.open_crud(n))
            grid.addWidget(btn, row, col)

    def open_crud(self, table_name):
        print(f"Opening CRUD for {table_name}")
        match table_name:
            case "Department":
                self.stack.setCurrentWidget(self.dept_view)
            case "Student":
                self.stack.setCurrentWidget(self.student_view)
            case "Room":
                self.stack.setCurrentWidget(self.room_view)
            case "Instructor":
                self.stack.setCurrentWidget(self.instructor_view)
            case "Section":
                self.stack.setCurrentWidget(self.section_view)
            case "Group":
                self.stack.setCurrentWidget(self.group_view)
        