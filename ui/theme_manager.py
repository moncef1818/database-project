"""
Theme Manager for Database Management System
Provides utilities for applying and managing the modern blue/black theme
"""

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from pathlib import Path


class ThemeManager:
    """Centralized theme management for the application"""

    # Color Constants
    COLORS = {
        'bg_dark': '#0a0e27',
        'bg_medium': '#1a1f3a',
        'bg_light': '#1e2444',
        'primary': '#1976d2',
        'primary_hover': '#2196f3',
        'primary_dark': '#0d47a1',
        'accent': '#64b5f6',
        'success': '#00897b',
        'danger': '#d32f2f',
        'warning': '#f57c00',
        'border': '#37474f',
        'text': '#e8eaf6',
        'text_secondary': '#90a4ae',
    }

    @staticmethod
    def load_theme(app: QApplication, theme_file='modern_theme.qss'):
        """
        Load and apply theme stylesheet to application

        Args:
            app: QApplication instance
            theme_file: Path to .qss stylesheet file

        Returns:
            bool: True if successfully loaded, False otherwise
        """
        theme_path = Path(theme_file)

        # Try multiple possible locations
        possible_paths = [
            theme_path,
            Path(__file__).parent / theme_file,
            Path(__file__).parent.parent / theme_file,
        ]

        for path in possible_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        stylesheet = f.read()
                        app.setStyleSheet(stylesheet)
                    print(f"✅ Theme loaded successfully: {path}")
                    return True
                except Exception as e:
                    print(f"❌ Error loading theme: {e}")
                    return False

        print(f"❌ Theme file not found: {theme_file}")
        print(f"   Searched in: {[str(p) for p in possible_paths]}")
        return False

    @staticmethod
    def create_card_container():
        """
        Create a styled card container widget

        Returns:
            QWidget: Styled container widget
        """
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {ThemeManager.COLORS['bg_medium']};
                border: 2px solid {ThemeManager.COLORS['border']};
                border-radius: 12px;
                padding: 20px;
            }}
        """)
        return card

    @staticmethod
    def get_title_style(size=24):
        """
        Get title label stylesheet

        Args:
            size: Font size in pixels

        Returns:
            str: Stylesheet string
        """
        return f"font-size: {size}px; font-weight: bold; color: {ThemeManager.COLORS['accent']};"

    @staticmethod
    def get_subtitle_style(size=13):
        """
        Get subtitle label stylesheet

        Args:
            size: Font size in pixels

        Returns:
            str: Stylesheet string
        """
        return f"font-size: {size}px; color: {ThemeManager.COLORS['text_secondary']}; font-style: italic;"

    @staticmethod
    def get_section_header_style():
        """Get section header stylesheet"""
        return f"""
            font-size: 16px;
            font-weight: bold;
            color: {ThemeManager.COLORS['accent']};
            padding: 10px 0px;
            border-bottom: 2px solid {ThemeManager.COLORS['primary']};
        """

    @staticmethod
    def get_info_label_style():
        """Get info/warning label stylesheet"""
        return f"""
            color: {ThemeManager.COLORS['warning']};
            background-color: rgba(245, 124, 0, 0.1);
            border-left: 4px solid {ThemeManager.COLORS['warning']};
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
        """

    @staticmethod
    def get_success_label_style():
        """Get success message label stylesheet"""
        return f"""
            color: {ThemeManager.COLORS['success']};
            background-color: rgba(0, 137, 123, 0.1);
            border-left: 4px solid {ThemeManager.COLORS['success']};
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
        """

    @staticmethod
    def get_error_label_style():
        """Get error message label stylesheet"""
        return f"""
            color: {ThemeManager.COLORS['danger']};
            background-color: rgba(211, 47, 47, 0.1);
            border-left: 4px solid {ThemeManager.COLORS['danger']};
            padding: 10px;
            border-radius: 4px;
            font-size: 12px;
        """

    @staticmethod
    def apply_window_properties(window):
        """
        Apply theme-specific window properties

        Args:
            window: QMainWindow or QWidget instance
        """
        window.setStyleSheet(f"background-color: {ThemeManager.COLORS['bg_dark']};")

    @staticmethod
    def get_separator_style():
        """Get horizontal separator line stylesheet"""
        return f"""
            background-color: {ThemeManager.COLORS['border']};
            max-height: 2px;
            min-height: 2px;
        """


# Example usage in main.py
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Apply the theme
    ThemeManager.load_theme(app, 'modern_theme.qss')

    # Create and show your main window
    # window = YourMainWindow()
    # window.show()

    # sys.exit(app.exec_())
