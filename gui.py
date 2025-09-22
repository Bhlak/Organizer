from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QWidget, QPushButton, QListWidget, QLabel, QFileDialog
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Monitor")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Watched Folders")
        layout.addWidget(self.label)

        self.folder_list = QListWidget()
        self.folder_list.addItems(["Inbox/Reports", "Inbox/Alerts"])
        layout.addWidget(self.folder_list)

        self.add_button = QPushButton("Add Folder")
        layout.addWidget(self.start_button)

        self.trigger_button = QPushButton("Save Lineup")
        layout.addWidget(self.trigger_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_button.clicked.connect(self.add_folder)
    
    def add_folder(self):
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder:
                 self.folder_list.addItem(folder)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
