import os
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QGroupBox, QApplication, QSizePolicy, QFrame)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class HealthTrackerUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("HealthTrackerUI")
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        # --- Main Layout ---
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # --- Header Section ---
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Realtime rPPG Tracker")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.title_label)
        self.main_layout.addLayout(header_layout)

        # --- Content Layout (Split View) ---
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(20)
        self.main_layout.addLayout(self.content_layout)

        # --- Left Pane: Video Feed & Controls ---
        self.left_card = QFrame()
        self.left_card.setObjectName("Card")
        left_layout = QVBoxLayout(self.left_card)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)

        # Video Feed
        self.video_label = QLabel("Waiting for Camera...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_label.setObjectName("VideoPlaceholder")
        left_layout.addWidget(self.video_label, stretch=1)

        # Controls
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        self.start_button = QPushButton("START MONITORING")
        self.end_button = QPushButton("STOP")
        
        # Set icons or just text styling
        self.start_button.setCursor(Qt.PointingHandCursor)
        self.end_button.setCursor(Qt.PointingHandCursor)

        button_layout.addWidget(self.start_button, 2)
        button_layout.addWidget(self.end_button, 1)
        left_layout.addLayout(button_layout)

        self.content_layout.addWidget(self.left_card, stretch=3)

        # --- Right Pane: Analytics ---
        self.right_card = QFrame()
        self.right_card.setObjectName("Card")
        right_layout = QVBoxLayout(self.right_card)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(15)

        # Heart Rate Display
        hr_container = QFrame()
        hr_container.setObjectName("StatBox")
        hr_layout = QHBoxLayout(hr_container)
        
        # Icon
        self.hr_icon_label = QLabel()
        current_dir_hr = os.path.dirname(os.path.abspath(__file__))
        icon_path_heart = os.path.join(current_dir_hr, "..", "icon", "heart-icon.png")
        if os.path.exists(icon_path_heart):
            self.hr_icon_label.setPixmap(QPixmap(icon_path_heart).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # Value
        self.hr_value_label = QLabel("--")
        self.hr_value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Unit
        hr_unit_label = QLabel("BPM")
        hr_unit_label.setObjectName("UnitLabel")

        hr_layout.addWidget(self.hr_icon_label)
        hr_layout.addStretch()
        hr_layout.addWidget(self.hr_value_label)
        hr_layout.addWidget(hr_unit_label)
        
        right_layout.addWidget(hr_container)

        # Graph
        self.hr_fig, self.ax_rppg = plt.subplots()
        self.hr_canvas = FigureCanvas(self.hr_fig)
        self.hr_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.hr_canvas, stretch=1)

        self.content_layout.addWidget(self.right_card, stretch=2)

    def _apply_styles(self):
        # Color Palette
        bg_color = "#121212"
        card_bg = "#1E1E1E"
        primary_color = "#00ADB5" # Teal
        danger_color = "#FF2E63" # Red/Pink
        text_color = "#EEEEEE"
        secondary_text = "#AAAAAA"

        self.setStyleSheet(f"""
            QWidget#HealthTrackerUI {{
                background-color: {bg_color};
            }}

            QWidget {{
                color: {text_color};
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }}
            
            QFrame#Card {{
                background-color: {card_bg};
                border-radius: 12px;
                border: 1px solid #333;
            }}

            QLabel {{
                color: {text_color};
            }}

            QLabel#TitleLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {primary_color};
            }}

            QLabel#VideoPlaceholder {{
                background-color: #000;
                border-radius: 8px;
                border: 1px dashed #444;
                color: #666;
            }}

            QPushButton {{
                background-color: {card_bg};
                border: 2px solid {primary_color};
                border-radius: 8px;
                color: {primary_color};
                padding: 10px 20px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {primary_color};
                color: #fff;
            }}

            QPushButton:pressed {{
                background-color: #008C94;
                border-color: #008C94;
            }}

            QPushButton#StartButton {{
                background-color: {primary_color};
                color: #fff;
                border: none;
            }}
            QPushButton#StartButton:hover {{
                background-color: #00FFF5;
                color: #000;
            }}

            QPushButton#EndButton {{
                border-color: {danger_color};
                color: {danger_color};
            }}
            QPushButton#EndButton:hover {{
                background-color: {danger_color};
                color: #fff;
            }}

            QFrame#StatBox {{
                background-color: #252526;
                border-radius: 8px;
                padding: 10px;
            }}

            QLabel#ValueLabel {{
                font-size: 36px;
                font-weight: bold;
                color: {text_color};
            }}

            QLabel#UnitLabel {{
                font-size: 14px;
                color: {secondary_text};
                margin-bottom: 5px;
            }}
        """)

        # Specific Object Names for Styling
        self.title_label.setObjectName("TitleLabel")
        self.start_button.setObjectName("StartButton")
        self.end_button.setObjectName("EndButton")
        self.hr_value_label.setObjectName("ValueLabel")

        # Matplotlib Styling
        self.hr_fig.patch.set_facecolor(card_bg)
        self.ax_rppg.set_facecolor(card_bg)
        
        # Remove spines
        for spine in self.ax_rppg.spines.values():
            spine.set_visible(False)
        
        # Grid and Ticks
        self.ax_rppg.grid(True, color='#333', linestyle='--', linewidth=0.5)
        self.ax_rppg.tick_params(axis='x', colors=secondary_text, labelsize=8)
        self.ax_rppg.tick_params(axis='y', colors=secondary_text, labelsize=8)
        
        # Tight layout
        self.hr_fig.tight_layout()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = HealthTrackerUI()
    ui.setGeometry(100, 100, 1280, 720)
    ui.show()
    sys.exit(app.exec_())