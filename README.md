## Reversi Project

From Wiki, here are the rules of Reversi

> Two players compete, using 64 identical game pieces ("disks") that are light on one side and dark on the other. Each player chooses one color to use throughout the game. Players take turns placing one disk on an empty square, with their assigned color facing up. After a play is made, any disks of the opponent's color that lie in a straight line bounded by the one just played and another one in the current player's color are turned over. When all playable empty squares are filled, the player with more disks showing in their own color wins the game.

Programs

1. reversi.py - it contains code for Reversi in python that I have picked up from http://inventwithpython.com/chapter15.html.
2. supervisor.py - this is the Supervisor used to play two UCT-style Reversi programs against each other

   Provided Players

   1. computer.py
   2. random_player.py

   Players (implemented programs) 3. ordinary.py 4. improved.py

Now to run the superviser.py, you need to execute -

`python supervisor.py <player1> <player2> <timeout_threshold> <verbose>`
or
`python3 supervisor.py <player1> <player2> <timeout_threshold> <verbose>`

- player1 (required)- represents the program running player 1. eg. with the current file you can have player1=computer or player1=random.
- player2 (required)- represents the program running player 2.
- timeout_threshold  (optional) - number of seconds to wait for one move. Default set to 1.
- verbose (optional) - whether to display the board after each move or not. Default set to 1.

i.e.
`python supervisor.py computer ordinary`
