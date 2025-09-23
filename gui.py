from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QWidget, QPushButton, QListWidget, QLabel, QFileDialog,
    QTabWidget, QTimeEdit, QStatusBar, QMessageBox, QAbstractItemView, 
    QRadioButton, QStackedWidget, QSpinBox, QComboBox, QHBoxLayout,
    QFormLayout
)
from PySide6.QtCore import Qt, QEvent, QTime
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Monitor")
        self.setGeometry(200, 200, 500, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Home
        home_tab = QWidget()
        home_layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to The Folder Organizer!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 5px; border: 2px dotted; border-radius: 30%")
        home_layout.addWidget(welcome_label)

        self.current_schedule_label = QLabel("No schedule set")
        home_layout.addWidget(self.current_schedule_label)
        home_tab.setLayout(home_layout)
        self.tabs.addTab(home_tab, "Home")

        # Schedule
        schedule_tab = QWidget()
        schedule_layout = QVBoxLayout()
        schedule_tab.setLayout(schedule_layout)

        self.daily_radio = QRadioButton("Daily")
        self.weekly_radio = QRadioButton("Weekly")
        self.monthly_radio = QRadioButton("Monthly")

        schedule_layout.addWidget(self.daily_radio)
        schedule_layout.addWidget(self.weekly_radio)
        schedule_layout.addWidget(self.monthly_radio)

        self.schedule_forms = QStackedWidget()
        schedule_layout.addWidget(self.schedule_forms)

        daily_form = QWidget()
        daily_form_layout = QFormLayout(daily_form)
        self.daily_spin = QSpinBox()
        self.daily_spin.setMinimum(1)
        self.daily_spin.setFixedWidth(60)
        self.daily_time = QTimeEdit()
        self.daily_time.setDisplayFormat("HH:mm")
        self.daily_time.setTime(QTime.currentTime())
        self.daily_time.setFixedWidth(90)
        daily_controls = QHBoxLayout()
        daily_controls.addWidget(QLabel("Run every"))
        daily_controls.addWidget(self.daily_spin)
        daily_controls.addWidget(QLabel("Day(s) At"))
        daily_controls.addWidget(self.daily_time)
        daily_controls.addStretch()
        daily_form_layout.addRow(daily_controls)
        self.schedule_forms.addWidget(daily_form)

        weekly_form = QWidget()
        weekly_form_layout = QFormLayout(weekly_form)
        self.weekly_spin = QSpinBox()
        self.weekly_spin.setMinimum(1)
        self.weekly_spin.setFixedWidth(60)
        self.weekly_time = QTimeEdit()
        self.weekly_time.setDisplayFormat("HH:mm")
        self.weekly_time.setFixedWidth(90)
        self.weekly_time.setTime(QTime.currentTime())
        self.weekday_combo = QComboBox()
        self.weekday_combo.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        weekly_controls = QHBoxLayout()
        weekly_controls.addWidget(QLabel("Run every"))
        weekly_controls.addWidget(self.weekly_spin)
        weekly_controls.addWidget(QLabel("Week(s) On"))
        weekly_controls.addWidget(self.weekday_combo)
        weekly_controls.addWidget(QLabel("At"))
        weekly_controls.addWidget(self.weekly_time)
        weekly_controls.addStretch()
        weekly_form_layout.addRow(weekly_controls)
        self.schedule_forms.addWidget(weekly_form)

        monthly_form = QWidget()
        monthly_form_layout = QFormLayout(monthly_form)
        self.monthly_spin = QSpinBox()
        self.monthly_spin.setRange(1, 31)
        self.monthly_spin.setFixedWidth(60)
        self.monthly_time = QTimeEdit()
        self.monthly_time.setDisplayFormat("HH:mm")
        self.monthly_time.setTime(QTime.currentTime())
        self.monthly_time.setFixedWidth(90)
        monthly_controls = QHBoxLayout()
        monthly_controls.addWidget(QLabel("Run on day"))          
        monthly_controls.addWidget(self.monthly_spin)
        monthly_controls.addWidget(QLabel("At"))
        monthly_controls.addWidget(self.monthly_time)
        monthly_controls.addStretch()
        monthly_form_layout.addRow(monthly_controls)
        self.schedule_forms.addWidget(monthly_form)

        self.daily_radio.toggled.connect(lambda checked: self.schedule_forms.setCurrentIndex(0) if checked else None)
        self.weekly_radio.toggled.connect(lambda checked: self.schedule_forms.setCurrentIndex(1) if checked else None)
        self.monthly_radio.toggled.connect(lambda checked: self.schedule_forms.setCurrentIndex(2) if checked else None)
        
        self.daily_radio.setChecked(True)

        self.schedule_button = QPushButton("Set Schedule")
        schedule_layout.addWidget(self.schedule_button)
        self.schedule_button.clicked.connect(self.save_schedule)

        self.tabs.addTab(schedule_tab, "Schedule")


        # Folders
        folders_tab = QWidget()
        folders_layout = QVBoxLayout()        

        self.folders_label = QLabel("Watched Folders")
        folders_layout.addWidget(self.folders_label)

        self.folder_list = QListWidget()
        self.folder_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.folder_list.installEventFilter(self)
        folders_layout.addWidget(self.folder_list)

        self.add_button = QPushButton("Add Folder")
        folders_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Folder")
        folders_layout.addWidget(self.delete_button)

        self.save_button = QPushButton("Save Folders")
        folders_layout.addWidget(self.save_button)

        folders_tab.setLayout(folders_layout)
        self.tabs.addTab(folders_tab, "Folders")

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.add_button.clicked.connect(self.add_folder)
        self.delete_button.clicked.connect(self.remove_folders)
        self.save_button.clicked.connect(self.save_folders)

        self.load_folders()
        self.render_schedule()
    
    def eventFilter(self, source, event):
        if source is self.folder_list and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.remove_folders()
                return True
        return super().eventFilter(source, event)

    def add_folder(self):
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder and not any(self.folder_list.item(i).text() == folder for i in range(self.folder_list.count())):
                 self.folder_list.addItem(folder)

    def remove_folders(self):
        folders = self.folder_list.selectedItems()
        count = len(folders)
        if count == 1:
            current_item = folders[0]
            if current_item:
                temp = current_item.text()
                reply = QMessageBox.question(
                    self,
                    "Confirm Delete",
                    f"Are you sure you would like to remove: \n{current_item.text()}?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.folder_list.takeItem(self.folder_list.row(current_item))
                    self.save_folders()
                    self.status.showMessage(f"{temp} Removed!")

        elif (count > 1):
            if folders:
                reply = QMessageBox.question(
                    self,
                    "Confirm Delete",
                    f"Are you sure you would like to remove {len(folders)} folders?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    for i in folders:
                        self.folder_list.takeItem(self.folder_list.row(i))
                        self.save_folders()
                    self.status.showMessage(f"{len(folders)} Folders Removed from Watchlist!")

        else:
            self.status.showMessage("No Folder Selected")
    
    def save_folders(self):
        folders = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
        with open("folders.txt", "w") as f:
            f.write("\n".join(folders))
        self.status.showMessage("Folders Saved!", 3000)

    def load_folders(self):
        import os
        if os.path.exists("folders.txt"):             
            with open("folders.txt", "r") as f:
                folders = f.read().splitlines()
                self.folder_list.addItems(folders)
    
    def save_schedule(self):
        import json
        
        schedule_data = {}

        if self.daily_radio.isChecked():
            schedule_data["type"] = "daily"
            schedule_data["every"] = self.daily_spin.value()
            schedule_data["time"] = self.daily_time.time().toString("HH:mm")
        elif self.weekly_radio.isChecked():
            schedule_data["type"] = "weekly"
            schedule_data["every"] = self.weekly_spin.value()
            schedule_data["weekday"] = self.weekday_combo.currentText()
            schedule_data["time"] = self.weekly_time.time().toString("HH:mm")
        elif self.monthly_radio.isChecked():
            schedule_data["type"] = "monthly"
            schedule_data["day"] = self.monthly_spin.value()
            schedule_data["time"] = self.monthly_time.time().toString("HH:mm")
        
        with open("schedule.json", "w") as f:
            json.dump(schedule_data, f, indent=4)
        
        self.status.showMessage("Schedule Saved!", 3000)
        self.render_schedule()

    def load_schedule(self):
        import os
        import json

        if os.path.exists("schedule.json"):
            with open("schedule.json", "r") as f:
                schedule_data = json.load(f)
                return schedule_data
    
    def render_schedule(self):
        schedule_data = self.load_schedule()
        schedule_type = schedule_data.get("type")

        if schedule_type=="daily":
            text = f"Schedule: Daily at {schedule_data.get('time','-')}"
        elif schedule_type=="weekly":
            text = (f"Schedule: Weekly, every {schedule_data.get('every','1')} week(s) "
                        f"on {schedule_data.get('weekday','-')} at {schedule_data.get('time','-')}")
        elif schedule_type=="monthly":
             text = (f"Schedule: Monthly on day {schedule_data.get('day','-')} "
                        f"at {schedule_data.get('time','-')}")
        else:
            text = "No valid schedule set"
        
        self.current_schedule_label.setText(text)

            
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
