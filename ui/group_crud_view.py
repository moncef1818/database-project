from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QStackedWidget, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QFormLayout,
                             QMessageBox, QHeaderView, QComboBox)
from PyQt5.QtCore import Qt
from db import group_crud_queries


class GroupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Screen 0: Operations Menu
        self.operations_menu = self.create_operations_menu()
        self.stack.addWidget(self.operations_menu)
        
        # Screen 1: Create
        self.create_screen = self.create_create_screen()
        self.stack.addWidget(self.create_screen)

        # Screen 2: Read
        self.read_screen = self.create_read_screen()
        self.stack.addWidget(self.read_screen)

        # Screen 3: Update
        self.update_screen = self.create_update_screen()
        self.stack.addWidget(self.update_screen)

        # Screen 4: Delete
        self.delete_screen = self.create_delete_screen()
        self.stack.addWidget(self.delete_screen)
        
        self.stack.setCurrentIndex(0)

    def create_operations_menu(self):
        menu = QWidget()
        layout = QVBoxLayout(menu)

        title = QLabel("Group Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        
        btn_create = QPushButton("Create New\nGroup")
        btn_read = QPushButton("View All\nGroups")
        btn_update = QPushButton("Update\nGroup")
        btn_delete = QPushButton("Delete\nGroup")
        btn_back = QPushButton("← Back to Core Data")

        for btn in [btn_create, btn_read, btn_update, btn_delete]:
            btn.setFixedSize(180, 120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-size: 14px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
        
        btn_back.setStyleSheet("background-color: #34495e; color: white; padding: 10px;")
        
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

        title = QLabel("Create New Group")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()

        # Section ComboBox
        self.create_section_id_input = QComboBox()
        self.load_sections_combo(self.create_section_id_input)
        form.addRow("Section:", self.create_section_id_input)

        # Group Name Input
        self.create_name_input = QLineEdit()
        self.create_name_input.setPlaceholderText("e.g., Group 1, Group 2")
        form.addRow("Group Name:", self.create_name_input)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Group")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_save.clicked.connect(self.save_new_group)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Groups")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Search and Sort Controls
        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["Group ID", "Group Name", "Section ID"])
        self.search_field_combo.setFixedWidth(120)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Group ID (Ascending)", "Group ID (Descending)", 
            "Group Name (A-Z)", "Group Name (Z-A)",
            "Section ID (Ascending)", "Section ID (Descending)"
        ])
        
        btn_search = QPushButton("Search")
        btn_search.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        btn_search.clicked.connect(self.perform_search)

        controls.addWidget(search_label)
        controls.addWidget(self.search_field_combo)
        controls.addWidget(search_input_label)
        controls.addWidget(self.search_input)
        controls.addSpacing(20)
        controls.addWidget(sort_label)
        controls.addWidget(self.sort_combo)
        controls.addWidget(btn_search)
        controls.addStretch()

        layout.addLayout(controls)

        # Table
        self.read_table = QTableWidget()
        self.read_table.setColumnCount(4)
        self.read_table.setHorizontalHeaderLabels(["Group ID", "Group Name", "Section ID", "Section Name"])
        self.read_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.read_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.read_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.read_table)

        btn_back = QPushButton("← Back to Operations")
        btn_back.setStyleSheet("background-color: #34495e; color: white; padding: 10px;")
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_back)

        return screen

    def create_update_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Update A Group")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Table to select group
        self.update_table = QTableWidget()
        self.update_table.setColumnCount(4)
        self.update_table.setHorizontalHeaderLabels(["Group ID", "Group Name", "Section ID", "Section Name"])
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.cellClicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        # Update Form
        form = QFormLayout()
        self.update_group_id_label = QLabel("Select a Group above")
        self.update_section_combo = QComboBox()
        self.load_sections_combo(self.update_section_combo)
        self.update_group_name_input = QLineEdit()
        
        form.addRow("Group ID:", self.update_group_id_label)
        form.addRow("New Section:", self.update_section_combo)
        form.addRow("New Group Name:", self.update_group_name_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Group")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_update.clicked.connect(self.update_group)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete A Group")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(4)
        self.delete_table.setHorizontalHeaderLabels(["Group ID", "Group Name", "Section ID", "Section Name"])
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")
    
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_delete.clicked.connect(self.delete_group)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    
    def load_sections_combo(self, combo_box):
        """Load all sections into a combobox"""
        combo_box.clear()
        sections = group_crud_queries.GroupCRUD.get_all_sections()
        for section_id, name in sections:
            combo_box.addItem(f"{name} (ID: {section_id})", section_id)

    
    def save_new_group(self):
        """Create a new group"""
        name = self.create_name_input.text().strip()
        section_id = self.create_section_id_input.currentData()
    
        if not name:
            QMessageBox.warning(self, "Validation Error", "Group name is required!")
            return
        
        if not section_id:
            QMessageBox.warning(self, "Validation Error", "Please select a section!")
            return
    
        group_id = group_crud_queries.GroupCRUD.create_group(name, section_id)
        if group_id:
            QMessageBox.information(self, "Success", f"Group '{name}' created successfully!")
            self.create_name_input.clear()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to create group!")

    def perform_search(self):
        """Execute search with current parameters"""
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()
    
        # Map search field to database column
        field_map = {
            "Group ID": "group_id",
            "Group Name": "group_name",
            "Section ID": "section_id"
        }
        db_field = field_map.get(search_field)
    
        # Get sort parameters
        sort_index = self.sort_combo.currentIndex()
        sort_map = {
            0: ('group_id', 'ASC'),
            1: ('group_id', 'DESC'),
            2: ('group_name', 'ASC'),
            3: ('group_name', 'DESC'),
            4: ('section_id', 'ASC'),
            5: ('section_id', 'DESC')
        }
        sort_by, sort_order = sort_map[sort_index]
    
        # Query database
        results = group_crud_queries.GroupCRUD.get_all_groups(
            search_field=db_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order
        )
    
        # Display in table
        self.read_table.setRowCount(len(results))
        for row_idx, (group_id, group_name, section_id, section_name) in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(group_id)))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(group_name))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(str(section_id)))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(section_name))

    def load_for_update(self, row):
        """Load selected group into update form"""
        group_id = self.update_table.item(row, 0).text()
        group_name = self.update_table.item(row, 1).text()
        section_id = int(self.update_table.item(row, 2).text())
    
        self.current_group_id = group_id
        self.update_group_id_label.setText(group_id)
        self.update_group_name_input.setText(group_name)
        
        # Set combobox to current section
        for i in range(self.update_section_combo.count()):
            if self.update_section_combo.itemData(i) == section_id:
                self.update_section_combo.setCurrentIndex(i)
                break

    def update_group(self):
        """Update the selected group"""
        if not hasattr(self, 'current_group_id'):
            QMessageBox.warning(self, "No Selection", "Please select a group first!")
            return

        new_name = self.update_group_name_input.text().strip()
        new_section_id = self.update_section_combo.currentData()

        if not new_name:
            QMessageBox.warning(self, "Validation Error", "Group name is required!")
            return
    # Fixed: correct parameter order (group_id, name, section_id)
        success = group_crud_queries.GroupCRUD.update_group(
            self.current_group_id, new_name, new_section_id
        )

        if success:
            QMessageBox.information(self, "Success", "Group updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update group!")


    def delete_group(self):
        """Delete selected group"""
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a group to delete!")
            return
    
        row = selected[0].row()
        group_id = self.delete_table.item(row, 0).text()
        group_name = self.delete_table.item(row, 1).text()
    
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{group_name}'?\n"
            f"This may affect students assigned to this group.\n"
            f"This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if reply == QMessageBox.Yes:
            success = group_crud_queries.GroupCRUD.delete_group(group_id)
            if success:
                QMessageBox.information(self, "Success", "Group deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete group!")

    # ==================== Screen Navigation ====================

    def show_read_screen(self):
        """Show read screen with all groups"""
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        """Show update screen with groups table"""
        results = group_crud_queries.GroupCRUD.get_all_groups()
        self.update_table.setRowCount(len(results))
        for row_idx, (group_id, group_name, section_id, section_name) in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(group_id)))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(group_name))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(section_id)))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(section_name))
    
        self.update_group_id_label.setText("Select a group above")
        self.update_group_name_input.clear()
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        """Show delete screen with groups table"""
        results = group_crud_queries.GroupCRUD.get_all_groups()
        self.delete_table.setRowCount(len(results))
        for row_idx, (group_id, group_name, section_id, section_name) in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(group_id)))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(group_name))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(str(section_id)))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(section_name))
    
        self.stack.setCurrentIndex(4)
