
# Jet Set Brian

This is a fun Python-based platformer game that uses `pygame`. In the game, the player can collect items, avoid enemies, and navigate through different maps. If the player loses all lives, they can restart by pressing any key.

## Prerequisites

- Python 3.8 or higher
- `pip` (Python's package installer)

## Setup Instructions

Follow the instructions below to set up and run the game:

### 1. Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/briscanlon/jet-set-brian.git
```

### 2. Navigate to the Project Directory

Change into the project directory where the `app.py` file and `requirements.txt` are located:

```bash
cd jet-set-brian
```

### 3. Install Required Dependencies

Make sure you have `pip` installed. If not, [install `pip`](https://pip.pypa.io/en/stable/installation/) first.

Next, install all the required dependencies from the `requirements.txt` file using the following command:

```bash
pip install -r requirements.txt
```

This will install `pygame` and any other necessary libraries for the game.

### 4. Run the Game

Once the dependencies are installed, you can run the game using the following command:

```bash
python app.py
```

### 5. Controls

- **Arrow Keys**: Use the left and right arrow keys to move your character.
- **Space Bar**: Press the space bar to jump.
- **Restart**: If you lose all lives or complete the game, press any key to restart.

### 6. Game Objective

- **Collectibles**: Collect all the yellow squares (collectibles) scattered across the platforms.
- **Avoid Enemies**: Blue squares are enemies. Avoid them or you will lose a life.
- **Lives**: You start with 3 lives. If you collide with an enemy, you lose a life.
- **Game Over**: Once all lives are lost, a "Game Over" screen will appear. Press any key to restart.

---

### 7. Troubleshooting

If you encounter issues running the game, make sure that:
- Python 3.x is installed on your machine.
- You are using a terminal with the correct path to `app.py` and have installed the required libraries.

### License

This project is licensed under the MIT License.
