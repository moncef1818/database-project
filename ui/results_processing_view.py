
#  Main menu for Results Processing operations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class ResultsProcessingView(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        # Main layout setup
        self.main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("Results Processing & Analysis")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)

        # Stacked widget for menu and submenu views
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Menu page (index 0)
        self.menu_page = self.create_menu_page()
        self.stack.addWidget(self.menu_page)

        # Initialize with menu
        self.stack.setCurrentIndex(0)

    def create_menu_page(self):

        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)

        # Subtitle
        subtitle = QLabel("Select a category to view reports")
        subtitle.setStyleSheet("font-size: 12px; color: #7f8c8d; font-style: italic;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Button grid
        grid = QGridLayout()

        # Category buttons
        categories = [
            (" Student Status\nReports", 0, 0, "#3498db"),
            (" Course\nAnalysis", 0, 1, "#e67e22"),
            (" Grade\nStatistics", 1, 0, "#9b59b6"),
            (" Admin\nActions", 1, 1, "#27ae60"),
        ]

        for name, row, col, color in categories:
            btn = QPushButton(name)
            btn.setFixedSize(200, 120)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 10px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(color, 0.3)};
                }}
            """
            )
            btn.clicked.connect(lambda checked, n=name: self.open_category(n))
            grid.addWidget(btn, row, col)

        # Center the grid
        grid.setAlignment(Qt.AlignCenter)
        layout.addLayout(grid)
        layout.addStretch()

        # Back button
        btn_back = QPushButton("← Back to Main Menu")
        btn_back.setStyleSheet(
            """
            background-color: #34495e;
            color: white;
            padding: 10px;
            font-size: 12px;
            border-radius: 5px;
        """
        )
        btn_back.clicked.connect(self.go_back_to_main)
        layout.addWidget(btn_back)

        return menu_widget

    def darken_color(self, hex_color, factor=0.2):
        """
        Darkens a hex color by a given factor.
        Args:
            hex_color: Hex color string (e.g., '#3498db')
            factor: Darken factor (0.0 to 1.0)
        Returns:
            str: Darkened hex color
        """
        # Remove '#' and convert to RGB
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

        # Darken
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))

        return f"#{r:02x}{g:02x}{b:02x}"

    def open_category(self, category_name):

        if "Student Status" in category_name:
            self.show_student_status_reports()
        elif "Course" in category_name:
            self.show_course_analysis()
        elif "Statistics" in category_name:
            self.show_grade_statistics()
        elif "Admin" in category_name:
            self.show_admin_actions()

    def show_student_status_reports(self):

        from ui.student_status_reports_view import StudentStatusReportsView

        status_view = StudentStatusReportsView(parent=self)
        self.stack.addWidget(status_view)
        self.stack.setCurrentWidget(status_view)

    def show_course_analysis(self):

        from ui.course_analysis_view import CourseAnalysisView

        analysis_view = CourseAnalysisView(parent=self)
        self.stack.addWidget(analysis_view)
        self.stack.setCurrentWidget(analysis_view)

    def show_grade_statistics(self):

        from ui.grade_statistics_view import GradeStatisticsView

        stats_view = GradeStatisticsView(parent=self)
        self.stack.addWidget(stats_view)
        self.stack.setCurrentWidget(stats_view)

    def show_admin_actions(self):

        from ui.admin_actions_view import AdminActionsView

        admin_view = AdminActionsView(parent=self)
        self.stack.addWidget(admin_view)
        self.stack.setCurrentWidget(admin_view)

    def go_back_to_main(self):

        main_window = self.window()
        if hasattr(main_window, "content_stack"):
            main_window.content_stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(0)

    def show_menu(self):

        # Remove all submenu views from stack (keep only menu)
        while self.stack.count() > 1:
            widget = self.stack.widget(1)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        # Show menu
        self.stack.setCurrentIndex(0)
