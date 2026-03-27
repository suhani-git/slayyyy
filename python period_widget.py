import sys, json, os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QCalendarWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush

DATA_FILE = "my_period_data.json"
ICONS = ["🎀", "💖", "🌸", "✨", "💅"]

class PeriodCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Period Widget")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(360, 440)
        self.setStyleSheet("background-color: #2e2a4d; border-radius: 15px; color: #ffffff;")

        self.period_dates = self.load_data()

        self.label = QLabel("My Glow-Up Calendar 🎀")
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setStyleSheet("color: #ffb6c1;")
        self.label.setAlignment(Qt.AlignCenter)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {background-color: #3a355b; color: #fff; font-size: 14px;}
            QCalendarWidget QAbstractItemView:enabled {color: #fff;}
            QCalendarWidget QToolButton {color: #ffb6c1;}
        """)
        self.calendar.clicked.connect(self.mark_period)

        self.icon_picker = QComboBox()
        self.icon_picker.addItems(ICONS)
        self.icon_picker.setStyleSheet("background-color: #3a355b; color: #ffb6c1; border: 1px solid #ffb6c1;")

        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_data)
        self.save_btn.setStyleSheet("background-color: #ffb6c1; color: #2e2a4d; font-weight: bold;")

        self.close_btn = QPushButton("❌")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setFixedWidth(30)
        self.close_btn.setStyleSheet("background-color: transparent; color: #fff;")

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.label)
        top_bar.addWidget(self.close_btn)

        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.calendar)
        layout.addWidget(QLabel("Add Icon to Date:"))
        layout.addWidget(self.icon_picker)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self.calendar.viewport())
        for date_str, icon in self.period_dates.items():
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            rect = self.calendar.geometry()
            cell_rect = self.calendar.visualRect(qdate)
            if not cell_rect.isNull():
                painter.drawText(cell_rect, Qt.AlignBottom | Qt.AlignHCenter, icon)

    def mark_period(self, date):
        date_str = date.toString("yyyy-MM-dd")
        emoji = self.icon_picker.currentText()
        self.period_dates[date_str] = emoji
        self.calendar.update()

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.period_dates, f)
        QMessageBox.information(self, "Saved", "Your glow-up calendar has been saved, queen 💾👑")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = PeriodCalendar()
    widget.show()
    sys.exit(app.exec_())
