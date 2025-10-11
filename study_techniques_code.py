#this code still not implement in the GUI
# techniques/pomodoro_timer.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.study_duration = 30 * 60  # 30 minutes
        self.break_duration = 10 * 60  # 10 minutes
        self.time_left = self.study_duration
        self.is_study_time = True
        self.is_running = False

        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Pomodoro Timer")
        self.title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.timer_display = QLabel(self.format_time(self.time_left))
        self.timer_display.setFont(QFont("Arial", 48))
        self.timer_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Study Time")
        self.status_label.setFont(QFont("Arial", 20))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.reset_btn = QPushButton("Reset")

        self.start_btn.clicked.connect(self.toggle_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.reset_btn)

        layout.addWidget(self.title_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.timer_display)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02}:{secs:02}"

    def toggle_timer(self):
        if self.is_running:
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            self.timer.start(1000)
            self.start_btn.setText("Pause")
        self.is_running = not self.is_running

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_display.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText("Start")
            self.switch_mode()

    def switch_mode(self):
        if self.is_study_time:
            self.time_left = self.break_duration
            self.status_label.setText("Break Time (Flashcards Paused)")
        else:
            self.time_left = self.study_duration
            self.status_label.setText("Study Time")
        self.is_study_time = not self.is_study_time
        self.timer_display.setText(self.format_time(self.time_left))

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.start_btn.setText("Start")
        self.time_left = self.study_duration if self.is_study_time else self.break_duration
        self.timer_display.setText(self.format_time(self.time_left))

# techniques/interleaved_practice.py

import random
import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class InterleavedPractice(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interleaved Practice")
        self.deck = []
        self.current_index = 0
        self.showing_answer = False

        self.init_ui()
        self.load_flashcards()
        self.show_flashcard()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.flashcard_label = QLabel("")
        self.flashcard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flashcard_label.setFont(QFont("Arial", 28))
        self.flashcard_label.setWordWrap(True)

        self.next_btn = QPushButton("Next")
        self.next_btn.setFixedWidth(200)
        self.next_btn.setFont(QFont("Arial", 18))
        self.next_btn.clicked.connect(self.next_card)

        layout.addWidget(self.flashcard_label)
        layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def load_flashcards(self):
        folder = "flashcards_data"
        combined_deck = []

        # Load all .json files in the folder
        for file in os.listdir(folder):
            if file.endswith(".json"):
                path = os.path.join(folder, file)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    combined_deck.extend(data)

        random.shuffle(combined_deck)
        self.deck = combined_deck

    def show_flashcard(self):
        if self.current_index >= len(self.deck):
            self.flashcard_label.setText("🎉 Done with all flashcards!")
            self.next_btn.setEnabled(False)
            return

        flashcard = self.deck[self.current_index]
        if self.showing_answer:
            self.flashcard_label.setText(f"💡 {flashcard['answer']}")
            self.next_btn.setText("Next")
        else:
            self.flashcard_label.setText(f"❓ {flashcard['question']}")
            self.next_btn.setText("Show Answer")

    def next_card(self):
        if not self.showing_answer:
            self.showing_answer = True
        else:
            self.current_index += 1
            self.showing_answer = False
        self.show_flashcard()

# techniques/reverse_flashcards.py

class ReverseFlashcards:
    def __init__(self):
        self.reversed = False

    def toggle(self):
        self.reversed = not self.reversed

    def apply(self, card: dict):
        """Return a new card with question/answer flipped if reverse mode is on"""
        if self.reversed:
            return {"question": card["answer"], "answer": card["question"]}
        return card



