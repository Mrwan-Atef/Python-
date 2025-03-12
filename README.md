# Domino Game

## Overview
This is a GUI-based Domino game where a player competes against a computer opponent. The game follows traditional Domino rules with a scoring system where the first player to reach **101 points** wins. The game is built using **Python** and **Tkinter** for the user interface.

## Features
- **Player vs Computer Gameplay**
- **Graphical User Interface (GUI)** using Tkinter
- **Score Keeping** (game ends when a player reaches 101 points)
- **Automatic Tile Drawing and Placement**
- **New Round System** (resets game state while keeping scores)

## Installation
To run the game on your local machine, follow these steps:

### Prerequisites
Ensure you have Python installed (version 3.6 or higher). If you don’t have Python, download it from [python.org](https://www.python.org/).

### Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/domino-game.git
   cd domino-game
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the game:
   ```sh
   python main.py
   ```

## How to Play
1. **Starting the Game**:
   - The player and computer are each dealt **7 random tiles**.
   - The player makes the first move if they have the **highest double tile** (e.g., 6-6).
   
2. **Game Rules**:
   - Players take turns placing tiles that match numbers at either end of the chain.
   - If a player has no valid move, they must **draw a tile** until they find a playable one.
   - The round ends when a player **places all their tiles** or when no valid moves remain.
   
3. **Scoring System**:
   - At the end of each round, the **losing player’s remaining tile values** are summed and added to the winner’s score.
   - The first player to reach **101 points wins** the game.
   
4. **Starting a New Round**:
   - If no player has reached 101 points, the game resets while **keeping the scores**.
   - If a player reaches 101 points, a **Game Over** message is displayed, and the game ends.


```

## Future Enhancements
- Add multiplayer mode
- Implement AI difficulty levels
- Improve tile graphics and animations

## Contributions
Pull requests are welcome! If you’d like to contribute, please fork the repository and submit a PR.



