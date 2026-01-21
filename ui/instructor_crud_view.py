# New file: ui/instructor_crud_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QStackedWidget, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QFormLayout,
                             QMessageBox, QHeaderView, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt
from db import instructor_crud_queries

class InstructorView(QWidget):
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

        title = QLabel("Instructor Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nInstructor")
        btn_read = QPushButton("View All\nInstructors")
        btn_update = QPushButton("Update\nInstructor")
        btn_delete = QPushButton("Delete\nInstructor")
        btn_back = QPushButton("← Back to Core Data")

        for btn in [btn_create, btn_read, btn_update, btn_delete]:
            btn.setFixedSize(180, 120)
            
        grid.addWidget(btn_create, 0, 0)
        grid.addWidget(btn_read, 0, 1)
        grid.addWidget(btn_update, 1, 0)
        grid.addWidget(btn_delete, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()
        layout.addWidget(btn_back)

        btn_create.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_read.clicked.connect(self.show_read_screen)
        btn_update.clicked.connect(self.show_update_screen)
        btn_delete.clicked.connect(self.show_delete_screen)

        return menu

    def create_create_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Create New Instructor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        self.create_department_id_input = QSpinBox()
        self.create_department_id_input.setMinimum(1)
        self.create_department_id_input.setMaximum(9999)

        self.create_last_name_input = QLineEdit()
        self.create_last_name_input.setPlaceholderText("e.g., Djoudi")
        self.create_last_name_input.setMaxLength(25)

        self.create_first_name_input = QLineEdit()
        self.create_first_name_input.setPlaceholderText("e.g., Karim")
        self.create_first_name_input.setMaxLength(25)

        self.create_rank_combo = QComboBox()
        self.create_rank_combo.addItems(['Substitute', 'MCB', 'MCA', 'PROF'])

        self.create_phone_input = QLineEdit()
        self.create_phone_input.setPlaceholderText("e.g., 0556789012")
        self.create_phone_input.setMaxLength(10)

        self.create_fax_input = QLineEdit()
        self.create_fax_input.setPlaceholderText("e.g., 0556789013")
        self.create_fax_input.setMaxLength(10)

        self.create_email_input = QLineEdit()
        self.create_email_input.setPlaceholderText("e.g., karim.djoudi@ensc.dz")
        self.create_email_input.setMaxLength(100)

        form.addRow("Department ID:*", self.create_department_id_input)
        form.addRow("Last Name:*", self.create_last_name_input)
        form.addRow("First Name:*", self.create_first_name_input)
        form.addRow("Rank:", self.create_rank_combo)
        form.addRow("Phone:", self.create_phone_input)
        form.addRow("Fax:", self.create_fax_input)
        form.addRow("Email:", self.create_email_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Instructor")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_save.clicked.connect(self.save_new_instructor)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Instructors")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["ID", "Last Name", "First Name", "Rank", "Email"])
        self.search_field_combo.setFixedWidth(100)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["ID (Asc)", "ID (Desc)", "Last Name (A-Z)", "Last Name (Z-A)",
                                  "First Name (A-Z)", "First Name (Z-A)", "Rank (Asc)", "Rank (Desc)"])

        btn_search = QPushButton("Search")
        btn_search.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        btn_search.clicked.connect(self.perform_search)

        controls.addWidget(search_label)
        controls.addWidget(self.search_field_combo)
        controls.addWidget(search_input_label)
        controls.addWidget(self.search_input)
        controls.addWidget(sort_label)
        controls.addWidget(self.sort_combo)
        controls.addWidget(btn_search)

        layout.addLayout(controls)

        self.read_table = QTableWidget()
        self.read_table.setColumnCount(8)
        self.read_table.setHorizontalHeaderLabels(["ID", "Dept ID", "Last Name", "First Name", "Rank", "Phone", "Fax", "Email"])
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.read_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("Back to Menu")
        btn_back.setStyleSheet("background-color: #34495e; color: white; padding: 10px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def create_update_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Update Instructor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(8)
        self.update_table.setHorizontalHeaderLabels(["ID", "Dept ID", "Last Name", "First Name", "Rank", "Phone", "Fax", "Email"])
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()

        self.update_id_label = QLabel("Select an instructor above")

        self.update_department_id_input = QSpinBox()
        self.update_department_id_input.setMinimum(1)
        self.update_department_id_input.setMaximum(9999)

        self.update_last_name_input = QLineEdit()
        self.update_last_name_input.setMaxLength(25)

        self.update_first_name_input = QLineEdit()
        self.update_first_name_input.setMaxLength(25)

        self.update_rank_combo = QComboBox()
        self.update_rank_combo.addItems(['Substitute', 'MCB', 'MCA', 'PROF'])

        self.update_phone_input = QLineEdit()
        self.update_phone_input.setMaxLength(10)

        self.update_fax_input = QLineEdit()
        self.update_fax_input.setMaxLength(10)

        self.update_email_input = QLineEdit()
        self.update_email_input.setMaxLength(100)

        form.addRow("ID:", self.update_id_label)
        form.addRow("Department ID:*", self.update_department_id_input)
        form.addRow("Last Name:*", self.update_last_name_input)
        form.addRow("First Name:*", self.update_first_name_input)
        form.addRow("Rank:", self.update_rank_combo)
        form.addRow("Phone:", self.update_phone_input)
        form.addRow("Fax:", self.update_fax_input)
        form.addRow("Email:", self.update_email_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Instructor")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_update.clicked.connect(self.update_instructor)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Instructor")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(8)
        self.delete_table.setHorizontalHeaderLabels(["ID", "Dept ID", "Last Name", "First Name", "Rank", "Phone", "Fax", "Email"])
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")

        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_delete.clicked.connect(self.delete_instructor)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def save_new_instructor(self):
        department_id = self.create_department_id_input.value()
        last_name = self.create_last_name_input.text().strip()
        first_name = self.create_first_name_input.text().strip()
        rank = self.create_rank_combo.currentText()
        phone = self.create_phone_input.text().strip() or None
        fax = self.create_fax_input.text().strip() or None
        email = self.create_email_input.text().strip() or None

        if not department_id or not last_name or not first_name:
            QMessageBox.warning(self, "Validation Error", "Department ID, Last Name, and First Name are required!")
            return

        success = instructor_crud_queries.InstructorCRUD.create_instructor(
            department_id, last_name, first_name, rank, phone, fax, email
        )
        if success:
            QMessageBox.information(self, "Success", "Instructor created successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to create instructor—check FK or DB issue.")

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = 'instructor_id', 'ASC'
        elif sort_index == 1:
            sort_by, sort_order = 'instructor_id', 'DESC'
        elif sort_index == 2:
            sort_by, sort_order = 'last_name', 'ASC'
        elif sort_index == 3:
            sort_by, sort_order = 'last_name', 'DESC'
        elif sort_index == 4:
            sort_by, sort_order = 'first_name', 'ASC'
        elif sort_index == 5:
            sort_by, sort_order = 'first_name', 'DESC'
        elif sort_index == 6:
            sort_by, sort_order = 'rank', 'ASC'
        else:
            sort_by, sort_order = 'rank', 'DESC'

        results = instructor_crud_queries.InstructorCRUD.get_all_instructors(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order
        )

        self.read_table.setRowCount(len(results))
        for row_idx, instructor in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(instructor[0])))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(str(instructor[1])))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(instructor[2]))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(instructor[3]))
            self.read_table.setItem(row_idx, 4, QTableWidgetItem(instructor[4] or ""))
            self.read_table.setItem(row_idx, 5, QTableWidgetItem(instructor[5] or ""))
            self.read_table.setItem(row_idx, 6, QTableWidgetItem(instructor[6] or ""))
            self.read_table.setItem(row_idx, 7, QTableWidgetItem(instructor[7] or ""))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        instructor_id = int(self.update_table.item(row, 0).text())
        department_id = int(self.update_table.item(row, 1).text())
        last_name = self.update_table.item(row, 2).text()
        first_name = self.update_table.item(row, 3).text()
        rank = self.update_table.item(row, 4).text()
        phone = self.update_table.item(row, 5).text()
        fax = self.update_table.item(row, 6).text()
        email = self.update_table.item(row, 7).text()

        self.current_instructor_id = instructor_id
        self.update_id_label.setText(str(instructor_id))
        self.update_department_id_input.setValue(department_id)
        self.update_last_name_input.setText(last_name)
        self.update_first_name_input.setText(first_name)
        self.update_rank_combo.setCurrentText(rank)
        self.update_phone_input.setText(phone)
        self.update_fax_input.setText(fax)
        self.update_email_input.setText(email)

    def update_instructor(self):
        if not hasattr(self, 'current_instructor_id'):
            QMessageBox.warning(self, "No Selection", "Please select an instructor first!")
            return

        department_id = self.update_department_id_input.value()
        last_name = self.update_last_name_input.text().strip()
        first_name = self.update_first_name_input.text().strip()
        rank = self.update_rank_combo.currentText()
        phone = self.update_phone_input.text().strip() or None
        fax = self.update_fax_input.text().strip() or None
        email = self.update_email_input.text().strip() or None

        if not department_id or not last_name or not first_name:
            QMessageBox.warning(self, "Validation Error", "Department ID, Last Name, and First Name are required!")
            return

        success = instructor_crud_queries.InstructorCRUD.update_instructor(
            self.current_instructor_id, department_id, last_name, first_name, rank, phone, fax, email
        )
        if success:
            QMessageBox.information(self, "Success", "Instructor updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update instructor!")

    def delete_instructor(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select an instructor to delete!")
            return

        row = selected[0].row()
        instructor_id = int(self.delete_table.item(row, 0).text())
        last_name = self.delete_table.item(row, 2).text()
        first_name = self.delete_table.item(row, 3).text()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{first_name} {last_name}' (ID: {instructor_id})?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = instructor_crud_queries.InstructorCRUD.delete_instructor(instructor_id)
            if success:
                QMessageBox.information(self, "Success", "Instructor deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete instructor!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = instructor_crud_queries.InstructorCRUD.get_all_instructors()
        self.update_table.setRowCount(len(results))
        for row_idx, instructor in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(instructor[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(str(instructor[1])))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(instructor[2]))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(instructor[3]))
            self.update_table.setItem(row_idx, 4, QTableWidgetItem(instructor[4] or ""))
            self.update_table.setItem(row_idx, 5, QTableWidgetItem(instructor[5] or ""))
            self.update_table.setItem(row_idx, 6, QTableWidgetItem(instructor[6] or ""))
            self.update_table.setItem(row_idx, 7, QTableWidgetItem(instructor[7] or ""))

        self.update_id_label.setText("Select an instructor above")
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = instructor_crud_queries.InstructorCRUD.get_all_instructors()
        self.delete_table.setRowCount(len(results))
        for row_idx, instructor in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(instructor[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(str(instructor[1])))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(instructor[2]))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(instructor[3]))
            self.delete_table.setItem(row_idx, 4, QTableWidgetItem(instructor[4] or ""))
            self.delete_table.setItem(row_idx, 5, QTableWidgetItem(instructor[5] or ""))
            self.delete_table.setItem(row_idx, 6, QTableWidgetItem(instructor[6] or ""))
            self.delete_table.setItem(row_idx, 7, QTableWidgetItem(instructor[7] or ""))

        self.stack.setCurrentIndex(4)
