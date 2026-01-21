from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QComboBox,
    QDateEdit,
)
from db import student_crud_queries


class StudentView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.operations_menu = self.create_operations_menu()
        self.stack.addWidget(self.operations_menu)

        self.create_screen = self.create_create_screen()
        self.stack.addWidget(self.create_screen)

        self.read_screen = self.create_read_screen()
        self.stack.addWidget(self.read_screen)

        self.update_screen = self.create_update_screen()
        self.stack.addWidget(self.update_screen)

        self.delete_screen = self.create_delete_screen()
        self.stack.addWidget(self.delete_screen)

        self.stack.setCurrentIndex(0)

    def create_operations_menu(self):
        menu = QWidget()
        layout = QVBoxLayout(menu)

        layout.addStretch(1)  # Centers content vertically

        title = QLabel("Student Operations")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignCenter)  # Centers buttons horizontally

        btn_create = QPushButton("Add New\nStudent")
        btn_read = QPushButton("View All\nStudents")
        btn_update = QPushButton("Update\nStudent")
        btn_delete = QPushButton("Delete\nStudent")

        for btn in [btn_create, btn_read, btn_update, btn_delete]:
            btn.setFixedSize(180, 120)
            
        grid.addWidget(btn_create, 0, 0)
        grid.addWidget(btn_read, 0, 1)
        grid.addWidget(btn_update, 1, 0)
        grid.addWidget(btn_delete, 1, 1)
        layout.addLayout(grid)

        layout.addStretch(1)

        btn_create.clicked.connect(self.show_create_screen)
        btn_read.clicked.connect(self.show_read_screen)
        btn_update.clicked.connect(self.show_update_screen)
        btn_delete.clicked.connect(self.show_delete_screen)

        return menu

    def create_create_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        layout.addWidget(
            QLabel(
                "Register New Student", styleSheet="font-size: 16px; font-weight: bold;"
            )
        )

        form = QFormLayout()
        self.c_fname = QLineEdit()
        self.c_lname = QLineEdit()
        self.c_dob = QDateEdit(calendarPopup=True)
        self.c_dob.setDisplayFormat("yyyy-MM-dd")
        self.c_group_combo = QComboBox()
        self.c_email = QLineEdit()
        self.c_phone = QLineEdit()
        self.c_address = QLineEdit()
        self.c_city = QLineEdit()
        self.c_zip = QLineEdit()

        form.addRow("First Name:*", self.c_fname)
        form.addRow("Last Name:*", self.c_lname)
        form.addRow("DOB:*", self.c_dob)
        form.addRow("Group:", self.c_group_combo)
        form.addRow("Email:", self.c_email)
        form.addRow("Phone:", self.c_phone)
        form.addRow("Address:", self.c_address)
        form.addRow("City:", self.c_city)
        form.addRow("Zip:", self.c_zip)
        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_save = QPushButton("Save Student")
        btn_save.clicked.connect(self.save_student)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        controls = QHBoxLayout()
        self.search_field = QComboBox()
        self.search_field.addItems(["Student ID", "Last Name", "Group"])
        self.search_input = QLineEdit()
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.perform_search)
        controls.addWidget(self.search_field)
        controls.addWidget(self.search_input)
        controls.addWidget(btn_search)
        layout.addLayout(controls)

        self.read_table = QTableWidget(0, 9)
        self.read_table.setHorizontalHeaderLabels(
            ["ID", "First", "Last", "DOB", "Group", "Section", "Email", "Phone", "GID"]
        )
        self.read_table.hideColumn(8)
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)
        return screen

    def create_update_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        self.update_table = QTableWidget(0, 9)
        self.update_table.setHorizontalHeaderLabels(
            ["ID", "First", "Last", "DOB", "Group", "Section", "Email", "Phone", "GID"]
        )
        self.update_table.hideColumn(8)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_student_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()
        self.u_id_lbl = QLabel("Select student...")
        self.u_fname = QLineEdit()
        self.u_lname = QLineEdit()
        self.u_dob = QDateEdit(calendarPopup=True)
        self.u_dob.setDisplayFormat("yyyy-MM-dd")
        self.u_group_combo = QComboBox()
        self.u_email = QLineEdit()
        self.u_phone = QLineEdit()
        form.addRow("ID:", self.u_id_lbl)
        form.addRow("First:", self.u_fname)
        form.addRow("Last:", self.u_lname)
        form.addRow("DOB:", self.u_dob)
        form.addRow("Group:", self.u_group_combo)
        form.addRow("Email:", self.u_email)
        form.addRow("Phone:", self.u_phone)
        layout.addLayout(form)

        btn_upd = QPushButton("Update")
        btn_upd.clicked.connect(self.update_student)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_upd)
        layout.addWidget(btn_back)
        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)
        self.delete_table = QTableWidget(0, 9)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)
        btn_del = QPushButton("Delete Selected")
        btn_del.clicked.connect(self.delete_student)
        layout.addWidget(btn_del)
        layout.addWidget(
            QPushButton("Back", clicked=lambda: self.stack.setCurrentIndex(0))
        )
        return screen

    def load_groups_combo(self, combo):
        combo.clear()
        combo.addItem("No Group", 0)
        groups = student_crud_queries.StudentCRUD.get_all_groups()
        for g_id, g_name, s_name in groups:
            combo.addItem(f"{s_name} - {g_name}", g_id)

    def show_create_screen(self):
        self.load_groups_combo(self.c_group_combo)
        self.stack.setCurrentIndex(1)

    def show_read_screen(self):
        self.perform_search(self.read_table)
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        self.load_groups_combo(self.u_group_combo)
        self.perform_search(self.update_table)
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        self.perform_search(self.delete_table)
        self.stack.setCurrentIndex(4)

    def save_student(self):
        success = student_crud_queries.StudentCRUD.create_student(
            self.c_fname.text(),
            self.c_lname.text(),
            self.c_dob.date().toString("yyyy-MM-dd"),
            self.c_group_combo.currentData(),
            self.c_email.text(),
            self.c_phone.text(),
            self.c_address.text(),
            self.c_city.text(),
            self.c_zip.text(),
        )
        if success:
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to create.")

    def perform_search(self, target_table=None):
        if not target_table:
            target_table = self.read_table
        results = student_crud_queries.StudentCRUD.get_all_students(
            self.search_field.currentText(), self.search_input.text()
        )
        target_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, val in enumerate(data):
                target_table.setItem(
                    row, col, QTableWidgetItem(str(val) if val is not None else "")
                )

    def load_student_for_update(self):
        selected = self.update_table.selectedItems()
        if not selected:
            return
        sid = int(self.update_table.item(selected[0].row(), 0).text())
        details = student_crud_queries.StudentCRUD.get_student_details(sid)
        if details:
            self.current_student_id = sid
            self.u_id_lbl.setText(str(sid))
            self.u_fname.setText(details[0])
            self.u_lname.setText(details[1])
            self.u_dob.setDate(QDate.fromString(str(details[2]), "yyyy-MM-dd"))
            idx = self.u_group_combo.findData(details[3])
            self.u_group_combo.setCurrentIndex(idx if idx >= 0 else 0)
            self.u_email.setText(details[4] or "")
            self.u_phone.setText(details[5] or "")

    def update_student(self):
        if not hasattr(self, "current_student_id"):
            return
        success = student_crud_queries.StudentCRUD.update_student(
            self.current_student_id,
            self.u_fname.text(),
            self.u_lname.text(),
            self.u_dob.date().toString("yyyy-MM-dd"),
            self.u_group_combo.currentData(),
            self.u_email.text(),
            self.u_phone.text(),
            "",
            "",
            "",
        )
        if success:
            self.stack.setCurrentIndex(0)

    def delete_student(self):
        selected = self.delete_table.selectedItems()
        if not selected:
            return
        sid = int(self.delete_table.item(selected[0].row(), 0).text())
        if student_crud_queries.StudentCRUD.delete_student(sid):
            self.perform_search(self.delete_table)
