#main app

import sys

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel)
    
    
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PROJECT")
        self.resize(1000, 800)
        self.setWindowIcon(QIcon("Screenshot 2025-08-14 135744.png"))
        
        self.image = QLabel(self)
        
        pixmap = QPixmap("Screenshot 2025-08-14 135744.png")
        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())
        
        self.setCentralWidget(self.image)
    
