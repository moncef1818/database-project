from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QFormLayout,
    QMessageBox,
    QHeaderView,
    QComboBox,
    QDateEdit,
)
from PyQt5.QtCore import Qt, QDate
from db import semester_crud_queries


class SemesterView(QWidget):
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

        title = QLabel("Semester Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nSemester")
        btn_read = QPushButton("View All\nSemesters")
        btn_update = QPushButton("Update\nSemester")
        btn_delete = QPushButton("Delete\nSemester")
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

        title = QLabel("Create New Semester")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        self.create_name_input = QLineEdit()
        self.create_name_input.setPlaceholderText("e.g., Fall 2025, Spring 2026")
        self.create_name_input.setMaxLength(50)

        self.create_start_date = QDateEdit()
        self.create_start_date.setCalendarPopup(True)
        self.create_start_date.setDate(QDate.currentDate())
        self.create_start_date.setDisplayFormat("yyyy-MM-dd")

        self.create_end_date = QDateEdit()
        self.create_end_date.setCalendarPopup(True)
        self.create_end_date.setDate(QDate.currentDate().addMonths(4))
        self.create_end_date.setDisplayFormat("yyyy-MM-dd")

        form.addRow("Semester Name:*", self.create_name_input)
        form.addRow("Start Date:*", self.create_start_date)
        form.addRow("End Date:*", self.create_end_date)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Semester")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_save.clicked.connect(self.save_new_semester)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Semesters")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["ID", "Name", "Year"])
        self.search_field_combo.setFixedWidth(100)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "ID (Asc)",
                "ID (Desc)",
                "Name (A-Z)",
                "Name (Z-A)",
                "Start Date (Oldest)",
                "Start Date (Newest)",
                "End Date (Oldest)",
                "End Date (Newest)",
            ]
        )

        btn_search = QPushButton("Search")
        btn_search.setStyleSheet(
            "background-color: #3498db; color: white; padding: 8px;"
        )
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
        self.read_table.setColumnCount(4)
        self.read_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Start Date", "End Date"]
        )
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.read_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("Back to Menu")
        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def create_update_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Update Semester")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(4)
        self.update_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Start Date", "End Date"]
        )
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()

        self.update_id_label = QLabel("Select a semester above")

        self.update_name_input = QLineEdit()
        self.update_name_input.setMaxLength(50)

        self.update_start_date = QDateEdit()
        self.update_start_date.setCalendarPopup(True)
        self.update_start_date.setDisplayFormat("yyyy-MM-dd")

        self.update_end_date = QDateEdit()
        self.update_end_date.setCalendarPopup(True)
        self.update_end_date.setDisplayFormat("yyyy-MM-dd")

        form.addRow("ID:", self.update_id_label)
        form.addRow("Semester Name:*", self.update_name_input)
        form.addRow("Start Date:*", self.update_start_date)
        form.addRow("End Date:*", self.update_end_date)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Semester")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_update.clicked.connect(self.update_semester)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Semester")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(4)
        self.delete_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Start Date", "End Date"]
        )
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")

        btn_delete.setStyleSheet(
            "background-color: #e74c3c; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_delete.clicked.connect(self.delete_semester)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def save_new_semester(self):
        name = self.create_name_input.text().strip()
        start_date = self.create_start_date.date().toString("yyyy-MM-dd")
        end_date = self.create_end_date.date().toString("yyyy-MM-dd")

        if not name:
            QMessageBox.warning(self, "Validation Error", "Semester name is required!")
            return

        if self.create_start_date.date() >= self.create_end_date.date():
            QMessageBox.warning(
                self, "Validation Error", "Start date must be before end date!"
            )
            return

        success = semester_crud_queries.SemesterCRUD.create_semester(
            name, start_date, end_date
        )
        if success:
            QMessageBox.information(self, "Success", "Semester created successfully!")
            self.create_name_input.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self, "Error", "Failed to create semester—check DB constraints."
            )

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = "semester_id", "ASC"
        elif sort_index == 1:
            sort_by, sort_order = "semester_id", "DESC"
        elif sort_index == 2:
            sort_by, sort_order = "name", "ASC"
        elif sort_index == 3:
            sort_by, sort_order = "name", "DESC"
        elif sort_index == 4:
            sort_by, sort_order = "start_date", "ASC"
        elif sort_index == 5:
            sort_by, sort_order = "start_date", "DESC"
        elif sort_index == 6:
            sort_by, sort_order = "end_date", "ASC"
        else:
            sort_by, sort_order = "end_date", "DESC"

        results = semester_crud_queries.SemesterCRUD.get_all_semesters(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.read_table.setRowCount(len(results))
        for row_idx, semester in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(semester[0])))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(semester[1]))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(str(semester[2])))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(str(semester[3])))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        semester_id = int(self.update_table.item(row, 0).text())
        name = self.update_table.item(row, 1).text()
        start_date = self.update_table.item(row, 2).text()
        end_date = self.update_table.item(row, 3).text()

        self.current_semester_id = semester_id
        self.update_id_label.setText(str(semester_id))
        self.update_name_input.setText(name)
        self.update_start_date.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        self.update_end_date.setDate(QDate.fromString(end_date, "yyyy-MM-dd"))

    def update_semester(self):
        if not hasattr(self, "current_semester_id"):
            QMessageBox.warning(self, "No Selection", "Please select a semester first!")
            return

        name = self.update_name_input.text().strip()
        start_date = self.update_start_date.date().toString("yyyy-MM-dd")
        end_date = self.update_end_date.date().toString("yyyy-MM-dd")

        if not name:
            QMessageBox.warning(self, "Validation Error", "Semester name is required!")
            return

        if self.update_start_date.date() >= self.update_end_date.date():
            QMessageBox.warning(
                self, "Validation Error", "Start date must be before end date!"
            )
            return

        success = semester_crud_queries.SemesterCRUD.update_semester(
            self.current_semester_id, name, start_date, end_date
        )
        if success:
            QMessageBox.information(self, "Success", "Semester updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update semester!")

    def delete_semester(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select a semester to delete!"
            )
            return

        row = selected[0].row()
        semester_id = int(self.delete_table.item(row, 0).text())
        semester_name = self.delete_table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{semester_name}' (ID: {semester_id})?\n\n"
            f"Warning: This will affect all enrollments and grades in this semester!",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success = semester_crud_queries.SemesterCRUD.delete_semester(semester_id)
            if success:
                QMessageBox.information(
                    self, "Success", "Semester deleted successfully!"
                )
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete semester!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = semester_crud_queries.SemesterCRUD.get_all_semesters()
        self.update_table.setRowCount(len(results))
        for row_idx, semester in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(semester[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(semester[1]))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(semester[2])))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(str(semester[3])))

        self.update_id_label.setText("Select a semester above")
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = semester_crud_queries.SemesterCRUD.get_all_semesters()
        self.delete_table.setRowCount(len(results))
        for row_idx, semester in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(semester[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(semester[1]))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(str(semester[2])))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(str(semester[3])))

        self.stack.setCurrentIndex(4)
