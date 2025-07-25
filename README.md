# 🧠 Memory Game

## 📜 Description
### Memory Game is a colorful, emoji-based card-matching game implemented in Python using the PySide6 GUI framework. The game supports single-player and two-player modes, with customizable difficulty settings. Challenge yourself or a friend to match all pairs of cards as quickly as possible before the timer runs out. Features include sound effects, save/load functionality, a high score board, and a polished, glassy interface with intuitive controls.

---

## 🚀 Features
### 🎮 Game Modes:
- ✅ Single Player (vs self/time)
- ✅ Two Players (local multiplayer)
  
### 🎯 Gameplay
- Responsive grid of cards with emoji
- Timer countdown and scoring with attempts
- Turn indicators and score tracking for both players
- Smooth card flip animations and matching logic
- Pause/resume game and toggle sound effects

### ⚙️ Game Settings
- Easy / Medium / Hard difficulty (affects board size and timer)
- Player name inputs
- Sound On/Off toggle
- Save and load games from JSON file
- Persistent high score list tracking attempts and remaining time

### 🌈 User Interface
- Clean, modern glassy theme with light/dark mode support
- Emoji-based card backs and content
- Animated banners for win, loss, and pause states
- Toggleable game menu with icons for Restart, Save, Load, Theme change, Scores, Sound, and Pause

---

## 💻 Installation
## 1️⃣ Clone the repository:
```
✅ 1. Requirements:
- Python 3.7+
- PySide6
Install via pip:
```bash
pip install PySide6
---

✅ 2. Download the Project:
- Clone this repository using Git:
```bash
git clone https://github.com/anujadevelops/Memory-Game.git
```
## 2️⃣ Navigate to the project directory:
```
cd Memory-Game
```
## 3️⃣ Run the application:
```
Run using the command line:
python Memory_Game.py

```
## 4️⃣ Build .exe (Optional):
#### Open your command prompt or terminal and run:
```
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "cards.jpg;." --add-data "flip.mp3;." --add-data "match.mp3;." Memory_Game.py
```

## 🛠️ Features in Detail
The Memory Game offers the following core features:

---
### ✅ Gameplay Mechanics:
- Card grid layout scales with difficulty: Easy (4×4), Medium (6×6), Hard (8×8)
- Track attempts and remaining time
- Switch turns and maintain individual scores
- Game pause/resume with banner
- Highlight matched cards with color and disable them
- Reveal all cards on timeout

### ✅ User Interface Components:
- Top bar with timer, score, turn indicators, and menu toggle
- Toggled control menu with icon-labeled buttons
- Banners animated with bounce effect for game status messages
- Dialogs for settings and high scores with modern styling
  
### ✅ Sound Effects:
- Flip card
- Match found
- Toggle sound on/off from menu

### ✅ Game Persistence:
- Save/load current game state (cards, scores, timer, etc.)
- High score file appends winners' info for later review
- Confirm save on exit prompt

## 🤝 Contributing
### 1️⃣ Fork the repository.
### 2️⃣ Create a new branch (e.g., `git checkout -b feature-branch`).
### 3️⃣ Make your changes and thoroughly test them.
### 4️⃣ Commit your changes (e.g., `git commit -am "Add: Description of new feature or fix"`).
### 5️⃣ Push to your fork (e.g., `git push origin feature-branch`).
### 6️⃣ Submit a pull request describing your changes and the purpose of the contribution.

## 💡 Feedback
### If you have suggestions or encounter any issues, feel free to open an issue or pull request for bugs, improvements, or suggestions! on the repository or reach out directly.

## ⚠️ Limitations
### ❌ Local multiplayer only (no online mode)
### ❌ Not optimized for mobile/touch devices
### ❌ No AI opponent yet
### ❌ Sound effects require accompanying mp3 files (flip.mp3 and match.mp3) in the project folder

---
## Thank you for checking out the Memory Game! Enjoy matching those pairs 🧠🎴🎉
