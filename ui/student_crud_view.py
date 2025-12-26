from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QStackedWidget, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QFormLayout,
                             QMessageBox, QHeaderView, QComboBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
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

        title = QLabel("Student Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        
        btn_create = QPushButton("Create New\nStudent")
        btn_read = QPushButton("View All\nStudents")
        btn_update = QPushButton("Update\nStudent")
        btn_delete = QPushButton("Delete\nStudent")
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

        title = QLabel("Create New Student")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Form with all student fields
        form = QFormLayout()
        
        self.create_last_name_input = QLineEdit()
        self.create_last_name_input.setPlaceholderText("e.g., Benali")
        
        self.create_first_name_input = QLineEdit()
        self.create_first_name_input.setPlaceholderText("e.g., Ahmed")
        
        self.create_dob_input = QDateEdit()
        self.create_dob_input.setCalendarPopup(True)
        self.create_dob_input.setDate(QDate(2000, 1, 1))
        self.create_dob_input.setDisplayFormat("yyyy-MM-dd")
        
        self.create_address_input = QLineEdit()
        self.create_address_input.setPlaceholderText("Optional: e.g., 123 Rue de la Liberté")
        
        self.create_city_input = QLineEdit()
        self.create_city_input.setPlaceholderText("Optional: e.g., Blida")
        
        self.create_zip_input = QLineEdit()
        self.create_zip_input.setPlaceholderText("Optional: e.g., 09000")
        
        self.create_phone_input = QLineEdit()
        self.create_phone_input.setPlaceholderText("Optional: e.g., 0555123456")
        
        self.create_fax_input = QLineEdit()
        self.create_fax_input.setPlaceholderText("Optional")
        
        self.create_email_input = QLineEdit()
        self.create_email_input.setPlaceholderText("Optional: e.g., ahmed.benali@example.com")
        
        form.addRow("Last Name:*", self.create_last_name_input)
        form.addRow("First Name:*", self.create_first_name_input)
        form.addRow("Date of Birth:*", self.create_dob_input)
        form.addRow("Address:", self.create_address_input)
        form.addRow("City:", self.create_city_input)
        form.addRow("Zip Code:", self.create_zip_input)
        form.addRow("Phone:", self.create_phone_input)
        form.addRow("Fax:", self.create_fax_input)
        form.addRow("Email:", self.create_email_input)
        
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Student")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet("background-color: #27ae60; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_save.clicked.connect(self.save_new_student)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))  

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()
        return screen      

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Students")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()  
        self.search_field_combo.addItems(["ID", "Last Name", "First Name", "Email"])
        self.search_field_combo.setFixedWidth(120)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "ID (Ascending)", 
            "ID (Descending)", 
            "Last Name (A-Z)", 
            "Last Name (Z-A)",
            "First Name (A-Z)",
            "First Name (Z-A)"
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
        self.read_table = QTableWidget()
        self.read_table.setColumnCount(10)  # Change from 6 to 10
        self.read_table.setHorizontalHeaderLabels([
            "ID", "Last Name", "First Name", "DOB", "Address", 
            "City", "Zip Code", "Phone", "Fax", "Email"
        ])
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

        title = QLabel("Update A Student")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Selection table
        self.update_table = QTableWidget()
        self.update_table.setColumnCount(10)
        self.update_table.setHorizontalHeaderLabels([
            "ID", "Last Name", "First Name", "DOB", "Address", 
            "City", "Zip Code", "Phone", "Fax", "Email"
        ])
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.cellClicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        # Update form
        form = QFormLayout()
        
        self.update_id_label = QLabel("Select a student above")
        self.update_last_name_input = QLineEdit()
        self.update_first_name_input = QLineEdit()
        self.update_dob_input = QDateEdit()
        self.update_dob_input.setCalendarPopup(True)
        self.update_dob_input.setDisplayFormat("yyyy-MM-dd")
        self.update_address_input = QLineEdit()
        self.update_city_input = QLineEdit()
        self.update_zip_input = QLineEdit()
        self.update_phone_input = QLineEdit()
        self.update_fax_input = QLineEdit()
        self.update_email_input = QLineEdit()
        
        form.addRow("Student ID:", self.update_id_label)
        form.addRow("Last Name:", self.update_last_name_input)
        form.addRow("First Name:", self.update_first_name_input)
        form.addRow("Date of Birth:", self.update_dob_input)
        form.addRow("Address:", self.update_address_input)
        form.addRow("City:", self.update_city_input)
        form.addRow("Zip Code:", self.update_zip_input)
        form.addRow("Phone:", self.update_phone_input)
        form.addRow("Fax:", self.update_fax_input)
        form.addRow("Email:", self.update_email_input)
        
        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Student")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_update.clicked.connect(self.update_student)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete A Student")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
        layout.addWidget(title)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(10)
        self.delete_table.setHorizontalHeaderLabels([
            "ID", "Last Name", "First Name", "DOB", "Address", 
            "City", "Zip Code", "Phone", "Fax", "Email"
        ])
        self.delete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.delete_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.delete_table)

        btn_layout = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        btn_cancel = QPushButton("Cancel")
    
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        btn_cancel.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")

        btn_delete.clicked.connect(self.delete_student)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen
    
    # ===== CRUD Operations =====
    
    def save_new_student(self):
        """Validate and save new student"""
        last_name = self.create_last_name_input.text().strip()
        first_name = self.create_first_name_input.text().strip()
        dob = self.create_dob_input.date().toString("yyyy-MM-dd")
        
        if not last_name or not first_name:
            QMessageBox.warning(self, "Validation Error", "Last name and first name are required!")
            return
        
        # Get optional fields (set to None if empty)
        address = self.create_address_input.text().strip() or None
        city = self.create_city_input.text().strip() or None
        zip_code = self.create_zip_input.text().strip() or None
        phone = self.create_phone_input.text().strip() or None
        fax = self.create_fax_input.text().strip() or None
        email = self.create_email_input.text().strip() or None
        
        print(f"Creating student: {first_name} {last_name}")
        student_id = student_crud_queries.StudentCRUD.create_student(
            last_name, first_name, dob, address, city, zip_code, 
            phone, fax, email
        )
        
        if student_id:
            QMessageBox.information(self, "Success", 
                                  f"Student '{first_name} {last_name}' created successfully!")
            self.clear_create_form()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to create student!")

    def perform_search(self):
        """Execute search with current parameters"""
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()
        
        # Map UI field names to database column names
        field_map = {
            "ID": "student_id",
            "Last Name": "last_name",
            "First Name": "first_name",
            "Email": "email"
        }
        
        # Get sort parameters
        sort_index = self.sort_combo.currentIndex()
        sort_options = [
            ('student_id', 'ASC'),
            ('student_id', 'DESC'),
            ('last_name', 'ASC'),
            ('last_name', 'DESC'),
            ('first_name', 'ASC'),
            ('first_name', 'DESC')
        ]
        sort_by, sort_order = sort_options[sort_index]
        
        # Query database
        results = student_crud_queries.StudentCRUD.get_all_students(
            search_field=field_map.get(search_field) if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Display in table (columns: ID, last_name, first_name, dob, address, city, zip_code, phone, fax, email)
        self.read_table.setRowCount(len(results))
        for row_idx, student in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(student[0])))   # ID
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(student[1] or ""))  # Last name
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(student[2] or ""))  # First name
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(str(student[3]) if student[3] else ""))  # DOB
            self.read_table.setItem(row_idx, 4, QTableWidgetItem(student[4] or ""))  # Address
            self.read_table.setItem(row_idx, 5, QTableWidgetItem(student[5] or ""))  # City
            self.read_table.setItem(row_idx, 6, QTableWidgetItem(student[6] or ""))  # Zip code
            self.read_table.setItem(row_idx, 7, QTableWidgetItem(student[7] or ""))  # Phone
            self.read_table.setItem(row_idx, 8, QTableWidgetItem(student[8] or ""))  # Fax
            self.read_table.setItem(row_idx, 9, QTableWidgetItem(student[9] or ""))  # Email


    def load_for_update(self, row):
        """Load selected student into update form"""
        student_id = self.update_table.item(row, 0).text()
        
        # Fetch full student details
        student = student_crud_queries.StudentCRUD.get_student_by_id(student_id)
        
        if student:
            self.current_student_id = student_id
            self.update_id_label.setText(student_id)
            self.update_last_name_input.setText(student[1] or "")
            self.update_first_name_input.setText(student[2] or "")
            
            if student[3]:  # DOB
                dob = QDate.fromString(str(student[3]), "yyyy-MM-dd")
                self.update_dob_input.setDate(dob)
            
            self.update_address_input.setText(student[4] or "")
            self.update_city_input.setText(student[5] or "")
            self.update_zip_input.setText(student[6] or "")
            self.update_phone_input.setText(student[7] or "")
            self.update_fax_input.setText(student[8] or "")
            self.update_email_input.setText(student[9] or "")

    def update_student(self):
        """Update the selected student"""
        if not hasattr(self, 'current_student_id'):
            QMessageBox.warning(self, "No Selection", "Please select a student first!")
            return
        
        last_name = self.update_last_name_input.text().strip()
        first_name = self.update_first_name_input.text().strip()
        
        if not last_name or not first_name:
            QMessageBox.warning(self, "Validation Error", "Last name and first name are required!")
            return
        
        dob = self.update_dob_input.date().toString("yyyy-MM-dd")
        address = self.update_address_input.text().strip() or None
        city = self.update_city_input.text().strip() or None
        zip_code = self.update_zip_input.text().strip() or None
        phone = self.update_phone_input.text().strip() or None
        fax = self.update_fax_input.text().strip() or None
        email = self.update_email_input.text().strip() or None
        
        success = student_crud_queries.StudentCRUD.update_student(
            self.current_student_id, last_name, first_name, dob, address, 
            city, zip_code, phone, fax, email
        )
        
        if success:
            QMessageBox.information(self, "Success", "Student updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Error", "Failed to update student!")

    def delete_student(self):
        """Delete selected student"""
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a student to delete!")
            return
        
        row = selected[0].row()
        student_id = self.delete_table.item(row, 0).text()
        last_name = self.delete_table.item(row, 1).text()
        first_name = self.delete_table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete student '{first_name} {last_name}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = student_crud_queries.StudentCRUD.delete_student(student_id)
            if success:
                QMessageBox.information(self, "Success", "Student deleted successfully!")
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete student!")

    # ===== Helper Methods =====

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = student_crud_queries.StudentCRUD.get_all_students()
        self.update_table.setRowCount(len(results))
        for row_idx, student in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(student[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(student[1] or ""))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(student[2] or ""))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(str(student[3]) or ""))
            self.update_table.setItem(row_idx, 4, QTableWidgetItem(student[4] or ""))
            self.update_table.setItem(row_idx, 5, QTableWidgetItem(student[5] or ""))
            self.update_table.setItem(row_idx, 6, QTableWidgetItem(student[6] or ""))
            self.update_table.setItem(row_idx, 7, QTableWidgetItem(student[7] or ""))
            self.update_table.setItem(row_idx, 8, QTableWidgetItem(student[8] or ""))
            self.update_table.setItem(row_idx, 9, QTableWidgetItem(student[9] or ""))
        
        self.update_id_label.setText("Select a student above")
        self.clear_update_form()
        self.stack.setCurrentIndex(3)
        
    def show_delete_screen(self):
        results = student_crud_queries.StudentCRUD.get_all_students()
        self.delete_table.setRowCount(len(results))
        for row_idx, student in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(student[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(student[1] or ""))
            self.delete_table.setItem(row_idx, 2, QTableWidgetItem(student[2] or ""))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(str(student[3]) or ""))
            self.delete_table.setItem(row_idx, 4, QTableWidgetItem(student[4] or ""))
            self.delete_table.setItem(row_idx, 5, QTableWidgetItem(student[5] or ""))
            self.delete_table.setItem(row_idx, 6, QTableWidgetItem(student[6] or ""))
            self.delete_table.setItem(row_idx, 7, QTableWidgetItem(student[7] or ""))
            self.delete_table.setItem(row_idx, 8, QTableWidgetItem(student[8] or ""))
            self.delete_table.setItem(row_idx, 9, QTableWidgetItem(student[9] or ""))
    
        self.stack.setCurrentIndex(4)

    def clear_create_form(self):
        """Clear all create form fields"""
        self.create_last_name_input.clear()
        self.create_first_name_input.clear()
        self.create_dob_input.setDate(QDate(2000, 1, 1))
        self.create_address_input.clear()
        self.create_city_input.clear()
        self.create_zip_input.clear()
        self.create_phone_input.clear()
        self.create_fax_input.clear()
        self.create_email_input.clear()

    def clear_update_form(self):
        """Clear all update form fields"""
        self.update_last_name_input.clear()
        self.update_first_name_input.clear()
        self.update_dob_input.setDate(QDate(2000, 1, 1))
        self.update_address_input.clear()
        self.update_city_input.clear()
        self.update_zip_input.clear()
        self.update_phone_input.clear()
        self.update_fax_input.clear()
        self.update_email_input.clear()
