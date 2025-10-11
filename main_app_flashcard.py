# main_app_flashcard.py
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QStackedWidget,
    QLineEdit, QHBoxLayout, QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QPixmap
from data_model_flashcard import AppData
from ui_styles_flashcard import (
    APP_STYLE, SIDEBAR_BUTTON_STYLE, HAMBURGER_STYLE,
    FONT_LARGE_BOLD, FONT_MEDIUM, FONT_BUTTON, FONT_LABEL,
    FONT_SUBTITLE, APP_STYLE_DARK, APP_STYLE_LIGHT, CREATE_FLASH
)

class FadeWidget(QWidget):
    def __init__(self, widget, parent_window):
        super().__init__()
        self.widget = widget
        self.parent_window = parent_window
        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.effect = QGraphicsOpacityEffect()
        self.widget.setGraphicsEffect(self.effect)
        self.anim = None

    def fade_in(self):
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()

    def fade_out(self, next_widget):
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(500)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.finished.connect(lambda: self.switch_page(next_widget))
        self.anim.start()

    def switch_page(self, next_widget):
        next_widget.fade_in()
        self.parent_window.stacked.setCurrentWidget(next_widget)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data = AppData()
        
        self.setWindowTitle("Remora App Flow")
        self.setStyleSheet(APP_STYLE)
        self.setWindowIcon(QIcon("Icon.png"))
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.clicked.connect(self.toggle_btn)
        
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)
        
        self.stacked = QStackedWidget()
        
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        
        # Pages
        self.start_page = FadeWidget(self.create_start_page(), self)
        self.name_page = FadeWidget(self.create_name_page(), self)
        self.greet_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.greet_page.widget.setFont(FONT_MEDIUM)
        self.welcome_page = FadeWidget(self.create_welcome_page(), self)
        self.ask_page = FadeWidget(self.create_ask_page(), self)
        self.main_page = FadeWidget(self.create_main_page(), self)
        
        self.tutorial_page = FadeWidget(self.create_tutorial_page(), self)
        self.current_tutorial_step = 0  # track which tutorial slide we're on

        self.welcome_back_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.welcome_back_page.widget.setFont(FONT_MEDIUM)

        for page in [self.start_page, self.name_page, self.greet_page, self.welcome_page, self.ask_page, self.main_page]:
            self.stacked.addWidget(page)
            
        self.stacked.addWidget(self.tutorial_page)
        self.stacked.addWidget(self.welcome_back_page)

        # Connections
        self.start_btn.clicked.connect(lambda: self.start_page.fade_out(self.name_page))
        self.submit_name_btn.clicked.connect(self.show_greet)
        
        self.yes_btn.clicked.connect(self.show_tutorial)
        self.no_btn.clicked.connect(self.show_welcome_back)

        # Start page
        self.stacked.setCurrentWidget(self.start_page)
        self.start_page.fade_in()

        # Apply default theme
        self.apply_theme()
    
        
    def toggle_btn(self):
        self.data.theme = "dark" if self.data.theme == "light" else "light"
        self.apply_theme()
        
        if self.data.theme == "dark":
            self.theme_btn.setText("☀️")
        else:
            self.theme_btn.setText("🌙")
        
        
    def apply_theme(self):
        if self.data.theme == "dark":
            self.setStyleSheet(APP_STYLE_DARK)
        else:
            self.setStyleSheet(APP_STYLE_LIGHT)

    def create_start_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap("Icon.png")
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("READY WHEN YOU ARE!")
        subtitle.setFont(FONT_SUBTITLE)
        subtitle.setStyleSheet("color: #FC483D; letter-spacing: 2px; font-weight: 900;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.start_btn = QPushButton("BEGIN")
        self.start_btn.setFont(FONT_LARGE_BOLD)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget

    def create_name_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.name_label = QLabel("ENTER YOUR NAME")
        self.name_label.setFont(FONT_SUBTITLE)
        self.name_label.setStyleSheet("color: #434190")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type it here...")
        
        self.name_input.repaint()
        self.name_input.setFont(FONT_SUBTITLE)
        
        self.submit_name_btn = QPushButton("Next")
        self.submit_name_btn.setFont(FONT_BUTTON)
        self.name_input.returnPressed.connect(self.show_greet)
        
        layout.addStretch()
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)
        layout.addWidget(self.submit_name_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget

    def create_ask_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.ask_label = QLabel("New here?")
        self.ask_label.setFont(FONT_LABEL)
        self.ask_label.setStyleSheet("color: #434190")
        self.ask_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.yes_btn = QPushButton("Yes")
        self.no_btn = QPushButton("No")
        self.yes_btn.setFont(FONT_BUTTON)
        self.no_btn.setFont(FONT_BUTTON)
        layout.addStretch()
        layout.addWidget(self.ask_label)
        layout.addWidget(self.yes_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.no_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        return widget
    
    def create_tutorial_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
    
        self.tutorial_title = QLabel()
        self.tutorial_title.setFont(FONT_LARGE_BOLD)
        self.tutorial_title.setStyleSheet("color: #434190; font-weight: bold;")
        self.tutorial_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.tutorial_desc = QLabel()
        self.tutorial_desc.setFont(FONT_LABEL)
        self.tutorial_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tutorial_desc.setWordWrap(True)
        self.tutorial_desc.setStyleSheet("color: #555;")
    
        self.next_btn = QPushButton("Next ➜")
        self.next_btn.setFont(FONT_BUTTON)
        self.next_btn.clicked.connect(self.next_tutorial_step)
        
        self.skip_btn = QPushButton("Skip Tutorial ⏭️")
        self.skip_btn.setFont(FONT_BUTTON)
        self.skip_btn.clicked.connect(lambda: self.tutorial_page.fade_out(self.main_page))
        
        self.tutorial_desc.setStyleSheet("color: #555; padding: 0 40px;")
        
        layout.addStretch()
        layout.addWidget(self.tutorial_title)
        layout.addWidget(self.tutorial_desc)
        layout.addSpacing(20)
        layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.skip_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    
        return widget

    def show_tutorial(self):
        self.current_tutorial_step = 0
        self.ask_page.fade_out(self.tutorial_page)
        self.update_tutorial_step()
        
    def update_tutorial_step(self):
        """Update tutorial content based on current step"""
        steps = [
            {
                "title": "Adding Flashcards",
                "desc": "Click the '+' button or 'Add Flashcard' in the main screen to create a new flashcard.\nYou can enter a question, an answer, and save it instantly."
            },
            {
                "title": "Navigating the App",
                "desc": "Use the sidebar ☰ to explore:\n🏠 Home – View your flashcards\n👤 Profile – Check your info\n⚙️ Settings – Customize your theme\n📊 Statistics – See your study progress."
            },
            {
                "title": "Using Existing Flashcards",
                "desc": "Select any flashcard to study. Flip the card to see the answer and mark if you got it right or wrong. Remora tracks your progress automatically!"
            }
        ]
    
        # Update content
        step = steps[self.current_tutorial_step]
        self.tutorial_title.setText(step["title"])
        self.tutorial_desc.setText(step["desc"])
    
        # Update button text
        if self.current_tutorial_step < len(steps) - 1:
            self.next_btn.setText("Next ➜")
        else:
            self.next_btn.setText("Finish ✅")

    def next_tutorial_step(self):
        """Handle next step or finish tutorial"""
        self.current_tutorial_step += 1
        if self.current_tutorial_step < 3:
            self.update_tutorial_step()
        else:
            # End tutorial and go to main page
            self.tutorial_page.fade_out(self.main_page)

    def show_welcome_back(self):
        """Show personalized welcome back message before main content"""
        name = self.data.username or "User"
        self.welcome_back_page.widget.setText(f"Welcome back, {name}!")
        self.welcome_back_page.widget.setStyleSheet("color: #434190; font-weight: bold;")
        self.ask_page.fade_out(self.welcome_back_page)
        QTimer.singleShot(2000, lambda: self.welcome_back_page.fade_out(self.main_page))

    def create_main_page(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = QFrame()
        self.sidebar.setMaximumWidth(0)
        self.sidebar.setStyleSheet("background-color: #2d3436; color: white;")
        side_layout = QVBoxLayout(self.sidebar)
        side_layout.setContentsMargins(10, 20, 10, 10)
        
        for text in ["Home", "Profile", "Settings", "Statistics"]:
            btn = QPushButton(text)
            btn.setStyleSheet(SIDEBAR_BUTTON_STYLE)
            btn.clicked.connect(lambda _, t=text: self.show_page(t))
            side_layout.addWidget(btn)
            side_layout.addStretch()
            
            
        pixmap = QPixmap("Remora-Main.png")
        pixmap = pixmap.scaled(800, 800, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.existing_flashcard = QPushButton("Existing Flashcards")
        self.existing_flashcard.setFont(FONT_LARGE_BOLD)
        self.existing_flashcard.setStyleSheet(CREATE_FLASH)
        self.existing_flashcard.clicked.connect(self.toggle_existing_flashcard)
        
            
        self.create_flashcard = QPushButton("Create Flashcard")
        self.create_flashcard.setFont(FONT_LARGE_BOLD)
        self.create_flashcard.setStyleSheet(CREATE_FLASH)
        self.create_flashcard.clicked.connect(self.toggle_create_flashcard)

        self.hamburger = QPushButton("☰")
        self.hamburger.setStyleSheet(HAMBURGER_STYLE)
        self.hamburger.clicked.connect(self.toggle_sidebar)

        top = QHBoxLayout()
        top.addWidget(self.hamburger)
        top.addStretch()

        content_layout = QVBoxLayout()
        content_layout.addLayout(top)
        content_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.existing_flashcard, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.create_flashcard, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addStretch()

        layout.addWidget(self.sidebar)
        layout.addLayout(content_layout)
        
        return page
    
    def toggle_create_flashcard(self):
        print(" ")
        
    def toggle_existing_flashcard(self):
        print(" ")

    def show_greet(self):
        name = self.name_input.text().strip() or "User"
        self.data.username = name
        self.greet_page.widget.setText(f"Hi, {name}!")
        self.greet_page.widget.setStyleSheet("color: #434190")
        self.name_page.fade_out(self.greet_page)
        QTimer.singleShot(500, lambda: self.show_welcome())

    def create_welcome_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap("Icon.png")
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("WELCOME!")
        title.setFont(FONT_LARGE_BOLD)
        title.setStyleSheet("color: #FC483D; font-weight: 900; letter-spacing: 2px;")
        
        subtitle = QLabel("Remora is a flashcard for students")
        subtitle.setFont(FONT_LABEL)
        subtitle.setStyleSheet("color: #A0522D; font-weight: bold;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget
    
    def show_welcome(self):
        self.greet_page.fade_out(self.welcome_page)
        QTimer.singleShot(500, lambda: self.welcome_page.fade_out(self.ask_page))

    def toggle_sidebar(self):
        current_width = self.sidebar.maximumWidth()
        new_width = 180 if current_width == 0 else 0
        anim = QPropertyAnimation(self.sidebar, b"maximumWidth")
        anim.setDuration(400)
        anim.setStartValue(current_width)
        anim.setEndValue(new_width)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()
        self.sidebar.anim = anim

    def show_page(self, text):
        self.main_content.setText(f"You selected: {text}")
