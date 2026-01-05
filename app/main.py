import os
import sys
from pathlib import Path

from db import connection
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from ui import crud_view
from ui.academic_records_view import (
    AcademicRecordsView,
)
from ui.report_analytics_view import (
    Report_analytics,
)
from ui.results_processing_view import ResultsProcessingView

BASE_DIR = Path(__file__).parent.resolve()
IMG_PATH = os.path.join(BASE_DIR, "image.png")


class MainWindow(QMainWindow):
    def __init__(self):
        self.connection = connection.get_connection()
        super().__init__()
        self.setWindowTitle("Student App")
        self.resize(1100, 700)

        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 1. Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #1e86fc;")
        sidebar_layout = QVBoxLayout(self.sidebar)

        self.btn_crud = QPushButton("Core Data Management")
        self.btn_staff_scheduling = QPushButton("Staff & Scheduling")
        self.btn_accadimic = QPushButton("Academic Records")
        self.btn_resaults_processing = QPushButton("Results Processing")
        self.btn_reports = QPushButton("Reports & Analytics")
        self.btn_audit = QPushButton("System Audit")

        for btn in [
            self.btn_crud,
            self.btn_staff_scheduling,
            self.btn_accadimic,
            self.btn_resaults_processing,
            self.btn_reports,
            self.btn_audit,
        ]:
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        # 2. Content Area (Stacked Widget)
        self.content_stack = QStackedWidget()
        label2 = QLabel(self)
        pixmap = QPixmap(IMG_PATH)
        label2.setPixmap(pixmap)
        label2.setScaledContents(True)
        self.content_stack.addWidget(label2)

        # 3. Add layouts to main
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

        # Connect signals
        self.btn_crud.clicked.connect(self.show_crud_menu)
        self.btn_reports.clicked.connect(self.show_reports_analytics)
        self.btn_accadimic.clicked.connect(self.show_academic_records)
        self.btn_resaults_processing.clicked.connect(self.show_results_processing)

    def init_UI(self):
        pass

    def show_crud_menu(self):
        crud_view_instance = crud_view.CrudView()
        self.content_stack.addWidget(crud_view_instance)
        self.content_stack.setCurrentWidget(crud_view_instance)

    def show_reports_analytics(self):
        reports_view_instance = Report_analytics()
        self.content_stack.addWidget(reports_view_instance)
        self.content_stack.setCurrentWidget(reports_view_instance)

    def show_academic_records(self):
        academic_view_instance = AcademicRecordsView(self)
        self.content_stack.addWidget(academic_view_instance)
        self.content_stack.setCurrentWidget(academic_view_instance)

    def show_results_processing(self):

        results_view = ResultsProcessingView(parent=self)
        self.content_stack.addWidget(results_view)
        self.content_stack.setCurrentWidget(results_view)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
