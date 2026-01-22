# Lost but Found - Game Dev


**Lost But Found** is a 2D interactive game developed using Python and the Pygame framework. The game challenges players to manage items, interact with various NPCs, and navigate through a dynamic environment while dealing with game elements like the police and thieves.



## Design Thinking


<img width="2400" height="1350" alt="image" src="https://github.com/user-attachments/assets/05c6b80c-5544-4697-960b-22305bc7bea5" />


***Entity System:***   Includes diverse characters such as customers, police officers, and thieves, each with unique behaviors.


***Item Management:***   A system to handle various in-game items and inventory mechanics.


***State Machine:***   Robust game state management including Menu, Gameplay, and GameOver states.


***UI & HUD:***   Interactive buttons, popups, and a Head-Up Display (HUD) for a seamless user experience.


***Multimedia Integration:***   Supports custom fonts, background music (BGM), and sound effects (SFX).



## Tech Stack

***Language:*** Python 


***Library:*** Pygame 


***Design Patterns:*** State Pattern for game flow, Manager classes for system handling.

## Repository Structure
```Plaintext

.
├── assets/             # Game assets (images, sounds, fonts) 
├── config/             # Global settings and configurations
├── game/
│   ├── entities/       # Character and item classes (Police, Thief, Customer, etc.)
│   ├── managers/       # Inventory and game logic managers
│   ├── states/         # Game state definitions (Menu, Gameplay, Game Over) 
│   └── ui/             # UI components (Buttons, HUD, Popups) 
├── test/               # Unit tests for gameplay logic
└── start.py            # Main entry point to launch the game
```

## How to Run
Prerequisites: Ensure you have Python installed.

Install Dependencies:

```bash
pip install pygame
```

Launch Game:

```Bash
python start.py
```

## Inspiration & References

***This project was inspired by a famous game Lost but Found on Steam.*** https://store.steampowered.com/app/3204250/_/

It marks my journey in learning Python and game design. By mimicking a popular game on Steam, I've moved beyond basic syntax to design a complex NPC interaction system and a scalable backend, bridging the gap between beginner tutorials and academic-level software architecture.
