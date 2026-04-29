# Mini Game Hub
This is Vedansh(25b0950) and Majid's(25b1001) course project for CS108 (Software Systems Lab) taken in Spring 2026.

It is a 2-player game hub using Bash for authentication and Python (Pygame) for gameplay. Users log in, play games via GUI, and results are shown onto a leaderboard.

The games in the hub are:
+ Tic-Tac-Toe
+ Othello
+ Connect 4
+ Game 4: TBD

Run `bash main.sh` for user authentication.

Once both players are authenticated, main.sh calls game.py with both usernames as command-line arguments.

`python3 game.py <username1> <username2>`

The game window appears and the players can start.
