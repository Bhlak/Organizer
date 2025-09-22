from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QWidget, QPushButton, QListWidget, QLabel, QFileDialog, QTabWidget
)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Monitor")
        self.setGeometry(200, 200, 500, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        home_tab = QWidget()
        home_layout = QVBoxLayout()
        home_layout.addWidget(QLabel("Welcome to The Folder Organizer!"))
        home_tab.setLayout(home_layout)
        self.tabs\.addTab(home_tab, "Home")


        folders_tab = QWidget()
        folders_layout = QVBoxLayout()        

        self.label = QLabel("Watched Folders")
        folders_layout.addWidget(self.label)

        self.folder_list = QListWidget()
        # self.folder_list.addItems(["Inbox/Reports", "Inbox/Alerts"])
        folders_layout.addWidget(self.folder_list)

        self.add_button = QPushButton("Add Folder")
        folders_layout.addWidget(self.add_button)

        self.save_button = QPushButton("Save Folders")
        folders_layout.addWidget(self.save_button)

        folders_tab.setLayout(folders_layout)
        self.tabs.addTab(folders_tab, "Watched Folders")

        # container = QWidget()
        # container.setLayout(layout)
        # self.setCentralWidget(container)

        self.add_button.clicked.connect(self.add_folder)
        self.save_button.clicked.connect(self.save_folders)

        self.load_folders()
    
    def add_folder(self):
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            print(folder)
            if folder:
                 self.folder_list.addItem(folder)
    
    def save_folders(self):
        folders = [self.folder_list.item(i).text() for i in range(self.folder_list.count())]
        with open("folders.txt", "w") as f:
            f.write("\n".join(folders))
        # print(f"Saved: {folders}")

    def load_folders(self):
        import os
        if os.path.exists("folders.txt"):             
            with open("folders.txt", "r") as f:
                folders = f.read().splitlines()
                self.folder_list.addItems(folders)
            # print(f"Loaded: {folders}")
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
