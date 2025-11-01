# Python Text-Based RPG

This is a simple text-based RPG game written in Python.

## About the Project

This game is a classic-style text-based RPG where you can create a character, explore a world, fight enemies, and collect loot. The game features a save/load system, a shop, and random events.

## Getting Started

To run the game, you need to have Python 3 installed.

1.  Clone the repository:
    ```bash
    git clone https://github.com/YOUR-USERNAME/Python_text_RPG_practice.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd Python_text_RPG_practice
    ```
3.  Run the game:
    ```bash
    python3 Main.py
    ```

## How to Play

*   **Character Creation:** When you start a new game, you will be asked to enter a name for your character.
*   **Exploring the World:** The game will present you with a description of your surroundings and a list of possible actions. You can move between rooms, search for items, and interact with objects.
*   **Combat:** When you encounter an enemy, you will enter into a turn-based combat. You can choose to attack, defend, or use items.
*   **Inventory:** You can view your inventory at any time to see the items you have collected by choosing the 'Inventory' option.
*   **Shop:** You can visit the shop to buy and sell items.
*   **Saving and Loading:** You can save your progress at any time and load it later.

## Project Structure

The project is organized into the following files:

*   `Main.py`: The main entry point of the game.
*   `Game.py`: Contains the main game loop and game logic.
*   `Player.py`: Defines the player character.
*   `World.py`: Defines the game world and its rooms.
*   `Room.py`: Defines a single room in the game world.
*   `Enemy.py`: Defines the enemies that the player can encounter.
*   `Weapon.py`: Defines the weapons that the player can use.
*   `Armour.py`: Defines the armour that the player can wear.
*   `Shop.py`: Defines the shop where the player can buy and sell items.
*   `RandomEvent.py`: Defines the random events that can occur in the game.
*   `tests/`: Contains the unit tests for the project.
