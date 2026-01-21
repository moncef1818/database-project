from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from db import room_crud_queries


class RoomView(QWidget):
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

        title = QLabel("Room Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nRoom")
        btn_read = QPushButton("View All\nRooms")
        btn_update = QPushButton("Update\nRoom")
        btn_delete = QPushButton("Delete\nRoom")
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

        title = QLabel("Create New Room")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        self.create_building_input = QLineEdit()
        self.create_building_input.setPlaceholderText("e.g., A")
        self.create_building_input.setMaxLength(1)

        self.create_roomno_input = QLineEdit()
        self.create_roomno_input.setPlaceholderText("e.g., 101")
        self.create_roomno_input.setMaxLength(20)

        self.create_capacity_input = QSpinBox()
        self.create_capacity_input.setMinimum(1)
        self.create_capacity_input.setMaximum(9999)
        self.create_capacity_input.setValue(1)

        form.addRow("Building:*", self.create_building_input)
        form.addRow("Room Number:*", self.create_roomno_input)
        form.addRow("Capacity:*", self.create_capacity_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Room")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_save.clicked.connect(self.save_new_room)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Rooms")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["Building", "RoomNo", "Capacity"])
        self.search_field_combo.setFixedWidth(100)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "Building (A-Z)",
                "Building (Z-A)",
                "RoomNo (Asc)",
                "RoomNo (Desc)",
                "Capacity (Asc)",
                "Capacity (Desc)",
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
        self.read_table.setColumnCount(3)
        self.read_table.setHorizontalHeaderLabels(["Building", "RoomNo", "Capacity"])
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

        title = QLabel("Update Room")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(3)
        self.update_table.setHorizontalHeaderLabels(["Building", "RoomNo", "Capacity"])
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(
            self.load_for_update
        )  # Changed from selectedIndexes to clicked for simplicity
        layout.addWidget(self.update_table)

        form = QFormLayout()
        self.update_building_label = QLabel("Select a room above")
        self.update_roomno_label = QLabel("")
        self.update_capacity_input = QSpinBox()
        self.update_capacity_input.setMinimum(1)
        self.update_capacity_input.setMaximum(9999)

        form.addRow("Building:", self.update_building_label)
        form.addRow("RoomNo:", self.update_roomno_label)
        form.addRow("Capacity:", self.update_capacity_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Room")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_update.clicked.connect(self.update_room)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Room")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(3)
        self.delete_table.setHorizontalHeaderLabels(["Building", "RoomNo", "Capacity"])
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

        btn_delete.clicked.connect(self.delete_room)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def save_new_room(self):
        building = self.create_building_input.text().strip().upper()
        roomno = self.create_roomno_input.text().strip()
        capacity = self.create_capacity_input.value()

        if not building or not roomno or capacity < 1:
            QMessageBox.warning(
                self, "Validation Error", "All fields required; capacity >=1!"
            )
            return

        success = room_crud_queries.RoomCRUD.create_room(building, roomno, capacity)
        if success:
            QMessageBox.information(
                self, "Success", f"Room '{building}-{roomno}' created!"
            )
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed—check if exists or DB issue.")

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = "building", "ASC"
        elif sort_index == 1:
            sort_by, sort_order = "building", "DESC"
        elif sort_index == 2:
            sort_by, sort_order = "roomno", "ASC"
        elif sort_index == 3:
            sort_by, sort_order = "roomno", "DESC"
        elif sort_index == 4:
            sort_by, sort_order = "capacity", "ASC"
        else:
            sort_by, sort_order = "capacity", "DESC"

        results = room_crud_queries.RoomCRUD.get_all_rooms(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.read_table.setRowCount(len(results))
        for row_idx, (building, roomno, capacity) in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(building))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(roomno))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(str(capacity)))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        building = self.update_table.item(row, 0).text()
        roomno = self.update_table.item(row, 1).text()
        capacity = int(self.update_table.item(row, 2).text())

        self.current_building = building
        self.current_roomno = roomno

        self.update_building_label.setText(building)
        self.update_roomno_label.setText(roomno)
        self.update_capacity_input.setValue(capacity)

    def update_room(self):
        if not hasattr(self, "current_building"):
            QMessageBox.warning(self, "No Selection", "Please select a room first!")
            return
        new_capacity = self.update_capacity_input.value()
        if new_capacity < 1:
            QMessageBox.warning(self, "Input Error", "Capacity must be at least 1.")
            return
        success = room_crud_queries.RoomCRUD.update_room(
            self.current_building, self.current_roomno, new_capacity
        )

        if success:
            QMessageBox.information(self, "Success", "Room updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update room!")

    def delete_room(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a room to delete!")
            return

        row = selected[0].row()
        building = self.delete_table.item(row, 0).text()
        roomno = self.delete_table.item(row, 1).text()

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete room '{building}-{roomno}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            success = room_crud_queries.RoomCRUD.delete_room(building, roomno)
            if success:
                QMessageBox.information(self, "Success", "Room deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete room!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = room_crud_queries.RoomCRUD.get_all_rooms()
        self.update_table.setRowCount(len(results))
        for row_idx, (building, roomno, capacity) in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(building))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(roomno))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(capacity)))

        self.update_building_label.setText("Select a room above")
        self.update_roomno_label.setText("")
        self.update_capacity_input.setValue(1)
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = room_crud_queries.RoomCRUD.get_all_rooms()
        self.delete_table.setRowCount(len(results))
        for row_idx, (building, roomno, capacity) in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(building))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(roomno))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(str(capacity)))

        self.stack.setCurrentIndex(4)
