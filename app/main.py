import os
import sys
from pathlib import Path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from db import connection

# Import your views
from ui import crud_view
from ui.academic_records_view import AcademicRecordsView
from ui.audit_log_view import AuditLogView
from ui.report_analytics_view import Report_analytics
from ui.reservation_view import ReservationView
from ui.results_processing_view import ResultsProcessingView

BASE_DIR = Path(__file__).parent.resolve()
LOGO_PATH = os.path.join(BASE_DIR, "image_9038d0.png")


class SideButton(QPushButton):
    """Sleek minimalist sidebar button"""

    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(50)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = connection.get_connection()
        self.setWindowTitle("NSCS Command Center")
        self.resize(1300, 850)

        # 1. APPLY GLOBAL STYLES (Cyberpunk aesthetic)
        self.apply_cyber_style()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR (The Aesthetic Part) ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(280)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)

        # Creative Logo Integration
        self.logo_container = QFrame()
        logo_layout = QVBoxLayout(self.logo_container)

        self.logo_label = QLabel()
        pixmap = QPixmap(LOGO_PATH)
        self.logo_label.setPixmap(
            pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Neon Glow Effect for Logo
        logo_glow = QGraphicsDropShadowEffect()
        logo_glow.setBlurRadius(40)
        logo_glow.setColor(QColor(0, 255, 255, 120))  # Cyan glow
        logo_glow.setOffset(0, 0)
        self.logo_label.setGraphicsEffect(logo_glow)

        logo_layout.addWidget(self.logo_label)
        sidebar_layout.addWidget(self.logo_container)

        # Minimalist Brand Text
        brand_label = QLabel("NSCS MANAGEMENT")
        brand_label.setObjectName("brandLabel")
        brand_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(brand_label)

        sidebar_layout.addSpacing(40)

        # Navigation
        self.btn_group = []
        nav_items = [
            ("DATA CORE MANAGMENT ", self.show_crud_menu),
            ("SCUDUALING STAFF ", self.show_staff_scheduling),
            ("ACADEMIC RECORDS ", self.show_academic_records),
            ("RESULTS PROCESSING ", self.show_results_processing),
            ("ANALYTICS", self.show_reports_analytics),
            ("AUDIT LOGS", self.show_audit_records),
        ]

        for text, callback in nav_items:
            btn = SideButton(text)
            btn.clicked.connect(callback)
            btn.clicked.connect(self.handle_nav_selection)
            sidebar_layout.addWidget(btn)
            self.btn_group.append(btn)

        sidebar_layout.addStretch()

        # --- MAIN CONTENT AREA ---
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentArea")

        # Initial View (Put your nice background image here or a placeholder)
        self.home_view = QLabel("UNIVERSITY  DATABASE \n MANAGMENT SYSTEM")
        self.home_view.setAlignment(Qt.AlignCenter)
        self.home_view.setObjectName("homeView")
        self.content_stack.addWidget(self.home_view)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

    def apply_cyber_style(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #020408;
            }
            #sidebar {
                background-color: #05070a;
                border-right: 1px solid #1a1f26;
            }
            #brandLabel {
                color: #00ffff;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 4px;
                margin-top: 10px;
            }
            SideButton {
                background-color: transparent;
                color: #5d6d7e;
                border: none;
                border-radius: 4px;
                text-align: left;
                padding-left: 15px;
                font-size: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            SideButton:hover {
                color: #00ffff;
                background-color: rgba(0, 255, 255, 0.05);
            }
            SideButton:checked {
                color: #ffffff;
                background-color: rgba(0, 255, 255, 0.1);
                border-left: 3px solid #00ffff;
            }
            #contentArea {
                background-color: #070b14;
                margin: 10px;
                border-radius: 20px;
                border: 1px solid #1a1f26;
            }
            #homeView {
                color: #1a1f26;
                font-size: 40px;
                font-weight: bold;
                letter-spacing: 10px;
            }
        """
        )

    def handle_nav_selection(self):
        sender = self.sender()
        for btn in self.btn_group:
            btn.setChecked(False)
        sender.setChecked(True)

    def show_crud_menu(self):
        inst = crud_view.CrudView()
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)

    def show_staff_scheduling(self):
        inst = ReservationView(self)
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)

    def show_reports_analytics(self):
        inst = Report_analytics()
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)

    def show_academic_records(self):
        inst = AcademicRecordsView(self)
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)

    def show_audit_records(self):
        inst = AuditLogView(self)
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)

    def show_results_processing(self):
        inst = ResultsProcessingView(self)
        self.content_stack.addWidget(inst)
        self.content_stack.setCurrentWidget(inst)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # This keeps your OTHER styles intact
    try:
        with open("modern_theme.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(app.styleSheet() + f.read())
    except:
        pass

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
