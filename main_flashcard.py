# main_flashcard.py
import sys
from PyQt6.QtWidgets import QApplication
from main_app_flashcard import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec())
