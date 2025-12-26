from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QStackedWidget, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QFormLayout,
                             QMessageBox, QHeaderView, QComboBox)
from PyQt5.QtCore import Qt
from db import department_crud_queries

class DepartmentView(QWidget):
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

        title = QLabel("Department Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        
        btn_create = QPushButton("Create New\nDepartment")
        btn_read = QPushButton("View All\nDepartments")
        btn_update = QPushButton("Update\nDepartment")
        btn_delete = QPushButton("Delete\nDepartment")
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

        title = QLabel("Create New Department")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        self.create_name_input = QLineEdit()
        self.create_name_input.setPlaceholderText("e.g., Computer Science")
        form.addRow("Department Name:", self.create_name_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Department")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_save.clicked.connect(self.save_new_department)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))  

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen      

    def create_read_screen(self):
        
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Departments")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()  
        self.search_field_combo.addItems(["ID", "Name"])
        self.search_field_combo.setFixedWidth(100)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")
        

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["ID (Ascending)", "ID (Descending)", 
                                  "Name (A-Z)", "Name (Z-A)"])
        
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

        self.read_table = QTableWidget()
        self.read_table.setColumnCount(2)
        self.read_table.setHorizontalHeaderLabels(["ID", "Department Name"])
        self.read_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
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

        title = QLabel("Update A Department")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(2)
        self.update_table.setHorizontalHeaderLabels(["ID", "Department Name"])
        self.update_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.cellClicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()
        self.update_id_label = QLabel("Select a department above")
        self.update_name_input = QLineEdit()
        form.addRow("Department ID:", self.update_id_label)
        form.addRow("New Name:", self.update_name_input)
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Department")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_update.clicked.connect(self.update_department)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete A Department")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(2)
        self.delete_table.setHorizontalHeaderLabels(["ID", "Department Name"])
        self.delete_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")
    
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_delete.clicked.connect(self.delete_department)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen
    
    def save_new_department(self):
        name = self.create_name_input.text().strip()
    
        if not name:
            QMessageBox.warning(self, "Validation Error", "Department name is required!")
            return
    
        
        print(f"Creating department: {name}")
        id = department_crud_queries.DepartmentCRUD.create_department(name)
        if id:
            QMessageBox.information(self, "Success", f"Department '{name}' created successfully!")
            self.create_name_input.clear()
            self.stack.setCurrentIndex(0)

    def perform_search(self):
        """Execute search with current parameters"""
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()
    
        # Get sort parameters
        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = 'department_id', 'ASC'
        elif sort_index == 1:
            sort_by, sort_order = 'department_id', 'DESC'
        elif sort_index == 2:
            sort_by, sort_order = 'name', 'ASC'
        else:
            sort_by, sort_order = 'name', 'DESC'
    
        # Query database
        results = department_crud_queries.DepartmentCRUD.get_all_departments(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order
        )
    
        # Display in table
        self.read_table.setRowCount(len(results))
        for row_idx, (dept_id, name) in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(dept_id)))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(name))

    def load_for_update(self, row):
        """Load selected department into update form"""
        dept_id = self.update_table.item(row, 0).text()
        name = self.update_table.item(row, 1).text()
    
        self.current_dept_id = dept_id
        self.update_id_label.setText(dept_id)
        self.update_name_input.setText(name)


    def update_department(self):
        """Update the selected department"""
        if not hasattr(self, 'current_dept_id'):
            QMessageBox.warning(self, "No Selection", "Please select a department first!")
            return
    
        new_name = self.update_name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Validation Error", "Department name is required!")
            return
    
        success = department_crud_queries.DepartmentCRUD.update_department(
            self.current_dept_id, new_name
        )
    
        if success:
            QMessageBox.information(self, "Success", "Department updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update department!")

    def delete_department(self):
        """Delete selected department"""
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a department to delete!")
            return
    
        row = selected[0].row()
        dept_id = self.delete_table.item(row, 0).text()
        name = self.delete_table.item(row, 1).text()
    
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{name}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
    
        if reply == QMessageBox.Yes:
            success = department_crud_queries.DepartmentCRUD.delete_department(dept_id)
            if success:
                QMessageBox.information(self, "Success", "Department deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete department!")


    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = department_crud_queries.DepartmentCRUD.get_all_departments()
        self.update_table.setRowCount(len(results))
        for row_idx, (dept_id, name) in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(dept_id)))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(name))
    
        self.update_id_label.setText("Select a department above")
        self.update_name_input.clear()
        self.stack.setCurrentIndex(3)
    def show_delete_screen(self):
        results = department_crud_queries.DepartmentCRUD.get_all_departments()
        self.delete_table.setRowCount(len(results))
        for row_idx, (dept_id, name) in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(dept_id)))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(name))
    
        self.stack.setCurrentIndex(4)