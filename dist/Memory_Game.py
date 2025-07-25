import sys, random, json, os
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QGridLayout, QMessageBox, QDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QStackedLayout, QLineEdit, QRadioButton, QCheckBox,
    QComboBox, QFrame
)
from PySide6.QtGui import QFont, QPixmap, QColor, QPalette
from PySide6.QtCore import Qt, QTimer, QUrl, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


CARD_BACK = "🔲"
ALL_EMOJIS = list(
    "🍎🍌🍇🍒🍉🍓🥝🥥🍑🍍🥑🌽🥕🍅🍆🥔🧄🧅🍞🥐🥨🧀🍗🍖🍔🍟🍕🌭🥪🍿🍩🍪🍰🎂🧁🍫🍬🍭🍮🍯🥤"
    "🧃🧋🫖☕🍵🍼🍽️🥣🥄🍴🥢🍶🧂🥫🥙🍱🍛🍚🍜🍲🥘🥗🥓🥩🍖🍗🦴🍠🌮🌯🥟🍢🍡🍧🍨🍦🥮🍥"
    "🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐸🐵🐔🦆🦉🦇🐺🐗🐴🦄🐝🐞🦋🐌🐚🪸🪼🐢🐍🦎🦖🦕"
    "🚗🚕🚙🚌🚎🏎🚓🚑🚒🚐🚛🚜🛺🚲🛴🚨🚍🚘🚖🚔🚡🚠🚟🚃🚋🚉🚅🚄🚈🚂✈️🛫🛬🚀🛸🛰️"
    "⚽🏀🏈⚾🎾🏐🏉🎱🏓🏸🥅🏒🏑🥍🏏⛳🪃🥊🥋🎯🎮🎲🧩♟️🃏🀄🪀🪁🧸🪅🎭🎨🎤🎧🎼🎹🥁🪘"
    "🎷🎺🪗🎸🪕🎻📯📻📺📷📸📹🎥📞☎️📟📠💻🖥🖨⌨️🖱🖲📱📲🔋🔌💡🔦🕯️🧯🛢⚙️🗜️🧰🔧🔨⛏🛠"
)
random.shuffle(ALL_EMOJIS)
SAVE_FILE = "savegame.json"
HIGHSCORE_FILE = "highscores.txt"


def glassy_palette():
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(250, 250, 255, 200))
    pal.setColor(QPalette.Base, QColor(255, 255, 255, 230))
    pal.setColor(QPalette.WindowText, QColor(41, 50, 70))
    return pal

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class BannerWidget(QFrame):
    def __init__(self, text, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 18px;
                padding: 22px 30px;
                box-shadow: 0px 8px 32px 0px rgba(31,38,135,0.2);
            }}
            QLabel {{
                color: white; font-size: 26pt; font-weight: bold;
                letter-spacing: 1px;
            }}
        """)
        self.setGraphicsEffect(None)
        hl = QHBoxLayout(self)
        hl.setAlignment(Qt.AlignCenter)
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        hl.addWidget(lbl)
        self.lbl = lbl
        self.setVisible(False)

    def show_banner(self, text=None):
        if text:
            self.lbl.setText(text)
        self.setVisible(True)
        self.raise_()
        self.anim = QPropertyAnimation(self, b"geometry")
        parent_rect = self.parent().rect()
        h = 100
        self.setGeometry(parent_rect.width() // 2 - 200, -h, 400, h)
        self.anim.setStartValue(QRect(parent_rect.width() // 2 - 200, -h, 400, h))
        self.anim.setEndValue(QRect(parent_rect.width() // 2 - 200, 25, 400, h))
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutBounce)
        self.anim.start()

    def hide_banner(self):
        self.setVisible(False)


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Game")
        self.setFixedSize(350, 470)
        self.stack = QStackedLayout()
        self.init_welcome_page()
        self.init_setup_page()
        container = QWidget()
        container.setLayout(self.stack)
        main_layout = QVBoxLayout()
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        self.setStyleSheet("""QDialog {background: #34394f;}
            QLabel {color: #fff; font-size: 13.5pt; margin: 6px 0;}
            QRadioButton, QCheckBox { font-size: 12.2pt; color: #fff;}
            QRadioButton::indicator, QCheckBox::indicator { width: 18px; height: 18px;}
            QLineEdit, QComboBox {
                background: #fff; color: #2d3762; font-size: 11pt;
                border: 1.5px solid #949ecc; border-radius: 6px; padding: 6px 10px;
            }
            QLineEdit:focus, QComboBox:focus { border-color: #2a6ad8;}
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #54a0ff, stop:1 #b0feea);
                color: #222; border-radius: 10px; font-weight: 700; font-size: 14pt; padding: 10px 15px;
            }
            QPushButton:hover {background-color: #2e70e3;}
        """)

    def init_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        image = QLabel()
        pixmap = QPixmap(resource_path("cards.jpg"))
        if not pixmap.isNull():
            image.setPixmap(pixmap.scaledToWidth(260, Qt.SmoothTransformation))
        else:
            image.setText("Image not found.")
        image.setAlignment(Qt.AlignCenter)
        layout.addWidget(image)
        play_button = QPushButton("🎮 Play")
        play_button.setFont(QFont("Arial", 13, QFont.Bold))
        play_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(play_button)
        layout.addStretch(1)
        page.setLayout(layout)
        self.stack.addWidget(page)

    def init_setup_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        players_box = QHBoxLayout()
        self.one_player_radio = QRadioButton("1 Player")
        self.two_player_radio = QRadioButton("2 Players")
        self.one_player_radio.setChecked(True)
        self.one_player_radio.setMinimumHeight(28)
        self.two_player_radio.setMinimumHeight(28)
        players_box.addWidget(self.one_player_radio)
        players_box.addWidget(self.two_player_radio)
        layout.addLayout(players_box)

        layout.addWidget(QLabel("Player 1 Name:"))
        self.p1_name = QLineEdit()
        self.p1_name.setFixedHeight(38)
        layout.addWidget(self.p1_name)

        layout.addWidget(QLabel("Player 2 Name:"))
        self.p2_name = QLineEdit()
        self.p2_name.setFixedHeight(38)
        self.p2_name.setEnabled(False)
        layout.addWidget(self.p2_name)

        layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setFixedHeight(38)
        layout.addWidget(self.difficulty_combo)

        self.sound_checkbox = QCheckBox("Enable Sound")
        self.sound_checkbox.setChecked(True)
        self.sound_checkbox.setMinimumHeight(28)
        layout.addWidget(self.sound_checkbox)

        self.start_button = QPushButton("🚀 Start Game")
        self.start_button.clicked.connect(self.accept)
        layout.addWidget(self.start_button)
        page.setLayout(layout)
        self.stack.addWidget(page)
        self.one_player_radio.toggled.connect(self.toggle_player_fields)
        self.two_player_radio.toggled.connect(self.toggle_player_fields)
        self.toggle_player_fields()

    def toggle_player_fields(self):
        self.p1_name.setEnabled(True)
        self.p2_name.setEnabled(self.two_player_radio.isChecked())

    def get_difficulty(self):
        return self.difficulty_combo.currentText().lower()

    def get_player1_name(self):
        return self.p1_name.text().strip() or "Player 1"

    def get_player2_name(self):
        return self.p2_name.text().strip() or "Player 2"

    def is_sound_enabled(self):
        return self.sound_checkbox.isChecked()

    def get_num_players(self):
        return 2 if self.two_player_radio.isChecked() else 1


class Memory_Game(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Memory Game")
        self.resize(780, 820)
        self.theme = "light"
        self.init_ui()
        # self.banner must be created before calling reset_game
        self.reset_game(first_time=True)

    def init_ui(self):
        self.setAutoFillBackground(True)
        pal = glassy_palette()
        self.setPalette(pal)
        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #e6ecfb, stop:1 #bed2f0);
            color: #142139; font-family: 'Segoe UI', Arial, sans-serif;
        }
        QPushButton {
            background: rgba(210,230,255,0.5);
            border-radius: 22px;
            font-size: 2.4vw;
            min-width: 0; /*disable expand*/
            min-height: 0;
            color: #384770;
            border: 1.3px solid #9bbad2; box-shadow: 0 3px 8px rgba(27,60,135,0.08);
            font-family:'Segoe UI Emoji';
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #e0ecff,stop:1 #cafafe);
        }
        QPushButton:disabled {
            background: #e1e8ee; color: #b5b9c1; border: 1.3px solid #c4c9cf;
        }
        QLabel {font-size: 1.25vw;}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 14, 20, 16)
        main_layout.setSpacing(8)
        self.setLayout(main_layout)

        # Top bar with timer, score, turn and menu button
        self.top_frame = QFrame()
        top_bar = QHBoxLayout(self.top_frame)
        top_bar.setContentsMargins(0, 4, 0, 4)
        top_bar.setSpacing(10)
        font_top = QFont("Segoe UI", 13, QFont.Medium)
        self.timer_label = QLabel("⏱ 60")
        self.timer_label.setFont(font_top)
        self.timer_label.setStyleSheet("color:#3583d8; font-weight:700;")
        self.score_label = QLabel("🎯 0")
        self.score_label.setFont(font_top)
        self.score_label.setStyleSheet("color:#490e7c; font-weight:700;")
        self.turn_label = QLabel("👤 -")
        self.turn_label.setFont(font_top)
        self.turn_label.setStyleSheet("color:#198754; font-weight:700;")
        # Add timer label first

        # Menu button to toggle controls menu
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.menu_btn.setFixedHeight(28)
        self.menu_btn.setToolTip("Show/Hide Game Menu")
        top_bar.addWidget(self.menu_btn)
        top_bar.addWidget(self.timer_label)

        top_bar.addStretch(1)
        top_bar.addWidget(self.score_label)
        top_bar.addStretch(1)
        top_bar.addWidget(self.turn_label)
        top_bar.setAlignment(Qt.AlignVCenter)
        self.top_frame.setMaximumHeight(40)
        self.top_frame.setStyleSheet(
            "QFrame{background: rgba(180,210,245,0.55); border-radius:14px;}"
        )
        main_layout.addWidget(self.top_frame)

        # Banner for win/loss messages
        self.banner = BannerWidget("", "#6dd5ed", self)
        self.banner.setVisible(False)
        self.banner.raise_()
        main_layout.addWidget(self.banner)
        main_layout.setAlignment(self.banner, Qt.AlignHCenter)
        self.banner.setMaximumHeight(90)

        # Create toggled menu with control buttons, initially hidden
        self.menu_widget = QFrame()
        self.menu_widget.setFrameShape(QFrame.StyledPanel)
        self.menu_widget.setStyleSheet("""
            QFrame {
                background: #cde4ff;
                border-radius: 10px;
                padding: 6px;
            }
        """)
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(10)
        menu_layout.setContentsMargins(10, 5, 10, 5)
        self.menu_widget.setLayout(menu_layout)
        main_layout.insertWidget(2, self.menu_widget)

        # Control buttons in menu: icon + label
        self.menu_buttons = []
        for icon, tooltip, label_text in [
            ("🔁", "Restart", "Restart"),
            ("💾", "Save", "Save"),
            ("📂", "Load", "Load"),
            ("🎨", "Theme", "Theme"),
            ("📊", "Scores", "Scores"),
            ("🔊", "Sound", "Sound"),
            ("⏸️", "Pause/Resume", "Pause")
        ]:
            btn = QPushButton(icon)
            btn.setFixedSize(40, 40)
            btn.setFont(QFont("Segoe UI", 18, QFont.Bold))
            btn.setToolTip(tooltip)
            vbox = QVBoxLayout()
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(2)
            vbox.setAlignment(Qt.AlignCenter)
            vbox.addWidget(btn, alignment=Qt.AlignCenter)
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 9pt; color: #384770;")
            vbox.addWidget(label)
            container = QFrame()
            container.setLayout(vbox)
            menu_layout.addWidget(container)
            self.menu_buttons.append(btn)

        (
            self.restart_btn,
            self.save_btn,
            self.load_btn,
            self.theme_btn,
            self.scoreboard_btn,
            self.sound_btn,
            self.pause_btn
        ) = self.menu_buttons

        self.menu_widget.setVisible(False)
        self.menu_btn.clicked.connect(lambda: self.menu_widget.setVisible(not self.menu_widget.isVisible()))

        # Connect buttons to functions
        self.restart_btn.clicked.connect(self.reset_game)
        self.save_btn.clicked.connect(self.save_game)
        self.load_btn.clicked.connect(self.load_game)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.scoreboard_btn.clicked.connect(self.show_scores)
        self.sound_btn.clicked.connect(self.toggle_sound)
        self.pause_btn.clicked.connect(self.toggle_pause)

        # Sounds
        self.flip_sound = QMediaPlayer()
        if os.path.exists(resource_path("flip.mp3")):
            self.flip_sound.setSource(QUrl.fromLocalFile(resource_path("flip.mp3")))
        self.match_sound = QMediaPlayer()
        if os.path.exists(resource_path("flip.mp3")):
            self.match_sound.setSource(QUrl.fromLocalFile(resource_path("match.mp3")))
        self.flip_output = QAudioOutput()
        self.flip_sound.setAudioOutput(self.flip_output)
        self.match_output = QAudioOutput()
        self.match_sound.setAudioOutput(self.match_output)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        # Game variables
        self.game_paused = False

        # Grid layout for cards
        self.grid = QGridLayout()
        self.grid.setSpacing(8)
        main_layout.addLayout(self.grid, 3)

    def prompt_start_settings(self):
        dlg = SettingsDialog()
        if dlg.exec():
            self.difficulty = dlg.get_difficulty()
            self.sound_enabled = dlg.is_sound_enabled()
            self.num_players = dlg.get_num_players()
            self.player1_name = dlg.get_player1_name()
            self.player2_name = dlg.get_player2_name()
            return True
        return False

    def reset_game(self, first_time=False):
        self.timer.stop()
        self.banner.hide_banner()
        if not first_time:
            if not self.prompt_start_settings():
                return
        else:
            if not self.prompt_start_settings():
                sys.exit(0)

        # Board size and card sizes (cards bigger now)
        if self.difficulty == "easy":
            self.rows, self.cols = 4, 4
            self.total_time = 60
            emoji_font_size = 46
            card_size = 100
        elif self.difficulty == "medium":
            self.rows, self.cols = 6, 6
            self.total_time = 120
            emoji_font_size = 30
            card_size = 80
        else:
            self.rows, self.cols = 8, 8
            self.total_time = 160
            emoji_font_size = 24
            card_size = 64

        # Clear grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.buttons = []
        needed = (self.rows * self.cols) // 2
        if needed > len(ALL_EMOJIS):
            QMessageBox.warning(self, "Error", "Not enough unique emojis for board size!")
            sys.exit(1)

        emojis = ALL_EMOJIS[:needed] * 2
        random.shuffle(emojis)
        self.cards = emojis
        self.revealed = []
        self.matched = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                btn = QPushButton(CARD_BACK)
                btn.setFont(QFont("Arial", emoji_font_size))
                btn.setFixedSize(card_size, card_size)
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255,255,255,0.81);
                        border-radius: 14px;
                        color: #2d3558;
                        box-shadow: 0 2px 14px #8bc9ff11;
                        font-weight: bold;
                        font-family: 'Segoe UI Emoji';
                        border: 2.5px solid #b5d0f4;
                    }
                    QPushButton:disabled { background: #e0e4f0; color: #98a0b3;}
                """)
                btn.clicked.connect(self.card_clicked)
                self.grid.addWidget(btn, i, j)
                row.append(btn)
            self.buttons.append(row)
        self.attempts = 0
        self.score_label.setText("🎯 0")
        self.remaining_time = self.total_time
        self.timer_label.setText(f"⏱ {self.remaining_time}")
        self.current_player = 1
        self.scores = {1: 0, 2: 0}
        self.update_turn_label()
        self.enable_cards(True)

        # Set sound state
        self.sound_btn.setText("🔊" if self.sound_enabled else "🔇")
        vol = 1.0 if self.sound_enabled else 0.0
        self.flip_output.setVolume(vol)
        self.match_output.setVolume(vol)

        self.timer.start(1000)
        self.game_paused = False
        self.pause_btn.setText("⏸️")

    def update_turn_label(self):
        if self.num_players == 1:
            self.turn_label.setText(f"👤 {self.player1_name} | Score: {self.scores[1]}")
        else:
            name = self.player1_name if self.current_player == 1 else self.player2_name
            self.turn_label.setText(f"👤 {name} | Score: {self.scores[self.current_player]}")

    def toggle_pause(self):
        if self.game_paused:
            self.timer.start()
            self.pause_btn.setText("⏸️")
            self.enable_cards(True)
            self.banner.hide_banner()
        else:
            self.timer.stop()
            self.pause_btn.setText("▶️")
            self.enable_cards(False)
            self.banner.show_banner("⏸️ PAUSED")
        self.game_paused = not self.game_paused

    def enable_cards(self, enable):
        for row in self.buttons:
            for btn in row:
                if btn.text() == CARD_BACK:
                    btn.setEnabled(enable)

    def card_clicked(self):
        btn = self.sender()
        i, j = self.get_button_index(btn)
        index = i * self.cols + j
        if btn.text() != CARD_BACK or len(self.revealed) >= 2 or self.game_paused:
            return
        btn.setText(self.cards[index])
        if self.sound_enabled:
            self.flip_sound.play()
        self.revealed.append((i, j))
        btn.repaint()
        if len(self.revealed) == 2:
            QTimer.singleShot(480, self.check_match)

    def check_match(self):
        (i1, j1), (i2, j2) = self.revealed
        idx1, idx2 = i1 * self.cols + j1, i2 * self.cols + j2
        match_color = "#17b978"
        if self.cards[idx1] == self.cards[idx2]:
            if self.sound_enabled:
                self.match_sound.play()
            self.buttons[i1][j1].setEnabled(False)
            self.buttons[i2][j2].setEnabled(False)
            self.matched.extend([self.cards[idx1]])
            for i, j in [(i1, j1), (i2, j2)]:
                self.buttons[i][j].setStyleSheet(
                    f"background: {match_color}; color: white; border-radius:14px; border: 3px solid #3cf88e;"
                )
        else:
            QTimer.singleShot(360, lambda: [
                self.buttons[i1][j1].setText(CARD_BACK),
                self.buttons[i2][j2].setText(CARD_BACK)
            ])
        self.scores[self.current_player] += 1
        self.revealed = []
        self.attempts += 1
        self.score_label.setText(f"🎯 {self.attempts}")
        if self.num_players == 2:
            self.current_player = 2 if self.current_player == 1 else 1
        self.update_turn_label()
        if len(self.matched) == (self.rows * self.cols) // 2:
            self.timer.stop()
            self.save_high_score()
            victory_text = ""
            if self.num_players == 1:
                victory_text = f"🎉 YOU WIN!\nAttempts: {self.attempts}, Time left: {self.remaining_time}s"
            else:
                s1, s2 = self.scores[1], self.scores[2]
                if s1 > s2:
                    victory_text = f"🏆 {self.player1_name} wins! {self.scores[1]}:{self.scores[2]}"
                elif s2 > s1:
                    victory_text = f"🏆 {self.player2_name} wins! {self.scores[2]}:{self.scores[1]}"
                else:
                    victory_text = "🤝 It's a tie!"
            self.banner.setStyleSheet("""
                QFrame {background: #27C4A7; border-radius:19px;}
                QLabel {color:#fff; font-size: 22pt; font-weight: bold;}
            """)
            self.banner.show_banner(victory_text)
            self.disable_all_cards()

    def update_timer(self):
        if self.game_paused:
            return
        self.remaining_time -= 1
        self.timer_label.setText(f"⏱ {self.remaining_time}")
        if self.remaining_time <= 0:
            self.timer.stop()
            self.remaining_time = 0
            self.banner.setStyleSheet("""
                QFrame {background: #df2956; border-radius:19px;}
                QLabel {color:#fff; font-size: 22pt; font-weight: bold;}
            """)
            self.banner.show_banner(f"⏰ OUT OF TIME!\nAttempts: {self.attempts}")
            self.reveal_all_cards()
            self.disable_all_cards()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.setText("🔊" if self.sound_enabled else "🔇")
        vol = 1.0 if self.sound_enabled else 0.0
        self.flip_output.setVolume(vol)
        self.match_output.setVolume(vol)

    def get_button_index(self, btn):
        for i, row in enumerate(self.buttons):
            if btn in row:
                return i, row.index(btn)
        return None, None

    def save_game(self):
        data = {
            'cards': self.cards,
            'matched': self.matched,
            'attempts': self.attempts,
            'time': self.remaining_time,
            'current_player': self.current_player,
            'player1': self.player1_name,
            'player2': self.player2_name,
            'num_players': self.num_players,
            'scores': self.scores,
            'difficulty': self.difficulty,
            'theme': self.theme,
            'sound_enabled': self.sound_enabled
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
        self.show_banner_message("💾 Saved", "#1143a9")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.show_banner_message("⚠️ No Save!", "#bd4040")
            return
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
        self.cards = data['cards']
        self.matched = data['matched']
        self.attempts = data['attempts']
        self.remaining_time = data['time']
        self.current_player = data.get('current_player', 1)
        self.player1_name = data.get('player1', "Player 1")
        self.player2_name = data.get('player2', "Player 2")
        self.num_players = data.get('num_players', 1)
        self.scores = {int(k): v for k, v in data.get('scores', {1: 0, 2: 0}).items()}
        self.difficulty = data.get('difficulty', "easy")
        self.theme = data.get('theme', "light")
        self.sound_enabled = data.get('sound_enabled', True)

        # Board sizes and card sizes for load (same larger sizes)
        if self.difficulty == "easy":
            self.rows, self.cols = 4, 4
            emoji_font_size = 46
            card_size = 100
        elif self.difficulty == "medium":
            self.rows, self.cols = 6, 6
            emoji_font_size = 30
            card_size = 80
        else:
            self.rows, self.cols = 8, 8
            emoji_font_size = 24
            card_size = 64

        # Clear grid
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.buttons = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                btn = QPushButton(CARD_BACK)
                btn.setFont(QFont("Arial", emoji_font_size))
                btn.setFixedSize(card_size, card_size)
                btn.clicked.connect(self.card_clicked)
                self.grid.addWidget(btn, i, j)
                row.append(btn)
            self.buttons.append(row)

        for i in range(self.rows):
            for j in range(self.cols):
                idx = i * self.cols + j
                value = self.cards[idx]
                btn = self.buttons[i][j]
                if value in self.matched:
                    btn.setText(value)
                    btn.setEnabled(False)
                else:
                    btn.setText(CARD_BACK)
                    btn.setEnabled(True)

        self.score_label.setText(f"🎯 {self.attempts}")
        self.timer_label.setText(f"⏱ {self.remaining_time}")
        self.update_turn_label()
        self.timer.start(1000)
        self.enable_cards(True)
        self.sound_btn.setText("🔊" if self.sound_enabled else "🔇")
        vol = 1.0 if self.sound_enabled else 0.0
        self.flip_output.setVolume(vol)
        self.match_output.setVolume(vol)
        self.banner.hide_banner()
        self.pause_btn.setText("⏸️")
        self.game_paused = False

    def toggle_theme(self, theme=None):
        if theme:
            self.theme = theme.lower()
        else:
            self.theme = "dark" if self.theme == "light" else "light"
        if self.theme == "dark":
            bg = "#222230"
            card = "#253550"
            txt = "#eef"
            accent = "#ffc887"
        else:
            bg = "#ecf1fa"
            card = "#fff"
            txt = "#16294f"
            accent = "#90caf9"
        self.setStyleSheet(f"""
        QWidget {{
            background: {bg};
            color: {txt};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QPushButton {{
            background: {card};
            border-radius: 20px;
            font-size: 2.2vw;
            color: {txt};
            border: 1.5px solid {accent};
            font-family:'Segoe UI Emoji';
        }}
        QPushButton:disabled {{ background: #e6e6ec; color: #b5b5c6;}}
        QLabel {{font-size: 1.13vw;}}
        """)

    def save_high_score(self):
        if self.num_players == 1:
            entry = f"{self.player1_name}: Attempts {self.attempts}, Time Left {self.remaining_time}"
        else:
            entry = f"{self.player1_name}: {self.scores[1]} | {self.player2_name}: {self.scores[2]} | Attempts {self.attempts}, Time Left {self.remaining_time}"
        with open(HIGHSCORE_FILE, 'a') as f:
            f.write(entry + "\n")

    def show_scores(self):
        if not os.path.exists(HIGHSCORE_FILE):
            self.show_banner_message("📊 No Scores!", "#1143a9")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("🏆 High Scores")
        layout = QVBoxLayout()
        table = QTableWidget()
        with open(HIGHSCORE_FILE) as f:
            lines = f.readlines()
        table.setRowCount(len(lines))
        if lines and "|" in lines[0]:
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Player 1", "Score 1", "Player 2 & Score 2", "Attempts & Time"])
            for i, line in enumerate(lines):
                parts = line.strip().split('|')
                for j, val in enumerate(parts):
                    table.setItem(i, j, QTableWidgetItem(val.strip()))
        else:
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Name/Score", "Attempts/Time"])
            for i, line in enumerate(lines):
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    table.setItem(i, 0, QTableWidgetItem(parts[0].strip()))
                    table.setItem(i, 1, QTableWidgetItem(parts[1].strip()))
                else:
                    table.setItem(i, 0, QTableWidgetItem(""))
                    table.setItem(i, 1, QTableWidgetItem(line.strip()))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.resize(660, 340)
        dialog.exec()

    def closeEvent(self, event):
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("Save Game?")
        msgbox.setText("Do you want to save before exiting?")
        msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msgbox.setDefaultButton(QMessageBox.Yes)
        msgbox.setStyleSheet("""
        QMessageBox { font-size: 13pt; font-family: 'Segoe UI'; }
        QPushButton { font-size: 13pt; }
        """)
        result = msgbox.exec()
        if result == QMessageBox.Yes:
            self.save_game()
            event.accept()
        elif result == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

    def reveal_all_cards(self):
        for i in range(self.rows):
            for j in range(self.cols):
                idx = i * self.cols + j
                self.buttons[i][j].setText(self.cards[idx])
                self.buttons[i][j].setEnabled(False)

    def disable_all_cards(self):
        for row in self.buttons:
            for btn in row:
                btn.setEnabled(False)

    def show_banner_message(self, text, color="#4773d6"):
        self.banner.setStyleSheet(
            f"QFrame{{background:{color};border-radius:18px;}} QLabel{{color:white;font-size:24pt;font-weight:700;}}"
        )
        self.banner.show_banner(text)
        QTimer.singleShot(1450, self.banner.hide_banner)
  
def main():
    app = QApplication(sys.argv)
    game = Memory_Game()
    game.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
