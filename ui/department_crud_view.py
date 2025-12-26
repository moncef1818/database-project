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
        """


        self.update_screen = self.create_update_screen()
        self.stack.addWidget(self.update_screen)

        self.delete_screen = self.create_delete_screen()
        self.stack.addWidget(self.delete_screen)
        """
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
        btn_read.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_update.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_delete.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        
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
        pass
    def create_delete_screen(self):
        pass
    def save_new_department(self):
        pass

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

          

