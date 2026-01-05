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

from db import audit_log_queries

class AuditLogView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_audit_logs()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        header_label = QLabel("Audit Log Viewer")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(header_label)
        filter_layout = QHBoxLayout()
        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(
            ["ID", "Table Name", "Operation", "Timestamp", "User"]
        )
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search value...")  
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_clicked)
        filter_layout.addWidget(QLabel("Search by:"))
        filter_layout.addWidget(self.search_field_combo)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.search_button)
        self.sort_by_combo = QComboBox()
        self.sort_by_combo.addItems(
            ["audit_id", "table_name", "operation", "timestamp"]
        )
        self.sort_order_combo = QComboBox()
        self.sort_order_combo.addItems(["ASC", "DESC"])
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_by_combo)
        filter_layout.addWidget(self.sort_order_combo)

        main_layout.addLayout(filter_layout)
        self.audit_log_table = QTableWidget()
        self.audit_log_table.setColumnCount(5)
        self.audit_log_table.setHorizontalHeaderLabels(
            ["ID", "Table Name", "Operation", "Timestamp", "User"]
        )
        self.audit_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.audit_log_table)
    def load_audit_logs(self):
        search_field = self.search_field_combo.currentText()
        search_value = self.search_input.text().strip()
        sort_by = self.sort_by_combo.currentText()
        sort_order = self.sort_order_combo.currentText()

        logs = audit_log_queries.AuditLogQueries.get_audit_logs(
            search_field=search_field,
            search_value=search_value,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        self.audit_log_table.setRowCount(0)

        for row_data in logs:
            row_number = self.audit_log_table.rowCount()
            self.audit_log_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.audit_log_table.setItem(row_number, column_number, item)

    def on_search_clicked(self):
        self.load_audit_logs() 

