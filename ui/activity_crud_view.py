# New file: ui/activity_crud_view.py
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
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from db import activity_crud_queries


class ActivityView(QWidget):
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

        title = QLabel("Activity Operations")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info_label = QLabel(
            "Manage course activities (Lectures, Tutorials, Practicals)"
        )
        info_label.setStyleSheet("font-size: 12px; color: #7f8c8d; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        grid = QGridLayout()

        btn_create = QPushButton("Create New\nActivity")
        btn_read = QPushButton("View All\nActivities")
        btn_update = QPushButton("Update\nActivity")
        btn_delete = QPushButton("Delete\nActivity")
        btn_back = QPushButton("← Back to Core Data")

        for btn in [btn_create, btn_read, btn_update, btn_delete]:
            btn.setFixedSize(180, 120)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-size: 14px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
            )

        btn_back.setStyleSheet(
            "background-color: #34495e; color: white; padding: 10px;"
        )

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

        title = QLabel("Create New Activity")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        info = QLabel(
            "Note: Each course can have only ONE activity of each type.\n"
            "Lecture is created automatically when you create a course."
        )
        info.setStyleSheet("color: #e67e22; font-size: 11px; padding: 5px;")
        info.setWordWrap(True)
        layout.addWidget(info)

        form = QFormLayout()

        # 1. Initialize widgets first
        self.create_course_combo = QComboBox()
        self.create_type_combo = QComboBox()
        self.create_type_combo.addItems(["Tutorial", "Practical"])
        self.create_status_label = QLabel("")
        self.create_status_label.setStyleSheet("color: #27ae60; font-size: 11px;")

        # 2. Connect signals
        self.create_course_combo.currentIndexChanged.connect(
            self.update_available_types_create
        )

        # 3. Load data (which triggers signals)
        self.load_courses_combo(self.create_course_combo)

        form.addRow("Course:*", self.create_course_combo)
        form.addRow("Activity Type:*", self.create_type_combo)
        form.addRow("Status:", self.create_status_label)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Activity")
        btn_cancel = QPushButton("Cancel")

        btn_save.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_save.clicked.connect(self.save_new_activity)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        layout.addStretch()

        # Initial update
        self.update_available_types_create()

        return screen

    def create_read_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("View All Activities")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        search_label = QLabel("Search by:")
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(
            ["Activity ID", "Course ID", "Course Name", "Activity Type"]
        )
        self.search_field_combo.setFixedWidth(120)

        search_input_label = QLabel("Enter:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type here...")

        sort_label = QLabel("Sort by:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(
            [
                "Activity ID (Asc)",
                "Activity ID (Desc)",
                "Course ID (Asc)",
                "Course ID (Desc)",
                "Course Name (A-Z)",
                "Course Name (Z-A)",
                "Type (A-Z)",
                "Type (Z-A)",
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
        self.read_table.setColumnCount(6)
        self.read_table.setHorizontalHeaderLabels(
            [
                "Activity ID",
                "Course ID",
                "Dept ID",
                "Course Name",
                "Department",
                "Activity Type",
            ]
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

        title = QLabel("Update Activity")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        warning = QLabel(
            "⚠️ Warning: Changing activity type will move attendance records!"
        )
        warning.setStyleSheet("color: #e74c3c; font-size: 11px; padding: 5px;")
        layout.addWidget(warning)

        self.update_table = QTableWidget()
        self.update_table.setColumnCount(6)
        self.update_table.setHorizontalHeaderLabels(
            [
                "Activity ID",
                "Course ID",
                "Dept ID",
                "Course Name",
                "Department",
                "Activity Type",
            ]
        )
        self.update_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.update_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.update_table.clicked.connect(self.load_for_update)
        layout.addWidget(self.update_table)

        form = QFormLayout()

        self.update_id_label = QLabel("Select an activity above")

        self.update_course_combo = QComboBox()
        self.update_course_combo.currentIndexChanged.connect(
            self.update_available_types_update
        )
        self.load_courses_combo(self.update_course_combo)

        self.update_type_combo = QComboBox()
        self.update_type_combo.addItems(["Lecture", "Tutorial", "Practical"])

        self.update_status_label = QLabel("")
        self.update_status_label.setStyleSheet("color: #27ae60; font-size: 11px;")

        form.addRow("Activity ID:", self.update_id_label)
        form.addRow("Course:*", self.update_course_combo)
        form.addRow("Activity Type:*", self.update_type_combo)
        form.addRow("Status:", self.update_status_label)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_update = QPushButton("Update Activity")
        btn_cancel = QPushButton("Cancel")

        btn_update.setStyleSheet(
            "background-color: #27ae60; color: white; padding: 10px;"
        )
        btn_cancel.setStyleSheet(
            "background-color: #95a5a6; color: white; padding: 10px;"
        )

        btn_update.clicked.connect(self.update_activity)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_update)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def create_delete_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        title = QLabel("Delete Activity")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        warning = QLabel(
            "⚠️ Note: Lecture activities cannot be deleted (mandatory for courses)"
        )
        warning.setStyleSheet("color: #e74c3c; font-size: 11px; padding: 5px;")
        layout.addWidget(warning)

        self.delete_table = QTableWidget()
        self.delete_table.setColumnCount(6)
        self.delete_table.setHorizontalHeaderLabels(
            [
                "Activity ID",
                "Course ID",
                "Dept ID",
                "Course Name",
                "Department",
                "Activity Type",
            ]
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

        btn_delete.clicked.connect(self.delete_activity)
        btn_cancel.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        btn_layout.addWidget(btn_delete)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        return screen

    def load_courses_combo(self, combo):
        """Load courses into combo box"""
        combo.clear()
        courses = activity_crud_queries.ActivityCRUD.get_all_courses()
        for course_id, dept_id, course_name, dept_name in courses:
            combo.addItem(
                f"{course_name} ({dept_name}) - ID: {course_id}", (course_id, dept_id)
            )

    def update_available_types_create(self):
        """Update available activity types based on selected course"""
        if not hasattr(self, "create_course_combo") or not hasattr(
            self, "create_type_combo"
        ):
            return

        if self.create_course_combo.count() == 0:
            return

        course_data = self.create_course_combo.currentData()
        if not course_data:
            return

        course_id, dept_id = course_data
        counts = activity_crud_queries.ActivityCRUD.get_activity_counts_for_course(
            course_id, dept_id
        )

        # Clear and rebuild type combo
        self.create_type_combo.clear()
        available = []

        if "Tutorial" not in counts:
            available.append("Tutorial")
        if "Practical" not in counts:
            available.append("Practical")

        if available:
            self.create_type_combo.addItems(available)
            self.create_status_label.setText(
                f"✓ {len(available)} activity type(s) available"
            )
            self.create_status_label.setStyleSheet("color: #27ae60; font-size: 11px;")
        else:
            self.create_status_label.setText(
                "⚠️ All activity types already exist for this course"
            )
            self.create_status_label.setStyleSheet("color: #e67e22; font-size: 11px;")

    def update_available_types_update(self):
        """Update status for update screen"""
        if not hasattr(self, "current_activity_id"):
            return

        course_data = self.update_course_combo.currentData()
        if not course_data:
            return

        course_id, dept_id = course_data
        counts = activity_crud_queries.ActivityCRUD.get_activity_counts_for_course(
            course_id, dept_id
        )

        status_parts = []
        if "Lecture" in counts:
            status_parts.append("Lecture ✓")
        if "Tutorial" in counts:
            status_parts.append("Tutorial ✓")
        if "Practical" in counts:
            status_parts.append("Practical ✓")

        self.update_status_label.setText(
            "Existing: " + ", ".join(status_parts) if status_parts else "No activities"
        )

    def save_new_activity(self):
        course_data = self.create_course_combo.currentData()
        if not course_data:
            QMessageBox.warning(self, "Validation Error", "Please select a course!")
            return

        course_id, dept_id = course_data
        activity_type = self.create_type_combo.currentText()

        if not activity_type:
            QMessageBox.warning(
                self,
                "Validation Error",
                "All activity types already exist for this course!",
            )
            return

        success = activity_crud_queries.ActivityCRUD.create_activity(
            course_id, dept_id, activity_type
        )
        if success:
            QMessageBox.information(
                self, "Success", f"{activity_type} activity created successfully!"
            )
            self.update_available_types_create()
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self, "Error", "Failed to create activity—this type may already exist."
            )

    def perform_search(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()

        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:
            sort_by, sort_order = "activity_id", "ASC"
        elif sort_index == 1:
            sort_by, sort_order = "activity_id", "DESC"
        elif sort_index == 2:
            sort_by, sort_order = "course_id", "ASC"
        elif sort_index == 3:
            sort_by, sort_order = "course_id", "DESC"
        elif sort_index == 4:
            sort_by, sort_order = "course_name", "ASC"
        elif sort_index == 5:
            sort_by, sort_order = "course_name", "DESC"
        elif sort_index == 6:
            sort_by, sort_order = "activity_type", "ASC"
        else:
            sort_by, sort_order = "activity_type", "DESC"

        results = activity_crud_queries.ActivityCRUD.get_all_activities(
            search_field=search_field if search_value else None,
            search_value=search_value if search_value else None,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.read_table.setRowCount(len(results))
        for row_idx, activity in enumerate(results):
            self.read_table.setItem(row_idx, 0, QTableWidgetItem(str(activity[0])))
            self.read_table.setItem(row_idx, 1, QTableWidgetItem(str(activity[1])))
            self.read_table.setItem(row_idx, 2, QTableWidgetItem(str(activity[2])))
            self.read_table.setItem(row_idx, 3, QTableWidgetItem(activity[3] or ""))
            self.read_table.setItem(row_idx, 4, QTableWidgetItem(activity[4] or ""))
            self.read_table.setItem(row_idx, 5, QTableWidgetItem(activity[5]))

    def load_for_update(self):
        selected = self.update_table.selectedIndexes()
        if not selected:
            return

        row = selected[0].row()
        activity_id = int(self.update_table.item(row, 0).text())
        course_id = int(self.update_table.item(row, 1).text())
        dept_id = int(self.update_table.item(row, 2).text())
        activity_type = self.update_table.item(row, 5).text()

        self.current_activity_id = activity_id
        self.update_id_label.setText(str(activity_id))

        # Set course combo
        for i in range(self.update_course_combo.count()):
            if self.update_course_combo.itemData(i) == (course_id, dept_id):
                self.update_course_combo.setCurrentIndex(i)
                break

        self.update_type_combo.setCurrentText(activity_type)
        self.update_available_types_update()

    def update_activity(self):
        if not hasattr(self, "current_activity_id"):
            QMessageBox.warning(
                self, "No Selection", "Please select an activity first!"
            )
            return

        course_data = self.update_course_combo.currentData()
        if not course_data:
            QMessageBox.warning(self, "Validation Error", "Please select a course!")
            return

        course_id, dept_id = course_data
        activity_type = self.update_type_combo.currentText()

        success = activity_crud_queries.ActivityCRUD.update_activity(
            self.current_activity_id, course_id, dept_id, activity_type
        )
        if success:
            QMessageBox.information(self, "Success", "Activity updated successfully!")
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Failed to update activity—may conflict with existing types.",
            )

    def delete_activity(self):
        selected = self.delete_table.selectedIndexes()
        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select an activity to delete!"
            )
            return

        row = selected[0].row()
        activity_id = int(self.delete_table.item(row, 0).text())
        course_name = self.delete_table.item(row, 3).text()
        activity_type = self.delete_table.item(row, 5).text()

        if activity_type == "Lecture":
            QMessageBox.warning(
                self,
                "Cannot Delete",
                "Lecture activities cannot be deleted as they are mandatory for courses!",
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the {activity_type} activity for '{course_name}'?\n\n"
            f"This will also delete all related attendance records and reservations!",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            success = activity_crud_queries.ActivityCRUD.delete_activity(activity_id)
            if success:
                QMessageBox.information(
                    self, "Success", "Activity deleted successfully!"
                )
                self.stack.setCurrentIndex(0)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete activity!")

    def show_read_screen(self):
        self.perform_search()
        self.stack.setCurrentIndex(2)

    def show_update_screen(self):
        results = activity_crud_queries.ActivityCRUD.get_all_activities()
        self.update_table.setRowCount(len(results))
        for row_idx, activity in enumerate(results):
            self.update_table.setItem(row_idx, 0, QTableWidgetItem(str(activity[0])))
            self.update_table.setItem(row_idx, 1, QTableWidgetItem(str(activity[1])))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(activity[2])))
            self.update_table.setItem(row_idx, 3, QTableWidgetItem(activity[3] or ""))
            self.update_table.setItem(row_idx, 4, QTableWidgetItem(activity[4] or ""))
            self.update_table.setItem(row_idx, 5, QTableWidgetItem(activity[5]))

        self.update_id_label.setText("Select an activity above")
        self.stack.setCurrentIndex(3)

    def show_delete_screen(self):
        results = activity_crud_queries.ActivityCRUD.get_all_activities()
        self.delete_table.setRowCount(len(results))
        for row_idx, activity in enumerate(results):
            self.delete_table.setItem(row_idx, 0, QTableWidgetItem(str(activity[0])))
            self.delete_table.setItem(row_idx, 1, QTableWidgetItem(str(activity[1])))
            self.update_table.setItem(row_idx, 2, QTableWidgetItem(str(activity[2])))
            self.delete_table.setItem(row_idx, 3, QTableWidgetItem(activity[3] or ""))
            self.delete_table.setItem(row_idx, 4, QTableWidgetItem(activity[4] or ""))
            self.delete_table.setItem(row_idx, 5, QTableWidgetItem(activity[5]))

        self.stack.setCurrentIndex(4)
